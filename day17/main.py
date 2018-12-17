import os
import typing
from utils.geometry import Bbox, Point


Map = typing.List[typing.List[str]]


class Underground:
    def __init__(self, underground: Map, start: Point) -> None:
        self.map = underground
        self.start = start
        self.cache: typing.Dict[typing.Tuple[int, int], typing.Tuple[int, bool]] = {}

    @property
    def width(self):
        return len(self.map[0])

    @property
    def height(self):
        return len(self.map)

    def fill(self) -> int:
        w, _ = self.fill_down(self.start)
        for x in range(self.width):
            if self.map[0][x] in '|~':
                w -= 1
                self.map[0][x] = '.'
            if self.map[self.height - 1][x] in '|~':
                w -= 1
                self.map[self.height - 1][x] = '.'
        return w

    def fill_down(self, point: Point) -> typing.Tuple[int, bool]:
        key = point.x, point.y
        if key not in self.cache:
            self.cache[key] = self.fill_down_impl(point)
        return self.cache[key]

    def fill_down_impl(self, point: Point) -> typing.Tuple[int, bool]:
        water_tiles = 0
        bottom = self.height
        x = point.x
        for y in range(point.y, self.height):
            if self.map[y][x] == '#':
                break

            if self.map[y][x] == '.':
                water_tiles += 1
            self.map[y][x] = '|'
            bottom = y
        else:
            return water_tiles, True

        for y in range(bottom, point.y, -1):
            infinite = False
            if x > 0 and self.map[y][x - 1] != '#':
                w, inf = self.fill_left(Point(x - 1, y))
                infinite |= inf
                water_tiles += w
            if x + 1 < self.width and self.map[y][x + 1] != '#':
                w, inf = self.fill_right(Point(x + 1, y))
                infinite |= inf
                water_tiles += w
            if infinite:
                return water_tiles, True

        return water_tiles, False

    def fill_left(self, point: Point) -> typing.Tuple[int, bool]:
        water_tiles = 0
        y = point.y

        for x in range(point.x, -1, -1):
            if self.map[y][x] == '#':
                return water_tiles, False

            if self.map[y][x] == '.':
                water_tiles += 1
            self.map[y][x] = '~'

            if y + 1 < self.height and self.map[y + 1][x] != '#':
                w, inf = self.fill_down(Point(x, y + 1))
                water_tiles += w
                if inf:
                    return water_tiles, True

        return water_tiles, True

    def fill_right(self, point: Point) -> typing.Tuple[int, bool]:
        water_tiles = 0
        y = point.y

        for x in range(point.x, self.width):
            if self.map[y][x] == '#':
                return water_tiles, False

            if self.map[y][x] == '.':
                water_tiles += 1
            self.map[y][x] = '~'

            if y + 1 < self.height and self.map[y + 1][x] != '#' and (self.map[y + 1][x - 1] == "#" or x == point.x):
                w, inf = self.fill_down(Point(x, y + 1))
                water_tiles += w
                if inf:
                    return water_tiles, True

        return water_tiles, True

    def __repr__(self) -> str:
        return os.linesep.join(
            ''.join(map(lambda xv: '+' if self.start.x == xv[0] and y == 0 else xv[1], enumerate(line)))
            for y, line in enumerate(self.map)
        )


def extract_data() -> Underground:
    clay: typing.Set[typing.Tuple[int, int]] = set()
    bbox = Bbox()

    with open('input.txt', 'r') as fd:
        for line in fd.read().splitlines(keepends=False):
            c1, c2 = line.split(', ')
            dim1, dim2 = c1[0], c2[0]
            v1 = int(c1[2:])
            v2 = range(*map(lambda x: int(x[1]) if x[0] == 0 else int(x[1]) + 1, enumerate(c2[2:].split('..'))))
            point = {dim1: v1}
            for v in v2:
                point[dim2] = v
                p = point['x'], point['y']
                clay.add(p)
                bbox.extend(p)

    underground: Map = [['.' for _ in range(bbox.width + 2)] for _ in range(bbox.height + 2)]
    for c in clay:
        underground[c[1] + 1 - bbox.lt.y][c[0] + 1 - bbox.lt.x] = '#'

    return Underground(underground, Point(501 - bbox.lt.x, 0))


def calc_water(underground: Underground) -> int:
    # print(underground)
    ret = underground.fill()
    # print(underground)
    return ret


if __name__ == '__main__':
    data = extract_data()
    print(calc_water(data))
