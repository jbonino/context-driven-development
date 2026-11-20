# 001-005 — Read a doc by name — **Ad hoc**

**Feature.** [Reading a doc by name](../design_document.md#feature-reading-a-doc-by-name) · **System.** [Scripts](../architecture.md#scripts) · **Estimate.** 2 — one verb over the paths 001-004 holds · **Model.** Sonnet 5.5, low — a heading parser

`uv run cdd read design "Feature: Splitting the work"` prints that
section, so a skill reads part of a doc with no path or grep.

## Acceptance criteria

- [Reading a doc by name](../design_document.md#feature-reading-a-doc-by-name)

## Workflow steps

- [Designing a phase](../design_document.md#workflow-designing-a-phase) step 1: the brainstorm reads by name
- [Architecting a phase](../design_document.md#workflow-architecting-a-phase) step 1: the brainstorm reads by name

## Build notes

- Waits on 001-004 for `cdd.py` and its paths.
- Headings inside a gherkin fence don't count.
