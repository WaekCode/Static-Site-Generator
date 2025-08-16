import unittest
from htmlnode import HTMLNode,LeafNode,ParentNode

class TestHtmlNode(unittest.TestCase):
    def test_if_props_is_not_somthing(self):
        node = HTMLNode('a','this some text',[],{'a':2})
        self.assertNotEqual(node.props_to_html(),'')

    def test_what_props_should_be(self):
        node = HTMLNode('a','this some text',[],{"href": "https://www.google.com", "target": "_blank"})
        self.assertEqual(node.props_to_html(),' href="https://www.google.com" target="_blank"')

    
    def test_empty_props(self):
        node = HTMLNode('a', 'text', [], {})
        self.assertEqual(node.props_to_html(), '')

    def test_leaf_to_html_p(self):
        node = LeafNode("p", "Hello, world!")
        self.assertEqual(node.to_html(), "<p>Hello, world!</p>")


    def test_leaf_to_html_a(self):
        node = LeafNode("a", "Hello, world!")
        self.assertEqual(node.to_html(), "<a>Hello, world!</a>")


    def test_leaf_to_html_b(self):
        node = LeafNode("b", "Hello, world!")
        self.assertEqual(node.to_html(), "<b>Hello, world!</b>")

    def test_leaf_not_html_withUrl(self):
        node = LeafNode("a", "Click me!", {"href": "https://www.google.com"})
        self.assertEqual(node.to_html(), '<a href="https://www.google.com">Click me!</a>')

    def test_to_html_no_children(self):
        parent_node = ParentNode("div", [])
        self.assertEqual(parent_node.to_html(), "<div></div>")

    def test_to_html_multiple_children(self):
        child1 = LeafNode("span", "child1")
        child2 = LeafNode("span", "child2")
        parent_node = ParentNode("div", [child1, child2])
        self.assertEqual(parent_node.to_html(), "<div><span>child1</span><span>child2</span></div>")

    def test_to_html_nested_parents(self):
        # A parent inside another parent, with multiple children
        grandchild1 = LeafNode("i", "grandchild1")
        grandchild2 = LeafNode("b", "grandchild2")
        child1 = ParentNode("span", [grandchild1])
        child2 = ParentNode("p", [grandchild2])
        parent_node = ParentNode("div", [child1, child2])
        self.assertEqual(
            parent_node.to_html(),
            "<div><span><i>grandchild1</i></span><p><b>grandchild2</b></p></div>"
        )

    def test_to_html_text_only_leaf_node(self):
        leaf = LeafNode("p", "just text")
        self.assertEqual(leaf.to_html(), "<p>just text</p>")

    def test_to_html_deeply_nested(self):
        # 4-level nesting
        level4 = LeafNode("em", "deep")
        level3 = ParentNode("b", [level4])
        level2 = ParentNode("i", [level3])
        level1 = ParentNode("div", [level2])
        self.assertEqual(level1.to_html(), "<div><i><b><em>deep</em></b></i></div>")

    def test_to_html_empty_leaf_node(self):
        leaf = LeafNode("span", "")
        self.assertEqual(leaf.to_html(), "<span></span>")



if __name__ == "__main__":
    unittest.main()