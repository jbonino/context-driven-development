# Context Driven Development

How a team of people and agents turn a customer's feedback into a plan that
delivers a product and learns from each cycle. Start with
[foundations](docs/foundations.md).

| Directory | Holds |
|---|---|
| `.claude/skills/` | The phase skills |
| `docs/` | CDD's own foundations, design, architecture, roadmap, backlog, deferred and retros |
| `docs/templates/` | Blanks a new team copies into its own `docs/` |
| `presentations/` | A slide deck that explains the method |
| `scripts/` | Saving and mining agent sessions |

## Two repos

A ticket spans this repo and a team repo. This repo holds the docs, and the
team repo holds the code. Skills refer to the team repo's own conventions for
its branch and PR.

| Part | Lives in | Merges |
|---|---|---|
| Docs branch | This repo, from `branching-from-main` | After the team PR merges |
| Code branch and PR | The team repo | Per that repo's conventions |
| Release playbook | `docs/release/phase-{n}.md` | Checked by `releasing` |

## Commands

Needs [uv](https://docs.astral.sh/uv/).

| Command | Does |
|---|---|
| `uv run --with pytest pytest scripts/` | Runs the scripts' tests |
| `scripts/save-transcripts.sh` | Saves this repo's Claude Code and Copilot sessions to `docs/retro/raw/`, gitignored. Run it before each merge |
| `uv run --script scripts/mine-transcripts.py {n}` | Mines phase `n`'s saved sessions for the phase-close retro |
