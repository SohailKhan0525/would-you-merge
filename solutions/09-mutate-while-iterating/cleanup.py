"""cleanup.py: session housekeeping."""


def drop_expired(sessions: list, now: int) -> list:
    """Remove every session whose `expires_at` is <= `now`, in place.

    Returns the same list object, for convenience.
    """
    sessions[:] = [s for s in sessions if s["expires_at"] > now]
    return sessions
