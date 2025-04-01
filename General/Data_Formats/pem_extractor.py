from Cryptodome.PublicKey import RSA

key = open("PEM.pem","r").read()
print(RSA.import_key(key).d)