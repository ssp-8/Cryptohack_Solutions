import socket
import json
from Cryptodome.Util.number import *

def connect():
    HOST,PORT = "socket.cryptohack.org",13403
    s = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    s.connect((HOST,PORT))
    recv = ""
    while True:
        data = s.recv(4096)
        if not data:
            break
        recv+=data.decode()
        if "0x" in recv:
            break
    p = int(recv.split("0x")[-1].split("Send")[0].replace('"',"").replace("\n",""),16)
    to_send = {
        "g":hex(p+1),
        "n":hex(p**2)
    }
    s.sendall(json.dumps(to_send).encode())
    recv = ""
    while True:
        data = s.recv(4096)
        if not data:
            break
        recv+=data.decode()
        if "What is my private key" in recv:
            break
    received = recv.split("What is")[0].split("key: ")[1].replace('"',"")
    print(received)
    to_send = {"x":hex((int(received[2:],16)-1)//p)}
    s.sendall(json.dumps(to_send).encode())
    recv = ""
    while True:
        data = s.recv(4096)
        if not data:
            break
        recv+=data.decode()
        print(recv)




connect()