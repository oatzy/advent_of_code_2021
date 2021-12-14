from collections import Counter, deque
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


def polymerise(template, rules):
    new = []
    for i in range(len(template)-1):
        new.append(template[i])
        new.append(rules[template[i:i+2]])
    new.append(template[-1])

    return ''.join(new)


def perform(data, steps):
    template = data.template

    for t in range(steps):
        # print(t)
        template = polymerise(template, data.rules)

    counts = [c[1] for c in Counter(template).most_common()]

    return counts[0] - counts[-1]


def polymerise_deque(template, rules):
    d = template
    length = len(template)

    for _ in range(length-1):
        x = rules[f"{d[0]}{d[1]}"]
        d.rotate(-1)
        d.append(x)

    d.rotate(-1)

    return d


def perform_deque(data, steps):
    template = deque(data.template)

    for t in range(steps):
        # print(t)
        template = polymerise_deque(template, data.rules)
        counts = Counter(template).most_common()
        print(counts[0], counts[-1])

    counts = [c[1] for c in Counter(template).most_common()]

    return counts[0] - counts[-1]


@dataclass
class Node:
    value: str
    next: int


def polymerise_linked_list(template, rules):
    cur = template[0]

    while cur.next is not None:
        next = cur.next

        x = rules[f"{cur.value}{template[cur.next].value}"]
        template.append(Node(x, next))
        cur.next = len(template) - 1

        cur = template[next]

    return template


def perform_linked_list(data, steps):
    template = [Node(x, i+1) for i, x in enumerate(data.template)]
    template[-1].next = None

    for t in range(steps):
        print(t)
        template = polymerise_linked_list(template, data.rules)

    counts = [c[1] for c in Counter(n.value for n in template).most_common()]

    return counts[0] - counts[-1]


def part1(data):
    return perform_deque(data, 20)


def part2(data):
    return perform(data, 40)


def main():
    data = load_data('input.txt')
    print(part1(data))
    # print(part2(data))


if __name__ == '__main__':
    main()


class Test:

    def setup_method(self):
        self.data = load_data('test.txt')

    def test_part1(self):
        assert part1(self.data) == 1588

    def test_part2(self):
        assert part2(self.data) == 2188189693529
