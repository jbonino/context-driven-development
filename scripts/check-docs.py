#!/usr/bin/env -S uv run --script
# /// script
# requires-python = ">=3.13"
# dependencies = []
# ///
"""Checks that each fact holds its place: each part has its home, each doc
names only what's above it, and every link resolves.

Run: uv run --script scripts/check-docs.py. Exits 1 and lists each problem.
Rename: uv run --script scripts/check-docs.py rename "{old}" "{new}"
"""
import difflib
import os
import re
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DESIGN = "docs/design_document.md"
ARCHITECTURE = "docs/architecture.md"
FOUNDATIONS = "docs/foundations.md"
KINDS = ("journey", "workflow", "scenario", "rule", "decision")
HISTORY = ("docs/done/", "docs/retro/", "docs/deferred/", "docs/feedback.md")
FIXTURES = ("scripts/test_check_docs.py", "scripts/test_check_caps.py")

HEADING = re.compile(r"^(#+) (.+)$")
SCENARIO = re.compile(r"^\s*Scenario(?: Outline)?: (.+)$")
GHERKIN_RULE = re.compile(r"^\s*Rule: (.+)$")
LINK = re.compile(r"\]\(([^)\s]+)\)")
TICKET_FILE = re.compile(r"^docs/(?:backlog|done)/\d{3}-\d{3}[a-z]?-[\w-]+\.md$")


def lines_outside_code(text):
    """Each line with whether it sits inside a fenced block."""
    fenced = False
    for line in text.splitlines():
        if line.lstrip().startswith("```"):
            fenced = not fenced
            continue
        yield line, fenced


def parse(text):
    """The workflows, journeys, features, scenarios, Gherkin rules and each
    heading's bullets. A feature is a heading that holds scenarios."""
    tree = {"workflows": set(), "journeys": set(), "features": set(), "scenarios": [], "rules": [], "bullets": {}}
    heading = None
    for line, fenced in lines_outside_code(text):
        match = None if fenced else HEADING.match(line)
        if match:
            heading = match.group(2).strip()
            for kind, key in (("Workflow: ", "workflows"), ("Journey: ", "journeys")):
                if heading.startswith(kind):
                    tree[key].add(heading[len(kind):])
            continue
        scenario = SCENARIO.match(line) if fenced else None
        rule = GHERKIN_RULE.match(line) if fenced else None
        if scenario and heading:
            tree["features"].add(heading)
            tree["scenarios"].append((heading, scenario.group(1).strip()))
        elif rule and heading:
            tree["rules"].append((heading, rule.group(1).strip()))
        elif heading and not fenced and line.startswith("- "):
            tree["bullets"].setdefault(heading, []).append(line[2:])
        elif heading and not fenced and line.startswith("  ") and line.strip() and tree["bullets"].get(heading):
            tree["bullets"][heading][-1] += " " + line.strip()
    return tree


def slug(name):
    return re.sub(r"[^a-z0-9]+", "_", name.lower()).strip("_")


def anchor(title):
    """GitHub's anchor for a heading."""
    title = re.sub(r"\[([^\]]+)\]\([^)]*\)", r"\1", title)
    return re.sub(r"[^\w\- ]", "", title.strip().lower()).replace(" ", "-")


def anchors(text):
    """Every anchor a file's headings make, with GitHub's -1, -2 for repeats."""
    seen, found = {}, set()
    for line, fenced in lines_outside_code(text):
        match = None if fenced else HEADING.match(line)
        if match:
            base = anchor(match.group(2))
            count = seen.get(base, 0)
            seen[base] = count + 1
            found.add(base if count == 0 else f"{base}-{count}")
    return found


def rule_name(bullet):
    """A bullet's first sentence, with footnotes, links, backticks and bold stripped."""
    text = re.sub(r"\[\^[^\]]*\]", "", bullet)
    text = re.sub(r"\[([^\]]+)\]\([^)]*\)", r"\1", text).replace("`", "").replace("**", "")
    return re.split(r"(?<=[.!?])\s", text.strip(), maxsplit=1)[0].rstrip(".")


