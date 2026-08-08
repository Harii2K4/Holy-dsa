from md_parser import BlockType, md_to_block, text_to_textnode, block_to_block_types
from htmlnode import HtmlNode, ParentNode, LeafNode
from textnode import text_node_to_html_node


def block_type_to_tag_and_normilize(
    block_type: BlockType, content: str
) -> tuple[str, str]:
    match block_type:
        case BlockType.HEADING:
            idx = 0
            while content[idx] == "#":
                idx += 1
            if not idx < 6:
                raise ValueError(f"Not a proper heading:{content}")
            return f"h{idx}", content[idx:]
        case BlockType.OL_LIST:
            res = []
            for line in content.split("\n"):
                res.append(line[3])
            return "ol", "\n".join(res)
        case BlockType.UL_LIST:
            res = []
            for line in content.split("\n"):
                res.append(line.strip("-"))
            return "ul", "\n".join(res)
        case BlockType.PARAGRAPH:
            return "p", content
        case BlockType.QUOTE:
            return "blockquote", content.lstrip(">")
        case BlockType.CODE:
            return "code", content.strip("```")
        case _:
            raise TypeError("Invalid block type")


def get_children(block_content: str, type: BlockType) -> list[HtmlNode]:
    lines = block_content.split("\n")
    split_textnodes = []
    for line in lines:
        split_textnodes.extend(text_to_textnode(line + " "))
    children = list(map(text_node_to_html_node, split_textnodes))
    if type == BlockType.UL_LIST or type == BlockType.OL_LIST:
        for child in children:
            if child.tag is None:
                child.tag = "li"

    return children


def md_to_html_nodes(md_text: str) -> ParentNode:
    # normilize the md(remove ending and starting newlines)
    norm_md = md_text.strip(" ").strip("\n") + "\n"

    blocks = md_to_block(norm_md)
    html_nodes = []
    for block in blocks:
        block_type = block_to_block_types(block)
        tag, norm_block = block_type_to_tag_and_normilize(block_type, content=block)
        if block_type == BlockType.CODE:
            html_nodes.append(
                ParentNode(tag="pre", children=[LeafNode(tag=tag, value=norm_block)])
            )
        else:
            html_nodes.append(
                ParentNode(tag=tag, children=get_children(norm_block, block_type))
            )

    root_node = ParentNode(tag="div", children=html_nodes)
    return root_node


md = """
            This is **bolded** paragraph
            text in a p
            tag here

            This is another paragraph with _italic_ text and `code` here
"""
# md = """
#         - one oh this has **bold** btw
#         - two
#         - three
# """
#
print(md_to_html_nodes(md).to_html())
