"""cdd: one command for the scripts. It alone holds each doc's path.

    uv run cdd new {doc} [{n}] [{name}]              start a doc from its template
    uv run cdd read {doc} [{n}] [{name}] [heading]   print a doc or one section
    uv run cdd next-ticket                           name the next open ticket
    uv run cdd branch {kind} {args}                  claim a branch and open its worktree
    uv run cdd merge {branch} [title]                merge a signed-off branch. A plan or chore takes a title
    uv run cdd save                                  save the sessions for the phase's close
    uv run cdd check [caps]                          run the checks, or the caps alone
    uv run cdd check rename {old} {new}              rename a source with its links and tests
    uv run cdd mine {n} [--top 10]                   mine phase n's saved sessions
"""
import os
import re
import subprocess
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
CHECKS = os.path.join(HERE, "checks")
APP = os.path.join(ROOT, "apps/cdd")
SESSION = os.path.join(APP, "scripts")
USAGE = __doc__.split("\n\n", 1)[1].rstrip()

# Each doc's path, keyed by its template's name. {n} is a phase. {name} is a file's name.
DOCS = {
    "forms": "forms/forms.md",
    "foundations": "apps/cdd/foundations.md",
    "design_document": "apps/cdd/docs/design_document.md",
    "architecture": "apps/cdd/docs/architecture.md",
    "product_roadmap": "apps/cdd/docs/product_roadmap.md",
    "deferred": "apps/cdd/docs/deferred/{name}.md",
    "ticket": "apps/cdd/docs/backlog/{name}.md",
    "backlog-README": "apps/cdd/docs/backlog/README.md",
    "feedback": "apps/cdd/docs/feedback.md",
    "release-playbook": "apps/cdd/docs/release/phase-{n}.md",
    "retro": "apps/cdd/docs/retro/{n}/retro.md",
    "retro-entry": "apps/cdd/docs/retro/{n}/{name}.md",
}
FOLDERS = {"raw": "apps/cdd/docs/retro/raw/", "templates": "forms/templates/"}


def before_the_move(path):
    """Where a doc sat before 001-010 moved CDD under apps/cdd/, for the history before it."""
    return "docs/" + path.removeprefix("apps/cdd/").removeprefix("docs/")


def folder(doc):
    """The folder a doc sits in, like apps/cdd/docs/backlog/ for a ticket."""
    return os.path.dirname(DOCS[doc].split("{")[0]) + "/"


ARG = {"n": re.compile(r"\d+"), "name": re.compile(r"[^/\\]+")}


def script(name, *args, home=CHECKS):
    return ["uv", "run", "--script", os.path.join(home, name), *args]


STEPS = {
    "tests": ("The scripts' tests", ["uv", "run", "-q", "--with", "pytest", "pytest", "-q", CHECKS, SESSION]),
    "docs": ("Each fact in its place", script("check-docs.py")),
    "caps": ("Each form under its cap. Warns, never fails", script("check-caps.py")),
}


def new(doc, args):
    """Copy the doc's template to its path and print the path."""
    if doc not in DOCS:
        sys.exit(f"cdd doesn't know {doc}. It knows {', '.join(DOCS)}")
    fields = re.findall(r"{(\w+)}", DOCS[doc])
    if len(args) != len(fields) or not all(ARG[f].fullmatch(a) and a != ".." for f, a in zip(fields, args)):
        sys.exit(f"cdd new {doc} takes {' '.join('{' + f + '}' for f in fields) or 'nothing more'}")
    path = DOCS[doc].format(**dict(zip(fields, args)))
    template = os.path.join(ROOT, FOLDERS["templates"], f"{doc}.md")
    if not os.path.exists(template):
        sys.exit(f"{doc} has no template in {FOLDERS['templates']}")
    target = os.path.join(ROOT, path)
    if os.path.exists(target):
        sys.exit(f"{path} exists")
    os.makedirs(os.path.dirname(target), exist_ok=True)
    with open(template, encoding="utf-8") as source, open(target, "x", encoding="utf-8") as out:
        out.write(source.read())
    print(path)


def docs_in(folder):
    """The .md files in a folder, less those another doc names, like the backlog README."""
    held = os.path.join(ROOT, folder)
    named = {os.path.basename(p) for p in DOCS.values() if os.path.dirname(p) == folder}
    return sorted(f for f in os.listdir(held) if f.endswith(".md") and f not in named) if os.path.isdir(held) else []


