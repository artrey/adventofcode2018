from functools import partial
import typing


Map = typing.List[typing.List[str]]
Point = typing.Tuple[int, int]


def extract_data() -> Map:
    with open('input.txt', 'r') as fd:
        return [[c for c in line] for line in fd.read().splitlines(keepends=False)]


def passable(area: Map, point: Point) -> bool:
    w, h = len(area[0]), len(area)
    x, y = point
    return 0 <= x < w and 0 <= y < h


def neighbors(area: Map, point: Point) -> typing.List[Point]:
    x, y = point
    candidates: typing.List[Point] = [(x, y-1), (x+1, y-1), (x+1, y), (x+1, y+1),
                                      (x, y+1), (x-1, y+1), (x-1, y), (x-1, y-1)]
    area_passable: typing.Callable[[Point], bool] = partial(passable, area)
    return list(filter(area_passable, candidates))


def update_acre(current: str, *neighbors: typing.Tuple[str, ...]) -> str:
    if current == '.':
        if len([n for n in neighbors if n == '|']) > 2:
            return '|'
    elif current == '|':
        if len([n for n in neighbors if n == '#']) > 2:
            return '#'
    elif current == '#':
        if not ('#' in neighbors and '|' in neighbors):
            return '.'
    return current


def step(area: Map) -> Map:
    w, h = len(area[0]), len(area)
    new_area = [['.' for _ in range(w)] for _ in range(h)]
    for y in range(h):
        for x in range(w):
            new_area[y][x] = update_acre(area[y][x], *map(lambda x: area[x[1]][x[0]], neighbors(area, (x, y))))
    return new_area


def print_area(area: Map) -> None:
    w, h = len(area[0]), len(area)
    for y in range(h):
        print(''.join(area[y]))


def area_hash(area: Map) -> int:
    w, h = len(area[0]), len(area)
    values = {'.': 0, '|': w * h, '#': w * h * w * h}
    ret = 0
    for y in range(h):
        for x in range(w):
            ret += values[area[y][x]] + y * w + x
    return ret


def calc_resources(area: Map) -> int:
    trees = sum(v == '|' for line in area for v in line)
    lumberyards = sum(v == '#' for line in area for v in line)
    return trees * lumberyards


def resources(area: Map, steps: int) -> int:
    area_cache: typing.Dict[int, typing.Tuple[int, Map]] = {}
    current_diff = 0
    valid_cycle = 0

    for i in range(steps):
        h = area_hash(area)
        if h in area_cache:
            s, founded_area = area_cache[h]
            diff = i - s
            if diff == current_diff:
                valid_cycle += 1
                if valid_cycle:
                    area_idx = s + (steps - i) % diff
                    area = [a for idx, a in area_cache.values() if idx == area_idx][0]
                    break
            else:
                current_diff = diff
        else:
            valid_cycle = 0
            area_cache[h] = i, area

        area = step(area)

    return calc_resources(area)


if __name__ == '__main__':
    data = extract_data()
    print(resources(data, 10))
    print(resources(data, 1000000000))
