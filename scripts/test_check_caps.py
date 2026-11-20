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
    "architecture section": "architecture: Component: Caps has 2 decisions, past its cap of 1. "
                            "The owner decides whether to redesign its component or system",
}


def test_decision_a_form_past_its_cap():
    """A cap is read from the architecture's table, so a form at its cap is
    quiet. An outline under three rows warns too."""
    warned = cc.form_warnings("design", DESIGN, "architecture", ARCHITECTURE)
    assert all(w in warned for w in WARNINGS.values())
    assert len(warned) == 6
    assert not any("Short" in w or "Contents" in w for w in warned)
    design = ("```gherkin\n  Scenario Outline: Two\n    Given <a>\n\n    Examples:\n      | a |\n      | 1 |\n"
              "      | 2 |\n\n  Scenario Outline: Three\n    Given <a>\n\n    Examples:\n      | a |\n"
              "      | 1 |\n      | 2 |\n      | 3 |\n```\n")
    assert cc.short_outlines("design.md", design) == [
        "design.md: Scenario Outline: Two has 2 Examples rows, under 3. "
        "The owner decides whether to split it into scenarios"]


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
