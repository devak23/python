import unittest

from python_workbook.ch01.p11_fuel_efficiency import FuelEfficiency


class TestFuelEfficiency(unittest.TestCase):
    def setUp(self):
        self.fe = FuelEfficiency()

    def test_conversion_to_mpg_when_mileage_is_zero_produces_zero_result(self):
        self.assertEqual(0, self.fe.convert_to_miles_per_gallon(0))

    def test_conversion_to_mpg_when_mileage_is_negative_raises_ValueError(self):
        self.assertRaises(ValueError, self.fe.convert_to_miles_per_gallon, -12)

    def test_conversion_to_mpg_when_mileage_is_valid_produces_correct_result(self):
        self.assertEqual(79.9731, self.fe.convert_to_miles_per_gallon(34))

    def test_conversion_to_kpl_when_mileage_is_zero_produces_zero_result(self):
        self.assertEqual(0, self.fe.convert_to_kilometers_per_litre(0))

    def test_conversion_to_kpl_when_mileage_is_negative_raises_ValueError(self):
        self.assertRaises(ValueError, self.fe.convert_to_kilometers_per_litre, -34)

    def test_conversion_to_kpl_when_mileage_is_valid_produces_valid_result(self):
        self.assertEqual(5.101368, self.fe.convert_to_kilometers_per_litre(12.0))