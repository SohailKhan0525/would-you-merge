"""cleanup.py: session housekeeping."""


def drop_expired(sessions: list, now: int) -> list:
    """Remove every session whose `expires_at` is <= `now`, in place.

    Returns the same list object, for convenience.
    """
    for session in sessions:
        if session["expires_at"] <= now:
            sessions.remove(session)
    return sessions
