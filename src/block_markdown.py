from enum import Enum
from itertools import takewhile 
from htmlnode import HTMLNode, ParentNode
from inline_markdown import text_to_textnodes
from textnode import text_node_to_html_node, TextNode, TextType

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

def markdown_to_html_node(markdown):
    blocks = markdown_to_blocks(markdown)
    children = []
    for block in blocks:
        html_node = block_to_html_node(block)
        children.append(html_node)
    return ParentNode("div", children, None)

def block_to_html_node(block):
    block_type = block_to_block_type(block)
    if block_type == BlockType.PARAGRAPH:
        return create_paragraph_node(block)
    elif block_type == BlockType.HEADING:
        return create_heading_node(block)
    elif block_type == BlockType.QUOTE:
        return create_quote_node(block)
    elif block_type == BlockType.CODE:
        return create_code_node(block)
    elif block_type == BlockType.UNORDERED_LIST:
        return create_unordered_list_node(block)
    elif block_type == BlockType.ORDERED_LIST:
        return create_ordered_list_node(block)
    raise ValueError(f"Unknown block type: {block_type}")                        

def text_to_children(text):
    children = []
    text_nodes = text_to_textnodes(text)
    for node in text_nodes:
        child = text_node_to_html_node(node)
        children.append(child)
    return children

def create_paragraph_node(block):
    lines = block.split("\n")
    paragraph = " ".join(lines)
    children = text_to_children(paragraph)
    return ParentNode("p", children)

def create_heading_node(block):
    count = len(list(takewhile(lambda c: c == '#', block)))
    heading_tag = "h" + str(count)
    text = block[count:].strip()
    children = text_to_children(text)
    return ParentNode(tag=heading_tag, children=children)

def create_quote_node(block):
    lines = block.split("\n")
    new_lines = []
    for line in lines:
        if not line.startswith(">"):
            raise ValueError("Invalid quote block")
        new_lines.append(line.lstrip(">").strip())
    content = " ".join(new_lines)
    children = text_to_children(content)
    return ParentNode("blockquote", children)

def create_code_node(block):
    lines = block.splitlines()
    text = "\n".join(lines[1:-1])
    # Create the nested structure
    children = text_to_children(text)
    code = ParentNode("code", children)
    return ParentNode("pre", [code])

def create_unordered_list_node(block):
    list_of_nodes = []
    lines = block.splitlines()
    for line in lines:
        text = line[1:].strip()
        li_children = text_to_children(text)
        li_node = ParentNode(tag="li", children=li_children)
        list_of_nodes.append(li_node)
    return ParentNode("ul", children=list_of_nodes)

def create_ordered_list_node(block):
    list_of_nodes = []
    lines = block.splitlines()
    for line in lines:
        text = line[2:].strip()
        li_children = text_to_children(text)
        li_node = ParentNode(tag="li", children=li_children)
        list_of_nodes.append(li_node)
    return ParentNode("ol", children=list_of_nodes) 
