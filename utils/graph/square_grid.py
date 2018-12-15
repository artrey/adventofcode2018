import typing


Point = typing.Tuple[int, int]


class SquareGrid:
    def __init__(self, width: int, height: int) -> None:
        super().__init__()
        self.width = width
        self.height = height
        self.obstructions: typing.List[Point] = []

    def in_bounds(self, point: Point) -> bool:
        x, y = point
        return 0 <= x < self.width and 0 <= y < self.height

    def passable(self, point: Point) -> bool:
        return point not in self.obstructions

    def neighbors(self, point: Point) -> typing.List[Point]:
        x, y = point
        ret = [(x, y + 1), (x + 1, y), (x, y - 1), (x - 1, y)]
        return [p for p in ret if self.in_bounds(p) and self.passable(p)]
