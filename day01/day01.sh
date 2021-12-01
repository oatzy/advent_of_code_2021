#!/usr/bin/env bash

awk 'NR>1 {inc += ($0 > prev)} {prev = $0} END {print inc}' input.txt

# this is dumb :p
awk 'NR>3 {inc += ($0 > prev3)} NR>2 {prev3 = prev2} NR>1 {prev2 = prev} {prev = $0} END {print inc}' input.txt
