#!/usr/bin/env python

meter_partial = "4c435341b12aa000060001100ab99a000bffff000000a99aa99ba0000001081e0408"
meter_empty   = "4c435341b12aa000060000100ab99a000b0000000000a99aa99ba0000001081e0400"

# 26 segments

def hex2bytes(s):
    return [ int(s[i:i+2], 16) for i in range(0, len(s)-1, 2) ]

mpb = hex2bytes(meter_partial)
mpe = hex2bytes(meter_empty)

delta = [ a^b for (a,b) in zip(mpb, mpe) ]

for i,p in list(enumerate(delta)):
    if p != 0:
        print str( (i,p) )

        # Looks like the smeter is at byte 17, probably has 26b from there.
