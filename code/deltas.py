mode_a = {
    "A": 224,
    "K": 225,        
    "C": 233,
    "D": 235,
    "E": 239,
    "G": 229,
    "H": 231,
    "P": 234,
    }


mode_b = {
    "A": 240,
    "C": 249,
    "D": 251,
    "E": 255,
    "G": 245,
    "H": 247,
    "K": 241,
    "N": 252,
    "R": 254,
    "T": 243,
    "U": 246,
    "P": 250,
    }


mode_c = {
    "K": 32,
    "N": 45,
    "A": 33,
    "C": 37,
    "D": 39,
    "E": 35,
    "G": 41,
    "H": 43,
    "K": 32,
    "M": 46,
    "S": 44,
    "P": 38,
    }

pts = mode_c

base = min(pts.values())

retval = list("abcdefghijklmnopqrstuv")
retval = retval[0:16] # lazy? yes.

for c,v in pts.iteritems():
    retval[v-base] = c

print repr("".join(retval))
