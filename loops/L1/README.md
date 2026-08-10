# L1 — Functions: def, parameters vs arguments, return, default parameters

**Status:** ✅ closed
**Clears (partial):** Module 3 → course → *"Functions, parameters, keyword args, return statements, decorators, lambda, scope"* — the functions/params/return-statement portion only. Decorators, lambda, and scope are covered in L2–L4; don't mark the Module 3 item fully cleared until those close too.

## What this loop is about

Four core ideas, all about how information moves into and out of a function:

1. **Parameter vs argument** — a parameter is the placeholder named in a function's `def` line; an argument is the actual value supplied when the function is called. Parameter lives in the definition, argument lives in the call.
2. **`return`** — hands a value back to the caller. A function with no `return` statement always gives back `None` — nothing is "stored" anywhere for later; if you didn't capture it, it's gone.
3. **Default parameters** — `def f(a, b=10)` means: if the caller doesn't supply a second argument, `b` falls back to `10`. Overridden per-call by passing an explicit argument.
4. **Returning two values (tuple packing/unpacking)** — `return a, b` packs both values into a single tuple. On the caller's side, `x, y = f()` unpacks that tuple into two variables; `result = f()` instead captures the *whole tuple* as one object, e.g. `result = (1, 9)`, indexable with `result[0]`.

## The trap this loop actually catches: the mutable-default trap

`def f(x, items=[]):` looks safe but isn't. The default value `[]` is created **once**, when Python reads the `def` line — not fresh on every call. Every call that skips the `items` argument shares that *same* list object, so `.append()` keeps growing it across calls instead of resetting. This is officially an L2 topic, but it showed up directly in the L1 rebuild spec (see below), so it got taught here in its L1 context.

**A second, related trap surfaced during the rebuild:** naming a parameter or variable the same as a Python built-in (`list`, `max`, `sum`, `dict`, `str`, etc.) silently shadows the built-in with no warning — until something two functions later breaks in a confusing way. Rule: never name anything the same as a built-in.

## Why it matters for Django

This is the first rung of the ladder the recovery plan is built on: Python's function mechanics — especially `*args`/`**kwargs` (L2) and decorators (L4) — are exactly the vocabulary Django uses everywhere: `@login_required`, `def get_context_data(self, **kwargs)`, view functions that take `request` and return a response. Nothing here is Python-only trivia; it's the syntax Django is built out of.

## The rebuild spec I was given (not code — this is what I had to build from empty)

Open a brand new empty `.py` file. No docs, no AI, no old code. Write **five functions**:

1. A function with a default parameter (own scenario, not `greet`/`"Hello"`).
2. A function that returns two values — call it, unpack into two named variables, print each separately.
3. A function that takes `*args` (not yet taught at L1 — attempt or honestly skip).
4. A function that takes `**kwargs` (same note as #3).
5. A function that mutates a list passed into it — call it twice on the same variable, print after each call, and comment on *why* it changed the way it did.

Rules: no `input()` — pass arguments directly at the call site. Every function must actually be called, with the result printed.

## What happened in review

- `*args` and `**kwargs` were honestly skipped — correct call, since that's L2 material.
- First pass named a tuple-unpacking result variable `max, sum =` and a mutable-default parameter `list=[]` — both shadow Python built-ins. Fixed to `highest, total` and `country_list`.
- First pass had a leftover bug: parameter renamed to `country_list` but the function body still referenced `list` — this would have raised a `TypeError` (the built-in `list.append(country)` resolves, but calls the unbound method with the wrong argument count), not a `NameError`, since `list` still exists as the built-in even though nothing local uses that name anymore. Caught and fixed.

See [`rebuild.py`](rebuild.py) for the final, corrected version.
