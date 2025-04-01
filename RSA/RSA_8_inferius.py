#!/usr/bin/env python3

from Cryptodome.Util.number import getPrime, inverse, bytes_to_long, long_to_bytes, GCD
from sympy import factorint

# e = 0x10001

# # n will be 8 * (100 + 100) = 1600 bits strong (I think?) which is pretty good
# p = getPrime(100)
# q = getPrime(100)
# phi = (p - 1) * (q - 1)
# d = inverse(e, phi)

# n = p * q

# FLAG = b"crypto{???????????????}"
# pt = bytes_to_long(FLAG)
# ct = pow(pt, e, n)

# print(f"n = {n}")
# print(f"e = {e}")
# print(f"ct = {ct}")

# pt = pow(ct, d, n)
# decrypted = long_to_bytes(pt)
# assert decrypted == FLAG

#### decryption ######

n = 984994081290620368062168960884976209711107645166770780785733
p =  848445505077945374527983649411
q = 1160939713152385063689030212503
T = (p-1)*(q-1)
e = 65537
d = inverse(e,T)
ct = 948553474947320504624302879933619818331484350431616834086273
pt = pow(ct,d,n)
print(long_to_bytes(pt).decode())





