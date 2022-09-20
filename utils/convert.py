# -*- coding:utf-8 -*-
"""
@Author: Mas0n
@File: convert.py
@Time: 2022/6/28 22:44
@Desc: It's all about getting better.
"""
import struct
from typing import List, TypeVar, Type
from functools import reduce, partial
import operator
import logging


class _Config:
    _print_type: int = 0
    _print_list: List = ["DEC", "HEX", ]

    def __init__(self):
        logging.basicConfig(level=logging.getLevelName("WARN"), format='[%(module)s:%(lineno)d] %(levelname)s - %(message)s')

    def log_level(self, level: str) -> None:
        logging.getLogger().setLevel(level.upper())

    def print_type(self, t: str):
        assert t not in self._print_list
        self._print_type = self._print_list.index(t.upper())

    def print(self, v):
        if self._print_type == 0:
            return str(v)
        elif self._print_type == 1:
            return hex(v)


Config = _Config()


IntType = {
    'BYTE': {
        'size': 1,
        'max' : 0xff
    },
    'WORD': {
        'size': 2,
        'max' : 0xffff
    },
    'DWORD': {
        'size': 4,
        'max' : 0xffffffff
    },
    'QWORD': {
        'size': 8,
        'max' : 0xffffffffffffffff
    },
    'OWORD': {
        'size': 16,
        'max' : 0xffffffffffffffffffffffffffffffff
    },
}
SIZE_BYTE  = 8
SIZE_WORD  = SIZE_BYTE * 2
SIZE_DWORD = SIZE_BYTE * 4
SIZE_QWORD = SIZE_BYTE * 8
SIZE_OWORD = SIZE_BYTE * 16
# setattr(_SIZE, "BYTE", SIZE_BYTE)
# setattr(_SIZE, "WORD", SIZE_WORD)
# setattr(_SIZE, "DWORD", SIZE_DWORD)
# setattr(_SIZE, "QWORD", SIZE_QWORD)
# setattr(_SIZE, "OWORD", SIZE_OWORD)
_MAX = {}
MAX_BYTE  = 0xFF
MAX_WORD  = 0xFFFF
MAX_DWORD = 0xFFFFFFFF
MAX_QWORD = 0xFFFFFFFFFFFFFFFF
MAX_OWORD = 0xFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFF


def BYTEn(v, n):  return (v >> (n * SIZE_BYTE)) & MAX_BYTE
def WORDn(v, n):  return (v >> (n * SIZE_WORD)) & MAX_WORD
def DWORDn(v, n): return (v >> (n * SIZE_DWORD)) & MAX_DWORD
def QWORDn(v, n): return (v >> (n * SIZE_QWORD)) & MAX_QWORD
def OWORDn(v, n): return (v >> (n * SIZE_OWORD)) & MAX_OWORD


def As2n(lst: List, length: int, size: int) -> int:
    # assert len(lst) == length
    if len(lst) != length:
        logging.warning(f"length vaild, try auto padding: {lst}")
        # lst += [0] * (length - len(lst))
    tv = 0
    for i, v in enumerate(lst):
        tv |= (int(v) << (size * i))
    return tv


def As2ns(handler: callable, lst: List, step: int) -> List: return [handler(lst[i:i+step]) for i in range(0, len(lst), step)]
def n2As(handler: callable, lst: int, length: int) -> list: return [handler(lst, i) for i in range(length)]
def ns2As(handler: callable, lst: List) -> List: return reduce(lambda x, y: x + y, [handler(i) for i in lst])

