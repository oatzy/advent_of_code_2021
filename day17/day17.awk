#!/usr/bin/env -S awk -f

BEGIN{FS="=|\\."}{print $5*($5+1)/2}