import unittest
from ..convert import *


class Convert(unittest.TestCase):
    def test_BYTEn(self):
        Value = 0xdeadbeef
        self.assertEqual(Conversions.BYTEn(Value, 0), 0xef)
        self.assertEqual(Conversions.BYTEn(Value, 1), 0xbe)
        self.assertEqual(Conversions.BYTEn(Value, 2), 0xad)
        self.assertEqual(Conversions.BYTEn(Value, 3), 0xde)

    def test_WORDn(self):
        Value = 0xdeadbeef12abcdef
        self.assertEqual(Conversions.WORDn(Value, 0), 0xcdef)
        self.assertEqual(Conversions.WORDn(Value, 1), 0x12ab)
        self.assertEqual(Conversions.WORDn(Value, 2), 0xbeef)
        self.assertEqual(Conversions.WORDn(Value, 3), 0xdead)

    def test_DWORDn(self):
        Value = 0xdeadbeef12abcdefdeadbeef12abcdef
        self.assertEqual(Conversions.DWORDn(Value, 0), 0x12abcdef)
        self.assertEqual(Conversions.DWORDn(Value, 1), 0xdeadbeef)
        self.assertEqual(Conversions.DWORDn(Value, 2), 0x12abcdef)
        self.assertEqual(Conversions.DWORDn(Value, 3), 0xdeadbeef)

    def test_QWORDn(self):
        Value = 0xdeadbeef12abcdefdeadbeef12abcdefdeadbeef12abcdefdeadbeef12abcdef
        self.assertEqual(Conversions.QWORDn(Value, 0), 0xdeadbeef12abcdef)
        self.assertEqual(Conversions.QWORDn(Value, 1), 0xdeadbeef12abcdef)
        self.assertEqual(Conversions.QWORDn(Value, 2), 0xdeadbeef12abcdef)
        self.assertEqual(Conversions.QWORDn(Value, 3), 0xdeadbeef12abcdef)

    def test_OWORDn(self):
        Value = 0xdeadbeef12abcdefdeadbeef12abcdefdeadbeef12abcdefdeadbeef12abcdefdeadbeef12abcdefdeadbeef12abcdefdeadbeef12abcdefdeadbeef12abcdef
        self.assertEqual(Conversions.OWORDn(Value, 0), 0xdeadbeef12abcdefdeadbeef12abcdef)
        self.assertEqual(Conversions.OWORDn(Value, 1), 0xdeadbeef12abcdefdeadbeef12abcdef)
        self.assertEqual(Conversions.OWORDn(Value, 2), 0xdeadbeef12abcdefdeadbeef12abcdef)
        self.assertEqual(Conversions.OWORDn(Value, 3), 0xdeadbeef12abcdefdeadbeef12abcdef)

    def test_ROL(self):
        self.assertEqual(ROL(0x35, 12, IntTypeInfo.BYTE.size * 8), 0x53)
        self.assertEqual(ROL(0x1213, 31, IntTypeInfo.WORD.size * 8), 0x8909)
        self.assertEqual(ROL(0x12131141, 12, IntTypeInfo.DWORD.size * 8), 0x31141121)
        self.assertEqual(ROL(0x1213114112131141, 122, IntTypeInfo.QWORD.size * 8), 0x4484c4504484c45)
        self.assertEqual(ROL(0x1131131112314114112ff12a141121b4, 675, IntTypeInfo.OWORD.size * 8), 0x918a08a0897f8950a0890da089889888)

    def test_BYTE(self):
        # Constructor
        condition = BYTE(0x31)
        self.assertEqual(condition.int, 0x31)  # get value
        self.assertEqual(int(condition), 0x31)     # convert to int

        # Xor
        condition = BYTE(0x31) ^ BYTE(0x45)
        self.assertEqual(condition.int, 0x74)
        condition = BYTE(0x31) ^ 0x45
        self.assertEqual(condition.int, 0x74)

        # Rshift
        condition = BYTE(0x31) << BYTE(0x3)
        self.assertEqual(condition.int, 0x88)
        condition = BYTE(0x31) << 0x3
        self.assertEqual(condition.int, 0x88)
        # Rshift overflow
        condition = BYTE(0x31) << BYTE(0x34)
        self.assertEqual(condition.int, 0x0)
        # Rotate rshift
        condition = BYTE(0x31).bit_ror(0x12)
        self.assertEqual(condition.int, 0x4C)
        condition = BYTE(0x31).bit_ror(BYTE(0x12))
        self.assertEqual(condition.int, 0x4C)

        # Lshift
        condition = BYTE(0x45) >> BYTE(0x3)
        self.assertEqual(condition.int, 0x8)
        condition = BYTE(0x45) >> 0x3
        self.assertEqual(condition.int, 0x8)
        # Lshift overflow
        condition = BYTE(0x45) >> BYTE(0x12)
        self.assertEqual(condition.int, 0x0)
        # Rotate lshift
        condition = BYTE(0x31).bit_rol(0x34)
        self.assertEqual(condition.int, 0x13)
        condition = BYTE(0x31).bit_rol(BYTE(0x34))
        self.assertEqual(condition.int, 0x13)


if __name__ == '__main__':
    unittest.main()
