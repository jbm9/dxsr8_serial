#!/usr/bin/env python

"""This is just a quick one-off script to read in the alphabet for the
display, along with a quick confirmation check that I haven't
bollocksed the input.

"""

import sys
import tempfile
import os

from decode_screen import LCD16


(fd, path) = tempfile.mkstemp()
print "Writing output to %s" % path
print
f = os.fdopen(fd, "w")

for c in " _ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789":
    conf = "N"
    segs = ""

    while conf != "":
        print
        print "Segments for '" + c + "':"
        segs = sys.stdin.readline()
        d = LCD16(segs)

        print d.draw()
        print "Input empty line to confirm, anything else to redo input:"
        conf = sys.stdin.readline()
        conf = conf.strip()

    segs = segs.strip()
    f.write('"%s": "%s",\n' % (c, segs))

f.close()
    
