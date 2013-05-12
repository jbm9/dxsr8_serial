#!/usr/bin/env python

import sys

def byteses(l):
    l = l.replace(" ", "")
    a = [ int(l[i:i+2], 16) for i in range(0, len(l)-1, 2) ]
    return a


l0 = sys.stdin.readline() # prime it
h0 = byteses(l0)

for l in sys.stdin:
    h = byteses(l)

    def cof_delta(a,b):
        if a == b:
            return "     "

        return " %3d" % (a-b)


    def cof_sign(a,b):
        if a == b:
            return " "
        if a < b:
            return "d"
        if a > b:
            return "U"

    def cof_mask(a,b):
        if a == b:
            return ". "
        return "X "

    cof = cof_sign
    toprint = "".join([ cof(a,b) for (a,b) in zip(h0,h)])

    print toprint
    l0 = l
    h0 = h
    
