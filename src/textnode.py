from enum import Enum
from htmlnode import LeafNode
import re

class TextType(Enum):
    TEXT = "text"
    BOLD = "bold"
    ITALIC = "italic"
    CODE = "code"
    LINK = "link"
    IMAGE = "image"   

class TextNode():
    def __init__(self,text,text_type:TextType,url=None):
        self.text = text
        self.text_type = text_type
        self.url = url
        

    def __eq__(self,other):
        if not isinstance(other, TextNode):
            return False
        return (
        other.text == self.text
        and other.url == self.url
        and other.text_type == self.text_type)

    def __repr__(self):
        return f'TextNode({self.text}, {self.text_type}, {self.url})'
    

def text_node_to_html_node(text_node):
    if text_node.text_type == TextType.TEXT:
        return LeafNode(None,text_node.text)
    elif text_node.text_type == TextType.BOLD:
        return LeafNode('b',text_node.text)
    elif text_node.text_type == TextType.ITALIC:
        return LeafNode('i',text_node.text)
    elif text_node.text_type == TextType.CODE:
        return LeafNode('code',text_node.text)
    elif text_node.text_type == TextType.LINK:
        return LeafNode("a", text_node.text, {"href": text_node.url})  # ← Problem here
    elif text_node.text_type == TextType.IMAGE:
        return LeafNode("img", "", {"src": text_node.url, "alt": text_node.text})
    else:
        raise Exception()
    


def split_nodes_delimiter(old_nodes, delimiter, text_type):
    new_nodes = []
    for old_node in old_nodes:
        if old_node.text_type != TextType.TEXT:
            new_nodes.append(old_node)
            continue
        split_nodes = []
        sections = old_node.text.split(delimiter)
        if len(sections) % 2 == 0:
            raise ValueError("invalid markdown, formatted section not closed")
        for i in range(len(sections)):
            if sections[i] == "":
                continue
            if i % 2 == 0:
                split_nodes.append(TextNode(sections[i], TextType.TEXT))
            else:
                split_nodes.append(TextNode(sections[i], text_type))
        new_nodes.extend(split_nodes)
    return new_nodes





def extract_markdown_images(text):
    pattern = r"!\[([^\[\]]*)\]\(([^\(\)]*)\)"
    matches = re.findall(pattern, text)
    return matches


def extract_markdown_links(text):
    pattern = r"(?<!!)\[([^\[\]]*)\]\(([^\(\)]*)\)"
    matches = re.findall(pattern, text)
    return matches

def split_nodes_image(old_nodes):
    new_nodes = []
    for old_node in old_nodes:
        if old_node.text_type != TextType.TEXT:
            new_nodes.append(old_node)
            continue
        original_text = old_node.text
        images = extract_markdown_images(original_text)
        if len(images) == 0:
            new_nodes.append(old_node)
            continue
        for image in images:
            sections = original_text.split(f"![{image[0]}]({image[1]})", 1)
            if len(sections) != 2:
                raise ValueError("invalid markdown, image section not closed")
            if sections[0] != "":
                new_nodes.append(TextNode(sections[0], TextType.TEXT))
            new_nodes.append(
                TextNode(
                    image[0],
                    TextType.IMAGE,
                    image[1],
                )
            )
            original_text = sections[1]
        if original_text != "":
            new_nodes.append(TextNode(original_text, TextType.TEXT))
    return new_nodes


def split_nodes_link(old_nodes):
    new_nodes = []
    for old_node in old_nodes:
        if old_node.text_type != TextType.TEXT:
            new_nodes.append(old_node)
            continue
        original_text = old_node.text
        links = extract_markdown_links(original_text)
        if len(links) == 0:
            new_nodes.append(old_node)
            continue
        for link in links:
            sections = original_text.split(f"[{link[0]}]({link[1]})", 1)
            if len(sections) != 2:
                raise ValueError("invalid markdown, link section not closed")
            if sections[0] != "":
                new_nodes.append(TextNode(sections[0], TextType.TEXT))
            new_nodes.append(TextNode(link[0], TextType.LINK, link[1]))
            original_text = sections[1]
        if original_text != "":
            new_nodes.append(TextNode(original_text, TextType.TEXT))
    return new_nodes

def text_to_textnodes(text):
    # Start with a single Text node containing the full text
    textnodes = [TextNode(text, TextType.TEXT)]

    # Split bold first
    textnodes = split_nodes_delimiter(textnodes, '**', TextType.BOLD)

    # Split italic next
    textnodes = split_nodes_delimiter(textnodes, '_', TextType.ITALIC)

    # Split code next
    textnodes = split_nodes_delimiter(textnodes, '`', TextType.CODE)

    # Split images
    textnodes = split_nodes_image(textnodes)

    # Split links
    textnodes = split_nodes_link(textnodes)

    return textnodes


def markdown_to_blocks(markdown):
    parts = markdown.split("\n\n")  # Split the markdown by double newlines
    blocks = []
    
    for part in parts:
        stripped_block = part.strip()  # Remove whitespace at the start/end of the block

        if stripped_block:  # Only continue if the block is not empty
            # Split the block into individual lines
            lines = stripped_block.split("\n")
            cleaned_lines = []
         

            # Strip each line of leading/trailing spaces
            for line in lines:
                cleaned_line = line.strip()
                cleaned_lines.append(cleaned_line)
            

            # Join the cleaned lines back into one block
            final_block = "\n".join(cleaned_lines)
            blocks.append(final_block)
    
    return blocks

    
