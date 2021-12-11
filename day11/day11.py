
def load_data(path):
    levels = {}

    with open(path, 'r') as f:
        for y, row in enumerate(f):
            for x, c in enumerate(row.strip()):  # trailing newline
                levels[(x, y)] = int(c)

    return levels


def print_levels(levels):
    prevy = 0
    for p, e in sorted(levels.items(), key=lambda i: (i[0][1], i[0][0])):
        if p[1] != prevy:
            prevy += 1
            print()
        print(e, end='')
    print('\n')


def adjacent(position):
    x, y = position
    yield (x-1, y-1)  # NW
    yield (x, y-1)  # N
    yield (x+1, y-1)  # NE
    yield (x+1, y)  # E
    yield (x+1, y+1)  # SE
    yield (x, y+1)  # S
    yield (x-1, y+1)  # SW
    yield (x-1, y)  # W


def step(levels):
    levels = {p: v+1 for p, v in levels.items()}
    flashes = []

    flashed = True
    while flashed:
        flashed = False

        for p, e in list(levels.items()):
            if e <= 9:
                continue

            flashed = True
            levels.pop(p)
            flashes.append(p)

            for a in adjacent(p):
                if a in levels:
                    levels[a] += 1

    for p in flashes:
        levels[p] = 0

    return levels


def part1(data):
    flashes = 0
    for _ in range(100):
        # print_levels(data)
        data = step(data)
        flashes += sum(1 for v in data.values() if v == 0)
    return flashes


def part2(data):
    t = 1
    while True:
        # print_levels(data)
        data = step(data)
        if all(v == 0 for v in data.values()):
            return t
        t += 1


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
        assert part1(self.data) == 1656

    def test_part2(self):
        assert part2(self.data) == 195
