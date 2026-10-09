import unittest

from pagination import paginate


class TestPaginate(unittest.TestCase):
    ITEMS = list(range(1, 11))  # 1..10

    def test_first_page(self):
        self.assertEqual(paginate(self.ITEMS, 1, 3), [1, 2, 3])

    def test_middle_page(self):
        self.assertEqual(paginate(self.ITEMS, 2, 3), [4, 5, 6])

    def test_last_page_is_partial(self):
        self.assertEqual(paginate(self.ITEMS, 4, 3), [10])

    def test_page_past_the_end_is_empty(self):
        self.assertEqual(paginate(self.ITEMS, 5, 3), [])

    def test_page_zero_is_rejected(self):
        with self.assertRaises(ValueError):
            paginate(self.ITEMS, 0, 3)

    def test_negative_page_is_rejected(self):
        with self.assertRaises(ValueError):
            paginate(self.ITEMS, -1, 3)

    def test_bad_page_size_is_rejected(self):
        with self.assertRaises(ValueError):
            paginate(self.ITEMS, 1, 0)


if __name__ == "__main__":
    unittest.main()
