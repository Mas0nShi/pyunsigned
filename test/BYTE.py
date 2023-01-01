import unittest
from itertools import product
from uint import BYTE
from base.config import context
from ctypes import c_uint8
from random import randint

context.repr_format = 'hex'
context.trace_mode = True

class TestBYTE(unittest.TestCase):
    def test_overflow(self):
        for bits in (8, 16, 32, 64, 128):
            v = randint(1 << 0, (1 << bits) - 1)
            self.assertEqual(BYTE(v), c_uint8(v).value)

    def test_add(self):
        r1, r2 = 0x12, 0x34
        b1, b2 = BYTE.new(r1), BYTE.new(r2)
        r = c_uint8(r1 + r2).value
        for item in product((b1, r1), (b2, r2)):
            if isinstance(item[0], int) and isinstance(item[1], int):
                continue
            t = item[0] + item[1]
            self.assertEqual(t, r)

    def test_sub(self):
        r1, r2 = 0x12, 0x34
        b1, b2 = BYTE.new(r1), BYTE.new(r2)
        r = c_uint8(r1 - r2).value
        for item in product((b1, r1), (b2, r2)):
            if isinstance(item[0], int) and isinstance(item[1], int):
                continue
            t = item[0] - item[1]
            self.assertEqual(t, r)

    def test_mul(self):
        r1, r2 = 0x12, 0x34
        b1, b2 = BYTE.new(r1), BYTE.new(r2)
        r = c_uint8(r1 * r2).value
        for item in product((b1, r1), (b2, r2)):
            if isinstance(item[0], int) and isinstance(item[1], int):
                continue
            t = item[0] * item[1]
            self.assertEqual(t, r)

    def test_div(self):
        r1, r2 = 0x12, 0x34
        b1, b2 = BYTE.new(r1), BYTE.new(r2)
        r = c_uint8(r1 // r2).value
        for item in product((b1, r1), (b2, r2)):
            if isinstance(item[0], int) and isinstance(item[1], int):
                continue
            t = item[0] // item[1]
            self.assertEqual(t, r)

    def test_floordiv(self):
        r1, r2 = 0x12, 0x34
        b1, b2 = BYTE.new(r1), BYTE.new(r2)
        r = c_uint8(r1 // r2).value
        for item in product((b1, r1), (b2, r2)):
            if isinstance(item[0], int) and isinstance(item[1], int):
                continue
            t = item[0] // item[1]
            self.assertEqual(t, r)

    def test_mod(self):
        r1, r2 = 0x12, 0x34
        b1, b2 = BYTE.new(r1), BYTE.new(r2)
        r = c_uint8(r1 % r2).value
        for item in product((b1, r1), (b2, r2)):
            if isinstance(item[0], int) and isinstance(item[1], int):
                continue
            t = item[0] % item[1]
            self.assertEqual(t, r)

    def test_pow(self):
        r1, r2 = 0x12, 0x34
        b1, b2 = BYTE.new(r1), BYTE.new(r2)
        r = c_uint8(r1 ** r2).value
        for item in product((b1, r1), (b2, r2)):
            if isinstance(item[0], int) and isinstance(item[1], int):
                continue
            t = item[0] ** item[1]
            self.assertEqual(t, r)

    def test_lshift(self):
        r1, r2 = 0x12, 0x34
        b1, b2 = BYTE.new(r1), BYTE.new(r2)
        r = c_uint8(r1 << r2).value
        for item in product((b1, r1), (b2, r2)):
            if isinstance(item[0], int) and isinstance(item[1], int):
                continue
            t = item[0] << item[1]
            self.assertEqual(t, r)

    def test_rshift(self):
        r1, r2 = 0x12, 0x34
        b1, b2 = BYTE.new(r1), BYTE.new(r2)
        r = c_uint8(r1 >> r2).value
        for item in product((b1, r1), (b2, r2)):
            if isinstance(item[0], int) and isinstance(item[1], int):
                continue
            t = item[0] >> item[1]
            self.assertEqual(t, r)

    def test_and(self):
        r1, r2 = 0x12, 0x34
        b1, b2 = BYTE.new(r1), BYTE.new(r2)
        r = c_uint8(r1 & r2).value
        for item in product((b1, r1), (b2, r2)):
            if isinstance(item[0], int) and isinstance(item[1], int):
                continue
            t = item[0] & item[1]
            self.assertEqual(t, r)

    def test_or(self):
        r1, r2 = 0x12, 0x34
        b1, b2 = BYTE.new(r1), BYTE.new(r2)
        r = c_uint8(r1 | r2).value
        for item in product((b1, r1), (b2, r2)):
            if isinstance(item[0], int) and isinstance(item[1], int):
                continue
            t = item[0] | item[1]
            self.assertEqual(t, r)

    def test_xor(self):
        r1, r2 = 0x12, 0x34
        b1, b2 = BYTE.new(r1), BYTE.new(r2)
        r = c_uint8(r1 ^ r2).value
        for item in product((b1, r1), (b2, r2)):
            if isinstance(item[0], int) and isinstance(item[1], int):
                continue
            t = item[0] ^ item[1]
            self.assertEqual(t, r)

    def test_invert(self):
        r1 = 0x12
        b1 = BYTE.new(r1)
        r = c_uint8(~r1).value
        t = ~b1
        self.assertEqual(t, r)

    def test_neg(self):
        r1 = 0x12
        b1 = BYTE.new(r1)
        r = c_uint8(-r1).value
        t = -b1
        self.assertEqual(t, r)

    def test_pos(self):
        r1 = 0x12
        b1 = BYTE.new(r1)
        r = c_uint8(+r1).value
        t = +b1
        self.assertEqual(t, r)

    def test_abs(self):
        r1 = 0x12
        b1 = BYTE.new(r1)
        r = abs(r1)
        t = abs(b1)
        self.assertEqual(t, r)

    def test_int(self):
        r1 = 0x12
        b1 = BYTE.new(r1)
        r = int(r1)
        t = int(b1)
        self.assertEqual(t, r)

    def test_round(self):
        r1 = 0x12
        b1 = BYTE.new(r1)
        r = round(r1)
        t = round(b1)
        self.assertEqual(t, r)

    def test_ge(self):
        r1, r2 = 0x12, 0x34
        b1, b2 = BYTE.new(r1), BYTE.new(r2)
        r = r1 >= r2
        t = b1 >= b2
        self.assertEqual(t, r)

    def test_gt(self):
        r1, r2 = 0x12, 0x34
        b1, b2 = BYTE.new(r1), BYTE.new(r2)
        r = r1 > r2
        t = b1 > b2
        self.assertEqual(t, r)

    def test_le(self):
        r1, r2 = 0x12, 0x34
        b1, b2 = BYTE.new(r1), BYTE.new(r2)
        r = r1 <= r2
        t = b1 <= b2
        self.assertEqual(t, r)

    def test_lt(self):
        r1, r2 = 0x12, 0x34
        b1, b2 = BYTE.new(r1), BYTE.new(r2)
        r = r1 < r2
        t = b1 < b2
        self.assertEqual(t, r)

    def test_eq(self):
        r1, r2 = 0x12, 0x34
        b1, b2 = BYTE.new(r1), BYTE.new(r2)
        r = r1 == r2
        t = b1 == b2
        self.assertEqual(t, r)

    def test_ne(self):
        r1, r2 = 0x12, 0x34
        b1, b2 = BYTE.new(r1), BYTE.new(r2)
        r = r1 != r2
        t = b1 != b2
        self.assertEqual(t, r)

    def test_hash(self):
        r1 = 0x12
        b1 = BYTE.new(r1)
        r = hash(r1)
        t = hash(b1)
        self.assertEqual(t, r)



if __name__ == '__main__':
    unittest.main()
