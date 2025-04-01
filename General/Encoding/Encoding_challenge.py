from pwn import * # pip install pwntools
import json
import base64,codecs
from Cryptodome.Util.number import *

r = remote('socket.cryptohack.org', 13377, level = 'debug')

def json_recv():
    line = r.recvline()
    return json.loads(line.decode())

def json_send(hsh):
    request = json.dumps(hsh).encode()
    r.sendline(request)

ENCODINGS = [
    "base64",
    "hex",
    "rot13",
    "bigint",
    "utf-8",
]

def return_decoded(decoded):
    return {
        "decoded":decoded
    }

def handle_utf8(cipher):
    decoded = ""
    for num in cipher:
        decoded+=chr(num)
    return return_decoded(decoded)

def handle_base64(cipher):
    decoded = base64.b64decode(cipher)
    return return_decoded(decoded.decode())

def handle_rot13(cipher):
    print(cipher)
    return return_decoded(codecs.decode(cipher,"rot_13"))

def handle_bigint(cipher):
    return return_decoded(long_to_bytes(int(cipher,16)).decode())

def handle_hex(cipher):
    return return_decoded(bytes.fromhex(cipher).decode())

while True:
    received = json_recv()
    print(received)
    if received.get("flag","") != "":
        print(received["flag"])
        break
    if received.get("error","")!= "":
        break
    received_type = received["type"]
    if received_type == "utf-8":
        decoded = handle_utf8(received["encoded"])
        json_send(decoded)
    elif received_type == "hex":
        decoded = handle_hex(received["encoded"])
        json_send(decoded)
    elif received_type == "rot13":
        decoded = handle_rot13(received["encoded"])
        json_send(decoded)
    elif received_type == "base64":
        decoded = handle_base64(received["encoded"])
        json_send(decoded)
    elif received_type == "bigint":
        decoded = handle_bigint(received["encoded"])
        json_send(decoded)
