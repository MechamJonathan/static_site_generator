import unittest
from main import extract_title

class main(unittest.TestCase):
    def test_exctract_title(self):
        header = extract_title("# Header")
        self.assertEqual(header, "Header")

    def test_extract_no_title(self):
        with self.assertRaises(Exception) as context:
            extract_title("Header")
        self.assertEqual(str(context.exception), "no header found")

if __name__ == "__main__":
    unittest.main()
