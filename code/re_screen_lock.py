#!/usr/bin/env python

def hex2bytes(s):
    return [ int(s[i:i+2], 16) for i in range(0, len(s)-1, 2) ]


def which_bits_differ(s, t):
    mpb = hex2bytes(s)
    mpe = hex2bytes(t)

    delta = [ a^b for (a,b) in zip(mpb, mpe) ]

    retval = []

    for i,p in list(enumerate(delta)):
        if p != 0:
            for j in range(8):
                if 0 != p & (1<<j):
                    retval.append(8*i+j)


    return retval



cases = [
        ( "lock",
          "4c435341b12aa000060000000ad81ec81f000000cfafa99ae18de18c0001081e0400",
            "4c435341b12aa000060000100ad81ec81f000000cfafa99ae18fe18c0001081e0400"),

        ("star",
         "4c435341a12aa000060000000ad81ec81f000000ccdfa99aa081e18c0001e1040400",
         "4c435341a12aa000060000000ad81ec81f000000ccdfa99aa081e18c0000e1040400"),
        ]

for name,a,b in cases:
    print name + ": " + str(which_bits_differ(a,b))
