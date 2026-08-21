# L4 — Decorators: wrapping, @ syntax ⚠️

**Status:** ✅ closed (two sittings, as flagged)
**Clears:** Module 3 → course → *"Functions, parameters, keyword args, return statements, decorators, lambda, scope"* — the **decorators** portion. L1 (functions/params/return), L2 (scope), and L3 (lambda) already closed the other five pieces, so this is the last one — **the whole course line is now fully cleared**, not partial.

## What this loop is about

Builds directly on L3 (functions as objects, closures) — a decorator is that exact mechanism wearing different clothes:

1. **The shape.** A decorator is a function that takes a function in and returns a function out — same shape as L3's `division_maker`, just with a function sitting in the slot where a number used to sit. The returned function (conventionally named `wrapper`) is defined *inside* the decorator and is the thing that actually runs later.
2. **`@` is sugar for name-reassignment, nothing more.** `@my_decorator` written above `def target():` is exactly equivalent to `target = my_decorator(target)` run immediately after the `def` block. It does **not** rewrite `target`'s own body — the original function still exists, untouched, trapped inside `wrapper`'s closure. Only the *name* `target` gets reassigned to point at `wrapper` instead.
3. **`*args`/`**kwargs` in `wrapper`'s own signature.** A decorator gets written once and reused on functions with completely different signatures (`say_hi()`, `greet(name)`, `add(a, b)`, every Django view). `wrapper(*args, **kwargs)` collects whatever it's handed generically, without needing to know the original function's parameters in advance, then unpacks it back out again at `original_function(*args, **kwargs)`.
4. **Forwarding the return value.** `result = original_function(*args, **kwargs)` followed by `return result` matters even when it looks pointless — skip the `return` inside `wrapper` and the original function still runs and still computes its real value internally, but that value is discarded and the caller always gets `None` back, because `wrapper` itself then has no return statement of its own.
5. **The closure underneath it, precisely stated.** `wrapper` doesn't "remember" or "hold a copy of" the original function — it keeps a live reference into the decorator's own private scope from that specific call, and the original function (and its arguments, at call time) live inside that scope. This is the same mechanism L3 already covered; decorators don't add a new one.

## Why it matters for Django

`@login_required` is not special syntax — it's this exact shape already written for you. `login_required` is a function that takes a view function and returns a `wrapper` that checks `request.user.is_authenticated` before deciding whether to call the real view (with `*args, **kwargs`, since every view's signature differs) or redirect to login instead. Once this loop's mechanism is solid, `@login_required`, `@admin.register`, and `@receiver` all read as "a function call with `@` sugar," not magic.

## The misconception this loop corrected

Going in, `@` was described as something that "annoints" a function, and wrapping was defined circularly ("the function is held by `@____`, around it") — neither said what actually happens. The real content: `@` performs a name reassignment (`name = decorator(name)`) at definition time, and "wrapping" means writing a *new* function that decides whether/how/when to call the original, not modifying the original itself.

## The rebuild spec I was given (not code — this is what I had to build from empty)

Open a brand new empty `.py` file. No docs, no AI, no old code. Build:

1. A decorator with the correct shape (outer function takes a function, defines `wrapper(*args, **kwargs)`, calls the original inside it, returns `wrapper`) — applied *manually* first (`renamed = my_decorator(original_function)`), no `@` yet.
2. The same decorator applied to a **different** plain function using `@` syntax, called by its own name, proving it behaves the same way as the manual version.
3. A decorated function that takes arguments **and** returns a value, with the return value actually printed at the call site — not just called — to prove it survived the round trip through `wrapper`.
4. One deliberate break-it-then-fix-it experiment on the decorator mechanism itself, then explained in my own words.

## What happened in review

- Step 1's first pass had a `wrapper` that called the original function and returned its result, and nothing else — no added behavior at all. Indistinguishable from calling the original directly, so it didn't actually prove wrapping. Fixed by adding a genuine extra line (`print("You should call back as soon as possible!")`) inside `wrapper`.
- Step 2's first pass reused the *same* function (`call_received`, redefined with an identical body) instead of a genuinely different one — this silently overwrote step 1's `call_received` in the same file (the same naming-collision failure mode flagged back in L1 and L3) and didn't demonstrate anything beyond step 1. Fixed with a distinct function, `outgoing_call`.
- Step 3 went through three passes: first, `call_back` had no `return` at all, so it couldn't test return-forwarding (same `None`-producing shape as step 1's original function). Second, `return result` was added but the call site never printed the result, so a silently-dropped `return` inside `wrapper` would have looked identical from the output. Fixed by wrapping the call in `print(...)`.
- Step 4's first attempt broke the wrong layer: it dropped the `return` inside the *decorated function itself* (`call_now`), which correctly demonstrates L1's no-return-means-`None` rule but isn't specific to decorators at all — it would fail identically with no decorator present. Redone correctly by leaving the decorated function intact and instead removing `return result` from `wrapper`'s own body, run to observe `None` even though the decorated function genuinely computed `11` internally, then restored to confirm the fix.
- Separately, during concept-checking (before any code was written): `@` was first explained as something that "turns `say_hi` into a wrapper" — corrected to "reassigns the name `say_hi` to point at `wrapper`; the original function's body is never edited." And the closure explanation for why `wrapper` keeps access to the original function was first given as "keeps a copy... remembers" — corrected to "keeps a live reference into the outer function's private scope," matching the precise language L3 had already arrived at.

See [`rebuild.py`](rebuild.py) for the final, corrected version.
