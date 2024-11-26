import unittest

from block_markdown import markdown_to_blocks, block_to_block_type, BlockType

class TestBlockMarkdown(unittest.TestCase):
    def test_markdown_to_blocks(self):
        md = """
This is **bolded** paragraph

This is another paragraph with *italic* text and `code` here
This is the same paragraph on a new line

* This is a list
* with items
"""
        blocks = markdown_to_blocks(md)
        self.assertEqual(
            blocks,
            [
                "This is **bolded** paragraph",
                "This is another paragraph with *italic* text and `code` here\nThis is the same paragraph on a new line",
                "* This is a list\n* with items",
            ],
        )

    def test_markdown_to_blocks_newlines(self):
        md = """
This is **bolded** paragraph




This is another paragraph with *italic* text and `code` here
This is the same paragraph on a new line

* This is a list
* with items
"""
        blocks = markdown_to_blocks(md)
        self.assertEqual(
            blocks,
            [
                "This is **bolded** paragraph",
                "This is another paragraph with *italic* text and `code` here\nThis is the same paragraph on a new line",
                "* This is a list\n* with items",
            ],
        )


    def test_block_to_blocktype_heading(self):
        block = """### wow
        This is neat
        """
        self.assertEqual(block_to_block_type(block), BlockType.HEADING)

    def test_block_to_blocktype_code(self):
        block = """```
        wow
        This is code```"""
        self.assertEqual(block_to_block_type(block), BlockType.CODE)

    def test_block_to_blocktype_quote(self):
        block = """> wow
> This is a quote"""
        self.assertEqual(block_to_block_type(block), BlockType.QUOTE)

    def test_block_to_blocktype_unorderedlist(self):
        block = """* wow,
* This is unorderd,
- not neat at all"""
        self.assertEqual(block_to_block_type(block), BlockType.UNORDERED_LIST)

    def test_block_to_blocktype_orderedlist(self):
        block = """1. wow,
2. This is ordered,
3. very neat,
4. nice"""
        self.assertEqual(block_to_block_type(block), BlockType.ORDERED_LIST)

    def test_block_to_blocktype_paragraph(self):
        block = """This is my paragraph
        about nothing at all.
        """
        self.assertEqual(block_to_block_type(block), BlockType.PARAGRAPH)

if __name__ == "__main__":
    unittest.main()
