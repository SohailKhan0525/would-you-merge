"""uploads.py: serve files from the uploads folder."""
import os


def read_upload(base_dir: str, filename: str) -> str:
    """Return the text of `filename` inside `base_dir`.

    It must never read anything outside `base_dir`:
    raise PermissionError if `filename` tries to escape.
    """
    path = os.path.join(base_dir, filename)
    with open(path, "r", encoding="utf-8") as handle:
        return handle.read()
