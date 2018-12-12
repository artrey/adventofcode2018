import re
import time
import typing
from utils.geometry import Point, Bbox


class Velocity(Point):
    pass


class Star:
    def __init__(self, position: Point, velocity: Velocity) -> None:
        self.position = position
        self.velocity = velocity

    def do_step(self, times: int=1) -> 'Star':
        self.position.x += self.velocity.x * times
        self.position.y += self.velocity.y * times
        return self

    def __repr__(self) -> str:
        return f'<{self.position};{self.velocity}>'


def extract_data() -> typing.List[Star]:
    with open('input.txt', 'r') as fd:
        ret = []
        for line in fd:
            m = re.match('position=<([\s\d-]+),([\s\d-]+)> velocity=<([\s\d-]+),([\s\d-]+)>', line.strip())
            ret.append(Star(Point(int(m.group(1).strip()), int(m.group(2).strip())),
                            Velocity(int(m.group(3).strip()), int(m.group(4).strip()))))
        return ret


def print_sky(bbox: Bbox, sky_map: typing.Dict[int, typing.Dict[int, bool]]) -> None:
    sky = [['.' for _ in range(bbox.lt.x, bbox.rb.x + 1)] for _ in range(bbox.lt.y, bbox.rb.y + 1)]
    for line in sky:
        print(''.join(line))


def watch_message(data: typing.List[Star]) -> None:
    try:
        while True:
            bbox = Bbox()
            for star in data:
                bbox.extend(star.position)
            print_sky(bbox, {})
            if input('type "exit" to exit') == 'exit':
                break
    except KeyboardInterrupt:
        pass


if __name__ == '__main__':
    data = extract_data()
    watch_message(data)