# array to value.
def BYTEs2WORD(v: List):   return As2n(v, length=2,  size=SIZE_BYTE)
def BYTEs2DWORD(v: List):  return As2n(v, length=4,  size=SIZE_BYTE)
def BYTEs2QWORD(v: List):  return As2n(v, length=8,  size=SIZE_BYTE)
def BYTEs2OWORD(v: List):  return As2n(v, length=16, size=SIZE_BYTE)
def WORDs2DWORD(v: List):  return As2n(v, length=2,  size=SIZE_WORD)
def WORDs2QWORD(v: List):  return As2n(v, length=4,  size=SIZE_WORD)
def WORDs2OWORD(v: List):  return As2n(v, length=8,  size=SIZE_WORD)
def DWORDs2QWORD(v: List): return As2n(v, length=2,  size=SIZE_DWORD)
def DWORDs2OWORD(v: List): return As2n(v, length=4,  size=SIZE_DWORD)
def QWORDs2OWORD(v: List): return As2n(v, length=2,  size=SIZE_QWORD)
# value to array.
def WORD2BYTEs(v: int): return n2As(handler=BYTEn, lst=v, length=2)
def DWORD2BYTEs(v: int): return n2As(handler=BYTEn, lst=v, length=4)
def QWORD2BYTEs(v: int): return n2As(handler=BYTEn, lst=v, length=8)
def OWORD2BYTEs(v: int): return n2As(handler=BYTEn, lst=v, length=16)
def DWORD2WORDs(v: int): return n2As(handler=WORDn, lst=v, length=2)
def QWORD2WORDs(v: int): return n2As(handler=WORDn, lst=v, length=4)
def OWORD2WORDs(v: int): return n2As(handler=WORDn, lst=v, length=8)
def QWORD2DWORDs(v: int): return n2As(handler=DWORDn, lst=v, length=2)
def OWORD2DWORDs(v: int): return n2As(handler=DWORDn, lst=v, length=4)
def OWORD2QWORDs(v: int): return n2As(handler=QWORDn, lst=v, length=2)

# BYTEs
def BYTEs2WORDs(v: List) -> List:   return As2ns(handler=BYTEs2WORD,   lst=v, step=2)
def BYTEs2DWORDs(v: List) -> List:  return As2ns(handler=BYTEs2DWORD,  lst=v, step=4)
def BYTEs2QWORDs(v: List) -> List:  return As2ns(handler=BYTEs2QWORD,  lst=v, step=8)
def BYTEs2OWORDs(v: List) -> List:  return As2ns(handler=BYTEs2OWORD,  lst=v, step=16)
# WORDs
def WORDs2BYTEs(v: List) -> List:  return ns2As(handler=WORD2BYTEs, lst=v)  # TODO: not implementation.
def WORDs2DWORDs(v: List) -> List:  return As2ns(handler=WORDs2DWORD,  lst=v, step=2)
def WORDs2QWORDs(v: List) -> List:  return As2ns(handler=WORDs2QWORD,  lst=v, step=4)
def WORDs2OWORDs(v: List) -> List:  return As2ns(handler=WORDs2OWORD,  lst=v, step=8)
# DWORDs
def DWORDs2BYTEs(v: List) -> List:  return ns2As(handler=DWORD2BYTEs, lst=v)  # TODO: not implementation.
def DWORDs2WORDs(v: List) -> List:  return ns2As(handler=DWORD2WORDs, lst=v)  # TODO: not implementation.
def DWORDs2QWORDs(v: List) -> List: return As2ns(handler=DWORDs2QWORD, lst=v, step=2)
def DWORDs2OWORDs(v: List) -> List: return As2ns(handler=DWORDs2OWORD, lst=v, step=4)
# QWORDs
def QWORDs2BYTEs(v: List) -> List:  return ns2As(handler=QWORD2BYTEs, lst=v)  # TODO: not implementation.
def QWORDs2WORDs(v: List) -> List:  raise ns2As(handler=QWORD2WORDs, lst=v)  # TODO: not implementation.
def QWORDs2DWORDs(v: List) -> List:  raise ns2As(handler=QWORD2DWORDs, lst=v)  # TODO: not implementation.
def QWORDs2OWORDs(v: List) -> List: return As2ns(handler=QWORDs2OWORD, lst=v, step=2)
# OWORDs
def OWORDs2BYTEs(v: List) -> List:  return ns2As(handler=OWORD2BYTEs, lst=v)  # TODO: not implementation.
def OWORDs2WORDs(v: List) -> List:  raise ns2As(handler=OWORD2WORDs, lst=v)  # TODO: not implementation.
def OWORDs2DWORDs(v: List) -> List:  raise ns2As(handler=OWORD2DWORDs, lst=v)  # TODO: not implementation.
def OWORDs2QWORDs(v: List) -> List: return ns2As(handler=OWORD2QWORDs, lst=v)  # TODO: not implementation.


def ROL(data, shift, size):
    shift %= size
    remains = data >> (size - shift)
    body = (data << shift) - (remains << size)
    return body + remains


def ROR(data, shift, size):
    shift %= size
    body = data >> shift
    remains = (data << (size - shift)) - (body << size)
    return body + remains



