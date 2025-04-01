from Cryptodome.Util.number import *
import socket,json

HOST,PORT = ("socket.cryptohack.org", 13374)

def connect():
    s = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    s.connect((HOST,PORT))
    recv = ""
    while True:
        data = s.recv(4096)
        if not data:
            break
        recv+=data.decode()
        print(recv)
        if "sign" in recv:
            break
    to_send = {
      "option" : "get_pubkey"
    }
    s.sendall(json.dumps(to_send).encode())
    recv = ""
    while True:
        data = s.recv(4096)
        if not data:
            break
        recv+=data.decode()
        # print(recv)
        if "}" in recv:
            break
    key = json.loads(recv)
    to_send = {
        "option":"get_secret"
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
    key = json.loads(recv)
    to_send = {
        "option":"sign",
        "msg":key["secret"]
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
    key = json.loads(recv)
    m = long_to_bytes(int(key["signature"],16))
    print(m)

connect()