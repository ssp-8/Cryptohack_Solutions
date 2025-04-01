from Cryptodome.Util.number import bytes_to_long, long_to_bytes
import telnetlib
from Cryptodome.Cipher import AES
import json
import re
from pkcs1 import emsa_pkcs1_v15
import fastecdsa
from fastecdsa.point import Point
from Cryptodome.Util.Padding import pad

def bxor(a, b):
    return bytes(x ^ y for x, y in zip(a, b))


def hash(data, sig):
    data = pad(data, 16)
    out = sig
#     print(data)
    for i in range(0, len(data), 16):
        blk = data[i:i+16]
#         print(blk)
        out = bxor(AES.new(blk, AES.MODE_ECB).encrypt(out), out)
    return out

HOST = "socket.cryptohack.org"
PORT = 13388

def readline():
    return tn.read_until(b"\n")

def json_recv():
    line = readline().decode()
    st = line[line.find('{'):]
    return json.loads(st)

def json_send(hsh):
    request = json.dumps(hsh).encode()
    tn.write(request)

tn = telnetlib.Telnet(HOST, PORT)
print(readline())

to_send = json.loads(json.dumps({"option" : "sign", "message" : bytes([0]*15).hex()}))
json_send(to_send)
sig = json_recv()["signature"]
sig = hash(b'admin=True',bytes.fromhex(sig))

to_send = json.loads(json.dumps({"option" : "get_flag", "message" : (bytes([0]*15)+bytes([1])+b'admin=True').hex(), "signature" : sig.hex()}))
json_send(to_send)
print(json_recv())
