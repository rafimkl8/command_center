# L2 — Scope, `*args`/`**kwargs`, and the mutable-default trap in its own right

**Status:** ✅ closed
**Clears:** Module 3 → extra → *"Understand `*args` and `**kwargs` deeply — used everywhere in Django views"* (fully). Module 3 → course → *"Functions, parameters, keyword args, return statements, decorators, lambda, scope"* — the **scope** portion only. `lambda` (L3) and `decorators` (L4) still block that line from being marked fully cleared.

## What this loop is about

Three ideas, building on L1's function mechanics:

1. **Scope — local, global, enclosing.** A name defined inside a function is local and dies when the function returns. A name defined at the top of the file is global and lives for the program's life; any function can *read* it, but *writing* to it from inside a function requires the `global` keyword. Enclosing scope is the same idea one level down — a nested (inner) function can read a variable from its enclosing (outer) function automatically, but needs `nonlocal` to reassign it.
2. **The rule underneath both keywords.** Any assignment to a name anywhere inside a function body makes that name local for the *entire* function — even on lines before the assignment. This is why `count = count + 1` inside a function that never declared `global count` raises `UnboundLocalError`: Python decided `count` was local the moment it saw the assignment, then failed to find a local value to read on the right-hand side.
3. **`*args` / `**kwargs`.** `*args` collects extra positional arguments into a tuple; `**kwargs` collects extra keyword arguments into a dict. Both are always present with that type even when nothing is passed (`args` is `()`, not `None`). Parameter order in a `def` line is always: named parameters, then `*args`, then `**kwargs`. At the call site, `*`/`**` are for *unpacking* a collection into separate arguments — without them, a tuple or dict passed as a plain argument lands as a single item, not spread out.
4. **The mutable-default trap, mechanism-first.** `def f(x, items=[])` evaluates `[]` exactly once, at function **definition** time, not per call — the resulting list object is stored on the function itself and reused by every call that omits `items`. The trap only bites when the default is *mutated in place* (`.append()`, `.update()`, `[key] = val`) — reassignment (`x = x + [...]`) always builds a new object and rebinds the local name, leaving the stored default untouched. Immutable types (`int`, `str`, `tuple`) can't be mutated in place at all, so `def g(count=0): count = count + 1` never has this problem — the fix pattern is a `None` sentinel default with the real mutable object created fresh inside the function body on every call.

## Why it matters for Django

`*args`/`**kwargs` show up everywhere in Django's own API — `get_context_data(self, **kwargs)`, view functions, URL routing. Scope discipline (knowing what a function can read vs. must be told to write) is the same reasoning needed later for closures, decorators (L4), and class methods. The mutable-default trap is a classic Django/Python gotcha with model fields and view helpers that take default list/dict arguments.

## The rebuild spec I was given (not code — this is what I had to build from empty)

Open a brand new empty `.py` file. No docs, no AI, no old code. Build:

1. A global counter/tally variable, plus a function that increments it using `global`, and a separate function that only *reads* it (no keyword needed) — call both, print the result to show the global was actually mutated.
2. A nested function pair (outer + inner) where the inner function needs `nonlocal` to modify a variable defined in the outer function — call the outer function, print the result to prove the enclosing variable changed.
3. A function using `*args` and `**kwargs` together, alongside at least one required named parameter, that prints all three received pieces (the named value, the args tuple, the kwargs dict) — call it with a mix of positional extras and keyword extras to prove it collects correctly.
4. Two versions of a "collector" function: one written with a mutable default argument (the buggy version) and one fixed (using `None` as sentinel default) — call the buggy one twice with no argument and print the result both times to expose the bug, then call the fixed one twice with no argument and print to show it does not accumulate.

## What happened in review

- Part 1 initially called `counter2()` (the read-only function) but discarded its return value and printed the global directly instead — dead code that proved nothing. Fixed to print `counter2()`'s return value.
- Part 2 initially set `show = print("hi")`, which stores `None` (the return value of `print`), not the string `"hi"` — and never printed `show` at all, so nothing proved `nonlocal` had done anything. Fixed to `show = "hi"` with a `print(show)` after the inner call.
- Part 3, first pass: called `alltogether("Rafi", (1, 2, 5), {'height': "6ft"})` with no unpacking at the call site — this passes the tuple and dict as two single positional arguments, not spread into `args`/`kwargs`. Fixed to `alltogether("Rafi", *(1, 2, 5), **{'height': "6ft"})`. Also had `print(name, *args, **kwargs)` inside the function body, which forwards `kwargs` as real keyword arguments to `print()` itself — `print()` doesn't accept an arbitrary keyword like `height`, raising `TypeError: print() got an unexpected keyword argument 'height'`. Confirmed by running it. Fixed to three separate plain `print()` calls (`print(name)`, `print(args)`, `print(kwargs)`) — no unpacking needed when you're just displaying a value, only when spreading it into another call's arguments.
- Part 4's first-pass "fix" (`collector2`) didn't fix the actual bug — it overwrote `collection` with a string on every call, never touching the mutable default in a meaningful way. Rewritten using the `None`-sentinel pattern: `collection=None` in the signature, then `if collection is None: collection = []` as the first line of the body, so a fresh list is created on every call instead of once at definition time.

Verified by running the final version: output is `0`, `1`, `hello`, `Rafi`, `(1, 2, 5)`, `{'height': '6ft'}`, `['England']`, `['England', 'Bangladesh']`, `['Spain']`, `['Australia']` — matching expected behavior exactly.

See [`rebuild.py`](rebuild.py) for the final, corrected version.
