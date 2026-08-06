import unittest

from md_parser import (
    extract_markdown_images,
    extract_markdown_links,
    split_nodes_delimiter,
    split_nodes_image,
    split_nodes_link,
)
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


class TestExtractMDImages(unittest.TestCase):
    def test_extract_markdown_images_no_image(self):
        text = "This sentence contains no Markdown image."
        self.assertListEqual(extract_markdown_images(text), [])

    def test_extract_markdown_images_one_img(self):
        text = "![cat](cat.png)"
        self.assertListEqual(extract_markdown_images(text), [("cat", "cat.png")])

    def test_extract_markdown_images_one_img_space_sep(self):
        text = "![cat] (cat.png)"
        self.assertListEqual(extract_markdown_images(text), [("cat", "cat.png")])

    def test_extract_markdown_images_two_imgs(self):
        text = "![cat](cat.png) ![dog](dog.png)"
        self.assertListEqual(
            extract_markdown_images(text), [("cat", "cat.png"), ("dog", "dog.png")]
        )

    def test_extract_markdown_images_with_text(self):
        matches = extract_markdown_images(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png)"
        )
        self.assertListEqual([("image", "https://i.imgur.com/zjjcJKZ.png")], matches)


class TestExtractMDLinks(unittest.TestCase):
    def test_extract_markdown_link_multiple(self):
        text = "This is text with a link [to boot dev](https://www.boot.dev) and [to youtube](https://www.youtube.com/@bootdotdev)"
        self.assertListEqual(
            [
                ("to boot dev", "https://www.boot.dev"),
                ("to youtube", "https://www.youtube.com/@bootdotdev"),
            ],
            extract_markdown_links(text),
        )


class TextSplitTextNodeImages(unittest.TestCase):
    def test_split_images_one(self):
        node = TextNode(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_image([node])
        self.assertEqual(
            [
                TextNode("This is text with an ", TextType.TEXT),
                TextNode("image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png"),
            ],
            new_nodes,
        )

    def test_split_images_one_no_text(self):
        node = TextNode(
            "![image](https://i.imgur.com/zjjcJKZ.png)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_image([node])
        self.assertEqual(
            [
                TextNode("image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png"),
            ],
            new_nodes,
        )

    def test_split_images_one_newline(self):
        node = TextNode(
            "This here is our image:\n![image](https://i.imgur.com/zjjcJKZ.png)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_image([node])
        self.assertEqual(
            [
                TextNode("This here is our image:\n", TextType.TEXT),
                TextNode("image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png"),
            ],
            new_nodes,
        )

    def test_split_images_multiple(self):
        node = TextNode(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png) and another ![second image](https://i.imgur.com/3elNhQu.png)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("This is text with an ", TextType.TEXT),
                TextNode("image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png"),
                TextNode(" and another ", TextType.TEXT),
                TextNode(
                    "second image", TextType.IMAGE, "https://i.imgur.com/3elNhQu.png"
                ),
            ],
            new_nodes,
        )

    def test_split_images_but_link_ip(self):
        node = [
            TextNode(
                "This is text with an [link](https://i.imgur.com/)",
                TextType.TEXT,
            )
        ]
        new_nodes = split_nodes_image(node)
        self.assertEqual(
            node,
            new_nodes,
        )


class TextSplitTextNodeLinks(unittest.TestCase):
    def test_split_links_one(self):
        node = TextNode(
            "This is text with an [link](https://i.imgur.com/)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_link([node])
        self.assertEqual(
            [
                TextNode("This is text with an ", TextType.TEXT),
                TextNode("link", TextType.LINK, "https://i.imgur.com/"),
            ],
            new_nodes,
        )

    def test_split_links_multiple(self):
        node = TextNode(
            "This is text with an [link](https://i.imgur.com/) and another [link](https://i.imgur.com/)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_link([node])

        self.assertEqual(
            [
                TextNode("This is text with an ", TextType.TEXT),
                TextNode("link", TextType.LINK, "https://i.imgur.com/"),
                TextNode(" and another ", TextType.TEXT),
                TextNode("link", TextType.LINK, "https://i.imgur.com/"),
            ],
            new_nodes,
        )
