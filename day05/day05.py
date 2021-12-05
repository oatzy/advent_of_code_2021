
from collections import Counter


def load_data(path):
    lines = []
    with open(path, 'r') as f:
        for line in f:
            start, end = line.split(' -> ')
            lines.append((
                tuple(int(i) for i in start.split(',')),
                tuple(int(i) for i in end.split(',')),
            ))
    return lines


def horizontal(start, end):
    y = start[1]
    if start[0] < end[0]:
        xmin, xmax = start[0], end[0]
    else:
        xmin, xmax = end[0], start[0]

    for x in range(xmin, xmax+1):
        yield (x, y)


def vertical(start, end):
    x = start[0]
    if start[1] < end[1]:
        ymin, ymax = start[1], end[1]
    else:
        ymin, ymax = end[1], start[1]

    for y in range(ymin, ymax+1):
        yield (x, y)


def diagonal(start, end):
    # strictly 45deg, so x,y change by +/-1 each step

    # by sorting, x is always strictly increasing
    start, end = sorted([start, end])

    if start[1] < end[1]:
        dy = 1
    else:
        dy = -1

    current = start
    while current != end:
        yield current
        current = (current[0] + 1, current[1] + dy)

    yield end


def count_overlaps(lines, include_diagonal=False):
    grid = Counter()

    for start, end in lines:

        if start[0] == end[0]:
            points = vertical(start, end)
        elif start[1] == end[1]:
            points = horizontal(start, end)
        elif include_diagonal:
            points = diagonal(start, end)
        else:
            continue

        for point in points:
            grid[point] += 1

    return sum(1 for v in grid.values() if v >= 2)


def part1(lines):
    return count_overlaps(lines)


def part2(lines):
    return count_overlaps(lines, include_diagonal=True)


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
        assert part1(self.data) == 5

    def test_part2(self):
        assert part2(self.data) == 12
