#!/usr/bin/env python

import sys

def byteses(l):
    l = l.replace(" ", "")
    a = [ int(l[i:i+2], 16) for i in range(0, len(l)-1, 2) ]
    return a


l0 = sys.stdin.readline() # prime it
h0 = byteses(l0)
#h0 = h0[13:17]

b0 = "".join([    '{:08b}'.format(i)[::-1] for i in h0 ])

def cof(x,y):
    if x == y:
        return " "
    if x < y:
        return "U"
    if x > y:
        return "d"


    #print "".join([ cof(x,y) for (x,y) in zip(b0, b0) ]) #+  "\t" + "".join(["%02x" % i for i in h0])

toggles = [0] * len(b0)
netchange = [0] * len(b0)
for l in sys.stdin:
    h = byteses(l)
    #h = h[13:17]

    b = "".join([    '{:08b}'.format(i)[::-1] for i in h ])

    darr = [ cof(x,y) for (x,y) in zip(b0, b) ]

    #print "".join(darr) #+ "\t" + "".join(["%02x" % i for i in h])

    for i in range(0, len(b0)):
        if darr[i] != " ":
            toggles[i] += 1
            if darr[i] == "U":
                netchange[i] += 1
            else:
                netchange[i] -= 1

    b0 = b

print str(toggles)
print str(netchange)
