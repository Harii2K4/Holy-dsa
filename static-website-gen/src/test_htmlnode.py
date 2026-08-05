import unittest

from htmlnode import HtmlNode, LeafNode


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
