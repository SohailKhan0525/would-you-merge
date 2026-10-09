"""tokens.py: password-reset tokens."""
import secrets
import string

ALPHABET = string.ascii_letters + string.digits


def new_reset_token(length: int = 32) -> str:
    """Return an unguessable token for a password-reset link."""
    return "".join(secrets.choice(ALPHABET) for _ in range(length))
