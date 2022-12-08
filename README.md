Enable function chaining for any object.

Contained is a class that can wrap any type and make it possible to do function chaining on that object, much like functional piping.

Any method that is defined on the contained type is possible to call, whether it returns a copy or mutates in place.
It is also possible to call operators and any builtin function, without breaking the chain.
To get the original variable back out of the Contained, just call it with no args.

```python
ex = ['hello', 'world']
Contained(ex)() == ex  # True

# methods
Contained(['hello']).extend(['world'])() == ex  # True

# operators
Contained(['hello']).add(['world']).contains('hello')()  # True

# builtins
Contained(ex).len().type()()  # <class 'int'>
```
