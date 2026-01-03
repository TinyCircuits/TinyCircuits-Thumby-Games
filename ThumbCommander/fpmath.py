# fpmath.py - Fixed-point math functions for ThumbCommander
from array import array
from math import sin, pi, exp
try:
    from micropython import const
except ImportError:
    const = lambda x: x

@micropython.viper
def int2fp(v:int) -> int:
    return v << 16

@micropython.viper
def fp2int(v:int) -> int:
    return v >> 16

@micropython.native
def fp2float(v:int) -> float:
    return v / 65536

@micropython.native
def float2fp(v:float) -> int:
    return int(v * 65536)

@micropython.viper
def fpmul(a:int, b:int) -> int:
    return (a >> 8) * (b >> 8)

@micropython.viper
def fpdiv_a(a:int, b:int) -> int:
    return ((a << 4) // (b >> 4)) << 8

@micropython.viper
def fpdiv(a:int, b:int) -> int:
    return a if (b >> 3) == 0 else ((a << 3) // (b >> 3)) << 10

@micropython.viper
def project(xy:int, z:int, center_xy:int, sprite_wh:int=0) -> int:
    a:int = fpdiv(xy, abs(z))
    b:int = int(a)>>16
    c:int = sprite_wh >> 1
    return b + center_xy - c

# Sin/cos tables
sintab_sz = const(1024)
sintab_mask = const(sintab_sz - 1)
sintab_quart_mask = const(sintab_mask >> 2)
sintab_half_mask = const(sintab_mask >> 1)
sintab_sz_quart = const(sintab_sz >> 2)
sintab_sz_half = const(sintab_sz >> 1)
sintab = array('l', [int(sin(i * ((2 * pi) / sintab_sz)) * 65536) for i in range(sintab_sz // 4)])

@micropython.viper
def fpsin(a:int) -> int:
    a &= sintab_mask
    ta:int = a & sintab_quart_mask
    if (a & sintab_half_mask) >= sintab_sz_quart:
        ta = sintab_quart_mask - ta
    v:int = ptr32(sintab)[ta]
    if a >= sintab_sz_half:
        return 0 - v
    return v

@micropython.viper
def fpcos(a:int) -> int:
    return int(fpsin(a + sintab_sz_quart))

@micropython.viper
def rotate_z_x(x:int, y:int, angle:int) -> int:
    a:int = fpmul(x, fpcos(angle))
    b:int = fpmul(y, fpsin(angle))
    return int(a - b)

@micropython.viper
def rotate_z_y(x:int, y:int, angle:int) -> int:
    a:int = fpmul(x, fpsin(angle))
    b:int = fpmul(y, fpcos(angle))
    return int(a + b)

def sign(x):
    return (x > 0) - (x < 0)

@micropython.native
def sort_by_z(arr):
    """In-place insertion sort by Z (descending) - O(n) for nearly-sorted"""
    n = len(arr)
    i = 1
    while i < n:
        key = arr[i]
        key_z = key[2]
        j = i - 1
        while j >= 0 and arr[j][2] < key_z:
            arr[j + 1] = arr[j]
            j -= 1
        arr[j + 1] = key
        i += 1

# Physics table
TABLE_SIZE = const(128)
MIN_DAMPING = const(7)
MAX_T_DAMPING = const(10<<16)
EXP_TABLE = array('l', [0] * TABLE_SIZE)
for _i in range(TABLE_SIZE):
    EXP_TABLE[_i] = int(exp(-_i * (MAX_T_DAMPING>>16) / TABLE_SIZE) * 65536)
del _i

@micropython.native
def apply_physics(damping: int, desired_vel: int, initial_vel: int, t: int) -> int:
    if damping < MIN_DAMPING:
        return desired_vel
    dv = initial_vel - desired_vel
    t_damping = fpdiv_a(t, damping)
    if t_damping >= MAX_T_DAMPING:
        e = 0
    else:
        scaled = (t_damping * TABLE_SIZE) // (MAX_T_DAMPING >> 16)
        idx = min(TABLE_SIZE - 2, max(0, scaled >> 16))
        frac = scaled & 0xFFFF
        e = EXP_TABLE[idx] + (((EXP_TABLE[idx + 1] - EXP_TABLE[idx]) * frac) >> 16)
    return ((dv * e) >> 16) + desired_vel
