import typing


class Point:
    def __init__(self, x: int, y: int) -> None:
        self.x = x
        self.y = y

    def manhattan_length(self, x: int, y: int) -> int:
        return abs(self.x - x) + abs(self.y - y)

    def __repr__(self) -> str:
        return f'({self.x}, {self.y})'


class Bbox:
    def __init__(self):
        self.lt: typing.Optional[Point] = None
        self.rb: typing.Optional[Point] = None

    def extend(self, point: Point) -> None:
        if self.lt is None:
            self.lt = Point(point.x, point.y)
        if self.rb is None:
            self.rb = Point(point.x, point.y)

        self.lt.x = min(self.lt.x, point.x)
        self.lt.y = min(self.lt.y, point.y)
        self.rb.x = max(self.rb.x, point.x)
        self.rb.y = max(self.rb.y, point.y)

    def __repr__(self) -> str:
        return f'[{self.lt}, {self.rb}]'


def extract_data() -> typing.List[Point]:
    with open('input.txt', 'r') as fd:
        return [Point(*map(int, line.strip().split(', '))) for line in fd]


def bounding_box(points: typing.List[Point]) -> Bbox:
    bbox = Bbox()
    for point in points:
        bbox.extend(point)
    return bbox


def find_closest_point(points: typing.List[Point], x: int, y: int) -> typing.Optional[Point]:
    distances = {point: point.manhattan_length(x, y) for point in points}
    m = min(distances.items(), key=lambda x: x[1])
    distances.pop(m[0])
    if all([v > m[1] for v in distances.values()]):
        return m[0]
    return None


def manhattan_sum(points: typing.List[Point], x: int, y: int) -> int:
    return sum(point.manhattan_length(x, y) for point in points)


def largest_area(data: typing.List[Point]) -> int:
    bbox = bounding_box(data)
    areas = {}

    # exclude border
    for x in range(bbox.lt.x + 1, bbox.rb.x):
        for y in range(bbox.lt.y + 1, bbox.rb.y):
            point = find_closest_point(data, x, y)
            if point:
                areas[point] = areas.get(point, 0) + 1

    # exclude points on border (and points closest to border)
    for x in range(bbox.lt.x, bbox.rb.x + 1):
        point = find_closest_point(data, x, bbox.lt.y)
        if point and point in areas:
            areas.pop(point)
        point = find_closest_point(data, x, bbox.rb.y)
        if point and point in areas:
            areas.pop(point)
    for y in range(bbox.lt.y, bbox.rb.y + 1):
        point = find_closest_point(data, bbox.lt.x, y)
        if point and point in areas:
            areas.pop(point)
        point = find_closest_point(data, bbox.rb.x, y)
        if point and point in areas:
            areas.pop(point)

    return max(areas.values())


def specify_manhattan(data: typing.List[Point]) -> int:
    bbox = bounding_box(data)

    ret = 0
    for x in range(bbox.lt.x, bbox.rb.x + 1):
        for y in range(bbox.lt.y, bbox.rb.y + 1):
            if manhattan_sum(data, x, y) < 10000:
                ret += 1

    return ret


if __name__ == '__main__':
    data = extract_data()
    print(largest_area(data))
    print(specify_manhattan(data))
