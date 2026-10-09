import os
import tempfile
import unittest

from uploads import read_upload


def write(path, text):
    with open(path, "w", encoding="utf-8") as handle:
        handle.write(text)


class TestReadUpload(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        root = self.tmp.name
        self.base = os.path.join(root, "uploads")
        os.makedirs(os.path.join(self.base, "sub"))
        sibling = os.path.join(root, "uploads_private")
        os.makedirs(sibling)
        self.secret = os.path.join(root, "secret.txt")
        write(os.path.join(self.base, "notes.txt"), "hello")
        write(os.path.join(self.base, "sub", "a.txt"), "nested")
        write(self.secret, "top secret")
        write(os.path.join(sibling, "x.txt"), "private")

    def tearDown(self):
        self.tmp.cleanup()

    def test_reads_a_normal_file(self):
        self.assertEqual(read_upload(self.base, "notes.txt"), "hello")

    def test_reads_a_file_in_a_subfolder(self):
        self.assertEqual(read_upload(self.base, os.path.join("sub", "a.txt")), "nested")

    def test_dotdot_escape_is_refused(self):
        with self.assertRaises(PermissionError):
            read_upload(self.base, os.path.join("..", "secret.txt"))

    def test_absolute_path_is_refused(self):
        with self.assertRaises(PermissionError):
            read_upload(self.base, self.secret)

    def test_dotdot_in_the_middle_is_refused(self):
        with self.assertRaises(PermissionError):
            read_upload(self.base, os.path.join("sub", "..", "..", "secret.txt"))

    def test_sibling_folder_with_the_same_prefix_is_refused(self):
        with self.assertRaises(PermissionError):
            read_upload(self.base, os.path.join("..", "uploads_private", "x.txt"))


if __name__ == "__main__":
    unittest.main()
