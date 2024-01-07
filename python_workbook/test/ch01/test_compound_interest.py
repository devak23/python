import unittest

from python_workbook.ch01.p09_compound_interest2 import CompoundInterest


class TestCompoundInterest(unittest.TestCase):
    def setUp(self):
        self.instance = CompoundInterest()

    def test_compound_interest_for_negative_inputs_results_in_None(self):
        pass

    def test_compound_interest_for_zero_rate_of_interest_is_same_as_principal(self):
        pass

    def test_compound_interest_for_zero_compounding_factor_returns_None(self):
        pass

    def test_compound_interest_for_zero_number_of_years_returns_a_valid_amount(self):
        pass

    def test_compound_interest_for_zero_principal_returns_zero(self):
        pass

    def test_compound_interest_for_valid_inputs_results_in_valid_value(self):
        pass
