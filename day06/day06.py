
from typing import Counter


def load_data(path):
    with open(path, 'r') as f:
        return [int(i) for i in f.read().split(',')]


def simulate_old(timers, days):
    # naive implementation
    old, new = timers, []

    for _ in range(days):
        for l in old:
            if l == 0:
                new.extend([6, 8])
            else:
                new.append(l-1)
        old, new = new, []

    return len(old)


def simulate(timers, days):
    # use a counter to group together
    # all the lanternfish that are in sync
    old, new = Counter(timers), Counter()

    for _ in range(days):
        for l, n in old.items():
            if l == 0:
                new[6] += n
                new[8] += n
            else:
                new[l-1] += n
        old, new = new, Counter()

    return sum(old.values())


def part1(timers):
    return simulate(timers, 80)


def part2(timers):
    return simulate(timers, 256)


def main():
    data = load_data('input.txt')
    print(part1(data))
    print(part2(data))


if __name__ == '__main__':
    main()


class Test:

    def setup_method(self):
        self.data = load_data('test.txt')

    def test_simulate(self):
        assert simulate(self.data, 18) == 26

    def test_part1(self):
        assert part1(self.data) == 5934

    def test_part2(self):
        assert part2(self.data) == 26984457539
