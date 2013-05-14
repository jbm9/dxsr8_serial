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
    2222>111>000>333   sSS lowLLL   agc sOOO fFFF
"""

    allsegments = set()
    for c in digit:
        allsegments.add(c)

    w = digit

    for c in allsegments:
        if c == "\n" or c == " " or c.islower():
            continue
        if c in segments:
            w = w.replace(c, "#")
        else:
            w = w.replace(c, ".")

    return w


data_rf_amp = {
    "-20":        "4c435341ea50a0000a000ad00fb99b080b0000000000a99aa99b618ea081038d0400",
    "-10":        "4c435341ea51a0000a000ad00eb99b080b0000000000a99aa99b618ea081038d0400",
    "0":          "4c435341ea51a0000a000ad00eb99b080b0000000000a99aa99b618ea081138d0400",
    "+10":        "4c435341ea51a0000a000ad00eb99b080b0000000000a99aa99b618eb081138d0400",
    "-20lo":      "4c435341ea50a0000a000ad00eb99b080b0000000000a99aa99b618ea081038d0400",
    "-20hi-agcs": "4c435341fa50a0000a000ac00eb99a080b0000000000a99aa99b618ea081038c0400",
    "-20hi-agcf": "4c435341ea50a0000a000ac00eb99a080b0000000000a99aa99b618ea081038d0400",
  }

data = data_rf_amp


segments = {
    "-20": "2SLF",
    "-20lo": "2LF",    
    "-10": "21SLF",
    "0": "210LF",
    "+10": "2103LF",
    "-20hi-agcs": "2O",
    "-20hi-agcf": "2F"
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
    segmap = {128: ['2'], 129: ['2'], 2: ['2'], 3: ['2'], 214: ['2'], 6: ['2'], 8: ['2'], 9: ['2'], 258: ['2'], 14: ['2'], 16: ['2'], 17: ['2'], 131: ['2'], 20: ['2'], 22: ['2'], 24: ['2'], 239: ['2'], 30: ['2'], 231: ['2'], 33: ['2'], 191: ['2'], 35: ['2'], 36: ['O'], 37: ['2'], 38: ['2'], 39: ['2'], 40: ['1'], 44: ['2'], 240: ['2'], 46: ['2'], 176: ['2'], 179: ['2'], 53: ['2'], 55: ['2'], 116: ['2'], 187: ['2'], 188: ['2'], 232: ['2'], 241: ['2'], 181: ['2'], 192: ['2'], 65: ['2'], 67: ['2'], 197: ['2'], 199: ['2'], 200: ['2'], 201: ['2'], 183: ['2'], 204: ['2'], 207: ['2'], 208: ['2'], 81: ['2'], 83: ['2'], 251: ['2'], 213: ['2'], 203: ['2'], 185: ['2'], 217: ['2'], 218: ['2'], 219: ['2'], 92: ['L'], 94: ['2'], 95: ['2'], 97: ['2'], 98: ['2'], 99: ['2'], 228: ['3'], 229: ['2'], 195: ['2'], 223: ['2'], 104: ['2'], 107: ['2'], 108: ['2'], 109: ['2'], 111: ['2'], 112: ['L'], 113: ['2'], 115: ['2'], 244: ['0'], 119: ['2'], 248: ['F'], 250: ['2'], 123: ['2'], 255: ['2']}



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
