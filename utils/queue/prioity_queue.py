import heapq
import typing


class PriorityQueue:
    def __init__(self) -> None:
        self.elements = []

    def empty(self) -> bool:
        return len(self.elements) == 0

    def put(self, item: typing.Any, priority: typing.Any) -> None:
        heapq.heappush(self.elements, (priority, item))

    def get(self) -> typing.Any:
        return heapq.heappop(self.elements)[1]
