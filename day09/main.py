import re
import typing


class Player:
    def __init__(self, index: int) -> None:
        self.index = index
        self.score = 0

    def reset(self) -> None:
        self.score = 0


class Circle:
    def __init__(self) -> None:
        self.circle = [0]
        self.current_index = 0

    def reset(self) -> None:
        self.circle = [0]
        self.current_index = 0

    def calc_index(self, offset: int) -> int:
        idx = self.current_index + offset
        count = len(self.circle)
        while idx >= count:
            idx -= count
        while idx < 0:
            idx += count
        return idx

    def add_marble(self, number: int) -> int:
        if number % 23 == 0:
            idx = self.calc_index(-7)
            value = self.circle.pop(idx)
            self.current_index = idx
            return number + value
        else:
            idx = self.calc_index(2)
            self.circle.insert(idx, number)
            self.current_index = idx
            return 0

    def __str__(self) -> str:
        return str(self.circle)


class Game:
    def __init__(self, players_count: int) -> None:
        self.players = [Player(i) for i in range(players_count)]
        self.circle = Circle()

    def _turn(self, player_idx: int, number: int) -> int:
        score = self.circle.add_marble(number)
        self.players[player_idx].score += score
        return score

    def play(self, max_number: int) -> None:
        self.reset()
        number = 1
        while number <= max_number:
            for p in self.players:
                self._turn(p.index, number)
                number += 1
                if number > max_number:
                    break

    def reset(self) -> None:
        self.circle.reset()
        for p in self.players:
            p.reset()

    def __str__(self) -> str:
        return str(self.circle)


def extract_data() -> typing.Tuple[int, int]:
    with open('input.txt', 'r') as fd:
        m = re.match('(\d+) players; last marble is worth (\d+) points', fd.read())
        return int(m.group(1)), int(m.group(2))


def play(players: int, max_number: int) -> int:
    game = Game(players)
    game.play(max_number)
    return max(game.players, key=lambda x: x.score).score


if __name__ == '__main__':
    players, points = extract_data()
    print(play(players, points))
