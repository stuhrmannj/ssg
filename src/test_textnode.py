import unittest

from textnode import TextNode, TextType, split_nodes_delimiter

class TestTextNode(unittest.TestCase):
    def test_equality(self):
        node = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is a text node", TextType.BOLD)
        self.assertEqual(node, node2)
    def test_inequality_different_text(self):
        node = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is a different text node", TextType.BOLD)
        self.assertNotEqual(node, node2)
    def test_inequality_different_type(self):
        node = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is a text node", TextType.ITALIC)
        self.assertNotEqual(node, node2)
    def test_inequality_different_text_and_texttype(self):
        node = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is a different text node", TextType.ITALIC)
        self.assertNotEqual(node, node2)
    def test_url_default(self):
        node = TextNode("This is a text node", TextType.BOLD)
        self.assertEqual(node.url, None)
    def test_url_set(self):
        node = TextNode("This is a text node", TextType.BOLD, url="https://example.com")
        self.assertEqual(node.url, "https://example.com")
    def test_texttype_set(self):
        node = TextNode("This is a text node", TextType.BOLD)
        self.assertEqual(node.text_type, TextType.BOLD)
    def test_text_default(self):
        node = TextNode("This is a text node", TextType.BOLD)
        self.assertEqual(node.text, "This is a text node")
    def test_text_set(self):
        node = TextNode("This is a text node", TextType.BOLD)
        node.text = "This is a different text node"
        self.assertEqual(node.text, "This is a different text node")

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

if __name__ == "__main__":
    unittest.main()