import unittest

from htmlnode import HTMLNode, LeafNode


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


    def test_to_html_no_children(self):
        node = LeafNode("p", "this is a paragraph of text.")
        self.assertEqual(node.to_html(), "<p>this is a paragraph of text.</p>")

        node2 = LeafNode("a", "Click me!", {"href": "https://www.google.com"})
        self.assertEqual(node2.to_html(), "<a href=\"https://www.google.com\">Click me!</a>")
    
    def test_to_html_no_tag(self):
        node = LeafNode(None, "oops")
        self.assertEqual(node.to_html(), "oops")

if __name__ == "__main__":
    unittest.main()
