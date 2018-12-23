import math
import typing


Point3 = typing.Tuple[int, int, int]


def manhattan_distance(a: Point3, b: Point3) -> int:
    return abs(a[0] - b[0]) + abs(a[1] - b[1]) + abs(a[2] - b[2])


class Nanobot:
    def __init__(self, position: Point3, radius: int) -> None:
        self.pos = position
        self.radius = radius

    def intersect_with(self, other: 'Nanobot') -> bool:
        return manhattan_distance(self.pos, other.pos) <= self.radius + other.radius

    def __repr__(self) -> str:
        return f'<{repr(self.pos)}: {self.radius}>'


def extract_data() -> typing.List[Nanobot]:
    with open('input.txt', 'r') as fd:
        ret = []
        for line in fd:
            pos_str, r_str, *_ = line.strip().split(', ')
            pos: Point3 = tuple(map(int, pos_str[5:-1].split(',')))
            ret.append(Nanobot(pos, int(r_str[2:])))
        return ret


def in_max_range(nanobots: typing.List[Nanobot]) -> int:
    ret = 0
    max_range_nanobot = max(nanobots, key=lambda x: x.radius)
    for n in nanobots:
        if manhattan_distance(n.pos, max_range_nanobot.pos) <= max_range_nanobot.radius:
            ret += 1
    return ret


def max_in_range_point(nanobots: typing.List[Nanobot]) -> int:
    xs = [n.pos[0] for n in nanobots]
    ys = [n.pos[1] for n in nanobots]
    zs = [n.pos[2] for n in nanobots]

    diff = max(xs) - min(xs)
    step = int(math.pow(2, math.floor(math.log(diff, 2)) + 1))

    while True:
        points_count = 0
        closest_point: Point3 = (0, 0, 0)
        min_distance: int = 1e20

        for x in range(min(xs), max(xs) + 1, step):
            for y in range(min(ys), max(ys) + 1, step):
                for z in range(min(zs), max(zs) + 1, step):
                    count = 0
                    for bot in nanobots:
                        if (manhattan_distance((x, y, z), bot.pos) - bot.radius) // step <= 0:
                            count += 1

                    dist = manhattan_distance((x, y, z), (0, 0, 0))
                    if count > points_count:
                        points_count = count
                        closest_point = (x, y, z)
                        min_distance = dist
                    elif count == points_count and dist < min_distance:
                        closest_point = (x, y, z)
                        min_distance = dist

        if step == 1:
            return min_distance
        else:
            xs = [closest_point[0] - step, closest_point[0] + step]
            ys = [closest_point[1] - step, closest_point[1] + step]
            zs = [closest_point[2] - step, closest_point[2] + step]
            step //= 2


if __name__ == '__main__':
    data = extract_data()
    print(in_max_range(data))
    print(max_in_range_point(data))
