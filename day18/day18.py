from ast import literal_eval


def load_data(path):
    with open(path, 'r') as f:
        return [literal_eval(l) for l in f.read().splitlines()]


def iter_nodes_with_literal(number):
    if isinstance(number[0], int):
        yield number
        if isinstance(number[1], int):
            return
    else:
        yield from iter_nodes_with_literal(number[0])
    if isinstance(number[1], int):
        yield number
    else:
        yield from iter_nodes_with_literal(number[1])


def snail_sum(numbers):
    total = numbers[0]
    for number in numbers[1:]:
        total = add(total, number)
    return total


def add(left, right):
    return reduce([left, right])


def reduce(number):
    while True:
        if try_explode(number, root=number, depth=0):
            continue
        if try_split(number):
            continue
        break
    return number


def try_explode(number, root, depth=0):
    for i, n in enumerate(number):
        if isinstance(n, int):
            continue

        if depth >= 3:
            # explode
            explode(root, n)
            number[i] = 0
            return True

        # recurse
        elif try_explode(n, root=root, depth=depth+1):
            return True

    return False


def try_split(number):
    for i, n in enumerate(number):
        if isinstance(n, int):
            # split
            if n >= 10:
                number[i] = [n//2, n//2 + n % 2]
                return True

        # recurse
        elif try_split(n):
            return True

    return False


def explode(root, node):
    prev = None
    for n in iter_nodes_with_literal(root):
        if n is node:
            if prev is None:
                pass
            elif isinstance(prev[1], int):
                prev[1] += node[0]
            else:
                prev[0] += node[0]
        elif prev is node:
            if isinstance(n[0], int):
                n[0] += node[1]
            else:
                n[1] += node[1]
        prev = n


def magnitude(number):
    if isinstance(number, int):
        return number
    return 3 * magnitude(number[0]) + 2 * magnitude(number[1])


def part1(data):
    total = snail_sum(data)
    return magnitude(total)


def part2(data):
    pass


def main():
    data = load_data('input.txt')
    print(part1(data))
    print(part2(data))


if __name__ == '__main__':
    main()


class Test:
    import pytest

    def test_iter_nodes(self):
        assert list(iter_nodes_with_literal([1, 2])) == [[1, 2]]
        assert list(iter_nodes_with_literal([[1, 2], 3])) == [
            [1, 2], [[1, 2], 3]]
        assert list(iter_nodes_with_literal([1, [2, 3]])) == [
            [1, [2, 3]], [2, 3]]
        assert list(iter_nodes_with_literal([[1, 2], [3, 4]])) == [
            [1, 2], [3, 4]]

    def test_split_even(self):
        assert reduce([10, 0]) == [[5, 5], 0]

    def test_split_odd(self):
        assert reduce([11, 0]) == [[5, 6], 0]

    def test_split_multiple(self):
        assert reduce([11, 10]) == [[5, 6], [5, 5]]

    def test_split_example(self):
        number = [[[[0, 7], 4], [15, [0, 13]]], [1, 1]]
        assert try_split(number)
        assert number == [[[[0, 7], 4], [[7, 8], [0, 13]]], [1, 1]]
        assert try_split(number)
        assert number == [[[[0, 7], 4], [[7, 8], [0, [6, 7]]]], [1, 1]]

    def test_explode(self):
        assert reduce([[[[[9, 8], 1], 2], 3], 4]) == [[[[0, 9], 2], 3], 4]
        assert reduce([7, [6, [5, [4, [3, 2]]]]]) == [7, [6, [5, [7, 0]]]]
        assert reduce([[6, [5, [4, [3, 2]]]], 1]) == [[6, [5, [7, 0]]], 3]
        #assert reduce([[3,[2,[1,[7,3]]]],[6,[5,[4,[3,2]]]]]) == [[3,[2,[8,0]]],[9,[5,[4,[3,2]]]]]
        assert reduce([[3, [2, [8, 0]]], [9, [5, [4, [3, 2]]]]]) == [
            [3, [2, [8, 0]]], [9, [5, [7, 0]]]]

    def test_explode_example(self):
        number = [[[[[4, 3], 4], 4], [7, [[8, 4], 9]]], [1, 1]]
        assert try_explode(number, root=number)
        assert number == [[[[0, 7], 4], [7, [[8, 4], 9]]], [1, 1]]
        assert try_explode(number, root=number)
        assert number == [[[[0, 7], 4], [15, [0, 13]]], [1, 1]]

    def test_add(self):
        assert add([[[[4, 3], 4], 4], [7, [[8, 4], 9]]], [1, 1]) == [
            [[[0, 7], 4], [[7, 8], [6, 0]]], [8, 1]]

    def test_add_basic(self):
        assert add([1, 2], [[3, 4], 5]) == [[1, 2], [[3, 4], 5]]

    def test_add_multi_step(self):
        number = [[[0, [4, 5]], [0, 0]], [[[4, 5], [2, 6]], [9, 5]]]
        number = add(number, [7, [[[3, 7], [4, 3]], [[6, 3], [8, 8]]]])
        assert number == [[[[4, 0], [5, 4]], [[7, 7], [6, 0]]], [
            [8, [7, 7]], [[7, 9], [5, 0]]]]

    def test_magnitude(self):
        assert magnitude([[1, 2], [[3, 4], 5]]) == 143
        assert magnitude([[[[0, 7], 4], [[7, 8], [6, 0]]], [8, 1]]) == 1384
        assert magnitude([[[[1, 1], [2, 2]], [3, 3]], [4, 4]]) == 445
        assert magnitude([[[[3, 0], [5, 3]], [4, 4]], [5, 5]]) == 791
        assert magnitude([[[[5, 0], [7, 4]], [5, 5]], [6, 6]]) == 1137
        assert magnitude([[[[8, 7], [7, 7]], [[8, 6], [7, 7]]], [
                         [[0, 7], [6, 6]], [8, 7]]]) == 3488

    def test_snail_sum1(self):
        numbers = [[1, 1], [2, 2], [3, 3], [4, 4]]
        assert snail_sum(numbers) == [[[[1, 1], [2, 2]], [3, 3]], [4, 4]]

    def test_snail_sum2(self):
        numbers = [[1, 1], [2, 2], [3, 3], [4, 4], [5, 5]]
        assert snail_sum(numbers) == [[[[3, 0], [5, 3]], [4, 4]], [5, 5]]

    def test_snail_sum3(self):
        numbers = [[1, 1], [2, 2], [3, 3], [4, 4], [5, 5], [6, 6]]
        assert snail_sum(numbers) == [[[[5, 0], [7, 4]], [5, 5]], [6, 6]]

    def test_snail_sum_test_txt(self):
        assert snail_sum(load_data('test.txt')) == [[[[6, 6], [7, 6]], [[7, 7], [7, 0]]], [
            [[7, 7], [7, 7]], [[7, 8], [9, 9]]]]

    def test_snail_sum_test1_txt(self):
        assert snail_sum(load_data('test1.txt')) == [
            [[[8, 7], [7, 7]], [[8, 6], [7, 7]]], [[[0, 7], [6, 6]], [8, 7]]]

    def test_part1(self):
        assert part1(load_data('test.txt')) == 4140

    def test_part2(self):
        assert part2(load_data('test.txt')) == None
