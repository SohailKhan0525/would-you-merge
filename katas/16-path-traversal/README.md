# 16 · Download anything

`python` · 🔐 `security` · level ★★☆

> 🤖 **The prompt:** "Write a function to read a user's uploaded file by name from the uploads folder."

`os.path.join` is *right there* and it's the 'safe' way to build paths. Right?

```python
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
```

**Would you approve this PR?** Take a minute. Then try to break it.

## Your turn

Fix [`uploads.py`](./uploads.py) so the tests pass. **Don't edit the tests.**

```bash
python tools/check.py 16
```

Want a clean slate? `python tools/check.py --reset 16` restores the original file.

<details>
<summary>💡 Hint</summary>

What is `os.path.join('/srv/uploads', '../secret.txt')`? And what does `os.path.join('/srv/uploads', '/etc/passwd')` return?

</details>

<details>
<summary>🔓 Spoiler: the bug, and why AI writes it</summary>

`os.path.join` doesn't confine anything: `..` segments climb out of the folder, and an **absolute second argument replaces the base entirely**. Resolve the final path (`os.path.realpath`) and verify it is still inside the base directory using `os.path.commonpath`, **not** `str.startswith` (which wrongly accepts `/srv/uploads_private`).

Even better: never use user-supplied names as paths. Store files under server-generated IDs.

**A fix** (also in [`solutions/16-path-traversal/`](../../solutions/16-path-traversal/))

```python
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
```

**Go deeper**

- [OWASP: Path Traversal](https://owasp.org/www-community/attacks/Path_Traversal)
- [CWE-22: Path Traversal](https://cwe.mitre.org/data/definitions/22.html)

</details>
