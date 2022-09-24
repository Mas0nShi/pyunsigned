# -*- coding:utf-8 -*-
"""
@Author: Mas0n
@File: convert.py
@Time: 2022/6/28 22:44
@Desc: It's all about getting better.
"""
from typing import List, NamedTuple
from functools import reduce, partial
import operator
import logging


def getLogger():
    from loguru import logger
    import sys

    logger.remove()
    logger.add(sink=sys.stdout, format="<level>[{level.icon}] {message}</level>", colorize=True)

    logger.level("SUCCESS", icon="+", color="<g>")
    logger.level("DEBUG", icon="*", color="<blue>")
    logger.level("ERROR", icon="-", color="<red>")
    logger.level("WARNING", icon="!", color="<yellow>")

    return logger


log = getLogger()


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


class BaseIntType(NamedTuple):
    size: int
    max: int


class IntTypeInfo:
    BYTE = BaseIntType(1, 0xff)
    WORD = BaseIntType(2, 0xffff)
    DWORD = BaseIntType(4, 0xffffffff)
    QWORD = BaseIntType(8, 0xffffffffffffffff)
    OWORD = BaseIntType(16, 0xffffffffffffffffffffffffffffffff)


class _Conversions:
    @staticmethod
    def BYTEn(v, n): return (v >> (n * IntTypeInfo.BYTE.size * 8)) & IntTypeInfo.BYTE.max
    @staticmethod
    def WORDn(v, n): return (v >> (n * IntTypeInfo.WORD.size * 8)) & IntTypeInfo.WORD.max
    @staticmethod
    def DWORDn(v, n): return (v >> (n * IntTypeInfo.DWORD.size * 8)) & IntTypeInfo.DWORD.max
    @staticmethod
    def QWORDn(v, n): return (v >> (n * IntTypeInfo.QWORD.size * 8)) & IntTypeInfo.QWORD.max
    @staticmethod
    def OWORDn(v, n): return (v >> (n * IntTypeInfo.QWORD.size * 8)) & IntTypeInfo.QWORD.max

    def __init__(self):
        pass # TODO: not impl.


Conversions = _Conversions()


def As2n(lst: List, length: int) -> int:
    # assert len(lst) == length
    if len(lst) != length:
        log.warning(f"length vaild, try auto padding: {lst}")
        # lst += [0] * (length - len(lst))
    tv = 0
    for i, v in enumerate(lst):
        tv |= (int(v) << (length * 8 * i))
    return tv


def As2ns(handler: callable, lst: List, step: int) -> List:
    return [handler(lst[i:i + step]) for i in range(0, len(lst), step)]


def n2As(handler: callable, lst: int, length: int) -> list:
    return [handler(lst, i) for i in range(length)]


def ns2As(handler: callable, lst: List) -> List:
    return reduce(lambda x, y: x + y, [handler(i) for i in lst])


# array to value.
def BYTEs2WORD(v: List): return As2n(v, length=2)
def BYTEs2DWORD(v: List): return As2n(v, length=4)
def BYTEs2QWORD(v: List): return As2n(v, length=8)
def BYTEs2OWORD(v: List): return As2n(v, length=16)

def WORDs2DWORD(v: List):  return As2n(v, length=2)
def WORDs2QWORD(v: List):  return As2n(v, length=4)
def WORDs2OWORD(v: List):  return As2n(v, length=8)
def DWORDs2QWORD(v: List): return As2n(v, length=2)
def DWORDs2OWORD(v: List): return As2n(v, length=4)
def QWORDs2OWORD(v: List): return As2n(v, length=2)
# value to array.
def WORD2BYTEs(v: int): return n2As(handler=getattr(Conversions, "BYTEn"), lst=v, length=2)
def DWORD2BYTEs(v: int): return n2As(handler=getattr(Conversions, "BYTEn"), lst=v, length=4)
def QWORD2BYTEs(v: int): return n2As(handler=getattr(Conversions, "BYTEn"), lst=v, length=8)
def OWORD2BYTEs(v: int): return n2As(handler=getattr(Conversions, "BYTEn"), lst=v, length=16)
def DWORD2WORDs(v: int): return n2As(handler=getattr(Conversions, "WORDn"), lst=v, length=2)
def QWORD2WORDs(v: int): return n2As(handler=getattr(Conversions, "WORDn"), lst=v, length=4)
def OWORD2WORDs(v: int): return n2As(handler=getattr(Conversions, "WORDn"), lst=v, length=8)
def QWORD2DWORDs(v: int): return n2As(handler=getattr(Conversions, "DWORDn"), lst=v, length=2)
def OWORD2DWORDs(v: int): return n2As(handler=getattr(Conversions, "DWORDn"), lst=v, length=4)
def OWORD2QWORDs(v: int): return n2As(handler=getattr(Conversions, "QWORDn"), lst=v, length=2)

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


