#!/usr/bin/env bash

awk 'NR>1 {inc += ($0 > prev)} {prev = $0} END {print inc}' input.txt