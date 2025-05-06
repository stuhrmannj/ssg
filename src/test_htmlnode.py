import unittest

from htmlnode import HTMLNode

class TestHTMLNode(unittest.TestCase):
    def test_props_to_html_empty_props(self):
        # Test with None props
        node = HTMLNode("div", "text", None, None)
        self.assertEqual(node.props_to_html(), "")
        
        # Test with empty dict props
        node = HTMLNode("div", "text", None, {})
        self.assertEqual(node.props_to_html(), "")

    def test_props_to_html_with_props(self):
        # Test with single prop
        node = HTMLNode("a", "Click me", None, {"href": "https://example.com"})
        self.assertEqual(node.props_to_html(), ' href="https://example.com"')
        
        # Test with multiple props
        node = HTMLNode(
            "a",
            "Click me",
            None,
            {
                "href": "https://example.com",
                "target": "_blank",
                "class": "link"
            }
        )
        # Note: order in dictionaries is not guaranteed, so we check if each attribute is in the result
        result = node.props_to_html()
        self.assertIn(' href="https://example.com"', result)
        self.assertIn(' target="_blank"', result)
        self.assertIn(' class="link"', result)
        # Also check the total length to ensure no duplicates or extras
        expected_attrs = [' href="https://example.com"', ' target="_blank"', ' class="link"']
        self.assertEqual(len(result), sum(len(attr) for attr in expected_attrs))

    def test_repr_method(self):
        # Test that __repr__ returns a string
        node = HTMLNode("div", "text", None, {"class": "container"})
        repr_str = repr(node)
        self.assertIsInstance(repr_str, str)
        # Verify