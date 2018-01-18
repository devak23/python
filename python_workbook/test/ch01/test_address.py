import unittest

from python_workbook.ch01.p01_address import Address


class TestAddress(unittest.TestCase):

    def test_getting_address_should_not_return_None(self):
        address = Address()
        self.assertIsNotNone(address.get_address())
