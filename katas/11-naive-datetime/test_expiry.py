import unittest
from datetime import datetime, timedelta, timezone

from expiry import is_expired

IST = timezone(timedelta(hours=5, minutes=30))
NOW = datetime(2026, 1, 1, 12, 0, tzinfo=timezone.utc)


class TestIsExpired(unittest.TestCase):
    def test_long_past_is_expired(self):
        self.assertTrue(is_expired("2000-01-01T00:00:00+00:00"))

    def test_far_future_is_not_expired(self):
        self.assertFalse(is_expired("2999-01-01T00:00:00+00:00"))

    def test_offsets_are_respected(self):
        # 17:30 in +05:30 is exactly 12:00 UTC, i.e. exactly NOW
        self.assertFalse(is_expired("2026-01-01T17:30:00+05:30", now=NOW))
        self.assertTrue(is_expired("2026-01-01T17:29:59+05:30", now=NOW))

    def test_now_may_be_in_another_timezone(self):
        now_ist = datetime(2026, 1, 1, 17, 30, tzinfo=IST)  # same instant as NOW
        self.assertFalse(is_expired("2026-01-01T12:00:00+00:00", now=now_ist))
        self.assertTrue(is_expired("2026-01-01T11:59:59+00:00", now=now_ist))


if __name__ == "__main__":
    unittest.main()
