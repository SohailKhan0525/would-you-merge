# 21 · The email regex that melts your CPU

`python` · 🐌 `performance` · level ★★★

> 🤖 **The prompt:** "Write a regex to validate email addresses on the signup form."

Handles every valid address you try. It's the *invalid* one you didn't try that matters.

```python
"""email_check.py: signup form validation."""
import re

# local part: letters/digits with optional dots, underscores or hyphens in between
_EMAIL = re.compile(r"^([a-zA-Z0-9]+[._-]?)+@([a-zA-Z0-9-]+\.)+[a-zA-Z]{2,}$")


def is_valid_email(value: str) -> bool:
    """Return True for plausible email addresses.

    Keep the accept/reject behaviour (no empty parts, no consecutive dots), but it
    must stay fast on hostile input: a 65-character string may not take seconds.
    """
    return bool(_EMAIL.match(value))
```

**Would you approve this PR?** Take a minute. Then try to break it.

## Your turn

Fix [`email_check.py`](./email_check.py) so the tests pass. **Don't edit the tests.**

```bash
python tools/check.py 21
```

Want a clean slate? `python tools/check.py --reset 21` restores the original file.

<details>
<summary>💡 Hint</summary>

Try `is_valid_email("a" * 30 + "!")`, then 35, then 40, and watch the time. The pattern `([a-z]+[._-]?)+` can split the same run of letters in exponentially many ways.

</details>

<details>
<summary>🔓 Spoiler: the bug, and why AI writes it</summary>

A **nested quantifier** (a repeated group whose contents can repeat, with an *optional* separator) lets the regex engine try exponentially many ways to carve up the input before it finally gives up: **ReDoS**. One crafted request can pin a CPU core.

Make every repetition unambiguous (here: require a separator between groups), keep patterns simple, cap input length, and prefer a vetted parser or library for anything as hairy as email. LLM-written validators are often cloned from the same few over-clever snippets.

**A fix** (also in [`solutions/21-redos-email/`](../../solutions/21-redos-email/))

```python
"""email_check.py: signup form validation."""
import re

# local part: alphanumeric runs joined by a *required* single separator,
# so every character can be matched in only one way.
_EMAIL = re.compile(r"^[a-zA-Z0-9]+(?:[._-][a-zA-Z0-9]+)*@(?:[a-zA-Z0-9-]+\.)+[a-zA-Z]{2,}$")


def is_valid_email(value: str) -> bool:
    """Return True for plausible email addresses.

    Keep the accept/reject behaviour (no empty parts, no consecutive dots), but it
    must stay fast on hostile input: a 65-character string may not take seconds.
    """
    return bool(_EMAIL.match(value))
```

**Go deeper**

- [OWASP: ReDoS](https://owasp.org/www-community/attacks/Regular_expression_Denial_of_Service_-_ReDoS)
- [CWE-1333: Inefficient regular expression complexity](https://cwe.mitre.org/data/definitions/1333.html)

</details>
