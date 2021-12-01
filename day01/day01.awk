#!/usr/bin/env -S awk -f

# this is dumb :p
NR>3 {part2 += ($0 > prev3)} NR>2 {prev3 = prev2} NR>1 {part1 += ($0 > prev); prev2 = prev} {prev = $0} END {print part1 "\n" part2}
