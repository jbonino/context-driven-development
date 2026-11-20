# Context Driven Development
Humans please read this [article](https://jbonino.github.io/context-driven-development/articles/)

1. read [foundations](docs/foundations.md).
1. read [design](docs/design_document.md).
1. read [architecture](docs/architecture.md).

## Setup

| Need | How |
|---|---|
| The repo | `git clone https://github.com/jbonino/context-driven-development.git` |
| [Claude Code](https://claude.com/claude-code) | Install it, then run `claude` in the repo |
| The superpowers plugin | In Claude Code, run `/plugin install superpowers@claude-plugins-official` |
| [uv](https://docs.astral.sh/uv/) | Runs the scripts. It fetches their Python |
| [GitHub CLI](https://cli.github.com/) | `gh auth login`. The skills open PRs with it |

The CDD skills load from `.claude/skills/` with no install.

## Commands

| Command | Does |
|---|---|
| `uv run cdd check` | Runs the scripts' tests, then the checks. Fails on a fact out of place or a broken link. Warns on a form past its cap |
| `uv run cdd check rename "{old}" "{new}"` | Renames a scenario, feature, workflow, journey or rule, with its links and tests |
| `scripts/save-transcripts.sh` | Saves this repo's Claude Code and Copilot sessions to `docs/retro/raw/`, gitignored. Run it before each merge |
| `uv run --script scripts/mine-transcripts.py {n}` | Mines phase `n`'s saved sessions for the phase-close retro |
