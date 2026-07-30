from typing import Any
from user import User


class BSTNode:
    def __init__(self, val: Any = None) -> None:

        self.val = val
        self.left, self.right = None, None

    def insert(self, val: Any) -> None:
        if not val or not isinstance(val, User):
            return None

        if not self.val:
            self.val = val
            return None

        if self.val.id == val.id:
            return None

        if self.val.id > val.id:
            if not self.left:
                self.left = BSTNode(val)

            self = self.left
            self.insert(val)

        else:
            if not self.right:
                self.right = BSTNode(val)
            self = self.right
            self.insert(val)

    def get_min(self) -> Any:
        if not self.left:
            return self.val
        self = self.left
        return self.get_min()

    def get_right_min(self, node: "BSTNode") -> "BSTNode":
        if not node.left:
            return node
        return self.get_right_min(node.left)

    def get_max(self) -> Any:
        if not self.right:
            return self.val
        self = self.right
        return self.get_max()

    def delete(self, val: Any) -> "BSTNode|None":

        if not self:
            return None

        if not isinstance(val, User):
            return self

        # 3 Cases:
        if self.val.id == val.id:
            # if leaf node : Just delete
            if not self.left and not self.right:
                del self
                return None
            # only left subtree
            elif not self.right:
                return self.left
            # only right subtree
            elif not self.left:
                return self.right
            # both exist
            else:
                right_min = self.get_right_min(self.right)
                right_min.right = self.right.delete(right_min.val)
                right_min.left = self.left
                del self
                return right_min

        elif self.val.id > val.id:
            if self.left:
                self.left = self.left.delete(val)
            return self
        else:
            if self.right:
                self.right = self.right.delete(val)
            return self

    def preorder(self, visited: list[Any] = []) -> list[Any]:
        if not self.val:
            return []
        visited.append(self.val)
        if self.left:
            self.left.preorder(visited)
        if self.right:
            self.right.preorder(visited)
        return visited

    def postorder(self, visited: list[Any] = []) -> list[Any]:
        if not self.val:
            return []
        if self.left:
            self.left.postorder(visited)
        if self.right:
            self.right.postorder(visited)
        visited.append(self.val)
        return visited

    def inorder(self, visited: list[Any] = []) -> list[Any]:
        if not self.val:
            return []
        if self.left:
            self.left.inorder(visited)
        visited.append(self.val)
        if self.right:
            self.right.inorder(visited)
        return visited

    def exists(self, val: Any) -> bool:
        if not self.val:
            return False

        if self.val.id > val.id:
            return self.left.exists(val) if self.left else False
        elif self.val.id < val.id:
            return self.right.exists(val) if self.right else False
        else:
            return True

    def height(self) -> int:
        if not self.val:
            return 0
        if self.left:
            left_height = self.left.height()
        else:
            left_height = 0

        if self.right:
            right_height = self.right.height()
        else:
            right_height = 0

        return 1 + max(right_height, left_height)
