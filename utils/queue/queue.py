import collections
import typing


class Queue:
    def __init__(self) -> None:
        self.elements = collections.deque()

    def empty(self) -> bool:
        return len(self.elements) == 0

    def put(self, x: typing.Any) -> None:
        self.elements.append(x)

    def get(self) -> typing.Any:
        return self.elements.popleft()
