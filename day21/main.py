import typing


def compiled_alg() -> int:
    r = [0] * 6
    r[4] = 65536
    r[3] = 10649702

    while True:
        r[5] = r[4] & 255
        r[3] += r[5]
        r[3] &= 16777215
        r[3] *= 65899
        r[3] &= 16777215

        if r[4] < 256:
            return r[3]

        r[4] //= 256


def compiled_alg_max() -> int:
    store: typing.Set[int] = set()
    last_value = 0

    r = [0] * 6
    r[4] = 65536
    r[3] = 10649702

    while True:
        r[5] = r[4] & 255
        r[3] += r[5]
        r[3] &= 16777215
        r[3] *= 65899
        r[3] &= 16777215

        if r[4] < 256:
            if r[3] not in store:
                last_value = r[3]
            else:
                return last_value
            store.add(r[3])
            r[4] = r[3] | 65536
            r[3] = 10649702
            continue

        r[4] //= 256


if __name__ == '__main__':
    print(compiled_alg())
    print(compiled_alg_max())
