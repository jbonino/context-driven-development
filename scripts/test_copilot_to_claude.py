"""Tests for copilot_to_claude.py. Run: uv run --with pytest pytest scripts/"""
import gzip
import importlib.util
import json
import os

HERE = os.path.dirname(os.path.abspath(__file__))
spec = importlib.util.spec_from_file_location("c2c", os.path.join(HERE, "copilot_to_claude.py"))
c2c = importlib.util.module_from_spec(spec)
spec.loader.exec_module(c2c)


def event(kind, data, stamp="2026-11-17T18:00:00.000Z", **extra):
    return {"type": kind, "data": data, "timestamp": stamp, **extra}


def session(state, sid, cwd, events):
    path = state / sid
    path.mkdir(parents=True)
    (path / "workspace.yaml").write_text(f"id: {sid}\ncwd: {cwd}\n")
    (path / "events.jsonl").write_text("".join(json.dumps(e) + "\n" for e in events))


def test_branch_from_worktree_cwd(tmp_path):
    root = str(tmp_path)
    assert c2c.branch_for(f"{root}/.claude/worktrees/001-my-service-42", root) == "001-my-service-42"
    assert c2c.branch_for(f"{root}/.claude/worktrees/001-x/docs", root) == "001-x"
    assert c2c.branch_for("/elsewhere", root) is None


def test_tool_call_and_result_round_trip():
    entries = c2c.convert([
        event("assistant.message", {"messageId": "m1", "model": "claude-opus-5.5", "content": "Reading.",
                                    "toolRequests": [{"toolCallId": "t1", "name": "view",
                                                      "arguments": {"path": "/r/docs/architecture.md"}}]}),
        event("tool.execution_complete", {"toolCallId": "t1", "success": False,
                                          "error": {"message": "no such file"}}),
    ], "main")[None]
    use = entries[0]["message"]["content"][1]
    assert use == {"type": "tool_use", "id": "t1", "name": "Read",
                   "input": {"path": "/r/docs/architecture.md", "file_path": "/r/docs/architecture.md"}}
    result = entries[1]["message"]["content"][0]
    assert entries[1]["type"] == "user"
    assert result["tool_use_id"] == "t1" and result["is_error"] is True
    assert "no such file" in result["content"]
    assert all(e["gitBranch"] == "main" for e in entries)


def test_usage_maps_to_claude_fields():
    entries = c2c.convert([event("session.usage_record", {"usage": {
        "model": "claude-sonnet-5.5", "inputTokens": 1000, "outputTokens": 50,
        "cacheReadTokens": 600, "cacheWriteTokens": 300, "apiCallId": "msg_1"}})], "main")[None]
    message = entries[0]["message"]
    assert message["id"] == "msg_1" and message["model"] == "claude-sonnet-5.5"
    assert message["usage"] == {"input_tokens": 100, "output_tokens": 50,
                                "cache_read_input_tokens": 600, "cache_creation_input_tokens": 300}


def test_only_this_repos_sessions_are_saved(tmp_path):
    root, state, out = tmp_path / "repo", tmp_path / "state", tmp_path / "raw"
    root.mkdir()
    hello = [event("user.message", {"content": "hello"})]
    session(state, "aaa", f"{root}/.claude/worktrees/002-x", hello)
    session(state, "bbb", "/somewhere/else", hello)
    assert c2c.save_all(str(state), str(root), str(out)) == 1
    [saved] = os.listdir(out)
    assert saved == "2026-11-17-aaa.jsonl.gz"
    with gzip.open(out / saved, "rt") as handle:
        line = json.loads(handle.readline())
    assert line["gitBranch"] == "002-x" and line["message"]["content"] == "hello"
