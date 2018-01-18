import unittest
from python_workbook.ch01.p14_height_conversion import HeightConversion, HeightInFeet


class TestHeightConversion(unittest.TestCase):
    def setUp(self):
        self.hc = HeightConversion()

    def test_convert_when_height_passed_is_None_returns_None(self):
        self.assertEqual(None, self.hc.convert(None))

    def test_convert_when_height_passed_is_negative_throws_ValueError(self):
        self.assertRaises(ValueError, self.hc.convert, HeightInFeet(-2,-5))

    def test_convert_when_either_feet_or_inches_is_None_returns_correct_value(self):
        self.assertEqual(152.4, self.hc.convert(HeightInFeet(5, None)))
        self.assertEqual(12.7, self.hc.convert(HeightInFeet(None, 5)))

    def test_convert_when_height_passed_is_zero_returns_zero(self):
        self.assertEqual(0, self.hc.convert(HeightInFeet(0,0)))

    def test_convert_when_height_passed_is_not_a_right_type_throws_TypeError(self):
        self.assertRaises(TypeError, self.hc.convert, ())

    def test_convert_when_height_passed_is_valid_produces_a_valid_result(self):
        self.assertEqual(177.8, self.hc.convert(HeightInFeet(5,10)))
