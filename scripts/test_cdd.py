"""Tests for cdd.py. Run: uv run --with pytest pytest scripts/"""
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


CDD_NEW = {  # its args, and the path it lands at or None where it fails
    "a ticket lands in the backlog": (["ticket", "001-012-foo"], "docs/backlog/001-012-foo.md"),
    "a retro entry lands in its phase": (["retro-entry", "1", "001-012-foo"], "docs/retro/1/001-012-foo.md"),
    "a playbook lands by its phase": (["release-playbook", "1"], "docs/release/phase-1.md"),
    "the foundations land in docs": (["foundations"], "docs/foundations.md"),
    "a doc that exists fails": (["ticket", "001-012-mine"], None),
    "a doc with no template fails": (["product_roadmap"], None),
    "a doc cdd doesn't know fails": (["roadmap"], None),
    "a doc missing its name fails": (["ticket"], None),
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
        assert any(held.startswith(path) for held in cdd.DOCS.values()), path
    usage = subprocess.run(["uv", "run", "-q", "--project", ROOT, "cdd"], capture_output=True, text=True)
    assert usage.returncode == 2 and "uv run cdd" in usage.stderr


def step(code):
    return [sys.executable, "-c", f"print('ran {code}'); raise SystemExit({code})"]


CDD_CHECK = {  # its args, each step's exit code, what prints, and its exit
    "all pass": (["check"], (0, 0, 0), ["== tests", "ran 0", "== docs", "ran 0", "== caps", "ran 0"], None),
    "a failure exits 1 and names it": (["check"], (1, 0, 0),
                                       ["== tests", "ran 1", "== docs", "ran 0", "== caps", "ran 0"], "Failed: tests"),
    "each failure is named": (["check"], (0, 1, 1),
                              ["== tests", "ran 0", "== docs", "ran 1", "== caps", "ran 1"], "Failed: docs, caps"),
    "check caps runs the caps alone": (["check", "caps"], (1, 1, 0), ["== caps", "ran 0"], None),
}


@pytest.mark.parametrize("case", CDD_CHECK)
def test_decision_cdd_check(monkeypatch, capfd, case):
    args, codes, printed, exits = CDD_CHECK[case]
    monkeypatch.setattr(cdd, "STEPS", [(t, step(c)) for t, c in zip(("tests", "docs", "caps"), codes)])
    if exits:
        with pytest.raises(SystemExit) as failed:
            cdd.main(args)
        assert failed.value.code == exits
    else:
        cdd.main(args)
    assert capfd.readouterr().out.split("\n")[:-1] == printed
