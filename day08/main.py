import typing
from utils.tree import Tree, TreeNode


def parse_node(data: typing.List[int], start_idx: int) -> typing.Tuple[int, TreeNode]:
    ret = TreeNode()

    children = data[start_idx]
    metadata = data[start_idx + 1]
    start_idx += 2

    for child in range(children):
        start_idx, node = parse_node(data, start_idx)
        ret.append_child(node)

    ret.data = data[start_idx: start_idx + metadata]

    return start_idx + metadata, ret


def extract_data() -> Tree:
    with open('input.txt', 'r') as fd:
        data = list(map(int, fd.read().strip().split()))
        return Tree(parse_node(data, 0)[1])


def node_metadata(node: TreeNode) -> int:
    return sum(node.data) + sum([node_metadata(child) for child in node.children])


def metadata_sum(data: Tree) -> int:
    return node_metadata(data.root)


def node_value(node: TreeNode) -> int:
    if node.children:
        count = len(node.children)
        unique_metadata = {v: node_value(node.children[v-1]) for v in node.data if v <= count}
        return sum([unique_metadata[v] for v in node.data if v <= count])
    else:
        return sum(node.data)


def root_value(data: Tree) -> int:
    return node_value(data.root)


if __name__ == '__main__':
    data = extract_data()
    print(metadata_sum(data))
    print(root_value(data))
