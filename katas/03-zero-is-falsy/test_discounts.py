import unittest

from discounts import discount_percent


class TestDiscountPercent(unittest.TestCase):
    def test_custom_discount_wins(self):
        self.assertEqual(discount_percent({"discount": 25}), 25)

    def test_missing_key_uses_default(self):
        self.assertEqual(discount_percent({}), 10)

    def test_none_uses_default(self):
        self.assertEqual(discount_percent({"discount": None}), 10)

    def test_zero_is_a_real_value(self):
        self.assertEqual(discount_percent({"discount": 0}), 0)

    def test_custom_default(self):
        self.assertEqual(discount_percent({}, default=5), 5)


if __name__ == "__main__":
    unittest.main()
