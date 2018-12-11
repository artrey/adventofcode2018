import typing
import utils.utils as utils


class DListNode:
    """
    A node in a doubly-linked list.
    """
    def __init__(self,
                 data: typing.Any=None,
                 prev_node: typing.Optional['DListNode']=None,
                 next_node: typing.Optional['DListNode']=None) -> None:
        self.data = data
        self.prev = prev_node
        self.next = next_node

    def __repr__(self) -> str:
        return repr(self.data)

    def __str__(self) -> str:
        return str(self.data)

    def full_repr(self) -> str:
        return f'<DListNode {utils.hex_id(self)}>' \
            f' [prev: {utils.none_or_hex_id(self.prev)} | next: {utils.none_or_hex_id(self.next)}' \
            f' data: {repr(self.data)}'
