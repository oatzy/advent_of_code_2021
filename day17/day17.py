import re
from dataclasses import dataclass
from math import floor, sqrt


@dataclass
class Probe:
    vx: int
    vy: int
    x: int = 0
    y: int = 0

    def step(self):
        self.x += self.vx
        self.y += self.vy
        self.vy -= 1
        if self.vx:
            self.vx += 1 if self.vx < 0 else -1


@dataclass
class Trench:
    minx: int
    maxx: int
    miny: int
    maxy: int

    def is_hit(self, probe):
        return (
            self.minx <= probe.x <= self.maxx and
            self.miny <= probe.y <= self.maxy
        )

    def is_miss(self, probe):
        return probe.x > self.maxx or probe.y < self.miny


def fire(probe, trench):
    while not trench.is_miss(probe):
        probe.step()
        if trench.is_hit(probe):
            return True
    return False


def max_vy(trench):
    return - trench.miny - 1


def min_vx(trench):
    return int(floor(sqrt(2 * trench.minx) - 0.5))


def load_data(path):
    with open(path, 'r') as f:
        s = f.read().strip()
    m = re.match(
        "target area: x=(.+)\\.\\.(.+), y=(.+)\\.\\.(.+)", s
    )
    return Trench(*map(int, m.groups()))


def part1(trench):
    # motion in x and y are independent
    # max vy lands the probe at the bottom of the trench
    # the probe goes up distance Y and comes to rest (vy=0)
    # then comes down Y to 0 + distance to bottom of trench
    vy = max_vy(trench)
    return vy * (vy + 1) // 2


def part2(trench):
    minx = min_vx(trench)
    maxx = trench.maxx
    miny = trench.miny
    maxy = max_vy(trench)

    total = 0
    for vx in range(minx, maxx + 1):
        for vy in range(miny, maxy + 1):
            total += fire(Probe(vx, vy), trench)

    return total


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
        assert part1(self.data) == 45

    def test_part2(self):
        assert part2(self.data) == 112
