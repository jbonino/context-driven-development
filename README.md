# Context Driven Development

Start with [foundations](docs/foundations.md).

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
| `uv run --with pytest pytest scripts/` | Runs the scripts' tests |
| `scripts/save-transcripts.sh` | Saves this repo's Claude Code and Copilot sessions to `docs/retro/raw/`, gitignored. Run it before each merge |
| `uv run --script scripts/mine-transcripts.py {n}` | Mines phase `n`'s saved sessions for the phase-close retro |