def decisions(architecture):
    """Each decision's subject: a bullet's bold opening words."""
    return {m.group(1).replace("`", "") for bullets in architecture["bullets"].values() for b in bullets
            if (m := re.match(r"\*\*(.+?)\*\*", b))}


def rules(design, architecture, tickets):
    """The design's Gherkin rules, each system's Rules, and the rules open tickets propose."""
    found = {name for _, name in design["rules"]}
    found |= {rule_name(b) for b in architecture["bullets"].get("Rules", [])}
    return found | {name for text in tickets.values() for _, name in parse(text)["rules"]}


def rule_scenarios(path, text):
    """A Gherkin Rule holds over two scenarios at least. An outline's
    Examples rows each count as one, its first counted with the outline."""
    found, current, rows = [], None, None
    for line, fenced in lines_outside_code(text):
        rule = GHERKIN_RULE.match(line) if fenced else None
        stripped = line.strip()
        if rule:
            current, rows = [rule.group(1).strip(), 0], None
            found.append(current)
        elif not fenced:
            current = None
        elif current and SCENARIO.match(line):
            current[1] += 1
            rows = "outline" if "Outline" in line else None
        elif current and rows is not None and stripped.startswith("Examples:"):
            rows = -1 if rows == "outline" else 0  # skip the header, and the first block's first row
        elif current and isinstance(rows, int) and stripped.startswith("|"):
            current[1] += rows > 0
            rows += 1
    return [f"{path}: Rule: {name} holds over {n} scenario{'' if n == 1 else 's'}; a rule needs two"
            for name, n in found if n < 2]


def named_tests(kind, names, tests, baseline):
    """Each name has a test of its kind, or sits in the kind's baseline. A
    baseline line that no longer applies fails."""
    untested = {n for n in names if f"test_{kind}_{slug(n)}" not in tests}
    return ([f"{kind.title()}: {n} has no test_{kind}_{slug(n)}" for n in sorted(untested - baseline)]
            + [f"{n}  ← tested or gone: remove it from the {kind} baseline" for n in sorted(baseline - untested)])


def scenario_tests(scenarios, tests, tickets, baseline):
    """A scenario has a test named for it, or an open ticket cites it, or it
    sits in the baseline. A baseline line that no longer applies fails."""
    by_feature = {}
    for feature, name in scenarios:
        by_feature.setdefault(feature, []).append(name)
    pending = set()
    for text in tickets.values():
        for paragraph in text.split("\n\n"):
            for feature, names in by_feature.items():
                if re.search(rf"design(?:_document)?\.md#{anchor(feature)}\)", paragraph):
                    cited = [n for n in names if re.search(rf"(?<!\w){re.escape(n)}(?!\w)", paragraph)]
                    pending |= {f"{feature}: {n}" for n in cited or names}
    problems, untested = [], set()
    for feature, name in scenarios:
        key = f"{feature}: {name}"
        if f"test_scenario_{slug(name)}" in tests or key in pending:
            continue
        untested.add(key)
        if key not in baseline:
            problems.append(f"{feature}'s scenario {name} has no test_scenario_{slug(name)}, and no open ticket cites it")
    return problems + [f"{key}  ← tested, cited or gone: remove it from the scenario baseline"
                       for key in sorted(baseline - untested)]


def source_tests(tests, sources):
    """A test carries a kind's prefix and names a source of that kind. A near
    miss asks whether the source was renamed."""
    problems = []
    for test in sorted(tests):
        kind = next((k for k in KINDS if test.startswith(f"test_{k}_")), None)
        if kind is None:
            problems.append(f"{test} carries no prefix: {', '.join(k + '_' for k in KINDS)}")
            continue
        by_slug = {slug(n): n for n in sources.get(kind, set())}
        rest = test[len(f"test_{kind}_"):]
        if rest not in by_slug:
            near = difflib.get_close_matches(rest, by_slug, n=1)
            ask = f"; was it renamed to {by_slug[near[0]]}?" if near else ""
            problems.append(f"{test} names no {kind}{ask}")
    return problems


