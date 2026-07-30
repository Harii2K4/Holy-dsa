from typing import Any


class Queue:
    def __init__(self, items: list[Any] | None = None) -> None:
        self.items = items if items else []
        self.items.reverse()

    def push(self, item: Any) -> None:
        self.items = [item] + self.items

    def pop(self) -> Any | None:
        if not self.items:
            return None
        return self.items.pop()

    def size(self) -> int:
        return len(self.items)

    def peek(self) -> Any | None:
        if not self.items:
            return None
        return self.items[-1]
