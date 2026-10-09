# 12 · Tenant A's database host, now with Tenant B

`python` · 🧮 `data` · level ★★☆

> 🤖 **The prompt:** "Make a per-tenant config from the defaults without changing the defaults."

It *says* `.copy()`, so the defaults are safe. Aren't they?

```python
"""config_merge.py: per-tenant configuration."""

DEFAULTS = {"db": {"host": "localhost", "port": 5432}, "debug": False}


def tenant_config(overrides: dict) -> dict:
    """Return a NEW config: DEFAULTS with `overrides` applied.

    Nested dicts are merged, not replaced. DEFAULTS itself must never change.
    """
    config = DEFAULTS.copy()
    for key, value in overrides.items():
        if isinstance(value, dict) and isinstance(config.get(key), dict):
            config[key].update(value)
        else:
            config[key] = value
    return config
```

**Would you approve this PR?** Take a minute. Then try to break it.

## Your turn

Fix [`config_merge.py`](./config_merge.py) so the tests pass. **Don't edit the tests.**

```bash
python tools/check.py 12
```

Want a clean slate? `python tools/check.py --reset 12` restores the original file.

<details>
<summary>💡 Hint</summary>

Call `tenant_config({'db': {'host': 'x'}})`, then print `DEFAULTS`. Which objects does `dict.copy()` actually duplicate?

</details>

<details>
<summary>🔓 Spoiler: the bug, and why AI writes it</summary>

`dict.copy()` is a **shallow** copy: the new dict *shares* its nested dicts with the original. So `config[key].update(...)` writes straight into `DEFAULTS`, and one tenant's override leaks into every later tenant.

Use `copy.deepcopy`, or build new nested dicts while merging. It's a nasty one because the first call looks perfect; the damage only shows on the *second* call.

**A fix** (also in [`solutions/12-shallow-copy/`](../../solutions/12-shallow-copy/))

```python
"""config_merge.py: per-tenant configuration."""
import copy

DEFAULTS = {"db": {"host": "localhost", "port": 5432}, "debug": False}


def tenant_config(overrides: dict) -> dict:
    """Return a NEW config: DEFAULTS with `overrides` applied.

    Nested dicts are merged, not replaced. DEFAULTS itself must never change.
    """
    config = copy.deepcopy(DEFAULTS)
    for key, value in overrides.items():
        if isinstance(value, dict) and isinstance(config.get(key), dict):
            config[key].update(value)
        else:
            config[key] = value
    return config
```

</details>
