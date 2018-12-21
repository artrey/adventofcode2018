from collections import defaultdict
import typing


def extract_data() -> typing.Dict[typing.Tuple[int, int], int]:
    with open('input.txt') as fd:
        regex = fd.readline().rstrip()

    letter_to_move = {
        'N': (0, -1),
        'E': (1, 0),
        'S': (0, 1),
        'W': (-1, 0)
    }

    positions = []
    x, y = 5000, 5000
    came_from = defaultdict(set)
    prev_x, prev_y = x, y
    distances = defaultdict(int)
    for c in regex[1:-1]:
        if c == "(":
            positions.append((x, y))
        elif c == ")":
            x, y = positions.pop()
        elif c == "|":
            x, y = positions[-1]
        else:
            dx, dy = letter_to_move[c]
            x += dx
            y += dy
            came_from[(x, y)].add((prev_x, prev_y))
            if distances[(x, y)] != 0:
                distances[(x, y)] = min(distances[(x, y)], distances[(prev_x, prev_y)] + 1)
            else:
                distances[(x, y)] = distances[(prev_x, prev_y)] + 1

        prev_x, prev_y = x, y

    return distances


def furthest_room(distances: typing.Dict[typing.Tuple[int, int], int]) -> int:
    return max(distances.values())


def furthest_room_more_than_10000(distances: typing.Dict[typing.Tuple[int, int], int]) -> int:
    return len(list(filter(lambda x: distances[x] >= 1000, distances)))


if __name__ == '__main__':
    data = extract_data()
    print(furthest_room(data))
    print(furthest_room_more_than_10000(data))
