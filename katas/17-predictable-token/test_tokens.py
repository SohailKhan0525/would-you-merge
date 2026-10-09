import random
import string
import unittest

from tokens import ALPHABET, new_reset_token


class TestNewResetToken(unittest.TestCase):
    def test_length_and_alphabet(self):
        token = new_reset_token(40)
        self.assertEqual(len(token), 40)
        self.assertTrue(set(token) <= set(ALPHABET) | {"-", "_"})

    def test_default_length(self):
        self.assertEqual(len(new_reset_token()), 32)

    def test_tokens_are_unique(self):
        self.assertEqual(len({new_reset_token() for _ in range(500)}), 500)

    def test_tokens_cannot_be_reproduced_by_seeding_the_global_generator(self):
        random.seed(1234)
        first = new_reset_token()
        random.seed(1234)
        second = new_reset_token()
        self.assertNotEqual(first, second, "the token came from the seedable, predictable PRNG")


if __name__ == "__main__":
    unittest.main()
