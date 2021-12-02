#!/usr/bin/env python3

def read_input(path):
    items = []
    with open(path, 'r') as f:
        for line in f:
            direction, distance = line.split()
            items.append((direction, int(distance)))
    return items


def part1(directions):
    x = y = 0
    for d in directions:
        if d[0] == 'forward':
            x += d[1]
        elif d[0] == 'down':
            y += d[1]
        elif d[0] == 'up':
            y -= d[1]
    return x * y


def part2(directions):
    x = y = aim = 0
    for d in directions:
        if d[0] == 'forward':
            x += d[1]
            y += aim * d[1]
        elif d[0] == 'down':
            aim += d[1]
        elif d[0] == 'up':
            aim -= d[1]
    return x * y


def main():
    directions = read_input('input.txt')

    print(part1(directions))
    print(part2(directions))


if __name__ == '__main__':
    main()


class Test:

    def setup_method(self):
        self.directions = read_input('test.txt')

    def test_part1(self):
        assert part1(self.directions) == 150

    def test_part2(self):
        assert part2(self.directions) == 900
