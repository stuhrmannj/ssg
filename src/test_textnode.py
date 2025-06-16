import unittest

from textnode import TextNode, TextType

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

if __name__ == "__main__":
    unittest.main()