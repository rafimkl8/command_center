# L1 — English track

Written from memory, in my own words, self-corrected across review where wrong.

**Parameters vs arguments:**
> Parameters are placeholders for a function. When you call the function, you pass the argument to the function in place of the parameter. A parameter is the placeholder that gets replaced when you call a function with an argument.

**Return / no return:**
> Return works in a function like returning the output; if you don't return, the function output will be None.

**Default parameters:**
> Default parameters are the parameters that are used by the function when calling the function if arguments are not passed; it will produce the default one set by the function.

**Tuple packing/unpacking (corrected — first pass mislabeled this as the mutable-default trap and called the tuple "a list"):**
> It packs two return elements into one tuple, and when using different outputs like x, y, it produces the outputs separately, but if you use only result, it will give the output in a tuple like result = (1, 9).

**The mutable-default trap (corrected — first pass described the behavior but not why):**
> The mutable default trap happens when a function uses a default parameter with an empty list, like list=[]. If you don't pass your own list, calling the function repeatedly keeps appending to the same list instead of starting fresh — England, then Bangladesh, and so on — because Python creates that list once, and then it just keeps adding with append, it doesn't start empty after each call.
