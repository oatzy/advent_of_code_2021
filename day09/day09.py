from dataclasses import dataclass
from functools import reduce
from operator import mul
from typing import Dict, Tuple

Point = Tuple[int, int]


@dataclass
class HeightMap:
    heights: Dict[Point, int]


def load_data(path):
    heights = {}

    with open(path, 'r') as f:
        for y, row in enumerate(f):
            for x, c in enumerate(row.strip()):  # trailing newline
                heights[(x, y)] = int(c)

    return HeightMap(heights)


def adjacent(point: Point):
    x, y = point
    yield (x - 1, y)  # west
    yield (x, y - 1)  # north
    yield (x + 1, y)  # east
    yield (x, y + 1)  # south


def is_lowest(heights, point):
    # out-of-bounds points return default (10)
    # which is larger than any in-bounds point
    return all(heights[point] < heights.get(a, 10) for a in adjacent(point))


def lowest_point_from(heights, point):
    # return the lowest point that can be reached
    # by always descending from a given point
    #
    # could memoize, but would need to deal with dict being unhashable
    # (also, the code is fast enough as is)
    lowest_adj = min((heights.get(a, 10), a) for a in adjacent(point))

    if heights[point] < lowest_adj[0]:  # we're already at the bottom
        return point

    # we have to go deeper!
    return lowest_point_from(heights, lowest_adj[1])


def part1(data):
    return sum(
        h + 1 for p, h in data.heights.items()
        if is_lowest(data.heights, p)
    )


def part2(data):
    basins = {p: 0 for p in data.heights if is_lowest(data.heights, p)}

    for p, h in data.heights.items():
        if h == 9:
            continue
        basins[lowest_point_from(data.heights, p)] += 1

    return reduce(mul, sorted(basins.values())[-3:])


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
        assert part1(self.data) == 15

    def test_part2(self):
        assert part2(self.data) == 1134
