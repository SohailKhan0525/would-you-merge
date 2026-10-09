"""slugger.py: turn post titles into URL slugs."""
from slugkit_pro import slugify  # pip install slugkit-pro


def make_slug(title: str, max_len: int = 40) -> str:
    """Return a lowercase, hyphen-separated, ASCII-only slug.

    >>> make_slug("Héllo, Wörld!")
    'hello-world'
    """
    return slugify(title)[:max_len].rstrip("-")
