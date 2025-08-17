import unittest

from textnode import TextNode, TextType, text_node_to_html_node,split_nodes_delimiter,extract_markdown_images,extract_markdown_links


class TestTextNode(unittest.TestCase):
    def test_eq(self):
        node = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is a text node", TextType.BOLD)
        self.assertEqual(node, node2)

    def test_url(self):
        node = TextNode("This is a text node", TextType.BOLD,'https://www.boot.dev')
        node2 = TextNode("This is a text node", TextType.BOLD)
        self.assertNotEqual(node,node2)
    
    def test_text_type_diff(self):
        node = TextNode("This is a text node", TextType.ITALIC)
        node2 = TextNode("This is a text node", TextType.BOLD)
        self.assertNotEqual(node,node2)

    def test_text(self):
        node = TextNode("This is a text node", TextType.TEXT)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, None)
        self.assertEqual(html_node.value, "This is a text node")

    def test_bold(self):
        node = TextNode("This is a text node", TextType.BOLD)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, 'b')
        self.assertEqual(html_node.value, "This is a text node")

    def test_linkf(self):
        node = TextNode("This is a text node", TextType.LINK, 'https://www.boot.dev')
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, 'a')
        self.assertEqual(html_node.value, "This is a text node")
        self.assertEqual(html_node.props, {'href': 'https://www.boot.dev'})

    def test_IMAGE (self):
        node = TextNode("This is a text node", TextType.IMAGE, 'https://www.boot.dev')
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, 'img')
        self.assertEqual(html_node.value, '')
        self.assertEqual(html_node.props, {'src': 'https://www.boot.dev', 'alt': 'This is a text node'})

    #CHATGBT UNIT TESTS
    #splitting nodes from a deleimeter and making each node its own text node tests
    def test_basic_split_code(self):
        node = TextNode("This is text with a `code block` word", TextType.TEXT)
        result = split_nodes_delimiter([node], "`", TextType.CODE)

        self.assertEqual(len(result), 3)
        self.assertEqual(result[1].text, "code block")
        self.assertEqual(result[1].text_type, TextType.CODE)

    def test_multiple_code_blocks(self):
        node = TextNode("Here is `one` and `two`", TextType.TEXT)
        result = split_nodes_delimiter([node], "`", TextType.CODE)

        self.assertEqual(len(result), 4)
        self.assertEqual(result[1].text, "one")
        self.assertEqual(result[3].text, "two")

    def test_no_delimiters(self):
        node = TextNode("Plain text no code", TextType.TEXT)
        result = split_nodes_delimiter([node], "`", TextType.CODE)

        self.assertEqual(len(result), 1)
        self.assertEqual(result[0].text_type, TextType.TEXT)

    def test_mismatched_delimiters_raises(self):
        node = TextNode("This has `unclosed code", TextType.TEXT)
        with self.assertRaises(Exception):
            split_nodes_delimiter([node], "`", TextType.CODE)

    def test_non_text_node_passed_through(self):
        node = TextNode("Already code", TextType.CODE)
        result = split_nodes_delimiter([node], "`", TextType.CODE)
        self.assertEqual(result[0].text_type, TextType.CODE)

    # 🔥 New Tests Below 🔥

    def test_bold_with_double_asterisks(self):
        node = TextNode("This is **bold** text", TextType.TEXT)
        result = split_nodes_delimiter([node], "**", TextType.BOLD)

        self.assertEqual(len(result), 3)
        self.assertEqual(result[1].text, "bold")
        self.assertEqual(result[1].text_type, TextType.BOLD)

    def test_italic_with_underscore(self):
        node = TextNode("This is _italic_ text", TextType.TEXT)
        result = split_nodes_delimiter([node], "_", TextType.ITALIC)

        self.assertEqual(len(result), 3)
        self.assertEqual(result[1].text, "italic")
        self.assertEqual(result[1].text_type, TextType.ITALIC)

    def test_starts_with_code(self):
        node = TextNode("`start` of text", TextType.TEXT)
        result = split_nodes_delimiter([node], "`", TextType.CODE)

        self.assertEqual(result[0].text, "start")
        self.assertEqual(result[0].text_type, TextType.CODE)
        self.assertEqual(result[1].text, " of text")
        self.assertEqual(result[1].text_type, TextType.TEXT)

    def test_ends_with_code(self):
        node = TextNode("Text with `end`", TextType.TEXT)
        result = split_nodes_delimiter([node], "`", TextType.CODE)

        self.assertEqual(result[-1].text, "end")
        self.assertEqual(result[-1].text_type, TextType.CODE)

    def test_multiple_nodes_input(self):
        node1 = TextNode("First `code` block", TextType.TEXT)
        node2 = TextNode("Second **bold** block", TextType.TEXT)
        result = split_nodes_delimiter([node1, node2], "`", TextType.CODE)
        result = split_nodes_delimiter(result, "**", TextType.BOLD)

        # Check that both code and bold were processed
        code_nodes = [n for n in result if n.text_type == TextType.CODE]
        bold_nodes = [n for n in result if n.text_type == TextType.BOLD]

        self.assertEqual(code_nodes[0].text, "code")
        self.assertEqual(bold_nodes[0].text, "bold")

    #regex tests
    def test_extract_markdown_images(self):
        matches = extract_markdown_images(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png)"
        )
        self.assertListEqual([("image", "https://i.imgur.com/zjjcJKZ.png")], matches)



    def test_extract_markdown_images(self):
        matches = extract_markdown_images(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png)"
        )
        self.assertListEqual(
            [("image", "https://i.imgur.com/zjjcJKZ.png")],
            matches
        )

    def test_extract_multiple_images(self):
        matches = extract_markdown_images(
            "Here is ![img1](http://a.com/1.png) and ![img2](http://b.com/2.jpg)"
        )
        self.assertListEqual(
            [("img1", "http://a.com/1.png"), ("img2", "http://b.com/2.jpg")],
            matches
        )

    def test_extract_images_none(self):
        matches = extract_markdown_images("No images here!")
        self.assertEqual(matches, [])

    def test_extract_image_with_spaces_in_alt_text(self):
        matches = extract_markdown_images(
            "Check ![cool photo](http://example.com/photo.png)"
        )
        self.assertListEqual(
            [("cool photo", "http://example.com/photo.png")],
            matches
        )

    def test_extract_markdown_links(self):
        matches = extract_markdown_links(
            "This is a [link](https://www.google.com)"
        )
        self.assertListEqual(
            [("link", "https://www.google.com")],
            matches
        )

    def test_extract_multiple_links(self):
        matches = extract_markdown_links(
            "Go to [Google](https://google.com) or [GitHub](https://github.com)"
        )
        self.assertListEqual(
            [("Google", "https://google.com"), ("GitHub", "https://github.com")],
            matches
        )

    def test_extract_links_none(self):
        matches = extract_markdown_links("No links here!")
        self.assertEqual(matches, [])

    def test_extract_link_with_spaces_in_text(self):
        matches = extract_markdown_links(
            "Click [Open AI Homepage](https://openai.com)"
        )
        self.assertListEqual(
            [("Open AI Homepage", "https://openai.com")],
            matches
        )

if __name__ == "__main__":
    unittest.main()