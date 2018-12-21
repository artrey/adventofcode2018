import typing


def compiled_alg() -> int:
    r4 = 65536
    r3 = 10649702

    while True:
        r3 += r4 & 255
        r3 &= 16777215
        r3 *= 65899
        r3 &= 16777215

        if r4 < 256:
            return r3

        r4 //= 256


def compiled_alg_max() -> int:
    store: typing.Set[int] = set()
    last_value = 0

    r4 = 65536
    r3 = 10649702

    while True:
        r3 += r4 & 255
        r3 &= 16777215
        r3 *= 65899
        r3 &= 16777215

        if r4 < 256:
            if r3 not in store:
                last_value = r3
            else:
                return last_value
            store.add(r3)
            r4 = r3 | 65536
            r3 = 10649702
            continue

        r4 //= 256


if __name__ == '__main__':
    print(compiled_alg())
    print(compiled_alg_max())
