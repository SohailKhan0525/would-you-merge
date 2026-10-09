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
