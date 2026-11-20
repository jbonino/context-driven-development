# Phase 1 — 001-005 — Read a doc by name

The judgments that need fresh context. Everything else is in the raw
sessions under `docs/retro/raw/`, mined at phase close.

**Deviations from the plan and design**
- `cdd read` names a doc by its template, as `cdd new` does. The ticket's example now reads `cdd read design_document`.
- A doc with no name given prints each doc in its folder. `cdd read retro-entry 1` prints phase 1's files.
- The tests found three more failures. A missing file, an empty folder and args that don't fit. **`cdd read`** holds the five in a table.

**Code review**

| Severity | Finding | Outcome | Planning miss |
|---|---|---|---|
| Important | `cdd read ticket` printed the backlog README as a ticket | Fixed. A folder read leaves out a file another doc names | the ticket |
| Important | Fences were only a column-0 ```` ``` ````. `~~~`, indented and longer fences slipped, and `## A ##` kept its `##` | Fixed. A fence closes on its own mark and length. A heading is 1 to 6 `#`s | Tests |
| Important | The two heading rows listed the same thing, and the code had failures the table didn't name | Fixed. One heading row, plus rows for an empty folder and args that don't fit | `architecture.md` |
| Minor | Setext headings aren't found | Left. The docs use `#` headings alone | — |
| Minor | The usage lines weren't aligned | Fixed | — |
| Minor | A file was opened without `with` | Fixed | — |
| Minor | The usage check was one long condition | Fixed. Named conditions | — |
| Minor | A missing file listed non-`.md` files | Fixed | — |
| Minor | The ticket's example used `design` | Fixed | — |
| Minor | The fence assertion ran on every failure row | Left. One check that no row lists a fenced heading or a non-doc reads plainer | — |

- Verdict: With fixes.

**Changed after sign-off**
- None
