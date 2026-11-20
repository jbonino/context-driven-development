"""Tests for check-docs.py. Run: uv run --with pytest pytest scripts/"""
import importlib.util
import os

import pytest

HERE = os.path.dirname(os.path.abspath(__file__))
spec = importlib.util.spec_from_file_location("check_docs", os.path.join(HERE, "check-docs.py"))
cd = importlib.util.module_from_spec(spec)
spec.loader.exec_module(cd)


PARTS = {  # part and home: the check, and the failure it gives
    "a rule with two scenarios under it": (lambda: cd.rule_scenarios(
        "design.md", "```gherkin\nFeature: Notes\n  Rule: One alone\n\n    Scenario: Only\n```\n"),
        "design.md: Rule: One alone holds over 1 scenario; a rule needs two"),
    "a journey with a test named for it": (lambda: cd.named_tests("journey", {"A day"}, set(), set()),
                                           "Journey: A day has no test_journey_a_day"),
    "a workflow with a test named for it": (lambda: cd.named_tests("workflow", {"Closing"}, set(), set()),
                                            "Workflow: Closing has no test_workflow_closing"),
    "a scenario with a test named for it": (
        lambda: cd.scenario_tests([("Feature: Notes", "Only")], set(), {}, set()),
        "Feature: Notes's scenario Only has no test_scenario_only, and no open ticket cites it"),
    "a rule with a test named for it": (lambda: cd.named_tests("rule", {"One alone"}, set(), set()),
                                        "Rule: One alone has no test_rule_one_alone"),
    "a decision with a test named for it": (lambda: cd.named_tests("decision", {"A skill"}, set(), set()),
                                            "Decision: A skill has no test_decision_a_skill"),
    "a deferred thing in its own file": (
        lambda: cd.deferred_outside({"docs/deferred/skill-evals.md": "# skill-evals\n\n**Revisit when** cheap.\n",
                                     "docs/design_document.md": "Intro.\n\nSkill evals would test each skill.\n"}),
        "docs/design_document.md describes skill-evals outside its deferred file: Skill evals would test each skill."),
}

DESIGN = cd.parse("### Feature: Notes\n\n```gherkin\nScenario: A\n```\n\n"
                  "### Feature: Caps\n\n```gherkin\nScenario: B\n```\n")
PARTS |= {  # an architecture's part and home
    "a design feature on a component's opening line": (lambda: cd.components(DESIGN,
        "## Shared\n\n### Stack\n\n## System: Skills\n\nRuns as skills.\n\n"
        "### Component: Notebook\n\nNotes\n\n- **A note** is dated.\n\n### Component: Checks\n\n- **A check** fails.\n"),
        "design's Feature: Caps sits on no component's opening line in the architecture"),
    "a design feature on one component alone": (lambda: cd.components(DESIGN,
        "## System: Skills\n\n### Component: Notebook\n\nNotes · Caps\n\n### Component: Pad\n\nNotes\n"),
        "design's Feature: Notes sits on 2 components' opening lines in the architecture"),
    "an opening line's name in the design": (lambda: cd.components(DESIGN,
        "## System: Skills\n\n### Component: Notebook\n\nNotes · Caps · Typo\n"),
        "architecture's Typo names no feature in the design"),
    "a component under a system": (lambda: cd.components(DESIGN,
        "## System: Skills\n\n### Component: Notebook\n\nNotes · Caps\n\n## Shared\n\n### Component: Loose\n"),
        "architecture's Component: Loose sits under no system"),
    "a heading under a system that is a component": (lambda: cd.components(DESIGN,
        "## System: Skills\n\n### Component: Notebook\n\nNotes · Caps\n\n### Tracing\n"),
        "architecture's Tracing under System: Skills is no component"),
    "a top heading that is Shared, a system or Why": (lambda: cd.components(DESIGN,
        "## System: Skills\n\n### Component: Notebook\n\nNotes · Caps\n\n## Workflow: Tracing\n"),
        "architecture's Workflow: Tracing is no system. A top heading is Shared, a system or Why"),
}


@pytest.mark.parametrize("part", PARTS)
def test_decision_a_home(part):
    check, failure = PARTS[part]
    assert check() == [failure]


def test_decision_a_test_s_name():
    """A test names a source of its kind, and a rename carries a name to its
    tests, links and baselines."""
    assert cd.source_tests({"test_scenario_nobody_wrote"}, {"scenario": set()}) == [
        "test_scenario_nobody_wrote names no scenario"]
    files = {"docs/design_document.md": "## Feature: Old\n\n```gherkin\nScenario: Old thing\n```\n"
                                        "[x](#feature-old) Old things.\n",
             "scripts/test_x.py": "def test_scenario_old_thing():\n",
             "scripts/scenario-baseline.txt": "# A skill runs it\nFeature: Old: Old thing\n",
             "docs/retro/1/a.md": "Old thing\n"}
    renamed = cd.rename(files, "Old thing", "New thing")
    assert renamed.get("scripts/test_x.py") == "def test_scenario_new_thing():\n"
    assert "Scenario: New thing" in renamed["docs/design_document.md"]
    assert "Old things." in renamed["docs/design_document.md"]
    assert "docs/retro/1/a.md" not in renamed
    assert renamed["scripts/scenario-baseline.txt"] == "# A skill runs it\nFeature: Old: New thing\n"
    renamed = cd.rename(files, "Feature: Old", "Feature: New")
    assert "[x](#feature-new)" in renamed["docs/design_document.md"]
    assert cd.rename(files, "Nothing here", "X") == {}


