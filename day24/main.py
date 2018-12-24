from copy import deepcopy
import math
import re
import typing


class Unit:
    def __init__(self, hit_points: int, damage_amount: int, damage_type: str, initiative: int,
                 immunes: typing.List[str], weaks: typing.List[str]) -> None:
        self.hp = hit_points
        self.damage = damage_amount
        self.damage_type = damage_type
        self.initiative = initiative
        self.immunes = immunes
        self.weaks = weaks
        self.army: typing.Optional['Army'] = None

    def __repr__(self) -> str:
        return f'<Unit hp={self.hp}, damage={self.damage} {self.damage_type}, initiative={self.initiative},' \
            f' immunes={repr(self.immunes)}, weaks={repr(self.weaks)}>'


class Army:
    def __init__(self, title: str) -> None:
        self.title = title
        self.units: typing.Dict[Unit, int] = {}

    def effective_power(self, unit: Unit) -> int:
        return unit.damage * self.units[unit]

    def __repr__(self) -> str:
        return f'<Army {repr(self.title)}: {repr(self.units)}>'


def parse_units(lines: typing.List[str]) -> typing.Dict[Unit, int]:
    regex = re.compile(r'(\d+) units each with (\d+) hit points ([;,()\w\s]*)'
                       r'with an attack that does (\d+) (\w+) damage at initiative (\d+)')

    ret = {}
    for line in lines:
        m = regex.match(line)
        modifiers = m.group(3)
        immunes = []
        weaks = []
        if modifiers:
            for mod in modifiers.strip('() ').split('; '):
                mod_type, mod_values, *_ = mod.split(' to ')
                if mod_type == 'immune':
                    immunes = [*mod_values.split(', ')]
                elif mod_type == 'weak':
                    weaks = [*mod_values.split(', ')]
        u = Unit(int(m.group(2)), int(m.group(4)), m.group(5), int(m.group(6)), immunes, weaks)
        ret[u] = int(m.group(1))

    return ret


def extract_data() -> typing.Tuple[Army, Army]:
    with open('input.txt', 'r') as fd:
        lines = [x.strip() for x in fd]

    divider = lines.index('')

    army_description = lines[:divider]
    army1 = Army(army_description[0][:-1])
    army1.units.update(parse_units(army_description[1:]))
    for u in army1.units:
        u.army = army1

    army_description = lines[divider+1:]
    army2 = Army(army_description[0][:-1])
    army2.units.update(parse_units(army_description[1:]))
    for u in army2.units:
        u.army = army2

    return army1, army2


class Battle:
    def __init__(self, army1: Army, army2: Army) -> None:
        self.a1 = army1
        self.a2 = army2

    def actual_damage(self, u: Unit, e: Unit, base_dmg: int) -> int:
        if u.damage_type in e.weaks:
            return base_dmg * 2
        if u.damage_type in e.immunes:
            return 0
        return base_dmg

    def enemy_targeting(self, u: Unit, enemies: Army) -> typing.Dict[Unit, Unit]:
        power = u.army.effective_power(u)
        best_target = max(enemies.units, key=lambda e: ((self.actual_damage(u, e, power)),
                                                        enemies.effective_power(e), e.initiative))
        if self.actual_damage(u, best_target, power) == 0:
            return {}
        return {u: best_target}

    def targeting(self) -> typing.Dict[Unit, Unit]:
        ret = {}

        for u in self.a1.units:
            ret.update(self.enemy_targeting(u, self.a2))

        for u in self.a2.units:
            ret.update(self.enemy_targeting(u, self.a1))

        return ret

    def attacking(self, targets: typing.Dict[Unit, Unit]) -> None:
        for u, e in sorted(targets.items(), key=lambda x: x[0].initiative, reverse=True):
            if not u.army or not e.army:
                continue

            killed = self.actual_damage(u, e, u.army.effective_power(u)) // e.hp
            if killed == 0:
                continue

            e.army.units[e] -= killed
            if e.army.units[e] <= 0:
                e.army.units.pop(e)
                e.army = None

    def battle(self) -> None:
        self.attacking(self.targeting())

    @property
    def is_finish(self) -> bool:
        return not self.a1.units or not self.a2.units

    @property
    def winner(self) -> Army:
        return self.a1 if self.a1.units else self.a2


def units_lost(armies: typing.Tuple[Army, Army]) -> int:
    b = Battle(*armies)
    while not b.is_finish:
        b.battle()
    return sum(b.winner.units.values())


def get_winner(battle: Battle) -> Army:
    while not battle.is_finish:
        battle.battle()
    return battle.winner


def win_with_boost(armies: typing.Tuple[Army, Army]) -> int:
    b = Battle(*armies)

    boost_min = 0
    boost_max = 1
    while get_winner(deepcopy(b)).title != 'Immune System':
        boost_max *= 2

    while boost_min != boost_max:
        extra_pow = (boost_min + boost_max) // 2
        battle = deepcopy(b)
        for u in battle.a1.units:
            u.damage += extra_pow
        if get_winner(battle).title != 'Immune System':
            boost_min = math.ceil((boost_min + boost_max) / 2)
        else:
            boost_max = extra_pow

    return sum(battle.winner.units.values())


if __name__ == '__main__':
    data = extract_data()
    print(units_lost(deepcopy(data)))
    print(win_with_boost(deepcopy(data)))
