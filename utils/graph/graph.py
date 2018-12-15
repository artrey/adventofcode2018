import typing
from .graph_node import GraphNode


class Graph:
    def __init__(self):
        self.edges: typing.Dict[GraphNode, typing.List[GraphNode]] = {}

    def neighbors(self, node: GraphNode) -> typing.List[GraphNode]:
        return self.edges[node]
