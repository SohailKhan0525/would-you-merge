"""expiry.py: is an invite link still valid?"""
from datetime import datetime, timezone
from typing import Optional


def is_expired(expires_at: str, now: Optional[datetime] = None) -> bool:
    """`expires_at` is ISO-8601 *with* a UTC offset, e.g. '2030-01-01T00:00:00+00:00'.

    Return True only if that instant is strictly before `now`
    (`now` defaults to the current time).
    """
    now = now or datetime.now(timezone.utc)
    return datetime.fromisoformat(expires_at) < now
