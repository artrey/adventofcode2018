import typing


class Stack(list):
    def put(self, item: typing.Any) -> None:
        self.append(item)

    def get(self) -> typing.Any:
        return self.pop()

    def empty(self) -> bool:
        return not self
