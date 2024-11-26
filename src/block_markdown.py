from enum import Enum
from itertools import takewhile 

class BlockType(Enum):
    PARAGRAPH = "paragraph"
    HEADING = "heading"
    CODE = "code"
    QUOTE = "quote"
    UNORDERED_LIST = "unordered list"
    ORDERED_LIST = "ordered list"


def markdown_to_blocks(markdown):
    trimmed_markdown = markdown.split("\n\n")
    blocks = []

    for block in trimmed_markdown:
        if block == "":
            continue
        block = block.strip()
        blocks.append(block)
    return blocks

def block_to_block_type(single_block):
    lines = single_block.splitlines()
    if len(lines) == 0:
        return BlockType.PARAGRAPH
    if is_heading(lines[0]):
        return BlockType.HEADING
    if is_code_block(single_block):
        return BlockType.CODE
    if is_quote_block(lines):
        return BlockType.QUOTE
    if is_unordered_list_block(lines):
        return BlockType.UNORDERED_LIST
    if is_ordered_list_block(lines):
        return BlockType.ORDERED_LIST
    return BlockType.PARAGRAPH
    
   
    
def is_heading(line):
    count = len(list(takewhile(lambda c: c == '#', line)))
    return count <= 6 and count > 0 and len(line) > count + 1 and line[count] == " " and line[count + 1] != " "

def is_code_block(block):
    if block[:3] != "```" and block[-3:] != "```":
        return False
    return True
    
def is_quote_line(line):
    return line.startswith('>')

def is_quote_block(lines):
    return all(is_quote_line(line) for line in lines)

def is_unordered_list_line(line):
    return line[:2] == "* " or line[:2] == "- "

def is_unordered_list_block(lines):
    return all(is_unordered_list_line(line) for line in lines)

def is_ordered_list_line(line, index):
    expected_number = str(index + 1)
    return line.startswith(expected_number) and line[1] == "." and line[2] == " " and len(line) > 3

def is_ordered_list_block(lines):
    return all(is_ordered_list_line(line, i) for i, line in enumerate(lines))