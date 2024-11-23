import unittest

from textnode import TextNode, TextType


class TestTextNode(unittest.TestCase):
    def test_eq(self):
        node = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is a text node", TextType.BOLD)
        self.assertEqual(node, node2)
        self.assertEqual(node.text_type, TextType.BOLD)
        self.assertEqual(node2.text_type, TextType.BOLD)
        self.assertEqual(node.url, None)
        self.assertEqual(node2.url, None)


if __name__ == "__main__":
    unittest.main()
