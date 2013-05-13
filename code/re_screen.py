#!/usr/bin/env python

# Pulling apart the bits for the first digit of the frequency display,
# the others look to follow a very similar pattern.

# Sixteen segment displays
#     YY <-- arrow
#  AAAAAAAAA
# HK   M   NC
# H K  M  N C
# H  K M N  C
#   UUU PPP 
# G  T S R  D
# G T  S  R D
# GT   S   RD
#  EEEEEEEEE    XX <-- decimal


def draw_digit(segments):
    digit = """    YY
  AAAAAAAAA
 HK   M   NC
 H K  M  N C
 H  K M N  C
   UUU PPP
 G  T S R  D
 G T  S  R D
 GT   S   RD
  EEEEEEEEE    XX"""

    allsegments = set()
    for c in digit:
        allsegments.add(c)

    w = digit

    for c in allsegments:
        if c == "\n" or c == " ":
            continue
        if c in segments:
            w = w.replace(c, "#")
        else:
            w = w.replace(c, ".")

    return w


# Segment: A, candidates: set([91])
# Segment: C, candidates: set([99])
# Segment: E, candidates: set([100])
# Segment: D, candidates: set([97])
# Segment: G, candidates: set([93])
# Segment: H, candidates: set([95])
# Segment: K, candidates: set([90])
# Segment: M, candidates: set([69, 89, 102])
# Segment: N, candidates: set([103])
# Segment: P, candidates: set([98])
# Segment: S, candidates: set([69, 89, 102])
# Segment: R, candidates: set([101, 121])
# Segment: U, candidates: set([94])
# Segment: T, candidates: set([88])
# Segment: Y, candidates: set([])
# Segment: X, candidates: set([])

#  ---91---
# |    |   3|
# 9 9  8  0 9
# 5  0 9 1  9
#  -94- -98-
# 9  8 1 1  9
# 3 8  0  0 7
# |    2   1 |
#  EEEEEEEE   



#  0 T   # 88
#  1 MS
#  2 K
#  3 A
#  4 
#  5 G
#  6 U
#  7 H
#
#  0    # 96
#  1 D
#  2 P
#  3 C
#  4 E  #100
#  5 R
#  6 MS
#  7 N

#     "0":   "4c435341 b12a20800 a000a b99ab99ba99b0000000000a99aa99ba99a0001081e0400",

data = { # This is for the fifth number from the right, the MHz one's place
    "0":   "4c435341b12a20800a000ab99ab99ba99b0000000000a99aa99ba99a0001081e0400",
    "2":   "4c435341b12a20800a0000781cb99ba99b0000000000a99aa99ba99a0001081e0400",
    "3":   "4c435341b12a20800a0000581eb99ba99b0000000000a99aa99ba99a0001081e0400",
    "4":   "4c435341b12a20800a0000d00eb99ba99b0000000000a99aa99ba99a0001081e0400",
    "5":   "4c435341b12a20800a0000d816b99ba99b0000000000a99aa99ba99a0001081e0400",
    "6":   "4c435341b12a20800a0000f816b99ba99b0000000000a99aa99ba99a0001081e0400",
    "7":   "4c435341b12a20800a0000180ab99ba99b0000000000a99aa99ba99a0001081e0400",

    "8":   "4c435341b12a20800a0000f81eb99ba99b0000000000a99aa99ba99a0001081e0400",
    "9":   "4c435341b12a20800a0000d81eb99ba99b0000000000a99aa99ba99a0001081e0400",

    "ED":  "4c435341b12a20000a001010100011001100000000000100010001000001081e0400",
    "E":   "4c435341b12a20000a001010101011001100000000000100010101000001081e0400",

    "1":   "4c435341b12a20800a0000100ab99ba99b0000000000a99aa99ba99a0001081e0400",
    
    "1A":  "4c435341b12a20800a000a100ab99ba99b0000000000a99aa99ba99a0001081e0400",
    "1NA": "4c435341b12aa0000a000a100ab99ba99b0000000000a99aa99ba99a0001081e0400",

    "D": "4c43534112502b6b6aa01a1a5a4005e82d0000000000000004a0c08e038de1840400",
    "T": "4c43534112502f5b6ae80c1a400a41b0110000000000408ea18a4004038de1840400",
    "M": "4c43534112502f5f5a018eb48a4005000100000000000000a99ba000038de1840400",
    "R": "4c4353411250260f5ae80cf82ca81b0a410000000000408ea18a4004038de1840400",
    "S": "4c43534112502d3f5a0c161c16a81140050000000000a99a618c0000038de1840400",
    "K": "4c43534112502b660ae814f0a0e81506810000000000408ea18a4004038de1840400",
    }


segments = {
    "0": "ACDEGHTNXY",
    "1": "CDXY",
    "2": "ACEGUPXY",
    "3": "ACDEUPXY",
    "4": "HCUPDXY",
    "5": "AHUPDEXY",
    "6": "AHGEDUPXY",
    "7": "ACDXY",
    "8": "ACDEGHUPXY",
    "9": "HACDEUPXY",
    "ED": "EXY",
    "E": "EY",
    "1A": "CDXY",
    "1NA": "CDX",
    "D": "ACDEMS",
    "T": "AMS",
    "M": "HGKNCD",
    "R": "GHACUPR",
    "S": "AKPDE",
    "K": "HGUNR",
}




all_segments = set()
for v in segments.values():
    for c in v:
        all_segments.add(c)



def splitbits(s):
    bytes = [ int(s[i:i+2], 16) for i in range(0, len(s)-1, 2) ]
    b0 = "".join(['{:08b}'.format(i)[::-1] for i in bytes ])

    bits_lit = set()
    bits_out = set()

    for i,b in enumerate(b0):
        if b == "1":
            bits_lit.add(i)
        else:
            bits_out.add(i)

    return (bits_lit, bits_out)

data_bits = {}
for k,v in data.iteritems():
    data_bits[k] = splitbits(v)


for c in all_segments:
    candidate_bits = set( range(len(data["0"])/2*8)  )
    #candidate_bits = set( range(32,200)  )    
    
    for digit, bitsets in data_bits.iteritems():
        seglit = (-1 != segments[digit].find(c)) # is this segment lit?

        if seglit:
            candidate_bits -= bitsets[1]
        else:
            candidate_bits -= bitsets[0]
        

    print "Segment: %s, candidates: %s" % (c, str(candidate_bits))


for k,v in segments.iteritems():
    print "===== %s =====" % k
    print draw_digit(v)
    print
