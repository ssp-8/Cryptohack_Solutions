from Cryptodome.Cipher import AES
from Cryptodome.Util.Padding import pad, unpad
from Cryptodome.Util.number import *
from sympy.ntheory import discrete_log
import hashlib
import socket
import json

HOST = "socket.cryptohack.org"
PORT = 13373

def connect():
    s = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    s.connect((HOST,PORT))
    recv = ""
    print("Connected")
    p = 2410312426921032588552076022197566074856950548502459942654116941958108831682612228890093858261341614673227141477904012196503648957050582631942730706805009223062734745341073406696246014589361659774041027169249453200378729434170325843778659198143763193776859869524088940195577346119843545301547043747207749969763750084308926339295559968882457872412993810129130294592999947926365264059284647209730384947211681434464714438488520940127459844288859336526896320919633919
    a = 953463030999042663
    g = 2
    A = pow(g,a,p)
    # to_send_alice = {
    #     "p":hex(p),
    #     "g":hex(g),
    #     "A":""
    # }
    # s.sendall(json.dumps(to_send_alice).encode())
    aliceParameters = {}
    aliceResponse = {}
    while True:
        data = s.recv(4096)
        if not data:
            break
        recv+=data.decode()
        if "send him some parameters:" in recv:
            break
    
    responses = recv.split("\n")
    # print(responses)
    aliceParameters = json.loads(responses[0].removeprefix("Intercepted from Alice: ").encode())
    aliceResponse = json.loads(responses[2].removeprefix("Intercepted from Alice: ").encode())
    # print(aliceParameters,aliceResponse)
    s.sendall(json.dumps({
        "p":aliceParameters["p"],
        "g":aliceParameters["A"],
        "A":"0x1"
    }).encode())
    recv = ""
    while True:
        data = s.recv(4096)
        if not data:
            break
        recv+=data.decode()

    # print(recv)
    bobResponse = json.loads(recv.split("}")[0].removeprefix("Bob says to you: ")+"}")
    return bobResponse["B"],aliceResponse
       


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
    
p = 16014776862127327721
a = 953463030999042663
g = 3

# Intercepted values
Alice_parameters = {
    "p": "0xffffffffffffffffc90fdaa22168c234c4c6628b80dc1cd129024e088a67cc74020bbea63b139b22514a08798e3404ddef9519b3cd3a431b302b0a6df25f14374fe1356d6d51c245e485b576625e7ec6f44c42e9a637ed6b0bff5cb6f406b7edee386bfb5a899fa5ae9f24117c4b1fe649286651ece45b3dc2007cb8a163bf0598da48361c55d39a69163fa8fd24cf5f83655d23dca3ad961c62f356208552bb9ed529077096966d670c354e4abc9804f1746c08ca237327ffffffffffffffff",
    "g": "0x02",
    "A": "0x3c275aefc315edccd4a475fe024e385dc72861556942348a3428c0bc64abc9ea1ef0ae0793d7a4409285ac19ff76159ba072021fbd93ccc1805e443380da859604b9e2d7cfef127769b3c64f8c4abae453418c905aedc2d6531f0d27a70e164817adda3f8cb3e5d17640c3252d80c50b07e20962a13bcd409fc7640bb3f651cd2c5b3ebea6b74a1ff3543cb4f5c19bc2fe6b6c4f3198d60a0a3169b299e42157785a4321ad6b4548ced9484037462d858aca3802ca5fc5469067be7680753038"
}

Bob_and_Alice_conv = {
    "B": "0x8d79b69390f639501d81bdce911ec9defb0e93d421c02958c8c8dd4e245e61ae861ef9d32aa85dfec628d4046c403199297d6e17f0c9555137b5e8555eb941e8dcfd2fe5e68eecffeb66c6b0de91eb8cf2fd0c0f3f47e0c89779276fa7138e138793020c6b8f834be20a16237900c108f23f872a5f693ca3f93c3fd5a853dfd69518eb4bab9ac2a004d3a11fb21307149e8f2e1d8e1d7c85d604aa0bee335eade60f191f74ee165cd4baa067b96385aa89cbc7722e7426522381fc94ebfa8ef0"
}

Bob_and_me_conv = {"B": "0x05fc403452e946df"}

Bob_response = {
    "iv": "b6b4e072a0b0cf992b2b47e6a9cd52e3",
    "encrypted": "27eb6c1401c1d8253aaa622611efe9540bd84104b4e5a8f74b7b815c4c0f3f5cc8774cbf6095ae05d89ccf8180cbddca70c5cc22347affd3f99837e5714b421a024a2196eb20f0861e7a5f51af2876db"
}

Alice_response ={"iv": "334e93074352d518324ab8d1d737e761", "encrypted": "c1df98ac76a26c32cc3c4dbe8eaf2949d723b8659ffb05ec38223414933f6e72"}
Bob_and_me_conv["B"] = bytes_to_long(bytes.fromhex(Bob_and_me_conv["B"][2:]))
Bob_and_Alice_conv["B"] = bytes_to_long(bytes.fromhex(Bob_and_Alice_conv["B"][2:]))

Alice_parameters["p"] = bytes_to_long(bytes.fromhex(Alice_parameters["p"][2:]))
Alice_parameters["A"] = bytes_to_long(bytes.fromhex(Alice_parameters["A"][2:]))
Alice_parameters["g"] = bytes_to_long(bytes.fromhex(Alice_parameters["g"][2:]))

# b = discrete_log(p,Bob_and_me_conv["B"],g)

# print(discrete_log(p,b,g))

# shared_secret_alice_bob = Bob_and_Alice_conv["B"]

# # shared_secret_bob_me = pow(Bob_and_me_conv["B"],a,p)
# # print(decrypt_flag(shared_secret_bob_me, Bob_response["iv"], Bob_response["encrypted"]))

shared_secret,aliceResponse = connect()
shared_secret = int(shared_secret,16)
print(decrypt_flag(shared_secret, aliceResponse["iv"], aliceResponse["encrypted"]))
