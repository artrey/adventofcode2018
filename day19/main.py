from abc import ABC, abstractmethod
from copy import deepcopy
import re
import typing

Registers = typing.List[int]


class Command(ABC):
    @abstractmethod
    def execute(self, registers: Registers, a: int, b: int, c: int) -> None:
        pass

    def __repr__(self) -> str:
        return f'<Command {self.__class__.__name__.lower()}>'


class Addr(Command):
    def execute(self, registers: Registers, a: int, b: int, c: int) -> None:
        registers[c] = registers[a] + registers[b]


class Addi(Command):
    def execute(self, registers: Registers, a: int, b: int, c: int) -> None:
        registers[c] = registers[a] + b


class Mulr(Command):
    def execute(self, registers: Registers, a: int, b: int, c: int) -> None:
        registers[c] = registers[a] * registers[b]


class Muli(Command):
    def execute(self, registers: Registers, a: int, b: int, c: int) -> None:
        registers[c] = registers[a] * b


class Banr(Command):
    def execute(self, registers: Registers, a: int, b: int, c: int) -> None:
        registers[c] = registers[a] & registers[b]


class Bani(Command):
    def execute(self, registers: Registers, a: int, b: int, c: int) -> None:
        registers[c] = registers[a] & b


class Borr(Command):
    def execute(self, registers: Registers, a: int, b: int, c: int) -> None:
        registers[c] = registers[a] | registers[b]


class Bori(Command):
    def execute(self, registers: Registers, a: int, b: int, c: int) -> None:
        registers[c] = registers[a] | b


class Setr(Command):
    def execute(self, registers: Registers, a: int, b: int, c: int) -> None:
        registers[c] = registers[a]


class Seti(Command):
    def execute(self, registers: Registers, a: int, b: int, c: int) -> None:
        registers[c] = a


class Gtir(Command):
    def execute(self, registers: Registers, a: int, b: int, c: int) -> None:
        registers[c] = 1 if a > registers[b] else 0


class Gtri(Command):
    def execute(self, registers: Registers, a: int, b: int, c: int) -> None:
        registers[c] = 1 if registers[a] > b else 0


class Gtrr(Command):
    def execute(self, registers: Registers, a: int, b: int, c: int) -> None:
        registers[c] = 1 if registers[a] > registers[b] else 0


class Eqir(Command):
    def execute(self, registers: Registers, a: int, b: int, c: int) -> None:
        registers[c] = 1 if a == registers[b] else 0


class Eqri(Command):
    def execute(self, registers: Registers, a: int, b: int, c: int) -> None:
        registers[c] = 1 if registers[a] == b else 0


class Eqrr(Command):
    def execute(self, registers: Registers, a: int, b: int, c: int) -> None:
        registers[c] = 1 if registers[a] == registers[b] else 0


class Instruction:
    def __init__(self, opcode: str, a: int, b: int, c: int) -> None:
        self.opcode = opcode
        self.a = a
        self.b = b
        self.c = c

    def __repr__(self) -> str:
        return f'{{{self.opcode} {self.a} {self.b} {self.c}}}'


class Cpu:
    def __init__(self, initial_state: Registers, ip_index: int = 0) -> None:
        self.registers = initial_state
        self.ip_index = ip_index
        commands = [Addr(), Addi(), Mulr(), Muli(), Banr(), Bani(), Borr(), Bori(),
                    Setr(), Seti(), Gtir(), Gtri(), Gtrr(), Eqir(), Eqri(), Eqrr()]
        self.commands = {cmd.__class__.__name__.lower(): cmd for cmd in commands}

    def execute(self, instruction: Instruction) -> None:
        self.commands[instruction.opcode].execute(self.registers, instruction.a, instruction.b, instruction.c)

    def execute_program(self, instructions: typing.List[Instruction], max_iters: int = -1) -> None:
        total_instructions = len(instructions)
        ip = self.registers[self.ip_index]
        it = 0
        while 0 <= ip < total_instructions:
            if 0 < max_iters < it:
                break

            self.registers[self.ip_index] = ip
            self.execute(instructions[self.registers[self.ip_index]])
            ip = self.registers[self.ip_index] + 1

            it += 1
            if it % 100000 == 0:
                print(self)

    def __repr__(self) -> str:
        return f'<CPU state: {repr(self.registers)} ip: {self.ip_index}>'


def extract_data() -> typing.Tuple[int, typing.List[Instruction]]:
    with open('input.txt', 'r') as fd:
        ip_index = int(fd.readline().strip().split()[1])
        instructions: typing.List[Instruction] = []
        for line in fd:
            opcode, *params = line.strip().split()
            instructions.append(Instruction(opcode, *map(int, params)))
        return ip_index, instructions


def execute_program(ip_index: int, instructions: typing.List[Instruction]) -> int:
    cpu = Cpu([0] * 6, ip_index)
    cpu.execute_program(instructions)
    return cpu.registers[0]


def execute_program2(ip_index: int, instructions: typing.List[Instruction]) -> int:
    cpu = Cpu([1] + [0] * 5, ip_index)
    cpu.execute_program(instructions, 1000000)
    print(f'CPU after 1000000 iterations: {cpu}')
    return cpu.registers[0]


def compiled_alg(value: int) -> int:
    r0 = 0
    r1 = 1
    while r1 <= value:
        if value % r1 == 0:
            r0 += r1
        r1 += 1
    return r0


if __name__ == '__main__':
    ip_index, instructions = extract_data()
    print(execute_program(ip_index, instructions))
    print(execute_program2(ip_index, instructions))
    print(compiled_alg(10551355))
