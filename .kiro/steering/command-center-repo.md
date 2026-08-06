---
inclusion: fileMatch
fileMatchPattern: ["*.html", "*.js", "README.md"]
---

# Working on the command_center repo

My personal study/productivity system. **Static HTML, no build step, no dependencies, no package.json.** Each page is self-contained with inline `<style>` and inline `<script>`. Deployed by GitHub Pages from `main` at `/` — legacy Jekyll build, which is fine for plain HTML.

Live: `https://rafimkl8.github.io/command_center/`

## The pages

| File | Role |
|---|---|
| `index.html` | Hub — tiles + the Firebase sync setup guide |
| `recovery.html` | **The audit tool — the entry point.** Scores modules 1–21, tiers the debt, prices it, and holds the day-by-day plan |
| `weekly_tracker.html` | Module tracker — task checkboxes, "Remaining" backlog, overview counters |
| `command_center.html` | 9-tab master dashboard (long-range reference) |
| `refined_8_month_fullstack_plan.html` | All 40 modules as collapsible phase cards |
| `career_launchpad.html` | Freelance / job hunt / interview playbook |
| `print_routine.html`, `print_routine_variant_b.html` | Printable A4 daily routines |
| `weeks.js` | **Single source of truth** for the 40-module curriculum |
| `sync.js` | Firebase cross-device sync engine |

Filename note: `refined_8_month_fullstack_plan.html` keeps its name even though the plan spans 40 modules — renaming would break links for no gain.

## Hard rules

**`weeks.js` is the single source of truth.** It exports `window.WEEKS` (40 objects: `n`, `title`, `phase`, `badges`, `hrs`, `cats{course,extra,leet,project,git,eng}`, `note`). Both `weekly_tracker.html` and `recovery.html` load it. Edit a module **there**, never in a page. It must be loaded *before* the inline scripts.

**Task IDs must stay `module_category_index`** (e.g. `4_course_0`) and index-based. All my saved progress in `localStorage` keys off them — changing the scheme silently destroys months of ticks. Reordering items inside a category also shifts IDs; avoid it, and if unavoidable, say so loudly.

**Say module, not week.** `Week N` must not appear in any user-facing string. The sole exception is `Exam Week N`, which names an exam sitting and is deliberately preserved — do not "fix" it.

**Category weights must sum to 1.0** in the tracker's `CATS` (course .32, project .25, extra .18, leet .12, eng .08, git .05).

## localStorage + sync

- Audit: `rc_score`, `rc_done`, `rc_thru`
- Tracker: `wt_done`, `wt_current`, `wt_sel`, `wt_leetcode`, `wt_streak`, `wt_articles`, `wt_apps`
- Launchpad: `cl_done`
- Sync code: `sync_code`

`sync.js` only syncs keys explicitly registered via `CloudSync.start({keys:[...]})`. **A new key that is not registered will not sync and will not be backed up.** On first link it OR-merges any key whose name contains `"done"` so no progress is lost from either device; everything else is last-write-wins. Writes debounce 600ms and a per-tab random `origin` prevents echo loops.

## Security model — understand before touching

The Firebase web config in `sync.js` is a **public project identifier, not a secret**. Firebase is designed that way; it ships in client code on every site that uses it. Committing it is correct. **Never** commit an actual credential (OpenAI keys, DB passwords) — that distinction is the point.

The real protection is the Firestore rules:

```
match /trackers/{code} {
  allow get:            if code.size() >= 12;
  allow create, update: if code.size() >= 12;
}
```

`get` rather than `read` is deliberate — `read` also grants `list`, which would let anyone enumerate every sync code and read all of it. The 12-character floor is mirrored client-side as `MIN_CODE_LEN` so a short code fails with an explanation instead of a silent `permission-denied`. Do not weaken either.

## Verifying changes

**There is no browser and no jsdom in this sandbox.** Playwright has no browsers installed. To verify a page actually works, write a **throwaway Node harness with a minimal DOM stub** (`document.getElementById`, `classList`, `appendChild`, `localStorage`), `eval` the page's inline script plus `weeks.js`, expose the internals via `globalThis`, then assert on real behaviour and on the generated HTML.

Worth asserting: scripts parse; div/table/ul/li/tr/td tags balance; internal links resolve; no stray `Week <n>`; tracks cover the intended module range exactly once; scoring/tiering/hours compute correctly; task IDs unchanged; both tools still render all views.

**Delete the harness afterwards — never commit it.** The repo has no test infrastructure and does not want any. Node is at `/root/.nvm/versions/node/v22.23.2/bin/node`; if `node` is not found, prepend that to `PATH`.

## Git workflow

- **Branch per PR. Never push to `main` directly.**
- **Check PR state before pushing to an existing branch.** This bit me: PR #2 was merged mid-stream and five subsequent commits silently never reached `main`. `gh api "repos/rafimkl8/command_center/pulls?state=all&per_page=10"` — the default listing hides merged and closed PRs.
- `gh pr` and `gh issue` are GraphQL-backed and fail here. Use `gh api` REST endpoints.
- Direct `git push` to the `origin` gateway URL fails with an auth error; push to `https://github.com/rafimkl8/command_center.git` explicitly.
- Prefer verifying deployment by fetching the live URL and hashing against local — `cmp` and `diff` are not installed, so use Node's `crypto`.

## Style

Geist / Geist Mono from Google Fonts, `#eef2f6` body, white cards with `border-radius:12px`, teal `#0f766e` and blue `#1d4ed8` accents, monospace for numbers and dates. Mobile-first — I mostly read these on an iPhone, so keep grids collapsing at ~620px. Match the existing look; do not introduce a new design language.
