m = (2**11 - 1) / (2**11)
x = 1
while m >= 0.5:
    x+=1
    m*=(2**11 - 1)/(2**11)

print(x,m)