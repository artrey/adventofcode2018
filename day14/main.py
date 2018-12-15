import typing
from utils.linked_list import RoundedLinkedList


def extract_data() -> str:
    with open('input.txt', 'r') as fd:
        return fd.read().strip()


def ten_recipes(data: str) -> str:
    offset = int(data)
    final_len = offset + 10
    recipes = RoundedLinkedList()
    elf1 = recipes.append(3)
    elf2 = recipes.append(7)

    while len(recipes) < final_len:
        value = elf1.data + elf2.data
        if value > 9:
            recipes.append(value // 10)
        recipes.append(value % 10)

        for _ in range(1 + elf1.data):
            elf1 = elf1.next
        for _ in range(1 + elf2.data):
            elf2 = elf2.next

    ret = []
    curr = recipes.head.prev
    for _ in range(10):
        ret.append(str(curr.data))
        curr = curr.prev
    return ''.join(reversed(ret))


class Checker:
    def __init__(self, data: str) -> None:
        self.data = data
        self.prefix = self.calc_prefix()
        self.index = 0

    def calc_prefix(self) -> typing.List[int]:
        pattern = self.data
        v = [0] * len(pattern)
        for i in range(1, len(pattern)):
            k = v[i - 1]
            while k > 0 and pattern[k] != pattern[i]:
                k = v[k - 1]
            if pattern[k] == pattern[i]:
                k = k + 1
            v[i] = k
        return v

    def check(self, value: str) -> bool:
        while self.index > 0 and self.data[self.index] != value:
            self.index = self.prefix[self.index - 1]
        if self.data[self.index] == value:
            self.index += 1
        if self.index == len(self.data):
            return True
        return False


def when_scores_occurred(data: str) -> int:
    checker = Checker(data)

    recipes = RoundedLinkedList()
    elf1 = recipes.append(3)
    elf2 = recipes.append(7)

    while True:
        value = elf1.data + elf2.data
        if value > 9:
            if checker.check(str(recipes.append(value // 10).data)):
                return len(recipes) - len(data)
        if checker.check(str(recipes.append(value % 10).data)):
            return len(recipes) - len(data)

        for _ in range(1 + elf1.data):
            elf1 = elf1.next
        for _ in range(1 + elf2.data):
            elf2 = elf2.next


if __name__ == '__main__':
    data = extract_data()
    print(ten_recipes(data))
    print(when_scores_occurred(data))
