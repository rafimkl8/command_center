---
inclusion: always
---

# Revision schedule — spaced repetition for closed loops

Closing a loop (blank page → learn → rebuild → review → English critique) proves I could do it *once*, right after being taught. It does not prove I'll still have it in three weeks. This file exists to force that check, since nothing else in this repo will.

## The rule

**Every closed loop gets revisited on day +3, +10, and +30 after it closed.** Three short check-ins, not full loops.

**At the start of any session touching this repo, before starting new work: compare today's date against the table below.** If any row has a due/overdue revision (marked `[ ]`, date ≤ today) that hasn't been marked done, say so plainly before moving on to whatever the session's main task is — the same way I flag pace or debt elsewhere. Do not wait to be asked.

**What a revision check actually is (5–10 min, not a full loop):**
1. From memory, no notes: explain the loop's concept(s) out loud/in writing in ~2 minutes, like the original English-track paragraph.
2. Open `loops/L<n>/rebuild.py` (or `.js`) — but don't read it yet. First try to predict what it prints, cold.
3. Then open it and check the prediction. If wrong, that's a real signal — the loop isn't as durable as it looked at close time, and the topic may need a genuine re-teach, not just a glance.
4. Mark the row's checkbox done in this file, or tell me to, once actually done — not just because a session happened to open near the date.

**If a revision reveals real gaps (step 3 fails badly):** say so directly, the same way blank-page misses get called out at loop start. Don't quietly let a `[x]` get checked for a shaky recall.

## Table

Update this table every time a loop closes: add a row, compute +3/+10/+30 from the actual merge date (check `git log --merges --format="%ad %s" --date=short` in `command_center`, don't guess).

| Loop | Closed | +3d rev | +10d rev | +30d rev |
|---|---|---|---|---|
| L1 — functions, params, return, defaults | 2026-08-10 | [x] (lapsed, pre-dates this file) | [x] (lapsed, pre-dates this file) | [ ] 2026-09-09 |
| L2 — scope, `*args`/`**kwargs`, mutable-default | 2026-08-16 | [x] (lapsed, pre-dates this file) | [ ] 2026-08-26 | [ ] 2026-09-15 |
| L3 — functions as objects, `lambda` | 2026-08-22 | [ ] 2026-08-25 | [ ] 2026-09-01 | [ ] 2026-09-21 |
| L4 — decorators ⚠️ | 2026-08-22 | [ ] 2026-08-25 | [ ] 2026-09-01 | [ ] 2026-09-21 |
| L5 — classes, `__init__`, `self`, instance attributes, methods | 2026-08-23 | [ ] 2026-08-26 | [ ] 2026-09-02 | [ ] 2026-09-22 |
| L6 — class vs instance attributes, `@staticmethod`, `@classmethod` | 2026-08-23 | [ ] 2026-08-26 | [ ] 2026-09-02 | [ ] 2026-09-22 |
| L7 — inheritance, method overriding, `super()` | 2026-08-22 | [ ] 2026-08-25 | [ ] 2026-09-01 | [ ] 2026-09-21 |
| L8 — polymorphism, abstract classes (`ABC`) | 2026-08-23 | [ ] 2026-08-26 | [ ] 2026-09-02 | [ ] 2026-09-22 |

**Rows for L1's +3d/+10d and L2's +3d are marked lapsed** because this tracking file didn't exist yet when those dates passed — logged honestly as missed, not silently backfilled as done. Every loop from L3 onward gets tracked for real, starting now.

## Where this fits against the rest of the plan

This does not replace the Friday checkpoint (`recovery-plan.md`) or the loop mechanics (`how-to-coach-me.md`) — it's a third, narrower thing: those cover *pace* and *how a loop runs*, this covers *whether a closed loop stays closed*. If a +30d check fails on a loop that's supposed to be load-bearing for a later one (e.g. L5/L6 under L7's inheritance), flag that specifically — a decayed prerequisite is a real risk to the next loop, not just a private embarrassment to log quietly.
