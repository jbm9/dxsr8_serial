#!/usr/bin/env python

# Given an array of arrays in which the area of interest is held
# constant while others are varied, return bit ranges that could
# contain the area of interest.

data = {
    "SET": ["4c43534102512f360a0c16e80ce00f40050000000000408e408ea18a138df1840400",
            "4c43534102512f5b6ae80c0a400a41b0110000000000408ea18a4004138df1840400",
            "4c4353410251260b6a018ee80ca81b40050000000000408e408ea18a138df1840400",
            "4c43534102512b6b6aa01a0a5a4005e82d0000000000000004a0c08e138df1840400",
            "4c43534102512f2b6ae804a01aa42ba8110000000000a24aa84a4004138df1840400",
            "4c43534102502f5f5ae804a48a4005000100000000000000618dc186038de1840400",
            "4c43534102502f3f5aa01a0180a01140050000000000408e408ea18a038de1840400",
            "4c43534102502f560a018ea816a811400500000000000000a24aa18a038de1840400",
            "4c43534102502f560a018ea817a811400500000000000000a24aa18a038de1840400",
            "4c43534102502f560a018ea817a81140050000000000408e408ea18a038de1840400",
            "4c435341025026060a0a4005a10a510a410000000000a24aa18a4004038de1840400",
            "4c435341125026060a0a4105a10a510a41ffff700000a24aa18a4004038de1840408",
            "4c435341125026060a0a4105a00a500a410000000000a24aa18a4004038de1840408",
            ],

    "AM": [
        "4c435341b12aa0000a681de81e100ac00f0000000000a99a618fe00c0001081e0408",
        "4c435341b12aa0000a681de81e100ac81f0000000000a99a618fe1840001081e0408",
        "4c435341b12ba0000a681de81e100ac81fff00000000a99ae00de00c1001181e0408",
        "4c435341b12ba0000a681df81e100ac81fff70000000a99ae00de00c1001181e0408",
        "4c435341b12ba0000a681cf81e100ac81f0000000000a99ae00de00c1001181e0400",
        "4c435341b12ba0000a0001100af81e481fffff100000a99aa001a0801001181e0408"
        "4c435341b12ba0000a0001100af81e481ffffe000000a99ab001a0801001181e0408",
        "4c435341b12b20000a0001100af81e481fffff100000a99aa001a0801001181e0408",
        "4c435341a12b20000a0001100af81e481fffff100000a99aa001a0801001181f0408",
        "4c435341a12b20000a0001100af81e481fffff108cdfa99aa001a0801001181f0408",
        "4c435341a12b20800a0001100af81e481fffff10ccdfa99aa001a0801001181f0408",
        ],
    "FM": [
        "4c435341a12b20800a0001100af81e481fffff10ccdfa99aa001a0801001f1040408",
        "4c435341a12b20800a681c100ab99a080b000000ccdfa99a618d618e1001f1040400",
        "4c435341a12a20800a681c100ab99a080b0000000000a99a618d618e0001e1040400",
        "4c435341a12a20800a681c100bb99b080b0000000000a99a618d618e0001e1040400",
        "4c435341a12a20800a681c000bb99b080b0000000000a99a618d618e0001e1040400",
        ]
    }

data2 = [ # anti-contrast: find what _doesn't_ change with mode
          "4c435341a12a20800a681c100bb99b080b0000000000a99a618d618e0001e1040400", #FM, no agc
          "4c435341080a20800a681c100bb99b080b0000000000a99a618d618ea181a84b0400", # CWL, agcf
          "4c435341a80a20800a681c100bb99b080b0000000000a99a618d618ea181a84b0400", # CWU, agcf
          "4c435341fa5020800a681c100bb99b080b0000000000a99a618d618ea081038c0400", # LSB, agcs
          "4c435341ea50a0000a681c100bb99b080b0000000000a99a618d618ea081038d0400", # LSB, agcf
          "4c435341ea50a0000a681c100bb99b080b0000000000a99a618d618ea08b038d0400", # USB, agcf
          "4c435341a12aa0000a681c100bb99b080b0000000000a99a618d618e0001081f0400", # AM, agcs
    ]


def contrast_set(byteses):
    # Winnow down:
    # Create a blank "mask" of mismatched bits
    # xor 1 vs 2, and OR the result against the mask
    # xor 2 vs 3, and OR that against the mask
    # xor 3 vs 4, and OR and so on and so forth

    mask = [ 0 for b in byteses[0] ]
    for i in range(len(byteses)-1):
        xor_res = [ x_i ^ y_i for (x_i, y_i) in zip(byteses[i], byteses[i+1]) ]
        mask = [ m_i | x_i for (m_i, x_i) in zip(mask, xor_res) ]


    return mask
    


overall_mask = None
for k,v in data.iteritems():
    byteses = [  [ int(s[i:i+2], 16) for i in range(0, len(s)-1, 2) ] for s in v ]
    mask = contrast_set(byteses)


    if None == overall_mask:
        overall_mask = mask
    else:
        overall_mask = [ o|m for (o,m) in zip(overall_mask, mask) ]
    
    print k
    print str(mask)


print str(overall_mask)
print

for s in data2:
    bytes = [ int(s[i:i+2], 16) for i in range(0, len(s)-1, 2) ]
    bytes = [ b & ~m for (m,b) in zip(overall_mask, bytes) ]
    bytes = bytes[29:]
    b0 = "".join(['{:08b}'.format(i)[::-1] for i in bytes ])
    print b0



byteses2 = [  [ int(s[i:i+2], 16) for i in range(0, len(s)-1, 2) ] for s in data2 ]
same_bits = contrast_set(byteses2)
print str(same_bits)
