"""Tests for check-caps.py. Run: uv run --with pytest pytest scripts/"""
import importlib.util
import os

import pytest

HERE = os.path.dirname(os.path.abspath(__file__))
spec = importlib.util.spec_from_file_location("check_caps", os.path.join(HERE, "check-caps.py"))
cc = importlib.util.module_from_spec(spec)
spec.loader.exec_module(cc)

DESIGN = """## Journey: Long

| # | Workflow | Role | Leaves |
|---|---|---|---|
| 1 | [One](#workflow-one) | Dev | **B** |
| 2 | [Two](#workflow-two) | Dev | **C** |
| 3 | [Three](#workflow-three) | Dev | **D** |

## Workflow: Short

1. Do it
1. Do it again

## Workflow: Long steps

1. Do it ([Feature: Caps](#feature-caps))
1. Do it again ([Feature: Caps](#feature-caps)) ([Feature: Other](#feature-other))
1. Once more

### Feature: Caps

```gherkin
Feature: Caps

  Rule: A ticket takes two new scenarios at most

    Scenario: First
      Given a

  Rule: A ticket is at most one feature on one system and 5 points

    Scenario: Second
      Given a

    Scenario: Third
      Given a
```
"""

ARCHITECTURE = """## System: Skills

### Component: Caps

Caps

- **One** decision.
- **Two** decisions,
  wrapped onto a second line.

| form                 | cap                    | upstream              |
|---|---|---|
| journey              | 2 workflows            | the journey           |
| workflow             | 2 steps                | its journey           |
| workflow step        | 1 feature              | the step              |
| feature              | 2 scenarios or 1 rules | its workflows         |
| architecture section | 1 decisions            | its component or system |
| decision             | 2 sentences            | the decision          |

### Component: Long

- **A long one** holds `a.b`. It says more.[^why-x] And more again.

## Contents

- [System: Skills](#system-skills)
- [Component: Caps](#component-caps)
"""

WARNINGS = {
    "journey": "design: Journey: Long has 3 workflows, past its cap of 2. The owner decides whether to redesign the journey",
    "workflow": "design: Workflow: Long steps has 3 steps, past its cap of 2. The owner decides whether to redesign its journey",
    "workflow step": "design: Workflow: Long steps step 2 has 2 features, past its cap of 1. "
                     "The owner decides whether to redesign the step",
    "feature": "design: Feature: Caps has 3 scenarios, past its cap of 2. The owner decides whether to redesign its workflows",
    "decision": "architecture: Component: Long: A long one has 3 sentences, past its cap of 2. "
                "The owner decides whether to redesign the decision",
    "architecture section": "architecture: Component: Caps has 2 decisions, past its cap of 1. "
                            "The owner decides whether to redesign its component or system",
}


WARNED = cc.form_warnings("design", DESIGN, "architecture", ARCHITECTURE)
FORM_PAST_ITS_CAP = {  # a check, and what it gives
    **{f"a {form} past its cap": (lambda w=w: [x for x in WARNED if x == w], [w]) for form, w in WARNINGS.items()},
    "a form at its cap": (lambda: [w for w in WARNED if "Short" in w or "Contents" in w], []),
    "a wrapped line counts in its decision": (lambda: cc.decision_sentences(["- **A** is x.", "  More here."]), [("A", 2)]),
    "a line after a blank one counts in none": (lambda: cc.decision_sentences(["- **A** is x.", "", "  Loose."]), [("A", 1)]),
    "a nested bullet counts on its own": (lambda: cc.decision_sentences(["- **B** is y.", "  - **C** is z. More."]),
                                          [("B", 1), ("C", 2)]),
    "a footnote or a code span ends no sentence": (
        lambda: cc.decision_sentences(["- **D** holds `a. b`.[^why-d] More."]), [("D", 2)]),
}


@pytest.mark.parametrize("case", FORM_PAST_ITS_CAP)
def test_decision_a_form_past_its_cap(case):
    check, found = FORM_PAST_ITS_CAP[case]
    assert check() == found


SHORT_OUTLINE = """```gherkin
  Scenario Outline: Many
    Given <a>

    Examples:
      | a |
"""
SHORT = {  # an outline's rows, and the warning they give
    "two rows warn": ("      | 1 |\n      | 2 |\n```\n", [
        "design.md: Scenario Outline: Many has 2 Examples rows, under 3. The owner decides whether to split it into scenarios"]),
    "three rows are quiet": ("      | 1 |\n      | 2 |\n      | 3 |\n```\n", []),
}


@pytest.mark.parametrize("case", SHORT)
def test_decision_a_short_outline(case):
    rows, warned = SHORT[case]
    assert cc.short_outlines("design.md", SHORT_OUTLINE + rows) == warned


def test_rule_a_ticket_takes_two_new_scenarios_at_most():
    old = "```gherkin\n  Scenario: Kept\n  Scenario: Old name\n```\n"
    base = old + "```gherkin\n  Scenario: Another ticket's\n```\n"
    now = "```gherkin\n  Scenario: Kept\n  Scenario: New name\n  Scenario: Added\n  Scenario: Third\n  Scenario: Another ticket's\n```\n"
    added = cc.branch_adds(old, base, now)
    assert added == ["Added", "New name", "Third"]
    assert cc.new_scenario_warnings(added, cc.new_scenario_cap(DESIGN)) == [
        "This branch adds 3 scenarios since its plan's tag, past its cap of 2: Added, New name, Third. "
        "The owner decides: the ticket is redesigned in place, or the third goes to its retro"]


def test_rule_a_ticket_is_at_most_one_feature_on_one_system_and_5_points():
    tickets = {"docs/backlog/001-001-a.md": "**Feature.** x · **Estimate.** 8 — big",
               "docs/backlog/001-002-b.md": "**Feature.** x · **Estimate.** 5 — fits"}
    assert cc.point_warnings(tickets, cc.point_cap(DESIGN)) == [
        "docs/backlog/001-001-a.md is 8 points, past its cap of 5. The owner decides whether to redesign its feature"]
