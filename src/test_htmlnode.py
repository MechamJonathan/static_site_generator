import unittest

from htmlnode import HTMLNode


class TestHTMLNode(unittest.TestCase):
    def test_to_html_props(self):
        node = HTMLNode(
            "div",
            "Hello, world!",
            None,
            {"class": "greeting", "href": "https://boot.dev"},
        )
        self.assertEqual(
            node.props_to_html(),
            ' class="greeting" href="https://boot.dev"',
        )

    def test_values(self):
        node = HTMLNode("div", "I don't like sand")
        self.assertEqual(node.tag, "div")
        self.assertEqual(node.value, "I don't like sand")
        self.assertEqual(node.children, None)
        self.assertEqual(node.props, None)

    def test_repr(self):
        node = HTMLNode("p", "oh great", None, {"class: primary"})
        self.assertEqual(node.__repr__(), "HTMLNode(p, oh great, children: None, {'class: primary'})")

if __name__ == "__main__":
    unittest.main()