def outside_fences(lines):
    """(line index, level, text) for each # heading outside a ``` or ~~~ fence."""
    headings, fence = [], None
    for i, line in enumerate(lines):
        mark = re.match(r" {0,3}(`{3,}|~{3,})", line)
        if fence and mark and mark[1][0] == fence[0] and len(mark[1]) >= len(fence) and not line.strip(" \n`~"):
            fence = None
        elif not fence and mark:
            fence = mark[1]
        elif not fence and (found := re.match(r" {0,3}(#{1,6})[ \t]+(.*?)(?:[ \t]+#+)?[ \t]*$", line.rstrip("\n"))):
            headings.append((i, len(found[1]), found[2]))
    return headings


def read(doc, args):
    """Print a doc's section, the whole doc, or each of a phase's files."""
    if doc not in DOCS:
        sys.exit(f"cdd doesn't know {doc}. It knows {', '.join(DOCS)}")
    fields = re.findall(r"{(\w+)}", DOCS[doc])
    given, heading = args[:len(fields)], (args[len(fields):] or [None])[0]
    each = fields[-1:] == ["name"] and len(given) == len(fields) - 1  # no name: each file in the folder
    too_many = len(args) > len(fields) + 1
    too_few = len(given) < len(fields) and not each
    bad = not all(ARG[f].fullmatch(a) and a != ".." for f, a in zip(fields, given))
    if too_many or too_few or bad:
        sys.exit(f"cdd read {doc} takes {' '.join(['{' + f + '}' for f in fields] + ['[heading]'])}")
    path = DOCS[doc].format(**dict(zip(fields, given)), **({"name": ""} if each else {}))
    folder = os.path.dirname(path)
    held = docs_in(folder)
    if each:
        if not held:
            sys.exit(f"{folder} holds no docs. It holds nothing")
        for i, name in enumerate(held):
            with open(os.path.join(ROOT, folder, name), encoding="utf-8") as source:
                print("\n" * bool(i) + f"== {folder}/{name}\n{source.read()}", end="")
        return
    if not os.path.exists(os.path.join(ROOT, path)):
        sys.exit(f"{path} doesn't exist. Its folder holds {', '.join(held) or 'nothing'}")
    with open(os.path.join(ROOT, path), encoding="utf-8") as source:
        lines = source.read().splitlines(keepends=True)
    if heading is None:
        print("".join(lines), end="")
        return
    headings = outside_fences(lines)
    for k, (start, level, text) in enumerate(headings):
        if text == heading:
            end = next((i for i, lv, _ in headings[k + 1:] if lv <= level), len(lines))
            print("".join(lines[start:end]), end="")
            return
    sys.exit(f"{path} has no heading {heading}. Its headings are {', '.join(t for _, _, t in headings)}")


def git(*args, check=True):
    """Run git in ROOT. A failure exits with its error unless check is off."""
    done = subprocess.run(["git", "-C", ROOT, *args], capture_output=True, text=True)
    if check and done.returncode:
        sys.exit(f"git {' '.join(args)} failed: {done.stderr.strip()}")
    return done


def backlog():
    """(ticket's filename, its number, the numbers it waits on) for each row of origin's main, in order."""
    git("fetch", "-q", "origin", "main")
    readme = git("show", f"FETCH_HEAD:{DOCS['backlog-README']}").stdout
    rows = re.findall(r"^\|[^|]*\|[^|]*\]\(((\d+-\d+)[^)]*)\.md\)[^|]*\|([^|]*)\|", readme, re.M)
    return [(name, number, re.findall(r"\d+-\d+", waits)) for name, number, waits in rows]


def open_ticket():
    """The first ticket whose waits are merged and that has no branch on origin, and why each other isn't."""
    rows = backlog()
    listed = {number for _, number, _ in rows}
    claimed = git("ls-remote", "--heads", "origin").stdout
    why = []
    for name, number, waits in rows:
        if open_waits := [w for w in waits if w in listed]:
            why.append(f"{number} waits on {', '.join(open_waits)}")
        elif f"refs/heads/feature/{name}\n" in claimed:
            why.append(f"{number} has a branch on origin")
        else:
            return name, why
    return None, why


