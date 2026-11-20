"""Tests for cdd.py. Run: uv run --with pytest pytest scripts/"""
import contextlib
import importlib.util
import os
import re
import subprocess
import sys
import tomllib

import pytest

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
spec = importlib.util.spec_from_file_location("cdd", os.path.join(HERE, "cdd.py"))
cdd = importlib.util.module_from_spec(spec)
spec.loader.exec_module(cdd)

TEMPLATES = ("ticket", "retro-entry", "release-playbook", "foundations")


@pytest.fixture
def root(tmp_path, monkeypatch):
    os.makedirs(tmp_path / "docs/templates")
    for name in TEMPLATES:
        (tmp_path / f"docs/templates/{name}.md").write_text(f"# {name}\n")
    monkeypatch.setattr(cdd, "ROOT", str(tmp_path))
    return tmp_path


CDD_NEW = {  # its args, and the path it lands at. A row with None is a case in the decision's table
    "A ticket lands in the backlog": (["ticket", "001-012-foo"], "docs/backlog/001-012-foo.md"),
    "A retro entry lands in its phase": (["retro-entry", "1", "001-012-foo"], "docs/retro/1/001-012-foo.md"),
    "A playbook lands by its phase": (["release-playbook", "1"], "docs/release/phase-1.md"),
    "The foundations land in docs": (["foundations"], "docs/foundations.md"),
    "A doc that exists": (["ticket", "001-012-mine"], None),
    "A doc with no template": (["product_roadmap"], None),
    "A doc cdd doesn't know": (["roadmap"], None),
    "A doc missing its name": (["ticket"], None),
    "A doc missing its phase": (["release-playbook"], None),
    "A name that leaves its folder": (["ticket", "../escape"], None),
    "A phase that isn't a number": (["release-playbook", "x"], None),
}


@pytest.mark.parametrize("case", CDD_NEW)
def test_decision_cdd_new(root, capsys, case):
    args, path = CDD_NEW[case]
    (root / "docs/backlog").mkdir()
    (root / "docs/backlog/001-012-mine.md").write_text("mine\n")
    if path:
        cdd.main(["new", *args])
        assert (root / path).exists() and (root / path).read_text() == f"# {args[0]}\n"
        assert capsys.readouterr().out.strip() == path
    else:
        with pytest.raises(SystemExit) as failed:
            cdd.main(["new", *args])
        assert failed.value.code not in (0, None)
        assert (root / "docs/backlog/001-012-mine.md").read_text() == "mine\n"


def test_decision_each_script():
    with open(os.path.join(ROOT, "pyproject.toml"), "rb") as handle:
        assert tomllib.load(handle)["project"].get("scripts", {}).get("cdd") == "cdd:main"
    where = open(os.path.join(ROOT, "docs/architecture.md"), encoding="utf-8").read()
    table = where.split("### Where", 1)[1].split("\n\n", 2)[1]
    for path in re.findall(r"^\|[^|]+\| `([^`]+)`", table, re.M):
        assert any(held.startswith(path) for held in [*cdd.DOCS.values(), *cdd.FOLDERS.values()]), path
    usage = subprocess.run(["uv", "run", "-q", "--project", ROOT, "cdd"], capture_output=True, text=True)
    assert usage.returncode == 2 and "uv run cdd" in usage.stderr


def step(code):
    return [sys.executable, "-c", f"print('ran {code}'); raise SystemExit({code})"]


CDD_CHECK = {  # its args, each step's exit code, the steps that run, and whether it fails
    "all pass": (["check"], (0, 0, 0), ["ran 0", "ran 0", "ran 0"], False),
    "a failure exits 1": (["check"], (1, 0, 0), ["ran 1", "ran 0", "ran 0"], True),
    "each step runs past a failure": (["check"], (0, 1, 1), ["ran 0", "ran 1", "ran 1"], True),
    "check caps runs the caps alone": (["check", "caps"], (1, 1, 0), ["ran 0"], False),
}


@pytest.mark.parametrize("case", CDD_CHECK)
def test_decision_cdd_check(monkeypatch, capfd, case):
    args, codes, ran, fails = CDD_CHECK[case]
    monkeypatch.setattr(cdd, "STEPS", {t: (t, step(c)) for t, c in zip(("tests", "docs", "caps"), codes)})
    with pytest.raises(SystemExit) if fails else contextlib.nullcontext() as failed:
        cdd.main(args)
    if fails:
        assert failed.value.code not in (0, None)
    assert [line for line in capfd.readouterr().out.split("\n") if line.startswith("ran")] == ran


DESIGN = """# Design

## Feature: Splitting the work

Split it.

```gherkin
## Only in a fence
```

### A step

Its detail.

## Feature: Next

Next.
"""
HEADINGS = ["Design", "Feature: Splitting the work", "A step", "Feature: Next"]

CDD_READ = {  # its args, and what it prints or the names its failure lists
    "A section prints to the next heading of its level": (
        ["design_document", "Feature: Splitting the work"],
        DESIGN[DESIGN.index("## Feature: Splitting"):DESIGN.index("## Feature: Next")]),
    "A whole doc prints": (["design_document"], DESIGN),
    "Each of a phase's retro files prints": (
        ["retro-entry", "1"], "== docs/retro/1/a.md\nA\n\n== docs/retro/1/b.md\nB\n"),
    "A heading only inside a fence": (["design_document", "Only in a fence"], HEADINGS),
    "A heading that doesn't exist": (["design_document", "Feature: Missing"], HEADINGS),
    "A doc name with no place": (["design"], list(cdd.DOCS)),
    "A file that doesn't exist": (["retro-entry", "1", "c"], ["a.md", "b.md"]),
}


@pytest.mark.parametrize("case", CDD_READ)
def test_decision_cdd_read(root, capsys, case):
    args, expected = CDD_READ[case]
    (root / "docs/design_document.md").write_text(DESIGN)
    os.makedirs(root / "docs/retro/1")
    (root / "docs/retro/1/a.md").write_text("A\n")
    (root / "docs/retro/1/b.md").write_text("B\n")
    if isinstance(expected, str):
        cdd.main(["read", *args])
        assert capsys.readouterr().out == expected
    else:
        with pytest.raises(SystemExit) as failed:
            cdd.main(["read", *args])
        assert isinstance(failed.value.code, str)
        listed = failed.value.code.rsplit(". ", 1)[1]  # what exists, after the reason
        assert all(name in listed for name in expected) and "Only in a fence" not in listed