def test_decision_a_known_gap():
    """A baseline line is a part's only way out, and a line whose gap closed fails."""
    problems = cd.named_tests("workflow", {"Closing", "Opening"}, {"test_workflow_opening"}, {"Closing", "Opening"})
    assert problems == ["Opening  ← tested or gone: remove it from the workflow baseline"]
    assert cd.baseline("scripts/w.txt", "Closing\n")[1] == [
        "scripts/w.txt: Closing gives no reason; add \" — {reason}\", or a # line at the file's top"]
    assert cd.baseline("scripts/w.txt", "# A skill runs it\nClosing\n") == ({"Closing"}, [])


def test_decision_a_deferred_entry():
    assert cd.deferred_revisits({"docs/deferred/b.md": "# b\n\nWe never revisit.\n"}) == [
        "docs/deferred/b.md has no Revisit when line"]


MAY_NAME = [  # file, a link it may not hold
    ("docs/design_document.md", "architecture.md"),
    ("docs/architecture.md", "backlog/001-001-a.md"),
    ("scripts/check.py", "../docs/design_document.md"),
    ("docs/product_roadmap.md", "design_document.md"),
    ("docs/deferred/a.md", "../architecture.md"),
    ("docs/backlog/README.md", "../design_document.md"),
    ("docs/release/phase-1.md", "../design_document.md"),
]


@pytest.mark.parametrize("path, bad", MAY_NAME)
def test_decision_a_doc_s_links(path, bad):
    """A link in a code block, to the web or to the foundations names nothing."""
    assert cd.stream_names({path: f"[x]({bad})\n"}) == [f"{path} names {bad}, which it may not"]
    text = "```\n[x](architecture.md)\n```\n[w](https://example.com) [f](foundations.md) `[c](architecture.md)`\n"
    assert cd.stream_names({"docs/design_document.md": text}) == []


def test_decision_a_link():
    """A link lands on a file, and its anchor on its heading's GitHub slug."""
    assert cd.broken_links({"docs/a.md": "[gone](c.md)\n"}, lambda path: False) == [
        "docs/a.md links c.md, which is not there"]
    files = {"docs/a.md": "[bad](b.md#nope)\n", "docs/b.md": "## Plan\n"}
    assert cd.broken_links(files, lambda path: False) == ["docs/a.md links b.md#nope, which has no such heading"]
    files = {"docs/a.md": "# CDD — Design\n\n## Feature: Notes\n\n## Tech\n\n## Tech\n\n"
                          "## See [x](y.md)\n\n[a](#cdd--design) [b](#feature-notes) [c](#tech-1) [d](b.md#{feature}) [e](#see-x)\n"}
    assert cd.broken_links(files, lambda path: True) == []


def test_decision_a_workflow_with_steps_to_carry():
    """A workflow whose step links a feature runs on the skill of its name."""
    design = ("## Workflow: Tracing notes\n\n1. Trace ([Notes](#feature-notes))\n\nEnd: **Done**\n\n"
              "## Workflow: Talking\n\n1. Talk\n\n"
              "## Workflow: Releasing\n\n1. Ship ([Notes](#feature-notes))\n\n"
              "### Feature: Notes\n\n```gherkin\nScenario: A\n```\n")
    assert cd.workflow_skills(design, {"releasing", "editing-prose"}) == [
        "Workflow: Tracing notes links a feature, and no skill tracing-notes runs it"]


def test_decision_a_skill_s_paths():
    """A skill names no path: no link and no backticked path. Plain words pass."""
    text = ("Read the roadmap and run `cdd read design`.\n"
            "Run `uv run --script scripts/check.py`.\n"
            "Read [the design](../../../docs/design_document.md).\n"
            "Edit `CLAUDE.md`, then invoke `superpowers:brainstorming`.\n"
            "See [the guide](https://example.com) and [above](#above).\n"
            "Run `cdd` or and/or `main`.\n"
            "```\nscripts/check.py `x/y`\n```\n")
    assert cd.skill_paths({".claude/skills/x/SKILL.md": text}) == [
        ".claude/skills/x/SKILL.md names a path: Run `uv run --script scripts/check.py`.",
        ".claude/skills/x/SKILL.md names a path: Read [the design](../../../docs/design_document.md).",
        ".claude/skills/x/SKILL.md names a path: Edit `CLAUDE.md`, then invoke `superpowers:brainstorming`."]
    assert cd.skill_paths({"docs/a.md": "Run `scripts/check.py`.\n"}) == []
