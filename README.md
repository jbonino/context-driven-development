# Context Driven Development

Start with [foundations](docs/foundations.md).

## Commands

Needs [uv](https://docs.astral.sh/uv/).

| Command | Does |
|---|---|
| `uv run --with pytest pytest scripts/` | Runs the scripts' tests |
| `scripts/save-transcripts.sh` | Saves this repo's Claude Code and Copilot sessions to `docs/retro/raw/`, gitignored. Run it before each merge |
| `uv run --script scripts/mine-transcripts.py {n}` | Mines phase `n`'s saved sessions for the phase-close retro |
