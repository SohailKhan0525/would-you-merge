"""audit_log.py: tiny audit trail helper."""
from typing import List, Optional


def record_event(event: str, log: Optional[List[str]] = None) -> List[str]:
    """Append `event` to `log` and return the log.

    If no log is given, start a fresh one.
    """
    if log is None:
        log = []
    log.append(event)
    return log
