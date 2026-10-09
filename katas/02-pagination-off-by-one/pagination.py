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
