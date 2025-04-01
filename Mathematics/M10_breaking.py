import os
from Cryptodome.Cipher import AES
from Cryptodome.Util.Padding import pad, unpad
from Cryptodome.Util.number import *
from hashlib import sha1
import random
from math import isqrt
from sympy import discrete_log

from collections import namedtuple
# Create a simple Point class to represent the affine points.
Point = namedtuple("Point", "x y")

# FLAG = b"crypto{????????????????????????????????}"  # REMOVE ME


def point_addition(P, Q):
    Rx = (P.x*Q.x + D*P.y*Q.y) % p
    Ry = (P.x*Q.y + P.y*Q.x) % p
    return Point(Rx, Ry)


def scalar_multiplication(P, n):
    Q = Point(1, 0)
    while n > 0:
        if n % 2 == 1:
            Q = point_addition(Q, P)
        P = point_addition(P, P)
        n = n//2
    return Q


def gen_keypair():
    private = random.randint(1, p-1)
    public = scalar_multiplication(G, private)
    return (public, private)


def gen_shared_secret(P, d):
    return scalar_multiplication(P, d).x

def decrypt_flag(shared_secret: int,iv:str, encrypted_flag:str):
    key = sha1(str(shared_secret).encode('ascii')).digest()[:16]
    iv = bytes.fromhex(iv)
    cipher = AES.new(key,AES.MODE_CBC,iv)
    flag = bytes.fromhex(encrypted_flag)
    flag = cipher.decrypt(flag)
    return flag.decode(errors='ignore')


# ================ #
# Curve parameters #
# ================ #
p = 173754216895752892448109692432341061254596347285717132408796456167143559
D = 529
G = Point(29394812077144852405795385333766317269085018265469771684226884125940148,
          94108086667844986046802106544375316173742538919949485639896613738390948)

A = Point(x=155781055760279718382374741001148850818103179141959728567110540865590463, y=73794785561346677848810778233901832813072697504335306937799336126503714)
B = Point(x=171226959585314864221294077932510094779925634276949970785138593200069419, y=54353971839516652938533335476115503436865545966356461292708042305317630)
flag = {'iv': '64bc75c8b38017e1397c46f85d4e332b', 'encrypted_flag': '13e4d200708b786d8f7c3bd2dc5de0201f0d7879192e6603d7c5d6b963e1df2943e3ff75f7fda9c30a92171bbbc5acbf'}

phi_G = (G.x + 23*G.y) % p
phi_A = (A.x + 23*A.y) % p

n_a = discrete_log(p,phi_A,phi_G)

shared_secret = gen_shared_secret(B,n_a)
flag = decrypt_flag(shared_secret,flag['iv'],flag['encrypted_flag'])
print(flag)


