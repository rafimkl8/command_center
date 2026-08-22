# L6 — Class variables vs instance attributes, `@staticmethod`, `@classmethod`

**Status:** ✅ closed
**Clears:** Module 4 → course → *"Classes, objects, instance variables, class variables, methods, constructors, static methods"* — the **class variables** and **static methods** portion. Combined with L5 (classes, objects, instance variables, methods, constructors), this course line is now **fully cleared**.
**Also clears:** `recovery.html` loop index, L6 line — *"Class vs instance attributes, `@staticmethod`, `@classmethod`"* — in full. Note: `@classmethod` is named in that loop-index line but not in the weeks.js course string above (which says only "static methods"); this loop covers `@classmethod` regardless, matched against the loop-index text specifically.

## What this loop is about

Three ideas, building directly on L5's classes:

1. **Class variables.** Declared inside the class body, outside any method — belongs to the class itself, not to any one instance. Every instance that hasn't shadowed it looks the name up on the class and sees one shared value. This is the opposite default from instance attributes (L5), which are independent per instance from the start.
2. **The lookup-vs-assignment split — the actual mechanism, not just the outcome.** Reading `instance.attr` is a *lookup*: Python checks the instance's own data first, and only falls back to the class if the instance has no attribute of that name. Writing `instance.attr = value` is *unconditional assignment*: it always creates/rebinds a name directly on the instance, with no lookup involved, regardless of whether a class variable of that name exists. So `ClassName.attr = value` (assignment through the class) mutates the one shared value, visible to every instance that hasn't shadowed it — but `instance.attr = value` (assignment through an instance) never touches the class variable at all; it creates a new instance attribute that permanently shadows it for that one instance, from then on, even if the class variable is changed again afterward.
3. **Mutation vs reassignment on the shared object.** If a class variable is itself a mutable object (e.g. a list) and code does `instance.that_list.append(x)`, no assignment happens to `that_list` at all — Python looks it up (finds the one shared object via the class, since the instance has no attribute of that name) and mutates that same object in place. Every instance's lookup still resolves to that one object, so the appended item is visible through every instance. This is the same shared-mutable-object mechanism as L2's mutable-default-argument trap, in a new location.
4. **`@staticmethod`.** A method that takes neither `self` nor `cls`. It behaves exactly like a plain function — the only reason it lives inside the class is namespacing (it's logically grouped under the class). It has zero access to instance or class state; anything it needs must be passed in as a normal argument.
5. **`@classmethod`.** Takes `cls` as its first parameter (by convention, filled in automatically the same way `self` is), and `cls` refers to the class itself, not any instance. Because of this, a classmethod can read and reassign class variables through `cls`, and can build and return a new instance using `cls(...)` — the basis for alternative constructors.

## The misconception this loop corrected

Blank page treated class variables as if they followed the same "private per instance" rule as instance attributes ("the other instance doesn't change... same for the instance attribute, don't changes") — exactly backwards, since sharing across instances is the entire reason class variables exist as a distinct concept. `@staticmethod` was blank-page defined as "doesn't get changed," which isn't a definition of anything. During teaching, `Dog.species = "Feline"` (class-level reassignment, affects both instances) was initially answered identically to `d1.species = "Feline"` (instance-level assignment, shadows one instance only) — both were guessed as "Canine for both," collapsing two mechanically different operations into one. Corrected by separating every case into its read half and its write half explicitly, rather than reasoning about the outcome directly.

## Why it matters for Django

Class variables are how Django expresses configuration and defaults that belong to the *model itself*, not to any one row — `class Meta:` options, choices tuples, or a manager attribute like `objects = models.Manager()` are all class-level, shared across every instance (every row) unless a specific instance overrides something. `@classmethod` is the mechanism behind Django's own alternative constructors and manager methods (`Model.objects.create(...)`-style patterns build on exactly this: `cls(...)` inside a method that isn't `__init__`). `@staticmethod` shows up for logic that's related to a model conceptually but needs no access to `self` or `cls` at all — a pure helper function grouped under the class for organization.

## The rebuild spec I was given (not code — this is what I had to build from empty)

Open a brand new empty `.py` file. No docs, no AI, no old code. Build:

1. A class of my own choosing, with one class variable and an `__init__` setting at least one instance attribute.
2. At least two instances of that class.
3. Print the class variable through both instances, proving they see the same shared value.
4. Reassign the class variable through the **class name itself**, then print it through both instances again, proving the change is visible to both.
5. Assign a new value to that same-named attribute through **one instance only**, then print it through both instances again, proving that instance now shadows it while the other still sees the class-level value.
6. A `@staticmethod` taking at least one argument, touching no `self`/`cls`/instance/class state, returning a value — called and printed.
7. A `@classmethod` using `cls` to read/modify the class variable or build a new instance — called and printed.

Rules: no `input()`. Every step's effect must actually be printed, not just run silently.

## What happened in review

- First pass was logically complete and correctly ordered on the first attempt — every step's mechanism was actually demonstrated with a print, not just asserted, including the hard part (constructing both instances before mutating either, learned the hard way in L5).
- One naming issue: a `@staticmethod` that multiplied two numbers was first named `total`, which reads as addition/summation to anyone calling it cold — a real review comment, not a mechanical bug. Renamed to `multiplication`.
- One demonstration was incomplete on the first pass: after the `@classmethod` mutated the class variable, neither instance's attribute was printed afterward. Adding that print surfaced the loop's sharpest point — the previously-shadowed instance (`greeting1`) still showed its shadowed value after the classmethod's mutation, while the never-shadowed instance (`greeting2`) picked up the new class-level value. Reasoned through correctly before being told the answer: the shadow is a permanent, static fact about that one instance's own data from the moment it's created, completely independent of whatever happens to the class variable afterward — there is no re-checking or re-linking to the class once an instance has its own attribute of that name.

See [`rebuild.py`](rebuild.py) for the final, corrected version.
