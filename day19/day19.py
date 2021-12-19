from math import sqrt


def load_data(path):
    scanners = []

    with open(path, 'r') as f:
        raw_scanners = f.read().split('\n\n')

    for s in raw_scanners:
        scanners.append([
            tuple(map(int, l.split(',')))
            for l in s.splitlines()[1:]
        ])

    return scanners


def rotate(p):
    return (p[1], p[2], p[0])


def flipx(p):
    return (-p[0], p[1], p[2])


def flipy(p):
    return (p[0], -p[1], p[2])


def flipz(p):
    return (p[0], p[1], -p[2])


def rotators():
    yield lambda p: p
    yield lambda p: (p[2], p[1], -p[0])
    yield lambda p: (-p[0], p[1], -p[2])
    yield lambda p: (-p[2], p[1], p[0])
    yield lambda p: (-p[1], p[0], p[2])
    yield lambda p: (p[2], p[0], p[1])
    yield lambda p: (p[1], p[0], -p[2])
    yield lambda p: (-p[2], p[0], -p[1])
    yield lambda p: (p[0], p[2], -p[1])
    yield lambda p: (-p[1], p[2], -p[0])
    yield lambda p: (-p[0], p[2], p[1])
    yield lambda p: (p[1], p[2], p[0])
    yield lambda p: (p[0], -p[1], -p[2])
    yield lambda p: (-p[2], -p[1], -p[0])
    yield lambda p: (-p[0], -p[1], p[2])
    yield lambda p: (p[2], -p[1], p[0])
    yield lambda p: (-p[1], -p[0], -p[2])
    yield lambda p: (-p[2], -p[0], p[1])
    yield lambda p: (p[1], -p[0], p[2])
    yield lambda p: (p[2], -p[0], -p[1])
    yield lambda p: (p[0], -p[2], p[1])
    yield lambda p: (p[1], -p[2], -p[0])
    yield lambda p: (-p[0], -p[2], -p[1])
    yield lambda p: (-p[1], -p[2], p[0])


def rotations(ps):
    for r in rotators():
        yield [r(p) for p in ps]


def relative_to(ref, p):
    return (p[0] - ref[0], p[1] - ref[1], p[2] - ref[2])


def centers(ps):
    for p in ps:
        yield [relative_to(p, q) for q in ps]


def variants(ps):
    for r in rotations(ps):
        yield from centers(r)


def move_to(p, ps):
    q = min(ps)
    delta = relative_to(p, q)
    return [relative_to(delta, q) for q in ps]


def is_overlap(s1, s2):
    return len(set(s1).intersection(s2)) >= 12


def try_overlap(ref, scanner):
    for r in rotations(scanner):
        for p in ref:
            for q in r:
                delta = relative_to(p, q)
                aligned = [relative_to(delta, t) for t in r]
                if is_overlap(ref, aligned):
                    return aligned
    return None


def find_orientations(scanners):
    ref = scanners[0]
    found = {0: ref}

    # find the rest
    while len(found) != len(scanners):
        print(list(found))
        for i, s in enumerate(scanners):
            if i in found:
                continue

            for j, f in found.items():
                overlap = try_overlap(f, s)
                if overlap is None:
                    continue
                found[i] = overlap
                print(f"scanner {j} overlaps scanner {i}")
                break

    print(list(found))
    assert len(found) == len(scanners)
    # print(found)

    return list(found.values())


def part1(data):
    unique = set()
    for beacon in find_orientations(data):
        unique.update(beacon)
    return len(unique)


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
        assert part1(self.data) == 79

    def test_part2(self):
        assert part2(self.data) == None
