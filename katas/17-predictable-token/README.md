# 17 · An unguessable token (if you can't guess the seed)

`python` · 🔐 `security` · level ★★☆

> 🤖 **The prompt:** "Generate a password-reset token for a user."

32 random-looking characters. What could be more secure than *random*?

```python
"""tokens.py: password-reset tokens."""
import random
import string

ALPHABET = string.ascii_letters + string.digits


def new_reset_token(length: int = 32) -> str:
    """Return an unguessable token for a password-reset link."""
    return "".join(random.choice(ALPHABET) for _ in range(length))
```

**Would you approve this PR?** Take a minute. Then try to break it.

## Your turn

Fix [`tokens.py`](./tokens.py) so the tests pass. **Don't edit the tests.**

```bash
python tools/check.py 17
```

Want a clean slate? `python tools/check.py --reset 17` restores the original file.

<details>
<summary>💡 Hint</summary>

Does the `random` module's generator have a *seed*? What does it mean for security if the same seed always produces the same tokens?

</details>

<details>
<summary>🔓 Spoiler: the bug, and why AI writes it</summary>

`random` is a Mersenne Twister: fast, statistically fine, and **completely predictable** from its internal state. Seed it twice and you get the same stream; observe enough outputs and an attacker can reconstruct the state and predict the *next* reset token.

Security tokens need a cryptographically secure generator: `secrets.choice` / `secrets.token_urlsafe` in Python, `crypto.randomBytes` in Node. LLMs write `random.choice(...)` for tokens all the time because that's what most "generate a random string" snippets use.

**A fix** (also in [`solutions/17-predictable-token/`](../../solutions/17-predictable-token/))

```python
"""tokens.py: password-reset tokens."""
import secrets
import string

ALPHABET = string.ascii_letters + string.digits


def new_reset_token(length: int = 32) -> str:
    """Return an unguessable token for a password-reset link."""
    return "".join(secrets.choice(ALPHABET) for _ in range(length))
```

**Go deeper**

- [Python docs: secrets](https://docs.python.org/3/library/secrets.html)
- [CWE-338: Weak PRNG](https://cwe.mitre.org/data/definitions/338.html)

</details>
