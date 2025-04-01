string = "label"

xorr = ""
for char in string:
    xorr+=chr(ord(char)^13)

print("crypto{"+xorr+"}")
