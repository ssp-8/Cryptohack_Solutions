from Cryptodome.Util.number import *
import socket,json

HOST,PORT = ("socket.cryptohack.org", 13391)

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
        if "domain." in recv:
            break
    to_send = {
      "option" : "get_signature",
      "secret":"0x2"
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
    key["option"] = "verify"
    to_send = {
        "option":"verify",
        "msg":key["signature"],
        "N":key["N"],
        "e":key["e"]
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
    # key = json.loads(recv)
    # to_send = {
    #     "option":"sign",
    #     "msg":key["secret"]
    # }
    # s.sendall(json.dumps(to_send).encode())
    # recv = ""
    # while True:
    #     data = s.recv(4096)
    #     if not data:
    #         break
    #     recv+=data.decode()
    #     print(recv)
    #     if "}" in recv:
    #         break
    # key = json.loads(recv)
    # m = long_to_bytes(int(key["signature"],16))
    # print(m)

connect()