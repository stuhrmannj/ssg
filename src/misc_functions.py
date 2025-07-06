from textnode import *
from blocks import *
from htmlnode import *
import re

# splits text nodes for different inline text types
def split_nodes_delimiter(old_nodes, delimiter, text_type):
    new_nodes = []  #initialize an empty list for the results
    for old_node in old_nodes:
        if old_node.text_type != TextType.TEXT:
            new_nodes.append(old_node)
        else:
            parts = old_node.text.split(delimiter)
            if len(parts) % 2 == 0:
                raise Exception(f"Invalid markdown, closing delimiter not found: {delimiter}")
            else:
                for index, part in enumerate(parts):
                    if index % 2 == 0:
                        if part != "":
                            new_node = TextNode(part, TextType.TEXT)
                            new_nodes.append(new_node)
                    else:
                        if part != "":
                            new_node = TextNode(part, text_type)
                            new_nodes.append(new_node)
    return new_nodes

# takes raw markdown text and returns a list of tuples, 
# with each tuple containing the alt text and url of any markdown image
def extract_markdown_images(text):
    return re.findall(r"!\[([^\]]*)\]\((.*?)\)", text)

#takes raw markdown text and returns a list of tuples,
# with each tuple containing the anchor text and url of any markdown link
def extract_markdown_links(text):
    return re.findall(r"(?<!!)\[([^\]]*)\]\((.*?)\)", text)

# splits text nodes that have images
def split_nodes_image(old_nodes):
    new_nodes = []
    for old_node in old_nodes:
        # Start with the whole text as 'remainder'
        remainder = old_node.text
        images = extract_markdown_images(remainder)
        if images == []:
            new_nodes.append(old_node)
        else:
            # For each image found
            for image in images:
                # Split 'remainder' on the first occurrence of this image
                sections = remainder.split(f"![{image[0]}]({image[1]})", 1)
                # If there's text before the image, create a text node for it
                if sections[0] != "":
                    new_nodes.append(TextNode(sections[0], TextType.TEXT))
                #image node for current image
                new_nodes.append(TextNode(image[0], TextType.IMAGE, image[1]))
                # Update 'remainder' to what comes after the image
                remainder = sections[1]  
            # After processing all images, if remainder has anything left, add it as a text node
            if remainder != "":
                new_nodes.append(TextNode(remainder, TextType.TEXT))
    return new_nodes

# splits text nodes that have links
def split_nodes_link(old_nodes):
    new_nodes = []
    for old_node in old_nodes:
        # Start with the whole text as 'remainder'
        remainder = old_node.text
        links = extract_markdown_links(remainder)
        if links == []:
            new_nodes.append(old_node)
        else:
            # For each link found
            for link in links:
                # Split 'remainder' on the first occurrence of this link
                sections = remainder.split(f"[{link[0]}]({link[1]})", 1)
                # If there's text before the link, create a text node for it
                if sections[0] != "":
                    new_nodes.append(TextNode(sections[0], TextType.TEXT))
                #link node for current link
                new_nodes.append(TextNode(link[0], TextType.LINK, link[1]))
                # Update 'remainder' to what comes after the link
                remainder = sections[1]  
            # After processing all links, if remainder has anything left, add it as a text node
            if remainder != "":
                new_nodes.append(TextNode(remainder, TextType.TEXT))
    return new_nodes

# converts a raw string of markdown text into a list of Textnode objects
def text_to_textnodes(text):
    starting_node = []
    starting_node.append(TextNode(text, TextType.TEXT))
    with_images = split_nodes_image(starting_node)
    with_links = split_nodes_link(with_images)
    with_bold =  split_nodes_delimiter(with_links,"**", TextType.BOLD)
    with_italic = split_nodes_delimiter(with_bold,"_", TextType.ITALIC)
    with_code =  split_nodes_delimiter(with_italic,"`", TextType.CODE)
    return with_code

# convert text block to children html nodes
def text_to_children(block):
    textnodes = text_to_textnodes(block)
    htmlnodes = []
    for textnode in textnodes:
        htmlnodes.append(text_node_to_html_node(textnode))
    return htmlnodes

def markdown_to_html_node(markdown):
    # split markdown into blocks
    blocks = markdown_to_blocks(markdown)
    
    # prepare a list to collect HTML block nodes
    block_nodes = []

    # loop through each block
    for block in blocks:
        # determine the type of block
        block_type = block_to_block_type(block)

        # create appropriate HTMLNode(s) for this block
        if block_type == BlockType.PARAGRAPH:
            clean_block = block.replace("\n", " ")
            children_nodes = text_to_children(clean_block)
            block_html_node = ParentNode("p", children_nodes, None)
        elif block_type == BlockType.QUOTE:
            lines = block.splitlines()
            cleaned_lines = []
            for line in lines:
                # Remove leading '>' and any following whitespace
                if line.strip().startswith(">"):
                    cleaned_lines.append(line.lstrip()[1:].lstrip())
                else:
                    cleaned_lines.append(line)
            clean_block = " ".join(cleaned_lines)
            children_nodes = text_to_children(clean_block)
            block_html_node = ParentNode("blockquote", children_nodes, None)
        elif block_type == BlockType.HEADING:
            count = 0
            for char in block:
                if char == "#":
                    count += 1
                else:
                    break
            children_nodes = text_to_children(block[count:].lstrip())
            block_html_node = ParentNode(f"h{count}", children_nodes, None)
        elif block_type == BlockType.CODE:
            # Split the block into lines
            lines = block.splitlines()
            # Remove the opening and closing ```
            if lines and lines[0].strip().startswith("```"):
                lines = lines[1:]
            if lines and lines[-1].strip().startswith("```"):
                lines = lines[:-1]
            code_content = "\n".join(lines) + "\n"  # The `+ "\n"` keeps trailing newline as in sample outputs 
            code_text_node = TextNode(code_content, TextType.CODE, None)
            code_html_node = text_node_to_html_node(code_text_node)
            block_html_node = ParentNode("pre", [code_html_node], None)
        elif block_type == BlockType.OLIST:
            olist = []
            block_lines = block.splitlines()
            for block_line in block_lines:
                match = re.match(r"\s*\d+\.\s*(.*)", block_line)
                if match:
                    content = match.group(1)
                else:
                    content = block_line.lstrip()
                item_node = ParentNode("li", text_to_children(content), None)
                olist.append(item_node)
            block_html_node = ParentNode("ol", olist, None)
        elif block_type == BlockType.ULIST:
            ulist = []
            block_lines = block.splitlines()
            for block_line in block_lines:
                content = block_line[2:]
                item_node = ParentNode("li", text_to_children(content), None)
                ulist.append(item_node)
            block_html_node = ParentNode("ul", ulist, None)
  
        # Add your completed HTMLNode to the block_nodes list
        block_nodes.append(block_html_node)

    # return a parent <div> node containing all the block_nodes as children
    complete_html_node = ParentNode("div", block_nodes, None)
    return complete_html_node
