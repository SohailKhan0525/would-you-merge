import unittest

from audit_log import record_event


class TestRecordEvent(unittest.TestCase):
    def test_each_call_without_a_log_starts_fresh(self):
        first = record_event("login")
        second = record_event("logout")
        self.assertEqual(first, ["login"])
        self.assertEqual(second, ["logout"])

    def test_appends_to_a_given_log(self):
        log = ["boot"]
        result = record_event("login", log)
        self.assertEqual(result, ["boot", "login"])
        self.assertIs(result, log)


if __name__ == "__main__":
    unittest.main()
