#!/usr/bin/env python

# Emulate the head side of the connection, to poke/prod at the radio

import serial

ser = serial.Serial('/dev/tty.usbserial-A700eEqF', 38400)


curline = ""
while True:
    x = ser.readline()
    print x
    ser.write(x)

ser.close()
