import unittest

from htmlnode import HtmlNode, LeafNode, ParentNode


class TestHtmlNode(unittest.TestCase):
    def test_props_to_html_one(self):
        resExpected = ' id="1"'
        h = HtmlNode(
            tag="p",
            value="This is awesome",
            attributes={"id": 1},
            children=None,
        )
        self.assertEqual(resExpected, h.props_to_html())

    def test_props_to_html_attr_None(self):
        resExpected = ""
        h = HtmlNode(
            tag="p",
            value="This is awesome",
        )
        self.assertEqual(resExpected, h.props_to_html())

    def test_props_to_html_att_multi(self):
        resExpected = ' id="main-content" class="container primary" href="https://example.com" src="images/logo.png"'
        h = HtmlNode(
            tag="p",
            value="This is awesome",
            attributes={
                "id": "main-content",  # <div >
                "class": "container primary",  # <div >
                "href": "https://example.com",  # <a >
                "src": "images/logo.png",  # <img >
            },
        )
        self.assertEqual(resExpected, h.props_to_html())


class TestLeafNode(unittest.TestCase):
    def test_leafNode_with_tag_and_attr(self):
        res = '<p class="first">Hello world</p>'
        leaf_node = LeafNode(
            tag="p", value="Hello world", attributes={"class": "first"}
        )
        self.assertEqual(res, leaf_node.to_html())

    def test_leafNode_no_tag_and_attr(self):
        leaf_node = LeafNode(value="Hello world", tag=None)
        self.assertEqual("Hello world", leaf_node.to_html())

    def test_leafNode_no_tag_but_attr_exists(self):
        leaf_node = LeafNode(
            value="Hello world", tag=None, attributes={"class": "first"}
        )
        self.assertEqual("Hello world", leaf_node.to_html())


class TestParentNode(unittest.TestCase):
    def test_parentNode_to_html_with_children_1(self):
        h = ParentNode(
            tag="p",
            children=[
                LeafNode(None, value="This is normal text "),
                LeafNode("b", value="This is in bold"),
                LeafNode(None, value=" This is normal text"),
            ],
        )
        res = "<p>This is normal text <b>This is in bold</b> This is normal text</p>"
        self.assertEqual(res, h.to_html())

    def test_parentNode_to_html_with_children_2(self):
        child_node = LeafNode("span", "child")
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(
            "<div><span>child</span></div>",
            parent_node.to_html(),
        )

    def test_parentNode_to_html_with_grandchildren(self):
        grandchild_node = LeafNode("b", "grandchild")
        child_node = ParentNode("span", [grandchild_node])
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(
            "<div><span><b>grandchild</b></span></div>",
            parent_node.to_html(),
        )

    def test_parentNode_to_html_no_children(self):
        with self.assertRaises(ValueError):
            ParentNode(tag="body", children=[]).to_html()

    def test_parentNode_to_html_no_tag(self):
        with self.assertRaises(ValueError):
            ParentNode(
                tag=None, children=[LeafNode(tag="b", value="this wont run")]
            ).to_html()

    def test_parent_to_html_full(self):
        res = '<html><head><title>Statics</title></head><body style="background-color:black"><p>This Is <b>Amazing </b>Bro</p><ul style="color:red;list-style:None"><li>Item 1</li><li>Item 2</li><li>Item 3</li><li>Item 4</li><li>Item 5</li></ul></body></html>'
        list_ul = ParentNode(
            tag="ul",
            children=[
                LeafNode("li", value="Item 1"),
                LeafNode("li", value="Item 2"),
                LeafNode("li", value="Item 3"),
                LeafNode("li", value="Item 4"),
                LeafNode("li", value="Item 5"),
            ],
            attributes={"style": "color:red;list-style:None"},
        )
        h1 = ParentNode(
            tag="p",
            children=[
                LeafNode(None, value="This Is "),
                LeafNode("b", value="Amazing "),
                LeafNode(None, value="Bro"),
            ],
        )
        body = ParentNode(
            tag="body",
            children=[h1, list_ul],
            attributes={"style": "background-color:black"},
        )
        head = ParentNode(tag="head", children=[LeafNode("title", value="Statics")])
        html = ParentNode(tag="html", children=[head, body])

        self.assertTrue(res, html.to_html())
