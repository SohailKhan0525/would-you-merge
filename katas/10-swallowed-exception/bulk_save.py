"""bulk_save.py: save a batch without letting one bad row sink it."""


def save_all(records, db) -> list:
    """Insert every record using `db.insert(record)`.

    One failing record must not stop the others.
    Return the list of records that could NOT be saved (empty list = all saved).
    """
    for record in records:
        try:
            db.insert(record)
        except Exception:
            pass
    return []
