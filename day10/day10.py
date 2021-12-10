PAIRS = {'(': ')', '[': ']', '{': '}', '<': '>'}
CORRUPT_SCORES = {')': 3, ']': 57, '}': 1197, '>': 25137}
INCOMPLETE_SCORES = {')': 1, ']': 2, '}': 3, '>': 4}


class Corrupted(Exception):

    def __init__(self, char, offset):
        self.char = char
        self.offset = offset
        super().__init__(f"Unexpected '{char}' at {offset}")


class Incomplete(Exception):

    def __init__(self, unclosed):
        self.unclosed = unclosed
        super().__init__(f"Got unclosed brackets {''.join(unclosed)}")


def load_data(path):
    with open(path, 'r') as f:
        return f.read().splitlines()


def check(line):
    # using exceptions to approximate sum-types
    stack = []

    for i, c in enumerate(line):
        if c in PAIRS:
            stack.append(c)
        elif PAIRS[stack.pop()] != c:
            raise Corrupted(c, i)

    if stack:
        raise Incomplete(stack)


def part1(data):
    total = 0
    for line in data:

        try:
            check(line)
        except Corrupted as exc:
            total += CORRUPT_SCORES[exc.char]
        except Incomplete:
            continue

    return total


def complete_score(unclosed):
    total = 0
    # closing brackets are in reverse order
    for c in unclosed[::-1]:
        total = total*5 + INCOMPLETE_SCORES[PAIRS[c]]
    return total


def part2(data):
    scores = []
    for line in data:

        try:
            check(line)
        except Corrupted:
            continue
        except Incomplete as exc:
            scores.append(complete_score(exc.unclosed))

    return sorted(scores)[len(scores)//2]


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
        assert part1(self.data) == 26397

    def test_part2(self):
        assert part2(self.data) == 288957
