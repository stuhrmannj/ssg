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
