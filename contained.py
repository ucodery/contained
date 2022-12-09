"""Enable function chaining for any object"""
import builtins
import operator
from types import SimpleNamespace


class Contained:

    def __init__(self, contain, *, reversed=False, additional_methods=None):
        self.__additional_methods = SimpleNamespace(**(additional_methods or {}))
        self.__reversed = reversed
        self.__contain = contain

    def __repr__(self):
        return f"Contained({repr(self.__contain)})"

    def __call__(self):
        return self.__contain

    def __getattr__(self, fn):
        pre = post = ()
        if (chain_method := getattr(self.__contain, fn, None)) is not None:
            if not callable(chain_method):
                self.__contain = chain_method
                return self
        elif (chain_method := getattr(self.__additional_methods, fn, getattr(builtins, fn, getattr(operator, fn, None)))) is not None:
            pre = (self.__contain,)*(not self.__reversed)
            post = (self.__contain,)*(self.__reversed)
        else:
            raise AttributeError(f"'{fn}' is not an attribute of type object {type(self.__contain)} or a builtin or an operator")

        def __chained_method(*args, **kwargs):
            args = *pre, *args, *post
            if (result := chain_method(*args, **kwargs)) is not None:
                self.__contain = result
            return self
        return __chained_method
