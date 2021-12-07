#!/usr/bin/env -S awk -f

# BEGIN{FS=","}
# {
#     for(i=1;i<=NF;i++){
#         a[i]=$i;
#         m=$i>m?$i:m
#     }
# } END {
#     t=NF*m;
#     u=t*(m+1)/2;
#     for(;j<=m;j++){
#         y=0;z=0;
#         for(k in a){
#             d=j>a[k]?j-a[k]:a[k]-j;
#             y+=d;z+=d*(d+1)/2}
#         t=y<t?y:t;
#         u=z<u?z:u
#     }
#     print t,u
# }

# 183 chars
BEGIN{FS=","}{for(i=1;i<=NF;i++){a[i]=$i;m=$i>m?$i:m}}END{t=NF*m;u=t*(m+1)/2;for(;j<=m;j++){y=0;z=0;for(k in a){d=j>a[k]?j-a[k]:a[k]-j;y+=d;z+=d*(d+1)/2}t=y<t?y:t;u=z<u?z:u}print t,u}