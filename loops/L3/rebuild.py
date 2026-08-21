# L3 rebuild -- functions as objects (passing and returning functions),
# and lambda. Written from an empty file, no reference, no AI. Corrected
# through senior review (see ../README.md for what was wrong in the first
# pass and why).

# -- 1: higher-order function -- takes a value and a function, applies the
# function to the value, returns the result. Nothing else.
def apply_function(n, factor):
    return factor(n)

# -- 2: two plain functions to pass into it --
def division(m):
    return m / 2

print(apply_function(5, division))   # 2.5

def multiply(m):
    return m * 2

print(apply_function(5, multiply))   # 10

# -- 3: returning a function from a function (closure) --
# `factor` is locked in when division_maker runs. `divide_by` is defined
# *inside* division_maker and uses `factor` in its own body, so Python keeps
# `factor` alive attached to `divide_by` even after division_maker itself has
# already finished running. Two separate calls create two separate, private
# `factor` values -- hundred and fifty do not share state.
def division_maker(factor):
    def divide_by(n):
        return factor / n
    return divide_by

hundred = division_maker(100)
fifty = division_maker(50)

print(hundred(5))   # 20.0
print(fifty(5))     # 10.0

# -- 4: lambda, two patterns --

# 4a: assigned to a name, then called directly like a normal function.
is_negative = lambda n: n < 0
print(is_negative(5))   # False

# 4b: used inline, passed straight into a built-in higher-order function --
# never given a name. sorted() calls this internally on each item to decide
# order.
fruits = ["Apple", "Blackcurrant", "Banana"]
print(sorted(fruits, key=lambda x: len(x)))   # ['Apple', 'Banana', 'Blackcurrant']
