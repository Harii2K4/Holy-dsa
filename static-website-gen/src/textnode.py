from enum import Enum

from htmlnode import LeafNode


class TextType(Enum):
    TEXT = "text"
    BOLD = "bold"
    ITALIC = "italic"
    CODE = "code"
    LINK = "link"
    IMAGE = "image"


class TextNode:
    def __init__(
        self,
        content: str,
        type: TextType,
        link: str | None = None,
    ) -> None:

        self.content = content
        self.type = type
        self.link = link

    def __eq__(self, other: object, /) -> bool:
        if not isinstance(other, TextNode):
            raise TypeError(f"other should be of type Textnode not {type(other)}")

        isContentEqual = self.content == other.content
        isTypeEqual = self.type.value == other.type.value
        isLinkEqual = self.link == other.link

        return isContentEqual and isLinkEqual and isTypeEqual

    def __repr__(self) -> str:
        return f"TextNode({self.content}, {self.type.value}, {self.link})"


def text_node_to_html_node(text_node: TextNode) -> LeafNode:
    match text_node.type:
        case TextType.TEXT:
            return LeafNode(tag=None, value=text_node.content)
        case TextType.BOLD:
            return LeafNode(tag="strong", value=text_node.content)
        case TextType.ITALIC:
            return LeafNode(tag="em", value=text_node.content)
        case TextType.LINK:
            return LeafNode(
                tag="a", attributes={"href": text_node.link}, value=text_node.content
            )
        case TextType.IMAGE:
            return LeafNode(
                tag="img",
                attributes={"src": text_node.link, "alt": text_node.content},
                value="",
            )
        case TextType.CODE:
            return LeafNode(tag="code", value=text_node.content)
        case _:
            raise TypeError(f"Not a valid text type {text_node.type}")
