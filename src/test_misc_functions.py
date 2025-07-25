import unittest
from textnode import *
from misc_functions import *
from blocks import *

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
        node = TextNode("This is text with a _italic block_ word", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "_", TextType.ITALIC)
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

class TestSplitNodesImage(unittest.TestCase):
    def test_split_images(self):
        node = TextNode("This is text with an ![image](https://i.imgur.com/zjjcJKZ.png) and another ![second image](https://i.imgur.com/3elNhQu.png) and text at the end", TextType.TEXT)
        new_nodes = split_nodes_image([node])
        self.assertListEqual([TextNode("This is text with an ", TextType.TEXT),
                TextNode("image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png"),
                TextNode(" and another ", TextType.TEXT),
                TextNode("second image", TextType.IMAGE, "https://i.imgur.com/3elNhQu.png"),
                TextNode(" and text at the end", TextType.TEXT)], new_nodes) 
    
    def test_no_images(self):
        node = TextNode("This is text with no images", TextType.TEXT)
        new_nodes = split_nodes_image([node])
        self.assertListEqual([TextNode("This is text with no images", TextType.TEXT)], new_nodes)
    
    def test_image_at_beginning(self):
        node = TextNode("![image](https://i.imgur.com/zjjcJKZ.png) image at the beginning", TextType.TEXT)
        new_nodes = split_nodes_image([node])
        self.assertListEqual([TextNode("image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png"),
                TextNode(" image at the beginning", TextType.TEXT)], new_nodes)
    
    def test_image_at_end(self):
        node = TextNode("image at the end ![image](https://i.imgur.com/zjjcJKZ.png)", TextType.TEXT)
        new_nodes = split_nodes_image([node])
        self.assertListEqual([TextNode("image at the end ", TextType.TEXT), 
                              TextNode("image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png")], new_nodes)

    def test_back_to_back_images(self):
        node = TextNode("This is text with back-to-back images ![image](https://i.imgur.com/zjjcJKZ.png)![second image](https://i.imgur.com/3elNhQu.png) and text at the end", TextType.TEXT)
        new_nodes = split_nodes_image([node])
        self.assertListEqual([TextNode("This is text with back-to-back images ", TextType.TEXT),
                TextNode("image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png"),
                TextNode("second image", TextType.IMAGE, "https://i.imgur.com/3elNhQu.png"),
                TextNode(" and text at the end", TextType.TEXT)], new_nodes) 

    def test_one_image(self):
        node = TextNode("This is text with an ![image](https://i.imgur.com/zjjcJKZ.png) and text at the end", TextType.TEXT)
        new_nodes = split_nodes_image([node])
        self.assertListEqual([TextNode("This is text with an ", TextType.TEXT),
                TextNode("image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png"),
                TextNode(" and text at the end", TextType.TEXT)], new_nodes) 

    def test_incorrect_image(self):
        node = TextNode("This is text with an [image](https://i.imgur.com/zjjcJKZ.png) and text at the end", TextType.TEXT)
        new_nodes = split_nodes_image([node])
        self.assertListEqual([TextNode("This is text with an [image](https://i.imgur.com/zjjcJKZ.png) and text at the end", TextType.TEXT)], new_nodes) 

