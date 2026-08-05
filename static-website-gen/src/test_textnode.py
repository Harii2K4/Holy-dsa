import unittest

from textnode import TextNode, TextType, text_node_to_html_node


class TestTextNode(unittest.TestCase):
    def test_equal(self):
        t1 = TextNode(content="Hello world", type=TextType.TEXT)
        t2 = TextNode(content="Hello world", type=TextType.TEXT)
        self.assertEqual(t1, t2)

    def test_notequal(self):
        t1 = TextNode(content="Hello world", type=TextType.TEXT)
        t2 = TextNode(content="this aint equal dawg", type=TextType.TEXT)
        self.assertNotEqual(t1, t2)

    def test_no_url(self):
        t1 = TextNode(
            content="Hello world",
            type=TextType.LINK,
            link="https://www.boot.dev/lessons",
        )
        t2 = TextNode(content="Hello world", type=TextType.LINK)
        self.assertNotEqual(t1, t2)

    def test_diff_text_type(self):
        t1 = TextNode(content="Hello world", type=TextType.BOLD)
        t2 = TextNode(content="Hello world", type=TextType.TEXT)
        self.assertNotEqual(t1, t2)

    def test_invalid_object_type(self):
        t1 = TextNode(content="Hello world", type=TextType.BOLD)
        with self.assertRaises(TypeError):
            self.assertNotEqual(t1, "Hello World")


class ConvertTextNode(unittest.TestCase):
    def test_text_node_to_html_node_TEXT(self):
        node = TextNode("This is a text node", TextType.TEXT)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, None)
        self.assertEqual(html_node.value, "This is a text node")

    def test_text_node_to_html_node_LINK(self):
        node = TextNode(
            "About The Odin Project",
            TextType.LINK,
            link="https://www.theodinproject.com/about",
        )
        html_node = text_node_to_html_node(node)
        res = (
            '<a href="https://www.theodinproject.com/about">About The Odin Project</a>'
        )
        self.assertEqual(html_node.tag, "a")
        self.assertEqual(html_node.value, "About The Odin Project")
        self.assertEqual(res, html_node.to_html())

    def test_text_node_to_html_node_BOLD(self):
        node = TextNode("This is a bold text node", TextType.BOLD)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "strong")
        res = "<strong>This is a bold text node</strong>"
        self.assertEqual(res, html_node.to_html())

    def test_text_node_to_html_node_ITALIC(self):
        node = TextNode("This is an italic text node", TextType.ITALIC)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "em")
        res = "<em>This is an italic text node</em>"
        self.assertEqual(res, html_node.to_html())

    def test_text_node_to_html_node_CODE(self):
        node = TextNode("This is a code text node", TextType.CODE)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "code")
        res = "<code>This is a code text node</code>"
        self.assertEqual(res, html_node.to_html())

    def test_text_node_to_html_node_IMAGE(self):
        node = TextNode("Cute cat image", TextType.IMAGE, link="../cat.img")
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "img")
        res = '<img src="../cat.img" alt="Cute cat image">'
        self.assertEqual(res, html_node.to_html())
