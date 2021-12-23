def switched_off(instructions, p):
    for n in instructions[::-1]:
        if n.in_range(p):
            return not n.mode
    return False


def already_counted(instructions, p):
    for n in instructions:
        if n.in_range(p):
            return n.mode
    return False


def part2_alt(instructions):
    total = 0
    for i, n in enumerate(instructions):
        for p in n.cubes():
            if not already_counted(instructions[:i], p) and not switched_off(instructions[i+1:], p):
                total += 1
    return total
