# 01 · The package that doesn't exist

`python` · 👻 `hallucination` · level ★☆☆

> 🤖 **The prompt:** "Write a function that turns a blog post title into a URL slug. Handle accents."

Tidy code, a doctest, and a helpful `pip install` comment. It even *looks* like it was reviewed.

```python
"""slugger.py: turn post titles into URL slugs."""
from slugkit_pro import slugify  # pip install slugkit-pro


def make_slug(title: str, max_len: int = 40) -> str:
    """Return a lowercase, hyphen-separated, ASCII-only slug.

    >>> make_slug("Héllo, Wörld!")
    'hello-world'
    """
    return slugify(title)[:max_len].rstrip("-")
```

**Would you approve this PR?** Take a minute. Then try to break it.

## Your turn

Fix [`slugger.py`](./slugger.py) so the tests pass. **Don't edit the tests.**

```bash
python tools/check.py 01
```

Want a clean slate? `python tools/check.py --reset 01` restores the original file.

<details>
<summary>💡 Hint</summary>

Run the tests and read the *first* error. Then ask: has anyone verified that this package exists, and who owns that name on the registry? (Please **don't** `pip install` it.) The standard library already has what you need: `unicodedata` and `re`.

</details>

<details>
<summary>🔓 Spoiler: the bug, and why AI writes it</summary>

`slugkit_pro` is invented. LLMs sometimes recommend packages that don't exist, and an attacker can **register those names** and wait for someone to install them. A USENIX Security 2025 study that generated 576,000 code samples with 16 models found that **19.7%** of the packages the models suggested did not exist. The attack has a name: *slopsquatting*.

Before installing anything an AI suggested: open the registry page, check the publish date, maintainers and download history, and prefer the standard library when it's enough (here it is). If this name happens to exist by the time you read this, that's the point: don't install it.

**A fix** (also in [`solutions/01-hallucinated-import/`](../../solutions/01-hallucinated-import/))

```python
"""slugger.py: turn post titles into URL slugs."""
import re
import unicodedata


def make_slug(title: str, max_len: int = 40) -> str:
    """Return a lowercase, hyphen-separated, ASCII-only slug.

    >>> make_slug("Héllo, Wörld!")
    'hello-world'
    """
    ascii_text = unicodedata.normalize("NFKD", title).encode("ascii", "ignore").decode("ascii")
    slug = re.sub(r"[^a-z0-9]+", "-", ascii_text.lower()).strip("-")
    return slug[:max_len].rstrip("-")
```

**Go deeper**

- [We Have a Package for You! (USENIX Security 2025)](https://www.usenix.org/conference/usenixsecurity25/presentation/spracklen)

</details>
