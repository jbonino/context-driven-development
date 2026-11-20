# 001-004 — Start a doc from its template — **Ad hoc**

**System.** [Scripts](../architecture.md#system-scripts) · **Estimate.** 3 — a new entry point, and `check` moves under it · **Model.** Sonnet 5.5, medium — a small CLI over files

A user runs `uv run cdd new ticket 001-012-foo` and gets the ticket in its
place with its path printed. `uv run cdd check` runs the checks, as
`scripts/check.py` does today.

## Acceptance criteria

- [`cdd new`](../architecture.md#component-doc-commands)
- [`cdd check`](../architecture.md#component-doc-commands)
- [Each script](../architecture.md#system-scripts)
- [The session scripts](../architecture.md#system-scripts), for `cdd mine` alone

## Workflow steps

- None

## Build notes

- Waits on 001-008 for the decision kind.
- `scripts/cdd.py` holds the Where table's paths in one dict and dispatches the verbs.
- Keep `check.py` until 001-009 moves the skills off it.
- Add a foundations template. It holds What, Why, Who, Where and How, each with a comment.
