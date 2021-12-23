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

    def cubes(self):
        for i in range(self.x[0], self.x[1]+1):
            for j in range(self.y[0], self.y[1]+1):
                for k in range(self.z[0], self.z[1]+1):
                    yield (i, j, k)

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


def get_max_range(instructions):
    minx = maxx = miny = maxy = minz = maxz = None

    for i in instructions:
        if minx is None or minx > i.x[0]:
            minx = i.x[0]
        if maxx is None or maxx < i.x[1]:
            maxx = i.x[1]
        if miny is None or miny > i.y[0]:
            miny = i.y[0]
        if maxy is None or maxy < i.y[1]:
            maxy = i.y[1]
        if minz is None or minz > i.z[0]:
            minz = i.z[0]
        if maxz is None or maxz < i.z[1]:
            maxz = i.z[1]

    return (minx, maxx), (miny, maxy), (minz, maxz)


def part2(instructions):
    x, y, z = get_max_range(instructions)

    total = 0

    instructions = instructions[::-1]

    for i in range(x[0], x[1]+1):
        for j in range(y[0], y[1]+1):
            for k in range(z[0], z[1]+1):
                for n in instructions:
                    if n.in_range((i, j, k)):
                        total += n.mode
                        break

    return total


def part2_alt(instructions):
    total = 0
    instructions = instructions[::-1]

    for i, n in enumerate(instructions):
        if not n.mode:
            continue
        for p in n.cubes():
            for m in instructions[:i]:
                if m.in_range(p):
                    break
            else:
                total += 1

    return total


def part2_dumb(instructions):
    s = set()
    for i in instructions:
        if i.mode:
            s.update(i.cubes())
        else:
            s.difference_update(i.cubes())
    return len(s)


def main():
    data = load_data('test.txt')
    # print(part1(data))
    print(part2_alt(data))


if __name__ == '__main__':
    main()


class Test:

    import pytest

    def setup_method(self):
        self.data = load_data('test.txt')

    def test_part1_small(self):
        data = load_data('test-small.txt')
        assert part1(data) == 39

    def test_part1(self):
        assert part1(self.data) == 590784

    def test_part2_small(self):
        data = load_data('test-small.txt')
        assert part2_alt(data) == 39

    @pytest.mark.skip("not yet")
    def test_part2(self):
        assert part2(self.data) == None
