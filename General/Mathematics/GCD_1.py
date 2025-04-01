def gcd(a,b):
    if a == 0:
        return b
    return gcd(b%a,a)

# print(gcd(66528,52920))
print(gcd(1007621497415251,288260533169915))