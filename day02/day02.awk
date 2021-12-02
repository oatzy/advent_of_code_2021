#!/usr/bin/env -S awk -f

$1 == "forward" {x += $2} $1 == "down" {y += $2} $1 == "up" {y -= $2} END {print x*y}

# part1, co\de golf (45 chars)
# /f/{x+=$2}/n/{y+=$2}/u/{y-=$2}END{print x*y}