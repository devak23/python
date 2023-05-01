#!/usr/bin/python

def enter_upper_limit():
    """
    this function accepts user input and assigns it to the upper_limit variable
    """
    upper_limit = -1
    try:
        upper_limit = int(input("Enter a number (upper limit): "))
    except ValueError:
        print("Invalid number passed")
    return upper_limit


def is_prime(number=0):
    """
    this function identifies if a number is a prime number or not.
    """
    if number == 2 or number == 3 or number == 5 or number == 7:
        return True

    if number % 2 == 0 or number % 3 == 0 or number % 5 == 0 or number % 7 == 0:
        return False
    else:
        return True


def generate_all_primes(upper_limit):
    """
    This function loops from 0 to upper_limit and tries to identify the numbers that are prime
    """
    if upper_limit <= 0:
        return None
    else:
        all_primes = [2, 3, 5, 7]
        for number in range(9, upper_limit + 1, 2):
            if is_prime(number):
                all_primes.append(number)
        return all_primes


def main():
    upper_limit = enter_upper_limit()
    all_primes = generate_all_primes(upper_limit)
    if all_primes:
        print(f"Total {len(all_primes)} found: {all_primes}")
    else:
        print("Invalid upper limit provided. Program cannot execute.")
    pass


if __name__ == '__main__':
    main()
