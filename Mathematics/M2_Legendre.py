def get_ints_and_p(filepath):
    file = open(filepath,"r")
    contents = file.readlines()
    prime = int(contents[0].split(" ")[-1].replace("\n",""))

    ints = []
    nums = contents[-1].split(",")
    for num in nums:
        ints.append(int(num.replace("ints = [","").replace("]\n","").strip()))
    
    return ints,prime

def get_quadratic_residue(x,p):
    return pow(x,(p-1)//2,p) == 1

def get_square_root(x,p):
    return pow(x,(p+1)//4,p)

ints,p = get_ints_and_p("M2_output.txt")

for num in ints:
    if get_quadratic_residue(num,p):
        print(f"{num} is a quadratic residue with root {get_square_root(num,p)}")
    else:
        print(f"{num} is a quadratic-non residue")

