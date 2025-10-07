import unittest
from pkg.calculator import Calculator


class TestCalculator(unittest.TestCase):
    def setUp(self):
        self.calculator = Calculator()

    def test_addition(self):
        result = self.calculator.evaluate("3 + 5")
        self.assertEqual(result, 8)

    def test_subtraction(self):
        result = self.calculator.evaluate("10 - 4")
        self.assertEqual(result, 6)

    def test_multiplication(self):
        result = self.calculator.evaluate("3 * 4")
        self.assertEqual(result, 12)

    def test_division(self):
        result = self.calculator.evaluate("10 / 2")
        self.assertEqual(result, 5)

    def test_nested_expression(self):
        result = self.calculator.evaluate("3 * 4 + 5")
        self.assertEqual(result, 17)

    def test_complex_expression(self):
        result = self.calculator.evaluate("2 * 3 - 8 / 2 + 5")
        self.assertEqual(result, 7)

    def test_empty_expression(self):
        result = self.calculator.evaluate("")
        self.assertIsNone(result)

    def test_invalid_operator(self):
        with self.assertRaises(ValueError):
            self.calculator.evaluate("$ 3 5")

    def test_not_enough_operands(self):
        with self.assertRaises(ValueError):
            self.calculator.evaluate("+ 3")

    def test_logarithm_base_10(self):
        result = self.calculator.evaluate("log 100")
        self.assertEqual(result, 2.0)

    def test_natural_logarithm(self):
        result = self.calculator.evaluate("ln 2.71828")
        self.assertAlmostEqual(result, 1.0, places=4)

    def test_logarithm_base_2(self):
        result = self.calculator.evaluate("log2 8")
        self.assertEqual(result, 3.0)

    def test_logarithm_with_expression(self):
        result = self.calculator.evaluate("log 100 + 3")
        self.assertEqual(result, 5.0)

    def test_logarithm_expression_order(self):
        result = self.calculator.evaluate("3 + log 100")
        self.assertEqual(result, 5.0)

    def test_multiple_logarithms(self):
        result = self.calculator.evaluate("log 100 + ln 2.71828")
        self.assertAlmostEqual(result, 3.0, places=4)

    def test_logarithm_of_zero(self):
        with self.assertRaises(ValueError):
            self.calculator.evaluate("log 0")

    def test_logarithm_of_negative(self):
        with self.assertRaises(ValueError):
            self.calculator.evaluate("log -1")


if __name__ == "__main__":
    unittest.main()