from collections import defaultdict
import typing
from utils.queue import PriorityQueue
from utils.graph import Point


class AreaRegion:
    def __init__(self, depth: int) -> None:
        self._index = -1
        self.level = -1
        self.type = -1
        self.depth = depth

    @property
    def index(self) -> int:
        return self._index

    @index.setter
    def index(self, value: int) -> None:
        self._index = value
        self.calc(self.depth)

    def calc(self, depth: int) -> None:
        self.level = (self._index + depth) % 20183
        self.type = self.level % 3

    def __repr__(self) -> str:
        return repr((self._index, self.level, self.type))


Map = typing.List[typing.List[AreaRegion]]


def extract_data() -> typing.Tuple[int, Point]:
    with open('input.txt', 'r') as fd:
        depth = int(fd.readline().strip().split(': ')[1])
        target: Point = tuple(map(int, fd.readline().strip().split(': ')[1].split(',')))
        return depth, target


def calc_area(depth: int, target: Point) -> Map:
    w, h = target
    w += 100
    h += 100
    area = [[AreaRegion(depth) for _ in range(w)] for _ in range(h)]

    area[0][0].index = 0

    for y in range(1, h):
        area[y][0].index = y * 48271

    for x in range(1, w):
        area[0][x].index = x * 16807

    for y in range(1, h):
        for x in range(1, w):
            if (x, y) == target:
                area[y][x].index = 0
            else:
                area[y][x].index = area[y-1][x].level * area[y][x-1].level

    return area


def calc_risk_level(area: Map, target: Point) -> int:
    w, h = target
    return sum(area[y][x].type for y in range(h+1) for x in range(w+1))


def area_risk_level(depth: int, target: Point) -> int:
    area = calc_area(depth, target)
    return calc_risk_level(area, target)


RegionDescription = typing.Tuple[int, int, int]


class Area:
    VALID_TYPES = {
        0: [1, 2],
        1: [0, 1],
        2: [0, 2]
    }

    def __init__(self, area: Map) -> None:
        self.edges: typing.Dict[RegionDescription, typing.Set[RegionDescription]] = defaultdict(set)

        self.width, self.height = len(area[0]), len(area)
        for y in range(self.height):
            for x in range(self.width):
                self.fill_node(area, x, y)

    def in_bounds(self, point: Point) -> bool:
        x, y = point
        return 0 <= x < self.width and 0 <= y < self.height

    def fill_node(self, area: Map, x: int, y: int) -> None:
        p1, p2 = self._fill_node(area, x, y)
        self.fill_neighbors(area, p1, p2)

    def _fill_node(self, area: Map, x: int, y: int) -> typing.Tuple[RegionDescription, RegionDescription]:
        e1, e2 = self.VALID_TYPES[area[y][x].type]
        p1 = (x, y, e1)
        p2 = (x, y, e2)
        self.edges[p1].add(p2)
        self.edges[p2].add(p1)
        return p1, p2

    def fill_neighbors(self, area: Map, a: RegionDescription, b: RegionDescription) -> None:
        for x, y in filter(self.in_bounds, [(a[0]-1, a[1]), (a[0]+1, a[1]), (a[0], a[1]-1), (a[0], a[1]+1)]):
            p1, p2 = self._fill_node(area, x, y)
            if p1[2] == a[2]:
                self.edges[a].add(p1)
                self.edges[p1].add(a)
            if p2[2] == a[2]:
                self.edges[a].add(p2)
                self.edges[p2].add(a)
            if p1[2] == b[2]:
                self.edges[b].add(p1)
                self.edges[p1].add(b)
            if p2[2] == b[2]:
                self.edges[b].add(p2)
                self.edges[p2].add(b)

    def neighbors(self, node: RegionDescription) -> typing.Set[RegionDescription]:
        return self.edges[node]

    def cost(self, a: RegionDescription, b: RegionDescription) -> int:
        return 1 if a[2] == b[2] else 7

    def heuristic(self, a: RegionDescription, b: RegionDescription) -> int:
        x1, y1, _ = a
        x2, y2, _ = b
        return abs(x1 - x2) + abs(y1 - y2)


def a_star_search(graph: Area, start: RegionDescription, goal: RegionDescription):
    frontier = PriorityQueue()
    frontier.put(start, 0)
    came_from: typing.Dict[RegionDescription, RegionDescription] = {start: None}
    cost_so_far: typing.Dict[RegionDescription, int] = {start: 0}

    while not frontier.empty():
        current = frontier.get()

        if current == goal:
            break

        for neighbor in graph.neighbors(current):
            new_cost = cost_so_far[current] + graph.cost(current, neighbor)
            if neighbor not in cost_so_far or new_cost < cost_so_far[neighbor]:
                cost_so_far[neighbor] = new_cost
                priority = new_cost + graph.heuristic(goal, neighbor)
                frontier.put(neighbor, priority)
                came_from[neighbor] = current

    return came_from, cost_so_far


def min_time(depth: int, target: Point) -> int:
    area = calc_area(depth, target)
    graph = Area(area)
    target_description = target[0], target[1], 2
    paths, costs = a_star_search(graph, (0, 0, 2), target_description)
    return costs[target_description]


if __name__ == '__main__':
    depth, target = extract_data()
    print(area_risk_level(depth, target))
    print(min_time(depth, target))
