# L8 — Polymorphism, abstract classes (`ABC`)

**Status:** ✅ closed
**Clears:** `recovery.html` loop index, L8 row — *"Polymorphism, abstract classes (`ABC`)"* — in full.
**Also clears (partial):** Module 4 → course → *"Inheritance, polymorphism, method overriding, encapsulation, access modifiers"* — the **polymorphism** portion. Combined with L7 (inheritance, method overriding, `super()`), this line now has only **encapsulation, access modifiers** open (L10, `@property`).
**Also clears (partial, new):** Module 4 → course → *"Abstract classes, design patterns: Singleton, Factory, Builder, property decorators"* — the **abstract classes** portion only. **Design patterns (Singleton, Factory, Builder)** are deliberately parked per `recovery-plan.md` (not needed for Django, zero-cost debt) and **property decorators** are L10 — both still open on this line.

## What this loop is about

Two ideas, building directly on L7 (inheritance, method overriding, `super()`):

1. **Polymorphism.** Not a new mechanism — a name for a consequence of L7's method-lookup mechanism. If several subclasses of a common parent each override the same method name, then a single call site — `item.speak()` inside a loop over a mixed list of instances — produces different behavior per object, decided entirely by each object's own class (fixed at construction), with zero `if`/`isinstance` branching written by hand. Adding a new subclass with its own override costs zero edits to the code that already calls the shared method name.
2. **Abstract classes (`ABC`) and `@abstractmethod`.** New syntax: `from abc import ABC, abstractmethod` — `abc` is the built-in module; `ABC` and `abstractmethod` are two things imported from it. A class written as `class ParentClassName(ABC):` becomes **abstract**: Python refuses `ParentClassName()` directly, raising `TypeError`, unconditionally, forever — the abstract class can never satisfy its own requirement, only a subclass can. A method inside it marked `@abstractmethod` (decorator, from L4) has no real implementation (just `pass`) and is a hard requirement: any subclass that doesn't override it with a real implementation is *also* uninstantiable, for the same reason. The failure happens at **instantiation time**, not at class-definition time — defining a broken subclass causes no error at all; only trying to build an instance of it does.
3. **Why they're taught together.** Polymorphism only works safely if every object in the mixed list actually has the shared method. Plain L7 inheritance enforces nothing — a forgotten override just crashes later with `AttributeError`, whenever that method finally gets called, possibly far from the actual mistake. `ABC` + `@abstractmethod` moves that failure earlier and louder: a subclass missing the required method can't even be instantiated, so the mistake is caught immediately, at the exact point it was made.

## The blank page result

All four blank-page questions (what polymorphism is, how it relates to L7, what an abstract class is, what `ABC` does and what happens on a missing implementation) came back completely blank — no partial or wrong model to correct, same shape as L7's from-zero build.

## Why it matters for Django

Class-based views are polymorphism in practice: code that dispatches a request calls `.get()` or `.post()` on a view instance without knowing or checking which specific view subclass it is — each subclass's own override runs automatically. `django.db.models.Model` itself, and Django's own use of `abc`-style patterns in things like custom form fields or storage backends, follow the same "parent declares the contract, subclasses must implement it or fail immediately" shape that `ABC` + `@abstractmethod` teaches directly.

## The rebuild spec I was given (not code — this is what I had to build from empty)

Open a brand new empty `.py` file. No docs, no AI, no old code. Build:

1. Import what's needed from the `abc` module.
2. An abstract parent class inheriting from `ABC`, with at least one `@abstractmethod` (placeholder only) and at least one normal, non-abstract method with a real body that prints something.
3. At least two child classes inheriting from that parent, each providing a different implementation of the abstract method, each printing something that makes clear which subclass ran.
4. Attempt to instantiate the abstract parent directly and demonstrate/prove it raises an error (via `try`/`except` printing the exception, or a comment showing the exact error) — without letting that line actually crash the rest of the file.
5. One instance of each child class, in a single list, looped over calling the shared abstract method's name on each — output must make it visually obvious that different subclasses produced different behavior from the identical call.

Rules: no `input()`. Every step's effect must be printed, not just executed silently (except step 4's failure itself, which only prints if caught).

## What happened in review

- First pass re-marked the overriding methods in both child classes with `@abstractmethod` again — a real misunderstanding, not a typo: re-marking an override as abstract means Python still considers it unfinished, making the child class *also* uninstantiable, defeating the entire point of overriding it. Corrected by removing the decorator from both overrides, keeping only the real implementation.
- First pass also left `juice = JuiceMaker()` as a live, executable line (only commented as an inline note of what error it would raise) — if run as written, this crashes the whole file before steps 3 and 5 (the child instances, the list, the loop) ever execute. Fixed by commenting out the instantiation attempt entirely, per the spec's explicitly allowed option.
- Step 5 was talked through in stages rather than handed directly: instance creation, then the list, then the loop shape — each connected back to material already covered (L5 instances, general list-building, and the exact `for x in [...]: x.method()` pattern already worked through correctly during the polymorphism concept check). Self-written correctly once the shape was named.
- One requirement initially missed: `juice_name` (the required non-abstract method) was defined but never actually called anywhere in the file, so it produced no printed output — same category of gap as L7's "zero print statements inside the method" issue. Fixed by adding `JuiceMaker.juice_name("Orange")`, correctly called on the class itself since it's a `@staticmethod` with no `self`/`cls` need (L6 rule applied correctly, unprompted, once the gap was flagged).
- Naming: the loop variable was first `x`, flagged as communicating nothing about what's being iterated (same category as L5–L7's naming notes). Renamed to `item`.
- Noted, not required to fix: this rebuild never needed `super()` — no child `__init__` reused parent setup. Flagged so abstract classes aren't mistakenly conflated with `super()` as always paired; they're independent tools that happen to sometimes appear together.

## English critique history

- First draft: polymorphism sentences correct throughout every revision. First abstract-class attempt called `ABC` a "python module" that "allows us to use abstract class and abc methods" — conflating the module (`abc`) with the class imported from it (`ABC`). Also described satisfying an abstract method as "you change something on the same methods attribute in child classes" — the same L6/L7-style blending of attribute-value-shadowing with actually defining a new method body. Also stated the error happens "at method defination," contradicting their own correct spoken answer earlier in the session that it happens at instantiation, not definition.
- Second draft fixed the module/class distinction partially but then called `abstractmethod` a "python module" too (it's a decorator) and dropped `ABC` from the sentence entirely; the "assign something to it" phrasing for overriding persisted; the timing sentence was dropped rather than fixed.
- Third draft correctly separated `abc` (module) from `ABC` and `@abstractmethod` (the two things imported from it, correctly identified as a class and a decorator respectively), corrected the override description to "override the same method... in the child class," and restored the instantiation-not-definition timing sentence correctly. Remaining issues were spelling only (twice: "instantiantied"/"overriden") and one run-on comma-splice.
- Fourth draft: conceptually accurate throughout, grammar clean. Accepted as final, self-written throughout — never drafted or rewritten by AI at any point.

See [`rebuild.py`](rebuild.py) for the final, corrected version.
