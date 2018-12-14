import typing


def extract_data() -> typing.Tuple[str, typing.Dict[str, str]]:
    with open('input.txt', 'r') as fd:
        state = fd.readline().strip()[15:]
        fd.readline()
        patterns = {p: r for p, r in map(lambda x: x.strip().split(' => '), fd)}
        return state, patterns


def new_pot(state: str, patterns: typing.Dict[str, str]) -> str:
    return patterns[state]


def after_n_gen(data: typing.Tuple[str, typing.Dict[str, str]], gen_count: int) -> int:
    state, patterns = data
    offset = 0

    history = {state: (0, 0)}
    cycle_detected = False

    gen = 0
    while gen < gen_count:
        state = f'....{state}....'
        state = ''.join(new_pot(state[i - 2: i + 3], patterns) for i in range(2, len(state) - 2))
        left = state.index('#')
        right = state.rindex('#')
        state = state[left: right + 1]
        offset += 2 - left
        gen += 1

        if not cycle_detected:
            if state in history:
                history_offset, history_gen = history[state]
                gen_diff = gen - history_gen
                offset_diff = offset - history_offset

                total_cycle = gen_count - gen // gen_diff
                gen += total_cycle * gen_diff
                offset += total_cycle * offset_diff
                cycle_detected = True
            else:
                history[state] = (offset, gen)

    return sum(i - offset for i, pot in enumerate(state) if pot == '#')


def after20gen(data: typing.Tuple[str, typing.Dict[str, str]]) -> int:
    return after_n_gen(data, 20)


def after50000000000gen(data: typing.Tuple[str, typing.Dict[str, str]]) -> int:
    return after_n_gen(data, 50000000000)


if __name__ == '__main__':
    data = extract_data()
    print(after20gen(data))
    print(after50000000000gen(data))
