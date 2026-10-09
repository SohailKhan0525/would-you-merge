# 08 · A cent short

`python` · 🧮 `data` · level ★★☆

> 🤖 **The prompt:** "Add up a list of item prices and give me the total in cents."

The totals look right in the demo, and they're off by a cent in production, only sometimes.

```python
"""money.py: cart arithmetic."""
from typing import List


def total_cents(prices: List[float]) -> int:
    """Sum prices given in dollars (e.g. 19.99) and return the total in whole cents."""
    return int(sum(prices) * 100)
```

**Would you approve this PR?** Take a minute. Then try to break it.

## Your turn

Fix [`money.py`](./money.py) so the tests pass. **Don't edit the tests.**

```bash
python tools/check.py 08
```

Want a clean slate? `python tools/check.py --reset 08` restores the original file.

<details>
<summary>💡 Hint</summary>

Print `19.99 * 100`. Why isn't it `1999.0`? And what does `int()` do to `1998.9999999999998`?

</details>

<details>
<summary>🔓 Spoiler: the bug, and why AI writes it</summary>

Binary floating point cannot represent most decimal fractions exactly, and `int()` **truncates**, so a harmless `1e-13` error becomes a whole missing cent. Keep money in integer cents (or `decimal.Decimal`) from the moment it enters your system. If you must convert from floats, **round**, never truncate.

AI-written cart code often sums floats and truncates because the demo values happen to work.

**A fix** (also in [`solutions/08-float-money/`](../../solutions/08-float-money/))

```python
"""money.py: cart arithmetic."""
from typing import List


def total_cents(prices: List[float]) -> int:
    """Sum prices given in dollars (e.g. 19.99) and return the total in whole cents."""
    return sum(round(price * 100) for price in prices)
```

**Go deeper**

- [Python tutorial: floating-point arithmetic](https://docs.python.org/3/tutorial/floatingpoint.html)

</details>
