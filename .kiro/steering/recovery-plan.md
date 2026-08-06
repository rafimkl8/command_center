---
inclusion: auto
name: recovery-plan
description: The measured diagnosis of my learning debt from modules 1-21, the dependency-ordered recovery schedule with per-track deadlines, the three rebuild artifacts, and what is deliberately parked. Use whenever the topic is what to study, when to study it, whether I am on pace, how far behind I am, my schedule, module 21, or what to cut when I fall behind.
---

# The recovery plan (measured, not guessed)

Live version: `recovery.html` in this repo. If it disagrees with this file, **the tool wins** — it holds my actual scores.

## The audit

I scored every task from module 1 onward on a 0–3 scale, where `1` means *"AI did it for me, I cannot reproduce it"* and `2` means *"I can do it with docs open"*. **Only 0 and 1 count as debt. A `2` is not debt — professionals work at 2 all day.**

329 items, 113 scored so far, **84 flagged**. Flagged items are tiered, and only two tiers cost hours:

| Tier | Categories | Count | Charged |
|---|---|---|---|
| **concept** | course, project | 22 | full (0→0.75, 1→0.45 of budget) |
| **habit** | git, english | 22 | a quarter |
| **practice** | leetcode | 17 | zero — interview prep, a drip until 2027 |
| **resource** | self-study videos | 23 | zero — means, not skills |

Tiering dropped the headline from ~96h to **~50h**. An unwatched YouTube video is not a missing skill; conflating them is what made a recoverable gap feel like a catastrophe.

## The diagnosis — precise

Modules **1, 2 and 5** course items scored clean. Every course item in **module 3** (functions, scope, decorators, lambda · files, iterators, generators · try/except) and **module 4** (classes, inheritance, polymorphism, abstract classes, property decorators) is `AI-did-it`. **All of Django (modules 16–18) is 0 or 1.**

Module 4's own note in the plan predicted this: *"If you skip OOP depth, Django will feel like magic you can't control."* It does. That is the whole diagnosis.

**Python debt and Django debt are the same debt.** Django is Python's class system with a database attached. Teach the Python in Django's vocabulary and every hour counts twice:

| Missing from modules 3–4 | What it already is in Django |
|---|---|
| classes, `__init__`, attributes, methods | a model — `class Task(models.Model)` |
| inheritance, overriding, `super()` | `models.Model`, `class Meta`, `AbstractUser`, class-based views |
| `__str__`, `__repr__` | the `__str__` on every model — what the admin displays |
| `@property`, encapsulation | computed fields — `@property def is_overdue` |
| decorators | `@login_required`, `@admin.register`, `@receiver` |
| `*args` / `**kwargs` | `get_context_data(self, **kwargs)`, URL params into views |
| try/except, custom exceptions | `Task.DoesNotExist`, `ValidationError`, `get_object_or_404` |
| files and paths | `FileField`, `ImageField`, `MEDIA_ROOT` |
| iterators, generators, laziness | QuerySets do not hit the DB until iterated |

## Three builds clear almost everything

I do **not** rebuild every module. I rebuild the minimum set of artifacts that touches every missing concept.

| Build | When | Clears |
|---|---|---|
| **OOP To-Do, pure Python** | Day 7 | module 2/3/4 project debt + module 3/4 concepts |
| **Same app, in Django** | Days 8–10 | **module 19** + module 16–18 Django basics |
| **E-commerce** | module 21 | **module 20** (superseded, *not* rebuilt) + module 17/18 forms, auth, queries + SQL |

**Module 20's blog is never rebuilt.** Module 21's e-commerce teaches everything it would, and more. Log it as debt, let 21 absorb it, move on. Module 5's Weather app is likewise superseded by DRF (module 23).

## Schedule

Phases 1–2 use **numbered days, not dates** — miss a day and the numbers do not move. Started Aug 6.

