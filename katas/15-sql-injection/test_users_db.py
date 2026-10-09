import sqlite3
import unittest

from users_db import find_users


class TestFindUsers(unittest.TestCase):
    def setUp(self):
        self.conn = sqlite3.connect(":memory:")
        self.conn.execute("CREATE TABLE users (id INTEGER PRIMARY KEY, name TEXT)")
        self.conn.executemany(
            "INSERT INTO users (id, name) VALUES (?, ?)",
            [(1, "alice"), (2, "bob"), (3, "O'Brien")],
        )
        self.conn.commit()

    def tearDown(self):
        self.conn.close()

    def test_finds_an_exact_match(self):
        self.assertEqual(find_users(self.conn, "alice"), [(1, "alice")])

    def test_names_with_apostrophes_work(self):
        self.assertEqual(find_users(self.conn, "O'Brien"), [(3, "O'Brien")])

    def test_quote_tricks_do_not_change_the_query(self):
        self.assertEqual(find_users(self.conn, "x' OR '1'='1"), [])

    def test_unknown_name(self):
        self.assertEqual(find_users(self.conn, "nobody"), [])


if __name__ == "__main__":
    unittest.main()
