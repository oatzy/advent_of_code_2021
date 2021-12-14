from collections import Counter
from dataclasses import dataclass
from typing import Dict


@dataclass
class Instructions:
    template: str
    rules: Dict[str, str]


def load_data(path):
    with open(path, 'r') as f:
        template, rules = f.read().split('\n\n')

    return Instructions(
        template,
        dict(l.split(' -> ') for l in rules.splitlines())
    )


def cached(fn):
    cache = {}

    def inner(cur, rules, count):
        # rules isn't hashable
        # but doesn't need including since it doesn't change
        if (cur, count) not in cache:
            cache[(cur, count)] = fn(cur, rules, count)
        return cache[(cur, count)]

    return inner


@cached
def iterate(cur, rules, count):
    # recursive: f(XY) -> f(XM) + f(MY) - M
    if count == 0:
        return Counter(cur)

    mid = rules[cur]
    left = iterate(cur[0]+mid, rules, count-1)
    right = iterate(mid+cur[1], rules, count-1)

    ret = left + right
    # remove overlap
    ret[mid] -= 1

    return ret


def polymerise(template, rules, count):
    total = Counter()

    for i in range(len(template)-1):
        total += iterate(template[i:i+2], rules, count)
        # remove overlap
        total[template[i+1]] -= 1

    # re-add last since it doesn't overlap
    total[template[-1]] += 1

    return total


def perform(data, count):
    c = polymerise(data.template, data.rules, count)
    counts = [i[1] for i in c.most_common()]

    return counts[0] - counts[-1]


def part1(data):
    return perform(data, 10)


def part2(data):
    return perform(data, 40)


def main():
    data = load_data('input.txt')
    print(part1(data))
    print(part2(data))


if __name__ == '__main__':
    main()


class Test:

    def setup_method(self):
        self.data = load_data('test.txt')

    def test_part1(self):
        assert part1(self.data) == 1588

    def test_part2(self):
        assert part2(self.data) == 2188189693529
