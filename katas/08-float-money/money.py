"""money.py: cart arithmetic."""
from typing import List


def total_cents(prices: List[float]) -> int:
    """Sum prices given in dollars (e.g. 19.99) and return the total in whole cents."""
    return int(sum(prices) * 100)
