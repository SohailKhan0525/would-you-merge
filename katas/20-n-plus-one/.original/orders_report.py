"""orders_report.py: reporting queries."""
import sqlite3
from typing import List, Tuple


def orders_with_customer(conn: sqlite3.Connection) -> List[Tuple[int, str, int]]:
    """Return [(order_id, customer_name, total), ...] ordered by order id.

    Keep it cheap: the number of SQL statements must not grow with the number of orders.
    """
    out = []
    orders = conn.execute("SELECT id, customer_id, total FROM orders ORDER BY id").fetchall()
    for order_id, customer_id, total in orders:
        row = conn.execute("SELECT name FROM customers WHERE id = ?", (customer_id,)).fetchone()
        out.append((order_id, row[0], total))
    return out
