import unittest
import htmlnode
import textnode

class TestHTMLNode(unittest.TestCase):
    def test_props_to_html_empty_props(self):
        # Test with None props
        node = htmlnode.HTMLNode("div", "text", None, None)
        self.assertEqual(node.props_to_html(), "")
        
        # Test with empty dict props
        node = htmlnode.HTMLNode("div", "text", None, {})
        self.assertEqual(node.props_to_html(), "")

    def test_props_to_html_with_props(self):
        # Test with single prop
        node = htmlnode.HTMLNode("a", "Click me", None, {"href": "https://example.com"})
        self.assertEqual(node.props_to_html(), ' href="https://example.com"')
        
        # Test with multiple props
        node = htmlnode.HTMLNode(
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
        node = htmlnode.HTMLNode("div", "text", None, {"class": "container"})
        repr_str = repr(node)
        self.assertIsInstance(repr_str, str)
        # Verify

class TestLeafNode(unittest.TestCase):
    def test_to_html_no_value(self):
        # Test that ValueError is raised when value is None
        node = htmlnode.LeafNode("div", None, {"class": "container"})
        with self.assertRaises(ValueError):
            node.to_html() 

    def test_to_html_with_value(self):
        # Test that to_html returns the correct HTML string
        node = htmlnode.LeafNode("div", "text", {"class": "container"})
        self.assertEqual(node.to_html(), '<div class="container">text</div>') 

    def test_to_html_no_tag(self):
        # Test that to_html returns the value when tag is None
        node = htmlnode.LeafNode(None, "text", {"class": "container"})
        self.assertEqual(node.to_html(), "text") 

    def test_leaf_to_html_p(self):
        # Test that to_html returns the correct HTML string for a paragraph
        node = htmlnode.LeafNode("p", "text", {"class": "container"})
        self.assertEqual(node.to_html(), '<p class="container">text</p>')

    def test_leaf_to_html_b(self):
        # Test that to_html returns the correct HTML string for a bold text
        node = htmlnode.LeafNode("b", "text", {"class": "container"})
        self.assertEqual(node.to_html(), '<b class="container">text</b>')

class TestParentNode(unittest.TestCase):
    def test_to_html_no_tag(self):
        # Test that ValueError is raised when tag is None
        node = htmlnode.ParentNode(None, [htmlnode.LeafNode("div", "text")], {"class": "container"})
        with self.assertRaises(ValueError):
            node.to_html() 

    def test_to_html_no_children(self):
        # Test that ValueError is raised when children is None
        node = htmlnode.ParentNode("div", None, {"class": "container"})
        with self.assertRaises(ValueError):
            node.to_html() 

    def test_to_html_empty_children(self):
        # Test that ValueError is raised when children is empty
        node = htmlnode.ParentNode("div", [], {"class": "container"})
        with self.assertRaises(ValueError):
            node.to_html() 

    def test_to_html_with_children(self):
        # Test that to_html returns the correct HTML string
        child1 = htmlnode.LeafNode("p", "text1", {"class": "child"})
        child2 = htmlnode.LeafNode("p", "text2", {"class": "child"})
        node = htmlnode.ParentNode("div", [child1, child2], {"class": "container"})
        expected_html = '<div class="container"><p class="child">text1</p><p class="child">text2</p></div>'
        self.assertEqual(node.to_html(), expected_html)

    def test_to_html_with_grandchildren(self):
        grandchild_node = htmlnode.LeafNode("b", "grandchild")
        child_node = htmlnode.ParentNode("span", [grandchild_node])
        parent_node = htmlnode.ParentNode("div", [child_node])
        self.assertEqual(parent_node.to_html(),"<div><span><b>grandchild</b></span></div>")

    def test_to_html_with_grandchildren_and_props(self):
        grandchild_node = htmlnode.LeafNode("b", "grandchild", {"class": "grandchild"})
        child_node =  htmlnode.ParentNode("span", [grandchild_node], {"class": "child"})
        parent_node =  htmlnode.ParentNode("div", [child_node], {"class": "parent"})
        expected_html = '<div class="parent"><span class="child"><b class="grandchild">grandchild</b></span></div>'
        self.assertEqual(parent_node.to_html(), expected_html)
    
    def test_multiple_children(self):
        child1 =  htmlnode.LeafNode("p", "text1", {"class": "child"})
        child2 =  htmlnode.LeafNode("p", "text2", {"class": "child"})
        node =  htmlnode.ParentNode("div", [child1, child2], {"class": "container"})
        expected_html = '<div class="container"><p class="child">text1</p><p class="child">text2</p></div>'
        self.assertEqual(node.to_html(), expected_html)

    def test_parent_to_html_div(self):
        # Test that to_html returns the correct HTML string for a div
        child_node =  htmlnode.LeafNode("span", "child", {"class": "child"})
        parent_node =  htmlnode.ParentNode("div", [child_node], {"class": "parent"})
        self.assertEqual(parent_node.to_html(), '<div class="parent"><span class="child">child</span></div>')

    def test_parent_to_html_span(self):
        # Test that to_html returns the correct HTML string for a span
        child_node =  htmlnode.LeafNode("b", "child", {"class": "child"})
        parent_node =  htmlnode.ParentNode("span", [child_node], {"class": "parent"})
        self.assertEqual(parent_node.to_html(), '<span class="parent"><b class="child">child</b></span>')

class TestTextNodeToHTMLNode(unittest.TestCase):
    # Test that the text texttype is properly converted to html
    def test_text(self):
        node =  textnode.TextNode("This is a text node", textnode.TextType.TEXT)
        html_node = htmlnode.text_node_to_html_node(node)
        self.assertEqual(html_node.tag, None)
        self.assertEqual(html_node.value, "This is a text node") 
    # Test that the bold texttype is properly converted to html
    def test_bold(self):
        node =  textnode.TextNode("This is a bold node", textnode.TextType.BOLD)
        html_node = htmlnode.text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "b")
        self.assertEqual(html_node.value, "This is a bold node") 
    # Test that the italic texttype is properly converted to html
    def test_italic(self):
        node =  textnode.TextNode("This is an italic node", textnode.TextType.ITALIC)
        html_node = htmlnode.text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "i")
        self.assertEqual(html_node.value, "This is an italic node") 
    # Test that the code texttype is properly converted to html
    def test_code(self):
        node =  textnode.TextNode("This is a code node", textnode.TextType.CODE)
        html_node = htmlnode.text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "code")
        self.assertEqual(html_node.value, "This is a code node") 
    # Test that the link texttype is properly converted to html
    def test_link(self):
        test_link_url = "https://www.google.com"
        node =  textnode.TextNode("This is a link node", textnode.TextType.LINK, test_link_url)
        html_node = htmlnode.text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "a")
        self.assertEqual(html_node.value, "This is a link node") 
        self.assertEqual(html_node.props, {"href":test_link_url})
    # Test that the image texttype is properly converted to html
    def test_image(self):
        test_image_url = "https://www.image_site.com"
        node =  textnode.TextNode("This is an image node", textnode.TextType.IMAGE, test_image_url)
        html_node = htmlnode.text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "img")
        self.assertEqual(html_node.value, "") 
        self.assertEqual(html_node.props, {"src":test_image_url, "alt":"This is an image node"})
    # Test an incorrect texttype
    def test_unknown_type(self):
        node =  textnode.TextNode("This is a text node", textnode.TextType.TEXT)
        node.text_type = "unknown"
        with self.assertRaises(ValueError):
            htmlnode.text_node_to_html_node(node)
    
if __name__ == "__main__":
    unittest.main()    
