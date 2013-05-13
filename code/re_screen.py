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


#  0 E  # 208
#  1 K?
#  2 M?
#  3 N
#  4 R
#  5 D
#  6 P
#  7 C
#
#  0    # 216
#  1 G
#  2 U
#  3 H
#  4 T
#  5
#  6
#  7 A  # 223

#     "0":   "4c435341 b12a20800 a000a b99ab99ba99b0000000000a99aa99ba99a0001081e0400",

data_2 = { # This is for the fifth number from the right, the MHz one's place
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

data_kHz = { # third digit from the right, kHz, one's place, looks like a different layout, ugh.
    "0":   "4c435341b12aa0000a000a100ab99b000b0000000000a99aa99ba99a0001081e0400",
    "2":   "4c435341b12aa0000a000a100ab99b000b0000000000a99aa99bc1860001081e0400",
    "3":   "4c435341b12aa0000a000a100ab99b000b0000000000a99aa99be1840001081e0400",
    "4":   "4c435341b12aa0000a000a100ab99b000b0000000000a99aa99be00c0001081e0400",
    "5":   "4c435341b12aa0000a000a100ab99b000b0000000000a99aa99b618c0001081e0400",
    "6":   "4c435341b12aa0000a000a100ab99b000b0000000000a99aa99b618e0001081e0400",
    "7":   "4c435341b12aa0000a000a100ab99b000b0000000000a99aa99ba0800001081e0400",

    "8":   "4c435341b12aa0000a000a100ab99b000b0000000000a99aa99be18e0001081e0400",
    "9":   "4c435341b12aa0000a000a100ab99b000b0000000000a99aa99be18c0001081e0400",

    "ED":  "4c435341b12a20000a001010101011001100000000000100010101000001081e0400",
    "E":   "4c435341b12a20000a001010100011001100000000000100010001000001081e0400",

    "1":   "4c435341b12aa0000a000a100ab99b000b0000000000a99aa99ba0000001081e0400",
    }


data = { # second digit from the right, hundreds place
    "O": "4c43534112502b660ae814f0a0e81506810000000000408ea18a4004038de1840400",
    "0":   "4c43534112502f260aa12af80ca48b400500000000000000a99ac186038de1840400",
    "-": "4c435341125026360ae80c118e0a5b0a5b0000000000a24a4004010a038de1840400",
    "A": "4c43534112502d760a0a5ef0a00a51a42b000000000004a0e8104004038de1840400",
    
    "2":   "4c435341b12aa0000a000a000ab99b000b0000000000a99ac187a0000001081e0400",
    "3":   "4c435341b12aa0000a000a000ab99b000b0000000000a99ae185a0000001081e0400",
    "4":   "4c435341b12aa0000a000a000ab99b000b0000000000a99ae00da0000001081e0400",
    "5":   "4c435341b12aa0000a000a000ab99b000b0000000000a99a618da0000001081e0400",
    "6":   "4c435341b12aa0000a000a000ab99b000b0000000000a99a618fa0000001081e0400",
    "7":   "4c435341b12aa0000a000a000ab99b000b0000000000a99aa081a0000001081e0400",

    "8":   "4c435341b12aa0000a000a000ab99b000b0000000000a99ae18fa0000001081e0400",
    "9":   "4c435341b12aa0000a000a000ab99b000b0000000000a99ae18da0000001081e0400",

    "ED":  "4c435341b12a20000a001000101011001100000000000100010101000001081e0400",
    "E":   "4c435341b12a20000a001000100011001100000000000100010001000001081e0400",

    "1": "4c435341b12aa0000a000a000ab99b000b0000000000a99aa001a0000001081e0400",
    "F": "4c43534112502f360a0c16f80ce00f40050000000000408e408ea18a038de1840400",
    "T": "4c43534112502b6b6aa01a1a5a4005e82d0000000000000004a0c08e038de1840400",
    "M": "4c43534112502f2b6ae804b01aa42ba8110000000000a24aa84a4004038de1840400",
    "R": "4c4353411250263b6a0c1650040a51e805000000000004a0c28e4004038de1840400",
    "S": "4c43534112502f2f5a0c16b810400500010000000000000061c0a000038de1840400",
    "N": "4c4353411250263f5a0a5e50040c17a81100000000000000a24ae810038de1840400",
    " ": "4c43534112502d7f5a00001c16e0a10a51000000000000000000c08e038de1840400",
    }


segments = {
    "0": "ACDEGHTNXY",
    "O": "ACDEGH",
    "-": "UP",
    " ": "",
    "A": "TNPCD",
    "1": "CDXY",
    "2": "ACEGUPXY",
    "3": "ACDEUPXY",
    "4": "HCUPDXY",
    "5": "AHUPDE",
    "6": "AHGEDUPXY",
    "7": "ACDXY",
    "8": "ACDEGHUPXY",
    "9": "HACDEUPXY",
    "ED": "EXY",
    "E": "EY",
    "F": "AHGUP",
    "1A": "CDXY",
    "1NA": "CDX",
    "D": "ACDEMS",
    "T": "AMS",
    "M": "HGKNCD",
    "N": "HGKRCD",
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


def print_line(s):
    bytes = [ int(s[i:i+2], 16) for i in range(0, len(s)-1, 2) ]    
    for offset in range(0,4):
        segmap = "TSKAXGUHxDPCERMN"        
        segs =  unpack_segments(bytes, 8*(9+2*offset), segmap)
        print segs
        print draw_digit(segs)

    print
    print "SHIFT"
    print
    
    for offset in range(0,1):
        segmap = "EKMNRDPCxGUHTxxA"         
        segs =  unpack_segments(bytes, 8*(26+2*offset), segmap)
        print "kHz: " + segs
        print draw_digit(segs)


    for offset in range(0,1):
        segmap = "ERMNRDPCxGUHTSKA"         
        segs =  unpack_segments(bytes, 8*(24+2*offset), segmap)
        print "100: " + segs
        print draw_digit(segs)
        

    for offset in range(0,1):
        segmap = "ERMNRDPCxGUHTSKA"         
        segs =  unpack_segments(bytes, 8*(22+2*offset), segmap)
        print "100: " + segs
        print draw_digit(segs)


def unpack_segments(s, offset, segmap):
    byte_offset = offset/8
    
    bytes = s[byte_offset:(byte_offset+2)]
    mask = "".join(['{:08b}'.format(i)[::-1] for i in bytes ])
    print mask
    print segmap

    retval = "".join([ s if b == "1" else "" for (s,b) in zip(segmap, mask)])

    return retval
    

#print_line("4c43534112502b660ae814f0a0e81506810000000000408ea18a4004038de1840400")
#print_line("4c435341b12a20800a0000f81eb99ba99b0000000000a99aa99ba99a0001081e0400")
#print_line("4c435341 b12a2000 0a000a100ab99ba99b0000000000a99aa99ba99a0001081e0400")
#print_line("4c435341 b12a2080 0a000a100ab99ba99b0000000000a99aa99ba99a0001081e0400")

print_line("4c43534112502f2b6ae804a01aa42ba8110000000000a24aa84a4004038de1840400")
print_line("4c43534112502d760a0a5ee0a00a51a42b000000000004a0e8104004038de1840400")
print_line("4c43534112502d360a0c161a40400500010000000000a99aa99ae18e038de1840400")
print_line("4c435341125026360ae80c118e0a5b0a5b0000000000a24a4004010a038de1840400")
print_line("4c43534112502b660ae814f0a0e81506810000000000408ea18a4004038de1840400")
print_line("4c435341b12aa0000a000a100ab99b000b0000000000a99aa99ba0000001081e0400")
#print_line("4c435341b12aa0000a000a100ab99b000b0000000000a99aa99ba99a0001081e0400")
#print_line("4c435341b12aa0000a000a000ab99b000b0000000000a99aa00 1e1840001081e0400")
#print_line("4c435341b12aa0000a000a000ab99b000b0000000000a99aa99 be1840001081e0400")
#for k,v in segments.iteritems():
#    print "===== %s =====" % k
#    print draw_digit(v)
#    print
