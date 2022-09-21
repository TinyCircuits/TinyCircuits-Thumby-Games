AUTO   = const(0)
VIP    = const(1)
SCHIP  = const(2)
XOCHIP = const(3)

map = {
    "AUTO": AUTO,
    "VIP": VIP,
    "SCHIP": SCHIP,
    "XOCHIP": XOCHIP
}

def parseType(type):
    if isinstance(type, int):
        return type
    if isinstance(type, str) and type.upper() in map:
        return map[type.upper()]
