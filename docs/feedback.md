# Feedback

What came up with the team and the owner. Scoping reads it and deletes each entry it uses.

## Owner — 2026-11-20 — Restructure the repo

Root holds `forms/` and `apps/`. CDD becomes `apps/cdd/`, beside any other app.

```
/
├─ CLAUDE.md
├─ pyproject.toml            declares `cdd`
├─ .claude/skills/
├─ forms/                    shared by every app
│  ├─ forms.md               the What table, out of CDD's foundations
│  ├─ templates/             foundations, design, architecture, ticket…
│  └─ checks/
└─ apps/
   ├─ cdd/
   │  ├─ foundations.md      how the team works
   │  ├─ docs/               its own design, roadmap, backlog, retros
   │  ├─ scripts/
   │  └─ publish/            articles, presentations
   └─ {app}/
      ├─ foundations.md      its own What, Why, Who, Where and How
      ├─ docs/
      └─ src/
```

- Each app keeps its own backlog. `cdd` finds the app from the folder it runs in.
- The essay's Pages path moves with `publish/`.
