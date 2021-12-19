
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


def rotators():
    # there's a way to do this with matricies and the like
    # but I ended up just hand-enumerating them
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


def is_overlap(s1, s2):
    return len(set(s1).intersection(s2)) >= 12


def try_overlap(ref, scanner):
    # for every rotation, try aligning each point
    # against each point of reference
    # until we get an overlap
    #
    # given how slow this process is
    # I have to assume there's a quicker way
    for r in rotations(scanner):
        for p in ref:
            for q in r:
                delta = relative_to(p, q)
                aligned = [relative_to(delta, t) for t in r]
                if is_overlap(ref, aligned):
                    return aligned, delta
    return None, None


def get_alignment(scanners):
    ref = scanners[0]
    found = {0: ref}
    offsets = [(0, 0, 0)]

    while len(found) != len(scanners):
        # print(list(found))
        for i, s in enumerate(scanners):
            if i in found:
                continue

            for j, f in found.items():
                overlap, offset = try_overlap(f, s)
                if overlap is None:
                    continue
                found[i] = overlap
                offsets.append(offset)
                #print(f"scanner {j} overlaps scanner {i} at {offset}")
                break

    return list(found.values()), offsets


def part1(orientations):
    unique = set()
    for beacon in orientations:
        unique.update(beacon)
    return len(unique)


def distance(a, b):
    return abs(a[0]-b[0]) + abs(a[1] - b[1]) + abs(a[2] - b[2])


def part2(offsets):
    distances = []
    for a in offsets:
        for b in offsets:
            distances.append(distance(a, b))
    return max(distances)


def main():
    data = load_data('input.txt')
    orientations, offsets = get_alignment(data)
    print(part1(orientations))
    print(part2(offsets))


if __name__ == '__main__':
    main()


class Test:

    def setup_class(self):
        self.data = load_data('test.txt')
        self.orientations, self.offsets = get_alignment(self.data)

    def test_part1(self):
        assert part1(self.orientations) == 79

    def test_part2(self):
        assert part2(self.offsets) == 3621
