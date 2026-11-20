#!/usr/bin/env -S uv run --script
# /// script
# requires-python = ">=3.13"
# dependencies = []
# ///
"""Mine one phase's saved sessions for the phase-close retro.

Maps each transcript line to a ticket by its ``gitBranch`` and reports, per
ticket: cost, time sinks, files read and never edited, slow commands, and
scratch scripts written in two or more tickets. Then, across the phase:
context past 150k, what each skill carries, design-doc reads against edits,
estimated against actual, each model and effort beside its cost and rework,
skill steps skipped, the owner's corrections and waits, redesigns, split
tickets, the owner's retro notes, text repeated across the workflow's files,
and the order of acts, which shows steps a skill makes run twice or out of
turn. Usage:

    uv run cdd mine 1 [--top 10]

Run uv run cdd save first. It saves Claude Code and Copilot sessions.
"""
import argparse
import base64
import glob
import gzip
import json
import os
import re
import struct
import subprocess
import sys
from collections import defaultdict
from datetime import datetime

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "../../../forms"))
import cdd  # noqa: E402

ROOT = cdd.ROOT
RAW = os.path.join(ROOT, cdd.FOLDERS["raw"])
PLANNED = [cdd.DOCS[d] for d in ("foundations", "design_document", "architecture", "product_roadmap")]
RETRO = cdd.folder("retro")

before_the_move = cdd.before_the_move

# Cache reads bill at 0.1x input, cache writes at 1.25x, output at 5x.
WEIGHTS = {"input_tokens": 1.0, "cache_creation_input_tokens": 1.25,
           "cache_read_input_tokens": 0.1, "output_tokens": 5.0}

IMAGE_FALLBACK = 1600  # a capped image lands near here when dimensions are unreadable
DOC_FALLBACK = 3000    # a PDF page costs roughly this; most results carry one


def tokens(text):
    """Chars/4, the usual rough estimate for text."""
    return len(text) // 4


def jpeg_dimensions(raw):
    """Scan JPEG segments for a start-of-frame marker."""
    i = 2
    while i + 9 < len(raw):
        if raw[i] != 0xFF:
            i += 1
            continue
        marker = raw[i + 1]
        if 0xC0 <= marker <= 0xCF and marker not in (0xC4, 0xC8, 0xCC):
            height, width = struct.unpack(">HH", raw[i + 5:i + 9])
            return width, height
        if marker in (0xD8, 0x01) or 0xD0 <= marker <= 0xD7:
            i += 2
            continue
        i += 2 + struct.unpack(">H", raw[i + 2:i + 4])[0]
    return None


