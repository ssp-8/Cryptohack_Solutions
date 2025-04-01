from Cryptodome.Cipher import AES
from Cryptodome.Util.Padding import pad, unpad
from Cryptodome.Util.number import *
from sympy.ntheory import discrete_log
import hashlib
import socket
import json

HOST = "socket.cryptohack.org"
PORT = 13380

def connect():
    s = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    s.connect((HOST,PORT))
    recv = ""
    print("Connected")
    while True:
        data = s.recv(4096)
        if not data:
            break
        recv+=data.decode()
        if "Send to Alice" in recv:
            break
    print(recv)


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

Alice_parameters ={"p": "0xffffffffffffffffc90fdaa22168c234c4c6628b80dc1cd129024e088a67cc74020bbea63b139b22514a08798e3404ddef9519b3cd3a431b302b0a6df25f14374fe1356d6d51c245e485b576625e7ec6f44c42e9a637ed6b0bff5cb6f406b7edee386bfb5a899fa5ae9f24117c4b1fe649286651ece45b3dc2007cb8a163bf0598da48361c55d39a69163fa8fd24cf5f83655d23dca3ad961c62f356208552bb9ed529077096966d670c354e4abc9804f1746c08ca237327ffffffffffffffff", 
                   "g": "0x02", 
                   "A": "0x658a277c05317e90b9902719ef08986c2f213087a9691f7fa3b4b802a9fb8b8dca71cd0100c2c43c8380e1ba3b8748af0e37c9a7f91466f88a149e63e10c664b41865b98c216f5435caeb3640fb56215b3e77c08451ec499d38e5006ce1d438b85723abf9d30ca5516ed73d2f46a3f9accf3e180a354c6cd9c66a6f5a5c7baa5e8249ff29ceb4f3d354ed26206af90039a6655ac54918518933b9b7b0f1b3bf734dc268d756a4901596dca249d1d7eca4a2553aca591b7848148996ad1715c96"}

Bob_and_Alice_conv = {"B": "0x824702b017925e8c906067baf5ec8ffeb5573e07df1013a3ebb7db1d764a27bdfa16e73a41abfa50ada3575ed7423c2ee7c8516d53be58449a60aeb4a4437cc974f480c1c0e745a789358166f5a49befc3b15615a20e92b70400a3d96651ac68e9d6a6111a23c3ffea67eb251d1d2d218c79405611e60d21bf5ad39b0a62913587b901f6e055136c961301fba45e393a0e51f37d9fe87cd84ffc4ddfd0711523668bf177b0877a8229ddc900840da5014e860bbb8a12685989e23922a215b1ea"}

Alice_response ={"iv": "ae53ee365b11a24cbe8476157cd810f8", 
                 "encrypted": "2cf707181622195770e5ff2b06a62107a1674f0d0c3c9a207da259321cce0573621fd1be90618baf05b99c2db2d299b7"}

g = 2
p = bytes_to_long(bytes.fromhex(Alice_parameters["p"][2:]))
A = bytes_to_long(bytes.fromhex(Alice_parameters["A"][2:]))
B = bytes_to_long(bytes.fromhex(Bob_and_Alice_conv["B"][2:]))

a = (inverse(g,p) * A) % p
shared_secret = (B * a) % p

print(decrypt_flag(shared_secret, Alice_response["iv"], Alice_response["encrypted"]))

# connect()
