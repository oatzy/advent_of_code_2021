#!/usr/bin/env bash

#tac "$@" | awk 'BEGIN{FS=","}/=/{split($1,a,"=");d=a[2];i=$0~/x/?1:2}NF>1{d<$i?$i=2*d-$i:0;t+=!s[$1,$2]++}END{print t}'

# 89 chars awk; 110 char total
tac "$@" | awk -F, '/=/{split($1,a,"=");d=a[2];i=$0~/x/?1:2}NF>1{d<$i?$i=2*d-$i:0;t+=!s[$1,$2]++}END{print t}'