#!/usr/bin/env -S awk -f

BEGIN{RS=","}
{a[$1]++;t++}
END{
    for(i=0;i<256;i++){
        if(i==80)print t;
        for(k in a){
            n=a[k];
            if(k!=0){
                b[k-1]+=n
            }else{
                t+=n;
                b[6]+=n;
                b[8]+=n
            }
        }
        delete a;
        for(k in b)a[k]=b[k];
        delete b;
    }
    print t
}

#BEGIN{RS=","}{a[$1]++;t++}END{for(i=0;i<256;i++){if(i==80)print t;for(k in a){n=a[k];if(k!=0){b[k-1]+=n}else{t+=n;b[6]+=n;b[8]+=n}}delete a;for(k in b)a[k]=b[k];delete b}print t}