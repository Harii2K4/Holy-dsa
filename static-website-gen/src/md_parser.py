import re
from enum import Enum

from textnode import TextNode, TextType


class BlockType(Enum):
    PARAGRAPH = "paragraph"
    HEADING = "heading"
    CODE = "code"
    QUOTE = "quote"
    UL_LIST = "ul_list"
    OL_LIST = "ol_list"


def test_valid_delimiter(delimiter: str, type: str) -> bool:
    match type:
        case "bold":
            return delimiter == "**"
        case "italic":
            return delimiter == "_"
        case "code":
            return delimiter == "`"
        case _:
            return False


def split_nodes_delimiter(
    old_nodes: list[TextNode], delimiter: str, type: TextType
) -> list[TextNode]:

    if not test_valid_delimiter(delimiter=delimiter, type=type.value):
        raise ValueError(f"Not the correct delimiter:{delimiter} for type:{type.value}")

    inc = 1
    if type == TextType.BOLD:
        inc = 2

    new_nodes = []

    for node in old_nodes:
        if delimiter in node.content:
            left, r = 0, 0
            n = len(node.content)
            content = node.content

            while r < n:
                try:
                    r = content.index(delimiter, left)
                except ValueError:
                    new_node_content = content[left:]
                    new_nodes.append(TextNode(new_node_content, node.type))
                    break

                new_node_content = content[left:r]
                # get content upto delimiter
                if new_node_content:
                    new_nodes.append(TextNode(new_node_content, node.type))
                # find the closing delimiter
                r = r + inc
                left = r
                try:
                    r = content.index(delimiter, left)
                except ValueError:
                    new_node_content = content[left - inc :]
                    new_nodes.append(TextNode(new_node_content, node.type))
                    break
                # get the content within the delimiters
                new_node_content = content[left:r]
                if new_node_content:
                    new_nodes.append(TextNode(new_node_content, type))
                r = r + inc
                left = r
        else:
            new_nodes.append(node)

    return new_nodes


def extract_markdown_images(text: str) -> list[tuple[str, str]]:

    alt_texts = re.findall(r"(?<=\!)\[(.*?)\](?= *\(.*?\))", text)
    img_links = re.findall(r"!\[[^\]]*\]\s*\((.*?)\)", text)

    return list(zip(alt_texts, img_links))


def extract_markdown_links(text: str) -> list[tuple[str, str]]:
    alt_texts = re.findall(r"\[(.*?)\](?= *\(.*?\))", text)
    links = re.findall(r"\[[^\]]*\]\s*\((.*?)\)", text)

    return list(zip(alt_texts, links))


def split_nodes_link(old_nodes: list[TextNode]) -> list[TextNode]:

    new_nodes = []
    for node in old_nodes:
        left = 0
        n = len(node.content)
        text = node.content
        while left < n:
            search_res = re.search(r"\[[^\]]*\]\s*\(.*?\)", text[left:])
            if not search_res:
                if left != 0:
                    new_nodes.append(TextNode(text[left:], node.type))
                else:
                    new_nodes.append(node)
                break

            start_idx = search_res.start() + left
            end_idx = search_res.end() + left

            if start_idx != left:
                new_nodes.append(TextNode(text[left:start_idx], node.type))

            alt_text, link = extract_markdown_links(text[start_idx:end_idx])[0]
            new_nodes.append(TextNode(alt_text, type=TextType.LINK, link=link))
            left = end_idx
    return new_nodes


def split_nodes_image(old_nodes: list[TextNode]) -> list[TextNode]:

    new_nodes = []
    for node in old_nodes:
        left = 0
        n = len(node.content)
        text = node.content
        iter = 1
        while left < n:
            search_res = re.search(r"!\[[^\]]*\]\s*\(.*?\)", text[left:])
            if not search_res:
                if left != 0:
                    new_nodes.append(TextNode(text[left:], node.type))
                else:
                    new_nodes.append(node)
                break

            start_idx = search_res.start() + left
            end_idx = search_res.end() + left
            # print(f"{iter}:({start_idx + left},{end_idx + left})")

            if start_idx != left:
                new_nodes.append(TextNode(text[left:start_idx], node.type))

            alt_text, image = extract_markdown_images(text[start_idx:end_idx])[0]
            new_nodes.append(TextNode(alt_text, type=TextType.IMAGE, link=image))
            left = end_idx
            iter += 1
    return new_nodes


def text_to_textnode(text: str) -> list[TextNode]:
    if not text:
        return [TextNode(content="", type=TextType.TEXT)]

    start_node = [TextNode(content=text, type=TextType.TEXT)]

    nodes_split_bold = split_nodes_delimiter(
        start_node, delimiter="**", type=TextType.BOLD
    )
    nodes_split_italic = split_nodes_delimiter(
        nodes_split_bold, delimiter="_", type=TextType.ITALIC
    )
    nodes_split_code = split_nodes_delimiter(
        nodes_split_italic, delimiter="`", type=TextType.CODE
    )

    node_split_images = split_nodes_image(nodes_split_code)
    node_split_links = split_nodes_link(node_split_images)

    return node_split_links


# we assume that the inputs are well written markdown and blocks are seperated by newlines
def md_to_block(text: str) -> list[str]:
    if not text:
        return [""]
    lines = text.strip(" ").split("\n")
    output_blocks = []

    if lines[0]:
        lines = [""] + lines
    if lines[-1]:
        lines.append("")

    left, right = 0, 1
    n = len(lines)
    while right < n:
        while right < n and lines[right].strip(" "):
            right += 1

        curr_block = [line.strip(" ").strip("\t") for line in lines[left + 1 : right]]
        output_blocks.append("\n".join(curr_block))
        left = right
        right += 1
    return output_blocks


def block_to_block_types(block: str) -> BlockType:

    if block.startswith("#"):
        idx = 0
        while block[idx] == "#":
            idx += 1
        if not idx < 6 or not block[idx] == " ":
            return BlockType.PARAGRAPH
        return BlockType.HEADING

    elif block.startswith("```") and block.endswith("```"):
        return BlockType.CODE
    elif block.startswith(">"):
        lines = block.split("\n")
        for line in lines[1:]:
            if not line.startswith(">"):
                return BlockType.PARAGRAPH
        return BlockType.QUOTE
    elif block.startswith("-"):
        lines = block.split("\n")
        for line in lines:
            if not (line.startswith("-") and line[1] == " "):
                return BlockType.PARAGRAPH
        return BlockType.UL_LIST
    elif block.startswith("1"):
        lines = block.split("\n")
        line_num = 1
        for line in lines:
            if not (
                line.startswith(str(line_num)) and line[1] == "." and line[2] == " "
            ):
                return BlockType.PARAGRAPH
            line_num += 1

        return BlockType.OL_LIST
    else:
        return BlockType.PARAGRAPH
