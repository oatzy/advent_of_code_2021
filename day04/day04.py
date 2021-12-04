#!/usr/bin/env python3
from typing import List, Optional
from dataclasses import dataclass


def load_data(path: str) -> 'Bingo':
    with open(path, 'r') as f:
        data = f.read().split('\n\n')

    return Bingo(
        numbers=[int(i) for i in data[0].split(',')],
        boards=[Board.from_string(b) for b in data[1:]]
    )


@dataclass
class Bingo:
    numbers: List[int]
    boards: List['Board']


class Board:

    def __init__(self, board: List[List[Optional[int]]]):
        self._board = board

    def mark(self, number: int):
        for row in self._board:
            for i, n in enumerate(row):
                if n == number:
                    row[i] = None

    def _is_horizontal_win(self) -> bool:
        return any(all(i is None for i in row) for row in self._board)

    def _is_vertical_win(self) -> bool:
        return any(
            all(row[i] is None for row in self._board)
            for i in range(len(self._board[0]))
        )

    def is_winner(self) -> bool:
        return self._is_horizontal_win() or self._is_vertical_win()

    def total_remaining(self) -> int:
        return sum(
            sum(i for i in row if i is not None)
            for row in self._board
        )

    @classmethod
    def from_string(cls, string) -> 'Board':
        return cls([
            [int(i) for i in line.split()]
            for line in string.splitlines()
        ])


def part1(bingo: Bingo) -> int:
    for number in bingo.numbers:
        for board in bingo.boards:

            board.mark(number)

            if board.is_winner():
                return board.total_remaining() * number

    raise Exception("Oops, you've got a bug")


def part2(bingo: Bingo) -> int:
    winners = []

    for number in bingo.numbers:
        for i, board in enumerate(bingo.boards):
            if i in winners:
                continue

            board.mark(number)

            if board.is_winner():
                winners.append(i)

            if len(winners) == len(bingo.boards):
                return board.total_remaining() * number

    raise Exception("Oops, you've got a bug")


def main():
    data = load_data('input.txt')
    print(part1(data))
    # the boards are already marked from part 1
    # but it doesn't affect part 2
    print(part2(data))


if __name__ == '__main__':
    main()


class Test:

    def setup_method(self):
        self.data = load_data('test.txt')

    def test_part1(self):
        assert part1(self.data) == 4512

    def test_part2(self):
        assert part2(self.data) == 1924
