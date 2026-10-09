"""audit_log.py: tiny audit trail helper."""
from typing import List


def record_event(event: str, log: List[str] = []) -> List[str]:
    """Append `event` to `log` and return the log.

    If no log is given, start a fresh one.
    """
    log.append(event)
    return log
