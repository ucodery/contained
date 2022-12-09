import sys
from contained import Contained

def test_mutating_methods():
    """object methods that mutate the original object can be chained"""
    assert Contained([1, 1, 1, 1]).append(2).pop(1)() == 1


def test_copy_methods():
    """object methods that return a new object can be chained"""
    assert Contained("  test  ").strip().capitalize()() == "Test"


def test_attributes():
    """non-callable object attributes can be chained"""
    assert Contained((42).denominator.numerator)() == 1


def test_builtins():
    """builtins can be chained"""
    assert Contained(42.0).round().repr().set()() == {"4", "2"}


def test_operator():
    """operator functions can be chained"""
    assert Contained("test").add(" string").iadd("!").getitem(4)() == " "


def test_mixed_methods():
    assert Contained([1, 2, 3, 4, 5]).iter().next().numerator.isub(1).str().mul(4)() == "0000"


def test_type_mutation():
    c = Contained([1, 1, 1, 1])
    assert isinstance(c(), list)
    c.len()
    assert isinstance(c(), int)
    c.str()
    assert isinstance(c(), str)


def test_additional_methods():
    from importlib import import_module
    def drop(sequence, i):  # like pop, but don't chain on removed value
        sequence.pop(i)
    if sys.version_info[:2] < (3, 11):
        def call(obj, /, *args, **kwargs):
            return obj(*args, **kwargs)
    assert Contained("json", additional_methods=locals()).import_module().getattr("loads").call('{"test": [42], "extra": "missing"}').drop("extra")() == {"test": [42]}


def test_unwrap():
    """calling Contained is non-destructive"""
    c = Contained(42)
    assert c() == 42
    assert c() == 42


def test_nested():
    """Contained can contain other Contained"""
    orig = 42
    assert Contained(Contained(orig))()() == orig


def test_repr():
    assert repr(Contained(42)) == "Contained(42)"
    assert repr(Contained([1, 1])) == "Contained([1, 1])"
    assert repr(Contained(range(7))) == "Contained(range(0, 7))"
