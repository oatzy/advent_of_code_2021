#!/usr/bin/env -S awk -f

# part one, (92 chars)
BEGIN{FS=""}{for(i=1;i<=NF;i++)a[NF-i]+=$i}END{for(k in a)2*a[k]>NR?g+=2^k:e+=2^k;print g*e}