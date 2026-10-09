# 15 · Little Bobby Tables, again

`python` · 🔐 `security` · level ★★☆

> 🤖 **The prompt:** "Look up a user by name in SQLite."

The query reads like English. So does the attacker's.

```python
"""users_db.py: user lookups."""
import sqlite3
from typing import List, Tuple


def find_users(conn: sqlite3.Connection, name: str) -> List[Tuple[int, str]]:
    """Return (id, name) rows whose name matches `name` exactly."""
    query = f"SELECT id, name FROM users WHERE name = '{name}'"
    return conn.execute(query).fetchall()
```

**Would you approve this PR?** Take a minute. Then try to break it.

## Your turn

Fix [`users_db.py`](./users_db.py) so the tests pass. **Don't edit the tests.**

```bash
python tools/check.py 15
```

Want a clean slate? `python tools/check.py --reset 15` restores the original file.

<details>
<summary>💡 Hint</summary>

Print `query` when `name` is `x' OR '1'='1`. What does the database actually receive?

</details>

<details>
<summary>🔓 Spoiler: the bug, and why AI writes it</summary>

Building SQL with an f-string lets user input **rewrite the query** (SQL injection), and it also breaks on honest input like *O'Brien*. Use placeholders (`?` in sqlite3, `%s` in psycopg) and pass the values separately; the driver does the quoting.

LLMs still produce string-built SQL because so many tutorials and old answers in their training data do.

**A fix** (also in [`solutions/15-sql-injection/`](../../solutions/15-sql-injection/))

```python
"""users_db.py: user lookups."""
import sqlite3
from typing import List, Tuple


def find_users(conn: sqlite3.Connection, name: str) -> List[Tuple[int, str]]:
    """Return (id, name) rows whose name matches `name` exactly."""
    return conn.execute("SELECT id, name FROM users WHERE name = ?", (name,)).fetchall()
```

**Go deeper**

- [OWASP Top 10 (2021): A03 Injection](https://owasp.org/Top10/A03_2021-Injection/)
- [CWE-89: SQL Injection](https://cwe.mitre.org/data/definitions/89.html)

</details>
