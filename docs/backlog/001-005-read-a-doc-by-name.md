# 001-005 — Read a doc by name — **Ad hoc**

**System.** [Scripts](../architecture.md#system-scripts) · **Estimate.** 2 — one verb over the paths 001-004 holds · **Model.** Sonnet 5.5, low — a heading parser

`uv run cdd read design_document "Feature: Splitting the work"` prints that
section, so a skill reads part of a doc with no path or grep.

## Acceptance criteria

- `test_decision_cdd_read` holds **`cdd read`**: a section, a whole doc, and each of a phase's retro files print. A heading only inside a fence, a missing heading, and a doc name with no place each fail and list what exists.

## Workflow steps

- None

## Build notes

- Waits on 001-004 for `cdd.py` and its paths.
