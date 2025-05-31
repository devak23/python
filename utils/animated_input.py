import sys
import threading
import time


def pg_input(prompt: str, total: int = 30) -> str:
    """Shows a progress bar animation before prompting for input."""

    print()  # start on a new line
    for i in range(total + 1):
        sys.stdout.write(f"\r[{('█' * i).ljust(total)}] {i * 100 // total} %")
        sys.stdout.flush()
        time.sleep(0.1)

    print()  # new line after all that.
    return input(prompt)


# Some points regarding line# 11:

# 1. \r`: This is a carriage return. It moves the cursor back to the beginning of the current line in the terminal,
# allowing overwriting the previously printed line. This avoids printing new lines with each update (so the progress
# bar animates in place). If this is removed, the progressbar would be printed like this:
# [          ] 0 %
# [█         ] 10 %
# [██        ] 20 %
# [███       ] 30 %
# [████      ] 40 %
# [█████     ] 50 %
# [██████    ] 60 %
# [███████   ] 70 %
# [████████  ] 80 %
# [█████████ ] 90 %
# [██████████] 100 %

# 2. '█' * i`: This creates a string of `i` "blocks" (or "steps") to represent the progress visually. As i increases
# with each iteration, more blocks are added to the progress bar.
# 3. ljust(total): This ensures the string is total characters long by adding spaces to the right of the "█"
# characters if needed. Without this, the progress bar length would fluctuate, causing a messy visual output.
# 4. {i * 100 // total}: This calculates the percentage of completion, based on the current iteration step (i)
# divided by the total steps. For example, at halfway (i = total // 2), this will display 50 for 50%.
# 5. f"[{...}] ...%": This formats the entire progress bar into a neat string. For example, if total=10 and i=5,
# you might see the progressbar load up 50% like this:
#  [█████     ] 50 %


# The text 'prompt' gets typed out and erased repeatedly before being shown statically.
def deleting_input(prompt: str, delay=0.04, iterations=2) -> str:
    """ Repeatedly types and deletes part of the text."""

    for _ in range(iterations):
        for i in range(1, len(prompt) + 1):
            sys.stdout.write(f"\r{prompt[:i]}")  # Type one character at a time
            sys.stdout.flush()
            time.sleep(delay)

        time.sleep(0.08)  # Pause after typing the whole text

        for i in range(len(prompt), 0, -1):
            sys.stdout.write(f"\r{' ' * i}\r")  # clear the character one at a time
            sys.stdout.flush()
            time.sleep(delay)

    return input(prompt)


def spin_input(prompt: str) -> str:
    """Print prompt with a spinner animation while waiting for input."""
    spinner_running = True

    def spinner():
        while spinner_running:
            for cursor in "|/-\\":
                sys.stdout.write(f"\r{prompt} {cursor}")
                sys.stdout.flush()
                time.sleep(0.1)

    # start the spinner thread in a separate thread
    spinner_thread = threading.Thread(target=spinner)
    spinner_thread.start()

    # Wait for the user input
    user_input = input(f"\r{prompt}")
    spinner_running = False  # stop the spinner
    spinner_thread.join()  # Ensure thread stops properly
    return user_input


def animated_message(prompt: str, delay: float = 0.04) -> None:
    for char in prompt:
        sys.stdout.write(char)
        time.sleep(delay)
        sys.stdout.flush()


def animated_input(prompt: str, delay: float = 0.04) -> str:
    animated_message(prompt, delay)
    return input()


def dots_input(prompt, duration=3):
    """Displays a loading dots animation while waiting for user input."""
    dots_running = True

    def loading_dots():
        while dots_running:
            for i in range(4):
                sys.stdout.write(f"\r{prompt}{'.' * i}   ")  # Add dots
                sys.stdout.flush()
                time.sleep(0.5)

    # Start loading dots in a separate thread
    dots_thread = threading.Thread(target=loading_dots)
    dots_thread.start()

    # Wait for user input
    user_input = input(f"\r{prompt}")
    dots_running = False
    dots_thread.join()  # Stop the animation
    return user_input


def main(type: str):
    if type == 'ai':
        animated_message('Press enter to continue.', delay=0.1)
        choice = animated_input("Would you like to play a game of chess (Y/N): ", delay=0.1)

        if choice == "Y" or choice == "y":
            animated_message("You will lose, after all I am AI. Who can beat me?")
        else:
            animated_message("Indeed! Smart choice. You dont want to cross swords with me!")

    if type == 'pi':
        user_input = pg_input("Enter something after loading: ")
        animated_message(f"That didn't make a lot of sense to me. Have you visited a doctor regarding this?")

    if type == 'si':
        user_input = spin_input("Processing, enter your name: ")
        print(f"Hello, {user_input}!")

    if type == 'di':
        user_input = deleting_input("Enter your message to the world: ")
        print(f"You said: {user_input} to the whole world!")

    if type == 'doi':
        user_input = dots_input("Loading, enter your place of birth: ")
        print(f"Wow, You were born in {user_input}! Me too!! ")

if __name__ == '__main__':
    main('doi')
