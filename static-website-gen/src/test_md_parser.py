import unittest

from md_parser import (
    BlockType,
    block_to_block_types,
    md_to_block,
    extract_markdown_images,
    extract_markdown_links,
    split_nodes_delimiter,
    split_nodes_image,
    split_nodes_link,
    text_to_textnode,
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

        self.assertListEqual(res, split_nodes_delimiter(t, "**", TextType.BOLD))

    def test_split_node_delimiter_bold_end(self):
        t = [TextNode("world **hello**", TextType.TEXT)]
        res = [TextNode("world ", TextType.TEXT), TextNode("hello", TextType.BOLD)]

        self.assertListEqual(res, split_nodes_delimiter(t, "**", TextType.BOLD))

    def test_split_node_delimiter_bold_middle(self):
        t = [TextNode("world **hello** end", TextType.TEXT)]
        res = [
            TextNode("world ", TextType.TEXT),
            TextNode("hello", TextType.BOLD),
            TextNode(" end", TextType.TEXT),
        ]

        self.assertListEqual(res, split_nodes_delimiter(t, "**", TextType.BOLD))

    def test_split_node_delimiter_bold_no_closing_delimt(self):

        t = [TextNode("**hello end", TextType.TEXT)]
        res = [TextNode("**hello end", TextType.TEXT)]

        self.assertListEqual(res, split_nodes_delimiter(t, "**", TextType.BOLD))

    def test_split_node_delimiter_italic_start(self):

        t = [TextNode("_hello_ end", TextType.TEXT)]
        res = [TextNode("hello", TextType.ITALIC), TextNode(" end", TextType.TEXT)]

        self.assertListEqual(res, split_nodes_delimiter(t, "_", TextType.ITALIC))

    def test_split_node_delimiter_italic_middle(self):

        t = [TextNode("woah _hello_ end", TextType.TEXT)]
        res = [
            TextNode("woah ", TextType.TEXT),
            TextNode("hello", TextType.ITALIC),
            TextNode(" end", TextType.TEXT),
        ]

        self.assertListEqual(res, split_nodes_delimiter(t, "_", TextType.ITALIC))

    def test_split_node_delimiter_code_end(self):

        t = [TextNode("this is the code:```print('hello world')```", TextType.TEXT)]
        res = [
            TextNode("this is the code:", TextType.TEXT),
            TextNode("print('hello world')", TextType.CODE),
        ]

        self.assertListEqual(res, split_nodes_delimiter(t, "`", TextType.CODE))

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
            expected_res_final,
            split_nodes_delimiter(actual_res_mid, "**", TextType.BOLD),
        )


class TestExtractMDImages(unittest.TestCase):
    def test_extract_markdown_images_no_image(self):
        text = "This sentence contains no Markdown image."
        self.assertListEqual([], extract_markdown_images(text))

    def test_extract_markdown_images_one_img(self):
        text = "![cat](cat.png)"
        self.assertListEqual([("cat", "cat.png")], extract_markdown_images(text))

    def test_extract_markdown_images_one_img_space_sep(self):
        text = "![cat] (cat.png)"
        self.assertListEqual([("cat", "cat.png")], extract_markdown_images(text))

    def test_extract_markdown_images_two_imgs(self):
        text = "![cat](cat.png) ![dog](dog.png)"
        self.assertListEqual(
            extract_markdown_images(text), [("cat", "cat.png"), ("dog", "dog.png")]
        )

    def test_extract_markdown_images_with_text(self):
        matches = extract_markdown_images(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png)"
        )
        self.assertListEqual(matches, [("image", "https://i.imgur.com/zjjcJKZ.png")])


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


class TestTexttoTestNode(unittest.TestCase):
    def test_text_to_TestNode(self):
        text = "This is **text** with an _italic_ word and a `code block` and an ![obi wan image](https://i.imgur.com/fJRm4Vk.jpeg) and a [link](https://boot.dev)"
        expected_res = [
            TextNode("This is ", TextType.TEXT),
            TextNode("text", TextType.BOLD),
            TextNode(" with an ", TextType.TEXT),
            TextNode("italic", TextType.ITALIC),
            TextNode(" word and a ", TextType.TEXT),
            TextNode("code block", TextType.CODE),
            TextNode(" and an ", TextType.TEXT),
            TextNode(
                "obi wan image", TextType.IMAGE, "https://i.imgur.com/fJRm4Vk.jpeg"
            ),
            TextNode(" and a ", TextType.TEXT),
            TextNode("link", TextType.LINK, "https://boot.dev"),
        ]

        self.assertListEqual(expected_res, text_to_textnode(text))


