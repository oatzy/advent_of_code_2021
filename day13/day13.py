from dataclasses import dataclass
from typing import Tuple, List


@dataclass
class Instructions:
    dots: List[Tuple[int, int]]
    folds: List[Tuple[str, int]]


def load_data(path):
    with open(path, 'r') as f:
        coords, fold = f.read().split('\n\n')

    dots = [tuple(map(int, l.split(','))) for l in coords.splitlines()]

    folds = []
    for line in fold.splitlines():
        f = line.split()[-1]
        axis, n = f.split('=')
        folds.append((axis, int(n)))

    return Instructions(dots, folds)


def print_dots(dots):
    max_x = max(x for x, _ in dots)
    max_y = max(y for _, y in dots)

    for y in range(max_y + 1):
        for x in range(max_x + 1):
            print('#' if (x, y) in dots else '.', end='')
        print()


def perform_fold(dots, fold):
    inx = int(fold[0] == 'y')
    fold = fold[1]

    new = set()

    for dot in dots:
        d = [*dot]
        if d[inx] > fold:
            d[inx] = 2 * fold - d[inx]
        new.add(tuple(d))

    return new


def part1(data):
    return len(perform_fold(data.dots, data.folds[0]))


def part2(data):
    dots = data.dots

    for fold in data.folds:
        dots = perform_fold(dots, fold)

    print_dots(dots)


def main():
    data = load_data('input.txt')
    print(part1(data))
    part2(data)


if __name__ == '__main__':
    main()


class Test:

    def test_part1(self):
        assert part1(load_data('test.txt')) == 17
