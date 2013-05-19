#!/usr/bin/env python


def _get_bit(bytes, offset):
    i = int(offset)/8
    j = offset % 8

    if (bytes[i] & (1<<j)) != 0:
        return 1
    return 0

def _set_bit(bytes, offset):
    i = int(offset)/8
    j = offset % 8

    bytes[i] |= (1<<j);
    return bytes


def decode_SWDV(b):
    rit = b[4]
    ifshift = b[5]
    squelch = b[6]
    vol = b[7]


def decode_SWDR(b):
    x = b[4]
    if x == 0x80:
        return 0
    if x == 0x81:
        return 1 #clockwise
    if x == 0x7f:
        return -1 # anticlockwise

    return 0


KEYS = {
    'MF': 72,
    '1': 34,
    '2': 33,
    '3': 32,
    '4': 43,
    '5': 42,
    '6': 41,
    '7': 40,
    '8': 51,
    '9': 50,
    '*': 49,
    '0': 35,
    'ENT': 48,
    'FUNC': 75,
    'RIT': 74,
    'KEY': 73,
    'MODE': 67,
    'V/M': 66,
    'M/KHz': 65,
    'RF': 64,
    'UP': 83,
    'DOWN': 82,

    }


def decode_SWDS(b):
    retval = []

    bytes = [ ord(c) for c in b ]

    for key,bit in KEYS.iteritems():
        if 1 == _get_bit(bytes, bit):
            retval.append(key)

    return retval

def encode_SWDS(button):
    keyblank = "SWDS000000000100\r\n"

    if button == None:
        return keyblank
    
    blank_bytes = [ ord(c) for c in keyblank ]

    
    o = KEYS[button]
    bytes = _set_bit(blank_bytes, o)

    return "".join([chr(c) for c in bytes])
