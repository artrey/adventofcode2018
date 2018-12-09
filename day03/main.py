import functools
import re
import typing


class Rect:
    def __init__(self, rect_id: int, left: int, top: int, width: int, height: int) -> None:
        self.id = rect_id
        self.left = left
        self.top = top
        self.width = width
        self.height = height

    @property
    def right(self) -> int:
        return self.left + self.width

    @property
    def bottom(self) -> int:
        return self.top + self.height

    def __str__(self):
        return f'<Rect {self.id}> [{self.left}, {self.top}, {self.width}, {self.height}]'


def extract_data() -> typing.List[Rect]:
    pattern = r'#| @ |,|: |x'

    ret = []
    with open('input.txt', 'r') as fd:
        for line in fd:
            ret.append(Rect(*map(int, re.split(pattern, line.strip())[1:])))
    return ret


def reducer(acc: int, val: typing.Dict[int, int]) -> int:
    return acc + len(list(filter(lambda o: o > 1, val.values())))


def claims_overlap(data: typing.List[Rect]) -> int:
    claims = {}
    for rect in data:
        for x in range(rect.left, rect.right):
            x_claims = claims.get(x, {})
            for y in range(rect.top, rect.bottom):
                x_claims[y] = x_claims.get(y, 0) + 1
            claims[x] = x_claims
    return functools.reduce(reducer, claims.values(), 0)


def non_overlap_claim(data: typing.List[Rect]) -> int:
    rect_status = {}
    claims = {}
    for rect in data:
        for x in range(rect.left, rect.right):
            x_claims = claims.get(x, {})
            for y in range(rect.top, rect.bottom):
                if y not in x_claims:
                    x_claims[y] = rect.id
                else:
                    rect_status[x_claims[y]] = False
                    rect_status[rect.id] = False
            claims[x] = x_claims
        if rect.id not in rect_status:
            rect_status[rect.id] = True

    return list(filter(lambda x: x[1] is True, rect_status.items()))[0][0]


if __name__ == '__main__':
    data = extract_data()
    print(claims_overlap(data))
    print(non_overlap_claim(data))
