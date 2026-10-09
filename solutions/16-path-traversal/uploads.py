"""uploads.py: serve files from the uploads folder."""
import os


def read_upload(base_dir: str, filename: str) -> str:
    """Return the text of `filename` inside `base_dir`.

    It must never read anything outside `base_dir`:
    raise PermissionError if `filename` tries to escape.
    """
    base = os.path.realpath(base_dir)
    path = os.path.realpath(os.path.join(base, filename))
    try:
        inside = os.path.commonpath([base, path]) == base
    except ValueError:  # e.g. different drives on Windows
        inside = False
    if not inside:
        raise PermissionError("path escapes the upload directory")
    with open(path, "r", encoding="utf-8") as handle:
        return handle.read()
