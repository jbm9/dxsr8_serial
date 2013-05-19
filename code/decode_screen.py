#!/usr/bin/env python

def _get_bit(bytes, offset):
    i = int(offset)/8
    j = offset % 8

    if (bytes[i] & (1<<j)) != 0:
        return 1
    return 0
    

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
        " " : "",
        "_" : "FE",
        "/" : "TN",
        "-" : "PU",
        "*" : "TKUPRN",
        "&" : "SUDPCEMF",
        "+" : "SUPM",
        "\\": "KR",
        "=" : "UPEF",
        "(" : "RN",
        ")" : "TK",
        "$" : "SAUHDPEMBF",

        # This is cyrillic, apparently. transliterating to the best of my ability
        "z" : "AUERNBF",
        "g" : "AGHB",
        "d" : "TDCENF",
        "s" : "TKAPEBF",
        "zh": "TSKRMN",

        "i" : "TGHDCN",
        "j" : "TAGHDCNB",
        "l" : "TDCN",
        "p" : "AGHDCB",
        "ch": "TKN",
        "|X|": "TSKGHDCRMN",
        "ts": "SGHEMF",
        "sh": "SGHDCEMF",
        "f": "SAERMBF",
        "yu": "GUHDCRN",
        "ya": "TAUHDPCB",
        "~": "ADPCEBF",
        "!": "TGUHDC",
        "@": "TGUH",
        
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
            print ">>> %s MISSING: %s" % (str(self.__class__),  self.lit, )
            print self.draw()
            return None

        return self.lookup[lit_key]

    


class LCD16_a(LCD16):

    # This is the segment associated with each bit in the input, in
    # ascending bit order.
    
    SEGMENT_MAP = "TSKAyGUHxDPCERMN"
    
    @classmethod
    def from_bytes(cls, bytes, offset):
        lit = ""
        for k in range(16):
            if 1 == _get_bit(bytes, offset+k):
                lit += cls.SEGMENT_MAP[k]

        return cls(lit)

class LCD16_b(LCD16_a):
    """This is the same as the other 16 segment display, just wired differently.
    """
    SEGMENT_MAP = "ERMNyDPCaGUHTSKA"

class LCD16_c(LCD16_a):
    SEGMENT_MAP = "FRMNEDPCxGUHTSKA"

class LCD16_d(LCD16_a):
    SEGMENT_MAP = "ERMNyDPCxGUHTSKA"


class FrequencyDisplay:
    def decode(self, b):
        digits = [ LCD16_a.from_bytes(b, o) for o in [72, 88, 104, 120] ]
        digits += [ LCD16_b.from_bytes(b, 208) ]
        digits += [ LCD16_c.from_bytes(b, 192) ]
        digits += [ LCD16_d.from_bytes(b, 176) ]    

        return "".join([d.decode() for d in digits])

    def is_freq(self, b):
        disp = self.decode(b)

        for c in disp:
            if c not in list(" 0123456789"):
                return False

        inspace = True
        for i in range(len(disp)):
            c = disp[i]
            
            if c != " ":
                inspace = False
                
            if not inspace and c not in "0123456789":
                return False

        if inspace:
            return False
            
        return True


    def freq(self, b):
        if not self.is_freq(b):
            return None

        return int(self.decode(b))*10



    ################################################################################

class LCD16_mode_a(LCD16_a):
    SEGMENT_MAP = "AKcdeGgHiCPDmnoE"

class LCD16_mode_b(LCD16_a):
    SEGMENT_MAP = "AKcTeGUHiCPDNnRE"

class LCD16_mode_c(LCD16_a):
    SEGMENT_MAP = "KAcEeCPDiGkHSNMp"


class ModeDisplay:
    def decode(self, b):
        digits = [ LCD16_mode_a.from_bytes(b, 224),
                   LCD16_mode_b.from_bytes(b, 240),
                   LCD16_mode_c.from_bytes(b, 32) ]

        return "".join([d.decode() for d in digits])
    


    ################################################################################

class RFPowerDisplay:
    def decode(self, b):
        # It's not clear which bit is RF-20, so we just assume it's
        # lit.  We can't tell which one it is because it never goes
        # off, so this seems like a safe assumption.

        rf10 = _get_bit(b, 40)
        rf0 = _get_bit(b, 244)
        rfp10 = _get_bit(b, 228)

        if rfp10 == 1:
            return 10
        if rf0 == 1:
            return 0
        if rf10 == 1:
            return -10
        return -20


class AGCDisplay():
    def decode(self, b):
        if 1 == _get_bit(b, 36):
            return "AGC-S"
        if 1 == _get_bit(b, 248):
            return "AGC-F"
        return ""

class SMeterDisplay():
    def decode(self, b):
        busy = _get_bit(b, 80)
        if 0 == busy:
            return None

        maxtick = max([ i-136 if 1 == _get_bit(b, i) else 0 for i in range(136, 162+1) ])

        if maxtick == 0:
            return 0

        if maxtick < 9*2:
            return 1 + float(maxtick-1)/2

        step = 1.259921 # 2^(1/3)
        db = 10

        for i in range(18, maxtick):
            db *= step

        return db

    def decode_string(self, b):
        g = self.decode(b)
        if None == g:
            return "squelch"
        return "%.2f" % g


    ################################################################################


class BacklightDisplay:
    def decode(self, b):
        return b[32] # hurray, a trivial one!


    ################################################################################


class MiscDisplay:
    def decode(self, b):
        retval = []

        sets = {
            "FUNC": 76,
            "KEY": 92,
            "STAR": 232,
            "NB": 212,
            #            "Nar": 200, # XXX TODO Narrow is lost!
            "T": 184,
            "TUNE": 52,
            "SPLIT": 54, 
            }


        for name,i in sets.iteritems():
            if 1 == _get_bit(b, i):
                retval.append(name)
        
        return retval

    
