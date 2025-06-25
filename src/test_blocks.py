import unittest
from blocks import *

class TestMarkdownToBlocks(unittest.TestCase):
    def test_markdown_to_blocks(self):
        md = """
This is **bolded** paragraph

This is another paragraph with _italic_ text and `code` here
This is the same paragraph on a new line

- This is a list
- with items
"""
        blocks = markdown_to_blocks(md)
        self.assertEqual(
            blocks,
            [
                "This is **bolded** paragraph",
                "This is another paragraph with _italic_ text and `code` here\nThis is the same paragraph on a new line",
                "- This is a list\n- with items",
            ],
        ) 

    def test_empty_markdown_to_blocks(self):
        md = ""
        blocks = markdown_to_blocks(md)
        self.assertEqual(
            blocks,
            [],
        ) 

    def test_one_block_markdown_to_blocks(self):
        md = """
This is **bolded** paragraph
This is another paragraph with _italic_ text and `code` here
This is the same paragraph on a new line
- This is a list
- with items
"""
        blocks = markdown_to_blocks(md)
        self.assertEqual(
            blocks,
            [
                "This is **bolded** paragraph\nThis is another paragraph with _italic_ text and "
                "`code` here\nThis is the same paragraph on a new line\n- This is a list\n- with items"
            ],
        ) 

    def test_multiple_blank_lines_markdown_to_blocks(self):
        md = """
This is **bolded** paragraph




This is another paragraph with _italic_ text and `code` here
This is the same paragraph on a new line




- This is a list
- with items
"""
        blocks = markdown_to_blocks(md)
        self.assertEqual(
            blocks,
            [
                "This is **bolded** paragraph",
                "This is another paragraph with _italic_ text and `code` here\nThis is the same paragraph on a new line",
                "- This is a list\n- with items",
            ],
        ) 

    def test_multiple_start_and_end_blank_lines_markdown_to_blocks(self):
        md = """


This is **bolded** paragraph

This is another paragraph with _italic_ text and `code` here
This is the same paragraph on a new line

- This is a list
- with items


"""
        blocks = markdown_to_blocks(md)
        self.assertEqual(
            blocks,
            [
                "This is **bolded** paragraph",
                "This is another paragraph with _italic_ text and `code` here\nThis is the same paragraph on a new line",
                "- This is a list\n- with items",
            ],
        ) 

    def test_extra_spaces_markdown_to_blocks(self):
        md = """
            This is **bolded** paragraph

                  This is another paragraph with _italic_ text and `code` here
This is the same paragraph on a new line

       - This is a list
- with items
"""
        blocks = markdown_to_blocks(md)
        self.assertEqual(
            blocks,
            [
                "This is **bolded** paragraph",
                "This is another paragraph with _italic_ text and `code` here\nThis is the same paragraph on a new line",
                "- This is a list\n- with items",
            ],
        ) 

class TestBlockToBlockType(unittest.TestCase):
    def test_paragraph(self):
        block = "This is just a regular paragraph of text. It doesn't start with any special character."
        self.assertEqual(block_to_block_type(block), BlockType.PARAGRAPH)
        
    def test_heading(self):
        block = "## This is a heading"
        self.assertEqual(block_to_block_type(block), BlockType.HEADING)
        
    def test_code(self):
        block = '```print("Hello, Boot.dev!")```'
        self.assertEqual(block_to_block_type(block), BlockType.CODE)

    def test_quote(self):
        block = """> Success is not final,
> failure is not fatal."""
        self.assertEqual(block_to_block_type(block), BlockType.QUOTE)

    def test_ulist(self):
        block = """- apples
- bananas
- oranges"""
        self.assertEqual(block_to_block_type(block), BlockType.ULIST)

    def test_olist(self):
        block = """1. First item
2. Second item
3. Third item"""
        self.assertEqual(block_to_block_type(block), BlockType.OLIST)

    def test_wrong_heading(self):
        block = "####### This is a heading"
        self.assertEqual(block_to_block_type(block), BlockType.PARAGRAPH)

    def test_wrong_code(self):
        block = '``print("Hello, Boot.dev!")```'
        self.assertEqual(block_to_block_type(block), BlockType.PARAGRAPH)

    def test_wrong_quote(self):
        block = """> Success is not final,
 failure is not fatal."""
        self.assertEqual(block_to_block_type(block), BlockType.PARAGRAPH)

    def test_wrong_ulist(self):
        block = """- apples
- bananas
* oranges"""
        self.assertEqual(block_to_block_type(block), BlockType.PARAGRAPH)
    
    def test_wrong_olist(self):
        block = """1. First item
2. Second item
4. Third item"""
        self.assertEqual(block_to_block_type(block), BlockType.PARAGRAPH)
    
if __name__ == "__main__":
    unittest.main()