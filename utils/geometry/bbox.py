import typing
from .point import Point


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
