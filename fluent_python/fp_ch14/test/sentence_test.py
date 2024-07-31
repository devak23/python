import unittest

from fluent_python.fp_ch14.sentence import Sentence


class SentenceTest(unittest.TestCase):
    def test_length(self):
        sentence = Sentence('Fools rush in where angels fear to trade')
        self.assertIsNotNone(len(sentence))
        self.assertEqual(8, len(sentence))

    def test_getitem(self):
        sentence = Sentence('Many hands make light work')
        self.assertTrue(len(sentence) > 0)
        self.assertEqual('Many', sentence[0])

    def test_repr(self):
        sentence = Sentence('Honesty is the best policy')
        self.assertEqual(repr(sentence), 'Sentence(Honesty is the best policy)')

    def test_forloop(self):
        sentence = Sentence("Dont make a mountain of an anthill")
        count = 0
        for _ in sentence:
            count += 1
        self.assertEqual(count, 7)