import typing

from ..double_link_node import DListNode
from ..base_linked_list import BaseLinkedList
from ..iterators import RoundedListIterator


class RoundedLinkedList(BaseLinkedList):
    def __repr__(self) -> str:
        """
        Return a string representation of the list.
        Takes O(n) time.
        """
        return f'[{", ".join(str(val) for val in self)}]'

    def __iter__(self) -> typing.Iterator:
        return RoundedListIterator(self)

    def set_single_head(self, node: DListNode) -> DListNode:
        self._head = node
        self._head.next = self._head
        self._head.prev = self._head
        self._count = 1
        return node

    def insert_after(self, node: DListNode, after: DListNode) -> DListNode:
        node.prev = after
        node.next = after.next
        after.next.prev = node
        after.next = node
        self._count += 1
        return node

    def insert(self, data: typing.Any, after: DListNode) -> DListNode:
        """
        Insert a new element after the `after` node.
        Takes O(1) time.
        """
        return self.insert_after(DListNode(data=data), after)

    def prepend(self, data: typing.Any) -> DListNode:
        """
        Insert a new element before the head and set head to it.
        Takes O(1) time.
        """
        if self._count == 0:
            return self.set_single_head(DListNode(data))
        self._head = self.insert(data, self._head.prev)
        return self._head

    def append(self, data: typing.Any) -> DListNode:
        """
        Insert a new element before the head (after the tail).
        Takes O(1) time.
        """
        if self._count == 0:
            return self.set_single_head(DListNode(data))
        return self.insert(data, self._head.prev)

    def find(self, data: typing.Any) -> typing.Optional[DListNode]:
        """
        Search for the first element with `data` matching.
        Return the element or `None` if not found.
        Takes O(n) time.
        """
        if self._count == 0:
            return None

        curr = self._head
        idx = 0
        while idx < self._count and curr.data != data:
            curr = curr.next
            idx += 1

        if idx < self._count:
            return curr

        return None

    def remove_node(self, node: DListNode) -> DListNode:
        """
        Unlink an element from the list and return it.
        Takes O(1) time.
        """
        if self._count == 1:
            self.clear()
        else:
            node.prev.next = node.next
            node.next.prev = node.prev
            self._count -= 1
        return node
