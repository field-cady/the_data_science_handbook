import unittest
from mymath import fib

class TestFibonacci(unittest.TestCase):
  def test0(self):
    self.assertEqual(0, fib(0))
  def test1(self):
    self.assertEqual(1, fib(1))
  def test2(self):
    self.assertEqual(fib(0)+fib(1), fib(2))
  def test10(self):
    self.assertEqual(fib(8)+fib(9), fib(10))

unittest.main()
