#!/usr/bin/env python

# Takes hex dumps of packets as input on stdin, outputs parses on stdout
import sys
import struct

def packet_h(a):
    if a[0] != 'h' or a[1] != "\x1d":
        raise Exception("Invalid header")

    if a[-1] != '\x0a' or a[-2] != '\x00':
        raise Exception("Invalid header")


    if len(a) != 34:
        return {}

    def intat(i):
        rawv = struct.unpack("<I", a[i:i+4])[0]
        return rawv
        return int('{:032b}'.format(rawv)[::-1], 2)


    freq = intat(13)
    smeter = intat(0)
    agcish = intat(7)

    # Frequency seems to be at 13 on
    
    # Something at a[7] changes when idling
    # Also something at a[9]: signal strength?  AGC strength?

    v18 = "".join([ "%02x" % ord(c) for c in a[18:33] ])

    return {
        "freq": freq,
        "smeter": smeter,
        }


f0 = None
df = 0
for l in sys.stdin:
    line = "".join([ chr(int(l[i:i+2], 16)) for i in range(0, len(l)-1, 2) ])
    p = packet_h(line)


    
    if p != {}:
        if f0 == None:
            df = 0
        else:
            df = p["freq"] - f0

        print "%d %d" % (p["freq"], df)
        f0 = p["freq"]
        
