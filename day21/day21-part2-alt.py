from functools import lru_cache
from collections import Counter


def rolls():
    for i in range(1, 4):
        for j in range(1, 4):
            for k in range(1, 4):
                yield i+j+k


ROLLS = list(Counter(rolls()).items())


@lru_cache()
def step(p, n):
    pos, score = p
    pos = (pos + n) % 10 or 10
    score += pos
    return (pos, score)


def roll(p1, p2):
    cache = {}

    w1, w2 = 0, 0

    for r in rolls():
        if r not in cache:
            pn = step(p1, r)

            if pn[1] >= 21:
                cache[r] = (1, 0)

            else:
                # swap current player
                y, x = roll(p2, pn)
                cache[r] = (x, y)

        a, b = cache[r]
        w1 += a
        w2 += b

    return w1, w2


@lru_cache()
def cached_roll(p1, p2):
    w1, w2 = 0, 0

    for r, c in ROLLS:
        pn = step(p1, r)

        if pn[1] >= 21:
            a, b = (1, 0)

        else:
            # swap current player
            b, a = cached_roll(p2, pn)

        w1 += c*a
        w2 += c*b

    #print(w1, w2)
    return w1, w2


def play(p1, p2):
    s1, s2 = cached_roll((p1, 0), (p2, 0))
    return max(s1, s2)


if __name__ == '__main__':
    print(play(10, 8))