class TestMdToBlock(unittest.TestCase):
    def test_md_block_proper_blocks(self):
        md = """This is **bolded** paragraph

This is another paragraph with _italic_ text and `code` here
This is the same paragraph on a new line

- This is a list
- with items
"""

        blocks = md_to_block(md)

        self.assertEqual(
            [
                "This is **bolded** paragraph",
                "This is another paragraph with _italic_ text and `code` here\nThis is the same paragraph on a new line",
                "- This is a list\n- with items",
            ],
            blocks,
        )

    def test_md_block_empty(self):
        md = ""
        blocks = md_to_block(md)
        self.assertListEqual([""], blocks)

    def test_md_block_multiple_newline(self):
        md = "\n\n\n\n"
        blocks = md_to_block(md)
        self.assertListEqual(["", "", "", ""], blocks)

    def test_md_block_leading_and_trailing_spaces_and_tabs(self):
        md = """          This is **bolded** paragraph

        This is another paragraph with _italic_ text and `code` here
        This is the same paragraph on a new line

- This is a list
- with items
           """

        blocks = md_to_block(md)

        self.assertEqual(
            [
                "This is **bolded** paragraph",
                "This is another paragraph with _italic_ text and `code` here\nThis is the same paragraph on a new line",
                "- This is a list\n- with items",
            ],
            blocks,
        )

    def test_md_block_with_code(self):

        md = """
        #### Number Conversion:

Js converts everything to numbers like everything so we can get stuff like this

```js
true == '1'
```
"""
        blocks = md_to_block(md)

        self.assertEqual(
            [
                "#### Number Conversion:",
                "Js converts everything to numbers like everything so we can get stuff like this",
                "```js\ntrue == '1'\n```",
            ],
            blocks,
        )


class TestBlockToBlockType(unittest.TestCase):
    def test_block_to_block_types_proper_blocks(self):

        md = """## This is **bolded** paragraph

        This is another paragraph with _italic_ text and `code` here
        This is the same paragraph on a new line

        - This is a list
        - with items
        """
        blocks = md_to_block(md)
        block_types = list(map(block_to_block_types, blocks))
        res_expected = [BlockType.HEADING, BlockType.PARAGRAPH, BlockType.UL_LIST]
        self.assertListEqual(res_expected, block_types)

    def test_block_to_block_types_invalid_heading_and_ul(self):

        md = """##This is **bolded** paragraph

        This is another paragraph with _italic_ text and `code` here
        This is the same paragraph on a new line

        -This is a list
        -with items
        """
        blocks = md_to_block(md)
        block_types = list(map(block_to_block_types, blocks))
        res_expected = [BlockType.PARAGRAPH, BlockType.PARAGRAPH, BlockType.PARAGRAPH]
        self.assertListEqual(res_expected, block_types)

    def test_block_to_block_types_code(self):

        md = """``` python
        listT=[1,2,3,4,5]
        print(listT) ```
        """
        blocks = md_to_block(md)
        block_types = list(map(block_to_block_types, blocks))
        res_expected = [BlockType.CODE]
        self.assertListEqual(res_expected, block_types)

    def test_block_to_block_valid_block_type(self):

        md = """``` python
        listT=[1,2,3,4,5]
        print(listT) ```
        """
        blocks = md_to_block(md)
        block_types = list(map(block_to_block_types, blocks))
        res_expected = [BlockType.CODE]
        self.assertListEqual(res_expected, block_types)

    def test_block_to_block_invalid_block_type(self):

        md = """``` python
        listT=[1,2,3,4,5]
        print(listT)
        """
        blocks = md_to_block(md)
        block_types = list(map(block_to_block_types, blocks))
        res_expected = [BlockType.PARAGRAPH]
        self.assertListEqual(res_expected, block_types)

    def test_md_block_to_block_type_ol_valid(self):
        md = """
        # This is a List

        1. python
        2. c
        3. go
        4. ts
        """
        blocks = md_to_block(md)
        block_types = list(map(block_to_block_types, blocks))
        res_expected = [BlockType.HEADING, BlockType.OL_LIST]
        self.assertListEqual(res_expected, block_types)

    def test_md_block_to_block_type_ol_invalid_wrong_numbering(self):
        md = """
        # This is a List

        1. python
        3. go
        4. ts
        """
        blocks = md_to_block(md)
        block_types = list(map(block_to_block_types, blocks))
        res_expected = [BlockType.HEADING, BlockType.PARAGRAPH]
        self.assertListEqual(res_expected, block_types)

    def test_md_block_to_block_type_quoted(self):
        md = """
        # This is a quote with space

        > Life is race that i intend to enjoy

        # This is a quote without space

        >Life is race that i intend to enjoy
        """
        blocks = md_to_block(md)
        block_types = list(map(block_to_block_types, blocks))
        res_expected = [
            BlockType.HEADING,
            BlockType.QUOTE,
            BlockType.HEADING,
            BlockType.QUOTE,
        ]
        self.assertListEqual(res_expected, block_types)

    def test_md_block_to_block_type_actual_example_from_obsidian(self):
        md = """
        ## Comparisons:

Comparisons are a very useful part of conditionals and are used a lot in conditionals

#### String Comparisons:

 JavaScript uses the so-called “dictionary” or “lexicographical” order.Each char of each string is compared inorder until the end of the strings,
 if all the chars are equal then,longer string is greater or equal length means equal

It is not really dictionary order it is unicode value order for each char so
'A' > 'a'  is false as A->65 and a ->97

#### Number Conversion:

Js converts everything to numbers like everything so we can get stuff like this

```js
true == '1'
```

because true -> 1 and '1'-> 1 and since it is == and not === (true equals) it works.
something also funny is this.
        """
        blocks = md_to_block(md)
        self.assertEqual(9, len(blocks))
        block_types = [block_to_block_types(block) for block in blocks]
        expected_res = [
            BlockType.HEADING,
            BlockType.PARAGRAPH,
            BlockType.HEADING,
            BlockType.PARAGRAPH,
            BlockType.PARAGRAPH,
            BlockType.HEADING,
            BlockType.PARAGRAPH,
            BlockType.CODE,
            BlockType.PARAGRAPH,
        ]
        self.assertListEqual(expected_res, block_types)
