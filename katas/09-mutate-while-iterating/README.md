# 09 · Every other expired session

`python` · 🧠 `logic` · level ★★☆

> 🤖 **The prompt:** "Remove expired sessions from the list."

Clean, readable, three lines. It works until two expired sessions sit next to each other.

```python
"""cleanup.py: session housekeeping."""


def drop_expired(sessions: list, now: int) -> list:
    """Remove every session whose `expires_at` is <= `now`, in place.

    Returns the same list object, for convenience.
    """
    for session in sessions:
        if session["expires_at"] <= now:
            sessions.remove(session)
    return sessions
```

**Would you approve this PR?** Take a minute. Then try to break it.

## Your turn

Fix [`cleanup.py`](./cleanup.py) so the tests pass. **Don't edit the tests.**

```bash
python tools/check.py 09
```

Want a clean slate? `python tools/check.py --reset 09` restores the original file.

<details>
<summary>💡 Hint</summary>

Add a `print(session["id"])` inside the loop and run it on three expired sessions in a row. Which ones does the loop actually visit?

</details>

<details>
<summary>🔓 Spoiler: the bug, and why AI writes it</summary>

Removing items from a list while iterating over it shifts everything left, so the loop **skips the element right after each removal**: adjacent expired sessions survive.

Build a new list (a comprehension) and assign it into the slice (`sessions[:] = ...`) when callers rely on in-place mutation. The same family of bug exists in JavaScript (`splice` inside `forEach`) and Java (`ConcurrentModificationException`).

**A fix** (also in [`solutions/09-mutate-while-iterating/`](../../solutions/09-mutate-while-iterating/))

```python
"""cleanup.py: session housekeeping."""


def drop_expired(sessions: list, now: int) -> list:
    """Remove every session whose `expires_at` is <= `now`, in place.

    Returns the same list object, for convenience.
    """
    sessions[:] = [s for s in sessions if s["expires_at"] > now]
    return sessions
```

</details>
