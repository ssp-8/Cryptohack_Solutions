from Cryptodome.Cipher import AES
from Cryptodome.Util.Padding import pad, unpad
from Cryptodome.Util.number import *
import hashlib
import socket
import json

HOST = "socket.cryptohack.org"
PORT = 13371

def connect():
    s = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    s.connect((HOST,PORT))
    recv = ""
    print("Connected")
    p = 2410312426921032588552076022197566074856950548502459942654116941958108831682612228890093858261341614673227141477904012196503648957050582631942730706805009223062734745341073406696246014589361659774041027169249453200378729434170325843778659198143763193776859869524088940195577346119843545301547043747207749969763750084308926339295559968882457872412993810129130294592999947926365264059284647209730384947211681434464714438488520940127459844288859336526896320919633919
    a = 972107443837033796245864316200458246846904598488981605856765890478853088246897345487328491037710219222038930943365848626194109830309179393018216763327572120124760140018038673999837643377590434413866611132403979547150659053897355593394492586978400044375465657296027592948349589216415363722668361328689588996541370097559090335137676411595949335857341797148926151694299575970292809805314431447043469447485957669949989090202320234337890323293401862304986599884732815
    g = 2
    A = pow(g,a,p)
    to_send_bob = {
        "p":hex(p),
        "A":hex(A),
        "g":hex(g)
    }
    s.sendall(json.dumps(to_send_bob).encode())
    while True:
        data = s.recv(4096)
        if not data:
            break
        recv+=data.decode()
        
        if "Send to Alice" in recv:
            break
    print(recv)
    Alice_data = {"p": "0xffffffffffffffffc90fdaa22168c234c4c6628b80dc1cd129024e088a67cc74020bbea63b139b22514a08798e3404ddef9519b3cd3a431b302b0a6df25f14374fe1356d6d51c245e485b576625e7ec6f44c42e9a637ed6b0bff5cb6f406b7edee386bfb5a899fa5ae9f24117c4b1fe649286651ece45b3dc2007cb8a163bf0598da48361c55d39a69163fa8fd24cf5f83655d23dca3ad961c62f356208552bb9ed529077096966d670c354e4abc9804f1746c08ca237327ffffffffffffffff", "g": "0x02", "A": "0x18a157953b31e8694cf24f31b0b492928879406dfc15f0d972f89d2f77d36a166ab0fe4f49325648029ceed2ba97ce9f5bdcbca7e04d8014c7c113ba8e314357a39b81bbcd13bd0f1a20f2dcc0c89f06d606c1b2afde30f841065d9279c4fa43895ed5c939b40e6dad2ef43c9639c0fc79dac6f43f4a915da9dc5b4dc2ec123acfcc2198abc5d036c25a3f9b9f9d00a68f7a47f963ca7f332429e4e17caedac158386e04a29862cb4e6623e990f11babb40da4816f7bf1ccb8297199f1d5429b"}
    Bob_data = {"B": "0xce517a8ba18518f1d94486080d689609af22a46efc2d90ba4bb110b2ba081a172e7a0a0914300748ee2e1832c43097f08a6bfc364bfedf2bb488af74dbccb72cab4a8b82485b2f038dcff8f96860093133df82e5cabe4e90d0222bca00e9857e69b48e13164849847c0c65eeb620394eb82341684a2864d64e40ecac44445f8770a2a309fa4c07bebaa0d903c60aa45593f03860402a63cd110f71662656240b011a64c0ac31576e16bb6a7f06221442a415a8bdf1f8cdd999f250788b34e467"}
    to_send_alice = {
        "B":hex(A)
    }
    recv = ""
    s.sendall(json.dumps(to_send_alice).encode())
    while True:
        data = s.recv(4096)
        if not data:
            break
        recv+=data.decode()
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

p = 2410312426921032588552076022197566074856950548502459942654116941958108831682612228890093858261341614673227141477904012196503648957050582631942730706805009223062734745341073406696246014589361659774041027169249453200378729434170325843778659198143763193776859869524088940195577346119843545301547043747207749969763750084308926339295559968882457872412993810129130294592999947926365264059284647209730384947211681434464714438488520940127459844288859336526896320919633919
a = 972107443837033796245864316200458246846904598488981605856765890478853088246897345487328491037710219222038930943365848626194109830309179393018216763327572120124760140018038673999837643377590434413866611132403979547150659053897355593394492586978400044375465657296027592948349589216415363722668361328689588996541370097559090335137676411595949335857341797148926151694299575970292809805314431447043469447485957669949989090202320234337890323293401862304986599884732815
g = 2
A = "8dedc268e5b7148d42ebd96a7bb3817d2659cf0bbe511e959b5562c63ea448818a213f6829bcf9e7f96851a4db148f536424f10dbd522e9d6fcc812591de135d470e5b69c77817bd34075d0e6feb0be462a5855cecb709644cee4b58b6072c0dd005328d554940dbe138a29d0f087b65367d04657c5d3b41933bc98952ca808ba7d01d8a8cd76a5e70844c22323e135806bf1011e165b8919650901fc06b30a1eadccef3ee51df001daa3555ba94dafdd2a186224af2bc7df7887e98bb90e7eb"
shared_secret = pow(bytes_to_long(bytes.fromhex(A)),a,p)
print(shared_secret)
received = {"iv": "2c70ffaccce84f10ba9eb8f7fecaa7ba", "encrypted_flag": "6944543ea6aba16f750fa43c3330dbd978c65d7f42ce6a00937562ffed00a37a"}
print(decrypt_flag(shared_secret, received["iv"], received["encrypted_flag"]))

# connect()
