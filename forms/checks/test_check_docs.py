"""Tests for check-docs.py. Run: uv run --with pytest pytest forms/checks/

Each test proves one decision. Its cases are rows, each named for what it
shows, so a failure names its case.
"""
import importlib.util
import os
from textwrap import dedent

import pytest

HERE = os.path.dirname(os.path.abspath(__file__))
spec = importlib.util.spec_from_file_location("check_docs", os.path.join(HERE, "check-docs.py"))
cd = importlib.util.module_from_spec(spec)
spec.loader.exec_module(cd)


def md(text):
    """A fixture doc written indented, as it reads."""
    return dedent(text).lstrip("\n")


EACH_SOURCE = {  # a source with no test, and the failure it gives
    "a journey": (lambda: cd.named_tests("journey", {"A day"}, set(), set()),
                  ["Journey: A day has no test_journey_a_day"]),
    "a workflow": (lambda: cd.named_tests("workflow", {"Closing"}, set(), set()),
                   ["Workflow: Closing has no test_workflow_closing"]),
    "a scenario": (lambda: cd.scenario_tests([("Feature: Notes", "Only")], set(), {}, set()),
                   ["Feature: Notes's scenario Only has no test_scenario_only, and no open ticket cites it"]),
    "a rule": (lambda: cd.named_tests("rule", {"One alone"}, set(), set()),
               ["Rule: One alone has no test_rule_one_alone"]),
    "a decision": (lambda: cd.named_tests("decision", {"A skill"}, set(), set()),
                   ["Decision: A skill has no test_decision_a_skill"]),
    "a baseline line": (lambda: cd.named_tests("workflow", {"Closing"}, set(), {"Closing"}), []),
}


@pytest.mark.parametrize("case", EACH_SOURCE)
def test_decision_each_source(case):
    check, problems = EACH_SOURCE[case]
    assert check() == problems


OUTLINE = md("""
    ```gherkin
    Feature: Notes
      Rule: Rows

        Scenario Outline: Many
          Given <a>

          Examples:
            | a |
    """)
RULE_S_SCENARIOS = {  # an outline's rows, and the failure they give
    "two rows count as two": ("    | 1 |\n    | 2 |\n```\n", []),
    "one row counts as one": ("    | 1 |\n```\n", ["design.md: Rule: Rows holds over 1 scenario; a rule needs two"]),
}


@pytest.mark.parametrize("case", RULE_S_SCENARIOS)
def test_decision_a_rule_s_scenarios(case):
    rows, problems = RULE_S_SCENARIOS[case]
    assert cd.rule_scenarios("design.md", OUTLINE + rows) == problems


def test_decision_a_deferred_thing():
    files = {"apps/cdd/docs/deferred/skill-evals.md": md("""
                 # skill-evals

                 **Revisit when** cheap.
                 """),
             "apps/cdd/docs/design_document.md": md("""
                 Intro.

                 Skill evals would test each skill.
                 """)}
    assert cd.deferred_outside(files) == [
        "apps/cdd/docs/design_document.md describes skill-evals outside its deferred file: Skill evals would test each skill."]


DESIGN = cd.parse(md("""
    ### Feature: Notes

    ```gherkin
    Scenario: A
    ```

    ### Feature: Caps

    ```gherkin
    Scenario: B
    ```
    """))
NOTEBOOK = md("""
    ## System: Skills

    ### Component: Notebook

    Notes · Caps
    """)
DESIGN_FEATURE = {  # an architecture, and the failure it gives
    "a feature on no opening line": (md("""
        ## Shared

        ### Stack

        ## System: Skills

        Runs as skills.

        ### Component: Notebook

        Notes

        - **A note** is dated.

        ### Component: Checks

        - **A check** fails.
        """), ["design's Feature: Caps sits on no component's opening line in the architecture"]),
    "a feature on two opening lines": (NOTEBOOK + "\n### Component: Pad\n\nNotes\n",
                                       ["design's Feature: Notes sits on 2 components' opening lines in the architecture"]),
    "an opening line naming no design feature": (NOTEBOOK.replace("Caps", "Caps · Typo"),
                                                  ["architecture's Typo names no feature in the design"]),
    "a component under Shared": (NOTEBOOK + "\n## Shared\n\n### Component: Loose\n",
                                 ["architecture's Component: Loose sits under no system"]),
    "a heading under a system that is no component": (NOTEBOOK + "\n### Tracing\n",
                                                      ["architecture's Tracing under System: Skills is no component"]),
    "a top heading that is no system": (NOTEBOOK + "\n## Workflow: Tracing\n",
                                        ["architecture's Workflow: Tracing is no system. A top heading is Shared, a system or Why"]),
}


