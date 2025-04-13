
def accept_user_input():
    num1 = int(input("Enter number1: "))
    num2 = int(input("Enter number2: "))
    return num1, num2

def add(num1, num2):
    return num1 + num2

def multiply(num1, num2):
    return num1 * num2

def subtract(num1, num2):
    return num1 - num2

def divide(num1, num2):
    return num1 / num2

def square(num1, num2):
    return num1 * num1, num2 * num2

def maximum(num1, num2):
    return num1 if num1 > num2 else num2

def minimum(num1, num2):
    return num1 if num1 < num2 else num2
  
def main():
    num1, num2 = accept_user_input()    
    sum = add(num1, num2)
    product = multiply(num1, num2)
    diff = subtract(num1, num2)
    quotient = divide(num1, num2)
    square1, square2 = square(num1, num2)
    max = maximum(num1, num2)
    min = minimum(num1, num2)

    print(f"sum of {num1} and {num2} = {sum}")
    print(f"product of {num1} and {num2} = {product}")
    print(f"subtracting {num2} from {num1} = {diff}")
    print(f"dividing {num1} by {num2} = {quotient}")
    print(f"square of {num1} = {square1} and square of {num2} = {square2}")
    print(f"Max of {num1} and {num2} = {max}")
    print(f"Min of {num1} and {num2} = {min}")
main()