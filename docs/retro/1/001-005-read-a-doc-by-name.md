# Phase 1 — 001-005 — Read a doc by name

The judgments that need fresh context. Everything else is in the raw
sessions under `docs/retro/raw/`, mined at phase close.

**Deviations from the plan and design**
- `cdd read` names a doc by its template, as `cdd new` does. The ticket's `cdd read design` fails. `cdd read design_document` works.
- A doc with no name given prints each file in its folder. `cdd read retro-entry 1` prints phase 1's files.
- The tests found a fourth failure. A missing file lists its folder. **`cdd read`** holds the four in a table.

**Code review**

| Severity | Finding | Outcome | Planning miss |
|---|---|---|---|

- Verdict: 

**Changed after sign-off**
- None
