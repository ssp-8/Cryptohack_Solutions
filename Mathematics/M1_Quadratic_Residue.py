def get_square_root(x,p):
    for _ in range(p):
        if pow(_,2,p) == x:
            return _
    
    return "No"

ints = [14,6,11]

for num in ints:
    sqrt = get_square_root(num,29)
    if sqrt != "No":
        print(f"Root found for {num} : {sqrt}")
    else:
        print(f"{num} is a quadratic non-residue")
    

