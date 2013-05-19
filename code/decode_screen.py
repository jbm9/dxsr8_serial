#!/usr/bin/env python


class LCD16:
    """A 16 segment LCD display


    Layout is per Lite-On's naming convention:


     AAA BBB
    HK  M  NC
    H K M N C
      UU PP
    G T S R D
    GT  S  RD
     FFF EEE


    The alphabet is shown on page 54 of the DX-SR8 manual.
    
    """


    ALPHABET = {
        " ": "",
        "_": "FE",
        "-": "PU",
        "A": "TNPCD",
        "B": "ABCDMSFEP",
        "C": "ABHGFE",
        "D": "ABCDFEMS",
        "E": "ABHGFEUP",
        "F": "ABGHUP",
        "G": "BAHGFEDP",
        "H": "HGCDUP",
        "I": "ABMSFE",
        "J": "GFECD",
        "K": "HGUNR",
        "L": "HGFE",
        "M": "HGCDKN",
        "N": "HGKRCD",
        "O": "ABCDFEGH",
        "P": "ABCPUHG",
        "Q": "ABCDEFGHR",
        "R": "ABCUPGHR",
        "S": "ABKPDEF",
        "T": "ABMS",
        "U": "HGEFCD",
        "V": "HGTN",
        "W": "HGCDTR",
        "X": "KNRT",
        "Y": "KNS",
        "Z": "ABNTFE",
        "0": "ABCDEFGHNT",
        "1": "CD",
        "2": "ABCPUGFE",
        "3": "ABUPFECD",
        "4": "HUPCD",
        "5": "ABHUPDEF",
        "6": "ABHGFEDUP",
        "7": "ABCD",
        "8": "ABCDEFGHUP",
        "9": "ABHCUPDFE",
        }

    def fixup(self, l):
        """Fudges segments the same way the radio seems to.

        A and B are hardwired together, as are E and F"""


        fudges = [ ('A', 'B'),
                   ('E', 'F') ]

        for x,y in fudges:
            if x in l and y not in l:
                l += y
            if y in l and x not in l:
                l += x

        return l

    def __init__(self, lit=""):
        self.lit = self.fixup(lit)

        # create the alphabet lookup table. Yes, I want to do this
        # every runtime, since I have no proper tests, this makes me
        # feel much better about the delusion that everything is
        # working.
        
        self.lookup = {} # mask => character
        for c,m in self.ALPHABET.iteritems():
            m_sorted = "".join(sorted(list(m)))
            if m_sorted in self.lookup:
                raise Exception("Non-unique mask to character mapping: %s goes to both %s and %s" % (m, self.lookup[m_sorted], c))

            self.lookup[m_sorted] = c
            

    def draw(self):
        digit="""
     AAA BBB
    HK  M  NC
    H K M N C
      UU PP
    G T S R D
    GT  S  RD
     FFF EEE"""

        allsegments = set()
        for c in digit:
            allsegments.add(c)

        w = digit

        for c in allsegments:
            if c == "\n" or c == " " or c == ":"  or c.islower():
                continue
            if c in self.lit:
                w = w.replace(c, "#")
            else:
                w = w.replace(c, ".")

        return w
        
    def decode(self):
        lit_key = "".join(sorted([ c if c.isupper() else "" for c in self.lit]))

        if lit_key not in self.lookup:
            print ">>> MISSING: " + repr(lit_key)
            return None

        return self.lookup[lit_key]

    


class LCD16_a(LCD16):

    # This is the segment associated with each bit in the input, in
    # ascending bit order.
    
    SEGMENT_MAP = "TSKAyGUHxDPCERMN"
    
    @classmethod
    def from_bytes(cls, bytes, offset):
        i = int(offset)/8
        j = offset % 8

        lit = ""
        for k in range(16):
            di = (j + k) / 8
            jp = (j + k) % 8

            if (bytes[i+di] & (1<<(jp))) != 0:
                lit += cls.SEGMENT_MAP[k]

        return cls(lit)

class LCD16_b(LCD16_a):
    """This is the same as the other 16 segment display, just wired differently.
    """
    SEGMENT_MAP = "EKMNRDPCxGUHTxxA"

class LCD16_c(LCD16_a):
    SEGMENT_MAP = "ERMNRDPCxGUHTSKA"

class LCD16_d(LCD16_a):
    SEGMENT_MAP = "ERMNRDPCxGUHTSKA"


class FrequencyDisplay:
    def decode(self, s):
        b = [ int(s[i:i+2], 16) for i in range(0, len(s)-1, 2) ]

        digits = [ LCD16_a.from_bytes(b, o) for o in [72, 88, 104, 120] ]
        digits += [ LCD16_b.from_bytes(b, 208) ]
        digits += [ LCD16_c.from_bytes(b, 192) ]
        digits += [ LCD16_d.from_bytes(b, 176) ]    

        return "".join([d.decode() for d in digits])

    def is_freq(self, s):
        disp = self.decode(s)

        for c in disp:
            if c not in list(" 0123456789"):
                return False

        return True


    def freq(self, s):
        if not self.is_freq(s):
            return None

        return int(self.decode(s))*10



    ################################################################################

class LCD16_mode_a(LCD16_a):
    SEGMENT_MAP = "AKcdeGgHiCPDmnoE"

class LCD16_mode_b(LCD16_a):
    SEGMENT_MAP = "AKcTeGUHiCPDNnRE"

class LCD16_mode_c(LCD16_a):
    SEGMENT_MAP = "KAcEeCPDiGkHSNMp"


class ModeDisplay:
    def decode(self, s):
        b = [ int(s[i:i+2], 16) for i in range(0, len(s)-1, 2) ]

        digits = [ LCD16_mode_a.from_bytes(b, 224),
                   LCD16_mode_b.from_bytes(b, 240),
                   LCD16_mode_c.from_bytes(b, 32) ]

        return "".join([d.decode() for d in digits])
    
