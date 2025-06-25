from enum import Enum

# converts a raw string of markdown text and returns a list of block strings
def markdown_to_blocks(markdown):
    blocks = markdown.split("\n\n")
    blocks_stripped = [block.strip() for block in blocks if block.strip() != ""]
    return blocks_stripped

class BlockType(Enum):
    PARAGRAPH = "paragraph"
    HEADING = "heading"
    CODE = "code"
    QUOTE = "quote"
    ULIST = "unordered_list"
    OLIST = "ordered_list"

def block_to_block_type(block):
    # code block check
    if block.startswith("```") and block.endswith("```"):
        return BlockType.CODE
    
    # heading block check
    count = 0
    for char in block:
        if char == "#":
            count += 1
        else:
            break
    if count > 0 and count < 7 and len(block) >  count and block[count] == " ":
        return BlockType.HEADING

    # Check for quote block
    if all(line.startswith(">") for line in block.splitlines()):
        return BlockType.QUOTE

    # Check for unordered list
    if all(line.startswith("- ") for line in block.splitlines()):
        return BlockType.ULIST

    # Check for ordered list
    if all(line.startswith(f"{index}. ") for index, line in enumerate(block.splitlines(), start = 1)):
        return BlockType.OLIST

    # Otherwise, it's a paragraph
    return BlockType.PARAGRAPH 
