from md_parser import BlockType, md_to_block, text_to_textnode, block_to_block_types
from htmlnode import HtmlNode, ParentNode, LeafNode
from textnode import text_node_to_html_node


def normilize_block(content: str, type: BlockType) -> str:
    match type:
        case BlockType.HEADING:
            idx = 0
            while content[idx] == "#":
                idx += 1
            if not idx < 6:
                raise ValueError(f"Not a proper heading:{content}")
            return content[idx + 1 :].lstrip(" ")
        case BlockType.OL_LIST:
            res = []
            for line in content.split("\n"):
                res.append(line[3:].lstrip(" "))
            return "\n".join(res)
        case BlockType.UL_LIST:
            res = []
            for line in content.split("\n"):
                res.append(line.strip("-").lstrip(" "))
            return "\n".join(res)
        case BlockType.PARAGRAPH:
            return content.lstrip(" ")
        case BlockType.QUOTE:
            res = []
            for line in content.split("\n"):
                res.append(line.lstrip(">").lstrip(" "))
            return "\n".join(res)
        case BlockType.CODE:
            return content.strip("```")
        case _:
            raise TypeError("Invalid block type")


def block_type_to_tag(block_type: BlockType, content: str) -> str:
    match block_type:
        case BlockType.HEADING:
            idx = 0
            while content[idx] == "#":
                idx += 1
            if not idx < 6:
                raise ValueError(f"Not a proper heading:{content}")
            return f"h{idx}"
        case BlockType.OL_LIST:
            return "ol"
        case BlockType.UL_LIST:
            return "ul"
        case BlockType.PARAGRAPH:
            return "p"
        case BlockType.QUOTE:
            return "blockquote"
        case BlockType.CODE:
            return "code"
        case _:
            raise TypeError("Invalid block type")


def get_children(block_content: str, type: BlockType) -> list[HtmlNode]:
    lines = block_content.split("\n")
    result_nodes = []
    for line in lines:
        text_nodes = text_to_textnode(line + " ")
        children_nodes = list(map(text_node_to_html_node, text_nodes))
        if type == BlockType.UL_LIST or type == BlockType.OL_LIST:
            result_nodes.append(ParentNode("li", children=children_nodes))
        else:
            result_nodes.extend(children_nodes)
    print(result_nodes)

    return result_nodes


def md_to_html_nodes(md_text: str) -> ParentNode:
    # normilize the md(remove ending and starting newlines)
    norm_md = md_text.strip(" ").strip("\n") + "\n"

    blocks = md_to_block(norm_md)

    atomic_blocks = []
    for block in blocks:
        block_type = block_to_block_types(block)
        if block_type == BlockType.HEADING:
            atomic_blocks.extend(block.split("\n"))
        else:
            atomic_blocks.append(block)

    html_nodes = []
    for block in atomic_blocks:
        block_type = block_to_block_types(block)
        tag = block_type_to_tag(block_type, content=block)
        norm_block = normilize_block(block, block_type)
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
