import unittest

from python_workbook.ch02.even_odd import is_even


class TestEvenOdd(unittest.TestCase):
    def test_is_even_for_an_even_number_should_return_True(self):
        self.assertTrue(is_even(20))

    def test_is_even_for_an_odd_number_should_return_False(self):
        self.assertFalse(is_even(15))

    def test_is_even_for_a_None_number_should_throw_ValueError(self):
        self.assertRaises(ValueError, is_even, None)

    def test_is_even_for_a_negative_even_number_should_return_True(self):
        self.assertTrue(is_even(-34))

    def test_is_even_for_a_negative_odd_number_should_return_False(self):
        self.assertFalse(is_even(-123))

    def test_is_even_for_any_value_other_than_number_should_throw_TypeError(self):
        self.assertRaises(TypeError, is_even, "23")

    def test_is_even_for_a_even_number_with_decimal_point_should_return_False(self):
        self.assertFalse(is_even(13.64))

    def test_is_even_for_an_odd_number_with_decimal_point_should_return_False(self):
        self.assertFalse(is_even(192.13))
