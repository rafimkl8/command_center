# L1 rebuild — def, parameters vs arguments, return, default parameters
# Written from an empty file, no reference, no AI. Corrected through senior review
# (see ../README.md for what was wrong in the first pass and why).

# -- 1: default parameter --
def multi(a, b=10):
    return a + b

result = multi(7)
print(result)

# -- 2: returning two values (tuple packing/unpacking) --
def maxsum(numbers):
    return max(numbers), sum(numbers)

highest, total = maxsum([1, 4, 5, 9])
print(highest)
print(total)

# -- 3: *args --
# can't remember correctly, honestly skipped — this is L2 material

# -- 4: **kwargs --
# can't remember correctly, honestly skipped — this is L2 material

# -- 5: mutating a list passed into a function (the mutable-default trap) --
def currency_list(country, country_list=[]):
    country_list.append(country)
    return country_list

current_list = currency_list("England")
print(current_list)
current_list = currency_list("Bangladesh")
print(current_list)

# The output grows across calls instead of resetting, because country_list=[]
# is created ONCE, when Python reads the def line -- not fresh on every call.
# Every call that doesn't pass its own list shares that same list object, and
# .append() just keeps adding to it.