class TestSplitNodesLink(unittest.TestCase):
    def test_split_links(self):
        node = TextNode("This is text with an [link](https://www.boot.dev) and another [second link](https://www.google.com) and text at the end", TextType.TEXT)
        new_nodes = split_nodes_link([node])
        self.assertListEqual([TextNode("This is text with an ", TextType.TEXT),
                TextNode("link", TextType.LINK, "https://www.boot.dev"),
                TextNode(" and another ", TextType.TEXT),
                TextNode("second link", TextType.LINK, "https://www.google.com"),
                TextNode(" and text at the end", TextType.TEXT)], new_nodes) 
    
    def test_no_link(self):
        node = TextNode("This is text with no links", TextType.TEXT)
        new_nodes = split_nodes_link([node])
        self.assertListEqual([TextNode("This is text with no links", TextType.TEXT)], new_nodes)
    
    def test_link_at_beginning(self):
        node = TextNode("[link](https://www.boot.dev) link at the beginning", TextType.TEXT)
        new_nodes = split_nodes_link([node])
        self.assertListEqual([TextNode("link", TextType.LINK, "https://www.boot.dev"),
                TextNode(" link at the beginning", TextType.TEXT)], new_nodes)
    
    def test_link_at_end(self):
        node = TextNode("link at the end [link](https://www.boot.dev)", TextType.TEXT)
        new_nodes = split_nodes_link([node])
        self.assertListEqual([TextNode("link at the end ", TextType.TEXT), 
                              TextNode("link", TextType.LINK, "https://www.boot.dev")], new_nodes)

    def test_back_to_back_links(self):
        node = TextNode("This is text with back-to-back links [link](https://www.boot.dev)[second link](https://www.google.com) and text at the end", TextType.TEXT)
        new_nodes = split_nodes_link([node])
        self.assertListEqual([TextNode("This is text with back-to-back links ", TextType.TEXT),
                TextNode("link", TextType.LINK, "https://www.boot.dev"),
                TextNode("second link", TextType.LINK, "https://www.google.com"),
                TextNode(" and text at the end", TextType.TEXT)], new_nodes) 

    def test_one_link(self):
        node = TextNode("This is text with a [link](https://www.google.com) and text at the end", TextType.TEXT)
        new_nodes = split_nodes_link([node])
        self.assertListEqual([TextNode("This is text with a ", TextType.TEXT),
                TextNode("link", TextType.LINK, "https://www.google.com"),
                TextNode(" and text at the end", TextType.TEXT)], new_nodes) 

    def test_incorrect_link(self):
        node = TextNode("This is text with an ![link](https://www.google.com) and text at the end", TextType.TEXT)
        new_nodes = split_nodes_link([node])
        self.assertListEqual([TextNode("This is text with an ![link](https://www.google.com) and text at the end", TextType.TEXT)], new_nodes)

class TestToTextNodes(unittest.TestCase):
    def test_full_conversion(self):
        text = "This is **text** with an _italic_ word and a `code block` and " \
        "an ![obi wan image](https://i.imgur.com/fJRm4Vk.jpeg) and a [link](https://boot.dev)"
        self.assertListEqual([TextNode("This is ", TextType.TEXT),
            TextNode("text", TextType.BOLD),
            TextNode(" with an ", TextType.TEXT),
            TextNode("italic", TextType.ITALIC),
            TextNode(" word and a ", TextType.TEXT),
            TextNode("code block", TextType.CODE),
            TextNode(" and an ", TextType.TEXT),
            TextNode("obi wan image", TextType.IMAGE, "https://i.imgur.com/fJRm4Vk.jpeg"),
            TextNode(" and a ", TextType.TEXT),
            TextNode("link", TextType.LINK, "https://boot.dev")], text_to_textnodes(text))
    
    def test_normal_text(self):
        text = "This is just normal text"
        self.assertListEqual([TextNode("This is just normal text", TextType.TEXT)], text_to_textnodes(text))

    def test_empty(self):
        text = ""
        self.assertListEqual([], text_to_textnodes(text))
    
    def test_multiples(self):
        text = "This is **text****with** an _italic__word_ and `a``code block` and " \
        "an ![obi wan image](https://i.imgur.com/fJRm4Vk.jpeg)![obi wan image](https://i.imgur.com/fJRm4Vk.jpeg) and a [link](https://boot.dev)[link](https://boot.dev)"
        self.assertListEqual([TextNode("This is ", TextType.TEXT),
            TextNode("text", TextType.BOLD),
            TextNode("with", TextType.BOLD),
            TextNode(" an ", TextType.TEXT),
            TextNode("italic", TextType.ITALIC),
            TextNode("word", TextType.ITALIC),
            TextNode(" and ", TextType.TEXT),
            TextNode("a", TextType.CODE),
            TextNode("code block", TextType.CODE),
            TextNode(" and an ", TextType.TEXT),
            TextNode("obi wan image", TextType.IMAGE, "https://i.imgur.com/fJRm4Vk.jpeg"),
            TextNode("obi wan image", TextType.IMAGE, "https://i.imgur.com/fJRm4Vk.jpeg"),
            TextNode(" and a ", TextType.TEXT),
            TextNode("link", TextType.LINK, "https://boot.dev"),
            TextNode("link", TextType.LINK, "https://boot.dev")], text_to_textnodes(text))
    
    def test_only_one_type(self):
        text = "**This text only****has bold text in it**"
        self.assertListEqual([TextNode("This text only", TextType.BOLD),
            TextNode("has bold text in it", TextType.BOLD)], text_to_textnodes(text))
        
