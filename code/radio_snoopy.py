#!/usr/bin/env python

# Emulate the radio side of the connection, to poke/prod at the head
# unit.

import serial

ser = serial.Serial('/dev/tty.usbserial-A4006Dyk', 38400)

from decode_screen import *
fdisp = FrequencyDisplay()
mdisp = ModeDisplay()
rfdisp = RFPowerDisplay()
agcdisp = AGCDisplay()
smeterdisp = SMeterDisplay()
backlightdisp = BacklightDisplay()
miscdisp = MiscDisplay()

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


def print_state(sin):
    if not sin.startswith("LCSA"):
        return
    
    s = [ ord(c) for c in sin ]
    try:
        mode = mdisp.decode(s)

        rxstate = "%s RF:%+2d %s" % (agcdisp.decode(s), rfdisp.decode(s), smeterdisp.decode_string(s))

        line = "" # "%2d>" % backlightdisp.decode(s) # if you care about the backlight intensity.

        if fdisp.is_freq(s):
            line += "[%s] f = %s %s" % (mode, intWithCommas(fdisp.freq(s)), rxstate)
        else:
            line += "[%s] > %s < %s" % (mode, fdisp.decode(s), rxstate)

        line += str(sorted(miscdisp.decode(s)))

        print line
        
    except Exception, e:
        print
        print "Caught exception: " + str(e)
        print
        print "Input %s" % (s)
        print



curline = ""
while True:
    x = ser.read(1)
    curline += x[0]

    if -1 != curline.find("AL~READY"):
        print "GOT AL~READY."
        n = curline.find("AL~READY")
        curline = curline[n+8+1:]


    if 1 <= curline.find("LCSA"):
        print "SEEK to LCSA: %d" % curline.find("LCSA")
        print
        n = curline.find("LCSA")
        ser.write(curline[0:n])
        curline = curline[n:]
    
    while len(curline) >= 34:
        #print "line: " + "".join([ "%02x" % ord(c) for c in curline ])
        print_state(curline[0:34])
        ser.write(curline[0:34])
        curline = curline[34:]       

ser.close()
