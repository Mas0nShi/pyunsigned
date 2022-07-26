# -*- coding:utf-8 -*-
"""
@Author: Mas0n
@File: convert.py
@Time: 2022/6/28 22:44
@Desc: It's all about getting better.
"""
import struct
from typing import List, ClassVar


class Config:
    print_hex = False


SIZE_BYTE  = 8
SIZE_WORD  = SIZE_BYTE * 2
SIZE_DWORD = SIZE_BYTE * 4
SIZE_QWORD = SIZE_BYTE * 8
SIZE_OWORD = SIZE_BYTE * 16

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


def As2n(lst, length: int, size: int):
    assert len(lst) == length
    tv = 0
    for i, v in enumerate(lst):
        tv |= (v << (size * i))
    return tv


def As2ns(handler: callable, lst: List, step: int) -> List: return [handler(lst[i:i+step]) for i in range(0, len(lst), step)]


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


def BYTEs2WORDs(v: List) -> List:   return As2ns(handler=BYTEs2WORD,   lst=v, step=2)
def BYTEs2DWORDs(v: List) -> List:  return As2ns(handler=BYTEs2DWORD,  lst=v, step=4)
def BYTEs2QWORDs(v: List) -> List:  return As2ns(handler=BYTEs2QWORD,  lst=v, step=8)
def BYTEs2OWORDs(v: List) -> List:  return As2ns(handler=BYTEs2OWORD,  lst=v, step=16)
def WORDs2DWORDs(v: List) -> List:  return As2ns(handler=WORDs2DWORD,  lst=v, step=2)
def WORDs2QWORDs(v: List) -> List:  return As2ns(handler=WORDs2QWORD,  lst=v, step=4)
def WORDs2OWORDs(v: List) -> List:  return As2ns(handler=WORDs2OWORD,  lst=v, step=8)
def DWORDs2QWORDs(v: List) -> List: return As2ns(handler=DWORDs2QWORD, lst=v, step=2)
def DWORDs2OWORDs(v: List) -> List: return As2ns(handler=DWORDs2OWORD, lst=v, step=4)
def QWORDs2OWORDs(v: List) -> List: return As2ns(handler=QWORDs2OWORD, lst=v, step=2)


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



