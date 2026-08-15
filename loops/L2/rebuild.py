# L2 rebuild -- scope (local/global/enclosing), *args/**kwargs, and the
# mutable-default trap in its own right. Written from an empty file, no
# reference, no AI. Corrected through senior review (see ../README.md for
# what was wrong in the first pass and why).

# -- 1: global scope, read vs write --
count = 0

def counter():
    global count
    count = count + 1
    return count

def counter2():
    return count

print(counter2())   # reads the global with no keyword needed -> 0
print(counter())    # mutates the global via `global` -> 1

# -- 2: enclosing scope, nonlocal --
def action():
    show = "hi"

    def action2():
        nonlocal show
        show = "hello"

    action2()
    print(show)      # proves the enclosing variable actually changed -> hello

action()

# -- 3: *args and **kwargs together with a named parameter --
def alltogether(name, *args, **kwargs):
    print(name)      # "Rafi"
    print(args)      # (1, 2, 5) -- unpacked at the call site into positional args
    print(kwargs)    # {'height': '6ft'} -- unpacked at the call site into keyword args

alltogether("Rafi", *(1, 2, 5), **{'height': "6ft"})

# -- 4: the mutable-default trap, and the fix --

# Buggy version: the empty list is created ONCE, at function definition time,
# and every call that skips `collection` shares that same list object.
def collector(currency_name, collection=[]):
    collection.append(currency_name)
    return collection

print(collector("England"))       # ['England']
print(collector("Bangladesh"))    # ['England', 'Bangladesh']  <- accumulates, the bug

# Fixed version: None sentinel default, real list created fresh inside the
# body on every call, so nothing is shared across calls.
def collector2(currency_name, collection=None):
    if collection is None:
        collection = []
    collection.append(currency_name)
    return collection

print(collector2("Spain"))        # ['Spain']
print(collector2("Australia"))    # ['Australia']  <- does not accumulate, fixed
