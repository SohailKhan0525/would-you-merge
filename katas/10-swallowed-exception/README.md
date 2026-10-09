# 10 · Everything saved (probably)

`python` · 🙈 `errors` · level ★★☆

> 🤖 **The prompt:** "Save a batch of records. One bad record shouldn't crash the whole batch."

'Robust', says the commit message. Let's see who it's robust *for*.

```python
"""bulk_save.py: save a batch without letting one bad row sink it."""


def save_all(records, db) -> list:
    """Insert every record using `db.insert(record)`.

    One failing record must not stop the others.
    Return the list of records that could NOT be saved (empty list = all saved).
    """
    for record in records:
        try:
            db.insert(record)
        except Exception:
            pass
    return []
```

**Would you approve this PR?** Take a minute. Then try to break it.

## Your turn

Fix [`bulk_save.py`](./bulk_save.py) so the tests pass. **Don't edit the tests.**

```bash
python tools/check.py 10
```

Want a clean slate? `python tools/check.py --reset 10` restores the original file.

<details>
<summary>💡 Hint</summary>

`pass` inside an `except` block says "I'll deal with this later". Who ever does? What does the *caller* believe happened?

</details>

<details>
<summary>🔓 Spoiler: the bug, and why AI writes it</summary>

The function returns "nothing failed" no matter what: errors are swallowed, so the caller (and the user) believes everything was saved. AI code often wraps things in `try/except Exception: pass` to look "robust".

Robustness means **handling** errors (report, retry, roll back, alert), not hiding them. In review, treat any `pass` inside an `except` as a bug until proven otherwise.

**A fix** (also in [`solutions/10-swallowed-exception/`](../../solutions/10-swallowed-exception/))

```python
"""bulk_save.py: save a batch without letting one bad row sink it."""
import logging

log = logging.getLogger(__name__)


def save_all(records, db) -> list:
    """Insert every record using `db.insert(record)`.

    One failing record must not stop the others.
    Return the list of records that could NOT be saved (empty list = all saved).
    """
    failed = []
    for record in records:
        try:
            db.insert(record)
        except Exception:
            log.exception("could not save record %r", record)
            failed.append(record)
    return failed
```

</details>
