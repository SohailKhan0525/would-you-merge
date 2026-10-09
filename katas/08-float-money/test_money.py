import unittest

from money import total_cents


class TestTotalCents(unittest.TestCase):
    def test_simple_total(self):
        self.assertEqual(total_cents([10.00, 5.50]), 1550)

    def test_nineteen_ninety_nine(self):
        self.assertEqual(total_cents([19.99]), 1999)

    def test_twenty_nine_cents(self):
        self.assertEqual(total_cents([0.29]), 29)

    def test_more_awkward_prices(self):
        self.assertEqual(total_cents([0.57]), 57)
        self.assertEqual(total_cents([1.13]), 113)

    def test_refund_line(self):
        self.assertEqual(total_cents([20.00, -0.29]), 1971)

    def test_empty_cart(self):
        self.assertEqual(total_cents([]), 0)


if __name__ == "__main__":
    unittest.main()