def next_ticket():
    """Print the next open ticket, or say what each waits on."""
    name, why = open_ticket()
    if not name:
        sys.exit(f"No ticket is open. {'. '.join(why) or 'The backlog is empty'}")
    print(name)


BRANCHES = {"ticket": "feature/{name}", "plan": "design/phase-{n}", "adhoc": "adhoc/{n}-{name}", "chore": "chore/{name}"}


def branch(kind, args):
    """Claim the branch on origin by pushing origin's main under its name, then open its worktree."""
    fields = re.findall(r"{(\w+)}", BRANCHES.get(kind, ""))
    if not fields or len(args) != len(fields) or not all(ARG[f].fullmatch(a) and a != ".." for f, a in zip(fields, args)):
        takes = " or ".join(f"{k} " + " ".join("{" + f + "}" for f in re.findall(r"{(\w+)}", v)) for k, v in BRANCHES.items())
        sys.exit(f"cdd branch takes {takes}")
    given = dict(zip(fields, args))
    if kind == "ticket":
        found = [name for name, number, _ in backlog() if number == args[0]]
        if not found:
            sys.exit(f"The backlog has no ticket {args[0]}")
        given["name"] = found[0]
    name = BRANCHES[kind].format(**given)
    if git("check-ref-format", "--branch", name, check=False).returncode:
        sys.exit(f"{name} isn't a branch name git takes")
    tree = os.path.join(ROOT, ".claude/worktrees", name.split("/", 1)[1])
    if not git("rev-parse", "--verify", "--quiet", f"refs/heads/{name}", check=False).stdout:
        git("fetch", "-q", "origin", "main")
        lost = git("ls-remote", "--heads", "origin", name).stdout.strip()
        if not lost:
            pushed = git("push", "-q", f"--force-with-lease=refs/heads/{name}:", "origin", f"FETCH_HEAD:refs/heads/{name}", check=False)
            lost = pushed.returncode and git("ls-remote", "--heads", "origin", name).stdout.strip()
            if pushed.returncode and not lost:
                sys.exit(f"git push failed: {pushed.stderr.strip()}")
        if lost:
            next_name, _ = open_ticket()
            sys.exit(f"{name} is someone else's on origin. The next open ticket is {next_name or 'none'}")
        git("fetch", "-q", "origin", f"{name}:refs/remotes/origin/{name}")
        git("branch", "-q", "--track", name, f"origin/{name}")
    if os.path.isdir(tree):
        held = subprocess.run(["git", "-C", tree, "rev-parse", "--abbrev-ref", "HEAD"], capture_output=True, text=True).stdout.strip()
        if held != name:
            sys.exit(f"{tree} holds {held or 'no branch'}, not {name}")
    else:
        git("worktree", "add", "-q", tree, name)
    print(tree)


SAVE = ["bash", os.path.join(SESSION, "save-transcripts.sh")]


def main_checkout():
    """The main checkout's folder, from here or from any worktree."""
    return os.path.dirname(git("rev-parse", "--path-format=absolute", "--git-common-dir").stdout.strip())


def save():
    """Save the sessions into the main checkout's folder for them. False on a failure."""
    return not subprocess.run([*SAVE, os.path.join(main_checkout(), FOLDERS["raw"])]).returncode


