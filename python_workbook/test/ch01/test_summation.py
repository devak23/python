import unittest

from python_workbook.ch01.p07_summation import Summation


class TestSummation(unittest.TestCase):
    def setUp(self):
        self.summation_instance = Summation()

    def test_summation_with_positive_number_gives_correct_result(self):
        self.assertEqual(231, self.summation_instance.summation(21))
        self.assertEqual(1, self.summation_instance.summation(1))

    def test_summation_with_negative_number_gives_None(self):
        self.assertEqual(None, self.summation_instance.summation(-23))
        self.assertEqual(None, self.summation_instance.summation(-1))

    def test_summation_with_None_returns_None(self):
        self.assertEqual(None, self.summation_instance.summation(-23))
        self.assertEqual(None, self.summation_instance.summation(-1))

    def test_summation_with_zero_returns_None(self):
        self.assertEqual(None, self.summation_instance.summation(0))
