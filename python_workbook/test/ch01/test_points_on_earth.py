import unittest

from python_workbook.ch01.p12_points_on_earth import PointsOnEarth, LatLong


class TestPointsOnEarth(unittest.TestCase):
    def setUp(self):
        self.poe = PointsOnEarth()

    def test_distance_between_two_distinct_points_result_in_correct_value(self):
        locMumbai = LatLong(19.0760, 72.8777)
        locDelhi = LatLong(28.7041, 77.1025)
        self.assertEqual(7922.409322706468, self.poe.calculate_distance(locMumbai, locDelhi))

    def test_distance_between_two_same_points_result_in_zero(self):
        locMumbai = LatLong(19.0760, 72.8777)
        self.assertEqual(0, self.poe.calculate_distance(locMumbai, locMumbai))

    def test_distance_between_two_points_with_one_being_null_results_in_ValueError(self):
        locMumbai = LatLong(19.0760, 72.8777)
        self.assertRaises(ValueError, self.poe.calculate_distance, None, locMumbai)

    def test_distance_between_two_points_with_negative_longitude_results_in_correct_value(self):
        locStanfordUniv = LatLong(37.427619, -122.166972)
        locHarwardUniv = LatLong(42.3770, 71.1167)
        self.assertEquals(8295.549346729393, self.poe.calculate_distance(locHarwardUniv, locStanfordUniv))

    def test_distance_between_two_points_on_the_same_latitude_results_in_correct_value(self):
        locVaticanCity = LatLong(41.9029, 12.4534)
        locChicago = LatLong(41.9029, 87.6298)
        self.assertEquals(687.1085230005355, self.poe.calculate_distance(locVaticanCity, locChicago))

    def test_distance_between_two_points_on_the_same_longitude_results_in_correct_value(self):
        locDetroit = LatLong(42.3314, 83.0458)
        locLimon = LatLong(9.9913, 83.0415)
        self.assertEquals(5887.923363973593, self.poe.calculate_distance(locDetroit, locLimon))

    def test_distance_between_two_poles_result_in_correct_value(self):
        locNorthPole = LatLong(90,0)
        locSouthPole = LatLong(-90,0)
        self.assertEquals(14095.0562929323, self.poe.calculate_distance(locNorthPole, locSouthPole))
