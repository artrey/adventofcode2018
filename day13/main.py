from enum import Enum
import os
import typing
from utils.geometry import Point
from utils.linked_list import RoundedLinkedList


class Direction(Enum):
    up = '^'
    right = '>'
    down = 'v'
    left = '<'

    def rotate_right(self) -> 'Direction':
        return {
            self.up: self.right,
            self.right: self.down,
            self.down: self.left,
            self.left: self.up
        }[self]

    def rotate_left(self) -> 'Direction':
        return {
            self.up: self.left,
            self.left: self.down,
            self.down: self.right,
            self.right: self.up
        }[self]

    @property
    def trail(self) -> str:
        return {
            self.up: '|',
            self.right: '-',
            self.down: '|',
            self.left: '-'
        }[self]


class Cart:
    def __init__(self, point: Point, direction: Direction) -> None:
        self.point = point
        self.direction = direction
        self.directions_rules = RoundedLinkedList()
        self.directions_rules.append(0)
        self.directions_rules.append(1)
        self.directions_rules.append(2)

    def __repr__(self) -> str:
        return f'<Cart: {repr(self.point)} {repr(self.direction.value)}>'

    def move(self) -> None:
        if self.direction == Direction.left:
            self.point.x -= 1
        elif self.direction == Direction.right:
            self.point.x += 1
        elif self.direction == Direction.up:
            self.point.y -= 1
        elif self.direction == Direction.down:
            self.point.y += 1

    def change_direction(self) -> None:
        if self.directions_rules.head.data == 0:
            self.direction = self.direction.rotate_left()
        elif self.directions_rules.head.data == 2:
            self.direction = self.direction.rotate_right()
        self.directions_rules.head = self.directions_rules.head.next


class Map:
    def __init__(self, data: typing.List[typing.List[str]]) -> None:
        self.map = data
        self.carts: typing.List[Cart] = []
        directions = [v.value for v in Direction]
        for y, line in enumerate(data):
            for x, v in enumerate(line):
                if v in directions:
                    cart = Cart(Point(x, y), Direction(v))
                    self.map[y][x] = cart.direction.trail
                    self.carts.append(cart)

    def copy(self) -> 'Map':
        m = Map([])
        m.map = self.map.copy()
        for cart in self.carts:
            m.carts.append(Cart(Point(cart.point.x, cart.point.y), Direction(cart.direction)))
        return m

    def point_index(self, cart: Cart) -> int:
        return cart.point.y * len(self.map[0]) + cart.point.x

    def update_cart_direction(self, cart: Cart) -> None:
        x, y = cart.point.x, cart.point.y
        if self.map[y][x] == '+':
            cart.change_direction()
        elif self.map[y][x] == '\\':
            cart.direction = {
                Direction.up: Direction.left,
                Direction.right: Direction.down,
                Direction.down: Direction.right,
                Direction.left: Direction.up
            }[cart.direction]
        elif self.map[y][x] == '/':
            cart.direction = {
                Direction.up: Direction.right,
                Direction.right: Direction.up,
                Direction.down: Direction.left,
                Direction.left: Direction.down
            }[cart.direction]

    def move(self) -> typing.Optional[Point]:
        for cart in sorted(self.carts, key=self.point_index):
            cart.move()
            self.update_cart_direction(cart)

            for c in self.carts:
                if c != cart and self.point_index(c) == self.point_index(cart):
                    return cart.point
        return None

    def move_with_repair(self) -> typing.Optional[Point]:
        for cart in sorted(self.carts, key=self.point_index):
            if cart not in self.carts:
                continue

            cart.move()
            self.update_cart_direction(cart)

            for ci in range(len(self.carts)):
                c = self.carts[ci]
                if c != cart and self.point_index(c) == self.point_index(cart):
                    self.carts.pop(ci)
                    self.carts.remove(cart)
                    break
        return self.carts[0].point if len(self.carts) == 1 else None

    def __repr__(self) -> str:
        return os.linesep.join([''.join(line) for line in self.map])


def extract_data() -> Map:
    with open('input.txt', 'r') as fd:
        return Map([[c for c in line.rstrip(os.linesep)] for line in fd])


def first_crash_position(data: Map) -> Point:
    while True:
        point = data.move()
        if point:
            break
    return point


def last_cart_position(data: Map) -> Point:
    while True:
        point = data.move_with_repair()
        if point:
            break
    return point


if __name__ == '__main__':
    data = extract_data()
    print(first_crash_position(data.copy()))
    print(last_cart_position(data.copy()))
