BEGIN{
    FS=""
    pairs=" ()[]{}<>"
    score[")"]=3;score["]"]=57;score["}"]=1197;score[">"]=25137
}
{
    offset = 0;
    for(i=1;i<=NF;i++){
        if($i in score){
            if(substr(pairs,index(pairs,stack[offset])+1,1)==$i)offset--
            else {  # corrupt
                p += score[$i]
                offset=0
                break
            }
        }else stack[++offset]=$i
    }
    t=0
    while(offset)  # incomplete
        t=5*t+index(pairs,stack[offset--])/2
    if(t){
        for(j=0;j<incomplete;j++)if(t<q[j]){x=q[j];q[j]=t;t=x}
        q[incomplete++] = t
    }
}
END {
    print p,q[incomplete/2-.5]
}

# both parts (305 chars)
#BEGIN{FS="";p=" ()[]{}<>";c[")"]=3;c["]"]=57;c["}"]=1197;c[">"]=25137}{o=0;for(i=1;i<=NF;i++){if($i in c){if(substr(p,index(p,s[o])+1,1)==$i)o--;else{a+=c[$i];o=0;break}}else s[++o]=$i}t=0;while(o)t=5*t+index(p,s[o--])/2;if(t){for(j=0;j<n;j++)if(t<b[j]){x=b[j];b[j]=t;t=x};b[n++]=t}}END{print a,b[n/2-.5]}

# part1 (191 chars)
#{FS="";p="()[]{}<>";c[")"]=3;c["]"]=57;c["}"]=1197;c[">"]=25137;o=0;for(i=1;i<=NF;i++){if($i in c){if(substr(p,index(p,s[o])+1,1)==$i)o--;else{a+=c[$i];o=0;break}}else s[++o]=$i}}END{print a}
