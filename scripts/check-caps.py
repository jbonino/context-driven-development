#!/usr/bin/env -S uv run --script
# /// script
# requires-python = ">=3.13"
# dependencies = []
# ///
"""Warns where a form passes its soft cap, so the owner decides whether to
redesign upstream. A form's cap is read from the Examples of the outline
that warns, a ticket's points from Splitting the work's rule, and its new
scenarios from Signing off a change's. A warning never fails: the script
exits 0.

Run: uv run --script scripts/check-caps.py
"""
import os
import re
import subprocess

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DESIGN = "docs/design_document.md"
ARCHITECTURE = "docs/architecture.md"
HEADING = re.compile(r"^#+ (.+)$")
STEP = re.compile(r"^(?:\d+\. |\| \d+ \|)")
FEATURE_LINK = re.compile(r"\]\(#(feature-[^)]*)\)")
SCENARIO = re.compile(r"^\s*Scenario(?: Outline)?: (.+)$")
RULE = re.compile(r"^\s*Rule: ")
ROW = re.compile(r"^\s*\|(.+)\|\s*$")
CAP = re.compile(r"(\d+) (\w+)")
ESTIMATE = re.compile(r"\*\*Estimate\.\*\* (\d+)")
NEW_SCENARIOS = re.compile(r"Rule: A ticket takes (\w+) new scenarios at most")
POINTS = re.compile(r"Rule: A ticket is .*?(\d+) points")
WORDS = {"one": 1, "two": 2, "three": 3, "four": 4, "five": 5}
PLURAL = {"feature": "features"}


def examples(design):
    """The Examples rows under the outline whose header reads form, cap, upstream."""
    rows, header = [], False
    for line in design.splitlines():
        row = ROW.match(line)
        cells = [c.strip() for c in row.group(1).split("|")] if row else None
        if cells and cells[:3] == ["form", "cap", "upstream"]:
            header = True
        elif cells and header:
            rows.append(cells)
        else:
            header = header and bool(cells)
    return rows


def caps(design):
    """Each form's caps, by unit."""
    return {form: {unit: int(n) for n, unit in CAP.findall(cap)} for form, cap, _ in examples(design)}


def upstreams(design):
    """What the owner may redesign for each form."""
    return {form: upstream for form, _, upstream in examples(design)}


def new_scenario_cap(design):
    match = NEW_SCENARIOS.search(design)
    return WORDS.get(match.group(1)) if match else None


def point_cap(design):
    match = POINTS.search(design)
    return int(match.group(1)) if match else None


def short_outlines(name, design):
    """An outline with fewer than three Examples rows, which reads better as
    separate scenarios."""
    warnings, outline, rows, header = [], None, 0, False
    for line in design.splitlines() + ["```"]:
        scenario = SCENARIO.match(line)
        if scenario or RULE.match(line) or line.strip().startswith("```"):
            if outline and rows < 3:
                warnings.append(f"{name}: Scenario Outline: {outline} has {rows} Examples rows, under 3. "
                                "The owner decides whether to split it into scenarios")
            outline = scenario.group(1) if scenario and "Outline" in line else None
            rows, header = 0, False
        elif outline and line.strip().startswith("Examples:"):
            header = True
        elif outline and ROW.match(line):
            rows += 0 if header else 1
            header = False
    return warnings


def sections(text):
    """Each heading's lines up to the next heading. Inside a code fence only
    gherkin lines count. A heading named twice gathers both sections."""
    found, heading, fence = {}, None, None
    for line in text.splitlines():
        if line.lstrip().startswith("```"):
            fence = None if fence is not None else line.strip()[3:]
            continue
        match = HEADING.match(line) if fence is None else None
        if match:
            heading = match.group(1).strip()
            found.setdefault(heading, [])
        elif heading and (fence is None or fence == "gherkin" and (SCENARIO.match(line) or RULE.match(line))):
            found[heading].append(line)
    return found


