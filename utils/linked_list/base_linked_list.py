from abc import ABC, abstractmethod
import collections.abc
import typing

from .double_link_node import DListNode


class BaseLinkedList(collections.abc.Iterable, ABC):
    def __init__(self) -> None:
        self._head: typing.Optional[DListNode] = None
        self._count = 0

    def __len__(self) -> int:
        return self._count

    def clear(self) -> None:
        self._head = None
        self._count = 0

    @property
    def head(self) -> DListNode:
        return self._head

    @head.setter
    def head(self, node: DListNode) -> None:
        self._head = node

    @abstractmethod
    def insert(self, data: typing.Any, after: DListNode) -> DListNode:
        pass

    @abstractmethod
    def prepend(self, data: typing.Any) -> DListNode:
        pass

    @abstractmethod
    def append(self, data: typing.Any) -> DListNode:
        pass

    @abstractmethod
    def find(self, data: typing.Any) -> typing.Optional[DListNode]:
        pass

    @abstractmethod
    def remove_node(self, node: DListNode) -> DListNode:
        pass

    def remove(self, data: typing.Any) -> typing.Optional[DListNode]:
        """
        Remove the first occurrence of `data` in the list.
        Takes O(n) time.
        """
        elem = self.find(data)
        if elem is not None:
            return self.remove_node(elem)
        return None
