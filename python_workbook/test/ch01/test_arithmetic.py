import unittest

from python_workbook.ch01.p10_arithmetic import Arithmetic


class TestArithmetic(unittest.TestCase):
    def setUp(self):
        self.calc = Arithmetic()
        self.num1 = 25
        self.num2 = 5

    def test_addition_of_two_numbers_with_positive_values_produces_correct_result(self):
        actual = self.calc.add(self.num1, self.num2)
        self.assertEqual(30, actual)

    def test_addition_of_two_numbers_with_negative_values_produces_correct_result(self):
        actual = self.calc.add(-self.num1, -self.num2)
        self.assertEqual(-30, actual)

    def test_addition_of_two_null_numbers_values_raises_value_error(self):
        self.assertRaises(ValueError, self.calc.add, None, None)

    def test_addition_of_any_of_two_numbers_with_one_being_null_values_raises_value_error(self):
        self.assertRaises(ValueError, self.calc.add, 2, None)
        self.assertRaises(ValueError, self.calc.add, None, 2)

    def test_subtraction_of_two_numbers_with_positive_values_produces_correct_result(self):
        actual = self.calc.subtract(self.num1, self.num2)
        self.assertEqual(20, actual)
        actual = self.calc.subtract(self.num2, self.num1)
        self.assertEqual(-20, actual)

    def test_subtraction_of_two_numbers_with_negative_values_produces_correct_result(self):
        actual = self.calc.subtract(-self.num1, -self.num2)
        self.assertEqual(-20, actual)
        actual = self.calc.subtract(-self.num2, -self.num1)
        self.assertEqual(20, actual)

    def test_subtraction_with_null_numbers_produces_ValueError(self):
        self.assertRaises(ValueError, self.calc.subtract, None, None)

    def test_subtraction_with_two_numbers_and_one_being_null_produces_ValueError(self):
        self.assertRaises(ValueError, self.calc.subtract, None, 23)
        self.assertRaises(ValueError, self.calc.subtract, 5, None)

    def test_product_of_two_numbers_with_positive_values_produces_correct_result(self):
        actual = self.calc.product(self.num1, self.num2)
        self.assertEqual(125, actual)

    def test_product_of_two_numbers_with_negative_values_produces_correct_result(self):
        actual = self.calc.product(-self.num1, -self.num2)
        self.assertEqual(125, actual)

    def test_product_with_two_nulls_produces_ValueError(self):
        self.assertRaises(ValueError, self.calc.product, None, None)

    def test_product_with_two_numbers_with_one_being_null_produces_ValueError(self):
        self.assertRaises(ValueError, self.calc.product, 12, None)
        self.assertRaises(ValueError, self.calc.product, None, 23)

    def test_quotient_of_two_numbers_with_positive_values_produces_correct_result(self):
        actual = self.calc.quotient(self.num1, self.num2)
        self.assertEqual(5, actual)

    def test_quotient_of_two_numbers_with_negative_values_produces_correct_result(self):
        actual = self.calc.quotient(-self.num1, -self.num2)
        self.assertEqual(5, actual)

    def test_quotient_of_two_null_numbers_produces_ValueError(self):
        self.assertRaises(ValueError, self.calc.quotient, None, None)

    def test_quotient_of_two_numbers_with_one_being_null_produces_ValueError(self):
        self.assertRaises(ValueError, self.calc.quotient, 12, None)
        self.assertRaises(ValueError, self.calc.quotient, None, 5)

    def test_quotient_of_two_numbers_produces_ValueError_when_the_divisor_is_zero(self):
        self.assertRaises(ValueError, self.calc.quotient, 12, 0)

    def test_remainder_of_two_numbers_with_positive_values_produces_correct_result(self):
        actual = self.calc.remainder(self.num1, self.num2)
        self.assertEqual(0, actual)

    def test_remainder_of_two_numbers_with_negative_values_produces_correct_result(self):
        actual = self.calc.remainder(-self.num1, -self.num2)
        self.assertEqual(0, actual)

    def test_remainder_with_nulls_produces_ValueError(self):
        self.assertRaises(ValueError, self.calc.remainder, None, None)

    def test_remainder_with_two_numbers_and_one_being_null_produces_ValueError(self):
        self.assertRaises(ValueError, self.calc.remainder, 12, None)
        self.assertRaises(ValueError, self.calc.remainder, None, 12)

    def test_remainder_with_zero_as_divisor_produces_ValueError(self):
        self.assertRaises(ValueError, self.calc.remainder, 12, 0)

    def test_log_10_of_a_positive_number_yeilds_correct_result(self):
        actual = self.calc.log_10(self.num1)
        self.assertEqual(1.3979400086720377, actual)

    def test_log_10_of_zero_produces_ValueError(self):
        self.assertRaises(ValueError, self.calc.log_10, 0)

    def test_log_10_of_a_negative_number_yeilds_ValueError(self):
        self.assertRaises(ValueError, self.calc.log_10, -self.num1)

    def test_power_of_two_numbers_with_positive_values_produces_correct_result(self):
        actual = self.calc.raiseTo(self.num1, self.num2)
        self.assertEqual(9765625, actual)

    def test_power_of_two_numbers_with_negative_values_produces_correct_result(self):
        actual = self.calc.raiseTo(self.num1, -self.num2)
        self.assertEqual(1.024e-07, actual)

    def test_power_of_two_numbers_with_exponent_value_zero_produces_unity(self):
        actual = self.calc.raiseTo(self.num1, 0)
        self.assertEqual(1, actual)
