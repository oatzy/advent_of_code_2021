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


def count_paths(graph, node, visited):
    if node == 'END':
        return 1

    neighbours = [
        n for n in graph[node]
        if n.isupper() or n not in visited
    ]

    paths = 0
    for n in neighbours:
        paths += count_paths(graph, n, {n, *visited})

    return paths


def part1(graph):
    return count_paths(graph, 'START', set())


def count_paths_with_revisit(graph, node, visited):
    if node == 'END':
        return 1

    can_revisit = not any(v == 2 for v in visited.values())

    paths = 0
    for n in graph[node]:
        if n.isupper():
            paths += count_paths_with_revisit(graph, n, visited)
        elif visited[n] == 0 or can_revisit:
            v = visited.copy()
            v[n] += 1
            paths += count_paths_with_revisit(graph, n, v)

    return paths


def part2(graph):
    return count_paths_with_revisit(graph, 'START', Counter())


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
