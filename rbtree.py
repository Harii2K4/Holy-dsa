from typing import Any


class RBNode:
    def __init__(
        self,
        val: Any = None,
        parent: "RBNode|None" = None,
    ) -> None:
        self.val = val
        self.red = False
        # Reason is then you can do self.left.red because None.red is kinda weird no?
        self.left: "RBNode" = self
        self.right: "RBNode" = self
        self.parent: "RBNode|None" = parent


class RBTree:
    def __init__(self) -> None:
        self.nil = RBNode(None)
        self.root = self.nil

    def insert(self, val: Any) -> None:
        node = RBNode(val)
        node.left, node.right = self.nil, self.nil
        node.red = True

        if not self.root.val:
            node.red = False
            self.root = node
            return

        parent = self.find_parent(self.root, val, node)

        if not parent:
            return None
        # assign to parent
        node.parent = parent

        self.fix_insert(node)

    def find_parent(self, root: "RBNode", val: Any, node: "RBNode") -> RBNode | None:
        if root.val == val:
            return None
        elif root.val > val:
            if not root.left.val:
                root.left = node
                return root
            return self.find_parent(root.left, val, node)
        else:
            if not root.right.val:
                root.right = node
                return root
            return self.find_parent(root.right, val, node)

    def fix_insert(self, new_node: RBNode) -> None:
        curr_node = new_node

        while curr_node != self.root and curr_node.parent.red:
            parent = curr_node.parent
            assert parent is not None
            grandparent = parent.parent

            # new node is the child of root No need to do anything
            if not grandparent:
                return

            elif grandparent.left == parent:
                uncle = grandparent.right
                if uncle.red:
                    # no rotations needed
                    uncle.red, parent.red = False, False
                    grandparent.red = True
                    curr_node = grandparent
                else:
                    if parent.right == curr_node:
                        curr_node = parent
                        self.rotate_left(curr_node)
                        parent = curr_node.parent
                        assert parent is not None

                    parent.red = False
                    grandparent.red = True
                    self.rotate_right(grandparent)

            elif grandparent.right == parent:
                uncle = grandparent.left
                if uncle.red:
                    uncle.red, parent.red = False, False
                    grandparent.red = True
                    curr_node = grandparent
                else:
                    if parent.left == curr_node:
                        curr_node = parent
                        self.rotate_right(curr_node)
                        parent = curr_node.parent
                        assert parent is not None

                    parent.red = False
                    grandparent.red = True
                    self.rotate_left(grandparent)

            self.root.red = False

    def rotate_left(self, pivot_parent: RBNode) -> None:
        if not pivot_parent.val or not pivot_parent.right:
            return None
        pivot = pivot_parent.right
        pivot_parent.right, pivot.left = pivot.left, pivot_parent

        if not pivot_parent.parent:
            self.root = pivot
        elif pivot_parent.parent.left == pivot_parent:
            pivot_parent.parent.left = pivot
        else:
            pivot_parent.parent.right = pivot

        # Set parents
        if pivot_parent.right.val:
            pivot_parent.right.parent = pivot_parent

        pivot.parent = pivot_parent.parent
        pivot_parent.parent = pivot

    def rotate_right(self, pivot_parent: RBNode) -> None:
        if not pivot_parent.val or not pivot_parent.left:
            return None
        pivot = pivot_parent.left
        pivot_parent.left, pivot.right = pivot.right, pivot_parent

        if not pivot_parent.parent:
            self.root = pivot
        elif pivot_parent.parent.left == pivot_parent:
            pivot_parent.parent.left = pivot
        else:
            pivot_parent.parent.right = pivot

        # Set parents
        if pivot_parent.left.val:
            pivot_parent.left.parent = pivot_parent

        pivot.parent = pivot_parent.parent
        pivot_parent.parent = pivot


def inorder(node: "RBNode") -> None:
    if not node.val:
        # print("Nil", "red" if node.red else "black")
        return None
    inorder(node.left)
    print(node.val, "red" if node.red else "black")
    inorder(node.right)


def preorder(node: "RBNode") -> None:
    if not node.val:
        # print("Nil", "red" if node.red else "black")
        return None
    print(node.val, "red" if node.red else "black")
    preorder(node.left)
    preorder(node.right)


tree = RBTree()
tree.insert(7)
tree.insert(2)
tree.insert(8)
tree.insert(1)
tree.insert(3)
tree.insert(5)
tree.insert(6)
# tree.insert(4)
# tree.insert(3)
# tree.insert(5)
# tree.rotate_right(tree.root)
# inorder(tree.root)
print("-----------------")
preorder(tree.root)
