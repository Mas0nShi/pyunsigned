"""
#include <stdio.h>
#include <stdint.h>

/* take 64 bits of data in v[0] and v[1] and 128 bits of key[0] - key[3] */

void encipher(unsigned int num_rounds, uint32_t v[2], uint32_t const key[4]) {
    unsigned int i;
    uint32_t v0=v[0], v1=v[1], sum=0, delta=0x9E3779B9;
    for (i=0; i < num_rounds; i++) {
        v0 += (((v1 << 4) ^ (v1 >> 5)) + v1) ^ (sum + key[sum & 3]);
        sum += delta;
        v1 += (((v0 << 4) ^ (v0 >> 5)) + v0) ^ (sum + key[(sum>>11) & 3]);
    }
    v[0]=v0; v[1]=v1;
}

void decipher(unsigned int num_rounds, uint32_t v[2], uint32_t const key[4]) {
    unsigned int i;
    uint32_t v0=v[0], v1=v[1], delta=0x9E3779B9, sum=delta*num_rounds;
    for (i=0; i < num_rounds; i++) {
        v1 -= (((v0 << 4) ^ (v0 >> 5)) + v0) ^ (sum + key[(sum>>11) & 3]);
        sum -= delta;
        v0 -= (((v1 << 4) ^ (v1 >> 5)) + v1) ^ (sum + key[sum & 3]);
    }
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
    sum_ = 0x0
    delta = 0x9e3779b9  # constant
    for i in range(32):
        v0 += (((v1 << 4) ^ (v1 >> 5)) + v1) ^ (sum_ + k[sum_ & 3])
        sum_ += delta
        v1 += (((v0 << 4) ^ (v0 >> 5)) + v0) ^ (sum_ + k[(sum_ >> 11) & 3])
    return v0, v1


def decrypt(v: [DWORD, DWORD], k: [DWORD, DWORD, DWORD, DWORD]) -> [DWORD, DWORD]:
    v0, v1 = v
    sum_ = 0x9e3779b9 * 32  # constant
    for i in range(32):
        v1 -= (((v0 << 4) ^ (v0 >> 5)) + v0) ^ (sum_ + k[(sum_ >> 11) & 3])
        sum_ -= 0x9e3779b9  # constant
        v0 -= (((v1 << 4) ^ (v1 >> 5)) + v1) ^ (sum_ + k[sum_ & 3])
    return v0, v1


class TestXTEA(unittest.TestCase):
    key: (DWORD, DWORD, DWORD, DWORD) = (DWORD.new(0x12345678), DWORD.new(0x23456789), DWORD.new(0x34567890), DWORD.new(0x45678901))
    plainText: (DWORD, DWORD) = (DWORD.new(0x12345678), DWORD.new(0x23456789))
    cipherText: (DWORD, DWORD) = (DWORD.new(0xe0a7b2fa), DWORD.new(0x8e1759b1))

    def test_encrypt(self):
        self.assertEqual(encrypt(self.plainText, self.key), self.cipherText)

    def test_decrypt(self):
        self.assertEqual(decrypt(self.cipherText, self.key), self.plainText)


if __name__ == '__main__':
    unittest.main()

# generate c code:
"""
#include <stdio.h>
#include <stdint.h>

/* take 64 bits of data in v[0] and v[1] and 128 bits of key[0] - key[3] */

void encipher(unsigned int num_rounds, uint32_t v[2], uint32_t const key[4]) {
    unsigned int i;
    uint32_t v0=v[0], v1=v[1], sum=0, delta=0x9E3779B9;
    for (i=0; i < num_rounds; i++) {
        v0 += (((v1 << 4) ^ (v1 >> 5)) + v1) ^ (sum + key[sum & 3]);
        sum += delta;
        v1 += (((v0 << 4) ^ (v0 >> 5)) + v0) ^ (sum + key[(sum>>11) & 3]);
    }
    v[0]=v0; v[1]=v1;
}

void decipher(unsigned int num_rounds, uint32_t v[2], uint32_t const key[4]) {
    unsigned int i;
    uint32_t v0=v[0], v1=v[1], delta=0x9E3779B9, sum=delta*num_rounds;
    for (i=0; i < num_rounds; i++) {
        v1 -= (((v0 << 4) ^ (v0 >> 5)) + v0) ^ (sum + key[(sum>>11) & 3]);
        sum -= delta;
        v0 -= (((v1 << 4) ^ (v1 >> 5)) + v1) ^ (sum + key[sum & 3]);
    }
    v[0]=v0; v[1]=v1;
}

int main() {
    uint32_t key[4] = {0x12345678, 0x23456789, 0x34567890, 0x45678901};
    uint32_t v[2] = {0x12345678, 0x23456789};
    encipher(32, v, key);
    printf("0x%x, 0x%x\\n", v[0], v[1]);
    return 0;
}
"""