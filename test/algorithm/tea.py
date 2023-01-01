"""
#include <stdio.h>
#include <stdint.h>

void encrypt (uint32_t* v, uint32_t* k) {
    uint32_t v0=v[0], v1=v[1], sum=0, i;           /* set up */
    uint32_t delta=0x9e3779b9;                     /* a key schedule constant */
    uint32_t k0=k[0], k1=k[1], k2=k[2], k3=k[3];   /* cache key */
    for (i=0; i < 32; i++) {                       /* basic cycle start */
        sum += delta;
        v0 += ((v1<<4) + k0) ^ (v1 + sum) ^ ((v1>>5) + k1);
        v1 += ((v0<<4) + k2) ^ (v0 + sum) ^ ((v0>>5) + k3);
    }                                              /* end cycle */
    v[0]=v0; v[1]=v1;
}

void decrypt (uint32_t* v, uint32_t* k) {
    uint32_t v0=v[0], v1=v[1], sum=0xC6EF3720, i;  /* set up */
    uint32_t delta=0x9e3779b9;                     /* a key schedule constant */
    uint32_t k0=k[0], k1=k[1], k2=k[2], k3=k[3];   /* cache key */
    for (i=0; i<32; i++) {                         /* basic cycle start */
        v1 -= ((v0<<4) + k2) ^ (v0 + sum) ^ ((v0>>5) + k3);
        v0 -= ((v1<<4) + k0) ^ (v1 + sum) ^ ((v1>>5) + k1);
        sum -= delta;
    }                                              /* end cycle */
    v[0]=v0; v[1]=v1;
}

"""

import unittest
from uint import DWORD
from base.config import context

context.repr_format = 'hex'
context.trace_mode = False
context.strict_mode = True


def encrypt(v: [DWORD, DWORD], k: [DWORD, DWORD, DWORD, DWORD]) -> [DWORD, DWORD]:
    v0, v1 = v
    k0, k1, k2, k3 = k
    sum = 0x0
    delta = 0x9e3779b9  # constant
    for i in range(32):
        sum += delta
        v0 += ((v1 << 4) + k0) ^ (v1 + sum) ^ ((v1 >> 5) + k1)
        v1 += ((v0 << 4) + k2) ^ (v0 + sum) ^ ((v0 >> 5) + k3)
    return v0, v1


def decrypt(v: [DWORD, DWORD], k: [DWORD, DWORD, DWORD, DWORD]) -> [DWORD, DWORD]:
    v0, v1 = v
    k0, k1, k2, k3 = k
    sum_ = 0xC6EF3720
    delta = 0x9e3779b9  # constant
    for i in range(32):
        v1 -= ((v0 << 4) + k2) ^ (v0 + sum_) ^ ((v0 >> 5) + k3)
        v0 -= ((v1 << 4) + k0) ^ (v1 + sum_) ^ ((v1 >> 5) + k1)
        sum_ -= delta
    return v0, v1


class TestTea(unittest.TestCase):
    key: (DWORD, DWORD, DWORD, DWORD) = (DWORD.new(0x11111111), DWORD.new(0x22222222), DWORD.new(0x33333333), DWORD.new(0x44444444))
    plainText: (DWORD, DWORD) = (DWORD.new(0x12345678), DWORD.new(0x87654321))
    cipherText = (DWORD(0xde975088), DWORD(0x55e8c089))

    def test_encrypt(self):
        self.assertEqual(encrypt(self.plainText, self.key), self.cipherText)

    def test_decrypt(self):
        self.assertEqual(decrypt(self.cipherText, self.key), self.plainText)


if __name__ == '__main__':
    unittest.main()
