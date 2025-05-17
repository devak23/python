import sys
import time

def animated_message(prompt: str, delay: float = 0.04):
    for char in prompt:
        sys.stdout.write(char)
        time.sleep(delay)
        sys.stdout.flush()


def animated_input(prompt: str, delay: float = 0.04):
    animated_message(prompt, delay)
    return input()


def main():
    animated_message('Press enter to continue.', delay=0.1)
    choice = animated_input("Would you like to play a game of chess (Y/N): ", delay=0.1)

    if choice == "Y" or choice == "y":
        animated_message("You will lose, after all I am AI. Who can beat me?")
    else:
        animated_message("Indeed! Smart choice. You dont want to cross swords with me!")


if __name__ == '__main__':
    main()