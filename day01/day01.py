
def part1(depths):
    return sum(depths[i] > depths[i-1] for i in range(1, len(depths)))


def part2(depths):
    """
    Comparing sliding 3-window
        (a + b + c) < (b + c + d)
    we can cancel out
        b + c
    which leaves us with
        a < d
    """
    return sum(depths[i] > depths[i-3] for i in range(3, len(depths)))


def main():
    with open('input.txt', 'r') as f:
        depths = [int(i) for i in f]

    print(part1(depths))
    print(part2(depths))


class Test:

    def setup_method(self):
        with open('test.txt', 'r') as f:
            self.depths = [int(i) for i in f]

    def test_part01(self):
        assert part1(self.depths) == 7

    def test_part02(self):
        assert part2(self.depths) == 5


if __name__ == '__main__':
    main()
