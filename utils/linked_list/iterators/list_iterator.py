import collections.abc
import typing

from ..double_link_node import DListNode
from ..base_linked_list import BaseLinkedList


class ListIterator(collections.abc.Iterator):
    def __init__(self, collection: BaseLinkedList) -> None:
        self._collection = collection
        self._curr = DListNode(next_node=collection.head)

    def __next__(self) -> typing.Any:
        if self._curr.next is None:
            raise StopIteration()
        self._curr = self._curr.next
        return self._curr.data
