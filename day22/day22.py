from typing import Tuple
from dataclasses import dataclass

Range = Tuple[int, int]

MAX_RANGE = (-50, 50)


def clamped_range(start, end):
    s = max(start, MAX_RANGE[0])
    e = min(end, MAX_RANGE[1])
    return range(s, e + 1)


@dataclass
class Instruction:
    mode: bool
    x: Range
    y: Range
    z: Range

    def cubes_clamped(self):
        cubes = set()

        for i in clamped_range(*self.x):
            for j in clamped_range(*self.y):
                for k in clamped_range(*self.z):
                    cubes.add((i, j, k))

        return cubes

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


def part1(instructions):
    cubes = set()

    for i in instructions:
        delta = i.cubes_clamped()
        if i.mode:
            cubes.update(delta)
        else:
            cubes.difference_update(delta)

    return len(cubes)


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
        not a.mode,
        (xlow, xhigh),
        (ylow, yhigh),
        (zlow, zhigh),
    )


def part2(instructions):
    atoms = [instructions[0]]

    for n in instructions[1:]:
        new = []
        for a in atoms:
            new.append(a)
            overlap = find_overlap(a, n)
            if overlap is not None:
                new.append(overlap)
        if n.mode:
            new.append(n)
        atoms = new

    return sum(n.size() if n.mode else -n.size() for n in atoms)


def main():
    data = load_data('input.txt')
    print(part1(data))
    print(part2(data))


if __name__ == '__main__':
    main()


class Test:

    import pytest

    def test_part1_small(self):
        data = load_data('test-small.txt')
        assert part1(data) == 39

    def test_part1(self):
        assert part1(load_data('test.txt')) == 590784

    def test_part2_small(self):
        data = load_data('test-small.txt')
        assert part2(data) == 39

    def test_part2(self):
        assert part2(load_data('test2.txt')) == 2758514936282235
