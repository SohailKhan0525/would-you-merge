# 02 · Page one goes missing

`python` · 📏 `boundaries` · level ★☆☆

> 🤖 **The prompt:** "Write a paginate helper for my API. Pages start at 1."

Every list endpoint has one of these. Arithmetic that *looks* right gets skimmed past in review.

```python
"""pagination.py: slice a list into pages for an API response."""
from typing import List, Sequence, TypeVar

T = TypeVar("T")


def paginate(items: Sequence[T], page: int, per_page: int) -> List[T]:
    """Return the items on `page` (pages are numbered from 1).

    - page 1 holds the first `per_page` items
    - a page past the end returns an empty list
    - page < 1 or per_page < 1 raises ValueError
    """
    if per_page < 1:
        raise ValueError("per_page must be >= 1")
    start = page * per_page
    return list(items[start:start + per_page])
```

**Would you approve this PR?** Take a minute. Then try to break it.

## Your turn

Fix [`pagination.py`](./pagination.py) so the tests pass. **Don't edit the tests.**

```bash
python tools/check.py 02
```

Want a clean slate? `python tools/check.py --reset 02` restores the original file.

<details>
<summary>💡 Hint</summary>

The docstring says pages are numbered from 1. Which index does page 1 start at? Then re-read the validation rules: does anything enforce *all* of them?

</details>

<details>
<summary>🔓 Spoiler: the bug, and why AI writes it</summary>

`start = page * per_page` treats pages as 0-based, so page 1 silently skips the first page of data. The docstring also promises a `ValueError` for `page < 1`, but nothing enforces it, and Python slicing is forgiving: `page=-1` just returns `[]`.

LLMs mix 0-based indices and 1-based page numbers because both conventions are everywhere in their training data. When you review pagination, always check the **first item, the last item, one past each end**, and the invalid inputs.

**A fix** (also in [`solutions/02-pagination-off-by-one/`](../../solutions/02-pagination-off-by-one/))

```python
"""pagination.py: slice a list into pages for an API response."""
from typing import List, Sequence, TypeVar

T = TypeVar("T")


def paginate(items: Sequence[T], page: int, per_page: int) -> List[T]:
    """Return the items on `page` (pages are numbered from 1).

    - page 1 holds the first `per_page` items
    - a page past the end returns an empty list
    - page < 1 or per_page < 1 raises ValueError
    """
    if per_page < 1:
        raise ValueError("per_page must be >= 1")
    if page < 1:
        raise ValueError("page must be >= 1")
    start = (page - 1) * per_page
    return list(items[start:start + per_page])
```

</details>
