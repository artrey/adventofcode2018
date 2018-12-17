import copy
import os
import typing
from utils.graph import SquareGrid, Point
from utils.queue import Queue
from utils.stack import Stack
from utils.geometry import Bbox


class Underground(SquareGrid):
    def __init__(self, bbox: Bbox) -> None:
        super().__init__(bbox.width, bbox.height)
        self.bbox = bbox
        self.water: typing.Set[Point] = set()
        self.water_shift: typing.Set[Point] = set()

    def copy(self) -> 'Underground':
        bf = Underground(self.bbox)
        bf.obstructions = copy.deepcopy(self.obstructions)
        bf.water = copy.deepcopy(self.water)
        bf.water_shift = copy.deepcopy(self.water_shift)
        return bf

    def in_bounds(self, point: Point) -> bool:
        x, y = point
        return self.bbox.lt.x <= x <= self.bbox.rb.x and self.bbox.lt.y <= y <= self.bbox.rb.y

    def neighbor_order(self, point: Point) -> typing.List[Point]:
        x, y = point
        return [(x - 1, y), (x + 1, y)]

    def has_bottom(self, point: Point) -> bool:
        x, y = point
        bottom_point = x, y + 1
        return bottom_point not in self.water_shift and \
               (bottom_point in self.obstructions or bottom_point in self.water)

    def fill_down(self, point: Point) -> bool:
        sx, sy = point
        top = sy
        center = sx

        while sy < self.bbox.rb.y and not self.has_bottom((sx, sy)):
            self.water.add((sx, sy))
            self.water_shift.add((sx, sy))
            sy += 1

        if sy >= self.bbox.rb.y:
            return False

        finite_left, finite_right = True, True
        self.water.add((sx, sy))
        self.water_shift.add((sx, sy))
        sy += 1

        while sy > top:
            sy -= 1

            print(self)
            print()

            while finite_left and sx > self.bbox.lt.x:
                sx -= 1
                p = (sx, sy)
                if p in self.obstructions:
                    break

                if self.has_bottom(p):
                    self.water.add(p)
                elif self.fill_down(p):
                    finite_left = True
                    for ix in range(sx, center):
                        self.water_shift.add((ix, sy))
                else:
                    finite_left = False

            sx = center
            while finite_right and sx < self.bbox.rb.x:
                sx += 1
                p = (sx, sy)
                if p in self.obstructions:
                    break

                if self.has_bottom(p):
                    self.water.add(p)
                elif self.fill_down(p):
                    finite_right = True
                    for ix in range(center + 1, sx + 1):
                        self.water_shift.add((ix, sy))
                else:
                    finite_right = False

        return finite_left & finite_right

    def flood_fill_row(self, start: Point) -> typing.List[Point]:
        ret = []

        frontier = Queue()
        frontier.put(start)

        visited: typing.Set[Point] = {start}

        while not frontier.empty():
            current = frontier.get()
            self.water.add(current)

            for neighbor in self.neighbors(current):
                if neighbor not in visited:
                    visited.add(neighbor)

                    if self.has_bottom(neighbor):
                        frontier.put(neighbor)
                    else:
                        ret.append(neighbor)

        return ret

    def __repr__(self) -> str:
        def symbol(x: int, y: int) -> str:
            if (x, y) in self.obstructions:
                return '#'
            elif (x, y) in self.water:
                return '~'
            return '.'

        return os.linesep.join(
            ''.join(symbol(x, y) for x in range(self.bbox.lt.x, self.bbox.rb.x + 1))
            for y in range(self.bbox.lt.y, self.bbox.rb.y + 1)
        )


def extract_data() -> Underground:
    clay: typing.Set[Point] = set()
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

    bbox.extend((bbox.lt.x - 1, bbox.lt.y - 1))
    bbox.extend((bbox.rb.x + 1, bbox.rb.y + 1))
    u = Underground(bbox)
    u.obstructions = list(clay)
    return u


def calc_water(underground: Underground) -> int:

    underground.fill_down((500, underground.bbox.lt.y))

    # stack = Stack()
    #
    # stack.put((500, underground.bbox.lt.y))
    #
    # while not stack.empty():
    #     sx, sy = stack.get()
    #     if sy == underground.bbox.rb.y:
    #         continue
    #     top = sy
    #
    #     while sy < underground.bbox.rb.y and not underground.has_bottom((sx, sy)):
    #         sy += 1
    #
    #     fast_up = False
    #     while sy >= top:
    #         if fast_up:
    #             underground.water.add((sx, sy))
    #         else:
    #             for edge in underground.flood_fill_row((sx, sy)):
    #                 stack.put(edge)
    #                 fast_up = True
    #         sy -= 1
    #
    #     print(underground)

    for point in list(filter(lambda p: p[1] == underground.bbox.lt.y or p[1] == underground.bbox.rb.y, underground.water)):
        underground.water.remove(point)

    print(underground)

    return len(underground.water)


if __name__ == '__main__':
    data = extract_data()
    print(calc_water(data))
