
def load_data(path):
    with open(path, 'r') as f:
        return [int(i) for i in f.read().split(',')]


def differences(data, n):
    return sum(abs(n-i) for i in data)


def part1(data):
    return min(differences(data, i) for i in range(max(data)))


def triangular(n):
    return n*(n+1)//2


def weighted_differences(data, n):
    return sum(triangular(abs(n-i)) for i in data)


def part2(data):
    return min(weighted_differences(data, i) for i in range(max(data)))


def main():
    data = load_data('input.txt')
    print(part1(data))
    print(part2(data))


if __name__ == '__main__':
    main()


class Test:

    def setup_method(self):
        self.data = load_data('test.txt')

    def test_differences(self):
        assert differences(self.data, 1) == 41
        assert differences(self.data, 2) == 37
        assert differences(self.data, 3) == 39
        assert differences(self.data, 10) == 71

    def test_part1(self):
        assert part1(self.data) == 37

    def test_weighted_differences(self):
        assert weighted_differences(self.data, 2) == 206
        assert weighted_differences(self.data, 5) == 168

    def test_part2(self):
        assert part2(self.data) == 168
