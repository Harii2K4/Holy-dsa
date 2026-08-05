import unittest

from textnode import TextNode


class TestTextNode(unittest.TestCase):
    def test_equal(self):
        t1 = TextNode(content="Hello world", type="text")
        t2 = TextNode(content="Hello world", type="text")
        self.assertEqual(t1, t2)

    def test_notequal(self):
        t1 = TextNode(content="Hello world", type="text")
        t2 = TextNode(content="this aint equal dawg", type="text")
        self.assertNotEqual(t1, t2)

    def test_no_url(self):
        t1 = TextNode(
            content="Hello world", type="link", link="https://www.boot.dev/lessons"
        )
        t2 = TextNode(content="Hello world", type="link")
        self.assertNotEqual(t1, t2)

    def test_diff_text_type(self):
        t1 = TextNode(content="Hello world", type="Bold")
        t2 = TextNode(content="Hello world", type="text")
        self.assertNotEqual(t1, t2)

    def test_invalid_object_type(self):
        t1 = TextNode(content="Hello world", type="Bold")
        with self.assertRaises(TypeError):
            self.assertNotEqual(t1, "Hello World")
