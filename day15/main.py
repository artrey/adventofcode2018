from enum import Enum
import os
import typing
from utils.graph import SquareGrid, Point


class Race(Enum):
    Goblin = 'G'
    Elf = 'E'

    def enemy(self) -> 'Race':
        return Race.Goblin if self == Race.Elf else Race.Elf


class BattleField(SquareGrid):
    def __init__(self, width: int, height: int) -> None:
        super().__init__(width, height)
        self.units: typing.Dict[Point, Race] = {}

    def passable(self, point: Point) -> bool:
        if super().passable(point):
            return point not in self.units
        return False

    def __repr__(self) -> str:
        def symbol(x: int, y: int) -> str:
            if (x, y) in self.obstructions:
                return '#'
            elif (x, y) in self.units:
                return self.units[(x, y)].value
            return '.'

        return os.linesep.join(''.join(symbol(x, y) for x in range(self.width)) for y in range(self.height))


def extract_data() -> BattleField:
    with open('input.txt', 'r') as fd:
        data = fd.read().splitlines(keepends=False)
        ret = BattleField(len(data[0]), len(data))
        for y, line in enumerate(data):
            for x, v in enumerate(line):
                if v == '#':
                    ret.obstructions.append((x, y))
                elif v == 'G':
                    ret.units[(x, y)] = Race.Goblin
                elif v == 'E':
                    ret.units[(x, y)] = Race.Elf
        return ret


def combat_outcome(bf: BattleField) -> int:
    print(bf)
    return 0


if __name__ == '__main__':
    data = extract_data()
    print(combat_outcome(data))
