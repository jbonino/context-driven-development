# 001-010 — Restructure the repo — **Ad hoc**

**System.** [Scripts](../architecture.md#scripts) · **Estimate.** 5 — every file moves, and each path and link follows · **Model.** Sonnet 5.5, medium — many moves, each by the wireframe

The root holds the shared forms and the apps. CDD is one app beside any
other.

## Acceptance criteria

- The repo matches the wireframe below.
- The checks pass from the new places.
- The essay still serves on its Pages site.

## Workflow steps

- None

## Build notes

```
/
├─ CLAUDE.md                 imports the What table and CDD's foundations
├─ .claude/skills/
├─ forms/                    shared by every app
│  ├─ forms.md               the What table, out of CDD's foundations
│  ├─ templates/             foundations, design, architecture, ticket…
│  └─ checks/                the check scripts, their tests and baselines
└─ apps/
   ├─ cdd/
   │  ├─ foundations.md      how the team works
   │  ├─ docs/               its design, roadmap, backlog, retros…
   │  ├─ scripts/            the session scripts
   │  └─ publish/            articles, presentations
   └─ {app}/
      ├─ foundations.md
      ├─ docs/
      └─ src/
```

- Each app keeps its own backlog.
- Move each file with its history. Fix each path the skills and the architecture's Where name.
- Delete the empty done and in-progress folders.
