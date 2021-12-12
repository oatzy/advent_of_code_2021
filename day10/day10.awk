# BEGIN{
#     FS=""
# }
# {
#     offset = 0;
#     for(i=1;i<=NF;i++){
#         w=index("([{<)]}>", $i);
#         if(w>4){
#             if(stack[offset]==w-4)offset--
#             else {  # corrupt
#                 p += w==5?3:w==6?57:w==7?1197:25137
#                 offset=0
#                 break
#             }
#         }else stack[++offset]=w
#     }
#     t=0
#     while(offset)  # incomplete
#         t=5*t+stack[offset--]
#     if(t){
#         for(j=0;j<incomplete;j++)if(t<q[j]){x=q[j];q[j]=t;t=x}
#         q[incomplete++] = t
#     }
# }
# END {
#     print p,q[incomplete/2-.5]
# }

# both parts (257 chars)
BEGIN{FS=""}{o=0;for(i=1;i<=NF;i++){w=index("([{<)]}>",$i);if(w>4){if(s[o]==w-4)o--;else{a+=w==5?3:w==6?57:w==7?1197:25137;o=0;break}}else s[++o]=w}t=0;while(o)t=5*t+s[o--];if(t){for(j=0;j<n;j++)if(t<b[j]){x=b[j];b[j]=t;t=x};b[n++]=t}}END{print a,b[n/2-.5]}
