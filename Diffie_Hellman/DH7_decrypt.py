from Cryptodome.Cipher import AES
from Cryptodome.Util.Padding import pad, unpad
from Cryptodome.Util.number import *
from sympy.ntheory import discrete_log
import hashlib
import socket
import json

HOST = "socket.cryptohack.org"
PORT = 13379

def connect():
    s = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    s.connect((HOST,PORT))
    recv = ""
    print("Connected")
    p = 2410312426921032588552076022197566074856950548502459942654116941958108831682612228890093858261341614673227141477904012196503648957050582631942730706805009223062734745341073406696246014589361659774041027169249453200378729434170325843778659198143763193776859869524088940195577346119843545301547043747207749969763750084308926339295559968882457872412993810129130294592999947926365264059284647209730384947211681434464714438488520940127459844288859336526896320919633919
    a = 972107443837033796245864316200458246846904598488981605856765890478853088246897345487328491037710219222038930943365848626194109830309179393018216763327572120124760140018038673999837643377590434413866611132403979547150659053897355593394492586978400044375465657296027592948349589216415363722668361328689588996541370097559090335137676411595949335857341797148926151694299575970292809805314431447043469447485957669949989090202320234337890323293401862304986599884732815
    g = 2
    A = pow(g,a,p)
    to_send_bob = {
       "supported":["DH64"]
    }
    s.sendall(json.dumps(to_send_bob).encode())
    while True:
        data = s.recv(4096)
        if not data:
            break
        recv+=data.decode()
        
        if "Send to Alice" in recv:
            break
    print(recv)
    to_send_alice = {
        "chosen":"DH64"
    }
    recv = ""
    s.sendall(json.dumps(to_send_alice).encode())
    while True:
        data = s.recv(4096)
        if not data:
            break
        recv+=data.decode()
        # print(recv)
    print(recv)
    s.sendall(json.dumps(to_send_alice).encode())
    recv = ""
    s.sendall(json.dumps(to_send_alice).encode())
    while True:
        data = s.recv(4096)
        if not data:
            break
        recv+=data.decode()
        # print(recv)
    print(recv)


def get_a(p,g,A):
    print(p)
    for a in range(2,p):
        if pow(g,a,p) == A:
            return a


def is_pkcs7_padded(message):
    padding = message[-message[-1]:]
    return all(padding[i] == len(padding) for i in range(0, len(padding)))


def decrypt_flag(shared_secret: int, iv: str, ciphertext: str):
    # Derive AES key from shared secret
    sha1 = hashlib.sha1()
    sha1.update(str(shared_secret).encode('ascii'))
    key = sha1.digest()[:16]
    # Decrypt flag
    ciphertext = bytes.fromhex(ciphertext)
    iv = bytes.fromhex(iv)
    cipher = AES.new(key, AES.MODE_CBC, iv)
    plaintext = cipher.decrypt(ciphertext)

    if is_pkcs7_padded(plaintext):
        return unpad(plaintext, 16).decode('ascii')
    else:
        return plaintext.decode('ascii')

Alice =  {"p": "0xde26ab651b92a129", "g": "0x02", "A": "0x6afa7ed00525b07a"}
Bob = {"B": "0x3df1b9dafcc4adbe"}

p = bytes_to_long(bytes.fromhex(Alice["p"][2:]))
g = bytes_to_long(bytes.fromhex(Alice["g"][2:]))
A = bytes_to_long(bytes.fromhex(Alice["A"][2:]))


received =  {"iv": "21d05570531b3cb08be8e6b458227814", "encrypted_flag": "63ce0d851546d55649dc39d673663d789e2c59ce283219ef1198e4cc4e4610a6"}
a = discrete_log(p,A,g)
print(a)

shared_secret = pow(bytes_to_long(bytes.fromhex(Bob["B"][2:])),a,bytes_to_long(bytes.fromhex(Alice["p"][2:])))
print(decrypt_flag(shared_secret, received["iv"], received["encrypted_flag"]))

# connect()
