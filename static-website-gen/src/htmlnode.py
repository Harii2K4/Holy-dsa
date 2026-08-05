from shlex import join
from typing import Any


class HtmlNode:
    def __init__(
        self,
        tag: str | None = None,
        value: str | None = None,
        children: list["HtmlNode"] | None = None,
        attributes: dict[str, Any] | None = None,
    ) -> None:
        self.tag = tag
        self.value = value
        self.children = children
        self.attributes = attributes

    def to_html(self) -> str:
        raise NotImplementedError(HtmlNode)

    def props_to_html(self) -> str:
        if self.attributes:
            return " " + " ".join(
                [f'{key}="{self.attributes[key]}"' for key in self.attributes]
            )
        return ""

    def __repr__(self) -> str:
        return f"HtmlNode(\ntag:{self.tag},\nvalue:{self.value},\nattr:{self.attributes},\nchildren:{self.children}\n)"


class LeafNode(HtmlNode):
    def __init__(
        self, tag: str | None, value: str, attributes: dict[str, Any] | None = None
    ) -> None:
        super().__init__(tag, value, None, attributes)

    def to_html(self) -> str:
        assert self.value
        if not self.tag:
            return self.value
        return f"<{self.tag}{self.props_to_html()}>{self.value}</{self.tag}>"
