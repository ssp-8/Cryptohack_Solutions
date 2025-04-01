from Cryptodome.PublicKey import RSA

with open("transparency.pem", "rb") as f:
    key = RSA.import_key(f.read())

# Get the modulus (N)
modulus = key.n
print("Modulus:", modulus)
