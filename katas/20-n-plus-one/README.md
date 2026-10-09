# 20 · Fifty-one queries for fifty orders

`python` · 🐌 `performance` · level ★★★

> 🤖 **The prompt:** "Print each order with its customer's name."

Correct output, readable loop, instant on the three-row demo database.

```python
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
```

**Would you approve this PR?** Take a minute. Then try to break it.

## Your turn

Fix [`orders_report.py`](./orders_report.py) so the tests pass. **Don't edit the tests.**

```bash
python tools/check.py 20
```

Want a clean slate? `python tools/check.py --reset 20` restores the original file.

<details>
<summary>💡 Hint</summary>

Count the SQL statements for 50 orders. Now imagine 5,000 orders and a database that's a network hop away.

</details>

<details>
<summary>🔓 Spoiler: the bug, and why AI writes it</summary>

One query fetches the list, then **one more query per row** fetches the customer: the classic *N+1 query problem*. It is instant on a three-row demo database and painfully slow (and expensive) in production. ORMs hide it behind innocent-looking attribute access.

Fetch what you need in a single `JOIN` (or one `IN (...)` query), and add a query-count assertion to the tests so it can't creep back in. AI-generated code tends to be whatever the *simplest loop* is.

**A fix** (also in [`solutions/20-n-plus-one/`](../../solutions/20-n-plus-one/))

```python
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
```

</details>
