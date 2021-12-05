#!/usr/bin/env bash

sed 's/ -> /,/' "$1" | awk -F, '$1==$3{d=$2<$4?1:-1;while($2!=$4+d){a[$1,$2]+=1;$2+=d}}$2==$4{d=$1<$3?1:-1;while($1!=$3+d){a[$1,$2]+=1;$1+=d}}END{for(k in a)t+=a[k]>1;print t}'
