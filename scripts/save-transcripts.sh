#!/usr/bin/env bash
# Copies every Claude Code and Copilot session of this repo, worktrees and
# subagents included, into the folder it's given (gitignored) for the phase-close retro to mine.
# Run: uv run cdd save
# Claude Code deletes transcripts after 30 days, so run it at least that often.
# Base64 images are stripped. A session changed since its last copy is copied again.
set -euo pipefail
root="$(dirname "$(git -C "$(dirname "$0")" rev-parse --path-format=absolute --git-common-dir)")"
slug="$(printf '%s' "$root" | sed 's/[^A-Za-z0-9]/-/g')"
out="$1"
mkdir -p "$out"

save() { # save <transcript> <dest.jsonl.gz>
  [[ -f "$2" && "$2" -nt "$1" ]] && return
  mkdir -p "$(dirname "$2")"
  sed -E 's/"data":"[A-Za-z0-9+\/=]{200,}"/"data":"<image>"/g' "$1" | gzip -n >"$2"
}

count=0
for dir in "$HOME/.claude/projects/$slug" "$HOME/.claude/projects/$slug"--claude-worktrees-*; do
  [[ -d "$dir" ]] || continue
  for t in "$dir"/*.jsonl; do
    [[ -f "$t" ]] || continue
    sid="$(basename "$t" .jsonl)"
    day="$(grep -m1 -o '"timestamp":"[0-9-]\{10\}' "$t" | cut -d'"' -f4 || true)"
    name="${day:-undated}-$sid"
    save "$t" "$out/$name.jsonl.gz"
    for a in "$dir/$sid"/subagents/*.jsonl; do
      [[ -f "$a" ]] && save "$a" "$out/$name/$(basename "$a").gz"
    done
    count=$((count + 1))
  done
done
echo "$count Claude Code sessions in ${out#$root/}"
uv run --script "$root/scripts/copilot_to_claude.py" "$root" "$out"
