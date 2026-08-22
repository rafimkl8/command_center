# L6 rebuild -- class variables vs instance attributes, @staticmethod,
# @classmethod. Written from an empty file, no reference, no AI. Corrected
# through senior review (see ../README.md for what was wrong in the first
# pass and why).

# -- 1: the class, with a class variable (opening) declared outside any
# method, and an __init__ storing two instance attributes --
class Greet:
    opening = "Hello"

    def __init__(self, f_name, l_name):
        self.f_name = f_name
        self.l_name = l_name

    # -- 6: a staticmethod -- no self, no cls, touches no instance/class
    # state at all. Behaves exactly like a plain function; only lives here
    # for namespacing. Named for what it actually does (multiplication),
    # not something misleading like "total".
    @staticmethod
    def multiplication(a, b):
        return a * b

    # -- 7: a classmethod -- cls is supplied automatically, refers to the
    # class itself (not any instance). Used here to reassign the class
    # variable through cls and return the new value.
    @classmethod
    def end(cls, dialogue):
        cls.opening = "Farewell! " + dialogue
        return cls.opening


# -- 2: two separate instances --
greeting1 = Greet("Wasir", "Jayed")
greeting2 = Greet("Saira", "Shahriar")

# -- 3: class variable read through both instances -- both fall back to
# the class since neither instance has its own "opening" attribute yet.
print(greeting1.opening)     # "Hello"
print(greeting2.opening)     # "Hello" -- same shared value

# -- 4: reassignment THROUGH THE CLASS ITSELF -- this changes the one
# shared value. Neither instance has shadowed "opening", so both pick up
# the change on their next lookup.
Greet.opening = "Hi"
print(greeting1.opening)     # "Hi"
print(greeting2.opening)     # "Hi" -- both changed, proving the value is shared

# -- 5: assignment THROUGH ONE INSTANCE ONLY -- this does NOT touch the
# class variable. It's unconditional assignment: Python creates a new
# instance attribute "opening" on greeting1 specifically, with no lookup
# involved on the write side. From this point on, greeting1.opening
# resolves to its own instance attribute, permanently shadowing the class
# variable -- even if the class variable changes again later (see below).
greeting1.opening = "Hey"
print(greeting1.opening)     # "Hey" -- shadowed, own instance attribute now
print(greeting2.opening)     # "Hi" -- untouched, still reads the class variable

# -- 6 (call): staticmethod called and printed --
print(Greet.multiplication(3, 4))   # 12

# -- 7 (call): classmethod called and printed -- mutates the class
# variable via cls, returns the new value.
print(Greet.end("Stay well"))       # "Farewell! Stay well"

# -- proof that the shadow is permanent and independent of later class-
# level mutation: greeting1 already has its own "opening" attribute from
# the assignment above, so end()'s cls.opening reassignment never reaches
# it -- there is no re-checking or re-linking to the class once an
# instance has shadowed a name. greeting2 was never shadowed, so it still
# falls back to the class and picks up the classmethod's new value.
print(greeting1.opening)     # "Hey" -- unaffected by end(), still shadowed
print(greeting2.opening)     # "Farewell! Stay well" -- picks up the classmethod's change