def deferred_revisits(files):
    """Each deferred entry says when to revisit it."""
    return [f"{path} has no Revisit when line" for path, text in sorted(files.items())
            if path.startswith("docs/deferred/") and not path.endswith("README.md") and "**Revisit when**" not in text]


def deferred_outside(files):
    """A deferred thing is described in its own file alone. Its name is its
    file's title, dashes read as spaces. History and a link to it pass."""
    titles = {}
    for path, text in files.items():
        if path.startswith("docs/deferred/") and not path.endswith("README.md"):
            title = next((m.group(2).strip() for line in text.splitlines() if (m := HEADING.match(line))), None)
            if title:
                titles[os.path.basename(path)] = title
    problems = []
    for path, text in sorted(files.items()):
        if path.startswith(HISTORY + FIXTURES):
            continue
        for line in text.splitlines():
            for name, title in sorted(titles.items()):
                words = r"[\s-]+".join(map(re.escape, re.split(r"[\s-]+", title)))
                if re.search(rf"(?<!\w){words}(?!\w)", line, re.I) and f"deferred/{name}" not in line:
                    problems.append(f"{path} describes {title} outside its deferred file: {line.strip()}")
    return problems


def may_name(path):
    """What a file may name, by its row in A file that names one it may not."""
    if path in (DESIGN, "docs/product_roadmap.md") or (path.startswith("scripts/") and not path.endswith(".md")):
        return lambda t: False
    if path == ARCHITECTURE or (path.startswith("docs/deferred/") and not path.endswith("README.md")):
        return lambda t: t == DESIGN
    if path == "docs/backlog/README.md":
        return lambda t: bool(TICKET_FILE.match(t)) and t.startswith("docs/backlog/")
    if path.startswith("docs/release/"):
        return lambda t: bool(TICKET_FILE.match(t)) or t == ARCHITECTURE
    return None


def links(text):
    """Each link target outside code blocks and inline code."""
    for line, fenced in lines_outside_code(text):
        if not fenced:
            yield from LINK.findall(re.sub(r"`[^`]*`", "", line))


def stream_names(files):
    """A file links only the foundations and what its row may name."""
    problems = []
    for path, text in sorted(files.items()):
        allowed = may_name(path)
        if allowed is None:
            continue
        for target in links(text):
            file = target.partition("#")[0]
            if not file or re.match(r"[a-z]+:", target):
                continue
            resolved = os.path.normpath(os.path.join(os.path.dirname(path), file))
            if resolved not in (path, FOUNDATIONS) and not allowed(resolved):
                problems.append(f"{path} names {target}, which it may not")
    return problems


SPAN = re.compile(r"`([^`]+)`")
PATH = re.compile(r"/|\.(?:md|py|sh|json|ya?ml|toml|txt|js|html)\b")
SKILLS = ".claude/skills/"
SKILL_GAP = "A skill's paths"


def skill_paths(files):
    """A skill line names no path: no link to a file and no backticked path."""
    problems = []
    for path, text in sorted(files.items()):
        if not path.startswith(SKILLS):
            continue
        for line, fenced in lines_outside_code(text):
            spans = SPAN.findall(line)
            targets = LINK.findall(SPAN.sub("", line))
            if fenced:
                continue
            if any(PATH.search(s) for s in spans) or any(not re.match(r"[a-z]+:|#", t) for t in targets):
                problems.append(f"{path} names a path: {line.strip()}")
    return problems


def orphan_headings(design, architecture):
    """Each architecture heading for a workflow or feature names one in the design."""
    named = design["features"] | {f"Workflow: {w}" for w in design["workflows"]}
    problems = []
    for line, fenced in lines_outside_code(architecture):
        heading = None if fenced else HEADING.match(line)
        title = heading.group(2).strip() if heading else ""
        if title.startswith(("Feature: ", "Workflow: ")) and title not in named:
            problems.append(f"architecture's {title} names no workflow or feature in the design")
    return problems