#
# def wrapOperator(this: object, __a: any, __b: any):
#
#     IntTypeExpandNameList = ['BYTE', 'WORD', 'DWORD', 'QWORD', 'OWORD']
#     IntTypeExpandList: tuple = (BYTE, WORD, DWORD, QWORD, OWORD)
#     if isinstance(__a, IntTypeExpandList) and isinstance(__b, IntTypeExpandList):
#         __a._size > __b._size
#
#     this.__class__ if not isinstance(__b, ) and __a._size > other._size else other.__class__


# class BaseIntType:
#     _size:
#     def __init__(self):
#         pass
#     def __add__(self, other):
def _typeCast(self, other):
    if getattr(self.type, 'size') > getattr(other.type, 'size'):
        return self.__class__
    else:
        return other.__class__


def _binaryOperation(self, other, binaryOp: callable):
    wrap = None
    value = 0
    if issubclass(other.__class__, BaseIntType):
        wrap = _typeCast(self, other)
        value = other.value
    elif isinstance(other, int):
        wrap = self.__class__
    else:
        raise TypeError('only support int or BaseIntType.')

    result = binaryOp(self.value, value)
    # TODO: divmod
    if isinstance(result, tuple):
        result = (wrap(i) for i in result)
    return result


def _unaryOperation(self, unaryOp: callable):
    assert issubclass(self.__class__, BaseIntType)
    return self.__class__(unaryOp(self.value))


class BaseIntType:
    def __init__(self, v):
        self.type = getattr(IntType, self.__class__.__name__)
        self.value = v & getattr(self.type, 'max')

    def __int__(self): return self.value
    def __str__(self): return Config.print(self.value)
    def __repr__(self): return f'{self.__class__.__name__}({self.__str__()})'

    def __add__(self, other): return _binaryOperation(self, other, operator.add)
    def __sub__(self, other): return _binaryOperation(self, other, operator.sub)

    def __mul__(self, other): return _binaryOperation(self, other, operator.mul)
    def __floordiv__(self, other): return _binaryOperation(self, other, operator.floordiv)
    def __truediv__(self, other): return _binaryOperation(self, other, operator.truediv)
    def __mod__(self, other): return _binaryOperation(self, other, operator.mod)
    def __divmod__(self, other): return _binaryOperation(self, other, divmod)
    def __and__(self, other):  return _binaryOperation(self, other, operator.and_)
    def __or__(self, other): return _binaryOperation(self, other, operator.or_)
    def __xor__(self, other): return _binaryOperation(self, other, operator.xor)

    def __invert__(self): return _unaryOperation(self, operator.invert)
    def __lshift__(self, other): return _binaryOperation(self, other, operator.lshift)
    def __rshift__(self, other): return _binaryOperation(self, other, operator.rshift)

    def __radd__(self, other): return _binaryOperation(other, self, operator.add)
    def __rsub__(self, other): return _binaryOperation(other, self, operator.sub)
    def __rmul__(self, other): return _binaryOperation(other, self, operator.mul)
    def __rfloordiv__(self, other): return _binaryOperation(other, self, operator.floordiv)
    def __rtruediv__(self, other): return _binaryOperation(other, self, operator.truediv)
    def __rmod__(self, other): return _binaryOperation(other, self, operator.mod)
    def __rdivmod__(self, other): return _binaryOperation(other, self, divmod)
    def __rand__(self, other): return _binaryOperation(other, self, operator.and_)
    def __ror__(self, other): return _binaryOperation(other, self, operator.or_)
    def __rxor__(self, other): return _binaryOperation(other, self, operator.xor)
    def __rlshift__(self, other): return _binaryOperation(other, self, operator.lshift)
    def __rrshift__(self, other): return _binaryOperation(other, self, operator.rshift)
    # bool
    def __eq__(self, other): return _binaryOperation(self, other, operator.eq)
    def __ge__(self, other): return _binaryOperation(self, other, operator.ge)
    def __gt__(self, other): return _binaryOperation(self, other, operator.gt)
    def __le__(self, other): return _binaryOperation(self, other, operator.le)
    def __lt__(self, other): return _binaryOperation(self, other, operator.lt)
    def __bool__(self): return _unaryOperation(self, operator.is_not)
    # TODO: list[idx]
    # def __index__(self): return self.value
    # function
    def __hex__(self): return hex(self.value)

    def hex(self): return self.__hex__()
    def bit_ror(self, other): return BYTE(ROR(self.value, self._convert(other), SIZE_BYTE))
    def bit_rol(self, other): return BYTE(ROL(self.value, self._convert(other), SIZE_BYTE))

    def toWORD(self): return WORD(self.value)
    def toDWORD(self): return DWORD(self.value)
    def toQWORD(self): return QWORD(self.value)
    def toOWORD(self): return OWORD(self.value)


