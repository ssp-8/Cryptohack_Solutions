import socket,json
from Cryptodome.Util.number import *

HOST,PORT = "socket.cryptohack.org", 13392

def connect(prime,comp2):
    s = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    s.connect((HOST,PORT))
    recv = ""
    while True:
        data = s.recv(4096)
        if not data:
            break
        recv+=data.decode()
        if "number is prime" in recv:
            break
    to_send = {
        "option":"sign",
        "prime":prime
    }
    s.sendall(json.dumps(to_send).encode())
    recv = ""
    while True:
        data = s.recv(4096)
        if not data:
            break
        recv+=data.decode()
        if "}" in recv:
            break
    received = json.loads(recv)
    to_send = {
        "option":"check",
        "prime":comp2,
        "a":71,
        "signature":received["signature"]
    }
    s.sendall(json.dumps(to_send).encode())
    recv = ""
    while True:
        data = s.recv(4096)
        if not data:
            break
        recv+=data.decode()
        print(recv)
        if "}" in recv:
            break

x = "4dc968ff0ee35c209572d4777b721587d36fa7b21bdc56b74a3dc0783e7b9518afbfa200a8284bf36e8e4b55b35f427593d849676da0d1555d8360fb5f07fea2"
y = "4dc968ff0ee35c209572d4777b721587d36fa7b21bdc56b74a3dc0783e7b9518afbfa202a8284bf36e8e4b55b35f427593d849676da0d1d55d8360fb5f07fea2"

z = 1

xx = 0
yy = 0

while True:
    
    xx = bytes_to_long(bytes.fromhex(x) + long_to_bytes(z))
    yy = bytes_to_long(bytes.fromhex(y) + long_to_bytes(z))
    if isPrime(xx) and not isPrime(yy):
        break
    z += 2

print(xx.bit_length())
connect(xx,yy)