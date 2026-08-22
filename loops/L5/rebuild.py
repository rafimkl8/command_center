# L5 rebuild -- classes: class, __init__, self, instance attributes,
# methods. Written from an empty file, no reference, no AI. Corrected
# through senior review (see ../README.md for what was wrong in the first
# passes and why).

# -- 1: the class, with __init__ storing two instance attributes --
# DailyTask (CapWords) is the blueprint. __init__ runs automatically, once,
# each time DailyTask(...) is called -- it is not called by name directly.
# self is whichever instance is currently being constructed; self.first_task
# = first_task stores that value onto THIS instance specifically, not
# anywhere shared.
class DailyTask:
    def __init__(self, first_task, second_task):
        self.first_task = first_task
        self.second_task = second_task

    # -- methods: same shape as a plain function, defined inside the class,
    # self first -- Python auto-slots whatever sits before the dot at the
    # call site into self. Each of these reassigns one attribute on
    # whichever instance called it.
    def task_one(self, new_task_one):
        self.first_task = new_task_one

    def task_two(self, new_task_two):
        self.second_task = new_task_two


# -- 2: two separate instances, built with different values --
tasks = DailyTask("Brush teeth", "Have Breakfast")
tasks2 = DailyTask("Have dinner", "Sleep")

# -- 4: a method called on ONE instance only (tasks), not tasks2 --
tasks.task_one("Brush teeth & floss")
print(tasks.first_task)      # "Brush teeth & floss" -- tasks, mutated

tasks.task_two("Have breakfast with oats")
print(tasks.second_task)     # "Have breakfast with oats" -- tasks, mutated

# -- 5: same attribute (second_task), printed on BOTH instances afterward.
# tasks2 was never touched by any method call -- this is what proves the
# two instances hold independent data, not just "different because built
# differently." tasks2.second_task below is still exactly its original
# constructor value.
print(tasks2.second_task)    # "Sleep" -- tasks2, untouched, unaffected

# -- 3: an attribute from each instance, shown independently --
print(tasks.first_task)      # "Brush teeth & floss"
print(tasks2.first_task)     # "Have dinner" -- different value, same class
