from enum import Enum
from htmlnode import LeafNode
import re

class TextType(Enum):
    TEXT = "text"
    BOLD = "bold"
    ITALIC = "italic"
    CODE = "code"
    LINK = "link"      # <-- Already there!
    IMAGE = "image"    # <-- Already there!

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
    #1. need to loop throught the old nodes list and split it with the given delimiter
    #2. for each split/node i need to give the right text type 
    new_nodes_list = []
    for node in old_nodes:
        if node.text_type != TextType.TEXT:
            new_nodes_list.append(node)    
        else:       
            parts = node.text.split(delimiter)
            if len(parts) % 2 == 1:
                for i,text in enumerate(parts):
                    if len(text) != 0:
                        if i % 2 == 1:  # odd indexes = inside backticks
                            new_nodes_list.append(TextNode(text,text_type))
                        else:           # even indexes = outside backticks
                            new_nodes_list.append(TextNode(text,TextType.TEXT))
            else:
                raise Exception("delimiters did not properly match.")

    return new_nodes_list



def extract_markdown_images(text):
    matchs = re.findall(r"!\[([^\[\]]*)\]\(([^\(\)]*)\)",text)
    return matchs
def extract_markdown_links(text):
    mathes = re.findall(r"(?<!!)\[([^\[\]]*)\]\(([^\(\)]*)\)",text)
    return mathes





def split_nodes_image(old_nodes):
    pass 



def split_nodes_link(old_nodes):
    #1. i need to split the text 
    new_nodes_list = []
    for node in old_nodes:
        if node.text_type:
            text = extract_markdown_links(node.text)
            parts = node.text.split('[{text[0][0]}]({text[0][1]})',1)

    print(parts)


    # print(f'[{text[0][0]}]({text[0][1]})')
    # print(parts)
            
#[to youtube](https://www.youtube.com/@bootdotdev)
node = TextNode(
    "This is text with a link [to boot dev](https://www.boot.dev) and some more words",
    TextType.TEXT,)

split_nodes_link([node])