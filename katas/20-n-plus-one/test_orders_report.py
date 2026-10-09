import sqlite3
import unittest

from orders_report import orders_with_customer


class TestOrdersWithCustomer(unittest.TestCase):
    def setUp(self):
        self.conn = sqlite3.connect(":memory:")
        self.conn.executescript(
            """
            CREATE TABLE customers (id INTEGER PRIMARY KEY, name TEXT NOT NULL);
            CREATE TABLE orders (id INTEGER PRIMARY KEY, customer_id INTEGER NOT NULL, total INTEGER NOT NULL);
            """
        )
        self.conn.executemany("INSERT INTO customers VALUES (?, ?)", [(1, "Asha"), (2, "Ben"), (3, "Chen")])
        self.conn.executemany(
            "INSERT INTO orders VALUES (?, ?, ?)",
            [(i, (i % 3) + 1, i * 100) for i in range(1, 51)],
        )
        self.conn.commit()

    def tearDown(self):
        self.conn.close()

    def test_result_is_correct(self):
        rows = orders_with_customer(self.conn)
        self.assertEqual(len(rows), 50)
        self.assertEqual(rows[0], (1, "Ben", 100))
        self.assertEqual(rows[2], (3, "Asha", 300))
        self.assertEqual([r[0] for r in rows], list(range(1, 51)))

    def test_does_not_run_one_query_per_order(self):
        statements = []
        self.conn.set_trace_callback(statements.append)
        orders_with_customer(self.conn)
        self.conn.set_trace_callback(None)
        self.assertLessEqual(len(statements), 2, "%d SQL statements for 50 orders" % len(statements))


if __name__ == "__main__":
    unittest.main()