class TestMarkdownToHTMLNode(unittest.TestCase):
    def test_paragraphs(self):
        md = """
This is **bolded** paragraph
text in a p
tag here

This is another paragraph with _italic_ text and `code` here
"""

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><p>This is <b>bolded</b> paragraph text in a p tag here</p><p>This is another paragraph with <i>italic</i> text and <code>code</code> here</p></div>",
        )

    def test_codeblock(self):
        md = """
```
This is text that _should_ remain
the **same** even with inline stuff
```
"""

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><pre><code>This is text that _should_ remain\nthe **same** even with inline stuff\n</code></pre></div>",
        )
    
    def test_heading(self):
        md = "## This is a heading"
        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><h2>This is a heading</h2></div>"
        )

    def test_blockquote(self):
        md = "> This is a quote\n> with two lines."
        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><blockquote>This is a quote with two lines.</blockquote></div>"
        )

    def test_olist(self):
        md = "1. First item\n2. Second item"
        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><ol><li>First item</li><li>Second item</li></ol></div>"
        )

    def test_ulist(self):
        md = "- Apple\n- Banana\n- Cherry"
        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><ul><li>Apple</li><li>Banana</li><li>Cherry</li></ul></div>"
        )

    def test_paragraph_with_link(self):
        md = "Check [Boot.dev](https://boot.dev) for more info."
        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            '<div><p>Check <a href="https://boot.dev">Boot.dev</a> for more info.</p></div>',
        )

    def test_paragraph_with_image(self):
        md = "Here is an image: ![Alt](img.png)"
        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            '<div><p>Here is an image: <img src="img.png" alt="Alt" /></p></div>',
        )

    def test_combined_blocks(self):
        md = """# Heading Example

This is a **bold** and _italic_ paragraph with a [link](https://boot.dev) and an image ![Logo](logo.png).

> This is a quote
> that spans multiple lines.

- List item 1
- List **item** 2

1. First ordered
2. Second _ordered_

```
code example
with multiple lines
```
"""

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            (
                '<div>'
                '<h1>Heading Example</h1>'
                '<p>This is a <b>bold</b> and <i>italic</i> paragraph with a '
                '<a href="https://boot.dev">link</a> and an image '
                '<img src="logo.png" alt="Logo" />.</p>'
                '<blockquote>This is a quote that spans multiple lines.</blockquote>'
                '<ul><li>List item 1</li><li>List <b>item</b> 2</li></ul>'
                '<ol><li>First ordered</li><li>Second <i>ordered</i></li></ol>'
                '<pre><code>code example\nwith multiple lines\n</code></pre>'
                '</div>'
            )
        )

class TestExtractTitle(unittest.TestCase):
    def test_normal_header(self):
        markdown = "# Hello World"
        self.assertEqual(extract_title(markdown), "Hello World")

    def test_extra_whitespace(self):
        markdown = "   #   Shire News   "
        self.assertEqual(extract_title(markdown), "Shire News")

    def test_no_header(self):
        markdown = "## Only h2 here"
        with self.assertRaises(Exception):
            extract_title(markdown)

if __name__ == "__main__":
    unittest.main()