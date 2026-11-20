"""Tests for cdd.py. Run: uv run --with pytest pytest forms/checks/"""
import ast
import contextlib
import importlib.util
import os
import re
import subprocess
import sys
import tomllib

import pytest

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(os.path.dirname(HERE))
spec = importlib.util.spec_from_file_location("cdd", os.path.join(ROOT, "forms/cdd.py"))
cdd = importlib.util.module_from_spec(spec)
spec.loader.exec_module(cdd)

TEMPLATES = ("ticket", "retro-entry", "release-playbook", "foundations")


@pytest.fixture
def root(tmp_path, monkeypatch):
    os.makedirs(tmp_path / "forms/templates")
    os.makedirs(tmp_path / "apps/cdd/docs")
    for name in TEMPLATES:
        (tmp_path / f"forms/templates/{name}.md").write_text(f"# {name}\n")
    monkeypatch.setattr(cdd, "ROOT", str(tmp_path))
    return tmp_path


CDD_NEW = {  # its args, and the path it lands at. A row with None is a case in the decision's table
    "A ticket lands in the backlog": (["ticket", "001-012-foo"], "apps/cdd/docs/backlog/001-012-foo.md"),
    "A retro entry lands in its phase": (["retro-entry", "1", "001-012-foo"], "apps/cdd/docs/retro/1/001-012-foo.md"),
    "A playbook lands by its phase": (["release-playbook", "1"], "apps/cdd/docs/release/phase-1.md"),
    "The foundations land in their app": (["foundations"], "apps/cdd/foundations.md"),
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
    (root / "apps/cdd/docs/backlog").mkdir(parents=True)
    (root / "apps/cdd/docs/backlog/001-012-mine.md").write_text("mine\n")
    if path:
        cdd.main(["new", *args])
        assert (root / path).exists() and (root / path).read_text() == f"# {args[0]}\n"
        assert capsys.readouterr().out.strip() == path
    else:
        with pytest.raises(SystemExit) as failed:
            cdd.main(["new", *args])
        assert failed.value.code not in (0, None)
        assert (root / "apps/cdd/docs/backlog/001-012-mine.md").read_text() == "mine\n"


def test_decision_each_script():
    with open(os.path.join(ROOT, "pyproject.toml"), "rb") as handle:
        assert tomllib.load(handle)["project"].get("scripts", {}).get("cdd") == "cdd:main"
    where = open(os.path.join(ROOT, "apps/cdd/docs/architecture.md"), encoding="utf-8").read()
    table = where.split("### Where", 1)[1].split("\n\n", 2)[1]
    for path in re.findall(r"^\|[^|]+\| `([^`]+)`", table, re.M):
        assert any(held.startswith(path) for held in [*cdd.DOCS.values(), *cdd.FOLDERS.values()]), path
    usage = subprocess.run(["uv", "run", "-q", "--project", ROOT, "cdd"], capture_output=True, text=True)
    assert usage.returncode == 2 and "uv run cdd" in usage.stderr
    for script, held in strings_in_scripts():
        assert not any(path.split("{")[0] in held for path in where_paths()), f"{script} holds {held!r}"


def where_paths():
    where = open(os.path.join(ROOT, "apps/cdd/docs/architecture.md"), encoding="utf-8").read()
    table = where.split("### Where", 1)[1].split("\n\n", 2)[1]
    return re.findall(r"^\|[^|]+\| `([^`]+)`", table, re.M)


def strings_in_scripts():
    """(script, string) for each string a check or session script holds, less cdd.py, the tests and docstrings."""
    for name in sorted(os.path.join(home, n) for home in (HERE, cdd.SESSION) for n in os.listdir(home)):
        if name.endswith("/cdd.py") or os.path.basename(name).startswith("test_") or not name.endswith((".py", ".sh")):
            continue
        text = open(name, encoding="utf-8").read()
        if name.endswith(".sh"):
            for line in text.splitlines():
                if not line.lstrip().startswith("#"):
                    yield name, line
            continue
        tree = ast.parse(text)
        docstrings = {id(n.value) for n in ast.walk(tree) if isinstance(n, ast.Expr) and isinstance(n.value, ast.Constant)}
        for node in ast.walk(tree):
            if isinstance(node, ast.Constant) and isinstance(node.value, str) and id(node) not in docstrings:
                yield name, node.value


SESSION_SCRIPTS = {  # its args, and the command it runs
    "cdd save hands the script main's saved sessions' folder": (
        ["save"], lambda main: [*cdd.SAVE, os.path.join(main, "apps/cdd/docs/retro/raw/")]),
    "cdd mine mines a phase's": (
        ["mine", "1"], lambda main: cdd.script("mine-transcripts.py", "1", home=cdd.SESSION)),
}


@pytest.mark.parametrize("case", SESSION_SCRIPTS)
def test_decision_the_session_scripts(monkeypatch, case):
    args, command = SESSION_SCRIPTS[case]
    ran = []
    real = subprocess.run
    monkeypatch.setattr(cdd.subprocess, "run", lambda c, **kw: real(c, **kw) if c[0] == "git" else ran.append(c)
                        or subprocess.CompletedProcess(c, 0))
    with contextlib.suppress(SystemExit):
        cdd.main(args)
    main = os.path.dirname(real(["git", "-C", ROOT, "rev-parse", "--path-format=absolute", "--git-common-dir"],
                                capture_output=True, text=True).stdout.strip())
    assert ran == [command(main)]


def step(code):
    return [sys.executable, "-c", f"print('ran {code}'); raise SystemExit({code})"]


CDD_CHECK = {  # its args, each step's exit code, the steps that run, and whether it fails
    "all pass": (["check"], (0, 0, 0), ["ran 0", "ran 0", "ran 0"], False),
    "a failure exits 1": (["check"], (1, 0, 0), ["ran 1", "ran 0", "ran 0"], True),
    "each step runs past a failure": (["check"], (0, 1, 1), ["ran 0", "ran 1", "ran 1"], True),
    "check caps runs the caps alone": (["check", "caps"], (1, 1, 0), ["ran 0"], False),
    "check rename runs the docs' rename alone": (["check", "rename", "Old", "New"], (0, 1, 0), ["ran 1"], True),
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

````gherkin
## Only in a fence
```
## Still in it
````

  ~~~
## In a tilde fence
  ~~~

### A step ###

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
        ["retro-entry", "1"], "== apps/cdd/docs/retro/1/a.md\nA\n\n== apps/cdd/docs/retro/1/b.md\nB\n"),
    "Each ticket prints without the backlog README": (["ticket"], "== apps/cdd/docs/backlog/t.md\nT\n"),
    "A heading only inside a fence": (["design_document", "Only in a fence"], HEADINGS),
    "A heading that doesn't exist": (["design_document", "Feature: Missing"], HEADINGS),
    "A doc name with no place": (["design"], list(cdd.DOCS)),
    "A file that doesn't exist": (["retro-entry", "1", "c"], ["a.md", "b.md"]),
    "A folder with no docs": (["retro-entry", "2"], ["nothing"]),
    "Args that don't fit its place": (["release-playbook", "x"], ["{n}", "[heading]"]),
}


@pytest.mark.parametrize("case", CDD_READ)
def test_decision_cdd_read(root, capsys, case):
    args, expected = CDD_READ[case]
    (root / "apps/cdd/docs/design_document.md").write_text(DESIGN)
    os.makedirs(root / "apps/cdd/docs/retro/1")
    (root / "apps/cdd/docs/retro/1/a.md").write_text("A\n")
    (root / "apps/cdd/docs/retro/1/b.md").write_text("B\n")
    (root / "apps/cdd/docs/retro/1/notes.txt").write_text("not a doc\n")
    os.makedirs(root / "apps/cdd/docs/backlog")
    (root / "apps/cdd/docs/backlog/t.md").write_text("T\n")
    (root / "apps/cdd/docs/backlog/README.md").write_text("order\n")
    if isinstance(expected, str):
        cdd.main(["read", *args])
        assert capsys.readouterr().out == expected
    else:
        with pytest.raises(SystemExit) as failed:
            cdd.main(["read", *args])
        assert isinstance(failed.value.code, str)
        listed = failed.value.code.rsplit(". ", 1)[-1]  # what exists, after the reason if there is one
        assert all(name in listed for name in expected)
        assert not any(fenced in listed for fenced in ("fence", "Still in it", "notes.txt", "##"))


def git(cwd, *args):
    return subprocess.run(["git", "-C", str(cwd), *args], capture_output=True, text=True, check=True).stdout


BACKLOG = """# Backlog

| Group | Ticket | Waits on |
|---|---|---|
| 1 | [001-001 — One](001-001-one.md) | — |
| 2 | [001-002 — Two](001-002-two.md) | 001-001 |
| 3 | [001-003 — Three](001-003-three.md) | — |
| 3 | [001-004 — Four](001-004-four.md) | 001-002, 001-009 |
"""


@pytest.fixture
def repo(tmp_path, monkeypatch):
    """A clone of a bare origin, holding the backlog above on main."""
    origin, here = tmp_path / "origin.git", tmp_path / "here"
    git(tmp_path, "init", "-q", "--bare", "-b", "main", str(origin))
    git(tmp_path, "clone", "-q", str(origin), str(here))
    os.makedirs(here / "apps/cdd/docs/backlog")
    (here / "apps/cdd/docs/backlog/README.md").write_text(BACKLOG)
    for n in ("001-001-one", "001-002-two", "001-003-three", "001-004-four"):
        (here / f"apps/cdd/docs/backlog/{n}.md").write_text(f"# {n}\n")
    git(here, "add", ".")
    git(here, "-c", "user.name=t", "-c", "user.email=t@t", "commit", "-qm", "backlog")
    git(here, "push", "-q", "origin", "main")
    monkeypatch.setattr(cdd, "ROOT", str(here))
    return here


def claim_on_origin(repo, branch):
    git(repo, "push", "-q", "origin", f"main:refs/heads/{branch}")


CDD_NEXT_TICKET = {  # branches on origin, and what it prints or the waits its failure lists
    "The first ticket whose waits are merged": ([], "001-001-one"),
    "A ticket with a branch on origin is skipped": (["feature/001-001-one"], "001-003-three"),
    "With none open it says what each waits on": (["feature/001-001-one", "feature/001-003-three"], None),
}


@pytest.mark.parametrize("case", CDD_NEXT_TICKET)
def test_decision_cdd_next_ticket(repo, capsys, case):
    claimed, expected = CDD_NEXT_TICKET[case]
    for branch in claimed:
        claim_on_origin(repo, branch)
    if expected:
        cdd.main(["next-ticket"])
        assert capsys.readouterr().out.strip() == expected
    else:
        with pytest.raises(SystemExit) as failed:
            cdd.main(["next-ticket"])
        said = failed.value.code
        assert isinstance(said, str)
        assert "001-002 waits on 001-001" in said and "001-004 waits on 001-002." in said + "."
        assert "001-009" not in said, "a wait gone from the backlog is merged"


CDD_BRANCH = {  # its args, the branch it claims, and what came before: a claim on origin or a first run
    "A ticket": (["ticket", "001-003"], "feature/001-003-three", None),
    "A phase's plan": (["plan", "2"], "design/phase-2", None),
    "An ad hoc plan": (["adhoc", "002", "fix-links"], "adhoc/002-fix-links", None),
    "A chore": (["chore", "tidy"], "chore/tidy", None),
    "A branch already here is reused": (["chore", "tidy"], "chore/tidy", "here"),
    "A branch on origin lost the race and names the next open ticket": (
        ["ticket", "001-001"], "feature/001-001-one", "origin"),
}


@pytest.mark.parametrize("case", CDD_BRANCH)
def test_decision_cdd_branch(repo, capsys, case):
    args, branch, before = CDD_BRANCH[case]
    if before == "origin":
        claim_on_origin(repo, branch)
        with pytest.raises(SystemExit) as failed:
            cdd.main(["branch", *args])
        assert isinstance(failed.value.code, str) and "001-003-three" in failed.value.code
        assert not git(repo, "branch", "--list", branch).strip()
        return
    if before == "here":
        cdd.main(["branch", *args])
        capsys.readouterr()
    cdd.main(["branch", *args])
    printed = capsys.readouterr().out.split()
    assert printed, "cdd branch prints its worktree"
    tree = printed[-1]
    assert git(repo, "ls-remote", "--heads", "origin", branch).strip()
    assert git(tree, "rev-parse", "--abbrev-ref", "HEAD").strip() == branch
    assert tree == str(repo / ".claude/worktrees" / branch.split("/", 1)[1])


def commit(cwd, message):
    git(cwd, "add", "-A")
    git(cwd, "-c", "user.name=t", "-c", "user.email=t@t", "commit", "-qm", message)


def claimed(repo, kind, args, capsys):
    """Claim a branch with cdd branch, and commit a change on it. Its worktree."""
    cdd.main(["branch", kind, *args])
    tree = capsys.readouterr().out.split()[-1]
    with open(os.path.join(tree, "work.txt"), "w") as out:
        out.write("the branch's work\n")
    commit(tree, "work")
    return tree


CDD_MERGE = {  # the branch's kind and args, the merge's args, its message, and what goes wrong first
    "A ticket's merge carries its name and title and deletes it": (
        "ticket", ["001-003"], ["feature/001-003-three"], "001-003-three — Three", None),
    "A plan deletes no ticket": (
        "plan", ["2"], ["design/phase-2", "Phase 2 plan"], "phase-2 — Phase 2 plan", None),
    "A chore deletes no ticket": (
        "chore", ["tidy"], ["chore/tidy", "Tidy up"], "tidy — Tidy up", None),
    "A branch held only on origin merges before it's deleted": (
        "chore", ["tidy"], ["chore/tidy", "Tidy up"], "tidy — Tidy up", "origin only"),
    "A conflict leaves everything": (
        "chore", ["tidy"], ["chore/tidy", "Tidy up"], None, "conflict"),
    "A rejected push leaves everything, and a rerun finishes it": (
        "ticket", ["001-003"], ["feature/001-003-three"], "001-003-three — Three", "rejected"),
}


@pytest.mark.parametrize("case", CDD_MERGE)
def test_decision_cdd_merge(repo, capsys, monkeypatch, case):
    kind, args, merge_args, message, wrong = CDD_MERGE[case]
    monkeypatch.setattr(cdd, "SAVE", ["true"])
    git(repo, "config", "user.name", "t")
    git(repo, "config", "user.email", "t@t")
    (repo / "apps/cdd/docs/backlog/001-003-three.md").write_text("# 001-003 — Three\n")
    commit(repo, "titles")
    git(repo, "push", "-q", "origin", "main")
    branch = merge_args[0]
    tree = claimed(repo, kind, args, capsys)
    tickets = sorted(os.listdir(repo / "apps/cdd/docs/backlog"))
    if wrong == "conflict":
        (repo / "work.txt").write_text("main's work\n")
        commit(repo, "clash")
        git(repo, "push", "-q", "origin", "main")
    if wrong == "origin only":
        git(tree, "push", "-q", "origin", f"HEAD:{branch}")
        git(repo, "worktree", "remove", "--force", tree)
        git(repo, "branch", "-D", branch)
        wrong = None
    hook = repo.parent / "origin.git/hooks/pre-receive"
    if wrong == "rejected":
        hook.write_text("#!/bin/sh\nexit 1\n")
        hook.chmod(0o755)
    if wrong:
        before = git(repo, "rev-parse", "origin/main").strip()
        with pytest.raises(SystemExit) as failed:
            cdd.main(["merge", *merge_args])
        assert isinstance(failed.value.code, str)
        assert git(repo, "ls-remote", "origin", "main").split()[0] == before
        assert os.path.isdir(tree) and git(repo, "branch", "--list", branch).strip()
        assert git(repo, "ls-remote", "--heads", "origin", branch).strip()
        assert not os.path.exists(repo / ".git/MERGE_HEAD")
        if wrong == "conflict":
            return
        hook.unlink()
    cdd.main(["merge", *merge_args])
    head = git(repo, "log", "-1", "--merges", "--format=%s", "origin/main").strip()
    assert head == message
    assert git(repo, "show", "origin/main:work.txt") == "the branch's work\n"
    held = sorted(git(repo, "ls-tree", "--name-only", "origin/main", "apps/cdd/docs/backlog/").split())
    readme = git(repo, "show", "origin/main:apps/cdd/docs/backlog/README.md")
    if kind == "ticket":
        assert "apps/cdd/docs/backlog/001-003-three.md" not in held and "001-003-three" not in readme
    else:
        assert held == [f"apps/cdd/docs/backlog/{t}" for t in tickets] and readme == BACKLOG
    assert not os.path.exists(tree)
    assert not git(repo, "branch", "--list", branch).strip()
    assert not git(repo, "ls-remote", "--heads", "origin", branch).strip()


def test_decision_an_app():
    for held in ("apps/cdd/foundations.md", "apps/cdd/docs", "apps/cdd/scripts", "apps/cdd/publish",
                 "forms/forms.md", "forms/templates", "forms/checks", "forms/cdd.py"):
        assert os.path.exists(os.path.join(ROOT, held)), held
    tracked = subprocess.run(["git", "-C", ROOT, "ls-files", "docs", "scripts", "articles/images", "presentations"],
                             capture_output=True, text=True).stdout
    assert tracked == ""
    assert all(p.startswith(("apps/cdd/", "forms/")) for p in [*cdd.DOCS.values(), *cdd.FOLDERS.values()])


def test_decision_the_essay_s_old_address():
    page = open(os.path.join(ROOT, "articles/index.html"), encoding="utf-8").read()
    assert 'http-equiv="refresh" content="0; url=../apps/cdd/publish/articles/"' in page
