from queue import PriorityQueue


def can_enter_home(homes, t):
    home = homes[t-1]
    return all(i == t for i in home)


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
    depth = state[0]
    homes = state[1:-1]
    corridor = state[-1]

    for h, home in enumerate(homes, 1):
        if all(t == h for t in home):
            # all the crabs are in the right place
            continue

        candidate = home[-1]

        for c in possible_moves(corridor, h):
            new_state = (
                (depth,) +
                homes[:h-1] + (home[:-1],) + homes[h:] +
                (corridor[:c] + (candidate,) + corridor[c+1:],)
            )
            step = depth - len(home) + 1 + step_size(c, h)
            yield new_state, step * 10**(candidate-1)

    for c, t in enumerate(corridor):
        if not t:
            # empty square
            continue

        if can_enter_home(homes, t) and not is_blocked(corridor, c, t):
            new_state = (
                (depth,) +
                homes[:t-1] + (homes[t-1] + (t,),) + homes[t:] +
                (corridor[:c] + (0,) + corridor[c+1:],)
            )
            step = depth - len(homes[t-1]) + step_size(c, t)
            yield new_state, step * 10**(t-1)


def print_state(s):
    c = {0: '.', 1: 'A', 2: 'B', 3: 'C', 4: 'D'}

    depth = s[0]
    rooms = [{i: c[n] for i, n in enumerate(r)} for r in s[1:-1]]
    corridor = c[s[-1][0]] + '.'.join(c[i] for i in s[-1][1:-1]) + c[s[-1][-1]]

    print('#############')
    print(f'#{corridor}#')
    for i in range(depth-1, 0, -1):
        r1 = '#'.join(r.get(i, '.') for r in rooms)
        print(f'###{r1}###')
    print('  #########')


def print_path(path, end):
    p = []
    cur = end
    while cur is not None:
        p.append(cur)
        cur = path[cur]
    for s in p[::-1]:
        print_state(s)
        print()


def is_final_state(state):
    rooms = state[1:-1]
    if any(state[-1]):
        return False
    for t, r in enumerate(rooms, 1):
        if not all(i == t for i in r):
            return False
    return True


def find_minimum_energy(start):
    # a dijkstra based approach
    distances = {start: 0}

    q = PriorityQueue()
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

        if is_final_state(cur):
            return distances[cur]

    raise Exception("No solution was found")


def _split_line(l):
    c = {'A': 1, 'B': 2, 'C': 3, 'D': 4}
    return [c[i] for i in l.strip(' #').split('#')]


def load_data(path):
    with open(path, 'r') as f:
        lines = f.read().splitlines()

    homes = tuple(zip(*[_split_line(l) for l in lines[3:1:-1]]))

    # (depth, (home1), (home2), (home3), (home4), (corridor))
    return (len(homes[0]),) + homes + ((0,) * 7,)


def expand(state):
    #D#C#B#A#
    #D#B#A#C#
    return (
        4,
        (state[1][0], 4, 4, state[1][1]),
        (state[2][0], 2, 3, state[2][1]),
        (state[3][0], 1, 2, state[3][1]),
        (state[4][0], 3, 1, state[4][1]),
        state[-1],
    )


def part1(state):
    return find_minimum_energy(state)


def part2(state):
    state = expand(state)
    return find_minimum_energy(state)


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
        assert part1(self.data) == 12521

    def test_part2(self):
        assert part2(self.data) == 44169
