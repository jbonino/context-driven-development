# {Product} — Architecture

How {Product} is built, shaped around the design.

- [Shared](#shared)
- [System: {Name}](#system-name)
  - [Component: {Name}](#component-name)
- [Why](#why)

## Shared

### Stack

| Unit | Tech | Carries |
|---|---|---|
| {System} | {Tech} | {Its components} |

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

### Checkpoints

| Checkpoint | Evidence | Left by |
|---|---|---|
| {Checkpoint} | {What shows it in the repo} | {Workflow} |

## System: {Name}

- **{Subject}** {a decision every component here keeps}.

### Component: {Name}

{Feature} · {Feature}

- **{Subject}** {its decision}.[^why-{slug}]

## Why

Why each decision that's hard to undo holds, and the options it beat.

[^why-{slug}]: {The reason.} **Other considerations:** {Each option it beat, and why.}

<!--
Copy this to the architecture. Delete this comment.

| Slot | Content |
|---|---|
| Shared | The decisions every system shares |
| Where | A path for each doc in the foundations' Where |
| Testing strategy | This product's levels and runners. CDD's kinds sit above them. A lower level runs faster and breaks less |
| Checkpoints | The design's checkpoints, with what shows each in the repo |
| System | What its components run on. A Developer knows from it whether to open a skill, a script or an app |
| Component | A noun for what it builds. Its opening line names each design feature it builds, verbatim. One that builds none opens with its decisions. It holds 4 decisions at most |
| Subject | A bold subject opens each bullet. Rows that share columns make a table |
| Why | One footnote per decision that's hard to undo, naming every option it beat |

A decision names the design alone. It names no file paths, functions,
commands or addresses. The docs check warns past a section's cap, and the
owner decides.
-->
