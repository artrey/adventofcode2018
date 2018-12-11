import re
import typing


def extract_data() -> typing.List[typing.Tuple[str, str]]:
    with open('input.txt', 'r') as fd:
        ret = []
        for line in fd:
            m = re.match('Step ([A-Z]) must be finished before step ([A-Z]) can begin.', line)
            ret.append((m.group(1), m.group(2)))
        return ret


def workflow(data: typing.List[typing.Tuple[str, str]]) -> str:
    dependencies = {}
    for parent, child in data:
        dependencies.setdefault(child, []).append(parent)

    initial = {node for node, _ in data}
    for node in initial.difference(dependencies):
        dependencies[node] = []

    ret = []
    resolved = set()

    dependencies = sorted(dependencies.items(), key=lambda x: x[0])
    while dependencies:
        for idx in range(len(dependencies)):
            node, deps = dependencies[idx]
            if all(d in resolved for d in deps):
                ret.append(node)
                resolved.add(node)
                dependencies.pop(idx)
                break

    return ''.join(ret)


if __name__ == '__main__':
    data = extract_data()
    print(workflow(data))
