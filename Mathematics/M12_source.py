from Cryptodome.Util.number import getPrime, inverse, bytes_to_long, long_to_bytes

DATA = bytes.fromhex("372f0e88f6f7189da7c06ed49e87e0664b988ecbee583586dfd1c6af99bf20345ae7442012c6807b3493d8936f5b48e553f614754deb3da6230fa1e16a8d5953a94c886699fc2bf409556264d5dced76a1780a90fd22f3701fdbcb183ddab4046affdc4dc6379090f79f4cd50673b24d0b08458cdbe509d60a4ad88a7b4e2921")
FLAG = b'crypto{??????????????????????????????????????}'

def gen_keypair():
    p = getPrime(512)
    q = getPrime(512)
    N = p*q
    e = 65537
    phi = (p-1)*(q-1)
    d = inverse(e,phi)
    return N,e,d


def encrypt(m,e,N):
    m_int = bytes_to_long(m)
    c_int = pow(m_int,e,N)
    if m_int == c_int:
        print('RSA broken!?')
        return None
    else:
        return c_int

N,e,d = gen_keypair()

encrypted_data = encrypt(DATA,e,N)
encrypted_flag = encrypt(FLAG,e,N)

print(f'N = {hex(N)}')
print(f'e = {hex(e)}')
print(f'c = {hex(encrypted_flag)}')
