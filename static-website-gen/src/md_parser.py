from textnode import TextNode, TextType


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
            l, r = 0, 0
            n = len(node.content)
            content = node.content

            while r < n:
                try:
                    r = content.index(delimiter, l)
                except ValueError as v:
                    new_node_content = content[l:]
                    new_nodes.append(TextNode(new_node_content, node.type))
                    break

                new_node_content = content[l:r]
                # get content upto delimiter
                if new_node_content:
                    new_nodes.append(TextNode(new_node_content, node.type))
                # find the closing delimiter
                r = r + inc
                l = r
                try:
                    r = content.index(delimiter, l)
                except ValueError as v:
                    new_node_content = content[l - inc :]
                    new_nodes.append(TextNode(new_node_content, node.type))
                    break
                # get the content within the delimiters
                new_node_content = content[l:r]
                if new_node_content:
                    new_nodes.append(TextNode(new_node_content, type))
                r = r + inc
                l = r
        else:
            new_nodes.append(node)

    return new_nodes


t = TextNode("Hi this is a **Test Babes", TextType.TEXT)
t1 = TextNode("Hi this is a Test Babes", TextType.TEXT)
t2 = TextNode("**Hi** this is a Test Babes", TextType.TEXT)
t3 = TextNode("**", TextType.TEXT)
print(split_nodes_delimiter([t, t1, t2, t3], "**", TextType.BOLD))
