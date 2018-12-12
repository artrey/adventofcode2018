import typing

from ..base_linked_list import BaseLinkedList
from .list_iterator import ListIterator


class RoundedListIterator(ListIterator):
    def __init__(self, collection: BaseLinkedList) -> None:
        super().__init__(collection)
        self._head_visited = False

    def __next__(self) -> typing.Any:
        if self._curr.next == self._collection.head:
            if self._head_visited:
                raise StopIteration()
            else:
                self._head_visited = True
        return super().__next__()
