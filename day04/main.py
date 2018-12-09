from datetime import datetime, timedelta
import functools
import re
import typing


class SleepTime:
    def __init__(self, start: int) -> None:
        self.start = start
        self.end = 0

    @property
    def duration(self):
        return self.end - self.start

    def __str__(self):
        return f'<SleepTime> [{self.start} - {self.end}]'


class Guard:
    def __init__(self, guard_id: int) -> None:
        self.id = guard_id
        self.asleep_schedule: typing.Dict[datetime, typing.List[SleepTime]] = {}

    @property
    def total_asleep_time(self):
        return functools.reduce(lambda acc, val: acc + sum(map(lambda x: x.duration, val)),
                                self.asleep_schedule.values(), 0)

    def __str__(self):
        return f'<Guard {self.id}> [{self.asleep_schedule}]'


def closest_day(dt: datetime) -> datetime:
    current_day = datetime(dt.year, dt.month, dt.day)
    next_day = current_day + timedelta(days=1)
    if dt - current_day < next_day - dt:
        return current_day
    return next_day


def extract_asleep_schedule(
        schedule: typing.List[typing.Tuple[datetime, str]],
        start_idx: int) -> typing.Tuple[int, typing.List[SleepTime]]:
    idx = start_idx
    current_sleep_time = None
    ret = []
    while idx < len(schedule):
        dt, record = schedule[idx]
        if record.startswith('Guard'):
            break
        elif record == 'falls asleep':
            current_sleep_time = SleepTime(dt.minute)
        else:
            current_sleep_time.end = dt.minute
            ret.append(current_sleep_time)
        idx += 1
    return idx - 1, ret


def extract_data() -> typing.List[Guard]:
    pattern_dt = '^\[([^\]]+)\] ([\w\s#]+)'
    pattern_guard = r'[\w\s]+#([\d]+)[\w\s]+'
    date_format = '%Y-%m-%d %H:%M'

    schedule = []
    with open('input.txt', 'r') as fd:
        for line in fd:
            m = re.match(pattern_dt, line.strip())
            dt = datetime.strptime(m.group(1), date_format)
            schedule.append((dt, m.group(2)))
    schedule.sort(key=lambda x: x[0])

    guards = {}
    count = len(schedule)
    record_idx = 0
    while record_idx < count:
        dt, record = schedule[record_idx]
        m = re.match(pattern_guard, record)
        if m:
            guard_id = int(m.group(1))
            guard = guards.setdefault(guard_id, Guard(guard_id))
            record_idx, guard.asleep_schedule[closest_day(dt)] = extract_asleep_schedule(schedule, record_idx + 1)
        record_idx += 1

    return list(guards.values())


def max_asleep_guard(guards: typing.List[Guard]) -> Guard:
    return max(guards, key=lambda x: x.total_asleep_time)


def frequent_min(guard: Guard) -> int:
    sleep_times = {}
    for sleeps in guard.asleep_schedule.values():
        for sleep_time in sleeps:
            for minute in range(sleep_time.start, sleep_time.end):
                sleep_times[minute] = sleep_times.get(minute, 0) + 1
    return max(sleep_times.items(), key=lambda x: x[1])[0]


def checksum(guards: typing.List[Guard]) -> int:
    guard = max_asleep_guard(guards)
    return guard.id * frequent_min(guard)


if __name__ == '__main__':
    data = extract_data()
    print(checksum(data))
