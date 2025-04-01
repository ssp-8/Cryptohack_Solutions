cipher = "73626960647f6b206821204f21254f7d694f7624662065622127234f726927756d"
cipher = bytes.fromhex(cipher).decode()
for _ in range(128):
    deciphered = "".join([chr(ord(char)^_) for char in cipher])
    print(deciphered)