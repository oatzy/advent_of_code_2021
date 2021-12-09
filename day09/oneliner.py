# 195 char (when not auto-formatted)
print((lambda d: sum(d[p]+1 for p in d if all(d[p] < d.get((p[0]+i, p[1]+j), 10) for i, j in [(1, 0), (0, 1),
                                                                                              (-1, 0), (0, -1)])))({(x, y): int(c) for y, r in enumerate(open('i')) for x, c in enumerate(r[:-1])}))
