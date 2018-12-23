import typing
from .point import Point


class Bbox:
    def __init__(self):
        self.lt: typing.Optional[Point] = None
        self.rb: typing.Optional[Point] = None

    def extend(self, point: typing.Union[Point, typing.Tuple[int, int]]) -> None:
        if not isinstance(point, Point):
            point = Point(point[0], point[1])

        if self.lt is None:
            self.lt = Point(point.x, point.y)
        if self.rb is None:
            self.rb = Point(point.x, point.y)

        self.lt.x = min(self.lt.x, point.x)
        self.lt.y = min(self.lt.y, point.y)
        self.rb.x = max(self.rb.x, point.x)
        self.rb.y = max(self.rb.y, point.y)

    def intersect(self, other: 'Bbox') -> 'Bbox':
        high = self
        low = other

        if high.lt.y > other.lt.y:
            high, low = low, high

        ret = Bbox()

        if high.rb.y >= low.lt.y:
            if high.rb.x >= low.lt.x or high.lt.x <= low.rb.x:
                ret.extend((0, 0))
                ret.lt.x = max(high.lt.x, low.lt.x)
                ret.lt.y = max(high.lt.y, low.lt.y)
                ret.rb.x = min(high.rb.x, low.rb.x)
                ret.rb.y = min(high.rb.y, low.rb.y)

        return ret

    @property
    def width(self) -> int:
        return self.rb.x - self.lt.x + 1

    @property
    def height(self) -> int:
        return self.rb.y - self.lt.y + 1

    @property
    def square(self) -> int:
        return self.width * self.height

    def __repr__(self) -> str:
        return f'[{self.lt}, {self.rb}]'
