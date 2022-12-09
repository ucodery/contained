Enable function chaining for any object.

Contained is a class that can wrap any type and make it possible to do function
chaining on that object, much like functional piping.

Any method that is defined on the contained type is possible to call, whether it
returns a copy or mutates in place. It is also possible to call operators and
any builtin function, without breaking the chain. To get the original variable
back out of the Contained, just call it with no args.

```python
from contained import Contained
ex = ['hello', 'world']
Contained(ex)() == ex  # True

# methods
Contained(['hello']).extend(['world'])() == ex  # True

# operators
Contained(['hello']).add(['world']).contains('hello')()  # True

# builtins
Contained(ex).len().type()()  # <class 'int'>
```

Contained can also be given an additional namespace to allow for custom
chained methods. This can be a module dict, class dict, globals, locals, or
any other dict mapping names to objects.

```python
def stringify_number_colleciton(c):
    return (s if not str(s).isdigit() else int(s) for s in c)

(Contained({1, "A", 3.02, ()}, additional_methods=locals())
    .stringify_number_colleciton()
    .sorted(key=lambda s: str(s))
    () == 
[(), 1, 3.02, 'A'])
```

```python
import functools, itertools

# if you are on Python >= 3.9 use `additional_methods=(vars(functools) | vars(itertools))`
(Contained(42, reversed=True, additional_methods=Contained(vars(functools)).update(vars(itertools))())
    .range()
    .list()
    .takewhile(lambda x: x < 18)
    .dropwhile(lambda x: x <= 5)
    .map(hex)
    .reduce(lambda y, x: f"{y} {x}")
    () ==
"0x6 0x7 0x8 0x9 0xa 0xb 0xc 0xd 0xe 0xf 0x10 0x11")
```
