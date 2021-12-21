from collections import Counter
from dataclasses import dataclass, field
from functools import lru_cache

BOARD_SIZE = 10


@dataclass
class Player:
    position: int
    score: int = 0

    def move(self, step):
        # 10 % 10 == 0, but we want it to == 10
        self.position = (self.position + step) % BOARD_SIZE or BOARD_SIZE
        self.score += self.position


@dataclass
class Die:
    value: int = 0
    rolls: int = 0

    def roll(self, n=1) -> int:
        total = 0
        for _ in range(n):
            self.rolls += 1
            self.value += 1
            total += self.value
        return total


@dataclass
class Game:
    player1: Player
    player2: Player
    die: Die = field(default_factory=Die)
    target: int = 1000

    def is_over(self) -> bool:
        return (
            self.player1.score >= self.target or
            self.player2.score >= self.target
        )

    @classmethod
    def new(cls, player1pos, player2pos) -> 'Game':
        return Game(Player(player1pos), Player(player2pos))


def play(game):
    current, next = game.player1, game.player2
    d = game.die

    while not game.is_over():
        current.move(d.roll(3))
        current, next = next, current


def load_data(path):
    with open(path, 'r') as f:
        p1, p2 = f.read().splitlines()

    return Game.new(
        int(p1.split()[-1]),
        int(p2.split()[-1]),
    )


def part1(game) -> int:
    play(game)
    return game.die.rolls * min(game.player1.score, game.player2.score)


def _rolls():
    for i in range(1, 4):
        for j in range(1, 4):
            for k in range(1, 4):
                yield i+j+k


DIRAC_ROLLS = list(Counter(_rolls()).items())


@lru_cache()
def step(p, n):
    pos, score = p
    pos = (pos + n) % BOARD_SIZE or BOARD_SIZE
    return (pos, score + pos)


@lru_cache()
def dirac_roll(p1, p2):
    w1, w2 = 0, 0

    for r, c in DIRAC_ROLLS:
        pn = step(p1, r)

        if pn[1] >= 21:
            a, b = (1, 0)

        else:
            # swap current player
            b, a = dirac_roll(p2, pn)

        w1 += c*a
        w2 += c*b

    return w1, w2


def part2(game):
    s1, s2 = dirac_roll(
        (game.player1.position, 0),
        (game.player2.position, 0)
    )
    return max(s1, s2)


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
        assert part1(self.data) == 739785

    def test_part2(self):
        assert part2(self.data) == 444356092776315
