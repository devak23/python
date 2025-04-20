def add(x: int, y: int) -> int:
    return x + y

def subtract(x: int, y: int) -> int:
    return x - y


numbers = [5, 2]

funcs = [add, subtract] # functions are just like any other data type and therefore can be stored in a list as well

# we will then iterate and apply the functions add and subtract to the numbers passed in. First the addition and then subtraction
for func in funcs:
    print(func(*numbers))

