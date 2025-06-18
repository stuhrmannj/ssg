# converts a raw string of markdown text and returns a list of block strings
def markdown_to_blocks(markdown):
    blocks = markdown.split("\n\n")
    blocks_stripped = [block.strip() for block in blocks if block.strip() != ""]
    return blocks_stripped