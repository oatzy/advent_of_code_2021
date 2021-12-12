from collections import Counter, defaultdict


def load_data(path):
    graph = defaultdict(list)

    with open(path, 'r') as f:
        for line in f:

            a, b = line.strip().split('-')

            if a == 'start':
                graph['START'].append(b)
            elif b == 'start':
                graph['START'].append(a)

            elif b == 'end':
                graph[a].append('END')
            elif a == 'end':
                graph[b].append('END')

            else:
                graph[a].append(b)
                graph[b].append(a)

    return graph


def cached_count(fn):
    # can't use functools cache_lru because some params are unhashable
    # so hand-roll a bespoke version
    cache = {}

    def inner(graph, node, visited, max_visits=1):
        # dict keys must be hashable
        key = (tuple(graph.keys()), node, tuple(visited.items()), max_visits)

        if key not in cache:
            count = fn(graph, node, visited, max_visits)
            cache[key] = count

        return cache[key]

    return inner


@cached_count
def _count_paths(graph, node, visited, max_visits=1):
    if node == 'END':
        return 1

    can_revisit = not any(v == max_visits for v in visited.values())

    paths = 0
    for n in graph[node]:

        if n.isupper():
            paths += _count_paths(graph, n, visited, max_visits)

        elif visited[n] == 0 or can_revisit:
            v = visited.copy()
            v[n] += 1
            paths += _count_paths(graph, n, v, max_visits)

    return paths


def count_paths(graph, max_visits=1):
    return _count_paths(graph, 'START', Counter(), max_visits=max_visits)


def part1(graph):
    return count_paths(graph)


def part2(graph):
    return count_paths(graph, max_visits=2)


def main():
    data = load_data('input.txt')
    print(part1(data))
    print(part2(data))


if __name__ == '__main__':
    main()


class Test:

    def test_part1_small(self):
        assert part1(load_data('test.txt')) == 10

    def test_part1_medium(self):
        assert part1(load_data('test1.txt')) == 19

    def test_part1_large(self):
        assert part1(load_data('test2.txt')) == 226

    def test_part2_small(self):
        assert part2(load_data('test.txt')) == 36

    def test_part2_medium(self):
        assert part2(load_data('test1.txt')) == 103

    def test_part2_large(self):
        assert part2(load_data('test2.txt')) == 3509