def image_tokens(data):
    """(w x h) / 750 after the long edge is capped at 1568.

    Measuring the base64 payload instead over-reports by 25-50x, which is
    the difference between "that screenshot was the largest thing you
    read" and the truth. Images arrive as JPEG even when the file on disk
    was a PNG, so both are read.
    """
    try:
        chunk = data[:8000]
        raw = base64.b64decode(chunk[:len(chunk) // 4 * 4])
        if raw[:8] == b"\x89PNG\r\n\x1a\n":
            size = struct.unpack(">II", raw[16:24])
        elif raw[:2] == b"\xff\xd8":
            size = jpeg_dimensions(raw)
        else:
            size = None
    except Exception:
        size = None
    if not size or not all(size):
        return IMAGE_FALLBACK
    width, height = size
    longest = max(width, height)
    if longest > 1568:
        width = int(width * 1568 / longest)
        height = int(height * 1568 / longest)
    return int(width * height / 750)


def result_tokens(block):
    """Size the tool result the model actually receives.

    Subagent transcripts carry no `toolUseResult` key, so the content
    block is both the honest measure and the only portable one.
    """
    content = block.get("content")
    if content is None:
        return 0
    if isinstance(content, str):
        return tokens(content)
    if not isinstance(content, list):
        return tokens(json.dumps(content))
    total = 0
    for piece in content:
        if not isinstance(piece, dict):
            total += tokens(str(piece))
        elif piece.get("type") == "text":
            total += tokens(piece.get("text", ""))
        elif piece.get("type") == "image":
            total += image_tokens(piece.get("source", {}).get("data", ""))
        elif piece.get("type") == "document":
            total += DOC_FALLBACK
        else:
            total += tokens(json.dumps(piece))
    return total


SLOW_SECONDS = 60
BIG_CONTEXT = 150_000
DOCS = re.compile("/(" + "|".join(re.escape(p) for p in PLANNED + [before_the_move(p) for p in PLANNED]) + "|(?:"
                  + "|".join(re.escape(f) for d in ("release-playbook", "deferred")
                             for f in (cdd.folder(d), before_the_move(cdd.folder(d)))) + r")[^/]+\.md)$")
ACTS = [("server-", r"\bkill\b|pkill"),
        ("shot", r"shoo?ts?\.(js|sh)|screenshot"), ("test", r"pytest|vitest|pnpm test|turbo test"),
        ("deploy", r"deploy"),
        ("commit", r"git commit"), ("rebase", r"git rebase|git merge"),
        ("sleep", r"\bsleep\b"), ("curl", r"\bcurl\b")]
SKILL_LOAD = re.compile(r"Base directory for this skill: \S*/([^/\s]+)")
SCRATCH = re.compile(r"(scratch|/tmp/|_scratch)[^\s\"']*\.(py|sh|js)$")
# Each skill a parent tells the agent to load, by the name its base directory carries.
EXPECTED = {"working-a-ticket": ["using-git-worktrees", "brainstorming", "test-driven-development",
                                 "writing-a-retro-entry", "editing-prose", "requesting-code-review"],
            "reviewing-a-ticket": ["requesting-code-review", "merging-to-main"]}
CORRECTION = re.compile(r"^\s*(no\b|nope|wrong|that's not|that isn't|not what|actually\b|don't|do not"
                        r"|stop\b|why did|why are|why is|you (skipped|missed|forgot|didn't))", re.I)
NOT_TYPED = ("Base directory", "<local-command", "<command-", "<system-reminder", "<task-notification",
             "[Request interrupted", "Caveat:")
CACHE_MISS = 20_000  # a request that writes this much cache and reads none started cold
RETRY = 3            # the same command this many times running is a loop


def ticket_of(branch, phase):
    """`004-056d-x` → `004-056d`. A branch naming only the phase, like `001-my-service-42`, → `phase 001`."""
    if not branch:
        return None
    found = re.search(rf"\b({phase}-\d{{3}}[a-z]?)", branch)
    if found:
        return found.group(1)
    if phase in branch or branch.startswith(f"phase-{int(phase)}"):
        return f"phase {phase}"
    return None


def when(entry):
    stamp = entry.get("timestamp")
    return datetime.fromisoformat(stamp.replace("Z", "+00:00")) if stamp else None


def lines(path):
    with gzip.open(path, "rt", encoding="utf-8") as handle:
        for line in handle:
            try:
                yield json.loads(line)
            except ValueError:
                continue


def new_stats():
    return {"sessions": set(), "requests": {}, "seconds": 0.0,
            "tools": defaultdict(lambda: [0, 0]), "reads": defaultdict(int),
            "edits": set(), "slow": [], "scratch": set(),
            "skills": defaultdict(lambda: [0, 0]), "docs": defaultdict(lambda: [0, 0]),
            "acts": [], "refused": defaultdict(int),
            "models": defaultdict(int), "efforts": defaultdict(int), "agent_requests": {},
            "prompts": 0, "corrections": [], "interrupts": 0, "denied": defaultdict(int),
            "waits": [], "clears": 0, "compactions": 0, "cache_misses": 0,
            "bash": [], "green_at": None}


def family(model):
    """`claude-sonnet-5-5` → `sonnet`."""
    found = re.search(r"(opus|sonnet|haiku|fable)", model or "")
    return found.group(1) if found else None


def typed_text(entry):
    """What the owner typed, or None for tool results, skill bodies and harness notes."""
    if entry.get("type") != "user" or entry.get("isMeta") or entry.get("isCompactSummary"):
        return None
    content = (entry.get("message") or {}).get("content")
    if isinstance(content, list):
        if any(isinstance(b, dict) and b.get("type") == "tool_result" for b in content):
            return None
        content = " ".join(b.get("text", "") for b in content if isinstance(b, dict))
    if not isinstance(content, str) or not content.strip():
        return None
    if content.lstrip().startswith(NOT_TYPED):
        return None
    return content


def majority(counts):
    return max(counts, key=counts.get) if counts else None


def mine(phase):
    stats = defaultdict(new_stats)
    paths = glob.glob(os.path.join(RAW, "*.jsonl.gz")) + glob.glob(
        os.path.join(RAW, "*", "*.jsonl.gz"))
    for path in paths:
        pending = {}  # tool_use id → (ticket, name, input, started)
        last = {}     # ticket → previous timestamp, for active time
        # A session loads skills on main before it moves to the ticket's worktree.
        # Lines with no ticket go to the first ticket the session reaches.
        fallback = next((t for e in lines(path)
                         if (t := ticket_of(e.get("gitBranch"), phase))), None)
        branch = None
        loaded = {}   # skill → tokens, carried by every later request
        agent = os.path.dirname(path) != RAW  # a subagent's transcript sits in its session's folder
        replied = None  # when the agent last answered, to time the owner's wait
        for entry in lines(path):
            branch = entry.get("gitBranch") or branch
            ticket = ticket_of(branch, phase) or fallback
            if not ticket:
                continue
            s = stats[ticket]
            s["sessions"].add(os.path.basename(path).split(".")[0][:19])
            moment = when(entry)
            if moment and ticket in last:
                gap = (moment - last[ticket]).total_seconds()
                s["seconds"] += min(max(gap, 0), 300)  # idle past 5 min isn't work
            if moment:
                last[ticket] = moment
            message = entry.get("message") or {}
            if message.get("usage"):
                key = entry.get("requestId") or message.get("id") or len(s["requests"])
                if key not in s["requests"]:
                    for skill, size in loaded.items():
                        s["skills"][skill][1] += size
                    usage = message["usage"]
                    if not usage.get("cache_read_input_tokens") and \
                            usage.get("cache_creation_input_tokens", 0) > CACHE_MISS:
                        s["cache_misses"] += 1
                    if agent:
                        s["agent_requests"][key] = usage
                    elif family(message.get("model")):
                        s["models"][family(message["model"])] += 1
                        s["efforts"][entry.get("effort") or "unset"] += 1
                s["requests"][key] = message["usage"]
            if not agent:
                if entry.get("type") == "assistant" and moment:
                    replied = moment
                if entry.get("isCompactSummary") or entry.get("subtype") == "compact_boundary":
                    s["compactions"] += 1
                if entry.get("toolDenialKind"):
                    s["denied"][entry["toolDenialKind"]] += 1
                raw = json.dumps(message.get("content", ""))
                said = message.get("content")
                said = said if isinstance(said, str) else " ".join(
                    b.get("text", "") for b in said or [] if isinstance(b, dict) and b.get("type") == "text")
                if entry.get("type") == "user" and said.lstrip().startswith("[Request interrupted by user"):
                    s["interrupts"] += 1
                if "<command-name>/clear" in raw:
                    s["clears"] += 1
                typed = typed_text(entry)
                if typed:
                    s["prompts"] += 1
                    if CORRECTION.search(typed):
                        s["corrections"].append(typed.strip().splitlines()[0][:100])
                    if replied and moment:
                        s["waits"].append((moment - replied).total_seconds())
                    replied = None
            if entry.get("type") == "user" and isinstance(content := message.get("content"), list):
                for block in content:
                    text = block.get("text", "") if isinstance(block, dict) else ""
                    found = SKILL_LOAD.match(text)
                    if found:
                        loaded[found.group(1)] = tokens(text)
                        s["skills"][found.group(1)][0] += 1
                        s["acts"].append("skill:" + found.group(1))
            content = message.get("content")
            for block in content if isinstance(content, list) else []:
                if not isinstance(block, dict):
                    continue
                if block.get("type") == "tool_use":
                    name, args = block.get("name", "?"), block.get("input") or {}
                    pending[block.get("id")] = (ticket, name, args, moment)
                    target = args.get("file_path", "")
                    act = next((a for a, p in ACTS if name == "Bash"
                                and re.search(p, args.get("command", ""))), None)
                    if act and (not s["acts"] or s["acts"][-1] != act):
                        s["acts"].append(act)
                    doc = DOCS.search(target)
                    if doc:
                        s["docs"][doc.group(1)][0 if name == "Read" else 1] += name in ("Read", "Edit", "Write")
                    if name == "Read" and target:
                        s["reads"][target] += 1
                    elif name in ("Edit", "Write", "NotebookEdit") and target:
                        s["edits"].add(target)
                        if SCRATCH.search(target):
                            s["scratch"].add(os.path.basename(target))
                elif block.get("type") == "tool_result":
                    use = pending.pop(block.get("tool_use_id"), None)
                    if not use:
                        continue
                    owner, name, args, started = use
                    if block.get("is_error"):
                        text = block.get("content")
                        text = text if isinstance(text, str) else json.dumps(text)
                        if "isolated in the worktree" in text:
                            stats[owner]["refused"]["worktree guard"] += 1
                        elif "doesn't want to proceed" in text:
                            stats[owner]["refused"]["owner"] += 1
                    tally = stats[owner]["tools"][name]
                    tally[0] += 1
                    tally[1] += result_tokens(block)
                    if name == "Bash" and not agent:
                        command = args.get("command", "")
                        stats[owner]["bash"].append(command)
                        text = json.dumps(block.get("content", ""))
                        if stats[owner]["green_at"] is None and re.search(r"pytest|vitest|pnpm test|turbo test", command) \
                                and re.search(r"\d+ passed", text) and not re.search(r"\d+ (failed|error)", text):
                            stats[owner]["green_at"] = stats[owner]["seconds"]
                    if name == "Bash" and started and moment:
                        took = (moment - started).total_seconds()
                        if took >= SLOW_SECONDS:
                            stats[owner]["slow"].append(
                                (took, args.get("command", "")[:90].replace("\n", " ")))
    return stats


def cost(requests):
    return int(sum(u.get(k, 0) * w for u in requests.values()
                   for k, w in WEIGHTS.items()))


def context(usage):
    return sum(usage.get(k, 0) for k in WEIGHTS if k != "output_tokens")


def estimate(text):
    """A ticket's `## Estimate` → (points, planned model, planned effort)."""
    section = text.split("## Estimate", 1)[1][:600] if "## Estimate" in text else ""
    found = re.search(r"\*\*(\d+)(?: points?)?\*\*", section)
    plan = re.search(r"\*\*(Opus|Sonnet|Haiku|Fable)[^,*]*,\s*(\w+)", section)
    return (int(found.group(1)) if found else None,
            plan.group(1).lower() if plan else None, plan.group(2).lower() if plan else None)


def ticket_file(ticket):
    for path in glob.glob(os.path.join(ROOT, cdd.folder("ticket"), f"{ticket}*.md")):
        if re.match(rf"{re.escape(ticket)}(\.md|-)", os.path.basename(path)):
            return path
    return None


def points(ticket):
    path = ticket_file(ticket)
    return estimate(open(path).read())[0] if path else None


SUBJECTS = None


OWNER_COMMIT = re.compile(r"\bround \d|^sign-off:|\bowner", re.I)


def review_rounds(ticket):
    """Commits the owner's feedback drove: `round 2: ...`, `Sign-off: ...`, `The owner's calls ...`.
    Phase 5 named them three ways, so all three count."""
    global SUBJECTS
    if SUBJECTS is None:
        SUBJECTS = subprocess.run(["git", "-C", ROOT, "log", "--all", "--format=%s"],
                                  capture_output=True, text=True).stdout.splitlines()
    return sum(1 for line in SUBJECTS
               if (m := re.match(rf"{re.escape(ticket)}\b\S* — (.+)", line))
               and OWNER_COMMIT.search(m.group(1)))


def retro_facts(text):
    """A retro entry → (Critical and Important findings, changes after sign-off)."""
    findings = len(re.findall(r"^\| *(?:Critical|Important) *\|", text, re.M))
    changed = text.split("**Changed after sign-off**", 1)
    bullets = re.findall(r"^- (.+)", re.split(r"^\*\*", changed[1], maxsplit=1, flags=re.M)[0], re.M) \
        if len(changed) == 2 else []
    return findings, sum(1 for b in bullets if not b.strip().lower().startswith("none"))


def retro_of(phase, ticket):
    for path in glob.glob(os.path.join(ROOT, RETRO, phase, f"{ticket}*.md")):
        if re.match(rf"{re.escape(ticket)}(\.md|-)", os.path.basename(path)):
            return open(path).read()
    return ""


def retries(commands):
    """Runs of the same command RETRY or more times in a row."""
    runs, count = 0, 1
    for a, b in zip(commands, commands[1:]):
        count = count + 1 if a == b else 1
        runs += count == RETRY
    return runs


def phase_reports(stats):
    allreq = [u for s in stats.values() for u in s["requests"].values()]
    big = [u for u in allreq if context(u) > BIG_CONTEXT]
    whole = sum(cost({i: u for i, u in enumerate(allreq)}) for _ in [0]) or 1
    print(f"\n## Context over {BIG_CONTEXT // 1000}k")
    print(f"- {len(big)} of {len(allreq)} requests, "
          f"{cost(dict(enumerate(big))) / whole:.0%} of cost")
    for t in sorted(stats, key=lambda t: -sum(context(u) > BIG_CONTEXT
                                             for u in stats[t]["requests"].values()))[:8]:
        n = sum(context(u) > BIG_CONTEXT for u in stats[t]["requests"].values())
        print(f"- {t}: {n} of {len(stats[t]['requests'])}")

    skills = defaultdict(lambda: [0, 0])
    for s in stats.values():
        for name, (loads, carried) in s["skills"].items():
            skills[name][0] += loads
            skills[name][1] += carried
    print("\n## Skills: loads, and tokens re-sent by every later request")
    for name, (loads, carried) in sorted(skills.items(), key=lambda kv: -kv[1][1])[:12]:
        print(f"- {name}: {loads} loads, {carried / 1e6:.1f}M carried")

    docs = defaultdict(lambda: [0, 0, 0])
    for s in stats.values():
        for doc, (reads, edits) in s["docs"].items():
            docs[doc][0] += reads
            docs[doc][1] += edits
            docs[doc][2] += edits > 0
    print("\n## Design docs: reads, edits, tickets that edited")
    for doc, (reads, edits, tickets) in sorted(docs.items()):
        print(f"- {doc}: {reads} reads, {edits} edits, {tickets} tickets")

    unused = defaultdict(int)
    for s in stats.values():
        for path, n in s["reads"].items():
            if path not in s["edits"]:
                unused[re.sub(r".*/(?:worktrees/[^/]+/)?(?=apps/|forms/|docs/|\.claude/)", "", path)] += n
    print("\n## Read and never edited, whole phase")
    for path, n in sorted(unused.items(), key=lambda kv: -kv[1])[:15]:
        print(f"- {path}: {n}")



def ticket_rows(stats, phase):
    """One row per ticket: what was planned beside what ran."""
    rows = {}
    for t, s in stats.items():
        if not t[0].isdigit():
            continue
        path = ticket_file(t)
        pts, plan_model, plan_effort = estimate(open(path).read()) if path else (None, None, None)
        findings, changed = retro_facts(retro_of(phase, t))
        loaded = set(s["skills"])
        skipped = [k for parent, kids in EXPECTED.items() if parent in loaded
                   for k in kids if k not in loaded]
        expected = sum(len(kids) for parent, kids in EXPECTED.items() if parent in loaded)
        rows[t] = {"points": pts, "plan": f"{plan_model or '?'}/{plan_effort or '?'}",
                   "model": majority(s["models"]), "effort": majority(s["efforts"]),
                   "mixed": len(s["efforts"]) > 1, "cost": cost(s["requests"]) / 1e6,
                   "agent": cost(s["agent_requests"]) / 1e6, "hours": s["seconds"] / 3600,
                   "rounds": review_rounds(t), "findings": findings, "changed": changed,
                   "expected": expected, "skipped": skipped, "loaded": loaded,
                   "corrections": len(s["corrections"]) + s["interrupts"] + s["denied"]["user-rejected"]}
    return rows


def estimates(rows):
    print("\n## Estimated against actual")
    print("| Points | Tickets | Avg cost (M) | Avg active h | Avg owner rounds | Avg findings |")
    print("|---|---|---|---|---|---|")
    by_points = defaultdict(list)
    for r in rows.values():
        by_points[r["points"]].append(r)
    for p, rs in sorted(by_points.items(), key=lambda kv: kv[0] or 0):
        n = len(rs)
        print(f"| {p or 'none'} | {n} | {sum(r['cost'] for r in rs) / n:.1f} "
              f"| {sum(r['hours'] for r in rs) / n:.1f} | {sum(r['rounds'] for r in rs) / n:.1f} "
              f"| {sum(r['findings'] for r in rs) / n:.1f} |")
    planned = [(t, r) for t, r in rows.items() if r["points"] and r["model"]
               and "?" not in r["plan"] and r["effort"] != "unset"]
    off = [(t, r) for t, r in planned if r["plan"].split("/") != [r["model"], r["effort"]]]
    print(f"- ran on another model or effort than planned: {len(off)} of {len(planned)}")
    for t, r in sorted(off)[:20]:
        print(f"  - {t}: planned {r['plan']}, ran {r['model']}/{r['effort']}")


def by_model(rows):
    """Model and effort beside what each pair cost and what it took to sign off."""
    groups = defaultdict(list)
    for r in rows.values():
        if r["model"]:
            groups[(r["model"], r["effort"])].append(r)
    print("\n## By model and effort (a ticket counts under the pair most of its requests ran at)")
    print("| Model/effort | Tickets | Mixed effort | Points | Cost (M) per point | Active h per point "
          "| Owner rounds | Findings | Changed after sign-off | Corrections | Skill steps skipped |")
    print("|---|---|---|---|---|---|---|---|---|---|---|")
    for (model, effort), rs in sorted(groups.items()):
        pts = sum(r["points"] or 0 for r in rs) or 1
        expected = sum(r["expected"] for r in rs) or 1
        print(f"| {model}/{effort} | {len(rs)} | {sum(r['mixed'] for r in rs)} | {pts} "
              f"| {sum(r['cost'] for r in rs) / pts:.2f} | {sum(r['hours'] for r in rs) / pts:.2f} "
              f"| {sum(r['rounds'] for r in rs)} | {sum(r['findings'] for r in rs)} "
              f"| {sum(r['changed'] for r in rs)} | {sum(r['corrections'] for r in rs)} "
              f"| {sum(len(r['skipped']) for r in rs) / expected:.0%} |")
    steps = defaultdict(lambda: defaultdict(lambda: [0, 0]))  # skill → model → [skipped, expected]
    for r in rows.values():
        if not r["model"]:
            continue
        for parent, kids in EXPECTED.items():
            for k in kids:
                if parent in r["loaded"]:
                    steps[k][r["model"]][1] += 1
                    steps[k][r["model"]][0] += k in r["skipped"]
    families = sorted({r["model"] for r in rows.values() if r["model"]})
    print("\n| Skill a step names | " + " | ".join(f"{f} skipped" for f in families) + " |")
    print("|---|" + "---|" * len(families))
    for k, by in sorted(steps.items()):
        print(f"| {k} | " + " | ".join(
            f"{by[f][0]} of {by[f][1]}" if by[f][1] else "—" for f in families) + " |")


def owner_side(stats):
    """Where the owner stepped in, waited, or the session started over."""
    total = defaultdict(int)
    waits, corrections = [], []
    for t, s in stats.items():
        total["prompts"] += s["prompts"]
        total["interrupts"] += s["interrupts"]
        total["clears"] += s["clears"]
        total["compactions"] += s["compactions"]
        total["cache misses"] += s["cache_misses"]
        total["retry loops"] += retries(s["bash"])
        for why, n in s["denied"].items():
            total["denied: " + why] += n
        waits += s["waits"]
        corrections += [(t, c) for c in s["corrections"]]
    print("\n## The owner's side")
    print("- " + ", ".join(f"{k} {v}" for k, v in total.items()))
    if waits:
        waits.sort()
        print(f"- the owner's reply came {waits[len(waits) // 2] / 60:.0f} min after the agent's "
              f"(median), {sum(min(w, 8 * 3600) for w in waits) / 3600:.0f} h in all, "
              f"{sum(w > 3600 for w in waits)} waits over an hour")
    print(f"- corrections typed: {len(corrections)}")
    for t, c in corrections[:40]:
        print(f"  - {t}: {c}")
    print("\n| Ticket | Corrections, interrupts, refusals | Retry loops | Active h to first green | "
          "Subagent cost (M) | Cache misses |")
    print("|---|---|---|---|---|---|")
    order = sorted(stats, key=lambda t: -(len(stats[t]["corrections"]) + stats[t]["interrupts"]
                                          + stats[t]["denied"]["user-rejected"]))
    for t in order[:20]:
        s = stats[t]
        green = f"{s['green_at'] / 3600:.1f}" if s["green_at"] is not None else "—"
        print(f"| {t} | {len(s['corrections']) + s['interrupts'] + s['denied']['user-rejected']} "
              f"| {retries(s['bash'])} | {green} | {cost(s['agent_requests']) / 1e6:.1f} "
              f"| {s['cache_misses']} |")


def git(*args):
    return subprocess.run(["git", "-C", ROOT, *args], capture_output=True, text=True).stdout


def heading_at(text, line):
    """The nearest markdown heading at or above a 1-based line."""
    for row in reversed(text.splitlines()[:max(line, 1)]):
        if row.startswith("#"):
            return row.lstrip("# ").strip()
    return "(top)"


def hunks(diff):
    """`git show -U0` output → [(file, old start, removed lines, added lines)]."""
    found, file, current = [], None, None
    for row in diff.splitlines():
        if row.startswith("+++ "):
            file = row[6:] if row.startswith("+++ b/") else None
        elif row.startswith("@@"):
            start = int(re.match(r"@@ -(\d+)", row).group(1))
            current = [file, start, [], []]
            found.append(current)
        elif current and row.startswith("-") and not row.startswith("---"):
            current[2].append(row[1:])
        elif current and row.startswith("+") and not row.startswith("+++"):
            current[3].append(row[1:])
    return [tuple(h) for h in found if h[0]]


def is_redesign(removed, added):
    """A hunk that drops what a doc said, not one that adds or rewords it."""
    gone = " ".join(r for r in removed if r.strip())
    if not gone:
        return False
    import difflib
    # How much of the removed text survives in the added text; appended lines don't dilute it.
    kept = sum(b.size for b in difflib.SequenceMatcher(None, gone, " ".join(added),
                                                       autojunk=False).get_matching_blocks())
    return kept / len(gone) < 0.75


def trigger(subject):
    if OWNER_COMMIT.search(re.sub(r"^\S+ — ", "", subject)):
        return "owner"
    if re.search(r"code review|review finding", subject, re.I):
        return "reviewer"
    return "build"


def redesigns(phase):
    """Sections of the design and architecture docs changed after the phase's design was signed off."""
    docs = PLANNED[:3] + [before_the_move(p) for p in PLANNED[:3]]
    since = git("log", "--diff-filter=A", "--format=%aI", "--",
                cdd.DOCS["retro-entry"].format(n=phase, name="phase-tickets")).split()
    log = git("log", "--reverse", "--no-merges", "--format=%H\t%s",
              *([f"--since={since[-1]}"] if since else []), "--", *docs)
    touched = defaultdict(set)   # section → tickets that changed it so far
    found = []
    for row in log.splitlines():
        sha, subject = row.split("\t", 1)
        if re.search(r"editing-prose|prose|wording|reword", subject, re.I):
            continue  # a prose pass rewords; it changes no decision
        ticket = (re.match(rf"({phase}-\d{{3}}[a-z]?)", subject) or [None, None])[1]
        before = {f: git("show", f"{sha}^:{f}") for f in docs}  # a path not there yet shows nothing
        changed = defaultdict(lambda: [[], []])  # one count per section a commit changes
        for file, start, removed, added in hunks(git("show", "-U0", "--format=", sha, "--", *docs)):
            section = (before_the_move(file).removeprefix("docs/"),
                       heading_at(before[file], start))
            changed[section][0] += removed
            changed[section][1] += added
        for section, (removed, added) in changed.items():
            if is_redesign(removed, added):
                found.append((section, ticket, trigger(subject), len(touched[section] - {ticket})))
            if ticket:
                touched[section].add(ticket)
    print("\n## Redesigns: signed-off sections changed, not just added to or reworded")
    by_trigger = defaultdict(int)
    for f in found:
        by_trigger[f[2]] += 1
    print(f"- {len(found)} in all: " + ", ".join(f"{k} {v}" for k, v in by_trigger.items()))
    by_section = defaultdict(list)
    for section, ticket, why, before in found:
        by_section[section].append((ticket, why, before))
    print("| Doc | Section | Redesigns | Triggers | Tickets that edited it before |")
    print("|---|---|---|---|---|")
    for (doc, heading), items in sorted(by_section.items(), key=lambda kv: -len(kv[1]))[:25]:
        whys = defaultdict(int)
        for _, why, _ in items:
            whys[why] += 1
        print(f"| {doc} | {heading[:50]} | {len(items)} | "
              f"{', '.join(f'{k} {v}' for k, v in whys.items())} | {max(b for _, _, b in items)} |")


NOTE_HEADS = re.compile(r"^\*\*(Owner's calls|Owner feedback|For the phase close)\*\*", re.M)


def owner_notes(phase):
    """Every note the owner left in the phase's retro entries, for the close to group by theme."""
    print("\n## The owner's notes in the retro entries")
    for path in sorted(glob.glob(os.path.join(ROOT, RETRO, phase, "*.md"))):
        text = open(path).read()
        notes = []
        for head in NOTE_HEADS.finditer(text):
            body = re.split(r"^\*\*", text[head.end():], maxsplit=1, flags=re.M)[0]
            notes += [f"{head.group(1)}: {b}" for b in re.findall(r"^- (.+)", body, re.M)]
        notes += [m.strip() for m in re.findall(r"^The owner's note[^:]*: (.+)", text, re.M)]
        for note in notes:
            print(f"- {os.path.basename(path)}: {note[:160]}")


def splits(phase):
    # A signed-off ticket leaves the backlog.
    deleted = git("log", "--diff-filter=D", "--name-only", "--format=", "--", cdd.DOCS["ticket"].format(name=f"{phase}-*"),
                  before_the_move(cdd.DOCS["ticket"].format(name=f"{phase}-*")))
    names = {os.path.basename(p) for p in deleted.split()}
    split = defaultdict(list)
    for name in names:
        found = re.match(rf"({phase}-\d{{3}})([a-z])", name)
        if found:
            split[found.group(1)].append(found.group(2))
    print("\n## Tickets split mid-flight")
    print("- " + (", ".join(f"{t} into {''.join(sorted(p))}" for t, p in sorted(split.items())) or "none"))


def repeated_text():
    """Sentences that say the same thing in two or more of the workflow's files."""
    paths = (glob.glob(os.path.join(ROOT, ".claude/skills/**/*.md"), recursive=True)
             + glob.glob(os.path.join(ROOT, cdd.FOLDERS["templates"], "*.md"))
             + [os.path.join(ROOT, p) for p in ("CLAUDE.md", cdd.DOCS["architecture"])])
    where = defaultdict(set)  # an 8-word run → files holding it; reworded copies still share runs
    for path in paths:
        words = re.sub(r"[`*_\[\]()|>#-]", " ", open(path).read()).lower().split()
        for i in range(len(words) - 7):
            where[" ".join(words[i:i + 8])].add(os.path.relpath(path, ROOT))
    pairs = defaultdict(list)
    for run, ps in where.items():
        if len(ps) >= 2:
            pairs[tuple(sorted(ps))].append(run)
    print(f"\n## Repeated text: 8-word runs shared between workflow files")
    for ps, runs in sorted(pairs.items(), key=lambda kv: -len(kv[1]))[:15]:
        print(f"- {len(runs)} runs in {', '.join(ps)}: \"{runs[0]}\"")


def sequences(stats):
    """Acts in the order they ran, to find steps repeated or out of turn."""
    pairs, restarts, early = defaultdict(int), {}, []
    for t, s in stats.items():
        acts = s["acts"]
        for a, b in zip(acts, acts[1:]):
            pairs[(a, b)] += 1
        restarts[t] = sum(1 for a, b in zip(acts, acts[1:]) if (a, b) == ("server-", "server+"))
        signoff = next((i for i, a in enumerate(acts) if a in ("skill:signing-off-a-ticket", "skill:reviewing-a-ticket")), None)
        review = next((i for i, a in enumerate(acts) if a == "skill:requesting-code-review"), None)
        shot = next((i for i, a in enumerate(acts) if a == "shot"), None)
        if shot is not None and review is not None and shot > review and (
                signoff is None or shot < signoff):
            early.append(t)
    print("\n## Order of acts")
    print("- server stopped then started: " + ", ".join(
        f"{t} {n}" for t, n in sorted(restarts.items(), key=lambda kv: -kv[1]) if n))
    print(f"- screenshot after code review: {', '.join(sorted(early)) or 'none'}")
    refused = defaultdict(int)
    for s in stats.values():
        for why, n in s["refused"].items():
            refused[why] += n
    print("- refused calls: " + ", ".join(f"{w} {n}" for w, n in refused.items()))
    print("- most common next acts:")
    for (a, b), n in sorted(pairs.items(), key=lambda kv: -kv[1])[:15]:
        print(f"  - {n}× {a} → {b}")


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("phase", help="three digits, such as 004")
    parser.add_argument("--top", type=int, default=5)
    opts = parser.parse_args()
    opts.phase = f"{int(opts.phase):03d}"  # "6" would match any branch holding a 6
    stats = mine(opts.phase)
    order = sorted(stats, key=lambda t: -cost(stats[t]["requests"]))

    print(f"# Phase {opts.phase} sessions\n")
    print("| Ticket | Sessions | Active h | Requests | Cost (M input-eq) |")
    print("|---|---|---|---|---|")
    for t in order:
        s = stats[t]
        print(f"| {t} | {len(s['sessions'])} | {s['seconds'] / 3600:.1f} "
              f"| {len(s['requests'])} | {cost(s['requests']) / 1e6:.1f} |")

    for t in order:
        s = stats[t]
        print(f"\n## {t}")
        tools = sorted(s["tools"].items(), key=lambda kv: -kv[1][1])[:opts.top]
        print("- result tokens by tool: " + ", ".join(
            f"{n} {c}× {tok // 1000}k" for n, (c, tok) in tools))
        unused = sorted(((n, f) for f, n in s["reads"].items() if f not in s["edits"]),
                        reverse=True)[:opts.top]
        if unused:
            print("- read, never edited: " + ", ".join(
                f"{os.path.relpath(f, ROOT) if f.startswith(ROOT) else f} ×{n}"
                for n, f in unused))
        for took, command in sorted(s["slow"], reverse=True)[:opts.top]:
            print(f"- slow ({took:.0f}s): `{command}`")

    scripts = defaultdict(set)
    for t, s in stats.items():
        for name in s["scratch"]:
            scripts[name].add(t)
    repeated = {n: ts for n, ts in scripts.items() if len(ts) >= 2}
    phase_reports(stats)
    rows = ticket_rows(stats, opts.phase)
    estimates(rows)
    by_model(rows)
    owner_side(stats)
    redesigns(opts.phase)
    splits(opts.phase)
    owner_notes(opts.phase)
    repeated_text()
    sequences(stats)
    print("\n## Scratch scripts in two or more tickets")
    for name, ts in sorted(repeated.items(), key=lambda kv: -len(kv[1])):
        print(f"- `{name}`: {', '.join(sorted(ts))}")
    if not repeated:
        print("- none")


if __name__ == "__main__":
    main()
