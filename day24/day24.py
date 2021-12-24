from dataclasses import dataclass

CONSTANTS = (
    (11, 1, 6),
    (13, 1, 14),
    (15, 1, 14),
    (-8, 26, 10),
    (13, 1, 9),
    (15, 1, 12),
    (-11, 26, 8),
    (-4, 26, 13),
    (-15, 26, 12),
    (14, 1, 6),
    (14, 1, 9),
    (-1, 26, 15),
    (-8, 26, 4),
    (-14, 26, 10),
)


@dataclass
class ALU:
    w: int = 0
    x: int = 0
    y: int = 0
    z: int = 0

    def _maybe_variable(self, b):
        try:
            return int(b)
        except ValueError:
            return getattr(self, b)

    def inp(self, a, value):
        setattr(self, a, value)

    def add(self, a, b):
        v = getattr(self, a)
        v += self._maybe_variable(b)
        setattr(self, a, v)

    def mul(self, a, b):
        v = getattr(self, a)
        v *= self._maybe_variable(b)
        setattr(self, a, v)

    def div(self, a, b):
        v = getattr(self, a)
        v //= self._maybe_variable(b)
        setattr(self, a, v)

    def mod(self, a, b):
        v = getattr(self, a)
        v %= self._maybe_variable(b)
        setattr(self, a, v)

    def eql(self, a, b):
        v = getattr(self, a)
        v = v == self._maybe_variable(b)
        setattr(self, a, v)


def execute(program, inputs=None):
    alu = ALU()

    if inputs is not None:
        inputs = iter(inputs)

    for inst in program:
        if inst[0] == 'inp':
            alu.inp(inst[1], next(inputs))
        else:
            getattr(alu, inst[0])(inst[1], inst[2])

    return alu


def load_data(path):
    inst = []
    with open(path, 'r') as f:
        for line in f:
            line = line.split('#')[0].strip()
            if not line:
                continue
            inst.append(line.split())
    return inst


def validate(number):
    # manually translated into higher level constructs
    z = 0
    for w, (a, b, c) in zip(number, CONSTANTS):
        if (z % 26 + a) != w:
            z = 26 * (z//b) + w + c
        else:
            z //= b
    return z == 0

# brute-force approach - takes too long
# def decrement(x):
#     x = x[::-1]
#     for i, d in enumerate(x):
#         d -= 1
#         if d != 0:
#             x[i] = d
#             break
#         x[i] = 9
#     return x[::-1]


# def part1():
#     x = [9] * 14
#     while True:
#         if validate([9] + x + [1]):
#             return x

#         x = decrement(x)


def main():
    # part 1
    print(validate([9, 9, 3, 9, 4, 8, 9, 9, 8, 9, 1, 9, 7, 1]))
    # part 2
    print(validate([9, 2, 1, 7, 1, 1, 2, 6, 1, 3, 1, 9, 1, 1]))


if __name__ == '__main__':
    main()


class Test:

    def test_is_3_times(self):
        data = load_data('test-is-3-times.txt')

        alu = execute(data, [1, 3])
        assert alu.z == 1

        alu = execute(data, [1, 5])
        assert alu.z == 0

    def test_negate(self):
        data = load_data('test-negate.txt')

        alu = execute(data, [1])
        assert alu.x == -1

        alu = execute(data, [-3])
        assert alu.x == 3

    def test_to_binary(self):
        data = load_data('test-to-binary.txt')

        alu = execute(data, [5])
        assert alu.x == 1
        assert alu.y == 0
        assert alu.z == 1
        assert alu.w == 0
