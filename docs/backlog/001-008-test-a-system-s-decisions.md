# 001-008 — Test a system's decisions — **Ad hoc**

**System.** [Scripts](../architecture.md#scripts) · **Estimate.** 3 — a new test kind, its baseline, and one test · **Model.** Sonnet 5.5, medium — follows the other kinds

Each decision has a `decision_` test or a baseline line with its reason.
A skill that names a path fails its decision's test.

## Acceptance criteria

- The checks hold the Decision kind in the [Testing strategy](../architecture.md#testing-strategy) as they hold the others.
- `test_decision_a_skill_s_paths` fails on a skill line that names a doc, a script or an app's file by its path.
- Each other decision sits in the decision baseline with its reason.

## Workflow steps

- None

## Build notes

- `test_decision_a_skill_s_paths` sits in the baseline until 001-009 lands, since today's skills name paths.
- A path is a link or a backticked path. Plain words like "the roadmap" pass.
- A decision's subject is its bold opening words.
