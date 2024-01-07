#!/usr/bin/python

import random

import readchar

from game_stats import GameStats

dictionary = ['zugzwang', 'position', 'blunder', 'checkmate']


def read_input():
    """ This will take the user input each and every time and validate if it matches the required text """
    print('Please provide your next best guess (CTRL + C to break): ')
    return repr(readchar.readchar())


def banner():
    print("---------------------------------------------------------")
    print("-                H A N G M A N                          -")
    print("---------------------------------------------------------")
    print()


def select_word(my_dict):
    """ Randomly select a word to play """
    return random.choice(dictionary if my_dict is None or len(my_dict) == 0 else my_dict)


class Hangman:
    def __init__(self, word):
        self.stats = GameStats(word)

    def play_game(self):
        """ this controls the actual execution of the game """
        print("The word for you to guess is: ")
        self.stats.print_status()

        while self.stats.update(read_input()) > 0:
            self.stats.print_status()

        if self.stats.won():
            print("CONGRATULATIONS!!! ... YOU WON!")
        print("Done!")


if __name__ == '__main__':
    banner()
    selected_word = select_word(None)
    print(selected_word)
    h = Hangman(selected_word)
    h.play_game()
