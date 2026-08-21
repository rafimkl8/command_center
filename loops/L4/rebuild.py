# L4 rebuild -- decorators: wrapping, @ syntax. Written from an empty file,
# no reference, no AI. Corrected through senior review (see ../README.md for
# what was wrong in the first pass and why).

# -- 1: a basic decorator, applied manually first (no @ yet) --
# call_log is the decorator: it takes a function in, returns wrapper out.
# wrapper is what actually runs later -- it calls the original function
# (captured via closure as demo_function) and adds behavior around it.
def call_log(demo_function):
    def wrapper(*args, **kwargs):
        result = demo_function(*args, **kwargs)
        print("You should call back as soon as possible!")
        return result
    return wrapper

def call_received():
    print("From Saira at 2.00 22 August 2026")

# Manual application -- no @ sugar. show_call_received is the wrapper
# object, not a call. Nothing runs until show_call_received() below.
show_call_received = call_log(call_received)
show_call_received()

# -- 2: the same decorator, applied with @ syntax on a DIFFERENT function --
# @call_log above outgoing_call's def is exactly:
#     def outgoing_call(): ...
#     outgoing_call = call_log(outgoing_call)
# After this runs, the name outgoing_call no longer points at the original
# plain function -- it points at wrapper, with the original trapped inside
# wrapper's closure. The original function's own body is never edited.
@call_log
def outgoing_call():
    print("To Saira at 3.00 22 August 2026")

outgoing_call()

# -- 3: a decorated function that takes arguments AND returns a value --
# wrapper's (*args, **kwargs) collects name/a/b generically and forwards
# them to call_back untouched. wrapper's `return result` forwards the real
# computed value back out -- without it, the caller would always get None
# back no matter what call_back actually computed.
@call_log
def call_back(name, a, b):
    print(f"Call back: {name}, later in your free time!")
    result = a + b
    return result

# print() around the call is deliberate -- it's what actually proves the
# return value survived the round trip through wrapper, rather than just
# calling it and taking the return-forwarding on faith.
print(call_back("Rafi", 5, 6))   # 11

# -- 4: deliberate break-it-then-fix-it -- wrapper's own `return`, not the
# decorated function's. call_back itself is correct and unchanged; only
# wrapper's body is broken, to isolate the bug to the decorator mechanism.
def call_log_broken(demo_function):
    def wrapper(*args, **kwargs):
        result = demo_function(*args, **kwargs)
        print("You should call back as soon as possible!")
        # no `return result` here -- the bug.
    return wrapper

@call_log_broken
def call_back_broken(name, a, b):
    print(f"Call back: {name}, later in your free time!")
    result = a + b
    return result

# call_back_broken's own body still computes and returns 11 correctly --
# but wrapper never returns what it got back from demo_function, so that
# 11 is computed, then discarded. wrapper falls off the end with no return
# statement of its own, which always gives back None.
print(call_back_broken("Rafi", 5, 6))   # None -- the bug, reproduced

@call_log
def call_back_fixed(name, a, b):
    print(f"Call back: {name}, later in your free time!")
    result = a + b
    return result

# Same decorated function, correct decorator (wrapper has `return result`)
# -- the 11 now survives the round trip.
print(call_back_fixed("Rafi", 5, 6))    # 11 -- fixed
