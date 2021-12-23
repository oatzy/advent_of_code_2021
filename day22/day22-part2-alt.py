from dataclasses import dataclass
from queue import Queue
from typing import Tuple

Range = Tuple[int, int]


@dataclass
class Instruction:
    mode: bool
    x: Range
    y: Range
    z: Range

    def __hash__(self):
        return hash((self.x, self.y, self.z))

    def __eq__(self, other):
        return hash(self) == hash(other)

    def size(self):
        return (
            (self.x[1] - self.x[0] + 1) *
            (self.y[1] - self.y[0] + 1) *
            (self.z[1] - self.z[0] + 1)
        )


def load_data(path):
    instructions = []
    with open(path, 'r') as f:
        for line in f:

            mode, ranges = line.split()
            x, y, z = parse_ranges(ranges)
            instructions.append(Instruction(
                mode == 'on', x, y, z
            ))

    return instructions


def parse_ranges(ranges):
    return [
        tuple(map(int, x.split('=')[1].split('..')))  # sorry
        for x in ranges.split(',')
    ]


def splitx(i, x):
    return (
        Instruction(i.mode, (i.x[0], x-1), i.y, i.z),
        Instruction(i.mode, (x, i.x[1]), i.y, i.z)
    )


def splity(i, y):
    return (
        Instruction(i.mode, i.x, (i.y[0], y-1), i.z),
        Instruction(i.mode, i.x, (y, i.y[1]), i.z)
    )


def splitz(i, z):
    return (
        Instruction(i.mode, i.x, i.y, (i.z[0], z-1)),
        Instruction(i.mode, i.x, i.y, (z, i.z[1]))
    )


def split_overlap(a, b):
    #print('\n', b)
    atoms = []

    to_check = Queue()
    to_check.put(a)

    while not to_check.empty():
        a = to_check.get()

        if a.x[0] < b.x[0] <= a.x[1]:
            x, y = splitx(a, b.x[0])

        elif a.x[0] <= b.x[1] < a.x[1]:
            x, y = splitx(a, b.x[1]+1)

        elif a.y[0] < b.y[0] <= a.y[1]:
            x, y = splity(a, b.y[0])

        elif a.y[0] <= b.y[1] < a.y[1]:
            x, y = splity(a, b.y[1]+1)

        elif a.z[0] < b.z[0] <= a.z[1]:
            x, y = splitz(a, b.z[0])

        elif a.z[0] <= b.z[1] < a.z[1]:
            x, y = splitz(a, b.z[1]+1)

        else:
            atoms.append(a)
            continue

        # print(x, y)
        to_check.put(x)
        to_check.put(y)

    # print(atoms)
    return atoms


def find_overlap(a, b):
    xlow = max(a.x[0], b.x[0])
    xhigh = min(a.x[1], b.x[1])
    if xhigh < xlow:
        return None

    ylow = max(a.y[0], b.y[0])
    yhigh = min(a.y[1], b.y[1])
    if yhigh < ylow:
        return None

    zlow = max(a.z[0], b.z[0])
    zhigh = min(a.z[1], b.z[1])
    if zhigh < zlow:
        return None

    return Instruction(
        a.mode,
        (xlow, xhigh),
        (ylow, yhigh),
        (zlow, zhigh),
    )


def atomise(a, b):
    atoms = set([a])

    for n in b:
        if n == a:
            continue
        new = set()
        for x in atoms:
            overlap = find_overlap(x, n)
            if overlap is None or overlap == x:
                new.add(x)
            else:
                new.update(split_overlap(x, overlap))
        # print(len(new))
        atoms = new
    return atoms


def part2(instructions):
    atoms = set()

    for n in instructions:
        pieces = atomise(n, instructions)
        # print(len(pieces))
        if n.mode:
            atoms.update(pieces)
        else:
            atoms.difference_update(pieces)

        # print(atoms)

    return sum(n.size() for n in atoms)


def main():
    instructions = load_data('test-small.txt')
    print(part2(instructions))


if __name__ == '__main__':
    main()
