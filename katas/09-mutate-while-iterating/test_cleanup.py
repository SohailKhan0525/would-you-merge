import unittest

from cleanup import drop_expired


def make(*expiries):
    return [{"id": i, "expires_at": e} for i, e in enumerate(expiries, start=1)]


class TestDropExpired(unittest.TestCase):
    def test_removes_adjacent_expired_sessions(self):
        sessions = make(1, 2, 3, 100)
        result = drop_expired(sessions, now=10)
        self.assertEqual([s["id"] for s in result], [4])

    def test_keeps_live_sessions_in_order(self):
        sessions = make(100, 5, 200, 7, 300)
        drop_expired(sessions, now=10)
        self.assertEqual([s["id"] for s in sessions], [1, 3, 5])

    def test_modifies_in_place_and_returns_the_same_list(self):
        sessions = make(1, 100)
        self.assertIs(drop_expired(sessions, now=10), sessions)
        self.assertEqual(len(sessions), 1)

    def test_a_session_expiring_exactly_now_is_expired(self):
        self.assertEqual(drop_expired(make(10), now=10), [])


if __name__ == "__main__":
    unittest.main()
