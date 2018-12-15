import typing


class GraphNode:
    def __init__(self, data: typing.Any = None) -> None:
        self.data = data

    def __repr__(self) -> str:
        return repr(self.data)

    def __str__(self) -> str:
        return str(self.data)
