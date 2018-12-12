import re
import typing
from utils.linked_list import LinkedList


def extract_data() -> typing.List[typing.Tuple[str, str]]:
    with open('input.txt', 'r') as fd:
        ret = []
        for line in fd:
            m = re.match('Step ([A-Z]) must be finished before step ([A-Z]) can begin.', line)
            ret.append((m.group(1), m.group(2)))
        return ret


def task_dependencies(data: typing.List[typing.Tuple[str, str]]) -> typing.Dict[str, typing.List[str]]:
    dependencies = {}
    for parent, child in data:
        dependencies.setdefault(child, []).append(parent)

    initial = {node for node, _ in data}
    for node in initial.difference(dependencies):
        dependencies[node] = []

    return dependencies


def task_order(dependencies: typing.Dict[str, typing.List[str]]) -> typing.List[str]:
    ret = []
    resolved = set()
    tasks = sorted(dependencies.items(), key=lambda x: x[0])
    while tasks:
        for idx in range(len(tasks)):
            node, deps = tasks[idx]
            if all(d in resolved for d in deps):
                ret.append(node)
                resolved.add(node)
                tasks.pop(idx)
                break
    return ret


def workflow(data: typing.List[typing.Tuple[str, str]]) -> str:
    dependencies = task_dependencies(data)
    order = task_order(dependencies)
    return ''.join(order)


def task_time(task: str) -> int:
    return 61 + ord(task) - ord('A')


class Worker:
    def __init__(self) -> None:
        self._remain = 0
        self._task: typing.Any = None

    @property
    def remain(self) -> int:
        return self._remain

    @remain.setter
    def remain(self, value: int) -> None:
        self._remain = max(0, value)

    @property
    def idle(self) -> bool:
        return self._remain == 0

    @property
    def last_task(self):
        return self._task

    def set_work(self, time: int, task: typing.Any) -> None:
        self._remain = time
        self._task = task


class WorkersPool:
    def __init__(self, count: int) -> None:
        self.workers = [Worker() for _ in range(count)]

    def get_idle_worker(self) -> typing.Optional[Worker]:
        return next((w for w in self.workers if w.idle), None)

    def time_to_idle(self) -> int:
        return min([w.remain for w in self.workers if not w.idle], default=0)

    def time_to_finish(self) -> int:
        return max([w.remain for w in self.workers])

    def inc_time(self, count: int) -> typing.List[Worker]:
        ret = []
        for w in self.workers:
            if not w.idle:
                w.remain -= count
                if w.idle:
                    ret.append(w)
        return ret


def multiple_workflow_time(data: typing.List[typing.Tuple[str, str]]) -> int:
    workers = WorkersPool(5)

    dependencies = task_dependencies(data)

    tasks = LinkedList()
    for t in sorted(dependencies.items(), key=lambda x: x[0]):
        tasks.append(t)
    finished = set()

    time = 0
    while len(tasks) > 0:
        curr = tasks.head
        while curr is not None:
            task, deps = curr.data
            if all(d in finished for d in deps):
                w = workers.get_idle_worker()
                if w:
                    tasks.remove_node(curr)
                    w.set_work(task_time(task), task)
                else:
                    break
            curr = curr.next

        idle_time = workers.time_to_idle()
        time += idle_time
        for w in workers.inc_time(idle_time):
            finished.add(w.last_task)

    time += workers.time_to_finish()
    return time


if __name__ == '__main__':
    data = extract_data()
    print(workflow(data))
    print(multiple_workflow_time(data))