def _typeCast(self, other):
    assert issubclass(self.__class__, BaseInt)
    wrap = None
    if isinstance(other, int):
        wrap = self.__class__
    elif issubclass(other.__class__, BaseInt):
        if getattr(self.type, 'size') > getattr(other.type, 'size'):
            wrap = self.__class__
        else:
            wrap = other.__class__
    else:
        raise TypeError('only support int or BaseIntType.')

    return wrap(other)


def _baseBinaryOperation(base, other, binaryOp: callable, r: bool = False):
    cast_other = _typeCast(base, other)
    # TODO: e.g. radd and add.
    if r:
        result = binaryOp(cast_other.int, base.int)
    else:
        result = binaryOp(base.int, cast_other.int)
    # TODO: divmod
    if isinstance(result, tuple):
        return (_typeCast(base, i) for i in result)
    else:
        return _typeCast(base, result)


_binaryOperation = partial(_baseBinaryOperation, r=False)
_rbinaryOperation = partial(_baseBinaryOperation, r=True)


def _unaryOperation(self, unaryOp: callable):
    assert issubclass(self.__class__, BaseInt)
    return self.__class__(unaryOp(self.int))


class BaseInt:
    def __init__(self, v):
        self.type = getattr(IntTypeInfo, self.__class__.__name__)
        self.int = int(v) & getattr(self.type, 'max')

    def __int__(self): return self.int
    def __str__(self): return Config.print(self.int)
    def __repr__(self): return f'{self.__class__.__name__}({self.__str__()})'

    def __add__(self, other): return _binaryOperation(self, other, operator.add)
    def __sub__(self, other): return _binaryOperation(self, other, operator.sub)

    def __mul__(self, other): return _binaryOperation(self, other, operator.mul)
    def __floordiv__(self, other): return _binaryOperation(self, other, operator.floordiv)
    def __truediv__(self, other): return _binaryOperation(self, other, operator.floordiv)
    def __mod__(self, other): return _binaryOperation(self, other, operator.mod)
    def __divmod__(self, other): return _binaryOperation(self, other, divmod)
    def __and__(self, other):  return _binaryOperation(self, other, operator.and_)
    def __or__(self, other): return _binaryOperation(self, other, operator.or_)
    def __xor__(self, other): return _binaryOperation(self, other, operator.xor)

    def __invert__(self): return _unaryOperation(self, operator.invert)
    def __lshift__(self, other): return _binaryOperation(self, other, operator.lshift)
    def __rshift__(self, other): return _binaryOperation(self, other, operator.rshift)

    def __radd__(self, other): return _rbinaryOperation(self, other, operator.add)
    def __rsub__(self, other): return _rbinaryOperation(self, other, operator.sub)
    def __rmul__(self, other): return _rbinaryOperation(self, other, operator.mul)
    def __rfloordiv__(self, other): return _rbinaryOperation(self, other, operator.floordiv)
    def __rtruediv__(self, other): return _rbinaryOperation(self, other, operator.floordiv)
    def __rmod__(self, other): return _rbinaryOperation(self, other, operator.mod)
    def __rdivmod__(self, other): return _rbinaryOperation(self, other, divmod)
    def __rand__(self, other): return _rbinaryOperation(self, other, operator.and_)
    def __ror__(self, other): return _rbinaryOperation(self, other, operator.or_)
    def __rxor__(self, other): return _rbinaryOperation(self, other, operator.xor)
    def __rlshift__(self, other): return _rbinaryOperation(self, other, operator.lshift)
    def __rrshift__(self, other): return _rbinaryOperation(self, other, operator.rshift)
    # bool
    def __eq__(self, other): return _binaryOperation(self, other, operator.eq)
    def __ge__(self, other): return _binaryOperation(self, other, operator.ge)
    def __gt__(self, other): return _binaryOperation(self, other, operator.gt)
    def __le__(self, other): return _binaryOperation(self, other, operator.le)
    def __lt__(self, other): return _binaryOperation(self, other, operator.lt)
    def __ne__(self, other): return _binaryOperation(self, other, operator.ne)
    # index [1, 2, 3, 4][Type[BaseInt]]
    def __index__(self): return self.int
    # function
    def __hex__(self): return hex(self.int)
    def byteN(self): pass  # TODO: not impl.
    def hex(self): return self.__hex__()

    def bit_ror(self, other):
        portion = partial(ROR, size=getattr(self.type, 'size') * 8)
        return _binaryOperation(self, other, portion)

    def bit_rol(self, other):
        portion = partial(ROL, size=getattr(self.type, 'size') * 8)
        return _binaryOperation(self, other, portion)


