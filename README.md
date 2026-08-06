# 🧭 My Command Center

My personal operating system for becoming a **job-ready, AI-fluent software engineer** — while completing a Computer Science degree at the University of the People, staying consistent with faith, family, fitness, and sleep.

Everything here is a self-contained HTML page (no build step, no dependencies). Open the **hub** and navigate from there.

> **▶️ Live hub:** https://rafimkl8.github.io/command_center/
> *(enable once via repo Settings → Pages → Deploy from branch → `main` → `/root`)*

---

## 📍 Where I actually am (Aug 2026)

Modules 1–7 went well. **Modules 8–18 went sideways** — my father-in-law had open-heart bypass surgery and everything went to the family. Assignments and quizzes stayed submitted on time, but with heavy AI assistance, so the concepts never landed.

I'm now on **Module 19–20**, running a deliberate recovery backfill until **Oct 3**.

The audit measured it honestly instead of guessing:

| | |
|---|---|
| **Concept debt** | 22 items — concentrated in **Module 3** (functions, files, exceptions) and **Module 4** (all of OOP) |
| **Django** | modules 16–18 — all of it missing |
| **Counted hours** | ~50h Python + ~48h Django, against ~130h of runway before Sep 5 |
| **Deliberately parked** | all DSA recordings, LeetCode, CSS depth, TypeScript |

Module 4's own note in the plan predicted this exactly: *"If you skip OOP depth, Django will feel like magic you can't control."* It does. That's the whole diagnosis.

**👉 Start at [`recovery.html`](recovery.html), not the dashboard.**

---

## 🎯 The goal

Beginner → deployable full-stack + **AI Application Engineer**.
- **Skills + first freelance income:** end of 2026
- **First salaried role:** 2027
- **Pace:** ~46 study hours/week (sustainable, not the 67h of raw free time), 6× gym, prayer-anchored days, protected sleep.

Not "a coder who can only code." The durable skills are judgement, decomposition, debugging systems I didn't write, and **verifying** AI output — because you cannot review what you cannot read.

---

## 📂 What's in here

| File | What it is |
|------|------------|
| [`index.html`](index.html) | 🧭 **Hub** — links to everything + cross-device sync setup guide |
| [`recovery.html`](recovery.html) | 🩺 **Recovery Audit — start here.** Scores what I actually know from Module 1 on a 0–3 scale, tiers the gaps, prices them in hours, and carries the day-by-day plan through Oct 3 *(syncs across devices)* |
| [`command_center.html`](command_center.html) | ⚙️ **Master dashboard** (9 tabs): reality check, daily routine, weekly system, monthly goals, integrated plan, job "beast mode", sleep/family/hustle, AI career path, principles |
| [`refined_8_month_fullstack_plan.html`](refined_8_month_fullstack_plan.html) | 📚 **The full plan** — all 40 modules across 6 phases (Python → DBs → JS → Django → React → AI specialization) |
| [`weekly_tracker.html`](weekly_tracker.html) | 📅 **Module tracker** — every task as a checkbox, time estimates, auto-prioritized "Remaining" backlog *(syncs across devices)* |
| [`career_launchpad.html`](career_launchpad.html) | 🚀 **Career playbook** — freelancing, job hunt (local/remote/startup), interviews, templates *(syncs across devices)* |
| [`print_routine.html`](print_routine.html) | ⏰ Printable daily routine — **Variant A** (Sleep-Repair Mode) |
| [`print_routine_variant_b.html`](print_routine_variant_b.html) | ⚡ Printable daily routine — **Variant B** (Deep Work Mode) |
| [`weeks.js`](weeks.js) | 📦 The 40-module curriculum — **single source of truth**, loaded by the tracker and the audit |
| [`sync.js`](sync.js) | ☁️ Cross-device sync engine (Firebase) for the trackers |

> Edit a module in `weeks.js` once and both the tracker and the audit pick it up.

---

## 🔁 How I use it

**Daily — one loop, ~100 minutes.** The topic changes; the loop never does:

1. **Blank page, 10 min** — write what I remember before anything opens.
2. **Learn, 40 min** — timeboxed, one source. AI may explain and quiz. **AI may not author.**
3. **Rebuild from empty, 40 min** — the only step that actually builds anything. Never skipped.
4. **Explain it in a paragraph, 10 min** — in English. This *is* the English track.
5. **Log it, 2 min** — tick it in the audit; log anything AI wrote as a `1`.

**The floor:** on the worst day, **one 20-minute loop** is a complete day. There was no floor in module 8, so the floor became zero — and zero days are what compound into eleven-module gaps.

**Friday checkpoint — 30 min, non-negotiable.** Tick what cleared, log what AI wrote, check pace against each track's deadline, cut one thing deliberately if behind, write three sentences. Modules 8–18 didn't fail because the plan was wrong; they failed because nothing forced the drift to become visible.

**From Module 22:** work the `career_launchpad.html` checklists (freelance → applications → interviews).

---

## 🗓️ Recovery timeline

| Dates | Backfill | Live course |
|---|---|---|
| Aug 5–11 | Python, taught in Django's vocabulary | Module 20 — **last** AI-assisted submission |
| Aug 12–14 | Port the To-Do app to Django | Module 20 wrap |
| Aug 16–Sep 5 | Django + SQL, via the project itself | **Module 21 e-commerce — my own work from here** |
| Sep 6–12 | SQL mop-up | Module 22 — exam + deployment |
| Sep 13–26 | JavaScript core + the CSS weekend | Modules 23–24 — DRF, LMS backend |
| Sep 27–Oct 3 | JavaScript finish (async, fetch) | Module 25 — React intro |
| **Oct 4 →** | **Caught up.** DSA restarts, 2–3 problems/week | Module 26 onward at full depth |

**Three builds clear almost all of it:** the OOP To-Do in pure Python, the same app in Django, then the e-commerce project. Not every module gets rebuilt — some debt is cleared by building something bigger that subsumes it.

---

## ☁️ Cross-device sync (iPhone ⇄ Windows)

The trackers save to `localStorage` on each device and sync in real time via a free Firebase project + a private sync code. Full instructions are on the **hub page**.

**Status:** Firebase project created and wired into `sync.js`. Two steps left — publish the Firestore rules (from the hub page), then tap **Connect** and use the same code on both devices.

Security model, briefly: the Firebase web config in `sync.js` is a **public project identifier, not a secret** — Firebase is built that way and it ships in the client on every site that uses it. The real protection is the Firestore rules plus a long code. The rules grant `get` rather than `read` on purpose, because `read` also grants `list`, which would let anyone enumerate every sync code and read all of it. Codes must be 12+ characters, so guessing is impractical. Anyone who learns the exact code can read and overwrite that one document — so the code is a password.

> Until the devices are linked, the audit scores exist in **exactly one browser**. Clearing site data would erase them. Linking is also the backup.

---

## 🛠️ Tech (current → planned)

Python · SQL (PostgreSQL) · HTML/CSS/JS · Django · DRF · React · then AI integration (FastAPI · pgvector · RAG · agents · evals · observability).

> The long game: rebuild this whole Command Center as a real full-stack + AI app — my portfolio capstone.

---

*Consistency beats intensity. A 20-minute day is not a broken streak — it is the streak.*
