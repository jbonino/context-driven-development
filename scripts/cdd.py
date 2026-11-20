"""cdd: one command for the scripts. It alone holds each doc's path.

    uv run cdd new {doc} [{n}] [{name}]   start a doc from its template
    uv run cdd check [caps]               run the checks, or the caps alone
    uv run cdd mine {n} [--top 10]        mine phase n's saved sessions
"""
import os
import re
import subprocess
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
USAGE = __doc__.split("\n\n", 1)[1].rstrip()

# Each doc's path, keyed by its template's name. {n} is a phase, {name} a file's name.
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
    "raw": "docs/retro/raw/",
    "templates": "docs/templates/",
}


def script(name, *args):
    return ["uv", "run", "--script", os.path.join(HERE, name), *args]


STEPS = [
    ("The scripts' tests", ["uv", "run", "-q", "--with", "pytest", "pytest", "-q", HERE]),
    ("Each fact in its place", script("check-docs.py")),
    ("Each form under its cap. Warns, never fails", script("check-caps.py")),
]


def new(doc, args):
    """Copy the doc's template to its path and print the path."""
    if doc not in DOCS or doc in ("raw", "templates"):
        sys.exit(f"cdd doesn't know {doc}. It knows: {', '.join(d for d in DOCS if d not in ('raw', 'templates'))}")
    fields = re.findall(r"{(\w+)}", DOCS[doc])
    if len(args) != len(fields):
        sys.exit(f"cdd new {doc} takes {' '.join('{' + f + '}' for f in fields) or 'nothing more'}")
    path = DOCS[doc].format(**dict(zip(fields, args)))
    template = os.path.join(ROOT, DOCS["templates"], f"{doc}.md")
    if not os.path.exists(template):
        sys.exit(f"{doc} has no template in {DOCS['templates']}")
    target = os.path.join(ROOT, path)
    if os.path.exists(target):
        sys.exit(f"{path} exists")
    os.makedirs(os.path.dirname(target), exist_ok=True)
    with open(template, encoding="utf-8") as source, open(target, "x", encoding="utf-8") as out:
        out.write(source.read())
    print(path)


def check(steps):
    """Run each step. A failure exits 1 naming it. A warning prints and exits 0."""
    failed = []
    for title, command in steps:
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
        case ["check"]:
            check(STEPS)
        case ["check", "caps"]:
            check(STEPS[2:])
        case ["mine", n, *rest]:
            sys.exit(subprocess.run(script("mine-transcripts.py", n, *rest), cwd=ROOT).returncode)
        case _:
            print(USAGE, file=sys.stderr)
            sys.exit(2)


if __name__ == "__main__":
    main()