class BYTE:
    _size = SIZE_BYTE
    @staticmethod
    def _convert(obj): return obj._value if isinstance(obj, BYTE) else obj
    @staticmethod
    def _equation(obj): return obj._value if isinstance(obj, (BYTE, WORD, DWORD, QWORD, OWORD)) else obj
    def _type_convert(self, other): return self.__class__ if not isinstance(other, int) and self._size > other._size else other.__class__

    def __init__(self, v): self._value = v & MAX_BYTE
    def __int__(self): return self._value
    def __str__(self): return Config.print(self._value)
    def __repr__(self): return f'BYTE({self.__str__()})'

    def __add__(self, other): return self._type_convert(other)(operator.add(self._value, self._convert(other)))
    # def __add__(self, other): return self._type_convert(other)(operator.add(self._value, self._convert(other)))
    def __sub__(self, other): return self._type_convert(other)(self._value - self._convert(other))
    def __mul__(self, other): return self._type_convert(other)(self._value * self._convert(other))
    def __floordiv__(self, other): return self._type_convert(other)(self._value // self._convert(other))
    def __truediv__(self, other): return self._type_convert(other)(self._value // self._convert(other))
    def __mod__(self, other): return self._type_convert(other)(self._value % self._convert(other))
    def __divmod__(self, other): return self._type_convert(other)(divmod(self._value, self._convert(other)))
    def __and__(self, other): return self._type_convert(other)(self._value & self._convert(other))
    def __or__(self, other): return self._type_convert(other)(self._value | self._convert(other))
    def __xor__(self, other): return self._type_convert(other)(self._value ^ self._convert(other))

    def __invert__(self): return BYTE(~self._value)
    def __lshift__(self, other): return BYTE(self._value << self._convert(other))
    def __rshift__(self, other): return BYTE(self._value >> self._convert(other))

    def __radd__(self, other): return self._type_convert(other)(self._convert(other) + self._value)
    def __rsub__(self, other): return self._type_convert(other)(self._convert(other) - self._value)
    def __rmul__(self, other): return self._type_convert(other)(self._convert(other) * self._value)
    def __rfloordiv__(self, other): return self._type_convert(other)(self._convert(other) // self._value)
    def __rtruediv__(self, other): return self._type_convert(other)(self._convert(other) // self._value)
    def __rmod__(self, other): return self._type_convert(other)(self._convert(other) % self._value)
    def __rdivmod__(self, other): return tuple(self._type_convert(other)(_v) for _v in divmod(self._convert(other), self._value))  # TODO: Has Design Issue.
    def __rand__(self, other): return self._type_convert(other)(self._convert(other) & self._value)
    def __ror__(self, other): return self._type_convert(other)(self._convert(other) | self._value)
    def __rxor__(self, other): return self._type_convert(other)(self._convert(other) ^ self._value)
    def __rlshift__(self, other): return self._type_convert(other)(self._convert(other) << self._value)
    def __rrshift__(self, other): return self._type_convert(other)(self._convert(other) >> self._value)
    # bool
    def __eq__(self, other): return self._value == self._equation(other)
    def __ge__(self, other): return self._value >= self._equation(other)
    def __gt__(self, other): return self._value > self._equation(other)
    def __le__(self, other): return self._value <= self._equation(other)
    def __lt__(self, other): return self._value < self._equation(other)
    def __bool__(self): return self._value != 0
    # list[idx]
    def __index__(self): return self._value
    # function
    def hex(self): return hex(self._value)
    def value(self): return self._value

    def ror(self, other): return BYTE(ROR(self._value, self._convert(other), SIZE_BYTE))
    def rol(self, other): return BYTE(ROL(self._value, self._convert(other), SIZE_BYTE))

    def toWORD(self): return WORD(self._value)
    def toDWORD(self): return DWORD(self._value)
    def toQWORD(self): return QWORD(self._value)
    def toOWORD(self): return OWORD(self._value)


class WORD:
    _size = SIZE_WORD
    @staticmethod
    def _convert(obj): return obj.value() if isinstance(obj, WORD) else obj
    @staticmethod
    def _equation(obj): return obj.value() if isinstance(obj, (BYTE, WORD, DWORD, QWORD, OWORD)) else obj
    def _type_convert(self, other): return self.__class__ if not isinstance(other, int) and self._size > other._size else other.__class__

    def __init__(self, v): self._value = v & MAX_WORD
    def __int__(self): return self._value
    def __str__(self): return Config.print(self._value)
    def __repr__(self): return f'WORD({self.__str__()})'
    def __add__(self, other): return WORD(self._value + self._convert(other))
    def __sub__(self, other): return WORD(self._value - self._convert(other))
    def __mul__(self, other): return WORD(self._value * self._convert(other))
    def __floordiv__(self, other): return WORD(self._value // self._convert(other))
    def __truediv__(self, other): return WORD(self._value // self._convert(other))
    def __mod__(self, other): return WORD(self._value % self._convert(other))
    def __divmod__(self, other): return WORD(divmod(self._value, self._convert(other)))
    def __and__(self, other): return WORD(self._value & self._convert(other))
    def __or__(self, other): return WORD(self._value | self._convert(other))
    def __xor__(self, other): return WORD(self._value ^ self._convert(other))
    def __invert__(self): return WORD(~self._value)
    def __lshift__(self, other): return WORD(self._value << self._convert(other))
    def __rshift__(self, other): return WORD(self._value >> self._convert(other))

    def __radd__(self, other): return WORD(self._convert(other) + self._value)
    def __rsub__(self, other): return WORD(self._convert(other) - self._value)
    def __rmul__(self, other): return WORD(self._convert(other) * self._value)
    def __rfloordiv__(self, other): return WORD(self._convert(other) // self._value)
    def __rtruediv__(self, other): return WORD(self._convert(other) // self._value)
    def __rmod__(self, other): return WORD(self._convert(other) % self._value)
    def __rdivmod__(self, other): return WORD(divmod(self._convert(other), self._value))
    def __rand__(self, other): return WORD(self._convert(other) & self._value)
    def __ror__(self, other): return WORD(self._convert(other) | self._value)
    def __rxor__(self, other): return WORD(self._convert(other) ^ self._value)
    def __rlshift__(self, other): return WORD(self._convert(other) << self._value)
    def __rrshift__(self, other): return WORD(self._convert(other) >> self._value)
    # bool
    def __eq__(self, other): return self._value == self._equation(other)
    def __ge__(self, other): return self._value >= self._equation(other)
    def __gt__(self, other): return self._value > self._equation(other)
    def __le__(self, other): return self._value <= self._equation(other)
    def __lt__(self, other): return self._value < self._equation(other)
    def __bool__(self): return self._value != 0
    # list[idx]
    def __index__(self): return self._value
    # function
    def hex(self): return hex(self._value)
    def value(self): return self._value

    def ror(self, other): return WORD(ROR(self._value, self._convert(other), SIZE_WORD))  # Rotate Right
    def rol(self, other): return WORD(ROL(self._value, self._convert(other), SIZE_WORD))  # Rotate Left

    def byteN(self, idx): return BYTE(BYTEn(self._value, idx))
    def byte0(self): return self.byteN(0)
    def byte1(self): return self.byteN(1)
    def bytes(self): return [self.byteN(idx) for idx in range(2)]

    def toDWORD(self): return DWORD(self._value)
    def toQWORD(self): return QWORD(self._value)
    def toOWORD(self): return OWORD(self._value)


class DWORD:
    _size = SIZE_DWORD
    @staticmethod
    def _convert(obj): return obj.value() if isinstance(obj, DWORD) else obj
    @staticmethod
    def _equation(obj): return obj.value() if isinstance(obj, (BYTE, WORD, DWORD, QWORD, OWORD)) else obj
    def __init__(self, v): self._value = v & MAX_DWORD
    def __int__(self): return self._value
    def __str__(self): return Config.print(self._value)
    def __repr__(self): return f'DWORD({self.__str__()})'
    def __add__(self, other): return DWORD(self._value + self._convert(other))
    def __sub__(self, other): return DWORD(self._value - self._convert(other))
    def __mul__(self, other): return DWORD(self._value * self._convert(other))
    def __floordiv__(self, other): return DWORD(self._value // self._convert(other))
    def __truediv__(self, other): return DWORD(self._value // self._convert(other))
    def __mod__(self, other): return DWORD(self._value % self._convert(other))
    def __divmod__(self, other): return DWORD(divmod(self._value, self._convert(other)))
    def __and__(self, other): return DWORD(self._value & self._convert(other))
    def __or__(self, other): return DWORD(self._value | self._convert(other))
    def __xor__(self, other): return DWORD(self._value ^ self._convert(other))
    def __invert__(self): return DWORD(~self._value)
    def __lshift__(self, other): return DWORD(self._value << self._convert(other))
    def __rshift__(self, other): return DWORD(self._value >> self._convert(other))

    def __radd__(self, other): return DWORD(self._convert(other) + self._value)
    def __rsub__(self, other): return DWORD(self._convert(other) - self._value)
    def __rmul__(self, other): return DWORD(self._convert(other) * self._value)
    def __rfloordiv__(self, other): return DWORD(self._convert(other) // self._value)
    def __rtruediv__(self, other): return DWORD(self._convert(other) // self._value)
    def __rmod__(self, other): return DWORD(self._convert(other) % self._value)
    def __rdivmod__(self, other): return DWORD(divmod(self._convert(other), self._value))
    def __rand__(self, other): return DWORD(self._convert(other) & self._value)
    def __ror__(self, other): return DWORD(self._convert(other) | self._value)
    def __rxor__(self, other): return DWORD(self._convert(other) ^ self._value)
    def __rlshift__(self, other): return DWORD(self._convert(other) << self._value)
    def __rrshift__(self, other): return DWORD(self._convert(other) >> self._value)
    # bool
    def __eq__(self, other): return self._value == self._equation(other)
    def __ge__(self, other): return self._value >= self._equation(other)
    def __gt__(self, other): return self._value > self._equation(other)
    def __le__(self, other): return self._value <= self._equation(other)
    def __lt__(self, other): return self._value < self._equation(other)
    def __bool__(self): return self._value != 0
    # list[idx]
    def __index__(self): return self._value
    # function
    def hex(self): return hex(self._value)
    def value(self): return self._value

    def ror(self, other): return DWORD(ROR(self._value, self._convert(other), SIZE_DWORD))  # Rotate Right
    def rol(self, other): return DWORD(ROL(self._value, self._convert(other), SIZE_DWORD))  # Rotate Left

    def byteN(self, idx): return BYTE(BYTEn(self._value, idx))
    def byte0(self): return self.byteN(0)
    def byte1(self): return self.byteN(1)
    def byte2(self): return self.byteN(2)
    def byte3(self): return self.byteN(3)
    def bytes(self): return [self.byteN(idx) for idx in range(4)]

    def toQWORD(self): return QWORD(self._value)
    def toOWORD(self): return OWORD(self._value)


class QWORD:
    @staticmethod
    def _convert(obj): return obj.value() if isinstance(obj, QWORD) else obj
    @staticmethod
    def _equation(obj): return obj.value() if isinstance(obj, (BYTE, WORD, DWORD, QWORD, OWORD)) else obj
    def __init__(self, v): self._value = v & MAX_QWORD
    def __int__(self): return self._value
    def __str__(self): return Config.print(self._value)
    def __repr__(self): return f'QWORD({self.__str__()})'
    def __add__(self, other): return QWORD(self._value + self._convert(other))
    def __sub__(self, other): return QWORD(self._value - self._convert(other))
    def __mul__(self, other): return QWORD(self._value * self._convert(other))
    def __floordiv__(self, other): return QWORD(self._value // self._convert(other))
    def __truediv__(self, other): return QWORD(self._value // self._convert(other))
    def __mod__(self, other): return QWORD(self._value % self._convert(other))
    def __divmod__(self, other): return QWORD(divmod(self._value, self._convert(other)))
    def __and__(self, other): return QWORD(self._value & self._convert(other))
    def __or__(self, other): return QWORD(self._value | self._convert(other))
    def __xor__(self, other): return QWORD(self._value ^ self._convert(other))
    def __invert__(self): return QWORD(~self._value)
    def __lshift__(self, other): return QWORD(self._value << self._convert(other))
    def __rshift__(self, other): return QWORD(self._value >> self._convert(other))

    def __radd__(self, other): return QWORD(self._convert(other) + self._value)
    def __rsub__(self, other): return QWORD(self._convert(other) - self._value)
    def __rmul__(self, other): return QWORD(self._convert(other) * self._value)
    def __rfloordiv__(self, other): return QWORD(self._convert(other) // self._value)
    def __rtruediv__(self, other): return QWORD(self._convert(other) // self._value)
    def __rmod__(self, other): return QWORD(self._convert(other) % self._value)
    def __rdivmod__(self, other): return QWORD(divmod(self._convert(other), self._value))
    def __rand__(self, other): return QWORD(self._convert(other) & self._value)
    def __ror__(self, other): return QWORD(self._convert(other) | self._value)
    def __rxor__(self, other): return QWORD(self._convert(other) ^ self._value)
    def __rlshift__(self, other): return QWORD(self._convert(other) << self._value)
    def __rrshift__(self, other): return QWORD(self._convert(other) >> self._value)
    # bool
    def __eq__(self, other): return self._value == self._equation(other)
    def __ge__(self, other): return self._value >= self._equation(other)
    def __gt__(self, other): return self._value > self._equation(other)
    def __le__(self, other): return self._value <= self._equation(other)
    def __lt__(self, other): return self._value < self._equation(other)
    def __bool__(self): return self._value != 0
    # list[idx]
    def __index__(self): return self._value
    # function
    def hex(self): return hex(self._value)
    def value(self): return self._value

    def ror(self, other): return QWORD(ROR(self._value, self._convert(other), SIZE_QWORD))  # Rotate Right
    def rol(self, other): return QWORD(ROL(self._value, self._convert(other), SIZE_QWORD))  # Rotate Left

    def byteN(self, idx): return BYTE(BYTEn(self._value, idx))
    def byte0(self): return self.byteN(0)
    def byte1(self): return self.byteN(1)
    def byte2(self): return self.byteN(2)
    def byte3(self): return self.byteN(3)
    def bytes(self): return [self.byteN(idx) for idx in range(8)]

    def toOWORD(self): return OWORD(self._value)


class OWORD:
    @staticmethod
    def _convert(obj): return obj.value() if isinstance(obj, OWORD) else obj
    @staticmethod
    def _equation(obj): return obj.value() if isinstance(obj, (BYTE, WORD, DWORD, QWORD, OWORD)) else obj
    def __init__(self, v): self._value = v & MAX_OWORD
    def __int__(self): return self._value
    def __str__(self): return Config.print(self._value)
    def __repr__(self): return f'OWORD({self.__str__()})'
    def __add__(self, other): return OWORD(self._value + self._convert(other))
    def __sub__(self, other): return OWORD(self._value - self._convert(other))
    def __mul__(self, other): return OWORD(self._value * self._convert(other))
    def __floordiv__(self, other): return OWORD(self._value // self._convert(other))
    def __truediv__(self, other): return OWORD(self._value // self._convert(other))
    def __mod__(self, other): return OWORD(self._value % self._convert(other))
    def __divmod__(self, other): return OWORD(divmod(self._value, self._convert(other)))
    def __and__(self, other): return OWORD(self._value & self._convert(other))
    def __or__(self, other): return OWORD(self._value | self._convert(other))
    def __xor__(self, other): return OWORD(self._value ^ self._convert(other))
    def __invert__(self): return OWORD(~self._value)
    def __lshift__(self, other): return OWORD(self._value << self._convert(other))
    def __rshift__(self, other): return OWORD(self._value >> self._convert(other))

    def __radd__(self, other): return OWORD(self._convert(other) + self._value)
    def __rsub__(self, other): return OWORD(self._convert(other) - self._value)
    def __rmul__(self, other): return OWORD(self._convert(other) * self._value)
    def __rfloordiv__(self, other): return OWORD(self._convert(other) // self._value)
    def __rtruediv__(self, other): return OWORD(self._convert(other) // self._value)
    def __rmod__(self, other): return OWORD(self._convert(other) % self._value)
    def __rdivmod__(self, other): return OWORD(divmod(self._convert(other), self._value))
    def __rand__(self, other): return OWORD(self._convert(other) & self._value)
    def __ror__(self, other): return OWORD(self._convert(other) | self._value)
    def __rxor__(self, other): return OWORD(self._convert(other) ^ self._value)
    def __rlshift__(self, other): return OWORD(self._convert(other) << self._value)
    def __rrshift__(self, other): return OWORD(self._convert(other) >> self._value)
    # bool
    def __eq__(self, other): return self._value == self._equation(other)
    def __ge__(self, other): return self._value >= self._equation(other)
    def __gt__(self, other): return self._value > self._equation(other)
    def __le__(self, other): return self._value <= self._equation(other)
    def __lt__(self, other): return self._value < self._equation(other)
    def __bool__(self): return self._value != 0
    # list[idx]
    def __index__(self): return self._value

    # function
    def hex(self): return hex(self._value)
    def value(self): return self._value

    def ror(self, other): return OWORD(ROR(self._value, self._convert(other), SIZE_OWORD))  # Rotate Right
    def rol(self, other): return OWORD(ROL(self._value, self._convert(other), SIZE_OWORD))  # Rotate Left

    def byteN(self, idx): return BYTE(BYTEn(self._value, idx))
    def byte0(self): return self.byteN(0)
    def byte1(self): return self.byteN(1)
    def byte2(self): return self.byteN(2)
    def byte3(self): return self.byteN(3)
    def bytes(self): return [self.byteN(idx) for idx in range(16)]


class WrapList(list):
    def __init__(self, convert: callable, v: List):
        super().__init__()
        self.extend([convert(i) for i in v])


class BYTEList(WrapList):
    def __init__(self, v: List): super().__init__(BYTE, v)

    def toByteArray(self): return bytearray([i.value() for i in self])
    def toWORDList(self): return WORDList(BYTEs2WORDs(self))
    def toDWORDList(self): return DWORDList(BYTEs2DWORDs(self))
    def toQWORDList(self): return QWORDList(BYTEs2QWORDs(self))
    def toOWORDList(self): return OWORDList(BYTEs2OWORDs(self))


class WORDList(WrapList):
    def __init__(self, v): super().__init__(WORD, v)
    def toBYTEList(self): return BYTEList(WORDs2BYTEs(self))
    def toDWORDList(self): return DWORDList(WORDs2DWORDs(self))
    def toQWORDList(self): return QWORDList(WORDs2QWORDs(self))
    def toOWORDList(self): return OWORDList(WORDs2OWORDs(self))


class DWORDList(WrapList):
    def __init__(self, v): super().__init__(DWORD, v)

    def toBYTEList(self): return BYTEList(DWORDs2BYTEs(self))
    def toWORDList(self): return WORDList(DWORDs2WORDs(self))
    def toQWORDList(self): return QWORDList(DWORDs2QWORDs(self))
    def toOWORDList(self): return OWORDList(DWORDs2OWORDs(self))


class QWORDList(WrapList):
    def __init__(self, v): super().__init__(QWORD, v)

    def toBYTEList(self): return BYTEList(QWORDs2BYTEs(self))
    def toWORDList(self): return WORDList(QWORDs2WORDs(self))
    def toDWORDList(self): return DWORDList(QWORDs2DWORDs(self))
    def toOWORDList(self): return OWORDList(QWORDs2OWORDs(self))


class OWORDList(WrapList):
    def __init__(self, v): super().__init__(OWORD, v)

    def toBYTEList(self): return BYTEList(OWORDs2BYTEs(self))
    def toWORDList(self): return WORDList(OWORDs2WORDs(self))
    def toDWORDList(self): return WORDList(OWORDs2DWORDs(self))
    def toQWORDList(self): return QWORDList(OWORDs2QWORDs(self))


if __name__ == '__main__':
    from icecream import ic as prpr
    prpr.prefix = "open your heart ❤ fall in love -> "
    ch1 = DWORD(0x45)
    ch2 = BYTE(0x76)
    ch3 = DWORD(0x76)
    prpr(WORD(BYTEs2WORD([0x45, 0x76])))
    Config.print_type('hex')
    prpr(QWORD(WORDs2DWORD([0x7645, 0x1341])).hex())
    prpr(QWORD(WORDs2QWORD([0x7645, 0x1341, 0x7645, 0x1341])).hex())
    prpr(WORDs2DWORDs([0x7645, 0x1341, 0x7645, 0x1341]))
    prpr([1, 2, 3, 4][DWORD(0x1)])
    prpr(123 / BYTE(0x23), DWORD(344) / 0x23, DWORD(344) * QWORD(0x23))
    prpr(QWORD(0x222434343))
    prpr(DWORD(QWORD(0x134444) + 100000))

    prpr(BYTE(0x23) + DWORD(344))

    prpr(WORDs2BYTEs(WORDList([0x29, 0x1134])))
    prpr(WrapList(BYTE, [0x10, 0x23]))
    prpr(DWORDList([0x121012, 0x23, 0x7645, 0x1341, 0x7645, 0x24]).toQWORDList())




