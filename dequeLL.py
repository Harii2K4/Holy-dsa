from typing import Any


class Node:
    def __init__(
        self,
        val: Any | None = None,
        next: "Node | None " = None,
        prev: "Node | None" = None,
    ) -> None:
        self.val = val
        self.next = next
        self.prev = prev

    def set_next(self, node: "Node") -> None:
        self.next = node

    def set_prev(self, node: "Node") -> None:
        self.prev = node

    def __repr__(self) -> str:
        return str(self.val)


class LLDeque:
    def __init__(self, head: Node | None = None) -> None:
        self.head = head
        self.tail = head

    def __iter__(self):
        node = self.head
        while node:
            yield node
            node = node.next

    def add_to_tail(self, node: Node | None) -> None:
        if not self.head:
            self.head = node
            self.tail = self.head
            return

        if not isinstance(node, Node):
            raise ValueError(f"Node arg must be to type node recieved {type(node)}")

        if self.tail:
            self.tail.next = node
            self.tail = self.tail.next
        # Fallback: if some idiot set the tail of instance to None
        else:
            last_node = None
            for curr_node in self.__iter__():
                last_node = curr_node
            assert last_node
            last_node.next = node
            self.tail = last_node.next

    def add_to_head(self, node: Node | None = None) -> None:
        if not self.head:
            self.head = node
            self.tail = self.head
            return

        if isinstance(node, Node):
            node.next = self.head
            self.head = node
        else:
            raise ValueError(f"Node arg must be to type node recieved {type(node)}")

    def remove_from_head(self) -> None | Node:
        if not self.head:
            return None

        if not self.head.next:
            tmp = self.head
            self.head, self.tail = None, None
            return tmp

        tmp = self.head.next
        self.head.next = None
        res, self.head = self.head, tmp
        return res

    def remove_from_tail(self) -> None | Node:
        if not self.tail:
            return None
        if not self.tail.prev:
            tmp = self.tail
            self.tail, self.head = None, None
            return tmp

        tmp = self.tail
        self.tail = self.tail.prev
        self.tail.next = None
        return tmp

    def __repr__(self) -> str:
        nodes = []
        current = self.head
        while current and hasattr(current, "val"):
            nodes.append(str(current.val))
            current = current.next
        return "  ".join(nodes)


class deque:
    def __init__(self, items: list[Any] | None = None) -> None:
        self.lld = LLDeque()
        if not items:
            return

        if not isinstance(items, list):
            raise ValueError(f"Provide the arg items as a list recieved: {type(items)}")

        for item in items:
            self.lld.add_to_tail(item if isinstance(item, Node) else Node(item))

    def __repr__(self) -> str:
        return self.lld.__repr__()

    def pop_left(self) -> Any | None:
        node = self.lld.remove_from_head()
        return None if not node else node.val

    def peek_left(self) -> Any | None:
        node = self.lld.head
        return None if not node else node.val

    def append_left(self, item: Any = None) -> None:
        if not item:
            return

        item = Node(item) if not isinstance(item, Node) else item
        self.lld.add_to_head(item)

    def pop_right(self) -> Any | None:
        node = self.lld.remove_from_tail()
        return None if not node else node.val

    def peek_right(self) -> Any | None:
        node = self.lld.tail
        return None if not node else node.val

    def append_right(self, item: Any = None) -> None:
        if not item:
            return

        item = Node(item) if not isinstance(item, Node) else item
        self.lld.add_to_tail(item)

    def extend_right(self, items: list[Any]) -> None:
        for item in items:
            self.append_right(item)

    def is_empty(self) -> bool:
        return not self.lld.head and not self.lld.tail

    def __len__(self) -> int:
        count = 0
        if not self.lld.head:
            return 0
        tmp = self.lld.head
        while tmp:
            count += 1
            tmp = tmp.next
        return count


graph = {1: [3, 2], 2: [5, 1], 3: [6, 4, 1], 6: [3], 4: [3], 5: [2]}


def bfs(graph: dict[int, list[int]], start_idx: int) -> None:
    res = [start_idx]
    children = graph.get(start_idx, None)
    if not children:
        return

    d = deque(children)
    visited = set()
    visited.add(start_idx)

    while not d.is_empty():
        n = len(d)

        for _ in range(0, n):
            vertex = d.pop_left()
            if vertex:
                if vertex in visited:
                    continue
                res.append(vertex)
                visited.add(vertex)
                children = graph.get(vertex, None)
                if not children:
                    continue
                d.extend_right(children)

    print("->".join([str(v) for v in res]))


bfs(graph, 3)
