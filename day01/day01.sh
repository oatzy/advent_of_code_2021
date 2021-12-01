#!/usr/bin/env bash

# this is dumb :p
awk 'NR>3 {inc2 += ($0 > prev3)} NR>2 {prev3 = prev2} NR>1 {inc1 += ($0 > prev); prev2 = prev} {prev = $0} END {print inc1 "\n" inc2}' "${1:-input.txt}"
