import unittest
from inline_markdown import split_nodes_delimiter, extract_markdown_images, extract_markdown_links, split_nodes_image, split_nodes_link
from textnode import TextNode, TextType

class TestSplitDelimeter(unittest.TestCase):
    def test_code_block(self):
        node = TextNode("This is text with a `code block` word", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "`", TextType.CODE)
        self.assertEqual(new_nodes, [TextNode("This is text with a ", TextType.TEXT), 
                                     TextNode("code block", TextType.CODE),
                                     TextNode(" word", TextType.TEXT),
        ])

    def test_bold_text(self):
        node = TextNode("This is a **bold** word", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "**", TextType.BOLD)
        self.assertEqual(new_nodes, [
            TextNode("This is a ", TextType.TEXT),
            TextNode("bold", TextType.BOLD),
            TextNode(" word", TextType.TEXT),
        ])
    
    def test_itallic(self):
        node = TextNode("This is text with an *italic* word", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "*", TextType.ITALIC)
        self.assertEqual(new_nodes, [TextNode("This is text with an ", TextType.TEXT), 
                                     TextNode("italic", TextType.ITALIC),
                                     TextNode(" word", TextType.TEXT),
        ])

    def test_delim_bold_and_italic(self):
        node = TextNode("**bold** and *italic*", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "**", TextType.BOLD)
        new_nodes = split_nodes_delimiter(new_nodes, "*", TextType.ITALIC)
        self.assertListEqual(new_nodes, [TextNode("bold", TextType.BOLD),
                                        TextNode(" and ", TextType.TEXT),
                                        TextNode("italic", TextType.ITALIC),
        ])

    def test_delim_bold_multiword(self):
        node = TextNode(
            "This is text with a **bolded word** and **another**", TextType.TEXT
        )
        new_nodes = split_nodes_delimiter([node], "**", TextType.BOLD)
        self.assertListEqual(new_nodes, [TextNode("This is text with a ", TextType.TEXT),
                                        TextNode("bolded word", TextType.BOLD),
                                        TextNode(" and ", TextType.TEXT),
                                        TextNode("another", TextType.BOLD),
        ])

    def test_delim_bold_double(self):
        node = TextNode(
            "This is text with a **bolded** word and **another**", TextType.TEXT
        )
        new_nodes = split_nodes_delimiter([node], "**", TextType.BOLD)
        self.assertListEqual(new_nodes, [TextNode("This is text with a ", TextType.TEXT),
                                        TextNode("bolded", TextType.BOLD),
                                        TextNode(" word and ", TextType.TEXT),
                                        TextNode("another", TextType.BOLD),
        ])


class TestExtractingLinksAndImages(unittest.TestCase):
    def test_extract_image(self):  
        text = "This is text with a ![rick roll](https://i.imgur.com/aKaOqIh.gif) and ![obi wan](https://i.imgur.com/fJRm4Vk.jpeg)"
        self.assertEqual(extract_markdown_images(text), [("rick roll", "https://i.imgur.com/aKaOqIh.gif"), ("obi wan", "https://i.imgur.com/fJRm4Vk.jpeg")])

    def test_extract_link(self):
        text = "This is text with a link [to boot dev](https://www.boot.dev) and [to youtube](https://www.youtube.com/@bootdotdev)"
        self.assertEqual(extract_markdown_links(text), [("to boot dev", "https://www.boot.dev"), ("to youtube", "https://www.youtube.com/@bootdotdev")])

    def test_split_multiple_image(self):
        node = TextNode(
            "Here is an image of a bear ![bear](https://www.example.com/bear.jpg) and another one ![wizard](https://www.example.com/wizard.jpg)",
            TextType.TEXT,
        )
        self.assertEqual(split_nodes_image([node]), [
            TextNode("Here is an image of a bear ", TextType.TEXT),
            TextNode("bear", TextType.IMAGE, "https://www.example.com/bear.jpg"),
            TextNode(" and another one ", TextType.TEXT),
            TextNode("wizard", TextType.IMAGE, "https://www.example.com/wizard.jpg"),
        ])
    
    def test_split_single_image(self):
        node = TextNode(
            "The lone image ![stars](https://www.example.com/stars.jpg) shines in darkness.",
            TextType.TEXT,
        )
        self.assertEqual(split_nodes_image([node]), [
            TextNode("The lone image ", TextType.TEXT),
            TextNode("stars", TextType.IMAGE, "https://www.example.com/stars.jpg"),
            TextNode(" shines in darkness.", TextType.TEXT),
        ])
    
    def test_split_no_images(self):
        node = TextNode(
            "This text has no images, only plain words and sentences.",
            TextType.TEXT,
        )
        self.assertEqual(split_nodes_image([node]), [
            TextNode("This text has no images, only plain words and sentences.", TextType.TEXT),
        ])

    def test_split_single_link(self):
        node = TextNode(
            "This is text with a link [to boot dev](https://www.boot.dev) and [to youtube](https://www.youtube.com/@bootdotdev)",
            TextType.TEXT,
        )
        self.assertEqual(split_nodes_link([node]), [
            TextNode("This is text with a link ", TextType.TEXT),
            TextNode("to boot dev", TextType.LINK, "https://www.boot.dev"),
            TextNode(" and ", TextType.TEXT),
            TextNode(
                "to youtube", TextType.LINK, "https://www.youtube.com/@bootdotdev"
            ),
        ])

    def test_split_single_link(self):
        node = TextNode(
            "Visit [Boot.dev](https://www.boot.dev) for programming practice",
            TextType.TEXT,
        )
        self.assertEqual(split_nodes_link([node]), [
            TextNode("Visit ", TextType.TEXT),
            TextNode("Boot.dev", TextType.LINK, "https://www.boot.dev"),
            TextNode(" for programming practice", TextType.TEXT)
        ])
    
    def test_split_no_links(self):
        node = TextNode(
            "This is plain text with no links",
            TextType.TEXT,
        )
        self.assertEqual(split_nodes_link([node]), [
            TextNode("This is plain text with no links", TextType.TEXT)
        ])



if __name__ == "__main__":
    unittest.main()