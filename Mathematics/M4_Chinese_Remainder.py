i = 0
x = 17*i + 5
while True:
    x = 17*i + 5
    if (x % 5 == 2) and (x % 11 == 3):
        break
    i+=1
    
print(x)
print(x % 935)