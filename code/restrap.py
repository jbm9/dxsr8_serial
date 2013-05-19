#!/usr/bin/env python

# Emulate the radio side of the connection, to poke/prod at the head
# unit.

import serial

ser = serial.Serial('/dev/tty.usbserial-A4006Dyk', 38400, timeout=1)


curline = ""

ser.write("AL~READY")

disp = "4c435341a12aa000060000100ad81ec81f000000cdbda99aa99be18c0001e1040400"
disp = "".join([ chr(int(disp[i:i+2], 16)) for i in range(0, len(disp)-1, 2) ])

while True:
    x = ser.read(1)

    if len(x) > 0:
        curline += x[0]

        if -1 != curline.find("AL~READY"):
            print "GOT AL~READY."
            n = curline.find("AL~READY")
            curline = curline[n+8+1:]


        if 1 <= curline.find("LCSA"):
            print "SEEK to LCSA: %d" % curline.find("LCSA")
            n = curline.find("LCSA")
            ser.write(curline[0:n])
            curline = curline[n:]

        while len(curline) >= 34:
            print "line: " + "".join([ "%02x" % ord(c) for c in curline ])
            ser.write(curline[0:34])
            disp = curline[0:34]
            curline = curline[34:]

    ser.write(disp)

ser.close()
