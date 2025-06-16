import unittest
from textnode import *
from misc_functions import *

class TestSplitNodeDelimiter(unittest.TestCase):
    # test for inline code block text
    def test_inline_code_text(self):
        node = TextNode("This is text with a `code block` word", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "`", TextType.CODE)
        new_node_1 = TextNode("This is text with a ", TextType.TEXT)
        new_node_2 = TextNode("code block", TextType.CODE)
        new_node_3 = TextNode(" word", TextType.TEXT)
        self.assertEqual(new_nodes, [new_node_1, new_node_2, new_node_3])
    # test for inline bold block text
    def test_inline_bold_text(self):
        node = TextNode("This is text with a **bold block** word", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "**", TextType.BOLD)
        new_node_1 = TextNode("This is text with a ", TextType.TEXT)
        new_node_2 = TextNode("bold block", TextType.BOLD)
        new_node_3 = TextNode(" word", TextType.TEXT)
        self.assertEqual(new_nodes, [new_node_1, new_node_2, new_node_3])
    # test for inline italic block text
    def test_inline_italic_text(self):
        node = TextNode("This is text with a *italic block* word", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "*", TextType.ITALIC)
        new_node_1 = TextNode("This is text with a ", TextType.TEXT)
        new_node_2 = TextNode("italic block", TextType.ITALIC)
        new_node_3 = TextNode(" word", TextType.TEXT)
        self.assertEqual(new_nodes, [new_node_1, new_node_2, new_node_3])
    # test for nodes that are not TextType.TEXT
    def test_nodes_not_texttype_text(self):
        node = TextNode("This is not a text type node", TextType.BOLD)
        new_nodes = split_nodes_delimiter([node], "**", TextType.BOLD)
        self.assertEqual(new_nodes, [node])
    # test for text node with no occurrence of the delimiter
    def test_nodes_with_no_delimiter(self):
        node = TextNode("This node does not have the declared delimiter", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "*", TextType.ITALIC)
        self.assertEqual(new_nodes, [node])
    # test for text node contains the delimiter at the beginning or end
    def test_nodes_delimiter_on_edges(self):
        node = TextNode("**This node has the bold delimiter on its edges**", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "**", TextType.BOLD)
        updated_node = TextNode("This node has the bold delimiter on its edges", TextType.BOLD)
        self.assertEqual(new_nodes, [updated_node])
    # test for multiple sets of the same delimiter
    def test_multiple_same_delimiters(self):
        node = TextNode("This **node** has the **bold** delimiter on its edges", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "**", TextType.BOLD)
        node_1 = TextNode("This ", TextType.TEXT)
        node_2 = TextNode("node", TextType.BOLD)
        node_3 = TextNode(" has the ", TextType.TEXT)
        node_4 = TextNode("bold", TextType.BOLD)
        node_5 = TextNode(" delimiter on its edges", TextType.TEXT)
        self.assertEqual(new_nodes, [node_1, node_2, node_3, node_4, node_5])

class TestExtractMarkdownImages(unittest.TestCase):
    def test_extract_markdown_image(self):
        matches = extract_markdown_images("This is text with an ![image](https://i.imgur.com/zjjcJKZ.png)")
        self.assertListEqual([("image", "https://i.imgur.com/zjjcJKZ.png")], matches) 

    def test_no_image(self):
        matches = extract_markdown_images("This is text with no image.")
        self.assertListEqual([], matches) 

    def test_no_alt_text(self):
        matches = extract_markdown_images("This is text with missing alt text ![](https://i.imgur.com/zjjcJKZ.png)")
        self.assertListEqual([("", "https://i.imgur.com/zjjcJKZ.png")], matches)

    def test_multiple_images(self):
        matches = extract_markdown_images("Here is ![one](url1.png) and ![two](url2.png)")
        self.assertListEqual([("one", "url1.png"), ("two", "url2.png")], matches)
    
    def test_link_not_image(self):
        matches = extract_markdown_images("Here is [notanimage](https://www.boot.dev)")
        self.assertListEqual([], matches)
    
    def test_special_characters_image(self):
        matches = extract_markdown_images("This is text with special characters ![special.image](https://i.imgur.com/zjjcJKZ.png)")
        self.assertListEqual([("special.image", "https://i.imgur.com/zjjcJKZ.png")], matches)


class TestExtractMarkdownLinks(unittest.TestCase):
    def test_extract_markdown_link(self):
        matches = extract_markdown_links("This is text with a link [to boot dev](https://www.boot.dev)")
        self.assertListEqual([("to boot dev", "https://www.boot.dev")], matches) 
    
    def test_no_link(self):
        matches = extract_markdown_links("This is text with no link.")
        self.assertListEqual([], matches) 
    
    def test_no_anchor_text(self):
        matches = extract_markdown_links("This is text with missing anchor text [](https://www.boot.dev)")
        self.assertListEqual([("", "https://www.boot.dev")], matches)

    def test_multiple_links(self):
        matches = extract_markdown_links("Here is [one](https://www.boot.dev) and [two](https://www.google.com)")
        self.assertListEqual([("one", "https://www.boot.dev"), ("two", "https://www.google.com")], matches)
    
    def test_image_not_link(self):
        matches = extract_markdown_links("Here is ![notalink](image.png)")
        self.assertListEqual([], matches)

    def test_special_characters_link(self):
        matches = extract_markdown_links("This is text with special characters [to boot.dev](https://www.boot.dev)")
        self.assertListEqual([("to boot.dev", "https://www.boot.dev")], matches)

if __name__ == "__main__":
    unittest.main()