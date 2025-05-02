import random

p = lambda *anything: print(*anything)


def main() -> None:
    user_input = 0
    upper_limit, lower_limit = 1 , 50
    my_number: int = random.randint(upper_limit, lower_limit)

    while True:
        try:
            user_input: int = int(input(f"Guess the number between {upper_limit} and {lower_limit}: "))
        except ValueError:
            p(f"{user_input} is not a valid number. Please try again.")
            continue

        if user_input > my_number:
            p("It's on the higher side")
        elif user_input < my_number:
            p("Its on the lower side")
        else:
            p("You guessed the number!!")
            break

if __name__ == '__main__':
    main()