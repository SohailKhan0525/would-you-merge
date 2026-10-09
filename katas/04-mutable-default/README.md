# 04 · The log that remembers everything

`python` · 🧠 `logic` · level ★☆☆

> 🤖 **The prompt:** "Add a helper that records an audit event, optionally into an existing log list."

Works perfectly the first time you call it. That's the problem.

```python
"""audit_log.py: tiny audit trail helper."""
from typing import List


def record_event(event: str, log: List[str] = []) -> List[str]:
    """Append `event` to `log` and return the log.

    If no log is given, start a fresh one.
    """
    log.append(event)
    return log
```

**Would you approve this PR?** Take a minute. Then try to break it.

## Your turn

Fix [`audit_log.py`](./audit_log.py) so the tests pass. **Don't edit the tests.**

```bash
python tools/check.py 04
```

Want a clean slate? `python tools/check.py --reset 04` restores the original file.

<details>
<summary>💡 Hint</summary>

Call `record_event("a")` and then `record_event("b")` and print both results. *When* is the default value `[]` created?

</details>

<details>
<summary>🔓 Spoiler: the bug, and why AI writes it</summary>

Default argument values are evaluated **once**, when the function is *defined*, not on every call, so every call that omits `log` shares the same list. Use `None` as the default and create the list inside the function.

Linters catch this one (`ruff` rule `B006`, `flake8-bugbear`), which is a good argument for running a linter over AI-generated code before you read it.

**A fix** (also in [`solutions/04-mutable-default/`](../../solutions/04-mutable-default/))

```python
"""audit_log.py: tiny audit trail helper."""
from typing import List, Optional


def record_event(event: str, log: Optional[List[str]] = None) -> List[str]:
    """Append `event` to `log` and return the log.

    If no log is given, start a fresh one.
    """
    if log is None:
        log = []
    log.append(event)
    return log
```

**Go deeper**

- [Python tutorial: default argument values](https://docs.python.org/3/tutorial/controlflow.html#default-argument-values)

</details>
