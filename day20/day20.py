from typing import Set, Tuple
from dataclasses import dataclass

Point = Tuple[int, int]

PADDING = 50


@dataclass
class Scan:
    image: Set[Point]
    algorithm: str
    tl: Point
    br: Point


def load_data(path):
    with open(path, 'r') as f:
        algorithm, raw = f.read().split('\n\n')

    image = set()

    for y, line in enumerate(raw.splitlines()):
        for x, c in enumerate(line.strip()):
            if c == '#':
                image.add((x, y))

    return Scan(image, algorithm, (0, 0), (x, y))


def kernel(image, p):
    n = 0
    for y in range(p[1] - 1, p[1] + 2):
        for x in range(p[0] - 1, p[0] + 2):
            n |= (x, y) in image
            n <<= 1
    n >>= 1
    return n


def enhance(scan):
    new = set()

    for x in range(scan.tl[0], scan.br[0] + 1):
        for y in range(scan.tl[1], scan.br[1] + 1):
            if scan.algorithm[kernel(scan.image, (x, y))] == '#':
                new.add((x, y))

    return Scan(new, scan.algorithm, scan.tl, scan.br)


def expand(scan, size):
    return Scan(
        scan.image, scan.algorithm,
        (-2*size, -2*size),
        (scan.br[1]+2*size, scan.br[1]+2*size)
    )


def crop_padding(scan, padding):
    tl = (scan.tl[0]+padding, scan.tl[1]+padding)
    br = (scan.br[0]-padding, scan.br[1]-padding)
    image = set(
        (x, y) for x, y in scan.image
        if tl[0] <= x <= br[0] and tl[1] <= y <= br[1]
    )
    return Scan(image, scan.algorithm, tl, br)


def enhance_by(scan, size):
    scan = expand(scan, size)
    for _ in range(size):
        scan = enhance(scan)
    scan = crop_padding(scan, size)
    return scan


def illuminated(scan):
    return len(scan.image)


def print_image(scan):
    for y in range(scan.tl[1]-1, scan.br[1]+2):
        for x in range(scan.tl[0]-1, scan.br[0]+2):
            if (x, y) in scan.image:
                print('#', end='')
            else:
                print('.', end='')
        print()


def part1(scan):
    scan = enhance_by(scan, 2)
    return illuminated(scan)


def part2(scan):
    scan = enhance_by(scan, 50)
    return illuminated(scan)


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
        assert part1(self.data) == 35

    def test_part2(self):
        assert part2(self.data) == 3351
