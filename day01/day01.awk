#!/usr/bin/env -S awk -f

# this is dumb :p
NR>3 {part2 += ($0 > prev3)} NR>2 {prev3 = prev2} NR>1 {part1 += ($0 > prev); prev2 = prev} {prev = $0} END {print part1 "\n" part2}

# code golf (63 chars)
# NR>3{b+=($0>z)}NR>2{z=y}NR>1{a+=($0>x);y=x}{x=$0}END{print a,b}
