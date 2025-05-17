def is_prime(number: int) -> bool:
    if number < 2: # numbers less than 2 are not prime
        return False

    for i in range(2, int(number ** 0.5) + 1):
        # check for numbers which can divide up to sqrt(number)
        if number % i == 0:
            return False

    return True


print(f'is number 10 prime? {is_prime(10)}')

prime_numbers = [i for i in range(1, 101) if is_prime(i)]

print(f'prime numbers: {prime_numbers}')