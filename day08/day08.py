from dataclasses import dataclass
from typing import List


def load_data(path):
    with open(path, 'r') as f:
        return [Entry.from_str(l) for l in f]


def strsort(string):
    return "".join(sorted(string))


@dataclass
class Entry:
    digits: List[str]
    display: List[str]

    @classmethod
    def from_str(cls, string):
        digits, display = string.split(' | ')
        return cls(
            list(map(strsort, digits.split())),
            list(map(strsort, display.split())),
        )


def infer(digits):
    remaining = []
    mapping = {}

    # pick out digits with unique lengths
    for d in digits:
        if len(d) == 2:
            one = d
            mapping[d] = '1'
        elif len(d) == 4:
            four = d
            mapping[d] = '4'
        elif len(d) == 3:
            mapping[d] = '7'
        elif len(d) == 7:
            mapping[d] = '8'
        else:
            remaining.append(d)

    # chars in 4 but not 1 -> b and d
    bd = {c: [] for c in four if c not in one}
    for d in remaining:
        for c in bd:
            # 'd' appears in everything except 0
            if c not in d:
                bd[c].append(d)

    for ds in bd.values():
        if len(ds) == 1:
            zero = ds[0]
            mapping[ds[0]] = '0'
            remaining.remove(zero)

    # of remaining, b doesn't appears in only 2 and 3
    b = [c for c in bd if c in zero][0]

    for d in list(remaining):
        if b in d:
            continue
        # b has all the chars in 1
        if all(c in d for c in one):
            mapping[d] = '3'
            remaining.remove(d)
        else:
            # 2 doesn't
            mapping[d] = '2'
            remaining.remove(d)

    # of remaining
    for d in remaining:
        # 5 is only only one with 5 chars
        if len(d) == 5:
            mapping[d] = '5'
        # 9 is the only one with all chars from 1
        elif all(c in d for c in one):
            mapping[d] = '9'
        else:
            # 6 is whatever is left
            mapping[d] = '6'

    return mapping


def decode(entry: Entry):
    mapping = infer(entry.digits)
    return int("".join(
        mapping[i] for i in entry.display
    ))


def part1(entries):
    return sum(
        sum(1 for d in e.display if len(d) not in (5, 6))
        for e in entries
    )


def part2(entries):
    return sum(decode(e) for e in entries)


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
        assert part1(self.data) == 26

    def test_infer(self):
        digits = [
            "acedgfb", "cdfbe", "gcdfa", "fbcad", "dab",
            "cefabd", "cdfgeb", "eafb", "cagedb", "ab"
        ]
        assert infer(digits) == {
            "acedgfb": '8',
            "cdfbe": '5',
            "gcdfa": '2',
            "fbcad": '3',
            "dab": '7',
            "cefabd": '9',
            "cdfgeb": '6',
            "eafb": '4',
            "cagedb": '0',
            "ab": '1',
        }

    def test_decode(self):
        assert decode(Entry.from_str(
            "acedgfb cdfbe gcdfa fbcad dab cefabd cdfgeb eafb cagedb ab | cdfeb fcadb cdfeb cdbaf"
        )) == 5353

    def test_decode_more_cases(self):
        expect = [
            8394,
            9781,
            1197,
            9361,
            4873,
            8418,
            4548,
            1625,
            8717,
            4315,
        ]
        for entry, exp in zip(self.data, expect):
            assert decode(entry) == exp

    def test_part2(self):
        assert part2(self.data) == 61229
