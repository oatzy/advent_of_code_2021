#!/usr/bin/env -S awk -f

# NOTE: requires -v OFMT="%.0f" to get part 2 in non-scientific format

# BEGIN{RS=","}
# {a[$1]++;t++}
# END{
#     for(;i<256;){
#         u=i++==80?t:u;
#         for(k in a){
#             n=a[k];
#             if(k!=0)b[k-1]+=n
#             else{
#                 t+=n;
#                 b[6]+=n;
#                 b[8]+=n
#             }
#             delete a[k]
#         }
#         for(k in b){a[k]=b[k];delete b[k]}
#     }
#     print u,t
# }

# mawk only (170 char)
BEGIN{RS=","}{a[$1]++;t++}END{while(i<256){u=i++==80?t:u;for(k in a){n=a[k];if(k!=0)b[k-1]+=n;else{t+=n;b[6]+=n;b[8]+=n}}delete a;for(k in b)a[k]=b[k];delete b}print u,t}

# honest solution, with inline format (182 char)
#BEGIN{OFMT="%0.f";RS=","}{a[$1]++;t++}END{while(i<256){u=i++==80?t:u;for(k in a){n=a[k];if(k!=0)b[k-1]+=n;else{t+=n;b[6]+=n;b[8]+=n}}delete a;for(k in b)a[k]=b[k];delete b}print u,t}


# awk compatible (178 char)
#BEGIN{RS=","}{a[$1]++;t++}END{while(i<256){u=i++==80?t:u;for(k in a){n=a[k];if(k!=0){b[k-1]+=n}else{t+=n;b[6]+=n;b[8]+=n}delete a[k]}for(k in b){a[k]=b[k];delete b[k]}}print u,t}