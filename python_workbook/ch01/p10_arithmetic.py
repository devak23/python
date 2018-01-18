from math import log10

# Create a program that reads two integers, a and b, from the user. Your program should
# compute and display:
# The sum of a and b
# The difference when b is subtracted from a
# The product of a and b
# The quotient when a is divided by b
# The remainder when a is divided by b
# The result of log 10 a
# The result of a^b

NULL_PARAM_ERROR = ValueError("Cannot have null parameters")


def user_input():
    try:
        num1 = int(input("Enter number 1: "))
        num2 = int(input("Enter number 2: "))
        return num1, num2
    except ValueError:
        print("ValueError - Input provided was invalid")
        return None
    except TypeError:
        print("TypeError - Invalid input provided")
        return None


class Arithmetic:
    def add(self, num1, num2):
        if num1 is not None and num2 is not None:
            return num1 + num2
        raise NULL_PARAM_ERROR

    def subtract(self, num1, num2):
        if num1 is not None and num2 is not None:
            return num1 - num2
        raise NULL_PARAM_ERROR

    def product(self, num1, num2):
        if num1 is not None and num2 is not None:
            return num1 * num2
        raise NULL_PARAM_ERROR

    def quotient(self, num1, num2):
        if num1 is not None and num2 is not None:
            if num2 == 0:
                raise ValueError("Division by zero error")
            else:
                return num1 / num2
        raise NULL_PARAM_ERROR

    def remainder(self, num1, num2):
        if num1 is not None and num2 is not None:
            if num2 == 0:
                raise ValueError("Division by zero error")
            else:
                return num1 % num2
        raise NULL_PARAM_ERROR

    def log_10(self, num1):
        if num1:
            return log10(num1)
        raise NULL_PARAM_ERROR


    def raiseTo(self, num1, num2):
        return pow(num1, num2)


if __name__ == '__main__':
    values = user_input()
    if values:
        num1, num2 = values
        calculator = Arithmetic()
        print("Adding them: ", calculator.add(num1, num2))
        print("Subtract them: ", calculator.subtract(num1, num2))
        print("Multiply them: ", calculator.product(num1, num2))
        print("Quotient: ", calculator.quotient(num1, num2))
        print("Remainder: ", calculator.remainder(num1, num2))
        print("log_10: ", calculator.log_10(num1))
        print("power: ", calculator.raiseTo(num1, num2))
    else:
        print("Invalid inputs specified. Program cannot continue")