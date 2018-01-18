import unittest

from python_workbook.ch01.p08_widgets_and_gizmos import WidgetsGizmos, Cart


class TestWidgetsGizmos(unittest.TestCase):
    def setUp(self):
        self.instance = WidgetsGizmos()

    def test_total_weight_of_empty_tuple_with_empty_items_is_zero(self):
        self.assertEqual(0, self.instance.calculate_total_weight(Cart(0, 0)))

    def test_total_weight_of_tuple_with_negative_items_is_None(self):
        self.assertEqual(None, self.instance.calculate_total_weight(Cart(-23, -1)))

    def test_total_weight_of_tuple_with_valid_items_is_valid_result(self):
        self.assertEqual(187, self.instance.calculate_total_weight(Cart(1, 1)))

    def test_total_weight_of_tuple_with_None_input_is_None(self):
        self.assertEqual(None, self.instance.calculate_total_weight(None))

    def test_total_weight_of_tuple_with_None_items_in_it_is_None(self):
        self.assertEqual(None, self.instance.calculate_total_weight(Cart(None, None)))

    def test_total_weight_of_tuple_with_invalid_items_is_None(self):
        self.assertEqual(None, self.instance.calculate_total_weight(Cart(-12, None)))
        self.assertEqual(None, self.instance.calculate_total_weight(Cart(None, 2)))
        self.assertEqual(None, self.instance.calculate_total_weight(Cart(-12, 23)))
        self.assertEqual(None, self.instance.calculate_total_weight(Cart(23, -23)))

    def test_total_weight_of_tuple_with_wrong_type_raises_TypeError(self):
        self.assertRaises(TypeError, self.instance.calculate_total_weight, (3, 4))