class BYTE:
    _size = SIZE_BYTE
    @staticmethod
    def _convert(obj): return obj._value if isinstance(obj, BYTE) else obj
    @staticmethod
    def _equation(obj): return obj._value if isinstance(obj, (BYTE, WORD, DWORD, QWORD, OWORD)) else obj

    def _type_convert(self, other): return self.__class__ if self._size > other._size else other.__class__

    def __init__(self, v): self._value = v & MAX_BYTE
    def __int__(self): return self._value
    def __str__(self): return self.hex() if Config.print_hex else str(self._value)
    def __repr__(self): return f'BYTE({self.__str__()})'
    def __add__(self, other): return self._type_convert(other)(self._value + self._convert(other))
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
    def __rlshift__(self, other): return BYTE(self._convert(other) << self._value)
    def __rrshift__(self, other): return BYTE(self._convert(other) >> self._value)
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
    def __init__(self, v): self.v = v & MAX_WORD
    def __int__(self): return self.v
    def __str__(self): return self.hex() if Config.print_hex else str(self.v)
    def __repr__(self): return f'WORD({self.__str__()})'
    def __add__(self, other): return WORD(self.v + self._convert(other))
    def __sub__(self, other): return WORD(self.v - self._convert(other))
    def __mul__(self, other): return WORD(self.v * self._convert(other))
    def __floordiv__(self, other): return WORD(self.v // self._convert(other))
    def __truediv__(self, other): return WORD(self.v // self._convert(other))
    def __mod__(self, other): return WORD(self.v % self._convert(other))
    def __divmod__(self, other): return WORD(divmod(self.v, self._convert(other)))
    def __and__(self, other): return WORD(self.v & self._convert(other))
    def __or__(self, other): return WORD(self.v | self._convert(other))
    def __xor__(self, other): return WORD(self.v ^ self._convert(other))
    def __invert__(self): return WORD(~self.v)
    def __lshift__(self, other): return WORD(self.v << self._convert(other))
    def __rshift__(self, other): return WORD(self.v >> self._convert(other))

    def __radd__(self, other): return WORD(self._convert(other) + self.v)
    def __rsub__(self, other): return WORD(self._convert(other) - self.v)
    def __rmul__(self, other): return WORD(self._convert(other) * self.v)
    def __rfloordiv__(self, other): return WORD(self._convert(other) // self.v)
    def __rtruediv__(self, other): return WORD(self._convert(other) // self.v)
    def __rmod__(self, other): return WORD(self._convert(other) % self.v)
    def __rdivmod__(self, other): return WORD(divmod(self._convert(other), self.v))
    def __rand__(self, other): return WORD(self._convert(other) & self.v)
    def __ror__(self, other): return WORD(self._convert(other) | self.v)
    def __rxor__(self, other): return WORD(self._convert(other) ^ self.v)
    def __rlshift__(self, other): return WORD(self._convert(other) << self.v)
    def __rrshift__(self, other): return WORD(self._convert(other) >> self.v)
    # bool
    def __eq__(self, other): return self.v == self._equation(other)
    def __ge__(self, other): return self.v >= self._equation(other)
    def __gt__(self, other): return self.v > self._equation(other)
    def __le__(self, other): return self.v <= self._equation(other)
    def __lt__(self, other): return self.v < self._equation(other)
    def __bool__(self): return self.v != 0
    # list[idx]
    def __index__(self): return self.v
    # function
    def hex(self): return hex(self.v)
    def value(self): return self.v

    def ror(self, other): return WORD(ROR(self.v, self._convert(other), SIZE_WORD))  # Rotate Right
    def rol(self, other): return WORD(ROL(self.v, self._convert(other), SIZE_WORD))  # Rotate Left

    def byteN(self, idx): return BYTE(BYTEn(self.v, idx))
    def byte0(self): return self.byteN(0)
    def byte1(self): return self.byteN(1)

    def toDWORD(self): return DWORD(self.v)
    def toQWORD(self): return QWORD(self.v)
    def toOWORD(self): return OWORD(self.v)


class DWORD:
    _size = SIZE_DWORD
    @staticmethod
    def _convert(obj): return obj.value() if isinstance(obj, DWORD) else obj
    @staticmethod
    def _equation(obj): return obj.value() if isinstance(obj, (BYTE, WORD, DWORD, QWORD, OWORD)) else obj
    def __init__(self, v): self.v = v & MAX_DWORD
    def __int__(self): return self.v
    def __str__(self): return self.hex() if Config.print_hex else str(self.v)
    def __repr__(self): return f'DWORD({self.__str__()})'
    def __add__(self, other): return DWORD(self.v + self._convert(other))
    def __sub__(self, other): return DWORD(self.v - self._convert(other))
    def __mul__(self, other): return DWORD(self.v * self._convert(other))
    def __floordiv__(self, other): return DWORD(self.v // self._convert(other))
    def __truediv__(self, other): return DWORD(self.v // self._convert(other))
    def __mod__(self, other): return DWORD(self.v % self._convert(other))
    def __divmod__(self, other): return DWORD(divmod(self.v, self._convert(other)))
    def __and__(self, other): return DWORD(self.v & self._convert(other))
    def __or__(self, other): return DWORD(self.v | self._convert(other))
    def __xor__(self, other): return DWORD(self.v ^ self._convert(other))
    def __invert__(self): return DWORD(~self.v)
    def __lshift__(self, other): return DWORD(self.v << self._convert(other))
    def __rshift__(self, other): return DWORD(self.v >> self._convert(other))

    def __radd__(self, other): return DWORD(self._convert(other) + self.v)
    def __rsub__(self, other): return DWORD(self._convert(other) - self.v)
    def __rmul__(self, other): return DWORD(self._convert(other) * self.v)
    def __rfloordiv__(self, other): return DWORD(self._convert(other) // self.v)
    def __rtruediv__(self, other): return DWORD(self._convert(other) // self.v)
    def __rmod__(self, other): return DWORD(self._convert(other) % self.v)
    def __rdivmod__(self, other): return DWORD(divmod(self._convert(other), self.v))
    def __rand__(self, other): return DWORD(self._convert(other) & self.v)
    def __ror__(self, other): return DWORD(self._convert(other) | self.v)
    def __rxor__(self, other): return DWORD(self._convert(other) ^ self.v)
    def __rlshift__(self, other): return DWORD(self._convert(other) << self.v)
    def __rrshift__(self, other): return DWORD(self._convert(other) >> self.v)
    # bool
    def __eq__(self, other): return self.v == self._equation(other)
    def __ge__(self, other): return self.v >= self._equation(other)
    def __gt__(self, other): return self.v > self._equation(other)
    def __le__(self, other): return self.v <= self._equation(other)
    def __lt__(self, other): return self.v < self._equation(other)
    def __bool__(self): return self.v != 0
    # list[idx]
    def __index__(self): return self.v
    # function
    def hex(self): return hex(self.v)
    def value(self): return self.v

    def ror(self, other): return DWORD(ROR(self.v, self._convert(other), SIZE_DWORD))  # Rotate Right
    def rol(self, other): return DWORD(ROL(self.v, self._convert(other), SIZE_DWORD))  # Rotate Left

    def byteN(self, idx): return BYTE(BYTEn(self.v, idx))
    def byte0(self): return self.byteN(0)
    def byte1(self): return self.byteN(1)
    def byte2(self): return self.byteN(2)
    def byte3(self): return self.byteN(3)

    def toQWORD(self): return QWORD(self.v)
    def toOWORD(self): return OWORD(self.v)


class QWORD:
    @staticmethod
    def _convert(obj): return obj.value() if isinstance(obj, QWORD) else obj
    @staticmethod
    def _equation(obj): return obj.value() if isinstance(obj, (BYTE, WORD, DWORD, QWORD, OWORD)) else obj
    def __init__(self, v): self.v = v & MAX_QWORD
    def __int__(self): return self.v
    def __str__(self): return self.hex() if Config.print_hex else str(self.v)
    def __repr__(self): return f'QWORD({self.__str__()})'
    def __add__(self, other): return QWORD(self.v + self._convert(other))
    def __sub__(self, other): return QWORD(self.v - self._convert(other))
    def __mul__(self, other): return QWORD(self.v * self._convert(other))
    def __floordiv__(self, other): return QWORD(self.v // self._convert(other))
    def __truediv__(self, other): return QWORD(self.v // self._convert(other))
    def __mod__(self, other): return QWORD(self.v % self._convert(other))
    def __divmod__(self, other): return QWORD(divmod(self.v, self._convert(other)))
    def __and__(self, other): return QWORD(self.v & self._convert(other))
    def __or__(self, other): return QWORD(self.v | self._convert(other))
    def __xor__(self, other): return QWORD(self.v ^ self._convert(other))
    def __invert__(self): return QWORD(~self.v)
    def __lshift__(self, other): return QWORD(self.v << self._convert(other))
    def __rshift__(self, other): return QWORD(self.v >> self._convert(other))

    def __radd__(self, other): return QWORD(self._convert(other) + self.v)
    def __rsub__(self, other): return QWORD(self._convert(other) - self.v)
    def __rmul__(self, other): return QWORD(self._convert(other) * self.v)
    def __rfloordiv__(self, other): return QWORD(self._convert(other) // self.v)
    def __rtruediv__(self, other): return QWORD(self._convert(other) // self.v)
    def __rmod__(self, other): return QWORD(self._convert(other) % self.v)
    def __rdivmod__(self, other): return QWORD(divmod(self._convert(other), self.v))
    def __rand__(self, other): return QWORD(self._convert(other) & self.v)
    def __ror__(self, other): return QWORD(self._convert(other) | self.v)
    def __rxor__(self, other): return QWORD(self._convert(other) ^ self.v)
    def __rlshift__(self, other): return QWORD(self._convert(other) << self.v)
    def __rrshift__(self, other): return QWORD(self._convert(other) >> self.v)
    # bool
    def __eq__(self, other): return self.v == self._equation(other)
    def __ge__(self, other): return self.v >= self._equation(other)
    def __gt__(self, other): return self.v > self._equation(other)
    def __le__(self, other): return self.v <= self._equation(other)
    def __lt__(self, other): return self.v < self._equation(other)
    def __bool__(self): return self.v != 0
    # list[idx]
    def __index__(self): return self.v
    # function
    def hex(self): return hex(self.v)
    def value(self): return self.v

    def ror(self, other): return QWORD(ROR(self.v, self._convert(other), SIZE_QWORD))  # Rotate Right
    def rol(self, other): return QWORD(ROL(self.v, self._convert(other), SIZE_QWORD))  # Rotate Left

    def byteN(self, idx): return BYTE(BYTEn(self.v, idx))
    def byte0(self): return self.byteN(0)
    def byte1(self): return self.byteN(1)
    def byte2(self): return self.byteN(2)
    def byte3(self): return self.byteN(3)

    def toOWORD(self): return OWORD(self.v)


class OWORD:
    @staticmethod
    def _convert(obj): return obj.value() if isinstance(obj, OWORD) else obj
    @staticmethod
    def _equation(obj): return obj.value() if isinstance(obj, (BYTE, WORD, DWORD, QWORD, OWORD)) else obj
    def __init__(self, v): self.v = v & MAX_OWORD
    def __int__(self): return self.v
    def __str__(self): return self.hex() if Config.print_hex else str(self.v)
    def __repr__(self): return f'OWORD({self.__str__()})'
    def __add__(self, other): return OWORD(self.v + self._convert(other))
    def __sub__(self, other): return OWORD(self.v - self._convert(other))
    def __mul__(self, other): return OWORD(self.v * self._convert(other))
    def __floordiv__(self, other): return OWORD(self.v // self._convert(other))
    def __truediv__(self, other): return OWORD(self.v // self._convert(other))
    def __mod__(self, other): return OWORD(self.v % self._convert(other))
    def __divmod__(self, other): return OWORD(divmod(self.v, self._convert(other)))
    def __and__(self, other): return OWORD(self.v & self._convert(other))
    def __or__(self, other): return OWORD(self.v | self._convert(other))
    def __xor__(self, other): return OWORD(self.v ^ self._convert(other))
    def __invert__(self): return OWORD(~self.v)
    def __lshift__(self, other): return OWORD(self.v << self._convert(other))
    def __rshift__(self, other): return OWORD(self.v >> self._convert(other))

    def __radd__(self, other): return OWORD(self._convert(other) + self.v)
    def __rsub__(self, other): return OWORD(self._convert(other) - self.v)
    def __rmul__(self, other): return OWORD(self._convert(other) * self.v)
    def __rfloordiv__(self, other): return OWORD(self._convert(other) // self.v)
    def __rtruediv__(self, other): return OWORD(self._convert(other) // self.v)
    def __rmod__(self, other): return OWORD(self._convert(other) % self.v)
    def __rdivmod__(self, other): return OWORD(divmod(self._convert(other), self.v))
    def __rand__(self, other): return OWORD(self._convert(other) & self.v)
    def __ror__(self, other): return OWORD(self._convert(other) | self.v)
    def __rxor__(self, other): return OWORD(self._convert(other) ^ self.v)
    def __rlshift__(self, other): return OWORD(self._convert(other) << self.v)
    def __rrshift__(self, other): return OWORD(self._convert(other) >> self.v)
    # bool
    def __eq__(self, other): return self.v == self._equation(other)
    def __ge__(self, other): return self.v >= self._equation(other)
    def __gt__(self, other): return self.v > self._equation(other)
    def __le__(self, other): return self.v <= self._equation(other)
    def __lt__(self, other): return self.v < self._equation(other)
    def __bool__(self): return self.v != 0
    # list[idx]
    def __index__(self): return self.v


    # function
    def hex(self): return hex(self.v)
    def value(self): return self.v

    def ror(self, other): return OWORD(ROR(self.v, self._convert(other), SIZE_OWORD))  # Rotate Right
    def rol(self, other): return OWORD(ROL(self.v, self._convert(other), SIZE_OWORD))  # Rotate Left

    def byteN(self, idx): return BYTE(BYTEn(self.v, idx))
    def byte0(self): return self.byteN(0)
    def byte1(self): return self.byteN(1)
    def byte2(self): return self.byteN(2)
    def byte3(self): return self.byteN(3)


if __name__ == '__main__':
    from icecream import ic as prpr
    prpr.prefix = "open your heart ❤ fall in love -> "
    ch1 = DWORD(0x45)
    ch2 = BYTE(0x76)
    ch3 = DWORD(0x76)
    prpr(WORD(BYTEs2WORD([0x45, 0x76])))
    Config.print_hex = True
    prpr(QWORD(WORDs2DWORD([0x7645, 0x1341])).hex())
    prpr(QWORD(WORDs2QWORD([0x7645, 0x1341, 0x7645, 0x1341])).hex())
    prpr(WORDs2DWORDs([0x7645, 0x1341, 0x7645, 0x1341]))
    prpr([1, 2, 3, 4][DWORD(0x1)])
    prpr(123 / BYTE(0x23), DWORD(344) / 0x23, DWORD(344) * QWORD(0x23))
    prpr(QWORD(0x222434343))
    prpr(DWORD(QWORD(0x134444) + 100000))

    prpr(BYTE(0x23) + DWORD(344))





