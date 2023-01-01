from functools import wraps

class Meta(type):
    _repr_format: str
    _trace_mode: bool
    _strict_mode: bool

    @property
    def repr_format(self):
        return self._repr_format

    @repr_format.setter
    def repr_format(self, n):
        if n not in ('hex', 'bin', 'dec', 'raw'):
            raise ValueError(f'invalid repr format: {n}')
        self._repr_format = n

    @property
    def strict_mode(self):
        return self._strict_mode

    @strict_mode.setter
    def strict_mode(self, n):
        if n not in (True, False):
            raise ValueError(f'invalid strict mode: {n}')
        self._strict_mode = n

    @property
    def trace_mode(self):
        return self._trace_mode

    @trace_mode.setter
    def trace_mode(self, n):
        if n not in (True, False):
            raise ValueError(f'invalid trace mode: {n}')
        self._trace_mode = n


class context(metaclass=Meta):
    # repr format: "hex", "bin", "dec", "raw"
    _repr_format = 'raw'
    # strict mode
    _strict_mode = True
    # trace mode
    _trace_mode = False

    @staticmethod
    def trace(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            r = func(*args, **kwargs)
            if context.trace_mode:
                # left padding
                print(f"Trace => [ {func.__name__.rjust(10)} ] # {str(args)} = {r}")
            return r

        return wrapper



if __name__ == '__main__':
    print(context.repr_format)
    context.repr_format = 'hex'
    print(context.repr_format)

    print(context.strict_mode)