def counts(design, architecture):
    """Each form's count by unit, as (doc, form, name, unit, count)."""
    found = []
    for heading, lines in sections(design).items():
        steps = [line for line in lines if STEP.match(line)]
        if heading.startswith("Journey: "):
            found.append(("design", "journey", heading, "workflows", len(steps)))
        elif heading.startswith("Workflow: "):
            found.append(("design", "workflow", heading, "steps", len(steps)))
            found += [("design", "workflow step", f"{heading} step {n}", "feature", len(set(FEATURE_LINK.findall(s))))
                      for n, s in enumerate(steps, 1)]
        scenarios = sum(bool(SCENARIO.match(line)) for line in lines)
        if scenarios:
            found.append(("design", "feature", heading, "scenarios", scenarios))
            found.append(("design", "feature", heading, "rules", sum(bool(RULE.match(line)) for line in lines)))
    for heading, lines in sections(architecture).items():
        found.append(("architecture", "architecture section", heading, "decisions",
                      sum(line.startswith("- **") for line in lines)))
    return found


def form_warnings(design_name, design, architecture_name, architecture):
    """A form past its cap goes to the owner."""
    found, ups = caps(design), upstreams(design)
    names = {"design": design_name, "architecture": architecture_name}
    return [f"{names[doc]}: {name} has {count} {PLURAL.get(unit, unit)}, past its cap of {found[form][unit]}. "
            f"The owner decides whether to redesign {ups[form]}"
            for doc, form, name, unit, count in counts(design, architecture)
            if unit in found.get(form, {}) and count > found[form][unit]]


def point_warnings(tickets, cap):
    """An open ticket past the points a ticket takes."""
    if cap is None:
        return ["Splitting the work's rule names no points cap, so no ticket is checked"]
    return [f"{path} is {m.group(1)} points, past its cap of {cap}. The owner decides whether to redesign its feature"
            for path, text in sorted(tickets.items()) if (m := ESTIMATE.search(text)) and int(m.group(1)) > cap]


def titles(text):
    return {m.group(1).strip() for line in text.splitlines() if (m := SCENARIO.match(line))}


def branch_adds(at_tag, at_base, now):
    """The titles now holds that neither the plan's tag nor the branch's
    merge-base with main held. A rename counts as new. A title main gained
    from another ticket since the tag is that ticket's."""
    return sorted(titles(now) - titles(at_tag) - titles(at_base))


def new_scenario_warnings(added, cap):
    """A ticket's scenarios past the cap go to the owner."""
    if cap is None:
        return ["Signing off a change's rule names no count of new scenarios, so no branch is checked"]
    if len(added) <= cap:
        return []
    return [f"This branch adds {len(added)} scenarios since its plan's tag, past its cap of {cap}: "
            f"{', '.join(added)}. The owner decides: the ticket is redesigned in place, or the third goes to its retro"]


def git(*args):
    result = subprocess.run(["git", *args], cwd=ROOT, capture_output=True, text=True)
    return result.stdout.strip() if result.returncode == 0 else None


def read(path):
    with open(os.path.join(ROOT, path), encoding="utf-8") as handle:
        return handle.read()


def branch_scenarios():
    """The titles this branch adds to the design. Main, a detached HEAD and
    a branch with no plan's tag add none."""
    tag = git("describe", "--tags", "--abbrev=0", "--match", "phase-*")
    base = git("merge-base", "main", "HEAD")
    if not tag or not base or git("branch", "--show-current") in ("main", None, ""):
        return []
    return branch_adds(git("show", f"{tag}:{DESIGN}") or "", git("show", f"{base}:{DESIGN}") or "", read(DESIGN))


def main():
    design = read(DESIGN)
    warnings = form_warnings(DESIGN, design, ARCHITECTURE, read(ARCHITECTURE))
    warnings += short_outlines(DESIGN, design)
    backlog = os.path.join(ROOT, "docs", "backlog")
    tickets = {f"docs/backlog/{n}": read(f"docs/backlog/{n}") for n in sorted(os.listdir(backlog))
               if n.endswith(".md") and n != "README.md"}
    warnings += point_warnings(tickets, point_cap(design))
    warnings += new_scenario_warnings(branch_scenarios(), new_scenario_cap(design))
    for warning in warnings:
        print(f"warning: {warning}")


if __name__ == "__main__":
    main()
