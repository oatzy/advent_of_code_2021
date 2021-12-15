from typing import Dict, Tuple
from dataclasses import dataclass
from queue import PriorityQueue

Node = Tuple[int, int]


@dataclass
class Graph:
    nodes: Dict[Node, int]
    start: Node
    end: Node


def load_data(path):
    nodes = {}
    with open(path, 'r') as f:
        for y, line in enumerate(f):
            for x, c in enumerate(line.strip()):
                nodes[(x, y)] = int(c)

    return Graph(nodes, (0, 0), (x, y))


def neighbours(node):
    x, y = node
    yield (x, y - 1)  # N
    yield (x + 1, y)  # E
    yield (x, y + 1)  # S
    yield (x - 1, y)  # W


def dijkstra(nodes, start, end):
    visited = set()
    distances = {n: None for n in nodes}
    distances[start] = 0

    cur = start

    while cur != end:
        visited.add(cur)

        to_check = [
            n for n in neighbours(cur)
            if n in distances and n not in visited
        ]

        for n in to_check:
            tentative = nodes[n] + distances[cur]
            if distances[n] is None or tentative < distances[n]:
                distances[n] = tentative

        cur = min(
            (d, n) for n, d in distances.items()
            if d is not None and n not in visited
        )[1]

    return distances[end]


def dijkstra_queue(nodes, start, end):
    distances = {n: None for n in nodes}
    distances[start] = 0

    q = PriorityQueue()
    q.put((0, start))

    while not q.empty():
        dist, cur = q.get(block=False)
        if distances[cur] is not None and distances[cur] < dist:
            continue

        for n in neighbours(cur):
            if n not in nodes:
                continue

            tentative = nodes[n] + distances[cur]
            if distances[n] is None or tentative < distances[n]:
                distances[n] = tentative
                q.put((tentative, n))

        if cur == end:
            break

    return distances[end]


def part1(graph):
    return dijkstra(graph.nodes, graph.start, graph.end)


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
        assert part1(self.data) == 40

    def test_part2(self):
        assert part2(self.data) == None
