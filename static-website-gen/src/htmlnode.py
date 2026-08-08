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
        if not self.tag:
            assert self.value
            return self.value
        if self.tag == "img":
            return f"<{self.tag}{self.props_to_html()}>"
        assert self.value
        return f"<{self.tag}{self.props_to_html()}>{self.value}</{self.tag}>"

    def __repr__(self) -> str:
        content = ""
        if self.tag:
            content += f"\ntag:{self.tag},"
        content += f"\nvalue:{self.value},"
        if self.attributes:
            content += f"\nattr:{self.attributes}"
        return f"LeafNode({content}\n)"


class ParentNode(HtmlNode):
    def __init__(
        self,
        tag: str,
        children: list[HtmlNode],
        attributes: dict[str, Any] | None = None,
    ) -> None:
        super().__init__(tag, None, children, attributes)

    def __repr__(self) -> str:
        content = f"\ntag:{self.tag},"
        if self.value:
            content += f"\nvalue:{self.value}"
        if self.attributes:
            content += f"\nattr:{self.attributes}"
        content += f"\nchildren:{self.children}"
        return f"ParentNode({content}\n)"

    def to_html(self) -> str:
        if not self.tag:
            raise ValueError("Parent Nodes must have a tag")
        if not self.children:
            raise ValueError("Parent Nodes must have a children")

        if self.attributes:
            output = f"<{self.tag}{self.props_to_html()}>"
        else:
            output = f"<{self.tag}>"

        for child in self.children:
            output += child.to_html()

        return output + f"</{self.tag}>"


# list_ul = ParentNode(
#     tag="ul",
#     children=[
#         LeafNode("li", value="Item 1"),
#         LeafNode("li", value="Item 2"),
#         LeafNode("li", value="Item 3"),
#         LeafNode("li", value="Item 4"),
#         LeafNode("li", value="Item 5"),
#     ],
#     attributes={"style": "color:red;list-style:None"},
# )
# h1 = ParentNode(
#     tag="p",
#     children=[
#         LeafNode(None, value="This Is "),
#         LeafNode("b", value="Amazing "),
#         LeafNode(None, value="Bro"),
#     ],
# )
# body = ParentNode(
#     tag="body", children=[h1, list_ul], attributes={"style": "background-color:black"}
# )
# head = ParentNode(tag="head", children=[LeafNode("title", value="Statics")])
# html = ParentNode(tag="html", children=[head, body])
#
# with open("test.html", "w") as f:
#     f.write(html.to_html())
