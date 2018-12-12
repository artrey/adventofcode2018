import typing
from .tree_node import TreeNode


class Tree:
    def __init__(self, root_data: typing.Any=None) -> None:
        self._root = TreeNode.create(root_data)

    @property
    def root(self) -> TreeNode:
        return self._root

    def __repr__(self) -> str:
        return repr(self._root)