def system_features(design, architecture):
    """Each design feature sits on exactly one system's opening line, split by " · "."""
    listed, opening = {}, False
    for line, fenced in lines_outside_code(architecture):
        heading = None if fenced else HEADING.match(line)
        if heading:
            opening = len(heading.group(1)) == 2
        elif opening and line.strip():
            for name in line.split(" · "):
                listed[f"Feature: {name.strip()}"] = listed.get(f"Feature: {name.strip()}", 0) + 1
            opening = False
    problems = []
    for feature in sorted(design["features"]):
        count = listed.get(feature, 0)
        if count == 0:
            problems.append(f"design's {feature} sits on no system's opening line in the architecture")
        elif count > 1:
            problems.append(f"design's {feature} sits on {count} systems' opening lines in the architecture")
    return problems


def broken_links(files, exists, read_file=lambda path: ""):
    """A link lands on a file and anchor that exist. Paths in `files` are
    relative to the repo. `exists` answers for files outside it."""
    problems = []
    for path, text in sorted(files.items()):
        for target in links(text):
            if re.match(r"[a-z]+:", target) or "{" in target:
                continue
            file, _, mark = target.partition("#")
            resolved = os.path.normpath(os.path.join(os.path.dirname(path), file)) if file else path
            if resolved not in files and not exists(resolved):
                problems.append(f"{path} links {target}, which is not there")
            elif mark and resolved.endswith(".md") and mark not in anchors(files.get(resolved) or read_file(resolved)):
                problems.append(f"{path} links {target}, which has no such heading")
    return problems


def baseline(path, text):
    """A baseline's entries, and its problems. Each line reads
    "{name} — {reason}", unless a "#" line at the file's top gives the reason
    for all. An empty baseline, or a gone one the code still reads, fails."""
    if text is None:
        return set(), [f"{path} is gone: delete the code that reads it"]
    rows = [line for line in text.splitlines() if line.strip()]
    shared = bool(rows) and rows[0].startswith("#")
    rows = [line for line in rows if not line.startswith("#")]
    if not rows:
        return set(), [f"{path} is empty: delete it and the code that reads it"]
    if shared:
        return set(rows), []
    names, _, reasons = zip(*(line.partition(" — ") for line in rows))
    return set(names), [f"{path}: {name} gives no reason; add \" — {{reason}}\", or a # line at the file's top"
                        for name, reason in zip(names, reasons) if not reason.strip()]


def rename(files, old, new):
    """The files that change when a scenario, feature, workflow, journey or
    rule is renamed: its prose, the links to its heading and the tests named
    for it. A longer name holding it keeps its own. History keeps the old
    name, and the checks' own fixtures keep their prose. A name the docs
    lack renames nothing."""
    design = parse(files.get(DESIGN, ""))
    architecture = parse(files.get(ARCHITECTURE, ""))
    tickets = {p: t for p, t in files.items() if p.startswith("docs/backlog/") and not p.endswith("README.md")}
    by_kind = {"journey": design["journeys"], "workflow": design["workflows"],
               "scenario": {n for _, n in design["scenarios"]}, "rule": rules(design, architecture, tickets)}
    tests = {f"test_{k}_{slug(old)}": f"test_{k}_{slug(new)}" for k, names in by_kind.items() if old in names}
    marks = {}
    if old in design["features"]:
        marks[anchor(old)] = anchor(new)
    for kind in ("workflow", "journey"):
        if old in by_kind[kind]:
            marks[anchor(f"{kind.title()}: {old}")] = anchor(f"{kind.title()}: {new}")
    if not tests and not marks:
        return {}
    known = design["features"].union(*by_kind.values())
    longer = sorted((n for n in known if old in n and n != old), key=len, reverse=True)
    phrase = re.compile("|".join([re.escape(n) for n in longer] + [rf"(?<!\w){re.escape(old)}(?!\w)"]))
    changed = {}
    for path, text in files.items():
        if path.startswith(HISTORY):
            continue
        after = text
        if path.endswith((".md", ".txt")):
            after = phrase.sub(lambda m: new if m.group() == old else m.group(), after)
            for was, now in marks.items():
                after = after.replace(f"#{was})", f"#{now})")
        after = re.sub(r"\btest_\w+", lambda m: tests.get(m.group(), m.group()), after)
        if after != text:
            changed[path] = after
    return changed


