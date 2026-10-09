import logging
import unittest

from bulk_save import save_all


class FakeDB:
    def __init__(self, bad_ids=()):
        self.bad_ids = set(bad_ids)
        self.saved = []

    def insert(self, record):
        if record["id"] in self.bad_ids:
            raise ValueError("constraint failed")
        self.saved.append(record["id"])


class TestSaveAll(unittest.TestCase):
    def setUp(self):
        logging.disable(logging.CRITICAL)  # keep the test output clean

    def tearDown(self):
        logging.disable(logging.NOTSET)

    def test_everything_saved(self):
        db = FakeDB()
        failed = save_all([{"id": 1}, {"id": 2}, {"id": 3}], db)
        self.assertEqual(failed, [])
        self.assertEqual(db.saved, [1, 2, 3])

    def test_failures_are_reported_not_hidden(self):
        db = FakeDB(bad_ids={2, 4})
        records = [{"id": i} for i in range(1, 6)]
        failed = save_all(records, db)
        self.assertEqual([r["id"] for r in failed], [2, 4])

    def test_good_records_are_still_saved(self):
        db = FakeDB(bad_ids={2, 4})
        save_all([{"id": i} for i in range(1, 6)], db)
        self.assertEqual(db.saved, [1, 3, 5])


if __name__ == "__main__":
    unittest.main()