- **Days 1–7 — Python in Django's vocabulary.** functions → decorators → classes → inheritance → dunders/`@property` → files/exceptions → rebuild the OOP To-Do from empty.
- **Days 8–10 — the bridge.** Same app in Django: project/model/migrations/admin → views/URLs/templates → `ModelForm` CRUD + git habits. Spilling into module 21 is fine.
- **Aug 16 – Sep 5 — module 21 IS the Django curriculum.** Three weeks, 6 classes, no university load (break is Aug 15 – Sep 2). Not homework competing with recovery — the vehicle for it. Learn each thing when the project demands it: relationships for products/categories/orders, sessions for the cart, auth for checkout, and SQL by printing `queryset.query` and reading what the ORM emitted.
- **Sep 6 – Oct 3 — SQL mop-up, then JavaScript, then the CSS weekend.**

**Per-track deadlines** (need-by, not calendar order):

| Track | By | Why that date |
|---|---|---|
| Python & OOP | Day 7 | load-bearing for everything |
| Django | Sep 5 | end of module 21 |
| SQL | Sep 12 | mostly free via the ORM during module 21 |
| HTML/CSS | Sep 26 | before React |
| JavaScript | Oct 3 | the wall is **module 26** (hooks, state), not module 25 (JSX, props) |

Debt ~95h against a ~130h runway to Sep 5. Clear before module 28, where the job launch starts.

## Scope limits that keep this survivable

**JavaScript — only the React-critical subset:** `let`/`const` and scope, arrow functions, template literals, **array methods (`map`/`filter`/`reduce`/`find`)**, objects/destructuring/spread, `import`/`export`, **promises/`async`-`await`/`fetch`/try-catch**, minimal DOM. **Skip:** JS classes (React is hooks), prototypes, generators, deep closure theory, TypeScript.

**CSS — exactly four conceptual things:** box model, flexbox, grid, media queries. Everything else in CSS is lookup, forever, for everyone. One weekend, not a sprint. Flexbox Froggy + Grid Garden ≈ 3h.

## Parked on purpose — do not suggest these

- **All unwatched DSA recordings (modules 11–19).** Interview prep; interviews are 2027. Blocks nothing on the current path. Resume September as 2–3 *problems* a week — solve, do not watch. Most seductive item on the list because it feels like real CS.
- **Module 18's recording** (Django auth, advanced queries) — useless before I know basic Django; becomes optional revision after module 21.
- **Recordings generally** — attend live, never chase recordings. A missed class is gone; recordings are debt that compounds.
- **LeetCode, HTML/CSS polish, TypeScript** — none block anything before October.

## AI cutoff

**Module 20 is the last assignment I lean on AI for. From module 21 (Aug 16) I write what I submit.**

For an AI-assisted submission, extract value instead of nothing: write in plain words what the solution needs *before* AI sees it → let it produce → then 20 minutes of *"explain this line, why is it needed, what breaks without it?"* → break it on purpose and fix it back → **log every concept I could not have written as a `1`** → three README sentences on what it does, why it is built that way, and what I still do not understand.

## When I fall behind, cut in this order

1. CSS depth — learn on demand, accept ugly
2. LeetCode / DSA — already parked, park longer
3. Project polish — READMEs, deployment, styling
4. Project **scope** — three honest pages instead of ten
5. Last resort: slip the JavaScript deadline into module 26

**Never cut:** sleep, evenings with my wife, or the rebuild-from-empty step.

## Friday checkpoint — 30 min

Modules 8–18 did not fail because the plan was wrong. They failed because **nothing forced the drift to become visible**. Every Friday: tick what cleared → log anything AI wrote as a `1` → check pace against each track's deadline → if behind, cut *one* thing deliberately from the list above → three sentences on what I learned, what is fuzzy, what is next.

Track three numbers only: **did I loop today** (the floor counts), **concept debt count** (must fall weekly), **did I submit my own work** (from Aug 16, yes/no).
