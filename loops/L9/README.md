# L9 — Dunders: `__str__`, `__repr__`, `__eq__`, `__len__`

**Status:** ✅ closed
**Clears:** `recovery.html` loop index, L9 row — *"Dunders: `__str__`, `__repr__`, `__eq__`, `__len__`"* — in full.
**Also clears (in full, new):** Module 4 → `extra` → *"Understand `__str__`, `__repr__`, `__len__`, `__eq__` dunder methods — used constantly."* Unlike L7/L8, this line isn't bundled with any other still-open concept — closing it clears the whole line. **Note the tier:** this item is `extra` (tier `resource`), which `recovery-plan.md` already prices at zero hours — closing it does not move the audit's headline debt-hour total, unlike L5–L8 which each chipped into a priced `course`-tier line. No module 4 `course` bullet mentions dunders at all, so no course-line partial clearance happens here.

## What this loop is about

A **dunder** ("double underscore") is a method whose name starts and ends with `__`. The defining trait isn't the naming style — it's that it's called **implicitly** by Python in response to other syntax, never written explicitly by the caller. `__init__` (L5) was already an example; this loop names the pattern and covers four more:

1. **`__str__`** — human-readable string. Triggered by `print(obj)`, `str(obj)`, f-strings. Must `return` a string, never `print` internally — the outer call does the actual printing. With no `__str__` defined, Python shows the default `<ClassName object at 0x...>`.
2. **`__repr__`** — developer/debugging-facing string, by convention shaped like valid code that could recreate the object (e.g. `ClassName(x=5)`). Triggered directly by `repr(obj)` or a bare variable at a prompt. Also the **fallback** for `print()`/`str()` when a class has no `__str__` at all — not a response to `__str__` "failing," but to it never being defined.
3. **`__eq__`** — data-based equality instead of Python's default identity check (`==` without it compares "same object in memory," not "same data," so two separate instances with identical data are `False` by default). Takes `self` and `other` — `other` is the **whole other object**, not one of its attributes — and must `return` a boolean built from comparing attributes on both sides (e.g. `self.x == other.x`).
4. **`__len__`** — for classes that wrap a countable collection. Triggered by `len(obj)`. Must `return` a non-negative integer; anything else (a string, a negative number) raises an error at the `len()` call site, not silently.

**The payoff, tied back to L8's polymorphism:** any object that implements these plays by contract with Python's own generic syntax (`print`, `==`, `len`) without that syntax needing to know or care what class the object actually is — the same "shared name, per-class behavior, zero caller-side branching" idea from L8, just applied to built-in syntax instead of a method name you invented yourself.

## The blank page result

All five blank-page questions (what a dunder is generally, and what each of `__str__`/`__repr__`/`__eq__`/`__len__` does) came back completely blank — same shape as L7 and L8, a from-zero build with nothing to correct at that stage.

## Why it matters for Django

Every Django model's `__str__` is literally what the admin site and `print(some_queryset_item)` display — it's the single most common dunder you'll write in Django. `__repr__`'s "looks like code" convention shows up the same way in Django's own model reprs. `__eq__` and `__len__` are less central day-to-day in Django itself but are the same mechanism QuerySets and other Django internals build on.

## The rebuild spec I was given (not code — this is what I had to build from empty)

Open a brand new empty `.py` file. No docs, no AI, no old code. Build:

1. A class representing something with multiple pieces of data and something naturally countable inside it (own domain, own names).
2. `__str__` — a genuinely human-readable sentence built from the data, not just restating a raw attribute.
3. `__repr__` — following the "looks like code that could recreate the object" convention.
4. `__eq__` — comparing two instances by actual data, not identity.
5. `__len__` — returning the count of the countable-things list.
6. Two instances with genuinely different data.
7. Demonstrate all four dunders actually firing with printed output: `print()` each instance, `repr()` each instance printed, an `==` comparison showing both `True` and `False` cases, `len()` on each instance.

Rules: no `input()`. Every effect printed. No dunder allowed to `print()` internally — `return` only.

## What happened in review

- **Mutable default argument** — first draft had `def __init__(self, category_name, items=[])`. Same L2 trap, flagged as a real catch even though it didn't bite in that particular run (both instances passed explicit lists). Fixed by making `items` a required positional parameter with no default.
- **`__eq__`, first real bug:** `def __eq__(self, other_name): return self.category_name == other_name` — comparing `self.category_name` (a string) directly to `other_name`, which Python actually passes as the **whole other object**, not a name. This produced `AttributeError`-style thinking correctly for the `Placeholder`/int check-question earlier in the session, but the same misunderstanding reappeared in the rebuild itself.
- **`__eq__`, second bug — the more instructive one:** after the naive fix attempt `print(cart1 == cart2.catagory_name)`, traced why the *original* broken version still printed `True` by accident: `self.catagory_name == other_name` (string vs. object) has no direct comparison, so Python falls back and retries the comparison from the other side — `cart2.__eq__("Electronics")` — which then compares two matching strings and returns `True`, masking the bug rather than surfacing it. Real fix required reaching into `other` **inside** the method body (`self.category_name == other.category_name`), not unwrapping the attribute at the call site — the latter was tried first and correctly rejected as defeating the purpose of `__eq__` (callers should never need to know a class's internals to compare two instances).
- **`__repr__` spelling mismatch:** `__init__` used the correctly-spelled `category_name`, but the f-string inside `__repr__` said `catagory_name=` — meaning the repr's own output, if copy-pasted as code, would raise `TypeError: unexpected keyword argument`. Caught and fixed as a real violation of `__repr__`'s "valid code" convention, not cosmetic.
- **Coverage gaps across two passes:** `__repr__` was defined but never actually called/demonstrated in an early draft; `cart2` was compared and measured via `==`/`len()` but never plain-`print()`'d or `repr()`'d, so `__str__`/`__repr__` were only proven on one instance, not shown to generalize. Both fixed by adding the missing calls.
- **Naming:** `__eq__`'s parameter went from `other_name` (misleading — it's not a name) to `other_cart`, which accurately describes what it holds.
- **`__str__` richness:** first version only restated `category_name`; revised to also report `len(self.items)` inline, actually using both pieces of the class's data rather than one.

## English critique history

- First draft: five real issues — called `__repr__` a fallback for when `__str__` "fails" (wrong framing; nothing errors, it's a fallback for *absence*, not failure); conflated `__repr__`'s general purpose with its fallback trigger; described `__len__` as being about "any list object" rather than about a class you write yourself wrapping a collection; used "equity" instead of "equality"; several grammar issues (subject-verb agreement, lowercase "python", recurring `it's`/`its`).
- Second draft: fixed the three conceptual points correctly (fallback-on-absence framing, `__repr__`'s standalone purpose, `__len__` being about a custom class). "Equity" persisted unfixed; several previously-flagged grammar items (lowercase "python", pronoun mismatch, "gets printed", "the value come from") also persisted unchanged despite being named explicitly; one item regressed — "returns true or false" had been correct in an earlier attempt and was rewritten as "return true or false."
- Third draft: fixed all previously-flagged items (equality, capitalization, pronoun agreement, subject-verb agreement) except the regressed "return true or false," which remained.
- Fourth draft: final fix applied to "returns true or false." Accepted as final — conceptually accurate throughout, grammar clean, self-written throughout, never drafted or rewritten by AI at any point.

See [`rebuild.py`](rebuild.py) for the final, corrected version.
