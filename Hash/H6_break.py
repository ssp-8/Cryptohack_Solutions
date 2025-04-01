import socket
import json
from Cryptodome.Hash import MD5

HOST = "socket.cryptohack.org"
PORT = 13397

def connect(sock, request):
    if request:
        request_json = json.dumps(request).encode() + b"\n"
        sock.sendall(request_json)
    response = sock.recv(4096).decode()
    return response


key1_hex = "43727970746f4861636b2053656375726520536166650000000000000000000000000000000000000000000000000000000000000000000000000000000000008ff7b0f1af929b0af43c73f9ad2d40d4f0a6a2abd2e6f2de14d67e758c109afed3e9c3ee5c250876ef03ecfc10f6e0943e7daea180269d18c4d1c46a15be9fefce3af20a6af3880e73f86b8bb7ec8d2958387eb51ef9201ad517f6c0cc197d2eb38a16d6186293638bb4a1ef88697d889750ef1534acf4984424556884a95be3"
key2_hex = "43727970746f4861636b2053656375726520536166650000000000000000000000000000000000000000000000000000000000000000000000000000000000008ff7b0f1af929b0af43c73f9ad2d40d4f0a6a22bd2e6f2de14d67e758c109afed3e9c3ee5c250876ef03ecfc1076e1943e7daea180269d18c4d1c4ea15be9fefce3af20a6af3880e73f86b8bb7ec8d2958387e351ef9201ad517f6c0cc197d2eb38a16d6186293638bb4a1ef88e97c889750ef1534acf498442455e884a95be3"


key1_bytes = bytes.fromhex(key1_hex)
key2_bytes = bytes.fromhex(key2_hex)

md5_key1 = MD5.new(key1_bytes).hexdigest()
md5_key2 = MD5.new(key2_bytes).hexdigest()
print(md5_key1 == md5_key2)

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
    sock.connect((HOST, PORT))
    print(connect(sock,None))
    print(connect(sock, {"option": "insert_key", "key": key1_hex}))
    print(connect(sock, {"option": "insert_key", "key": key2_hex}))
    print(connect(sock, {"option": "unlock"}))