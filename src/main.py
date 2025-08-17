from textnode import TextNode,TextType
from htmlnode import HTMLNode,LeafNode,ParentNode

def main():
    text1 = TextNode('this is some text','**Bold text**','https://www.boot.dev')
    te = LeafNode('a','this some text.')
    node = ParentNode(
        "p",
        [
            LeafNode("b", "Bold text"),
            LeafNode(None, "Normal text"),
            LeafNode("i", "italic text"),
            LeafNode(None, "Normal text"),
        ],
    )






