

def load_data(path):
    with open(path, 'r') as f:
        return [list(map(int, line.strip())) for line in f]


def to_dec(bits):
    return sum(b << i for i, b in enumerate(bits[::-1]))


def part1(data):
    # one-liner for gamma
    # gamma = to_dec([(2 * sum(d[i] for d in data) > len(data)) for i in range(len(data[0]))])

    bits = [0 for _ in data[0]]

    for line in data:
        for i, b in enumerate(line):
            bits[i] += b

    gamma = to_dec([(2 * b > len(data)) for b in bits])
    epsilon = ((1 << len(bits)) - 1) ^ gamma  # flip bits

    return gamma * epsilon


def most_common(data, bit):
    return 2 * sum(d[bit] for d in data) >= len(data)


def oxygen_criteria(data, bit):
    return most_common(data, bit)


def scrubber_criteria(data, bit):
    return not most_common(data, bit)


def find_rating(data, bit_criteria):
    width = len(data[0])
    for bit in range(width):
        b = bit_criteria(data, bit)
        data = [d for d in data if d[bit] == b]
        if len(data) == 1:
            return to_dec(data[0])
    raise Exception("Oops, not found!")


def part2(data):
    return (
        find_rating(data, oxygen_criteria)
        * find_rating(data, scrubber_criteria)
    )


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
        assert part2(self.data) == 230
