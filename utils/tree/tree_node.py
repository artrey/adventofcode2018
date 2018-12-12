import typing
import utils.utils as utils


class TreeNode:
    """
    A node in a doubly-linked list.
    """
    def __init__(self,
                 data: typing.Any=None,
                 parent: typing.Optional['TreeNode']=None,
                 children: typing.Optional[typing.List['TreeNode']]=None) -> None:
        self.data = data
        self.parent = parent
        self.children: typing.List['TreeNode'] = [] if children is None else children

    @classmethod
    def create(cls, data: typing.Any) -> 'TreeNode':
        return data if isinstance(data, cls) else TreeNode(data)

    def append_child(self, node_data: typing.Any) -> 'TreeNode':
        node = TreeNode.create(node_data)
        self.children.append(node)
        node.parent = self
        return node

    def remove_child(self, node: 'TreeNode') -> 'TreeNode':
        self.children.remove(node)
        node.parent = None
        return node

    def __repr__(self) -> str:
        return f'{repr(self.data)} => {{{self.children}}}'

    def __str__(self) -> str:
        return str(self.data)

    def full_repr(self) -> str:
        return f'<TreeNode {utils.hex_id(self)}>' \
            f' [parent: {utils.none_or_hex_id(self.parent)} | children: {{{self.children}}}' \
            f' data: {repr(self.data)}'
