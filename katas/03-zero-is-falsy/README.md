# 03 · The discount that wouldn't be zero

`python` · 🧠 `logic` · level ★☆☆

> 🤖 **The prompt:** "Return the discount percentage for a customer. Use 10% if they don't have a custom one."

Passes every example that uses a 'normal' value. Quiet bugs love defaults.

```python
"""discounts.py: pricing helpers."""


def discount_percent(customer: dict, default: int = 10) -> int:
    """Return the customer's custom discount, or `default` if none is set.

    A custom discount of 0 is valid: it means "no discount".
    """
    return customer.get("discount") or default
```

**Would you approve this PR?** Take a minute. Then try to break it.

## Your turn

Fix [`discounts.py`](./discounts.py) so the tests pass. **Don't edit the tests.**

```bash
python tools/check.py 03
```

Want a clean slate? `python tools/check.py --reset 03` restores the original file.

<details>
<summary>💡 Hint</summary>

What does `0 or 10` evaluate to? And what should a customer who was *explicitly* given `0` receive?

</details>

<details>
<summary>🔓 Spoiler: the bug, and why AI writes it</summary>

`or` treats **every** falsy value (`0`, `0.0`, `""`, `[]`) as "missing". A customer who opted out of discounts (`0`) is handed the 10% default instead. Use `is None` when `0` is a legitimate value.

AI assistants reach for `x or default` constantly because it's short and idiomatic for strings. The bug only appears for the one value nobody put in the demo.

**A fix** (also in [`solutions/03-zero-is-falsy/`](../../solutions/03-zero-is-falsy/))

```python
"""discounts.py: pricing helpers."""


def discount_percent(customer: dict, default: int = 10) -> int:
    """Return the customer's custom discount, or `default` if none is set.

    A custom discount of 0 is valid: it means "no discount".
    """
    value = customer.get("discount")
    return default if value is None else value
```

</details>
