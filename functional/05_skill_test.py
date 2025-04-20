# Implement a Calculator by taking 2 values from the input and choosing an operation

n1 = input("Enter 1st number: ")
n2 = input("Enter 2nd number: ")
operation = input("Enter operation (add/subtract/multiply/divide): ")

def add(x: int, y: int) -> int:
    return x + y

def subtract(x: int, y: int) -> int:
    return x - y

def multiply(x: int, y: int) -> int:
    return x * y

def divide(x: int, y: int) -> float:
    if y == 0:
        raise ZeroDivisionError("Division by zero is not allowed")

    return x / y


funcs = {'add': add, 'subtract':subtract, 'multiply': multiply, 'divide': divide}

if operation in funcs:
    print(f"{operation} is executed resulting in: {funcs[operation](int(n1), int(n2))}")
else:
    print("Operation not supported")