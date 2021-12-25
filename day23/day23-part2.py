import heapq


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

# ((home1), (home2), (home3), (home4), (corridor))


MASK = 0b111


def make_state(homes):
    i = 0
    new = []
    for home in homes:
        new_home = []
        for n in home:
            new_home.append((i << 3) | n)
            i += 1
        new.append(tuple(new_home))
    new.append((0,) * 7)
    return tuple(new)


def can_enter_home(homes, t):
    home = homes[t-1]
    return all((i & MASK) == t for i in home)


def is_blocked(corridor, cur, home):
    if cur <= home:
        return any(corridor[j] for j in range(cur+1, home+1))
    else:
        return any(corridor[j] for j in range(home+1, cur))


def possible_moves(corridor, i):
    j = i + 1
    while j < len(corridor) and not corridor[j]:
        yield j
        j += 1

    while i >= 0 and not corridor[i]:
        yield i
        i -= 1


def step_size(corridor, home):
    if corridor == 0:
        return step_size(1, home) + 1
    if corridor == 6:
        return step_size(5, home) + 1
    h = 2 * home
    c = 2 * corridor - 1
    return abs(h-c)


def neighbours(state):
    homes = state[:-1]
    corridor = state[-1]

    for h, home in enumerate(homes, 1):
        if all((t & MASK) == h for t in home):
            # all the crabs are in the right place
            continue

        candidate = home[-1]

        for c in possible_moves(corridor, h):
            new_state = (
                homes[:h-1] + (home[:-1],) + homes[h:] +
                (corridor[:c] + (candidate,) + corridor[c+1:],)
            )
            step = 4 - len(home) + 1 + step_size(c, h)
            yield new_state, step * 10**((candidate & MASK)-1)

    for c, a in enumerate(corridor):
        if not a:
            # empty square
            continue

        t = a & MASK

        if can_enter_home(homes, t) and not is_blocked(corridor, c, t):
            new_state = (
                homes[:t-1] + (homes[t-1] + (a,),) + homes[t:] +
                (corridor[:c] + (0,) + corridor[c+1:],)
            )
            step = 4 - len(homes[t-1]) + step_size(c, t)
            yield new_state, step * 10**(t-1)


def is_end(state):
    homes = state[:-1]
    corridor = state[-1]
    if any(corridor):
        return False
    for h, home in enumerate(homes, 1):
        if not all((i & MASK) == h for i in home):
            return False
    return True


def print_state(s):
    c = {0: '.', 1: 'A', 2: 'B', 3: 'C', 4: 'D'}
    rooms = [{i: c[n & MASK] for i, n in enumerate(r)} for r in s[:-1]]
    print('#############')
    corridor = c[s[-1][0] & MASK] + \
        '.'.join(c[i & MASK] for i in s[-1][1:-1]) + c[s[-1][-1] & MASK]
    print(f'#{corridor}#')
    r1 = '#'.join(r.get(3, '.') for r in rooms)
    print(f'###{r1}###')
    r2 = '#'.join(r.get(2, '.') for r in rooms)
    print(f'  #{r2}#')
    r3 = '#'.join(r.get(1, '.') for r in rooms)
    print(f'  #{r3}#')
    r4 = '#'.join(r.get(0, '.') for r in rooms)
    print(f'  #{r4}#')
    print('  #########')


def unpack_state(s):
    print([[(i & MASK, i >> 3) for i in b] for b in s])


def print_path(path, end):
    p = []
    cur = end
    while cur is not None:
        p.append(cur)
        cur = path[cur]
    for s in p[::-1]:
        print_state(s)
        print()


def dijkstra(start, end):
    distances = {start: 0}

    q = Queue()  # PriorityQueue()
    q.put([0, start])
    path = {start: None}

    while not q.empty():
        dist, cur = q.get()
        if cur in distances and distances[cur] < dist:
            continue

        for n, size in neighbours(cur):

            tentative = size + distances[cur]
            if n not in distances or tentative < distances[n]:
                distances[n] = tentative
                path[n] = cur
                q.put([tentative, n])

        # if cur == end:
        #     break
        if is_end(cur):
            print_path(path, cur)
            return distances[cur]

    return distances[end]


def main():
    # start = make_state((
    #     (1, 4, 4, 2),
    #     (4, 2, 3, 3),
    #     (3, 1, 2, 2),
    #     (1, 3, 1, 4)
    # ))
    start = make_state((
        (3, 4, 4, 4),
        (3, 2, 3, 1),
        (2, 1, 2, 1),
        (2, 3, 1, 4)
    ))
    end = ((1,)*4, (2,)*4, (3,)*4, (4,)*4, (0,)*7)

    print(dijkstra(start, end))


if __name__ == '__main__':
    main()
