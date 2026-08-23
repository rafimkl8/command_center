# L7 — Inheritance, method overriding, `super()`

**Status:** ✅ closed
**Clears:** `recovery.html` loop index, L7 row — *"Inheritance, method overriding, `super()`"* — in full.
**Also clears (partial):** Module 4 → course → *"Inheritance, polymorphism, method overriding, encapsulation, access modifiers"* — the **inheritance, method overriding, `super()`** portion only. **Polymorphism (L8)** and **encapsulation/access modifiers (L10, `@property`)** are still open and keep this course line from being marked fully cleared.

## What this loop is about

Four ideas, building directly on L5 (classes, `__init__`, `self`) and L6 (the lookup-vs-assignment split, shadowing):

1. **Inheritance.** `class Dog(Animal):` — `Dog` is a **subclass**/**child class** of `Animal`, the **superclass**/**parent class**. Every method and `__init__`-set attribute logic on `Animal` becomes available on a `Dog` instance automatically, via the same child-then-parent lookup mechanism L6 already established for attributes, now applied to methods too. This exists to solve real duplication: shared behavior lives in exactly one place (the parent), and subclasses write only the delta.
2. **Method overriding.** If `Dog` defines its own version of a method that `Animal` also has, the lookup finds `Dog`'s version first and stops — `Animal`'s original is never reached for that call, but it is not modified, deleted, or affected in any way. A plain `Animal()` instance calling the same method still runs `Animal`'s version untouched, because it was never a `Dog` and has no `Dog` version in its lookup chain at all. This is the same shadowing mechanism as L6's instance-attribute-shadowing-a-class-variable, one level up, applied to methods instead of data.
3. **`super()`.** An explicit call written inside an override's own body — not something discovered by a lookup — that says "also run the parent's version of this method, right now, on this same instance." Used when a subclass overrides a method (most often `__init__`) but still wants to reuse the parent's existing logic for the part that's identical, instead of retyping it. `super().__init__(x)` inside `Dog.__init__` runs `Animal.__init__` with the instance already established; control returns to `Dog.__init__` immediately afterward to continue with the child's own new lines.
4. **No override at all.** If `Dog` defines no `__init__` (or no version of some other method) whatsoever, the plain child-then-parent lookup from point 1 finds and runs the parent's version with zero extra syntax — `super()` is only ever needed when a subclass *does* define its own version of a method and still wants the parent's behavior too. No override, no `super()` needed; override plus still wanting the parent's logic, `super()` is how.

## The blank page result

All four blank-page questions (what inheritance solves, which method runs on override, what `super()` does, what happens with no override) came back completely empty — no partial or wrong model to correct, just no prior exposure. Logged plainly as a from-zero build, not a misconception-correction loop like L5/L6.

## Why it matters for Django

`models.Model` is the parent class every Django model inherits from — a model class writing its own `__str__` or `save()` and calling `super().save()` inside it is this exact mechanism. `class Meta:` and `AbstractUser` (for custom user models) are inheritance-based extension points built the same way. Class-based views are a whole framework of overriding one parent view's methods (`get`, `post`, `get_context_data`) and selectively calling `super()` to keep the parent's behavior while adding your own.

## The rebuild spec I was given (not code — this is what I had to build from empty)

Open a brand new empty `.py` file. No docs, no AI, no old code. Build:

1. A parent class with an `__init__` taking at least one parameter and storing it as an instance attribute, plus at least one other method (not `__init__`) that uses `self` and prints something.
2. A child class inheriting from it, with its own `__init__` taking the parent's parameter(s) plus at least one new one, calling `super().__init__(...)` to set up the inherited part, then setting its own new attribute.
3. In the child class, override the same method from step 1 — genuinely different behavior, printing something that makes clear the child's version ran.
4. One instance of the parent, one of the child. Call the shared-named method on both — output must make it visually obvious two different versions ran.
5. Inside the child's override, call `super().<method_name>()` to also run the parent's version, printing both effects so the parent's logic is visibly shown to have actually run too, not just the child's.

Rules: no `input()`. Every step's effect must be printed, not just executed silently.

## What happened in review

- First pass had correct wiring (`class Alarm(Reminder):`, `super().__init__(text)`, `super().r_one(...)`) but **zero print statements inside either method** — both `r_one` implementations only did assignment. Deleting every external `print()` at the bottom would have produced no output at all from the methods themselves, failing steps 1, 3, and 5 outright, which all require the method's own effect to be printed, not just inspected from outside afterward.
- Naming: `r_one` and `no1_reminder` communicated nothing about what they did — same category of issue L5/L6 flagged (`task_one`/`task_two`, `total`→`multiplication`). Renamed to `show_reminder`.
- **Signature mismatch, the real blocker across two passes:** `Reminder.show_reminder(self, no1_reminder)` took one argument; `Alarm.show_reminder(self, new_reminder, new_time)` took two. This defeats the actual point of overriding — a caller holding either a `Reminder` or an `Alarm` should be able to call the same method the same way without knowing which subclass it has, e.g. looping over `[reminder1, alarm1]` calling `.show_reminder(x)` identically. Talked through rather than handed the fix: prompted to connect it back to L1's default-parameter tool. Self-resolved correctly with `new_time="At 8pm"` as a default, making both signatures callable with one argument.
- Flagged but not required to fix: the default `"At 8pm"` is a plausible-looking hardcoded string with no relationship to the actual `r_time` a given `Alarm` was constructed with (`alarm1.r_time = "At 6pm"` but `alarm1.new_time` ends up `"At 8pm"` regardless) — a real inconsistency to be aware of, distinct from L2's mutable-default trap (this default is an immutable string, so no shared-object bug, just a logic mismatch).

## English critique history

- First draft correctly described inheritance and `super().__init__` reuse, but the overriding sentence was conceptually wrong — described overriding as "modifying a value of an attribute of the same method," which blends L6's attribute-shadowing-by-value with L7's actual mechanism (a subclass defining its own version of a method with the same name — nothing about modifying a value). Sent back to their own correct check-2 answer from earlier in the session to self-correct, rather than being told the fix directly.
- Second draft fixed the conceptual error correctly, but `it's`/`its` (fixed three times, then recurred once), `classe's`, and a `,.` punctuation typo needed another pass.
- Third draft: conceptually accurate, grammar clean. Accepted as final, self-written throughout — never drafted or rewritten by AI at any point.

See [`rebuild.py`](rebuild.py) for the final, corrected version.
