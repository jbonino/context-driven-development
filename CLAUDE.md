@.claude/context-driven-development/foundations.md

- Read .claude/skills/editing-prose/SKILL.md and be proactive about agent output.
- **superpowers:brainstorming** Never write specs or writing plans. When `brainstorming` would normally write a design doc and hand off to `writing-plans`, stop after the design is approved and use `planning-ad-hoc` instead. Before the design is approved, walk two or three real cases from the team's code and data through it, each with its verdict, and a text wireframe where a screen is involved.
- **superpowers:test-driven-development** RED only counts when the named assertion fails — a module-not-found, a compile error, or a missing dependency install. Write the tests the ticket names. A case found while building joins the design as a row or a scenario, and the hand-off lists it for the owner.
- **superpowers:requesting-code-review** Dispatch a separate reviewer agent. Never review your own work. Check the change against the Rules of the ticket's System, and ask whether a new feature rule belongs there. Ask whether any fact sits higher than its kind: Foundations holds terms, ethics, roles and principles, the design holds numbers and behaviour, and the architecture holds the how. The skill that invokes the review adds its own questions.
- This repo is the source of truth for the team's work. It reads the team repo's docs and never writes into them.
- A ticket spans this repo and a team repo.

  | Part | Lives in | Merges |
  |---|---|---|
  | Docs branch | This repo, from `branching-from-main` | After the team PR merges |
  | Code branch and PR | The team repo | Per that repo's conventions |
  | Release playbook | `docs/release/phase-{n}.md` | Checked by `releasing` |

  A ticket file names its team issue, like `001-my-service-42.md`.
- Each phase runs every skill, cut to fit. The retro is never skipped.
- A doc grows only when a ticket touches its area.
- Facts flow down the table. A file names only the files above it.

  | File | May name |
  |---|---|
  | `docs/design_document.md` | nothing |
  | `docs/architecture.md` | the design |
  | A ticket | the design, the architecture |
  | Skills | anything |
