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

    def in_range(self, p):
        return (
            self.x[0] <= p[0] <= self.x[1] and
            self.y[0] <= p[1] <= self.y[1] and
            self.z[0] <= p[2] <= self.z[1]
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


def part1_alt(instructions):
    # for curiosity's sake
    # works, but slower than sets
    total = 0

    instructions = instructions[::-1]

    for x in range(-50, 51):
        for y in range(-50, 51):
            for z in range(-50, 51):
                for i in instructions:
                    if i.in_range((x, y, z)):
                        total += i.mode
                        break

    return total


def part2(data):
    pass


def main():
    data = load_data('input.txt')
    print(part1(data))
    print(part2(data))


if __name__ == '__main__':
    main()


class Test:

    def setup_method(self):
        self.data = load_data('test.txt')

    def test_part1_small(self):
        data = load_data('test-small.txt')
        assert part1(data) == 39

    def test_part1(self):
        assert part1(self.data) == 590784

    def test_part2(self):
        assert part2(self.data) == None
