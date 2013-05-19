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
    digit = """
 aaaaaa      iiiiii     uuuuuuu
f g    b    n o   pj   zA  B  Cv
f  g   b    n  o p j   z A B C v
e  hhhhc    mtttqqqj   y   EDDDw
e      c    m s r  k   y   E   w
e      c    ms   r k   y   E   w
 dddddd      llllll     xxxxxx
"""

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


mode_lcd = """
 aaaaaa      iiiiii     uuuuuuu
f g    b    n o   pj   zA  B  Cv
f  g   b    n  o p j   z A B C v
e  hhhhc    mtttqqqj   y   EDDDw
e      c    m s r  k   y   E   w
e      c    ms   r k   y   E   w
 dddddd      llllll     xxxxxx
"""


data_mode = {
    #    "CWL": "4c435341080aa0000a000a000ab99b000b0000000000a99ae18da000a181a84b0400",
    #     "CWU": "4c435341a80aa0000a000a000ab99b000b0000000000a99ae18da000a181a84b0400",
    #     "LSB": "4c435341fa50a0000a000a000ab99b000b0000000000a99ae18da000a081038c0400",
    #     "USB": "4c435341fa50a0000a000a000ab99b000b0000000000a99ae18da000a08b038c0400",
    #     "AM":  "4c435341b12aa0000a000a000ab99b000b0000000000a99ae18da0000001081e0400",
                        #     "FM":  "4c435341a12aa0000a000a000ab99b000b0000000000a99ae18da0000001e1040400",
                        #     "SET": "4c43534102502f2b6ae804a01aa42ba8110000000000a24aa84a4004038de1840400"
                        # 
    "FM":  "4c435341a12a20800a681c100bb99b080b0000000000a99a618d618e0001e1040400", #FM, no agc
    "CWL": "4c435341080a20800a681c100bb99b080b0000000000a99a618d618ea181a84b0400", # CWL, agcf
    "CWU": "4c435341a80a20800a681c100bb99b080b0000000000a99a618d618ea181a84b0400", # CWU, agcf
    "LSB": "4c435341fa5020800a681c100bb99b080b0000000000a99a618d618ea081038c0400", # LSB, agcs
    "lsb": "4c435341ea50a0000a681c100bb99b080b0000000000a99a618d618ea081038d0400", # LSB, agcf
    "USB": "4c435341ea50a0000a681c100bb99b080b0000000000a99a618d618ea08b038d0400", # USB, agcf
    "AM":  "4c435341a12aa0000a681c100bb99b080b0000000000a99a618d618e0001081f0400", # AM, agcs
    "SET": "4c435341025026060a0a4005a10a510a410000000000a24aa18a4004038de1840400",



    "SET2": "4c43534102512f360a0c16e80ce00f40050000000000408e408ea18a138df1840400",
    "SET3":        "4c43534102512f5b6ae80c0a400a41b0110000000000408ea18a4004138df1840400",
    "SET4":         "4c4353410251260b6a018ee80ca81b40050000000000408e408ea18a138df1840400",
    "SET5": "4c43534102512b6b6aa01a0a5a4005e82d0000000000000004a0c08e138df1840400",
    "SET6": "4c43534102512f2b6ae804a01aa42ba8110000000000a24aa84a4004138df1840400",
    "SET7": "4c43534102502f5f5ae804a48a4005000100000000000000618dc186038de1840400",

    "AM2":        "4c435341b12aa0000a681de81e100ac00f0000000000a99a618fe00c0001081e0408",
    "AM3":        "4c435341b12aa0000a681de81e100ac81f0000000000a99a618fe1840001081e0408",
    "AM4":        "4c435341b12ba0000a681de81e100ac81fff00000000a99ae00de00c1001181e0408",
    "AM5":        "4c435341b12ba0000a681df81e100ac81fff70000000a99ae00de00c1001181e0408",
    
    }

data = data_mode


segments = {
    "SET": "aghcdinmltquBE",
    "SET2": "aghcdinmltquBE",
    "SET3": "aghcdinmltquBE",
    "SET4": "aghcdinmltquBE",
    "SET5": "aghcdinmltquBE",
    "SET6": "aghcdinmltquBE",
    "SET7": "aghcdinmltquBE",        
    "FM": "inmtqyzACvw",
    "AM": "spqjkyzACvw",
    "AM2": "spqjkyzACvw",
    "AM3": "spqjkyzACvw",
    "AM4": "spqjkyzACvw",
    "AM5": "spqjkyzACvw",        
    "USB": "fedcbioqkluBEDxvw",
    "LSB": "fedioqkluBEDxvw",
    "lsb": "fedioqkluBEDxvw",
    "CWL": "afednmsrkjzyx",
    "CWU": "afednmsrkjzyxvw",
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


decode = {} # bitno => array of segments

for c in all_segments:
    candidate_bits = set( range(len(data["USB"])/2*8)  )
    #candidate_bits = set( range(32,200)  )    
    
    for digit, bitsets in data_bits.iteritems():
        seglit = (-1 != segments[digit].find(c)) # is this segment lit?

        if seglit:
            candidate_bits -= bitsets[1]
        else:
            candidate_bits -= bitsets[0]
        

    print "Segment: %s, candidates: %s" % (c, str(candidate_bits))
    for b in candidate_bits:
        if not b in decode:
            decode[b] = []
        decode[b].append(c)


print str(decode)


for k,segs in segments.iteritems():
    print k + ": " + segs
    print draw_digit(segs)


def print_line(s):
    segmap = {

    # 49: ['g', 'h'],  #bogons based on patterns
    # 57: ['g', 'h'],  # bogons based on patterns
        225: ['g'],
        234: ['h'],
        

        
        32: ['A', 'C'],
        45: ['A', 'C'],

        37: ['w', 'v'],
        39: ['w', 'v'],

        41: ['y', 'z'],
        43: ['y', 'z'],

        38: ['D'],
        241: ['o'],

        249: ['j'],
        243: ['s'],

        245: ['m', 'n'],
        247: ['m', 'n'],
        
        224: ['a'],
        233: ['b'],

        235: ['c'],
        239: ['d'],
        240: ['i'],
        246: ['t'],
        250: ['q'],
        251: ['k'],
        252: ['p'],
        254: ['r'],

        # These three are confirmed
        35: ['x'],        
        229: ['e', 'f'],
        231: ['e', 'f'],


        # These four are confirmed, oddly enough
        33: ['B', 'E', 'u'],
        44: ['B', 'E', 'u'],        
        46: ['B', 'E', 'u'],
        255: ['l'], # based on patterns
        }        



    bytes = [ int(s[i:i+2], 16) for i in range(0, len(s)-1, 2) ]
    segs = ""
    for b, lights in segmap.iteritems():
        byte_offset = b/8
        bit_offset = (b%8)
        candidate = bytes[byte_offset]
        if candidate & 1<<bit_offset:
            for l in lights:
                if l not in segs:
                    segs += l

    print segs
    print draw_digit(segs)



for k,l in data_mode.iteritems():
    print k
    print_line(l)



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
print_line("4c43534102502f3f55a01b0180a010404c43534102502f3f55a01b0180a010400500")
