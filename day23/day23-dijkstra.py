from queue import PriorityQueue
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
    crabs = []

    with open(path, 'r') as f:
        for y, line in enumerate(f):
            for x, c in enumerate(line.rstrip()):

                if c in ENERGY:
                    # crab = (id, energy, pos)
                    crabs.append((ENERGY[c], (x, y)))

    return tuple(sorted(crabs))


def game_over(crabs):
    return all(c[1] in HOMES[c[0]] for c in crabs)


def occupied(crabs, p):
    for c in crabs:
        if c[1] == p:
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
    homes = HOMES[crab[0]]

    home_base = occupied(crabs, homes[1])
    if home_base == crab:
        return

    same_base_type = home_base is not None and home_base[0] == crab[0]

    if crab[1] == homes[0] and same_base_type:
        return

    for n in MOVES[crab[1]]:

        if occupied(crabs, n):
            continue

        h = home_of(n)
        g = home_of(crab[1])

        # moving from corridor to home
        if h is not None and g is None:

            if h != crab[0]:
                # can't enter another type's home
                continue

            # if different type already in home
            if home_base is not None and home_base[0] != crab[0]:
                continue

        yield n, step_size(n, crab[1])


def neighbours(crabs):
    for i, crab in enumerate(crabs):
        for move, size in possible_moves(crab, crabs):
            next_state = tuple(sorted(
                crabs[:i] + ((crab[0], move),) + crabs[i+1:]
            ))
            yield next_state, size * crab[0]


def dijkstra(start, end):
    distances = {start: 0}

    q = PriorityQueue()
    q.put((0, start))

    while not q.empty():
        dist, cur = q.get(block=False)
        if cur in distances and distances[cur] < dist:
            continue

        for n, size in neighbours(cur):

            tentative = size + distances[cur]
            if n not in distances or tentative < distances[n]:
                distances[n] = tentative
                q.put((tentative, n))

        if cur == end:
            break

    return distances[end]
    # return min(v for k, v in distances.items() if game_over(k))


def main():
    start = load_data('input.txt')
    end = []
    for t, ps in HOMES.items():
        for p in ps:
            end.append((t, p))
    end = tuple(sorted(end))
    print(dijkstra(start, end))


if __name__ == '__main__':
    main()
