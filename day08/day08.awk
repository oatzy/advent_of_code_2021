#!/usr/bin/env -S awk -f

# part1 only (49 char)
{for(i=12;i<16;i++)t+=length($i)%5>1}END{print t}
