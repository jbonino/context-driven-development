# Phase 1 — 001-002 — What the skills need from Pi

The judgments that need fresh context. Everything else is in the raw
sessions under `apps/cdd/docs/retro/raw/`, mined at phase close.

**Deviations from the plan and design**
- The owner reframed the spike before it began. It asks whether CDD should move to Pi, not whether Pi runs on Copilot. Planning miss: the ticket.
- The analysis is on paper, from the sessions and Pi's docs.
- The miner's `--tools` change lives in the green-wagon repo, which holds the sessions. It needs its own commit there.

**Owner's calls**
- Pi's sign-in doesn't matter for this spike.

**Code review**

| Severity | Finding | Outcome | Planning miss |
|---|---|---|---|
| Critical | Bash's 727 sessions exceed the 678 mined | Fixed. The miner counts 740 transcripts, 399 sessions and 341 subagents. 678 was a wrong file count | Tests |
| Important | The rows sum to 2 short of the total | Fixed. `bash_placeholder` joins the rare row | Tests |
| Important | No skill rows, which a criterion asks for | Fixed. A skills table with loads | the ticket |
| Important | Pi claims read as tested fact | Fixed. They cite Pi 1.6.0's docs | — |
| Important | A and C tie, yet only A is bolded | Fixed. Both are bolded and the owner picks | — |
| Important | The footnote's 96% waits on the count fix | Fixed. It holds, and cites the docs | — |
| Minor | The table's key sits among the findings | Fixed | — |
| Minor | The decision holds two facts | Fixed. "Claude Code first" moves to its footnote | — |
| Minor | `import gzip` sits mid-file | Fixed | — |
| Minor | No test that a phase is needed without `--tools` | Left. The parser's own error covers it | — |

- Verdict: With fixes.

**Changed after sign-off**
- The owner picks C, Claude Code alone. The roadmap's goal drops Pi, 001-003 goes, and Pi becomes a deferred entry. Planning miss: `product_roadmap.md`, which scoped Pi before the spike.
