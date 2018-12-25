import typing


Point4 = typing.Tuple[int, int, int, int]


def extract_data() -> typing.List[Point4]:
    with open('input.txt', 'r') as fd:
        points: typing.List[Point4] = []
        for line in fd:
            points.append(tuple(map(int, line.strip().split(','))))
        return points


def manhattan_distance(a: Point4, b: Point4) -> int:
    return sum([abs(a[i] - b[i]) for i in range(len(a))])


def find_connected(points, p, dist, queue):
    count = len(points)
    i = 0
    while i < count:
        p2 = points[i]
        if manhattan_distance(p, p2) > dist:
            i += 1
        else:
            queue.append(p2)
            points.remove(p2)
            count -= 1


def constellations_count(points: typing.List[Point4]) -> int:
    constellations = {}
    constellation = 0
    while points:
        p = points.pop()
        constellation += 1
        constellations[p] = constellation
        q = []
        find_connected(points, p, 3, q)

        while q:
            p2 = q.pop()
            constellations[p2] = constellation
            find_connected(points, p2, 3, q)

    return constellation


if __name__ == '__main__':
    data = extract_data()
    print(constellations_count(data))
