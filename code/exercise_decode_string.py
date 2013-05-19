#!/usr/bin/env python


from decode_screen import *


def intWithCommas(x):
    if type(x) not in [type(0), type(0L)]:
        raise TypeError("Parameter must be an integer.")
    if x < 0:
        return '-' + intWithCommas(-x)
    result = ''
    while x >= 1000:
        x, r = divmod(x, 1000)
        result = ",%03d%s" % (r, result)
    return "%d%s" % (x, result)


screens  = [

    "4c43534112502b660ae814f0a0e81506810000000000408ea18a4004038de1840400",
    "4c435341b12a20800a0000f81eb99ba99b0000000000a99aa99ba99a0001081e0400",
    "4c435341b12a20000a000a100ab99ba99b0000000000a99aa99ba99a0001081e0400",
    "4c435341b12a20800a000a100ab99ba99b0000000000a99aa99ba99a0001081e0400",

    "4c43534112502f2b6ae804a01aa42ba8110000000000a24aa84a4004038de1840400",
    "4c43534112502d760a0a5ee0a00a51a42b000000000004a0e8104004038de1840400",
    "4c43534112502d360a0c161a40400500010000000000a99aa99ae18e038de1840400",
    "4c435341125026360ae80c118e0a5b0a5b0000000000a24a4004010a038de1840400",
    "4c43534112502b660ae814f0a0e81506810000000000408ea18a4004038de1840400",
    "4c435341b12aa0000a000a100ab99b000b0000000000a99aa99ba0000001081e0400",
    "4c435341b12aa0000a000a100ab99b000b0000000000a99aa99ba99a0001081e0400",
    "4c435341b12aa0000a000a000ab99b000b0000000000a99aa001e1840001081e0400",
    "4c435341b12aa0000a000a000ab99b000b0000000000a99aa99be1840001081e0400",
    
    "4c43534112502f2b6ae804a01aa42ba8110000000000a24aa84a4004038de1840400",
    "4c435341b12a20800a0000d00eb99ba99b0000000000a99aa99ba99a0001081e0400",
    ]


fdisp = FrequencyDisplay()
mdisp = ModeDisplay()

for i,s in enumerate(screens):
    try:
        mode = mdisp.decode(s)
        
        if fdisp.is_freq(s):
            print "[%s] f = %d" % (mode, fdisp.freq(s))
        else:
            print "[%s] > %s <" % (mode, fdisp.decode(s))
        
    except Exception, e:
        print "Caught exception: " + str(e)
        print
        print "Input #%d: %s" % (i, s)
        raise e
