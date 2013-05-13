#!/usr/bin/env python

# Takes the output of Salae Logic's Async serial decoder and
# restitches it into ASCII sequences

import sys

if len(sys.argv) != 3:
    print "Usage: logic_to_dump.py head_to_radio.txt radio_to_head.txt"
    sys.exit(1)

def parse_char_ascii(c):
    if c[0] == "'":
        return "\\x%02x" % int(c[1:-1])
    if c == "\\r":
        return "\r"
    if c == "\\n":
        return "\n"
    return c

def parse_char_hex(c):
    x = None

    if c == "' '":
        x = " "
        
    
    if c == "\\r":
        x = "\r"
    if c == "\\n":
        x = "\n"

    nl = ""
    if c == "\\n":
        nl = "\n"

    nl = ""

    if None == x:
        if c[0] == "'":
            try:
                return "%02x" % int(c[1:-1])
            except Exception, e:
                print "Exception: " + str(e)
                print "Input: %s" % c
                raise e
        else:
            x = c[0]

    return "%02x%s" % (ord(x), nl)

def parse_char_literal(c):
    x = None

    if c == "' '":
        return ' '
        
    
    if c == "\\r":
        return "\r"
    if c == "\\n":
        return "\n"

    if None == x:
        if c[0] == "'":
            try:
                return chr(int(c[1:-1]))
            except Exception, e:
                print "Exception: " + str(e)
                print "Input: %s" % c
                raise e
        else:
            return c[0]

parse_char = parse_char_hex

import struct

def packet_h(a):
    if a[0] != 'h' or a[1] != "\x1d":
        return Exception("Invalid header")

    if a[-1] != '\x0a' or a[-2] != '\x00':
        return Exception("Invalid header")


    if len(a) != 34:
        return {}

    v2 = struct.unpack("<i", a[2:6])
    v9 = struct.unpack("<i", a[9:13]) # usually all zeroes
    v13 = struct.unpack("<", a[13:17])


    v6 = struct.unpack("B", a[6])
    v7 = struct.unpack("B", a[7])
    v8 = struct.unpack("B", a[8])

    v17 = "".join([ "%02x" % ord(c) for c in a[17:33] ])

    return {
        "v2": v2,
        "v9": v9,

        "v13": v13,
        "v6": v6,
        "v7": v7,
        "v8": v8,
        "v17": v17
        }

BREAKLEN = 0.01

def stitch_lines(path, prefix):
    retval = []
    f = file(path)

    f.readline() # drop header

    t0 = None
    tp = None
    curline = ""
    for l in f:
        r = l.split(",")
        t = float(r[0])
        c = r[1]

        if t0 == None:
            t0 = t
            tp = t
        cp = parse_char(c)

        if t - tp > BREAKLEN:
            #        if cp[-1] == "\n":
            retval.append( (t0, prefix, curline) )
            t0 = None
            curline = ""

        if cp == "4c" and len(curline) == 34*2:
            curline = curline[0:(34*2)]
            retval.append( (t0, prefix, curline) )
            t0 = t
            tp = t
            curline = ""
            
        curline += cp

        tp = t

    if t0 != None:
        retval.append( (t0, prefix, curline) )        
        

    f.close()

    return retval


h2r = stitch_lines(sys.argv[1], "    -->")
r2h = stitch_lines(sys.argv[2], "<--")

flow = h2r + r2h
flow.sort()

t0 = None
for t,d,s in flow:
    if None == t0:
        t0 = t
    
    print "%0.2f %s %s" % (t-t0,d,    s.strip())
