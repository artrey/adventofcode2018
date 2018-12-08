import typing


def extract_data() -> typing.List[str]:
    with open('input.txt', 'r') as fd:
        return [line.strip() for line in fd]


def str_to_letters(string: str) -> typing.Dict[str, int]:
    return {}


def checksum(data: typing.List[str]) -> int:
    return 0


if __name__ == '__main__':
    data = extract_data()
    print(checksum(data))
