
ENERGY = {'A': 1, 'B': 10, 'C': 100, 'D': 1000}

HOMES = {
    1: ((3, 2), (3, 3)),
    10: ((5, 2), (5, 3)),
    100: ((7, 2), (7, 3)),
    1000: ((9, 2), (9, 3)),
}

MOVES = {
    (1, 1): ((2, 1),),
    (2, 1): ((1, 1), (3, 2), (4, 1)),
    (4, 1): ((2, 1), (3, 2), (5, 2), (6, 1)),
    (6, 1): ((4, 1), (5, 2), (7, 2), (8, 1)),
    (8, 1): ((6, 1), (7, 2), (9, 2), (10, 1)),
    (10, 1): ((8, 1), (9, 2), (11, 1)),
    (11, 1): ((10, 1),),
    (3, 2): ((2, 1), (4, 1), (3, 3)),
    (3, 3): ((3, 2),),
    (5, 2): ((4, 1), (6, 1), (5, 3)),
    (5, 3): ((5, 2),),
    (7, 2): ((6, 1), (8, 1), (7, 3)),
    (7, 3): ((7, 2),),
    (9, 2): ((8, 1), (10, 1), (9, 3)),
    (9, 3): ((9, 2),),
}


def load_data(path):
    id = 0

    crabs = []

    with open(path, 'r') as f:
        for y, line in enumerate(f):
            for x, c in enumerate(line.rstrip()):

                if c in ENERGY:
                    # crab = (id, energy, pos)
                    crabs.append((id, ENERGY[c], (x, y)))
                    id += 1

    return tuple(crabs)


def game_over(crabs):
    return all(c[2] in HOMES[c[1]] for c in crabs)


def occupied(crabs, p):
    for c in crabs:
        if c[2] == p:
            return c
    return None


def home_of(p):
    for t, h in HOMES.items():
        if p in h:
            return t
    return None


def step_size(p, q):
    return abs(p[0]-q[0])+abs(p[1]-q[1])


def possible_moves(crab, crabs):
    homes = HOMES[crab[1]]

    home_base = occupied(crabs, homes[1])
    if home_base == crab:
        return

    same_base_type = home_base is not None and home_base[1] == crab[1]

    if crab[2] == homes[0] and same_base_type:
        return

    for n in MOVES[crab[2]]:

        if occupied(crabs, n):
            continue

        h = home_of(n)
        g = home_of(crab[2])

        # moving from corridor to home
        if h is not None and g is None:

            if h != crab[1]:
                # can't enter another type's home
                continue

            # if different type already in home
            if home_base is not None and home_base[1] != crab[1]:
                continue

        yield n, step_size(n, crab[2])


def path_finder(crabs, seen, energy=0, depth=0):
    if game_over(crabs):
        print(f"game over {energy}")
        return energy

    if crabs in seen:
        # backtrack
        # print(f"seen {crabs}")
        return None

    if depth >= 50:
        # give up, avoid max recursion
        return None

    seen.add(crabs)

    min_move = None

    for i, crab in enumerate(crabs):
        for move, step in possible_moves(crab, crabs):
            #print(crab, move)
            next_state = (
                crabs[:i] + ((crab[0], crab[1], move),) + crabs[i+1:]
            )
            d = path_finder(next_state, seen, energy+step * crab[1], depth+1)

            if d is None:
                # deadend
                continue

            if min_move is None or d < min_move:
                min_move = d

    return min_move


def part1(crabs):
    return path_finder(crabs, set())


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

    def test_game_over(self):
        crabs = []
        for t, ps in HOMES.items():
            for p in ps:
                crabs.append((0, t, p))
        assert game_over(tuple(crabs))

    def test_part1(self):
        # print(self.data)
        assert part1(self.data) == 12521

    def test_part2(self):
        assert part2(self.data) == None
