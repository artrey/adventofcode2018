from abc import ABC, abstractmethod
from copy import deepcopy
import re
import typing


Registers = typing.List[int]


class Command(ABC):
    @abstractmethod
    def execute(self, registers: Registers, a: int, b: int, c: int) -> None:
        pass


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
    def __init__(self, opcode: int, a: int, b: int, c: int) -> None:
        self.opcode = opcode
        self.a = a
        self.b = b
        self.c = c

    def __repr__(self) -> str:
        return f'{{{self.opcode} {self.a} {self.b} {self.c}}}'


class Cpu:
    def __init__(self, initial_state: Registers) -> None:
        self.registers = initial_state
        self.commands: typing.Dict[int, Command] = {}

    def execute(self, instruction: Instruction) -> None:
        self.commands[instruction.opcode].execute(self.registers, instruction.a, instruction.b, instruction.c)


class Sample:
    def __init__(self, before: Registers, instruction: Instruction, after: Registers) -> None:
        self.before = before
        self.instruction = instruction
        self.after = after

    def __repr__(self) -> str:
        return f'{repr(self.before)} -> {repr(self.instruction)} -> {repr(self.after)}'


def extract_data() -> typing.Tuple[typing.List[Sample], typing.List[Instruction]]:
    with open('input.txt', 'r') as fd:
        samples_raw,  instructions_raw = fd.read().split('\n\n\n')

        samples = []
        for m in re.finditer(
                r'Before:\s+\[([\d\s,]+)\]\n([\d\s]+)\nAfter:\s+\[([\d\s,]+)\]',
                samples_raw
        ):
            samples.append(Sample(
                list(map(int, m.group(1).split(','))),
                Instruction(*map(int, m.group(2).split())),
                list(map(int, m.group(3).split(','))),
            ))

        instructions = []
        for line in instructions_raw.strip().split('\n'):
            instructions.append(Instruction(*map(int, line.split())))

        return samples, instructions


def complex_sample_amount(samples: typing.List[Sample]) -> int:
    commands = [Addr(), Addi(), Mulr(), Muli(), Banr(), Bani(), Borr(), Bori(),
                Setr(), Seti(), Gtir(), Gtri(), Gtrr(), Eqir(), Eqri(), Eqrr()]

    complex_sample = 0
    for sample in samples:
        behave = 0
        for cmd in commands:
            registers = deepcopy(sample.before)
            cmd.execute(registers, sample.instruction.a, sample.instruction.b, sample.instruction.c)
            if registers == sample.after:
                behave += 1
            if behave > 2:
                complex_sample += 1
                break

    return complex_sample


def determine_commands(samples: typing.List[Sample]) -> typing.Dict[int, Command]:
    ret = {}

    commands = [Addr(), Addi(), Mulr(), Muli(), Banr(), Bani(), Borr(), Bori(),
                Setr(), Seti(), Gtir(), Gtri(), Gtrr(), Eqir(), Eqri(), Eqrr()]
    commands_count = len(commands)

    while len(ret) < commands_count:
        for sample in samples:
            behave = 0
            command = None
            for cmd in commands:
                registers = deepcopy(sample.before)
                cmd.execute(registers, sample.instruction.a, sample.instruction.b, sample.instruction.c)
                if registers == sample.after:
                    behave += 1
                    command = cmd
            if behave == 1:
                ret[sample.instruction.opcode] = command
                commands.remove(command)

    return ret


def execute_instructions(samples: typing.List[Sample], instructions: typing.List[Instruction]) -> int:
    cpu = Cpu([0, 0, 0, 0])
    cpu.commands = determine_commands(samples)
    for instruction in instructions:
        cpu.execute(instruction)
    return cpu.registers[0]


if __name__ == '__main__':
    samples, instructions = extract_data()
    print(complex_sample_amount(samples))
    print(execute_instructions(samples, instructions))
