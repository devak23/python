import unittest

from hangman import *


class TestHangman(unittest.TestCase):

    def setUp(self) -> None:
        self.hangman = Hangman()

    def test_random_selection_when_no_dictionary_is_provided(self):
        word = self.hangman.select_word(None)
        self.assertIsNotNone(word)
        self.assertTrue(word in ['zugzwang', 'position', 'blunder', 'checkmate'])
        print('selected word = {}'.format(word))

    def test_random_selection_when_dictionary_is_provided(self):
        word = self.hangman.select_word(['Abhay', 'Soham'])
        self.assertIsNotNone(word)
        self.assertTrue(word in ['Abhay', 'Soham'])
        print(f'Selected word = {word}')
