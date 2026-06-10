import os
import tempfile
import unittest
from brd_gen_agent.node.parse_files_node import parse_all_files, extract_text


class TestParseFilesNode(unittest.TestCase):
    def setUp(self):
        self.temp_dir = tempfile.TemporaryDirectory()
        self.root = self.temp_dir.name

    def tearDown(self):
        self.temp_dir.cleanup()

    def test_extract_text_reads_text_file(self):
        file_path = os.path.join(self.root, "sample.txt")
        content = "Hello, brd-gen-agent!"
        with open(file_path, "w", encoding="utf-8") as f:
            f.write(content)

        result = extract_text(file_path)
        self.assertEqual(result, content)

    def test_extract_text_unsupported_extension_returns_none(self):
        file_path = os.path.join(self.root, "sample.bin")
        with open(file_path, "wb") as f:
            f.write(b"\x00\x01\x02")

        result = extract_text(file_path)
        self.assertIsNone(result)

    def test_parse_all_files_collects_supported_files(self):
        os.makedirs(os.path.join(self.root, "subdir"), exist_ok=True)
        text_file = os.path.join(self.root, "notes.md")
        other_file = os.path.join(self.root, "subdir", "ignore.bin")

        with open(text_file, "w", encoding="utf-8") as f:
            f.write("# Notes\nThis is a test.")
        with open(other_file, "wb") as f:
            f.write(b"\x00\x01")

        documents = parse_all_files(self.root)
        self.assertEqual(len(documents), 1)
        self.assertEqual(documents[0]["path"], "notes.md")
        self.assertIn("# Notes", documents[0]["content"])


if __name__ == "__main__":
    unittest.main()
