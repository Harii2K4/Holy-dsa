# import unittest
# from md_to_html_nodes import md_to_html_nodes
#
#
# class TestMdToHtml(unittest.TestCase):
#     def test_paragraphs(self):
#         md = """
#             This is **bolded** paragraph
#             text in a p
#             tag here
#
#             This is another paragraph with _italic_ text and `code` here
# """
#
#         node = md_to_html_nodes(md)
#         html = node.to_html()
#         self.assertEqual(
#             "<div><p>This is <strong>bolded</strong> paragraph text in a p tag here </p><p>This is another paragraph with <em>italic</em> text and <code>code</code> here </p></div>",
#             html,
#         )
#
#     def test_codeblock(self):
#         md = """ ```
#         This is text that _should_ remain
#         the **same** even with inline stuff
#         ```
# """
#
#         node = md_to_html_nodes(md)
#         html = node.to_html()
#         self.assertEqual(
#             "<div><pre><code>\nThis is text that _should_ remain\nthe **same** even with inline stuff\n</code></pre></div>",
#             html,
#         )
#
#     def test_with_blockquotes(self):
#         md = """
#         # This is a heading
#
#         > this is **quoted** bold
#
#         ```
#         This is text that _should_ remain
#         the **same** even with inline stuff
#         ```
# """
#
#         node = md_to_html_nodes(md)
#         html = node.to_html()
#         self.assertEqual(
#             "<div><h1> This is a heading </h1><blockquote> this is <strong>quoted</strong> bold </blockquote><pre><code>\nThis is text that _should_ remain\nthe **same** even with inline stuff\n</code></pre></div>",
#             html,
#         )
#
#     def test_unordered_list(self):
#         md = """
#                 - one
#                 - two
#         """
#         node = md_to_html_nodes(md)
#         html = node.to_html()
#         self.assertEqual(
#             "<div><ul><li> one </li><li> two </li></ul></div>",
#             html,
#         )
