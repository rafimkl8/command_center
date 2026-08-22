# L5 — Classes: `class`, `__init__`, `self`, instance attributes, methods

**Status:** ✅ closed
**Clears (partial):** Module 4 → course → *"Classes, objects, instance variables, class variables, methods, constructors, static methods"* — the **classes, objects, instance variables (attributes), methods, constructors** portion only. `class variables` and `static methods` are L6 material and still block this line from being marked fully cleared.

## What this loop is about

Five ideas, the first real OOP content in the recovery plan:

1. **`class`.** Not a function, not related to one — a blueprint for a new kind of value. `class Car:` on its own creates zero cars; it creates the shape a car can be made from. Each thing produced from that blueprint is an **instance** (or **object**) of the class — `car1 = Car()` and `car2 = Car()` are two separate instances of one class.
2. **`__init__`.** A method that runs automatically, exactly once, at the moment an instance is created (`Car("red")` triggers it) — never called directly by name. It is not the *only* method a class can have, and it does not run every time *any* method is called — only at construction. Its job is to set up that specific instance's starting data.
3. **`self`.** The specific instance a method is currently operating on. Python supplies it automatically — you never pass it yourself. For a method call like `car1.paint("green")`, whatever sits before the dot (`car1`) is what gets slotted into `self`; for `__init__`, it's the instance being constructed. Same code, different instance plugged in on each call.
4. **Instance attributes.** Data stored on one specific object via `self.name = value`. Each instance holds its own independent copy — changing one instance's attribute has zero effect on another instance of the same class, even though both were built from identical code.
5. **Methods.** Functions defined inside a class, always taking `self` as the first parameter, called via dot notation on an instance (`car1.paint(...)`). `__init__` is not a different *kind* of thing from other methods — it's the same mechanism with one special property (it auto-runs at creation). Methods aren't limited to mutating attributes — they can just as well read an attribute or run a calculation.

## The misconception this loop corrected

Going in, `__init__` was described as something that "gets read first when a function is run" — tangled up with L1–L4's function-call mechanics rather than being its own thing. Corrected in two passes: first to "runs automatically when *any* method is called" (still wrong — this would mean calling `car1.paint(...)` re-triggers `__init__`, which it does not), then finally pinned down to the accurate version: `__init__` runs automatically **only at instantiation**, and is not the *only* method a class is allowed to have.

## Why it matters for Django

A Django model — `class Task(models.Model):` — is exactly this shape. `__init__` (usually inherited, rarely written by hand in Django) is what runs when you build a model instance; every field (`title = models.CharField(...)`) becomes something that behaves like an instance attribute per row; every custom method on a model (`def is_overdue(self):`) is exactly the `self`-based method mechanism covered here. The recovery plan's own diagnosis is blunt about this: skipping OOP depth is what makes Django feel like unexplainable magic.

## The rebuild spec I was given (not code — this is what I had to build from empty)

Open a brand new empty `.py` file. No docs, no AI, no old code. Build:

1. A class of my own choosing (not `Car`/`Dog`), with an `__init__` taking at least two parameters (besides `self`), storing each as an instance attribute.
2. At least two separate instances of that class, constructed with different values.
3. Print an attribute from each instance separately, to prove they hold independent data.
4. At least one method (besides `__init__`) that uses `self` to read and/or change an instance attribute — called on **one instance only**.
5. After that method call, print the same attribute from **both** instances, to prove the untouched instance was unaffected.

Rules: no `input()` — pass values directly at the call site. Every method call's effect must actually be printed, not just run silently.

## What happened in review

- First pass only completed step 1 (the class + `__init__`) — no instances, no prints, no method use yet. Held for a full review pass until the rest existed.
- Naming: the class was first written as `daily_task` (snake_case). Flagged as a real convention violation — Python classes use `CapWords`/PascalCase (`DailyTask`), snake_case is for variables/functions/methods. Fixed.
- Second pass added the method logic (`task_one`, `task_two`, each a bespoke one-attribute setter) and called one of them, printing the result — but never created a second instance at all. This missed the entire point of the exercise: with only one instance in existence, nothing in the code could prove that instances hold independent, non-shared data — which was the reason for the exercise in the first place.
- Third pass added a second instance (`tasks2`) — but constructed it **after** `tasks.task_one(...)` had already run. This ordering meant the final comparison print only showed "two instances built with different constructor values look different," which is true but proves nothing about method calls specifically — there was no *before* state recorded for `tasks2` to compare against an *after* state.
- Fixed by reordering: both instances constructed first, *then* a method (`task_one`, `task_two`) called on `tasks` only, with `tasks.second_task` and `tasks2.second_task` printed afterward side by side — `tasks2.second_task` still showed its original constructor value (`"Sleep"`), `tasks` showed the mutated one. That pairing is what actually demonstrated instance independence under a method call, not construction alone.
- Design note surfaced, not required to fix: `task_one`/`task_two` as one bespoke setter method per attribute doesn't scale — flagged as a pattern to notice, not to repeat as a habit, rather than something wrong for this exercise specifically.

See [`rebuild.py`](rebuild.py) for the final, corrected version.
