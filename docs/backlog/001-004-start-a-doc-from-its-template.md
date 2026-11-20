# 001-004 — Start a doc from its template — **Ad hoc**

**Feature.** [Starting a doc from its template](../design_document.md#feature-starting-a-doc-from-its-template) · **System.** [Scripts](../architecture.md#scripts) · **Estimate.** 3 — a new entry point, and `check` moves under it · **Model.** Sonnet 5.5, medium — a small CLI over files

A skill runs `uv run cdd new ticket 001-010-foo` and gets the ticket in
its place with its path printed. `uv run cdd check` runs the checks, as
`scripts/check.py` does today.

## Acceptance criteria

- [Starting a doc from its template](../design_document.md#feature-starting-a-doc-from-its-template)
- `cdd check` prints and exits as `scripts/check.py` does. `cdd check caps` does the same for `check-caps.py`.
- `cdd mine {n}` runs `mine-transcripts.py` for phase n.

## Workflow steps

- [Writing the tickets](../design_document.md#workflow-writing-the-tickets) step 5: the playbook starts from its template

## Build notes

- `pyproject.toml` declares a `cdd` script. `scripts/cdd.py` holds the Where table's paths in one dict and dispatches the verbs.
- `check` calls what `scripts/check.py` runs. Keep `check.py` until 001-009 moves the skills off it.
- Add a foundations template. It holds What, Why, Who, Where and How, each with a comment.
