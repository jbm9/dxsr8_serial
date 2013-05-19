#!/usr/bin/env python

# Emulate the head side of the connection, to poke/prod at the radio

import serial
import os
import os.path
import time

from decode_head import *

ser = serial.Serial('/dev/tty.usbserial-A700eEqF', 38400, timeout=1)


curline = ""
while True:
    x = ser.readline()
    print x

    if x.startswith("SWDS"):
        print "KEYS DOWN: " + str(decode_SWDS(x))
    
    ser.write(x)

    if os.path.exists("/tmp/buttons"):
        f = file("/tmp/buttons")
        for l in f:
            l = l.strip()
            try:
                bdown = encode_SWDS(l)
                ser.write(bdown)
                time.sleep(0.01)
                bup = encode_SWDS(None)
                ser.write(bup)
                time.sleep(0.01)
                
            except Exception, e:
                print "Got exception: %s" + str(e)
        f.close()
        os.remove("/tmp/buttons")

ser.close()
