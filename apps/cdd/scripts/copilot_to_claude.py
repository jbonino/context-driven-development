#!/usr/bin/env -S uv run --script
# /// script
# requires-python = ">=3.13"
# dependencies = []
# ///
"""Save this repo's Copilot sessions as Claude Code transcripts for mine-transcripts.py.

A session counts when its workspace.yaml ``cwd`` is the repo root or a worktree
under ``.claude/worktrees/<name>``. Its ``gitBranch`` is ``<name>``, or for the
root the branch checked out there now, else ``main``. Events from a subagent,
those with an ``agentId``, go to ``<session>/agent-<id>.jsonl.gz``.

| Copilot event | Claude Code line |
|---|---|
| user.message | user, content as typed |
| assistant.message | assistant, text plus a tool_use per toolRequest |
| tool.execution_complete | user, one tool_result, is_error when not success |
| skill.invoked | user, "Base directory for this skill: skills/<name>" plus the body |
| session.usage_record | assistant, message.usage keyed by apiCallId |

Usage: Copilot's inputTokens includes the cache, so input_tokens is
inputTokens - cacheReadTokens - cacheWriteTokens. cacheReadTokens maps to
cache_read_input_tokens, cacheWriteTokens to cache_creation_input_tokens,
outputTokens to output_tokens. Reasoning tokens sit inside outputTokens.

Tool names map to Claude's where the miner reads them, and ``path`` is copied
to ``file_path``. Usage: copilot_to_claude.py <repo root> <out dir>
"""
import glob
import gzip
import json
import os
import re
import subprocess
import sys

TOOLS = {"bash": "Bash", "view": "Read", "edit": "Edit", "create": "Write"}
BASE64 = re.compile(r'"data": ?"[A-Za-z0-9+/=]{200,}"')


def branch_for(cwd, root):
    cwd, root = os.path.realpath(cwd), os.path.realpath(root)
    trees = os.path.join(root, ".claude", "worktrees") + os.sep
    if cwd.startswith(trees):
        return cwd[len(trees):].split(os.sep)[0]
    if cwd != root:
        return None
    found = subprocess.run(["git", "-C", cwd, "branch", "--show-current"],
                           capture_output=True, text=True)
    return found.stdout.strip() or "main"


def line(kind, stamp, branch, message, **extra):
    return {"type": kind, "timestamp": stamp, "gitBranch": branch, "message": message, **extra}


def convert(events, branch):
    """Copilot events → Claude Code lines, keyed by agentId (None for the main agent)."""
    out, effort = {}, None
    for e in events:
        data, stamp = e.get("data") or {}, e.get("timestamp")
        kind, entry = e.get("type"), None
        if kind in ("session.start", "session.resume", "session.model_change"):
            effort = data.get("reasoningEffort") or effort
        elif kind == "user.message":
            entry = line("user", stamp, branch, {"role": "user", "content": data.get("content", "")})
        elif kind == "assistant.message":
            blocks = [{"type": "text", "text": data["content"]}] if data.get("content") else []
            for call in data.get("toolRequests") or []:
                args = dict(call.get("arguments") or {})
                if "path" in args:
                    args["file_path"] = args["path"]
                blocks.append({"type": "tool_use", "id": call.get("toolCallId"),
                               "name": TOOLS.get(call.get("name"), call.get("name")), "input": args})
            entry = line("assistant", stamp, branch, {"role": "assistant", "model": data.get("model"),
                                                      "content": blocks}, effort=effort)
        elif kind == "tool.execution_complete":
            result = (data.get("result") or {}).get("content") or (data.get("error") or {}).get("message", "")
            entry = line("user", stamp, branch, {"role": "user", "content": [{
                "type": "tool_result", "tool_use_id": data.get("toolCallId"),
                "content": result, "is_error": not data.get("success", True)}]})
        elif kind == "skill.invoked":
            text = f"Base directory for this skill: skills/{data.get('name')}\n\n{data.get('content', '')}"
            entry = line("user", stamp, branch, {"role": "user", "content": [{"type": "text", "text": text}]},
                         isMeta=True)
        elif kind == "session.usage_record":
            u = data.get("usage") or {}
            read, write = u.get("cacheReadTokens", 0), u.get("cacheWriteTokens", 0)
            entry = line("assistant", stamp, branch, {
                "role": "assistant", "id": u.get("apiCallId"), "model": u.get("model"), "content": [],
                "usage": {"input_tokens": max(u.get("inputTokens", 0) - read - write, 0),
                          "output_tokens": u.get("outputTokens", 0),
                          "cache_read_input_tokens": read, "cache_creation_input_tokens": write}},
                effort=u.get("reasoningEffort") or effort)
        if entry:
            out.setdefault(e.get("agentId"), []).append(entry)
    return out


def cwd_of(folder):
    try:
        with open(os.path.join(folder, "workspace.yaml"), encoding="utf-8") as handle:
            return next((l.split(":", 1)[1].strip().strip("'\"") for l in handle if l.startswith("cwd:")), None)
    except OSError:
        return None


def write(path, entries, newer_than):
    if os.path.exists(path) and os.path.getmtime(path) > newer_than:
        return
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with gzip.open(path, "wt", encoding="utf-8") as handle:
        for entry in entries:
            handle.write(BASE64.sub('"data":"<image>"', json.dumps(entry)) + "\n")


def save_all(state, root, out):
    """Save each matching session under ``state`` into ``out``. Returns the count."""
    count = 0
    for folder in sorted(glob.glob(os.path.join(state, "*", ""))):
        cwd = cwd_of(folder)
        source = os.path.join(folder, "events.jsonl")
        branch = cwd and os.path.exists(source) and branch_for(cwd, root)
        if not branch:
            continue
        with open(source, encoding="utf-8") as handle:
            events = [json.loads(l) for l in handle if l.strip()]
        stamp = next((e["timestamp"] for e in events if e.get("timestamp")), "")
        name = f"{stamp[:10] or 'undated'}-{os.path.basename(folder.rstrip(os.sep))}"
        changed = os.path.getmtime(source)
        for agent, entries in convert(events, branch).items():
            path = (os.path.join(out, f"{name}.jsonl.gz") if agent is None
                    else os.path.join(out, name, f"agent-{agent}.jsonl.gz"))
            write(path, entries, changed)
        count += 1
    return count


if __name__ == "__main__":
    root, out = sys.argv[1], sys.argv[2]
    state = os.path.expanduser("~/.copilot/session-state")
    print(f"{save_all(state, root, out)} Copilot sessions in {os.path.relpath(out, root)}")