@pytest.mark.parametrize("case", DESIGN_FEATURE)
def test_decision_a_design_feature(case):
    architecture, problems = DESIGN_FEATURE[case]
    assert cd.components(DESIGN, architecture) == problems


TEST_S_NAME = {  # a test, and the failure it gives
    "a test of no source": ("test_scenario_nobody_wrote", ["test_scenario_nobody_wrote names no scenario"]),
    "a near miss": ("test_scenario_old_thin", ["test_scenario_old_thin names no scenario; was it renamed to Old thing?"]),
    "a test with no prefix": ("test_old_thing", ["test_old_thing carries no prefix: " + ", ".join(k + "_" for k in cd.KINDS)]),
    "a test of its source": ("test_scenario_old_thing", []),
}


@pytest.mark.parametrize("case", TEST_S_NAME)
def test_decision_a_test_s_name(case):
    test, problems = TEST_S_NAME[case]
    assert cd.source_tests({test}, {"scenario": {"Old thing"}}) == problems


FILES = {"apps/cdd/docs/design_document.md": md("""
             ## Feature: Old

             ```gherkin
             Scenario: Old thing
             ```
             [x](#feature-old) Old things.
             """),
         "forms/checks/test_x.py": "def test_scenario_old_thing():\n",
         "forms/checks/scenario-baseline.txt": "# A skill runs it\nFeature: Old: Old thing\n",
         "apps/cdd/docs/retro/1/a.md": "Old thing\n"}
RENAME = {  # old name, new name, a file, and what it holds after
    "the test follows": ("Old thing", "New thing", "forms/checks/test_x.py", "def test_scenario_new_thing():\n"),
    "the prose follows": ("Old thing", "New thing", "apps/cdd/docs/design_document.md", FILES["apps/cdd/docs/design_document.md"]
                          .replace("Scenario: Old thing", "Scenario: New thing")),
    "the baseline line follows": ("Old thing", "New thing", "forms/checks/scenario-baseline.txt",
                                  "# A skill runs it\nFeature: Old: New thing\n"),
    "history keeps the old name": ("Old thing", "New thing", "apps/cdd/docs/retro/1/a.md", None),
    "a link follows its heading": ("Feature: Old", "Feature: New", "apps/cdd/docs/design_document.md",
                                   FILES["apps/cdd/docs/design_document.md"].replace("Old", "New", 1).replace("#feature-old", "#feature-new")),
    "a name the docs lack renames nothing": ("Nothing here", "X", "apps/cdd/docs/design_document.md", None),
}


@pytest.mark.parametrize("case", RENAME)
def test_decision_a_rename(case):
    old, new, path, after = RENAME[case]
    assert cd.rename(FILES, old, new).get(path) == after


KNOWN_GAP = {  # a check over a baseline, and what it gives
    "a line with its reason": (lambda: cd.baseline("forms/checks/w.txt", "Closing — a skill runs it\n"), ({"Closing"}, [])),
    "a # line gives the reason for all": (lambda: cd.baseline("forms/checks/w.txt", "# A skill runs it\nClosing\n"),
                                          ({"Closing"}, [])),
    "a line with no reason": (lambda: cd.baseline("forms/checks/w.txt", "Closing\n"), ({"Closing"}, [
        "forms/checks/w.txt: Closing gives no reason; add \" — {reason}\", or a # line at the file's top"])),
    "an empty baseline": (lambda: cd.baseline("forms/checks/w.txt", ""),
                          (set(), ["forms/checks/w.txt is empty: delete it and the code that reads it"])),
    "a line whose gap closed": (lambda: cd.named_tests("workflow", {"Opening"}, {"test_workflow_opening"}, {"Opening"}),
                                ["Opening  ← tested or gone: remove it from the workflow baseline"]),
}


@pytest.mark.parametrize("case", KNOWN_GAP)
def test_decision_a_known_gap(case):
    check, found = KNOWN_GAP[case]
    assert check() == found


def test_decision_a_deferred_entry():
    assert cd.deferred_revisits({"apps/cdd/docs/deferred/b.md": "# b\n\nWe never revisit.\n"}) == [
        "apps/cdd/docs/deferred/b.md has no Revisit when line"]


