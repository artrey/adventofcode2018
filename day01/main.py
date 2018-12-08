import typing


def extract_data() -> typing.List[int]:
    with open('input.txt', 'r') as fd:
        return [int(line.strip()) for line in fd]


def result(data: typing.List[int]) -> int:
    return sum(data)


def twice_reach(data: typing.List[int]) -> int:
    already_seen = {0}
    current_state = 0
    while True:
        for value in data:
            current_state += value
            if current_state in already_seen:
                return current_state
            already_seen.add(current_state)
        len(already_seen)


if __name__ == '__main__':
    data = extract_data()
    print(result(data))
    print(twice_reach(data))
