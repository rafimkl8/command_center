# L3 — Functions as objects, lambda

**Status:** ✅ closed
**Clears:** Module 3 → course → *"Functions, parameters, keyword args, return statements, decorators, lambda, scope"* — the **lambda** portion. `decorators` (L4) is the last piece still open on that line; don't mark it fully cleared until L4 closes.

## What this loop is about

Three ideas, building on L1 (function mechanics) and L2 (scope):

1. **Functions are objects.** A function value has the same rights as any other value — it can be bound to a name, stored in a list/dict, passed into a function, returned from a function, and inspected (`f.__name__`). The rule that trips people up: referring to a function by name (`func`) is not the same as calling it (`func()`). No parentheses = "this function, the object itself." Parentheses = "call it right now and give me back whatever it returns."
2. **Passing a function as an argument (higher-order functions).** A function that takes another function as a parameter is a higher-order function. The parameter itself needs no parentheses in the `def` line — it's just a name. The parentheses only show up *inside* the function body, at the point where it actually calls what it was handed, e.g. `factor(n)`.
3. **Returning a function from a function — the closure.** A function can define a smaller function inside itself and return that inner function object (again, no parentheses — you're handing back the function, not its result). If the inner function's body refers to a variable from the outer function, Python keeps that variable alive, bundled with the inner function, even after the outer function has already finished running and its other local variables are gone. Each separate call to the outer function creates its own private copy of that captured variable — two returned functions from two different calls do not share state (proved with `hundred`/`fifty` below, `hundred is fifty` would be `False`, same for `division_maker(100) is division_maker(100)` called twice).
4. **`lambda`.** Syntax for a small, unnamed function limited to a single expression — no `return` keyword (the expression's value is returned automatically), no multi-line logic, no statements. Two distinct usage patterns, not one blended idea: assigned to a name and called like a normal function (`is_negative = lambda n: n < 0`), or used inline, passed directly into another function's argument and never named at all (`sorted(fruits, key=lambda x: len(x))`).

## The misconception this loop corrected

Going in, `lambda` was believed to be "a temporary function that only works once." Not true — a lambda can be called as many times as any other function; what actually limits it is that its body must be a single expression (no loops, no multi-statement logic, no `if`/`else` blocks — though a ternary expression is fine since it's still one expression).

## Why it matters for Django

Higher-order functions and closures are the exact mechanism decorators (L4) are built from — a decorator *is* a function that takes a function and returns a (usually wrapped) function. Understanding L3 properly is what makes `@login_required` and `@receiver` legible as "just a function call with `@` syntax sugar" instead of magic. `sorted(..., key=lambda ...)` is also the same shape Django's queryset methods and `key=` sorting use directly.

## The rebuild spec I was given (not code — this is what I had to build from empty)

Open a brand new empty `.py` file. No docs, no AI, no old code. Build:

1. A higher-order function that takes a value and a function, applies the function to the value, and returns the result.
2. At least two plain functions (regular `def`, no lambda) that could each be passed into the function from step 1, and calls demonstrating both.
3. A function that returns another function (a closure) — the outer function takes one argument that gets locked in, the inner function it returns takes a second argument and combines it with the locked-in one. At least two independent instances of the returned function, shown behaving independently.
4. At least two uses of `lambda`: one assigned to a name and called directly, one used inline passed straight into `sorted`/`map`/`filter`, never assigned a name.

## What happened in review

- Blank page surfaced two real gaps before any code was written: `text = lalu()` (calling immediately, storing the *result*) was written where `text = lalu` (referring to the function object itself) was intended — the core parentheses-mean-"call now" distinction wasn't there yet. Also, `lambda` was described as "only works once," which is inaccurate — corrected to: unlimited calls, but limited to a single expression.
- First rebuild attempt for step 1 (`division_maker(n, factor)`) wrote `result = factor / n`, treating the function parameter `factor` as if it were already a plain number — the same lalu()-vs-lalu trap resurfacing in real code. Corrected in stages: first to `factor(n) / n` (calling it correctly but then applying extra arithmetic on top that the spec never asked for), then to `n / factor(n)` (arithmetic flipped but still present), finally to the correct `return factor(n)` — apply the function, return exactly that, nothing added.
- Naming collision caught in review, not required by the spec: the step-1 helper was originally also named `division_maker`, colliding with the unrelated step-3 closure function of the same name, and a plain step-2 function was also named `division`, colliding with the step-3 inner closure function `divide_by`. Renamed the step-1 helper to `apply_function` (it's generic, not division-specific) and the step-3 inner function to `divide_by` to remove both collisions.
- First lambda attempt: assigned `add_one = lambda n: n+1` but then called `add(5)` — `add` was never defined, only `add_one` was. Caught and fixed to call `add_one(5)` — no output actually verified until the name matched.
- Closure section (step 3) had no bugs in the code itself on first attempt — `division_maker`/`divide_by` with `hundred`/`fifty` was correct immediately. The gap was in explaining *why* it works: initial explanations described the observed behavior ("different variables give different results") without explaining the mechanism (the inner function captures/keeps a private reference to the outer function's variable, which is why it survives after the outer call ends). Talked through by tracing `hundred(5)` and `fifty(5)` concretely against the code until the "captured variable, not a shared value" explanation was arrived at independently.

See [`rebuild.py`](rebuild.py) for the final, corrected version.
