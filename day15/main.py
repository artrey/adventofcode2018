import copy
from enum import Enum
import os
import typing
from utils.graph import SquareGrid, Point
from utils.queue import Queue


class Race(Enum):
    Goblin = 'G'
    Elf = 'E'

    def enemy(self) -> 'Race':
        return Race.Goblin if self == Race.Elf else Race.Elf


class Unit:
    def __init__(self, race: Race, hp: int, power: int) -> None:
        self.race = race
        self.hp = hp
        self.power = power

    @property
    def is_alive(self) -> bool:
        return self.hp > 0

    def attack(self, unit: 'Unit') -> None:
        unit.hp -= self.power

    def is_enemy(self, unit: 'Unit') -> bool:
        return self.race != unit.race

    def __repr__(self) -> str:
        return f'{repr(self.race)} [{self.hp} / {self.power}]'


class BattleField(SquareGrid):
    def __init__(self, width: int, height: int) -> None:
        super().__init__(width, height)
        self.units: typing.Dict[Point, Unit] = {}

    def copy(self) -> 'BattleField':
        bf = BattleField(self.width, self.height)
        bf.obstructions = copy.deepcopy(self.obstructions)
        bf.units = copy.deepcopy(self.units)
        return bf

    def passable(self, point: Point) -> bool:
        if super().passable(point):
            return point not in self.units
        return False

    def neighbor_order(self, point: Point) -> typing.List[Point]:
        x, y = point
        return [(x, y - 1), (x - 1, y), (x + 1, y), (x, y + 1)]

    def point_index(self, point: Point) -> int:
        x, y = point
        return self.width * y + x

    def bfs_nearest(self, start: Point, goals: typing.Set[Point]) -> Point:
        if start in goals:
            return start

        frontier = Queue()
        frontier.put((start, 0))

        came_from: typing.Dict[Point, typing.Optional[Point]] = {start: None}
        last_level = None
        nearest_goals: typing.List[Point] = []

        while not frontier.empty():
            current, level = frontier.get()

            if last_level is not None and level > last_level:
                continue

            if current in goals:
                last_level = level
                nearest_goals.append(current)

            for neighbor in self.neighbors(current):
                if neighbor not in came_from:
                    frontier.put((neighbor, level + 1))
                    came_from[neighbor] = current

        if not nearest_goals:
            return start

        bests_steps: typing.List[Point] = []
        for g in nearest_goals:
            while came_from[g] != start:
                g = came_from[g]
            bests_steps.append(g)
        bests_steps.sort(key=self.point_index)

        return bests_steps[0]

    def move(self, unit: Unit, position: Point) -> Point:
        in_range_points: typing.Set[Point] = set()
        for p, u in self.units.items():
            if u.is_enemy(unit):
                for in_range_point in self.neighbors(p):
                    in_range_points.add(in_range_point)

        return self.bfs_nearest(position, in_range_points)

    def attack(self, unit: Unit, position: Point) -> bool:
        pos, enemy = min(
            filter(
                lambda x: unit.is_enemy(x[1]),
                ((p, self.units[p]) for p in self.neighbor_order(position)
                 if super(BattleField, self).passable(p) and p in self.units)
            ),
            key=lambda x: x[1].hp,
            default=(None, None)
        )

        if pos and enemy:
            unit.attack(enemy)
            if not enemy.is_alive:
                self.units.pop(pos)
                return True
        return False

    def turn(self) -> bool:
        total_units = len(self.units)

        for idx, point in enumerate(sorted(self.units, key=self.point_index)):
            if point not in self.units:
                continue

            unit = self.units.pop(point)
            next_point = self.move(unit, point)
            self.units[next_point] = unit

            if self.attack(unit, next_point):
                if self.finish and idx + 1 < total_units:
                    return False

        return True

    @property
    def finish(self) -> bool:
        return len({u.race for u in self.units.values()}) == 1

    @property
    def total_hp(self) -> int:
        return sum(u.hp for u in self.units.values())

    def alive_amount(self, race: Race) -> int:
        return len([u for u in self.units.values() if u.race == race])

    @property
    def alive_elves(self) -> int:
        return self.alive_amount(Race.Elf)

    @property
    def alive_goblins(self) -> int:
        return self.alive_amount(Race.Goblin)

    def __repr__(self) -> str:
        def symbol(x: int, y: int) -> str:
            if (x, y) in self.obstructions:
                return '#'
            elif (x, y) in self.units:
                return self.units[(x, y)].race.value
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
                    ret.units[(x, y)] = Unit(Race.Goblin, 200, 3)
                elif v == 'E':
                    ret.units[(x, y)] = Unit(Race.Elf, 200, 3)
        return ret


def combat_outcome(bf: BattleField) -> int:
    i = 0
    while not bf.finish:
        if bf.turn():
            i += 1
    return i * bf.total_hp


def clear_win_outcome(bf: BattleField) -> int:
    ret = 0
    total_elves = bf.alive_elves

    current_power = 64
    modifier = current_power

    while modifier > 0:
        current_bf = bf.copy()
        for u in current_bf.units.values():
            if u.race == Race.Elf:
                u.power = current_power

        outcome = combat_outcome(current_bf)

        modifier //= 2
        if current_bf.alive_elves == total_elves:
            ret = outcome
            if current_power == 4:
                break
            current_power -= modifier
        else:
            current_power += modifier

    return ret


if __name__ == '__main__':
    data = extract_data()
    print(combat_outcome(data.copy()))
    print(clear_win_outcome(data.copy()))
