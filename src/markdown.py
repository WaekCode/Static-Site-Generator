from textnode import markdown_to_blocks, TextNode, text_to_textnodes, TextType, text_node_to_html_node
from block_type import block_to_block_type, BlockType
from htmlnode import LeafNode, ParentNode

def text_to_children(text):
    textnodes = text_to_textnodes(text)
    html_children = []
    for node in textnodes:
        if node.text_type == TextType.BOLD:
            html_children.append(LeafNode("b", node.text))
        elif node.text_type == TextType.ITALIC:
            html_children.append(LeafNode("i", node.text))
        elif node.text_type == TextType.CODE:
            html_children.append(LeafNode("code", node.text))
        else:
            html_children.append(LeafNode(None, node.text))
    return html_children

def markdown_to_html_node(markdown):
    blocks = markdown_to_blocks(markdown)
    parent = ParentNode("div", children=[])

    for i in blocks:
        type = block_to_block_type(i)

        if type == BlockType.QUOTE:
            lines = [line.lstrip("> ").strip() for line in i.splitlines()]
            text = " ".join(lines)
            parent.children.append(
                ParentNode("blockquote", children=text_to_children(text))
            )

        elif type == BlockType.UNORDERED_LIST:
            ul_node = ParentNode("ul", children=[])
            lines = i.split("\n")
            for line in lines:
                li_text = line.lstrip("- ").strip()
                li_node = ParentNode("li", children=text_to_children(li_text))
                ul_node.children.append(li_node)
            parent.children.append(ul_node)

        elif type == BlockType.ORDERED_LIST:
            ol_node = ParentNode("ol", children=[])
            lines = i.split("\n")
            for line in lines:
                li_text = line.split(". ", 1)[1].strip()
                li_node = ParentNode("li", children=text_to_children(li_text))
                ol_node.children.append(li_node)
            parent.children.append(ol_node)

        # ---------------- Code Block Logic ----------------
        elif type == BlockType.CODE:
            lines = i.splitlines()
            # Remove opening and closing ```
            if lines[0].startswith("```"):
                lines = lines[1:]
            if lines and lines[-1].startswith("```"):
                lines = lines[:-1]
            code_content = "\n".join(lines)
            if not code_content.endswith("\n"):
                code_content += "\n"  # important to pass unit test
            code_text_node = TextNode(code_content, TextType.CODE)
            code_html_node = text_node_to_html_node(code_text_node)
            parent.children.append(ParentNode("pre", children=[code_html_node]))

        elif type == BlockType.PARAGRAPH:
            normalized = " ".join(i.split())
            parent.children.append(ParentNode("p", children=text_to_children(normalized)))

        elif type == BlockType.HEADING:
            for line in i.splitlines():
                line = line.strip()
                if not line:
                    continue
                count = 0
                while count < len(line) and line[count] == "#":
                    count += 1
                heading_text = line[count:].strip()
                parent.children.append(
                    ParentNode(f"h{count}", children=text_to_children(heading_text))
                )

    return parent



md = """
# Heading 1
## Heading 2
"""

node = markdown_to_html_node(md)
html = node.to_html()
print(html)