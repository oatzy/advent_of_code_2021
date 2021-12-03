

def load_data(path):
    with open(path, 'r') as f:
        return f.read().splitlines()


def part1(data):
    bits = [0 for _ in data[0]]

    for line in data:
        for i, b in enumerate(line[::-1]):
            bits[i] += int(b)

    lines = len(data)

    # binary list to int
    gamma = sum((b > lines//2) << i for i, b in enumerate(bits))
    epsilon = ((1 << len(data[0])) - 1) ^ gamma  # flip bits

    return gamma * epsilon


def part2(data):
    pass


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
        assert part1(self.data) == 198

    def test_part2(self):
        assert part2(self.data) == None
