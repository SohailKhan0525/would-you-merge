# 11 · Expired in a different timezone

`python` · 🧮 `data` · level ★★☆

> 🤖 **The prompt:** "Check whether an invite link has expired. Expiry timestamps are stored as ISO-8601 UTC."

One comparison, two different clocks. Python refuses to compare them, which is the *good* outcome.

```python
"""expiry.py: is an invite link still valid?"""
from datetime import datetime
from typing import Optional


def is_expired(expires_at: str, now: Optional[datetime] = None) -> bool:
    """`expires_at` is ISO-8601 *with* a UTC offset, e.g. '2030-01-01T00:00:00+00:00'.

    Return True only if that instant is strictly before `now`
    (`now` defaults to the current time).
    """
    now = now or datetime.now()
    return datetime.fromisoformat(expires_at) < now
```

**Would you approve this PR?** Take a minute. Then try to break it.

## Your turn

Fix [`expiry.py`](./expiry.py) so the tests pass. **Don't edit the tests.**

```bash
python tools/check.py 11
```

Want a clean slate? `python tools/check.py --reset 11` restores the original file.

<details>
<summary>💡 Hint</summary>

In a REPL, run `datetime.fromisoformat('2030-01-01T00:00:00+00:00') < datetime.now()` and read the error message.

</details>

<details>
<summary>🔓 Spoiler: the bug, and why AI writes it</summary>

Python separates *aware* datetimes (they carry an offset) from *naive* ones (they don't) and refuses to compare them. The AI compared an aware timestamp with `datetime.now()`, which is naive **local** time.

Even where a naive comparison doesn't crash, it silently mixes local time and UTC, the classic "works on my laptop, off by 5½ hours in production" bug. Keep everything timezone-aware and use `datetime.now(timezone.utc)`. (`datetime.utcnow()` is deprecated since Python 3.12 for the same reason: it returns a naive object.)

**A fix** (also in [`solutions/11-naive-datetime/`](../../solutions/11-naive-datetime/))

```python
"""expiry.py: is an invite link still valid?"""
from datetime import datetime, timezone
from typing import Optional


def is_expired(expires_at: str, now: Optional[datetime] = None) -> bool:
    """`expires_at` is ISO-8601 *with* a UTC offset, e.g. '2030-01-01T00:00:00+00:00'.

    Return True only if that instant is strictly before `now`
    (`now` defaults to the current time).
    """
    now = now or datetime.now(timezone.utc)
    return datetime.fromisoformat(expires_at) < now
```

**Go deeper**

- [Python docs: aware and naive objects](https://docs.python.org/3/library/datetime.html#aware-and-naive-objects)

</details>
