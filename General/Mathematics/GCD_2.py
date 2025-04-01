# Python program to demonstrate working of 
# extended Euclidean Algorithm 

# Function for extended Euclidean Algorithm 
def gcdExtended(a, b, x, y):

    # Base Case 
    if a == 0: 
        x[0] = 0
        y[0] = 1
        return b 

    x1, y1 = [0], [0]
    gcd = gcdExtended(b % a, a, x1, y1)

    # Update x and y using results of 
    # recursive call 
    x[0] = y1[0] - (b // a) * x1[0] 
    y[0] = x1[0] 
    return gcd 

def findGCD(a, b):
    x, y = [1], [1]
    f = gcdExtended(a, b, x, y)
    print(x,y)

# Main function
def main():
    a, b = 26513,32321
    g = findGCD(a, b)

if __name__ == "__main__":
    main()