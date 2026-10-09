"""orders_report.py: reporting queries."""
import sqlite3
from typing import List, Tuple


def orders_with_customer(conn: sqlite3.Connection) -> List[Tuple[int, str, int]]:
    """Return [(order_id, customer_name, total), ...] ordered by order id.

    Keep it cheap: the number of SQL statements must not grow with the number of orders.
    """
    rows = conn.execute(
        "SELECT o.id, c.name, o.total "
        "FROM orders AS o JOIN customers AS c ON c.id = o.customer_id "
        "ORDER BY o.id"
    ).fetchall()
    return [(order_id, name, total) for order_id, name, total in rows]
