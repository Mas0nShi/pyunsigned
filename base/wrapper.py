import operator as op
from base.config import context, wraps
# FunctionType = lambda: None
# WrapperType = lambda: "Wrapper"

def typecast(func):
    @wraps(func)
    def wrapper(self, *args) -> "Wrapper":
        if len(args) == 0:
            return self.__class__(func(self, *args))

        arg0 = args[0]
        if isinstance(arg0, self.__class__):
            wrap = self.__class__ if self.max_bits > arg0.max_bits else arg0.__class__
            return wrap(func(self, arg0))
        elif isinstance(arg0, int):
            return self.__class__(func(self, arg0))
        else:
            raise TypeError(f"unsupported operand type(s) for {func.__name__}: '{self.__class__.__name__}' and '{type(arg0).__name__}'")

    return wrapper

class Int(int):
    ...


class Wrapper(Int):
    max_bits: int

    @context.trace
    def __new__(cls, *args):
        assert len(args) > 0, 'No arguments given'
        return super().__new__(cls, *args) if isinstance(args[0], str) else super(Wrapper, cls).__new__(cls, op.and_(args[0], (1 << cls.max_bits) - 1))

    @context.trace
    @typecast
    def __add__(self, *args) -> "Wrapper":
        return super().__add__(*args)  # type: ignore

    @context.trace
    @typecast
    def __sub__(self, *args) -> "Wrapper":
        return super().__sub__(*args)  # type: ignore

    @context.trace
    @typecast
    def __mul__(self, *args) -> "Wrapper":
        return super().__mul__(*args)  # type: ignore

    @context.trace
    @typecast
    def __truediv__(self, *args) -> "Wrapper":
        return super().__floordiv__(*args)  # type: ignore

    @context.trace
    @typecast
    def __floordiv__(self, *args) -> "Wrapper":
        return super().__floordiv__(*args)  # type: ignore

    @context.trace
    @typecast
    def __mod__(self, *args) -> "Wrapper":
        return super().__mod__(*args)  # type: ignore

    @context.trace
    def __divmod__(self, *args):
        return super().__divmod__(*args)

    @context.trace
    @typecast
    def __pow__(self, *args) -> "Wrapper":
        return super().__pow__(*args)  # type: ignore

    @context.trace
    @typecast
    def __lshift__(self, *args) -> "Wrapper":
        return super().__lshift__(*args)  # type: ignore

    @context.trace
    @typecast
    def __rshift__(self, *args) -> "Wrapper":
        return super().__rshift__(*args)  # type: ignore

    @context.trace
    @typecast
    def __and__(self, *args) -> "Wrapper":
        return super().__and__(*args)  # type: ignore

    @context.trace
    @typecast
    def __xor__(self, *args) -> "Wrapper":
        return super().__xor__(*args)  # type: ignore

    @context.trace
    @typecast
    def __or__(self, *args) -> "Wrapper":
        return super().__or__(*args)  # type: ignore

    @context.trace
    @typecast
    def __radd__(self, *args) -> "Wrapper":
        return self.__add__(*args)

    @context.trace
    @typecast
    def __rsub__(self, *args) -> "Wrapper":
        return self.__sub__(*args)  # type: ignore

    @context.trace
    @typecast
    def __rmul__(self, *args) -> "Wrapper":
        return self.__mul__(*args)  # type: ignore

    @context.trace
    @typecast
    def __rtruediv__(self, *args) -> "Wrapper":
        return self.__floordiv__(*args)  # type: ignore

    @context.trace
    @typecast
    def __rfloordiv__(self, *args) -> "Wrapper":
        return self.__floordiv__(*args)  # type: ignore

    @context.trace
    @typecast
    def __rmod__(self, *args) -> "Wrapper":
        return self.__mod__(*args)  # type: ignore

    @context.trace
    def __rdivmod__(self, *args):
        return super().__rdivmod__(*args)

    @context.trace
    @typecast
    def __rpow__(self, *args) -> "Wrapper":
        return self.__pow__(*args)  # type: ignore

    @context.trace
    @typecast
    def __rlshift__(self, *args) -> "Wrapper":
        return super().__rlshift__(*args)  # type: ignore

    @context.trace
    @typecast
    def __rrshift__(self, *args) -> "Wrapper":
        return super().__rrshift__(*args)  # type: ignore

    @context.trace
    @typecast
    def __rand__(self, *args) -> "Wrapper":
        return super().__rand__(*args)  # type: ignore

    @context.trace
    @typecast
    def __rxor__(self, *args) -> "Wrapper":
        return super().__rxor__(*args)  # type: ignore

    @context.trace
    @typecast
    def __ror__(self, *args) -> "Wrapper":
        return super().__ror__(*args)  # type: ignore

    @context.trace
    @typecast
    def __invert__(self) -> "Wrapper":
        return super().__invert__()  # type: ignore

    @context.trace
    @typecast
    def __neg__(self) -> "Wrapper":
        return super().__neg__()  # type: ignore

    @context.trace
    @typecast
    def __pos__(self) -> "Wrapper":
        return super().__pos__()  # type: ignore

    @context.trace
    @typecast
    def __abs__(self) -> "Wrapper":
        return super().__abs__()  # type: ignore

    @context.trace
    @typecast
    def __round__(self, *args) -> "Wrapper":
        return super().__round__(*args)  # type: ignore

    def __repr__(self):
        # the repr format in context of the class
        if context.repr_format == 'hex':
            return f'{self.__class__.__name__}(0x{hex(self)[2:].zfill(self.max_bits // 4)})'
        elif context.repr_format == 'bin':
            return f'{self.__class__.__name__}(0b{bin(self)[2:].zfill(self.max_bits)})'
        elif context.repr_format == 'dec':
            return f'{self.__class__.__name__}({super().__repr__()})'
        else:
            return super().__repr__()

    @classmethod
    def new(cls, v, base=None) -> "Wrapper":
        args = (v, base) if base else (v,)
        return cls(*args)

    @classmethod
    def wrap(cls, bits: int):
        # @Wrapper.wrap(8)
        # class XXX:
        #     ...
        def decorator(cls) -> "Wrapper":
            cls.max_bits = bits
            return cls

        return decorator
