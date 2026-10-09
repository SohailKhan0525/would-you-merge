import unittest

from slugger import make_slug


class TestMakeSlug(unittest.TestCase):
    def test_basic(self):
        self.assertEqual(make_slug("Hello, World!"), "hello-world")

    def test_accents_are_flattened(self):
        self.assertEqual(make_slug("Héllo, Wörld!"), "hello-world")

    def test_runs_of_separators_collapse(self):
        self.assertEqual(make_slug("  Rust  &  Go --- friends  "), "rust-go-friends")

    def test_truncation_never_leaves_a_trailing_hyphen(self):
        self.assertEqual(make_slug("alpha beta gamma delta", max_len=11), "alpha-beta")

    def test_nothing_sluggable(self):
        self.assertEqual(make_slug("!!!"), "")


if __name__ == "__main__":
    unittest.main()