def read(path):
    with open(os.path.join(ROOT, path), encoding="utf-8") as handle:
        return handle.read()


def text_files(top, suffixes):
    files = {}
    for folder, dirs, names in os.walk(os.path.join(ROOT, top)):
        dirs[:] = [d for d in dirs if d not in ("raw", "__pycache__")]
        for name in names:
            if name.endswith(suffixes):
                path = os.path.relpath(os.path.join(folder, name), ROOT)
                files[path] = read(path)
    return files


def load():
    """Everything the checks read, once."""
    docs = text_files("docs", ".md") | text_files(".claude/skills", ".md")
    docs |= {name: read(name) for name in ("CLAUDE.md", "README.md")}
    code = text_files("scripts", (".py", ".sh"))
    return docs, code


def baseline_path(kind):
    return f"scripts/{kind}-baseline.txt"


def baselines():
    """Each kind's baseline entries, and what is wrong with the files."""
    found, problems = {}, []
    for kind in KINDS:
        path = baseline_path(kind)
        text = read(path) if os.path.exists(os.path.join(ROOT, path)) else None
        found[kind], wrong = baseline(path, text)
        problems += wrong
    return found, problems


def check(docs, code):
    design, architecture = parse(docs[DESIGN]), parse(docs[ARCHITECTURE])
    tickets = {p: t for p, t in docs.items() if p.startswith("docs/backlog/") and not p.endswith("README.md")}
    tests = {name for path, text in code.items()
             if path.startswith("scripts/test_") for name in re.findall(r"^def (test_\w+)", text, re.M)}
    found, problems = baselines()
    named = {"journey": design["journeys"], "workflow": design["workflows"],
             "scenario": {n for _, n in design["scenarios"]}, "rule": rules(design, architecture, tickets),
             "decision": decisions(architecture)}
    problems += rule_scenarios(DESIGN, docs[DESIGN])
    for kind in ("journey", "workflow"):
        problems += named_tests(kind, named[kind], tests, found[kind])
    problems += named_tests("rule", {n for _, n in design["rules"]}, tests, found["rule"])
    problems += named_tests("decision", named["decision"], tests, found["decision"] - {SKILL_GAP})
    skills = skill_paths(docs)
    if SKILL_GAP in found["decision"] and not skills:
        problems.append(f"{SKILL_GAP}  ← no skill names a path: remove it from the decision baseline")
    if SKILL_GAP in found["decision"] and SKILL_GAP not in named["decision"]:
        problems.append(f"{SKILL_GAP}  ← gone: remove it from the decision baseline")
    elif SKILL_GAP not in found["decision"]:
        problems += skills
    problems += scenario_tests(design["scenarios"], tests, tickets, found["scenario"])
    problems += source_tests(tests, named)
    problems += deferred_revisits(docs) + deferred_outside(docs | code)
    problems += stream_names(docs | {p: t for p, t in code.items() if p not in FIXTURES})
    problems += orphan_headings(design, docs[ARCHITECTURE]) + system_features(design, docs[ARCHITECTURE])
    linked = {p: t for p, t in docs.items() if not p.startswith(("docs/done/", "docs/retro/"))}
    problems += broken_links(linked, lambda path: os.path.exists(os.path.join(ROOT, path)), read)
    return problems


def main():
    if sys.argv[1:2] == ["rename"] and len(sys.argv) == 4:
        docs, code = load()
        lines = {baseline_path(k): read(baseline_path(k)) for k in KINDS}
        changed = rename(docs | code | lines, sys.argv[2], sys.argv[3])
        if not changed:
            raise SystemExit(f"{sys.argv[2]} names no scenario, feature, workflow, journey or rule")
        for path, text in sorted(changed.items()):
            with open(os.path.join(ROOT, path), "w", encoding="utf-8") as handle:
                handle.write(text)
            print(f"renamed in {path}")
        return
    problems = check(*load())
    for problem in problems:
        print(problem)
    raise SystemExit(1 if problems else 0)


if __name__ == "__main__":
    main()
