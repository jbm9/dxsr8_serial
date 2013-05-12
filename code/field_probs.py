#!/usr/bin/env python

import sys

def label_line(l):
    fields = l.split(" ")
    label = fields[0]
    retval = {}

    changed = False

    #    print str(fields)

    if label != "idle":
        changed = True

    for i,v in enumerate(fields):
        val = 0
        if v == "X":
            val = 1
        
        retval["f%d-%s" % (i,str(changed))] = [val, 1]

    return retval


def merge_result(d, dp):
    for k,v in dp.iteritems():
        if not k in d:
            d[k] = [0,0]

        d[k][0] += v[0]
        d[k][1] += v[1]

    return d


def summarize(d):
    retval = {}
    
    for k,v in d.iteritems():
        p = float(v[0])/float(v[1])
        retval[k] = p

    return retval

lines = 0
idles = 0

data = {}
for l in sys.stdin:
    dp = label_line(l)
    data = merge_result(data, dp)
    
    lines += 1
    if l.startswith("idle"):
        idles += 1


s = summarize(data)
myks = data.keys()

fields = set()
for k in myks:
    fname,val = k.split("-")
    fields.add(fname)


def pof(d,f,v):
    keyname = f + "-" + str(v)
    if not keyname in d:
        return 0
    r = d[keyname]
    return r[0]/float(r[1])

for f in fields:
    p_true = pof(data, f, True)
    p_false = pof(data, f, False)

    print "%s %.3g %.3g" % (f, p_true, p_false)

    #print str(summarize(data))
