from textnode import *
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
# with each tuple containing the anchor text and urls
def extract_markdown_links(text):
    return re.findall(r"(?<!!)\[([^\]]*)\]\((.*?)\)", text)
