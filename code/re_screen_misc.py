#!/usr/bin/env python



def draw_digit(segments):
    digit = """
    vfo VVV AA BB  busy:SSSS key:KKKK nb:NN nar:WW star:TTT
    func:FFFF t/r led: LLL tone:EEE tune:UUU split:III
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


data_misc = {
    "vfoabusykey": "4c435341b80aa00006000bd00eb99a080b0000000000e18ce18d618ca181a84a0408",
    "vfoasqlkey":  "4c435341b80aa00006000ad00eb99a080b0000000000e18ce18d618ca181a84a0400",

    "vfobsqlkey":  "4c435341ea51a0000a000ad00eb99b080b0000000000a99aa99b618ea081038d0400",
    "vfobsqlnb":   "4c435341b80aa0000a000ac00eb99a080b0000000000e18ce18d718ca181a84a0400",
    "vfobsqlnar":  "4c435341b80aa0000a000ac00eb99a080b0000000000a99ab99b618ea181a84a0400",
    "vfobnostar":  "4c435341fa50a0000a000ac00eb99a080b0000000000a99aa99b618ea080038c0400",
    "func":    "4c435341fa50a00000100ac00eb99a080b0000000000a99aa99b618ea081038c0400",
    "vfobtone": "4c435341a12ba0000a000ad00eb99b080b0000000000a99ba99b618e0001e1040400",
    "vfobfmnotone": "4c435341a12ba0000a000ad00eb99b080b0000000000a99aa99b618e0001e1040400",
    "vfobtune": "4c435341000130000a000ad00eb99b080b0000000000a99aa99b618e000100000400",
    "vfobsplit": "4c435341a12be0000a000ad00eb99b080b0000000000a99aa99b618e0001e1040400",

    "foo": "4c4353410251260b65018ee80ca81a40050000000000408e408ea18a138df1850a00",
    "foo2": "4c435341a80b2fdf550000c81e781ce81f0000000000618cd187618ca181b84b0a00",
    "foo3": "4c435341a80b2fdf55000aa99a781ce81f0000000000e00cc187618ca181b84b0a00",
    
    }

data = data_misc


segments = {
    "foo": "AT",
    "foo2": "ATW",
    "foo3": "AT",
    "vfoabusykey": "VASKT",
    "vfoasqlkey" : "VAKT",
    "vfobsqlkey":  "VBKT",
    "vfobsqlnb":  "BVNT",
    "vfobsqlnar":  "VBWT",
    "vfobnostar": "VB",
    "func": "F",
    "vfobtone": "VBTE",
    "vfobfmnotone": "VBT",
    "vfobtune": "VBTU",
    "vfobsplit": "VBTI",
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
        65: ['V'],
        66: ['A'],
        67: ['B'],
        196: ['W'],
        267: ['S'],
        76: ['F'],
        80: ['S'],
        212: ['N'],
        54: ['I'],
        184: ['E'],
        52: ['U']
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
