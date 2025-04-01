cipher = "0e0b213f26041e480b26217f27342e175d0e070a3c5b103e2526217f27342e175d0e077e263451150104"

cipher = bytes.fromhex(cipher).decode()
key_len = 8
key = ""
key+=chr(ord('c')^ord(cipher[0]))
key+=chr(ord('r')^ord(cipher[1]))
key+=chr(ord('y')^ord(cipher[2]))
key+=chr(ord('p')^ord(cipher[3]))
key+=chr(ord('t')^ord(cipher[4]))
key+=chr(ord('o')^ord(cipher[5]))
key+=chr(ord('{')^ord(cipher[6]))
key+=chr(ord('}')^ord(cipher[-1]))

decipher = "".join([chr(ord(key[i%key_len])^ord(cipher[i])) for i in range(len(cipher))])
print(decipher)
