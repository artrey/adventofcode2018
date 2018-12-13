from sys import maxsize
import typing
from utils.geometry import Point


def extract_data() -> int:
    with open('input.txt', 'r') as fd:
        return int(fd.read().strip())


def calc_power_level(x: int, y: int, serial_number: int) -> int:
    rack_id = x + 10
    return (rack_id * y + serial_number) * rack_id // 100 % 10 - 5


def calc_board(serial_number: int, size: typing.Tuple[int, int]) -> typing.List[typing.List[int]]:
    w, h = size
    return [[calc_power_level(x, y, serial_number) for x in range(w)] for y in range(h)]


def max_square(board: typing.List[typing.List[int]], size: typing.Tuple[int, int]) -> typing.Tuple[Point, int]:
    w, h = len(board[0]), len(board)
    kw, kh = size

    strip_sum = [[0 for x in range(w - kw + 1)] for y in range(h)]

    for y in range(h):
        curr_sum = 0
        for x in range(kw):
            curr_sum += board[y][x]
        strip_sum[y][0] = curr_sum

        for x in range(1, w - kw + 1):
            curr_sum += (board[y][x + kw - 1] - board[y][x - 1])
            strip_sum[y][x] = curr_sum

    max_sum = -maxsize - 1
    position = Point(-1, -1)

    for x in range(w - kw + 1):
        curr_sum = 0
        for y in range(kh):
            curr_sum += strip_sum[y][x]

        if curr_sum > max_sum:
            max_sum = curr_sum
            position.x, position.y = x, 0

        for y in range(1, h - kh + 1):
            curr_sum += (strip_sum[y + kh - 1][x] - strip_sum[y - 1][x])

            if curr_sum > max_sum:
                max_sum = curr_sum
                position.x, position.y = x, y

    return position, max_sum


def point_max_power3(serial_number: int) -> Point:
    board = calc_board(serial_number, (300, 300))
    return max_square(board, (3, 3))[0]


def point_max_power(serial_number: int) -> typing.Tuple[Point, int]:
    board = calc_board(serial_number, (300, 300))
    ret = max([(*max_square(board, (size, size)), size) for size in range(1, 301)], key=lambda x: x[1])
    return ret[0], ret[2]


if __name__ == '__main__':
    data = extract_data()
    print(point_max_power3(data))
    print(point_max_power(data))
