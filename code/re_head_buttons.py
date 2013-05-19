#!/usr/bin/env python

keys = [
    "MF",
    "1",
    "2",
    "3",
    "4",
    "5",
    "6",
    "7",
    "8",
    "9",
    "*",
    "0",
    "ENT",
    "FUNC",
    "RIT",
    "KEY",
    "MODE",
    "V/M",
    "M/KHz",
    "RF",
    "UP",
    "DOWN" ]

keycaps = [
    "SWDS000001000100",
    "SWDS400000000100",
    "SWDS200000000100",
    "SWDS100000000100",
    "SWDS080000000100",
    "SWDS040000000100",
    "SWDS020000000100",
    "SWDS010000000100",
    "SWDS008000000100",
    "SWDS004000000100",
    "SWDS002000000100",
    "SWDS800000000100",
    "SWDS001000000100",
    "SWDS000008000100",
    "SWDS000004000100",
    "SWDS000002000100",
    "SWDS000080000100",
    "SWDS000040000100",
    "SWDS000020000100",
    "SWDS000010000100",
    "SWDS000000800100",
    "SWDS000000400100",
    ]

def bytes_of(s):
    bytes = [ ord(c) for c in s ]
    return bytes

def newlit(s):
    keyblank = "SWDS000000000100"
    blank_bytes = bytes_of(keyblank)

    s_bytes = bytes_of(s)

    diffs = [ x^y for (x,y) in zip(blank_bytes, s_bytes) ]

    bits = []

    for i in range(len(diffs)):
        for j in range(8):
            if 0 != (diffs[i] & (1<<j)):
                bits.append(8*i+j)

    return bits



if len(keys) != len(keycaps):
    print "Mismatch in lens: %d vs %d" % (len(keys), len(keycaps))


for keyname,s in zip(keys,keycaps):
    bits = newlit(s)

    print "    '%s': %s," % (keyname, str(bits[0]))
    
