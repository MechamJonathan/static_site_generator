import re
from textnode import TextType, TextNode


def split_nodes_delimiter(old_nodes, delimiter, text_type):
    new_nodes = []
    for node in old_nodes:
        if node.text_type is not TextType.TEXT:
            new_nodes.append(node)
        else:
            split_node = node.text.split(delimiter)
            if len(split_node) % 2 == 0:
                raise Exception("Unbalanced delimiters found in the text node")
            
            for index, split in enumerate(split_node):
                if len(split) == 0:
                    continue
                if index % 2 == 0:
                    new_nodes.append(TextNode(split, TextType.TEXT))
                else:
                    new_nodes.append(TextNode(split, text_type))
    return new_nodes

def extract_markdown_images(text):
    text_and_link = re.findall(r"!\[([^\[\]]*)\]\(([^\(\)]*)\)", text)
    return text_and_link

def extract_markdown_links(text):
    text_and_link = re.findall(r"(?<!!)\[([^\[\]]*)\]\(([^\(\)]*)\)", text)
    return text_and_link

def split_nodes_image(old_nodes):
    new_nodes = []
    for node in old_nodes:
        text = node.text
        while text:
            extracted_images = extract_markdown_images(text)

            if not extracted_images:
                new_nodes.append(TextNode(text, TextType.TEXT))
                break

            image_alt, image_link = extracted_images[0]
            sections = text.split(f"![{image_alt}]({image_link})", 1)
                
            if sections[0]:  # Check if there's text
                new_nodes.append(TextNode(sections[0], TextType.TEXT))

            new_nodes.append(TextNode(image_alt, TextType.IMAGE, image_link))
            text = sections[1]
    return new_nodes

def split_nodes_link(old_nodes):
    new_nodes = []
    for node in old_nodes:
        text = node.text
        while text:
            extracted_link = extract_markdown_links(text)

            if not extracted_link:
                new_nodes.append(TextNode(text, TextType.TEXT))
                break

            link_alt, link_link = extracted_link[0]
            sections = text.split(f"[{link_alt}]({link_link})", 1)
                
            if sections[0]:  # Check if there's text
                new_nodes.append(TextNode(sections[0], TextType.TEXT))

            new_nodes.append(TextNode(link_alt, TextType.LINK, link_link))
            text = sections[1]
    return new_nodes