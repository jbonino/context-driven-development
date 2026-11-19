#!/usr/bin/env -S uv run --script
# /// script
# requires-python = ">=3.13"
# dependencies = []
# ///
"""Runs the scripts' tests, then the checks. A failure exits 1. A cap
warning prints and exits 0.

Run: uv run --script scripts/check.py
"""
import os
import subprocess
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
STEPS = [
    ("The scripts' tests", ["uv", "run", "-q", "--with", "pytest", "pytest", "-q", HERE]),
    ("Each fact in its place", ["uv", "run", "--script", os.path.join(HERE, "check-docs.py")]),
    ("Each form under its cap. Warns, never fails", ["uv", "run", "--script", os.path.join(HERE, "check-caps.py")]),
]


def main():
    failed = []
    for title, command in STEPS:
        print(f"== {title}", flush=True)
        if subprocess.run(command, cwd=os.path.dirname(HERE)).returncode:
            failed.append(title)
    if failed:
        sys.exit(f"Failed: {', '.join(failed)}")


if __name__ == "__main__":
    main()
