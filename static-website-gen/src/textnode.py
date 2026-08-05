from enum import Enum


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
        type: str,
        link: str | None = None,
    ) -> None:

        self.content = content
        self.type = type
        self.link = link

    def __eq__(self, other: object, /) -> bool:
        if not isinstance(other, TextNode):
            raise TypeError(f"other should be of type Textnode not {type(other)}")

        isContentEqual = self.content == other.content
        isTypeEqual = self.type == other.type
        isLinkEqual = self.link == other.link

        return isContentEqual and isLinkEqual and isTypeEqual

    def __repr__(self) -> str:
        return f"TextNode({self.content}, {self.type}, {self.link})"
