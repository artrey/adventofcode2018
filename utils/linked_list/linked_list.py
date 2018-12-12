import typing
from typing import Iterator

from .double_link_node import DListNode
from .base_linked_list import BaseLinkedList
from .list_iterator import ListIterator


class LinkedList(BaseLinkedList):
    def __init__(self) -> None:
        super().__init__()
        self._tail: typing.Optional[DListNode] = None

    def __repr__(self) -> str:
        """
        Return a string representation of the list.
        Takes O(n) time.
        """
        return f'[{", ".join(str(val) for val in self)}]'

    def __iter__(self) -> Iterator:
        return ListIterator(self)

    @property
    def tail(self) -> DListNode:
        return self._tail

    @tail.setter
    def tail(self, node: DListNode) -> None:
        self._tail = node

    def clear(self) -> None:
        super().clear()
        self._tail = None

    def set_single_node(self, node: DListNode) -> None:
        self._head = node
        self._tail = node
        self._count = 1

    def insert(self, data: typing.Any, after: DListNode) -> DListNode:
        """
        Insert a new element after the `after` node.
        Takes O(1) time.
        """
        if after == self._tail:
            return self.append(data)

        node = DListNode(data=data)
        node.prev = after
        node.next = after.next
        after.next.prev = node
        after.next = node
        self._count += 1
        return node

    def prepend(self, data: typing.Any) -> DListNode:
        """
        Insert a new element before the head and set head to it.
        Takes O(1) time.
        """
        node = DListNode(data=data)
        if self._count > 0:
            self._head.prev = node
            node.next = self._head
            self._head = node
            self._count += 1
        else:
            self.set_single_node(node)
        return node

    def append(self, data: typing.Any) -> DListNode:
        """
        Insert a new element after the tail and set tail to it.
        Takes O(1) time.
        """
        node = DListNode(data=data)
        if self._count > 0:
            self._tail.next = node
            node.prev = self._tail
            self._tail = node
            self._count += 1
        else:
            self.set_single_node(node)
        return node

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
        while curr is not None and curr.data != data:
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
            if self._head == node:
                self._head = node.next
                self._head.prev = None
            elif self._tail == node:
                self._tail = node.prev
                self._tail.next = None
            else:
                node.prev.next = node.next
                node.next.prev = node.prev
            self._count -= 1
        return node
