import unittest

from md_parser import split_nodes_delimiter
from textnode import TextNode, TextType


class TestSplitNode(unittest.TestCase):
    def test_split_node_delimiter_wrong_delim(self):
        t = [TextNode("hello world", TextType.TEXT)]

        with self.assertRaises(ValueError):
            split_nodes_delimiter(t, "1", TextType.BOLD)

    # Parsing Bold
    def test_split_node_delimiter_bold_start(self):
        t = [TextNode("**hello** world", TextType.TEXT)]
        res = [TextNode("hello", TextType.BOLD), TextNode(" world", TextType.TEXT)]

        self.assertListEqual(split_nodes_delimiter(t, "**", TextType.BOLD), res)

    def test_split_node_delimiter_bold_end(self):
        t = [TextNode("world **hello**", TextType.TEXT)]
        res = [TextNode("world ", TextType.TEXT), TextNode("hello", TextType.BOLD)]

        self.assertListEqual(split_nodes_delimiter(t, "**", TextType.BOLD), res)

    def test_split_node_delimiter_bold_middle(self):
        t = [TextNode("world **hello** end", TextType.TEXT)]
        res = [
            TextNode("world ", TextType.TEXT),
            TextNode("hello", TextType.BOLD),
            TextNode(" end", TextType.TEXT),
        ]

        self.assertListEqual(split_nodes_delimiter(t, "**", TextType.BOLD), res)

    def test_split_node_delimiter_bold_no_closing_delimt(self):

        t = [TextNode("**hello end", TextType.TEXT)]
        res = [TextNode("**hello end", TextType.TEXT)]

        self.assertListEqual(split_nodes_delimiter(t, "**", TextType.BOLD), res)

    def test_split_node_delimiter_italic_start(self):

        t = [TextNode("_hello_ end", TextType.TEXT)]
        res = [TextNode("hello", TextType.ITALIC), TextNode(" end", TextType.TEXT)]

        self.assertListEqual(split_nodes_delimiter(t, "_", TextType.ITALIC), res)

    def test_split_node_delimiter_italic_middle(self):

        t = [TextNode("woah _hello_ end", TextType.TEXT)]
        res = [
            TextNode("woah ", TextType.TEXT),
            TextNode("hello", TextType.ITALIC),
            TextNode(" end", TextType.TEXT),
        ]

        self.assertListEqual(split_nodes_delimiter(t, "_", TextType.ITALIC), res)

    def test_split_node_delimiter_code_end(self):

        t = [TextNode("this is the code:```print('hello world')```", TextType.TEXT)]
        res = [
            TextNode("this is the code:", TextType.TEXT),
            TextNode("print('hello world')", TextType.CODE),
        ]

        self.assertListEqual(split_nodes_delimiter(t, "`", TextType.CODE), res)

    def test_split_node_delimiter_multiline(self):

        t = [
            TextNode("this is **super** cool", TextType.TEXT),
            TextNode("this is the code:```print('hello world')```", TextType.TEXT),
        ]
        expected_res_mid = [
            TextNode("this is **super** cool", TextType.TEXT),
            TextNode("this is the code:", TextType.TEXT),
            TextNode("print('hello world')", TextType.CODE),
        ]

        actual_res_mid = split_nodes_delimiter(t, "`", TextType.CODE)

        self.assertListEqual(actual_res_mid, expected_res_mid)

        expected_res_final = [
            TextNode("this is ", TextType.TEXT),
            TextNode("super", TextType.BOLD),
            TextNode(" cool", TextType.TEXT),
            TextNode("this is the code:", TextType.TEXT),
            TextNode("print('hello world')", TextType.CODE),
        ]

        self.assertListEqual(
            split_nodes_delimiter(actual_res_mid, "**", TextType.BOLD),
            expected_res_final,
        )

    def test_split_node_delimiter_nested(self):
        t = [TextNode("Hello world, _this is **super** cool_", TextType.TEXT)]
        expected_res_mid = [
            TextNode("Hello world, ", TextType.TEXT),
            TextNode("this is **super** cool", TextType.ITALIC),
        ]
        actual_res_mid = split_nodes_delimiter(t, "_", TextType.ITALIC)

        self.assertListEqual(actual_res_mid, expected_res_mid)

        expected_res_final = [
            TextNode("Hello world, ", TextType.TEXT),
            TextNode("this is ", TextType.ITALIC),
            TextNode("super", TextType.BOLD),
            TextNode(" cool", TextType.ITALIC),
        ]
        self.assertListEqual(
            split_nodes_delimiter(actual_res_mid, "**", TextType.BOLD),
            expected_res_final,
        )
