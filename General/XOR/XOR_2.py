from Cryptodome.Util.number import *

key1 = "a6c8b6733c9b22de7bc0253266a3867df55acde8635e19c73313"
t1 = "37dcb292030faa90d07eec17e3b1c6d8daf94c35d4c9191a5e1e"
t2 = "c1545756687e7573db23aa1c3452a098b71a7fbf0fddddde5fc1"
t3 = "04ee9855208a2cd59091d04767ae47963170d1660df7f56f5faf"

key1 = bytes.fromhex(key1)
t2 = bytes.fromhex(t2)
t3 = bytes.fromhex(t3)

flag = [t3[i]^t2[i]^key1[i] for i in range(len(key1))]

flag_str = "".join([chr(_) for _ in flag])
print(flag_str)
print(key1)