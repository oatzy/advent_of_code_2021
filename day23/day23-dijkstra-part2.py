import heapq
from math import log10
from queue import PriorityQueue

ENERGY = {'A': 1, 'B': 10, 'C': 100, 'D': 1000}

HOMES = {
    1: ((3, 2), (3, 3), (3, 4), (3, 5)),
    10: ((5, 2), (5, 3), (5, 4), (5, 5)),
    100: ((7, 2), (7, 3), (7, 4), (7, 5)),
    1000: ((9, 2), (9, 3), (9, 4), (9, 5)),
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
    (3, 3): ((3, 2), (3, 4)),
    (3, 4): ((3, 3), (3, 5)),
    (3, 5): ((3, 4),),
    (5, 2): ((4, 1), (6, 1), (5, 3)),
    (5, 3): ((5, 2), (5, 4)),
    (5, 4): ((5, 3), (5, 5)),
    (5, 5): ((5, 4),),
    (7, 2): ((6, 1), (8, 1), (7, 3)),
    (7, 3): ((7, 2), (7, 4)),
    (7, 4): ((7, 3), (7, 5)),
    (7, 5): ((7, 4),),
    (9, 2): ((8, 1), (10, 1), (9, 3)),
    (9, 3): ((9, 2), (9, 4)),
    (9, 4): ((9, 3), (9, 5)),
    (9, 5): ((9, 4),),
}

INX = {k: i for i, k in enumerate(MOVES)}
RINX = {v: k for k, v in INX.items()}


def to_hash(crabs):
    # convert a list of crabs into an integer
    h = 0
    for c in crabs:
        x = int(log10(c[0])) + 1
        x <<= 3*INX[c[1]]
        h |= x
    return h


def from_hash(h):
    crabs = []
    for i in range(len(RINX)):
        x = h & 7
        if x:
            crabs.append((10**(x-1), RINX[i]))
        h >>= 3
    return crabs


def load_data(path):
    crabs = []

    with open(path, 'r') as f:
        for y, line in enumerate(f):
            for x, c in enumerate(line.rstrip()):

                if c in ENERGY:
                    # crab = (id, energy, pos)
                    crabs.append((ENERGY[c], (x, y)))

    return crabs


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
    at_home = [occupied(crabs, h) for h in homes]

    if crab in at_home:
        h = at_home.index(crab)
        if all(
            at_home[i] is not None and at_home[i][0] == crab[0]
            for i in range(h, len(at_home))
        ):
            return

        if all(
            at_home[i] is None or at_home[i][0] == crab[0]
            for i in range(h, len(at_home))
        ):
            if h+1 < len(homes) and at_home[h+1] is None:
                yield homes[h+1], step_size(homes[h+1], crab[1])
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
            if any(c is not None and c[0] != crab[0] for c in at_home):
                continue

        yield n, step_size(n, crab[1])


def neighbours(crabs):
    crabs = from_hash(crabs)
    for i, crab in enumerate(crabs):
        for move, size in possible_moves(crab, crabs):
            next_state = to_hash((
                crabs[:i] + [(crab[0], move)] + crabs[i+1:]
            ))
            yield next_state, size * crab[0]


def h(s, end):
    return 0  # abs(s - end)


class Queue:
    # priority queue which will re-prioritise an item
    # if it is already present with a lower priority

    def __init__(self):
        self._queue = []
        self._items = {}

    def empty(self):
        return not self._queue

    def put(self, item):
        p, i = item
        if i not in self._items:
            heapq.heappush(self._queue, item)
            self._items[i] = item
        elif self._items[i][0] > p:
            self._items[i][0] = p
            heapq._siftdown(self._queue, 0, self._queue.index(item))

    def get(self):
        item = heapq.heappop(self._queue)
        self._items.pop(item[1])
        return item


def dijkstra(start, end):
    distances = {start: 0}

    q = Queue()  # PriorityQueue()
    q.put([0, start])

    while not q.empty():
        dist, cur = q.get()
        dist -= h(cur, end)
        if cur in distances and distances[cur] < dist:
            continue

        for n, size in neighbours(cur):

            tentative = size + distances[cur]
            if n not in distances or tentative < distances[n]:
                distances[n] = tentative
                q.put([tentative + h(n, end), n])

        if cur == end:
            break

    return distances[end]


def main():
    start = load_data('input2.txt')
    end = []
    for t, ps in HOMES.items():
        for p in ps:
            end.append((t, p))
    print(dijkstra(to_hash(start), to_hash(end)))


if __name__ == '__main__':
    main()
