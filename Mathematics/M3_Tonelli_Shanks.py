import random

def get_Q_and_S(x):
    z = 0
    while x % 2 == 0:
        x//=2
        z+=1
    
    return x,z

def get_quadratic_non_residue(p):
    while True:
        a = random.randint(2,p-1)
        # print(f"In get quadratic non residue {a}")
        # print(pow(a,(p-1)//2,p))
        if pow(a,(p-1)//2,p) == p-1:
            return a

def Tonelli_Shanks(n, p):

    q, s = get_Q_and_S(p - 1)
    z = get_quadratic_non_residue(p)

    m = s
    c = pow(z, q, p)
    t = pow(n, q, p)
    r = pow(n, (q+1)//2, p)

    while t != 1:
        i = 1
        while pow(t, 2**i, p) != 1:
            i += 1
        b = pow(c, 2**(m-i-1), p)
        m = i
        c = (b * b) % p
        t = (t * c) % p
        r = (r * b) % p

    return r

def get_p_and_n(filepath):
    contents = open(filepath,"r").readlines()
    n = int(contents[0].split(" ")[-1].replace("\n",""))
    p = int(contents[1].split(" ")[-1].replace("\n",""))
    return n,p

n,p = get_p_and_n("M3_output.txt")
r = Tonelli_Shanks(n,p)
print(r)
