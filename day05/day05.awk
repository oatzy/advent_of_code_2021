#!/usr/bin/env -S awk -f

# part 1 (162 char)
#BEGIN{FS=" -> |,"}$1==$3{d=$2<$4?1:-1;while($2!=$4+d){a[$1,$2]+=1;$2+=d}}$2==$4{d=$1<$3?1:-1;while($1!=$3+d){a[$1,$2]+=1;$1+=d}}END{for(k in a)t+=a[k]>1;print t}

# part 2 (149 char)
#BEGIN{FS=" -> |,"}{c=$1<$3?1:$1>$3?-1:0;d=$2<$4?1:$2>$4?-1:0;while($1!=$3+c||$2!=$4+d){a[$1,$2]+=1;$1+=c;$2+=d}}END{for(k in a)t+=a[k]>1;print t}

# both parts, using '-v p=0' for part1 or '-v p=1' for part2 (162 char)
#BEGIN{FS=" -> |,"}p||$1==$3||$2==$4{x=$1<$3?1:$1>$3?-1:0;y=$2<$4?1:$2>$4?-1:0;while($1!=$3+x||$2!=$4+y){z[$1,$2]+=1;$1+=x;$2+=y}}END{for(k in z)t+=z[k]>1;print t}

# both parts (185 chars)
BEGIN{FS=" -> |,"}{x=$1<$3?1:$1>$3?-1:0;y=$2<$4?1:$2>$4?-1:0;while($1!=$3+x||$2!=$4+y){a[$1,$2]+=$1==$3||$2==$4;b[$1,$2]+=1;$1+=x;$2+=y}}END{for(k in b){t+=a[k]>1;u+=b[k]>1};print t, u}
