# {Product} — Architecture

How {Product} is built, shaped around the design.

- [Foundations](#foundations)
- [{System}](#system)
- [Why](#why)

## Foundations

### Stack

| Unit | Tech | Carries |
|---|---|---|
| {System} | {Tech} | {Its features} |

### Where

| Doc | Path |
|---|---|
| {Doc} | {Path} |

### Constraints

- **{Subject}** {one fact every system keeps}.[^why-{slug}]

### Testing strategy

| Level | Runner | Runs |
|---|---|---|
| {Level} | {Runner and its prefix} | {Which kinds, and where} |

- **{Subject}** {one fact about how this product tests}.

## {System}

{Feature} · {Feature}

Runs on {tech}.

### Feature: {Name}

- **{Subject}** {its decision}.[^why-{slug}]

## Why

Why each decision that's hard to undo holds, and the options it beat.

[^why-{slug}]: {The reason.} **Other considerations:** {Each option it beat, and why.}

<!--
Copy this to the architecture. Delete this comment.

| Slot | Content |
|---|---|
| Foundations | The decisions every system shares |
| Where | A path for each doc in the foundations' Where |
| Testing strategy | This product's levels and runners. CDD's kinds sit above them. A lower level runs faster and breaks less |
| System | What its features run on. Its opening line lists each of its features. A Developer knows from it whether to open a skill, a script or an app |
| Feature | The design's workflow or feature name, verbatim. Only one with a decision of its own takes a heading |
| Subject | A bold subject opens each bullet. Rows that share columns make a table |
| Why | One footnote per decision that's hard to undo, naming every option it beat |

A decision names the design alone. It names no file paths, functions,
commands or addresses. The docs check warns past a section's cap, and the
owner decides.
-->
