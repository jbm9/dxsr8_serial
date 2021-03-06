#!/usr/bin/env python



def draw_digit(segments):
    digit = """
    txit: TTT    1  FAAB   GGGG
                222 E  B   M  H
                 3  E  B   MLLH
    rxit: RRR       E  C   K  I
                    EDDC N JJJJ
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
    "blank": "4c435341a12aa000060000000ad81ec81f0000000000a99ac187e18e0001e1040400",
    "rit00": "4c435341a12aa000060000000ad81ec81f0000008cdfa99ac187e18e0001e1040400",
    "txrit-05": "4c435341a12aa000060000000ad81ec81f000000cdbda99ae18de18e0001e1040400",
    "rit+07": "4c435341a12aa000060000000ad81ec81f0000008f87a99ac187e18e0001e1040400",
    "rit-07": "4c435341a12aa000060000000ad81ec81f0000008d87a99a618fe18e0001e1040400",
    "rit-11": "4c435341a12aa000060000000ad81ec81f0000008586a99a618fe18e0001e1040400",
    "rit-12": "4c435341a12aa000060000000ad81ec81f00000085eba99a618fe18e0001e1040400",
    "rit-08": "4c435341a12aa000060000000ad81ec81f0000008dffa99a618fe18e0001e1040400",
    "rit-09": "4c435341a12aa000060000000ad81ec81f0000008dbfa99a618fe18e0001e1040400",
    "txrit-11": "4c435341a12aa000060000000ad81ec81f000000c586a99ae18de18e0001e1040400",
    }

data = data_rit


segments = {
    "blank": "",
    "rit00": "RABCDEFGHIJKMN",
    "rit+07": "R123ABCDEFGHIN",
    "txrit-05": "TR2ABCDEFGMLIJN",
    "rit-07": "R2ABCDEFGHIN",
    "rit-08": "R2ABCDEFGHIMLKJN",
    "rit-09": "R2ABCDEFGHIMLJN",        
    "rit-11": "R2BCNHI",
    "rit-12": "R2BCNGHLKJ",
    "txrit-11": "TR2BCNHI",
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