def merge(name, title):
    """Save the sessions, merge the branch into main with its name and title, delete its ticket,
    push, then remove its worktree and branches. A conflict or a rejected push leaves the branch.
    A rerun skips a merge already on main."""
    prefix, _, short = name.partition("/")
    if prefix not in {v.split("/")[0] for v in BRANCHES.values()} or not short:
        sys.exit(f"cdd merge takes a branch cdd branch names, like {', '.join(BRANCHES.values())}")
    here = main_checkout()

    def main_git(*args, check=True):
        done = subprocess.run(["git", "-C", here, *args], capture_output=True, text=True)
        if check and done.returncode:
            sys.exit(f"git {' '.join(args)} failed: {done.stderr.strip()}")
        return done

    if main_git("branch", "--show-current").stdout.strip() != "main":
        sys.exit(f"{here} isn't on main")
    if main_git("status", "--porcelain", "--untracked-files=no").stdout.strip():
        sys.exit(f"{here} has uncommitted changes")
    ref = f"refs/heads/{name}"
    trees = [t.split("\n", 1)[0].removeprefix("worktree ")
             for t in main_git("worktree", "list", "--porcelain").stdout.split("\n\n") if f"\nbranch {ref}" in t]
    for tree in trees:
        if subprocess.run(["git", "-C", tree, "status", "--porcelain"], capture_output=True, text=True).stdout.strip():
            sys.exit(f"{tree} has uncommitted changes")
    on_origin = bool(main_git("ls-remote", "--heads", "origin", name).stdout.strip())
    held = bool(main_git("rev-parse", "--verify", "--quiet", ref, check=False).stdout)
    if not held and on_origin:  # a branch held only on origin merges before it's deleted
        main_git("fetch", "-q", "origin", f"{ref}:{ref}")
        held = True
    if not held:
        sys.exit(f"{name} is neither here nor on origin")
    main_git("fetch", "-q", "origin", "main")
    if main_git("merge", "-q", "--ff-only", "FETCH_HEAD", check=False).returncode:
        sys.exit("main and origin's main have parted. Run git reset --hard origin/main in main, then rerun")
    if held and main_git("merge-base", "--is-ancestor", ref, "HEAD", check=False).returncode:
        ticket = DOCS["ticket"].format(name=short) if prefix == "feature" else None
        if ticket:
            top = main_git("show", f"{ref}:{ticket}").stdout.split("\n", 1)[0]
            title = re.sub(r" — \*\*[^*]+\*\*$", "", top).split(" — ", 1)[-1]
        if not title:
            sys.exit(f"cdd merge {name} takes a title")
        if not save():
            sys.exit("Saving the sessions failed")
        if main_git("merge", "-q", "--no-ff", "--no-commit", ref, check=False).returncode:
            main_git("merge", "--abort")
            sys.exit(f"{name} conflicts with main. Merge main into it, then rerun")
        if ticket and os.path.exists(os.path.join(here, ticket)):
            main_git("rm", "-qf", ticket)  # a ticket the branch edits is staged by the merge
            readme = os.path.join(here, DOCS["backlog-README"])
            with open(readme, encoding="utf-8") as source:
                rows = [row for row in source if "](" + short + ".md)" not in row]
            with open(readme, "w", encoding="utf-8") as out:
                out.writelines(rows)
            main_git("add", DOCS["backlog-README"])
        committed = main_git("commit", "-q", "-m", f"{short} — {title}", check=False)
        if committed.returncode:
            main_git("merge", "--abort")
            sys.exit(f"git commit failed: {committed.stderr.strip()}")
    pushed = main_git("push", "-q", "origin", "main", check=False)
    if pushed.returncode:
        sys.exit(f"git push was rejected: {pushed.stderr.strip()}. Rerun once it can push")
    for tree in trees:
        main_git("worktree", "remove", "--force", tree)
    main_git("worktree", "prune")
    main_git("branch", "-q", "-D", name)
    if on_origin:
        main_git("push", "-q", "origin", "--delete", name)
    print(main_git("rev-parse", "--short", "HEAD").stdout.strip())


def check(steps):
    """Run each step. A failure exits 1 naming it. A warning prints and exits 0."""
    failed = []
    for title, command in steps.values():
        print(f"== {title}", flush=True)
        if subprocess.run(command, cwd=ROOT).returncode:
            failed.append(title)
    if failed:
        sys.exit(f"Failed: {', '.join(failed)}")


def main(argv=None):
    argv = sys.argv[1:] if argv is None else argv
    match argv:
        case ["new", doc, *args]:
            new(doc, args)
        case ["read", doc, *args]:
            read(doc, args)
        case ["next-ticket"]:
            next_ticket()
        case ["branch", kind, *args]:
            branch(kind, args)
        case ["merge", name, *title] if len(title) <= 1:
            merge(name, (title or [None])[0])
        case ["save"]:
            if not save():
                sys.exit("Saving the sessions failed")
        case ["check"]:
            check(STEPS)
        case ["check", "caps"]:
            check({"caps": STEPS["caps"]})
        case ["check", "rename", was, now]:
            title, command = STEPS["docs"]
            check({"rename": (title, [*command, "rename", was, now])})
        case ["mine", n, *rest]:
            sys.exit(subprocess.run(script("mine-transcripts.py", n, *rest, home=SESSION), cwd=ROOT).returncode)
        case _:
            print(USAGE, file=sys.stderr)
            sys.exit(2)


if __name__ == "__main__":
    main()
