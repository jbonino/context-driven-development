#!/usr/bin/env -S uv run --script
# /// script
# requires-python = ">=3.13"
# dependencies = []
# ///
"""Runs `uv run cdd check`, until the skills move onto it.

Run: uv run --script scripts/check.py
"""
import os
import subprocess
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

if __name__ == "__main__":
    sys.exit(subprocess.run(["uv", "run", "-q", "--project", ROOT, "cdd", "check"], cwd=ROOT).returncode)
