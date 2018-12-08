import typing


def extract_data() -> typing.List[str]:
    with open('input.txt', 'r') as fd:
        return [line.strip() for line in fd]


def str_to_letters(string: str) -> typing.Dict[str, int]:
    ret = {}
    for letter in string:
        ret[letter] = ret.get(letter, 0) + 1
    return ret


def has_amount(data: typing.Dict[str, int], count: int) -> bool:
    for v in data.values():
        if v == count:
            return True
    return False


def checksum(data: typing.List[str]) -> int:
    double = 0
    triple = 0
    for line in data:
        letters = str_to_letters(line)
        double += 1 if has_amount(letters, 2) else 0
        triple += 1 if has_amount(letters, 3) else 0
    return double * triple


def diff(a: str, b: str) -> int:
    d = 0
    count = len(a)
    for i in range(count):
        d += 1 if a[i] != b[i] else 0
    return d


def same(a: str, b: str) -> str:
    ret = ''
    count = len(a)
    for i in range(count):
        ret += a[i] if a[i] == b[i] else ''
    return ret


def common(data: typing.List[str]) -> str:
    count = len(data)
    for i in range(count - 1):
        for j in range(i + 1, count):
            d = diff(data[i], data[j])
            if d == 1:
                return same(data[i], data[j])
    return ''


if __name__ == '__main__':
    data = extract_data()
    print(checksum(data))
    print(common(data))
