import subprocess
import sys
import unittest
from pathlib import Path

from email_check import is_valid_email

HERE = Path(__file__).resolve().parent


class TestIsValidEmail(unittest.TestCase):
    def test_accepts_normal_addresses(self):
        for address in ["alice@example.com", "a.b-c_d@sub.example.co", "x1@y2.org"]:
            self.assertTrue(is_valid_email(address), address)

    def test_rejects_obviously_bad_ones(self):
        for address in ["", "plain", "@example.com", "a@b", "a..b@example.com", "a@example..com", "a b@example.com"]:
            self.assertFalse(is_valid_email(address), address)

    def test_stays_fast_on_hostile_input(self):
        code = "from email_check import is_valid_email; is_valid_email('a' * 64 + '!')"
        try:
            subprocess.run(
                [sys.executable, "-c", code],
                cwd=str(HERE), timeout=3, check=True, capture_output=True,
            )
        except subprocess.TimeoutExpired:
            self.fail("is_valid_email took more than 3 seconds on a 65-character string (catastrophic backtracking)")


if __name__ == "__main__":
    unittest.main()