class BYTE(BaseInt):
    def __init__(self, v): super(self.__class__, self).__init__(v)


class WORD(BaseInt):
    def __init__(self, v): super(self.__class__, self).__init__(v)


class DWORD(BaseInt):
    def __init__(self, v): super(self.__class__, self).__init__(v)


class QWORD(BaseInt):
    def __init__(self, v): super(self.__class__, self).__init__(v)


class OWORD(BaseInt):
    def __init__(self, v): super(self.__class__, self).__init__(v)


class BaseIntList(list):
    def __init__(self, v: List, impl):
        super().__init__()
        self.extend([impl(i) for i in v])


class BYTEList(BaseIntList):
    def __init__(self, v): super(BYTEList, self).__init__(v, BYTE)




class WORDList(BaseIntList):
    def __init__(self, v): super(WORDList, self).__init__(v, WORD)


class DWORDList(BaseIntList):
    def __init__(self, v): super(DWORDList, self).__init__(v, DWORD)


class QWORDList(BaseIntList):
    def __init__(self, v): super(QWORDList, self).__init__(v, QWORD)


class OWORDList(BaseIntList):
    def __init__(self, v): super(OWORDList, self).__init__(v, OWORD)


def test_unit(impl):
    import random
    log = getLogger()

    assert issubclass(impl, BaseInt)
    types = getattr(IntTypeInfo, impl.__name__)
    t_size= getattr(types, 'size')
    t_value = getattr(types, 'max')
    log.debug(f'impl type: {impl.__name__}, {types}')
    a = random.randint(1, t_value)
    b = random.randint(1, t_value)
    shiftBits = random.randint(1, 16)
    log.debug(f'generate number: a={hex(a)}, b={hex(b)}, shiftBits={hex(shiftBits)}')
    wrapA = impl(a)
    wrapB = impl(b)
    wrapShiftBits = impl(shiftBits)
    log.debug(f'wrap number: wrapA={wrapA}, wrapB={wrapB}, wrapShiftBits={wrapShiftBits}')

    assert wrapA + wrapB == (a + b) & t_value
    assert wrapA - wrapB == (a - b) & t_value
    assert wrapA * wrapB == (a * b) & t_value
    assert wrapA / wrapB == (a // b) & t_value
    assert wrapA // wrapB == (a // b) & t_value
    assert wrapA % wrapB == (a % b) & t_value
    assert list(divmod(wrapA, wrapB)) == list(i & t_value for i in divmod(a, b))
    assert wrapA & wrapB == (a & b) & t_value
    assert wrapA | wrapB == (a | b) & t_value
    assert (~wrapA) & t_value == (~a) & t_value and (~wrapB) & t_value == (~b) & t_value
    assert wrapA << wrapShiftBits == (a << wrapShiftBits) & t_value
    assert wrapA >> wrapShiftBits == (a >> wrapShiftBits) & t_value
    # r
    assert wrapB + wrapA  == (b + a) & t_value
    assert wrapB - wrapA == (b - a) & t_value
    assert wrapB * wrapA == (b * a) & t_value
    assert wrapB / wrapA == (b // a) & t_value
    assert wrapB // wrapA == (b // a) & t_value
    assert wrapB % wrapA == (b % a) & t_value
    assert list(divmod(wrapB, wrapA)) == list(i & t_value for i in divmod(b, a))
    assert wrapB & wrapA == (b & a) & t_value
    assert wrapB | wrapA == (b | a) & t_value
    assert wrapB ^ wrapA == (b ^ a) & t_value
    assert wrapB << wrapShiftBits == (b << wrapShiftBits) & t_value
    assert wrapB >> wrapShiftBits == (b >> wrapShiftBits) & t_value

    assert (wrapA != wrapB) == (a != b)
    assert (wrapA == wrapB) == (a == b)
    assert (wrapA >= wrapB) == (a >= b)
    assert (wrapA > wrapB) == (a > b)
    assert (wrapA <= wrapB) == (a <= b)
    assert (wrapA < wrapB) == (a < b)

    assert (wrapB == wrapA) == (b == a)
    assert (wrapB >= wrapA) == (b >= a)
    assert (wrapB > wrapA) == (b > a)
    assert (wrapB <= wrapA) == (b <= a)
    assert (wrapB < wrapA) == (b < a)
    assert (wrapB != wrapA) == (b != a)

    assert wrapA.bit_rol(wrapShiftBits) == ROL(a, wrapShiftBits, t_size * 8)
    assert wrapA.bit_ror(wrapShiftBits) == ROR(a, wrapShiftBits, t_size * 8)
    assert wrapB.bit_rol(wrapShiftBits) == ROL(b, wrapShiftBits, t_size * 8)
    assert wrapB.bit_rol(wrapShiftBits) == ROR(b, wrapShiftBits, t_size * 8)

    log.success(f'check end: a={hex(a)}, b={hex(b)}')


# class BYTEList(WrapList):
#     def __init__(self, v: List): super().__init__(BYTE, v)
#
#     def toBYTEList(self): return BYTEList(DWORDs2BYTEs(self))
#     def toByteArray(self): return bytearray([i.value() for i in self])
#     def toWORDList(self): return WORDList(BYTEs2WORDs(self))
#     def toDWORDList(self): return DWORDList(BYTEs2DWORDs(self))
#     def toQWORDList(self): return QWORDList(BYTEs2QWORDs(self))
#     def toOWORDList(self): return OWORDList(BYTEs2OWORDs(self))


# class WORDList(WrapList):
#     def __init__(self, v): super().__init__(WORD, v)
#     def toBYTEList(self): return BYTEList(WORDs2BYTEs(self))
#     def toDWORDList(self): return DWORDList(WORDs2DWORDs(self))
#     def toQWORDList(self): return QWORDList(WORDs2QWORDs(self))
#     def toOWORDList(self): return OWORDList(WORDs2OWORDs(self))
#
#
# class DWORDList(WrapList):
#     def __init__(self, v): super().__init__(DWORD, v)
#
#     def toBYTEList(self): return BYTEList(DWORDs2BYTEs(self))
#     def toWORDList(self): return WORDList(DWORDs2WORDs(self))
#     def toQWORDList(self): return QWORDList(DWORDs2QWORDs(self))
#     def toOWORDList(self): return OWORDList(DWORDs2OWORDs(self))
#
#
# class QWORDList(WrapList):
#     def __init__(self, v): super().__init__(QWORD, v)
#
#     def toBYTEList(self): return BYTEList(QWORDs2BYTEs(self))
#     def toWORDList(self): return WORDList(QWORDs2WORDs(self))
#     def toDWORDList(self): return DWORDList(QWORDs2DWORDs(self))
#     def toOWORDList(self): return OWORDList(QWORDs2OWORDs(self))


# class OWORDList(WrapList):
#     def __init__(self, v): super().__init__(OWORD, v)
#
#     def toBYTEList(self): return BYTEList(OWORDs2BYTEs(self))
#     def toWORDList(self): return WORDList(OWORDs2WORDs(self))
#     def toDWORDList(self): return WORDList(OWORDs2DWORDs(self))
#     def toQWORDList(self): return QWORDList(OWORDs2QWORDs(self))


if __name__ == '__main__':
    test_unit(BYTE)
    test_unit(WORD)
    test_unit(DWORD)
    test_unit(QWORD)
    test_unit(OWORD)

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
    prpr(BaseIntList([0x10, 0x23], BYTE))
    prpr(DWORDList([0x121012, 0x23, 0x7645, 0x1341, 0x7645, 0x24]))




