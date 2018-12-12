from utils.linked_list import LinkedList


def extract_data() -> LinkedList:
    data = LinkedList()
    with open('input.txt', 'r') as fd:
        for char in fd.read().strip():
            data.append(ord(char))
    return data


def check_opposite(unit1: int, unit2: int) -> bool:
    return abs(unit1 - unit2) == 32


def clean_polymer(data: LinkedList) -> LinkedList:
    cur = data.head
    while cur is not None:
        if cur.next is None:
            break
        if check_opposite(cur.data, cur.next.data):
            data.remove_node(cur.next)
            data.remove_node(cur)
            cur = cur.next if cur.prev is None else cur.prev
        else:
            cur = cur.next
    return data


def units_count(data: LinkedList) -> int:
    return len(clean_polymer(data))


def smallest_units_count(data: LinkedList) -> int:
    units = {}
    for unit in range(ord('A'), ord('Z') + 1):
        opposite_unit = unit + 32
        cur_data = data.copy()
        cur = cur_data.head
        while cur is not None:
            if cur.data in [unit, opposite_unit]:
                cur = cur_data.remove_node(cur).prev or cur_data.head
            cur = cur.next
        units[unit] = units_count(cur_data)
    return min(units.values())


if __name__ == '__main__':
    data = extract_data()
    print(units_count(data.copy()))
    print(smallest_units_count(data))
