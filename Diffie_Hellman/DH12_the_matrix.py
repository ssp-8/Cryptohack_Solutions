import random

from cairo import Matrix
from sympy import GF

P = 2
N = 50
E = 31337

FLAG = b'crypto{??????????????????????????}'

def bytes_to_binary(s):
    bin_str = ''.join(format(b, '08b') for b in s)
    bits = [int(c) for c in bin_str]
    return bits

def generate_mat():
    while True:
        msg = bytes_to_binary(FLAG)
        msg += [random.randint(0, 1) for _ in range(N*N - len(msg))]

        rows = [msg[i::N] for i in range(N)]
        mat = Matrix(GF(2), rows)

        if mat.determinant() != 0 and mat.multiplicative_order() > 10^12:
            return mat

def load_matrix(fname):
    data = open(fname, 'r').read().strip()
    rows = [list(map(int, row)) for row in data.splitlines()]
    return Matrix(GF(2), rows)

def save_matrix(M, fname):
    open(fname, 'w').write('\n'.join(''.join(str(x) for x in row) for row in M))

# mat = generate_mat()

# ciphertext = mat^E
# save_matrix(ciphertext, 'flag.enc')

from sympy import GF, Matrix, mod_inverse

def extract_flag(matrix):
    flat_bits = [matrix[i, 0] for i in range(matrix.rows)]
    binary_str = ''.join(map(str, flat_bits))
    byte_data = int(binary_str, 2).to_bytes(len(binary_str) // 8, byteorder='big')
    return byte_data.decode(errors='ignore')

def load_matrix(fname):
    with open(fname, 'r') as file:
        data = file.read().strip()
    rows = [map(int, row) for row in data.splitlines()]
    return Matrix(GF(2), rows)

def compute_modular_inverse(E, order):
    try:
        return mod_inverse(E, order)
    except ValueError:
        print("Modular inverse does not exist!")
        return None

def decrypt(ciphertext, E):
    # Get the multiplicative order of the ciphertext matrix
    order = ciphertext.multiplicative_order()
    print(f"Multiplicative Order: {order}")

    # Compute the modular inverse of E modulo the order
    E_inv = compute_modular_inverse(E, order)
    print(f"Modular Inverse of {E}: {E_inv}")

    if E_inv is None:
        return None

    # Decrypt the matrix
    plaintext_matrix = ciphertext ** E_inv
    return plaintext_matrix

ciphertext = load_matrix("DH12_flag.enc")
plaintext_matrix = decrypt(ciphertext, 31337)

if plaintext_matrix:
    print("Decrypted Matrix:")
    print(plaintext_matrix)


flag = extract_flag(plaintext_matrix)
print(f"Decrypted Flag: {flag}")


# mat = load_matrix("DH12_flag.enc")
# plaintext = mat^E
# print(plaintext)
