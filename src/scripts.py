from misc_functions import *

# text = "This is text with a ![rick roll](https://i.imgur.com/aKaOqIh.gif) and ![obi wan](https://i.imgur.com/fJRm4Vk.jpeg)"
# print(extract_markdown_images(text))
# # [("rick roll", "https://i.imgur.com/aKaOqIh.gif"), ("obi wan", "https://i.imgur.com/fJRm4Vk.jpeg")]

# text = "This is text with a link [to boot dev](https://www.boot.dev) and [to youtube](https://www.youtube.com/@bootdotdev)"
# print(extract_markdown_links(text))
# # [("to boot dev", "https://www.boot.dev"), ("to youtube", "https://www.youtube.com/@bootdotdev")]

node = TextNode("This is text with an incorrect image ![image]() and text at the end", TextType.TEXT)
print(split_nodes_image([node]))
# [TextNode(text=This is text with an incorrect image , text_type=Normal text, url=None), 
# TextNode(text=image, text_type=![alt text](url), url=), 
# TextNode(text= and text at the end, text_type=Normal text, url=None)]
