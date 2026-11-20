"""cdd: one command for the scripts. It alone holds each doc's path.

    uv run cdd new {doc} [{n}] [{name}]              start a doc from its template
    uv run cdd read {doc} [{n}] [{name}] [heading]   print a doc or one section
    uv run cdd check [caps]                          run the checks, or the caps alone
    uv run cdd mine {n} [--top 10]                   mine phase n's saved sessions
"""
import os
import re
import subprocess
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
USAGE = __doc__.split("\n\n", 1)[1].rstrip()

# Each doc's path, keyed by its template's name. {n} is a phase. {name} is a file's name.
DOCS = {
    "foundations": "docs/foundations.md",
    "design_document": "docs/design_document.md",
    "architecture": "docs/architecture.md",
    "product_roadmap": "docs/product_roadmap.md",
    "deferred": "docs/deferred/{name}.md",
    "ticket": "docs/backlog/{name}.md",
    "backlog-README": "docs/backlog/README.md",
    "feedback": "docs/feedback.md",
    "release-playbook": "docs/release/phase-{n}.md",
    "retro": "docs/retro/{n}/retro.md",
    "retro-entry": "docs/retro/{n}/{name}.md",
}
FOLDERS = {"raw": "docs/retro/raw/", "templates": "docs/templates/"}
ARG = {"n": re.compile(r"\d+"), "name": re.compile(r"[^/\\]+")}


def script(name, *args):
    return ["uv", "run", "--script", os.path.join(HERE, name), *args]


STEPS = {
    "tests": ("The scripts' tests", ["uv", "run", "-q", "--with", "pytest", "pytest", "-q", HERE]),
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
        case ["check"]:
            check(STEPS)
        case ["check", "caps"]:
            check({"caps": STEPS["caps"]})
        case ["mine", n, *rest]:
            sys.exit(subprocess.run(script("mine-transcripts.py", n, *rest), cwd=ROOT).returncode)
        case _:
            print(USAGE, file=sys.stderr)
            sys.exit(2)


if __name__ == "__main__":
    main()
