import textnode

class HTMLNode:
    def __init__(self, tag=None, value=None, children=None, props=None):
        self.tag = tag
        self.value = value
        self.children = children if children is not None else []
        self.props = props if props is not None else {}
    def to_html(self):
        raise NotImplementedError("Child classes will override this method")
    def props_to_html(self):
        if self.props is None or len(self.props) == 0:
            return ""
        return "".join([f' {key}="{value}"' for key, value in self.props.items()])
    def __repr__(self):
        return f"HTMLNode(tag={self.tag}, value={self.value}, children={self.children}, props={self.props})"
    
class LeafNode(HTMLNode):
    def __init__(self, tag=None, value=None, props=None):
        super().__init__(tag=tag, value=value, props=props)
    def to_html(self):
        if self.value is None:
            raise ValueError("LeafNode must have a value")
        if self.tag is None:
            return self.value
        return f"<{self.tag}{self.props_to_html()}>{self.value}</{self.tag}>"
    
class ParentNode(HTMLNode): 
    def __init__(self, tag=None, children=None, props=None):
        super().__init__(tag=tag, children=children, props=props)
    def to_html(self):
        if self.tag is None:
            raise ValueError("ParentNode must have a tag")
        if self.children is None or len(self.children) == 0:
            raise ValueError("ParentNode must have children")
        children_html = "".join(child.to_html() for child in self.children)
        return f"<{self.tag}{self.props_to_html()}>{children_html}</{self.tag}>"

def text_node_to_html_node(text_node):
    if text_node.text_type == textnode.TextType.NORMAL:
        return LeafNode(tag=None, value=text_node.text, props=None)
    elif text_node.text_type == textnode.TextType.BOLD:
        return LeafNode(tag="b", value=text_node.text, props=None)
    elif text_node.text_type == textnode.TextType.ITALIC:
        return LeafNode(tag="i", value=text_node.text, props=None)
    elif text_node.text_type == textnode.TextType.CODE:
        return LeafNode(tag="code", value=text_node.text, props=None)
    elif text_node.text_type == textnode.TextType.LINK:
        return LeafNode(tag="a", value=text_node.text, props={"href":text_node.url})
    elif text_node.text_type == textnode.TextType.IMAGE:
        return LeafNode(tag="img", value="", props={"src":text_node.url, "alt":text_node.text})
    else:
        raise ValueError

    

    
