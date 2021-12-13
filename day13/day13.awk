#!/usr/bin/env -S awk -f

# BEGIN{FS=",";M=1000}
# NF>1{s[$1*M+$2]++}
# /=/{
#     split($1,a,"=");d=a[2];
#     if($0~/x/){i=1;X=d}else{i=2;Y=d}
#     for(k in s){
#         $1=int(k/M);$2=k%M;
#         d<$i?$i=2*d-$i:0;
#         t+=s[M*$1+$2]++<2*!p
#     }p=1
# }
# END{
#     print t
#     for(;y<Y;y++){
#         for(x=0;x<X;x++){
#             printf M*x+y in s?"#":"."
#         }
#         print ""
#     }
# }


# part 2 only, 230 chars
#BEGIN{FS=",";M=1000}NF>1{s[$1*M+$2]++}/=/{split($1,a,"=");d=a[2];if($0~/x/){i=1;X=d}else{i=2;Y=d}for(k in s){$1=int(k/M);$2=k%M;d<$i?$i=2*d-$i:0;s[M*$1+$2]++}}END{for(;y<Y;y++){for(x=0;x<X;x++){printf M*x+y in s?"#":"."}print ""}}

# both parts (247 chars)
BEGIN{FS=",";M=1e3}NF>1{s[$1*M+$2]++}/=/{split($1,a,"=");d=a[2];if($0~/x/){i=1;X=d}else{i=2;Y=d}for(k in s){$1=int(k/M);$2=k%M;d<$i?$i=2*d-$i:0;t+=s[M*$1+$2]++<2*!p}p=1}END{print t;for(;y<Y;y++){for(x=0;x<X;x++){printf M*x+y in s?"#":"."}print""}}