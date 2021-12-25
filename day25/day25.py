from dataclasses import dataclass
from itertools import count
from typing import Dict, Tuple

Point = Tuple[int, int]


@dataclass
class Map:
    cucumbers: Dict[Point, str]
    width: int
    height: int


def load_data(path):
    cucumbers = {}

    with open(path, 'r') as f:
        for y, line in enumerate(f):
            for x, c in enumerate(line.strip()):
                if c in '>v':
                    cucumbers[(x, y)] = c

    return Map(cucumbers, x+1, y+1)


def iterate(cucumbers, width, height):
    new = {}

    for (x, y), v in cucumbers.items():
        if v == '>':
            n = ((x+1) % width, y)
            if n not in cucumbers:
                new[n] = v
                continue
        new[(x, y)] = v

    cucumbers = {}
    for (x, y), v in new.items():
        if v == 'v':
            n = (x, (y+1) % height)
            if n not in new:
                cucumbers[n] = v
                continue
        cucumbers[(x, y)] = v

    return Map(cucumbers, width, height)


def print_map(map):
    for y in range(map.height):
        for x in range(map.width):
            print(map.cucumbers.get((x, y), '.'), end='')
        print()
    print()


def part1(data):
    for i in count(1):
        new = iterate(data.cucumbers, data.width, data.height)
        if new.cucumbers == data.cucumbers:
            return i
        data = new


def main():
    data = load_data('input.txt')
    print(part1(data))


if __name__ == '__main__':
    main()


class Test:

    def setup_method(self):
        self.data = load_data('test.txt')

    def test_part1(self):
        assert part1(self.data) == 58
