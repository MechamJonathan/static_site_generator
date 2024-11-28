import unittest
from htmlnode import HTMLNode, LeafNode, ParentNode

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

    def test_to_html_with_children(self):
        child_node = LeafNode("span", "child")
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(parent_node.to_html(), "<div><span>child</span></div>")

    def test_to_html_with_grandchildren(self):
        grandchild_node = LeafNode("b", "grandchild")
        parent_node = ParentNode("span", [grandchild_node])
        grandparent_node = ParentNode("div", [parent_node])
        self.assertEqual(grandparent_node.to_html(), "<div><span><b>grandchild</b></span></div>")
    
    def test_to_html_many_children(self):
        child_node = LeafNode("b", "Bold text")
        child_node2 = LeafNode(None, "Normal text")
        child_node3 = LeafNode("i", "italic text")
        child_node4 = LeafNode(None, "Normal text")
        parent_node = ParentNode("p", [child_node, child_node2, child_node3, child_node4])
        self.assertEqual(parent_node.to_html(), "<p><b>Bold text</b>Normal text<i>italic text</i>Normal text</p>")

    def test_headings(self):
        child_node = LeafNode("b", "Bold text")
        child_node2 = LeafNode(None, "Normal text")
        child_node3 = LeafNode("i", "italic text")
        child_node4 = LeafNode(None, "Normal text")
        parent_node = ParentNode("h2", [child_node, child_node2, child_node3, child_node4])
        self.assertEqual(parent_node.to_html(), "<h2><b>Bold text</b>Normal text<i>italic text</i>Normal text</h2>")

if __name__ == "__main__":
    unittest.main()
