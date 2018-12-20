import typing
from utils.graph import Graph, GraphNode
from utils.stack import Stack


Point = typing.Tuple[int, int]


def extract_data() -> Graph:
    with open('input.txt', 'r') as fd:
        regex = fd.readline()

    stack_left = Stack()
    stacks_right: typing.Dict[GraphNode, typing.List[GraphNode]] = {}
    connected_nodes: typing.Set[GraphNode] = set()

    graph = Graph()
    fake_node = GraphNode()
    prev_node = fake_node
    graph.edges[prev_node] = []

    count = len(regex)
    idx = 0

    while idx < count:
        c = regex[idx]
        if c == '(':
            stack_left.put(prev_node)
            stacks_right[prev_node] = []
        elif c == ')':
            some_node = stack_left.get()
            for n in stacks_right.pop(some_node):
                connected_nodes.add(n)
            connected_nodes.add(prev_node)
            prev_node = some_node
        elif c == '|':
            stacks_right[stack_left.look()].append(prev_node)
            prev_node = stack_left.look()
        elif c in 'NWSE':
            node = GraphNode(c)
            graph.edges[node] = [prev_node]
            graph.edges[prev_node].append(node)
            prev_node = node
        idx += 1

    for node in graph.edges[fake_node]:
        graph.edges[node].remove(fake_node)
    graph.edges.pop(fake_node)
    return graph


def furthest_room(graph: Graph) -> int:
    print(graph.edges)
    return 0


if __name__ == '__main__':
    data = extract_data()
    print(furthest_room(data))
