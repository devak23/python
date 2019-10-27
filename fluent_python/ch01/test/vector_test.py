import unittest
from vectors import *

class VectorTest(unittest.TestCase):
	def test_hello(self):
		self.assertEqual(hello(), 'hello world')

if __name__ == '__main__':
	vt = VectorTest()
	vt.test_hello()
	print("Done!")