#!/usr/bin/env -S awk -f

# part1
#$1 == "forward" {x += $2} $1 == "down" {y += $2} $1 == "up" {y -= $2} END {print x*y}
# part2
#$1 == "forward" {x += $2; y += a * $2} $1 == "down" {a += $2} $1 == "up" {a -= $2} END {print x*y}

# part1, code golf (45 chars)
# /f/{x+=$2}/n/{y+=$2}/u/{y-=$2}END{print x*y}

# both parts, code golf (57 chars)
/f/{x+=$2;y+=a*$2}/n/{a+=$2}/u/{a-=$2}END{print x*a,x*y}