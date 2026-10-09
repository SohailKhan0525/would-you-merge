"""discounts.py: pricing helpers."""


def discount_percent(customer: dict, default: int = 10) -> int:
    """Return the customer's custom discount, or `default` if none is set.

    A custom discount of 0 is valid: it means "no discount".
    """
    value = customer.get("discount")
    return default if value is None else value
