
def load_data(path):
    with open(path, 'r') as f:
        return f.read().splitlines()


def part1(data):
    pass


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
        assert part1(self.data) == None

    def test_part2(self):
        assert part2(self.data) == None
