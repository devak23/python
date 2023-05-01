def read_user_input():
    a = int(input("Enter First Number : "))
    b = int(input("Enter Second Number : "))
    return a, b


def swap_numbers(a, b):
    b = a + b
    a = b - a
    b = b - a
    return a,b


def main():
    before_swapping = read_user_input()
    print(f"Numbers BEFORE swapping: {before_swapping[0]}, {before_swapping[1]}")
    after_swapping = swap_numbers(before_swapping[0], before_swapping[1])
    print(f"Numbers AFTER  swapping: {after_swapping[0]}, {after_swapping[1]}")


if __name__ == "__main__":
    main()
