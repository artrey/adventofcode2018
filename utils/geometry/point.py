class Point:
    def __init__(self, x: int, y: int) -> None:
        self.x = x
        self.y = y

    def manhattan_length(self, x: int, y: int) -> int:
        return abs(self.x - x) + abs(self.y - y)

    def __repr__(self) -> str:
        return f'({self.x}, {self.y})'
