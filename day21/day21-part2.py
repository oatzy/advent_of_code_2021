
# player = (pos, score)

def step(p, n, rolls):
    pos, score = p
    pos = (pos + n) % 10 or 10
    if rolls % 3 == 0:
        score += pos
    return (pos, score)


def is_winner(p):
    return p[1] >= 21


def roll(p1, p2, current, rolls):
    if rolls and rolls % 3 == 0:
        if is_winner(p1):
            #print("p1 win")
            return 1, 0
        elif is_winner(p2):
            #print("p2 win")
            return 0, 1
        # else swap players
        current = (current + 1) % 2

    s1, s2 = 0, 0

    for i in range(1, 4):
        # update current player for roll
        if current == 0:
            a, b = roll(step(p1, i, rolls+1), p2, current, rolls+1)
        else:
            a, b = roll(p1, step(p2, i, rolls+1), current, rolls+1)

        #print(rolls, i, a, b)
        s1 += a
        s2 += b

    return s1, s2


def play(p1, p2):
    s1, s2 = roll((p1, 0), (p2, 0), 0, 0)
    return max(s1, s2)


if __name__ == '__main__':
    print(play(10, 8))
