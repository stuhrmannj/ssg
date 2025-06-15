from enum import Enum

class TextType(Enum):
    TEXT = "Normal text"
    BOLD = "**Bold text**"
    ITALIC = "_Italic text_"
    CODE = "`Code text`"
    LINK = "[anchor text](url)"
    IMAGE = "![alt text](url)"

class TextNode:
    def __init__(self, text, text_type, url=None):
        self.text = text
        self.text_type = text_type
        self.url = url
    def __eq__(self, other):
        if not isinstance(other, TextNode):
            return False
        return(self.text == other.text and 
               self.text_type == other.text_type and 
               self.url == other.url)
    def __repr__(self):
        return f"TextNode(text={self.text}, text_type={self.text_type.value}, url={self.url})"

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
