"""email_check.py: signup form validation."""
import re

# local part: alphanumeric runs joined by a *required* single separator,
# so every character can be matched in only one way.
_EMAIL = re.compile(r"^[a-zA-Z0-9]+(?:[._-][a-zA-Z0-9]+)*@(?:[a-zA-Z0-9-]+\.)+[a-zA-Z]{2,}$")


def is_valid_email(value: str) -> bool:
    """Return True for plausible email addresses.

    Keep the accept/reject behaviour (no empty parts, no consecutive dots), but it
    must stay fast on hostile input: a 65-character string may not take seconds.
    """
    return bool(_EMAIL.match(value))
