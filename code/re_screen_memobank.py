#!/usr/bin/env python



def draw_digit(segments):
    digit = """
    memo O   O    1   AAA    HHH
         OO OO    1  F   B  M   I
    bank O O O    2  FGGGB  MNNNI
     a Y O   O    2  E   C  L   J
     b Z O   O    2  EDDDC  LKKKJ


"""

    allsegments = set()
    for c in digit:
        allsegments.add(c)

    w = digit

    for c in allsegments:
        if c == "\n" or c == " " or c == ":"  or c.islower():
            continue
        if c in segments:
            w = w.replace(c, "#")
        else:
            w = w.replace(c, ".")

    return w


data_rit = {
    "blank_a": "4c435341b12ba00006000ba99a781cc00fff10000000a99ae18fe18e1001181e0408",
    "blank_b": "4c435341a12aa000081001000ad81ec81f0000000000a99aa081e18e0001e1040408",
    "bp2":   "4c435341b12bab6378100ba99a781cc00fff10000000a99a618de18c1001181e0408",
    "bp1":   "4c435341b12ba60378100ba99a781cc00fff10000000a99a618fe18c1001181e0408",
    "b198":  "4c435341a12aaf7fb81001000ad81ec81f0000000000a99aa081e18e0001e1040408",
    "b193":  "4c435341a12aaf2fb81001000ad81ec81f0000000000a99aa081e18e0001e1040408",
    "00": "4c435341a12aaf5f501001000ad81ec81f0000000000a99aa001e18e0001e1040408",
    "15": "4c435341a12aad36001001000ad81ec81f0000000000a99a618fe18e0001e1040408",
    "27": "4c435341a12aa70b601001000ad81ec81f0000000000a99aa081e18e0001e1040408",
    "a12": "4c435341a12aab66041001000ad81ec81f0000000000a99a618de18e0001e1040408",
    "memoa00": "4c435341fa512f5f55000ba99a781cc00ff800000000a000618fe18cb081138c0408",
    "memoa00-2": "4c435341ea502f5f55000aa99a781cc00f0000000000e18c718de18ea08b038d0400",
    "memoa00-3": "4c435341b12a2f5f55000aa99a781cc00f0000000000a99a718de18e0001081e0400",
    }

data = data_rit


segments = {
    "blank_a": "Y",
    "blank_b": "Z",
    "bp2": "ZFEABGHINLK",
    "bp1": "ZFEABGIJ",
    "b198": "Z12ABCDFGHIJKLMN",
    "b193": "Z12ABCDFGHIJKN",
    "00": "ABCDEFHIJKLM",
    "memoa00": "OYABCDEFHIJKLM",
    "memoa00-2": "OYABCDEFHIJKLM",
    "memoa00-3": "OYABCDEFHIJKLM",        
    "15": "BCHMNJK",
    "27": "ABGEDHIJ",
    "a12": "YBCHINLK",
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

for c in sorted(all_segments):
    candidate_bits = set( range(len(data.values()[0])/2*8)  )
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
        160: ['2'],
        161: ['1', '3'],
        162: ['C', 'B'],
        163: ['A', 'E', 'D', 'F'],
        166: ['T'],
        167: ['R'],
        168: ['G'],
        169: ['H'],
        170: ['I'],
        171: ['J'],
        172: ['M'],
        173: ['L'],
        174: ['K'],
        175: ['N']
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



for k,l in data.iteritems():
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