DOC_S_LINKS = {  # a file, its text, and the failure it gives
    "the design links the architecture": ("apps/cdd/docs/design_document.md", "[x](architecture.md)\n",
                                          ["apps/cdd/docs/design_document.md names architecture.md, which it may not"]),
    "the architecture links a ticket": ("apps/cdd/docs/architecture.md", "[x](backlog/001-001-a.md)\n",
                                        ["apps/cdd/docs/architecture.md names backlog/001-001-a.md, which it may not"]),
    "the code links the design": ("forms/checks/check.py", "[x](../docs/design_document.md)\n",
                                  ["forms/checks/check.py names ../docs/design_document.md, which it may not"]),
    "the roadmap links the design": ("apps/cdd/docs/product_roadmap.md", "[x](design_document.md)\n",
                                     ["apps/cdd/docs/product_roadmap.md names design_document.md, which it may not"]),
    "a deferred entry links the architecture": ("apps/cdd/docs/deferred/a.md", "[x](../architecture.md)\n",
                                                ["apps/cdd/docs/deferred/a.md names ../architecture.md, which it may not"]),
    "the backlog README links the design": ("apps/cdd/docs/backlog/README.md", "[x](../design_document.md)\n",
                                            ["apps/cdd/docs/backlog/README.md names ../design_document.md, which it may not"]),
    "the playbook links the design": ("apps/cdd/docs/release/phase-1.md", "[x](../design_document.md)\n",
                                      ["apps/cdd/docs/release/phase-1.md names ../design_document.md, which it may not"]),
    "the architecture links the design": ("apps/cdd/docs/architecture.md", "[x](design_document.md)\n", []),
    "a link in a code block": ("apps/cdd/docs/design_document.md", "```\n[x](architecture.md)\n```\n", []),
    "a link in inline code": ("apps/cdd/docs/design_document.md", "`[c](architecture.md)`\n", []),
    "a link to the web": ("apps/cdd/docs/design_document.md", "[w](https://example.com)\n", []),
    "a link to the foundations": ("apps/cdd/docs/design_document.md", "[f](../foundations.md)\n", []),
    "a link to the forms": ("apps/cdd/docs/design_document.md", "[f](../../../forms/forms.md)\n", []),
}


@pytest.mark.parametrize("case", DOC_S_LINKS)
def test_decision_a_doc_s_links(case):
    path, text, problems = DOC_S_LINKS[case]
    assert cd.stream_names({path: text}) == problems


HEADINGS = md("""
    # CDD — Design

    ## Feature: Notes

    ## Tech

    ## Tech

    ## See [x](y.md)
    """)
LINK = {  # a doc's text, and the failure it gives
    "a missing file": ("[gone](c.md)\n", ["docs/a.md links c.md, which is not there"]),
    "a missing heading": ("[bad](b.md#nope)\n", ["docs/a.md links b.md#nope, which has no such heading"]),
    "a heading with a dash": (HEADINGS + "[a](#cdd--design)\n", []),
    "a heading with a colon": (HEADINGS + "[b](#feature-notes)\n", []),
    "a repeated heading": (HEADINGS + "[c](#tech-1)\n", []),
    "a heading holding a link": (HEADINGS + "[e](#see-x)\n", []),
    "a placeholder": (HEADINGS + "[d](b.md#{feature})\n", []),
}


@pytest.mark.parametrize("case", LINK)
def test_decision_a_link(case):
    text, problems = LINK[case]
    files = {"docs/a.md": text, "docs/b.md": "## Plan\n"}
    assert cd.broken_links(files, lambda path: path in ("docs/b.md", "docs/y.md")) == problems


def test_decision_a_workflow_with_steps_to_carry():
    """A workflow whose step links a feature runs on the skill of its name."""
    design = md("""
        ## Workflow: Tracing notes

        1. Trace ([Notes](#feature-notes))

        ## Workflow: Talking

        1. Talk

        ## Workflow: Releasing

        1. Ship ([Notes](#feature-notes))

        ### Feature: Notes

        ```gherkin
        Scenario: A
        ```
        """)
    assert cd.workflow_skills(design, {"releasing", "editing-prose"}) == [
        "Workflow: Tracing notes links a feature, and no skill tracing-notes runs it"]


SKILL_S_PATHS = {  # a skill line, and whether it names a path
    "a cdd verb": ("Read the roadmap and run `cdd read design`.", False),
    "a script path": ("Run `uv run --script forms/checks/check.py`.", True),
    "a link to a doc": ("Read [the design](../../../docs/design_document.md).", True),
    "a backticked file": ("Edit `CLAUDE.md`, then invoke `superpowers:brainstorming`.", True),
    "a web link and an anchor": ("See [the guide](https://example.com) and [above](#above).", False),
    "plain words with a slash": ("Run `cdd` or and/or `main`.", False),
    "a path in a code block": ("```\nscripts/check.py `x/y`\n```", False),
}


@pytest.mark.parametrize("case", SKILL_S_PATHS)
def test_decision_a_skill_s_paths(case):
    line, named = SKILL_S_PATHS[case]
    found = cd.skill_paths({".claude/skills/x/SKILL.md": line + "\n"})
    assert found == ([f".claude/skills/x/SKILL.md names a path: {line}"] if named else [])
