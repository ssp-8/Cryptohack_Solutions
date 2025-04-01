import socket,json
from Cryptodome.Util.number import *

HOST,PORT = "socket.cryptohack.org",13405

BLOCK_SIZE = 32

# Nothing up my sleeve numbers (ref: Dual_EC_DRBG P-256 coordinates)
W = [0x6b17d1f2, 0xe12c4247, 0xf8bce6e5, 0x63a440f2, 0x77037d81, 0x2deb33a0, 0xf4a13945, 0xd898c296]
X = [0x4fe342e2, 0xfe1a7f9b, 0x8ee7eb4a, 0x7c0f9e16, 0x2bce3357, 0x6b315ece, 0xcbb64068, 0x37bf51f5]
Y = [0xc97445f4, 0x5cdef9f0, 0xd3e05e1e, 0x585fc297, 0x235b82b5, 0xbe8ff3ef, 0xca67c598, 0x52018192]
Z = [0xb28ef557, 0xba31dfcb, 0xdd21ac46, 0xe2a91e3c, 0x304f44cb, 0x87058ada, 0x2cb81515, 0x1e610046]

# Lets work with bytes instead!
W_bytes = b''.join([x.to_bytes(4,'big') for x in W])
X_bytes = b''.join([x.to_bytes(4,'big') for x in X])
Y_bytes = b''.join([x.to_bytes(4,'big') for x in Y])
Z_bytes = b''.join([x.to_bytes(4,'big') for x in Z])

def pad(data):
    padding_len = (BLOCK_SIZE - len(data)) % BLOCK_SIZE
    return data + bytes([padding_len] * padding_len)

def xor(a, b):
    return bytes([x ^ y for x, y in zip(a, b)])

def rotate_left(data, x):
    x = x % BLOCK_SIZE
    return data[x:] + data[:x]

def rotate_right(data, x):
    x = x % BLOCK_SIZE
    return data[-x:] + data[:-x]

def blocks(data):
    return [data[i:(i+BLOCK_SIZE)] for i in range(0,len(data),BLOCK_SIZE)]


def cryptohash(msg):
    initial_state = xor(Y_bytes, Z_bytes)
    temp = initial_state
    msg_padded = pad(msg)
    msg_blocks = blocks(msg_padded)
    for i,b in enumerate(msg_blocks):
        mix_in = scramble_block(b)
        for _ in range(i):
            mix_in = rotate_right(mix_in, i+11)
            mix_in = xor(mix_in, X_bytes)
            mix_in = rotate_left(mix_in, i+6)
        initial_state = xor(initial_state,mix_in)
    return initial_state.hex(),temp

def scramble_block(block):
    for _ in range(40):
        block = xor(W_bytes, block)
        block = rotate_left(block, 6)
        block = xor(X_bytes, block)
        block = rotate_right(block, 17)
    return block

def unscramble(mix_in):
    for _ in range(40):
        mix_in = rotate_left(mix_in,17)
        mix_in = xor(X_bytes,mix_in)
        mix_in = rotate_right(mix_in,6)
        mix_in = xor(W_bytes,mix_in)
    return mix_in

def go_backward(mix_in):
    b = unscramble(mix_in)
    return b

def connect():
    s = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    s.connect((HOST,PORT))
    recv = ""
    while True:
        data = s.recv(4096)
        if not data:
            break
        recv+=data.decode()
        if "JSON:" in recv:
            break
    
    m1 = ("a"*64).encode()
    print(len(m1))
    hash,initial_state = cryptohash(m1)
    m2_mixin = int(hash,16)^bytes_to_long(initial_state)
    m2 = go_backward(long_to_bytes(m2_mixin))
    to_send = {
        "m1":hex(bytes_to_long(m1))[2:],
        "m2":hex(bytes_to_long(m2))[2:]
    }
    m2_hash,_ = cryptohash(m2)
    print(hash,m2_hash)
    s.sendall(json.dumps(to_send).encode())
    recv = ""
    while True:
        data = s.recv(4096)
        if not data:
            break
        recv+=data.decode()
        if "JSON:" in recv:
            break
    print(recv)

# print(len(W_bytes))
connect()