# Write a program that reads an integer from the user. Then your program should
# display a message indicating whether the integer is even or odd.


def is_even(number):
    if number is None:
        raise ValueError("Number cannot be of null value")

    type_of_num = type(number)

    if not (type_of_num is int or type_of_num is float):
        raise TypeError("Given input is not a number")

    return number % 2 == 0


def read_number():
    try:
        return int(input('Enter an integer value: '))
    except ValueError:
        print('Invalid value entered')


if __name__ == '__main__':
    number = read_number()
    print(f"Is the number {number} even? ", is_even(number))
