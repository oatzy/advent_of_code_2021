#!/usr/bin/env -S awk -f

# BEGIN{RS=","}
# {
#     a[NR]=$1;
#     m=$1>m?$1:m
# } END {
#     t=NR*m;
#     u=t*m;
#     for(;x<m;x++){
#         y=z=0;
#         for(k in a){
#             d=x-a[k];d=d<0?-d:d;
#             y+=d;z+=d*(d+1)/2}
#         t=y<t?y:t;
#         u=z<u?z:u
#     }
#     print t,u
# }

# 152 chars
BEGIN{RS=","}{a[NR]=$1;m=$1>m?$1:m}END{t=NR*m;u=t*m;for(;x<m;x++){y=z=0;for(k in a){d=x-a[k];d=d<0?-d:d;y+=d;z+=d*(d+1)/2}t=y<t?y:t;u=z<u?z:u}print t,u}