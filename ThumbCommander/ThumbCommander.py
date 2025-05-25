from sys import path
loc = "/Games/ThumbCommander/"
path.insert(0, '/Games/ThumbCommander')
from grayscale import display, Sprite
import Intro

#show the Intro while loading
display.enableGrayscale() 
Intro.__init__()
Intro.start()

from machine import freq
# Overclock. It doesn't seem to run above 250MHz
freq(200_000_000)

from thumbyButton import buttonA, buttonB, buttonU, buttonD, buttonL, buttonR, dpadPressed, inputJustPressed
from thumbyHardware import reset
from random import randint, randrange, choice
from time import sleep
from utime import ticks_us, ticks_ms, ticks_diff
from math import sin, pi, cos, exp
from array import array
from gc import collect
import json
from campaign_engine import CampaignEngine

WIDTH = const(72) 
HEIGHT = const(40)
CENTER_X = const(WIDTH // 2)
CENTER_Y = const(HEIGHT // 2)
SHIP_X:int = 4
SHIP_Y:int = 23
COLORS:int = [display.WHITE, display.DARKGRAY, display.LIGHTGRAY]
ORIENTATION:int = [-512,-427,-341,-256,-171,-85,0,85,171,256,341,427,512]
X_INDEX:int = [24,25,26,27,26,25,24,23,22,21,22,23,24]
X_MIRROR:bool = [False,False,False,False,True,True,True,True,True,False,False,False,False]
Y_SHIFT:int = [0,-7,-14,-21,-14,-7,0,7,14,21,14,7,0]
Y_MIRROR:bool = [True,False,False,False,False,False,True,True,True,True,True,True,True]
ASTROIDS:int = [1, 2]
SHIPS:int = [3]
Z_DISTANCE = const(30)
FPS = const(40)

# Player properties
player_speed:int = 65536
player_target_speed:int = 65536

lifes:int = 5
player_angle:int = [0, 0, 0]
score:int = 0
hudShip = None

# Sprites
OBJECTS = list(["","","",""])

OBJECTS[0] = Sprite(56,54,(loc+"explode_56.BIT.bin",loc+"explode_56.SHD.bin"),0,0,0)
OBJECTS[1] = Sprite(56,47,(loc+"astroid1_56.BIT.bin",loc+"astroid1_56.SHD.bin"),0,0,0)
OBJECTS[2] = Sprite(56,47,(loc+"astroid2_56.BIT.bin",loc+"astroid2_56.SHD.bin"),0,0,0)
OBJECTS[3] = Sprite(70,59,(loc+"enemy1_59.BIT.bin",loc+"enemy1_59.SHD.bin"),0,0,0)

# BITMAP: width: 66, height: 18
cockpit = bytearray([255,252,255,253,253,255,251,251,251,247,247,239,239,239,223,31,159,31,31,31,35,29,61,29,63,31,63,157,61,29,35,31,31,31,31,31,63,63,31,31,63,31,31,63,31,63,31,31,31,159,223,223,223,239,239,239,247,247,251,251,251,253,253,255,252,255,
           255,255,255,255,255,255,255,127,127,63,63,63,159,15,11,6,0,0,0,0,0,0,0,0,0,0,0,86,0,0,0,0,0,0,0,0,0,0,0,0,8,20,8,0,0,0,0,0,0,0,2,11,15,159,31,63,63,127,127,255,255,255,255,255,255,255,
           3,3,3,1,1,0,0,0,0,0,0,2,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,3,3,3,3,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,2,0,0,0,0,0,0,1,1,3,3,3])
cockpitSHD = bytearray([1,3,3,2,2,6,4,4,12,12,24,24,16,48,48,96,160,96,160,224,124,98,226,226,226,226,226,226,226,98,124,96,96,96,96,96,96,224,224,224,224,224,224,224,224,224,224,160,96,224,96,96,48,48,16,24,24,12,12,4,6,6,2,3,3,1,
           0,0,0,0,0,0,128,128,192,192,224,96,144,112,220,247,188,223,239,255,127,119,127,127,119,127,127,119,127,128,128,128,128,128,128,128,128,127,127,66,74,87,74,66,127,127,225,225,255,253,247,220,112,144,96,224,192,192,128,128,0,0,0,0,0,0,
           0,2,2,2,3,3,3,3,3,1,0,2,1,3,0,0,0,0,0,3,0,0,0,0,0,0,0,0,0,3,3,3,3,3,3,3,3,0,0,0,0,0,0,0,0,0,3,0,0,0,0,0,3,1,2,0,1,3,3,3,3,3,3,2,2,0])# BITMAP: width: 7, height: 7
target = bytearray([65,34,0,0,0,34,65])
targetSHD = bytearray([0,0,0,0,0,0,0])
# BITMAP: width: 7, height: 7
targetactive = bytearray([127,99,65,65,65,99,127])
targetactiveSHD = bytearray([62,65,65,65,65,65,62])
# BITMAP: width: 15, height: 15
radar = bytearray([192,152,132,130,130,128,129,255,129,128,130,130,132,152,192,
           1,4,16,32,32,0,64,127,64,0,32,32,16,12,1])
radarSHD = bytearray([192,152,132,130,130,128,129,255,129,128,130,130,132,152,192,
           1,4,16,32,32,0,64,127,64,0,32,32,16,12,1])
# BITMAP: width: 70, height: 70
shield = bytearray([0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,128,128,192,192,224,224,32,48,112,112,24,8,8,24,56,24,24,24,24,24,24,24,56,120,112,240,240,224,224,224,192,192,128,128,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,
           0,0,0,0,0,0,0,0,0,128,192,224,240,88,4,2,3,1,1,1,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,8,13,15,31,31,126,222,252,248,240,224,192,128,0,0,0,0,0,0,0,0,0,
           0,0,0,0,0,192,240,60,7,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,7,15,95,255,255,255,252,240,192,0,0,0,0,0,
           0,0,0,240,255,63,12,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,15,255,255,255,255,255,240,0,0,0,
           0,0,0,255,243,17,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,2,0,255,255,255,255,255,255,0,0,0,
           0,0,0,3,24,200,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,224,252,255,255,255,255,63,3,0,0,0,
           0,0,0,0,0,0,3,14,14,94,232,32,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,32,96,224,224,250,255,127,31,15,3,0,0,0,0,0,0,
           0,0,0,0,0,0,0,0,0,0,0,1,2,6,15,30,24,32,96,96,224,192,128,128,0,0,0,0,0,0,0,0,0,0,0,0,0,0,128,128,192,128,128,192,224,208,240,224,224,224,112,112,56,62,30,15,7,3,1,0,0,0,0,0,0,0,0,0,0,0,
           0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,1,1,3,3,3,6,4,4,4,6,6,6,6,6,7,7,7,7,7,3,3,3,1,1,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0])
shieldSHD = bytearray([0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,128,128,192,192,224,224,32,48,112,112,24,8,8,24,56,8,24,16,24,24,24,24,48,112,96,240,240,192,192,192,128,192,128,128,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,
           0,0,0,0,0,0,0,0,0,0,192,224,240,88,4,2,3,1,1,1,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,8,13,15,31,31,110,204,128,0,0,0,0,128,0,0,0,0,0,0,0,0,0,
           0,0,0,0,0,192,224,60,7,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,7,14,94,255,254,247,32,0,0,0,0,0,0,0,
           0,0,0,240,255,63,12,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,15,255,252,0,0,1,0,0,0,0,
           0,0,0,191,243,17,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,2,0,253,196,0,0,0,0,0,0,0,
           0,0,0,3,24,200,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,224,252,255,79,0,0,0,0,0,0,0,
           0,0,0,0,0,0,3,14,14,94,232,32,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,32,96,224,224,58,31,29,23,0,0,0,0,0,0,0,0,
           0,0,0,0,0,0,0,0,0,0,0,1,2,6,15,30,24,32,96,96,224,192,128,128,0,0,0,0,0,0,0,0,0,0,0,0,0,0,128,128,192,128,128,192,224,208,240,224,224,224,112,112,56,46,14,15,7,3,1,0,0,0,0,0,0,0,0,0,0,0,
           0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,1,1,3,3,3,6,4,4,4,6,6,6,6,6,7,7,7,3,1,1,3,2,1,1,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0])

DEFAULT_KEYS = array('B', [
    ord('A'),  # FIRE (index 0)
    ord('B'),  # SHIFT (index 1)
    ord('L'),  # MOVE_LEFT (index 2)
    ord('R'),  # MOVE_RIGHT (index 3)
    ord('D'),  # MOVE_UP (index 4)
    ord('U'),  # MOVE_DOWN (index 5)
    ord('U'),  # AFTERBURNER (index 6)
    ord('D'),  # BREAK (index 7)
    ord('R'),  # TARGET_NEXT (index 8)
    ord('L')   # TARGET_PREV (index 9)
])

# Constants for key indexes
KEY_FIRE = const(0)
KEY_SHIFT = const(1)
KEY_MOVE_LEFT = const(2)
KEY_MOVE_RIGHT = const(3)
KEY_MOVE_UP = const(4)
KEY_MOVE_DOWN = const(5)
KEY_AFTERBURNER = const(6)
KEY_BREAK = const(7)
KEY_TARGET_NEXT = const(8)
KEY_TARGET_PREV = const(9)

def copySprite(obj:Sprite):
    newSprite = Sprite(obj.width, obj.height,(bytearray(obj.bitmapByteCount), bytearray(obj.bitmapByteCount)),0,0,obj.key,obj.mirrorX,obj.mirrorY)
    newSprite.setFrame(obj.currentFrame)
    newSprite.bitmap[0][:] = obj.bitmap[0]
    newSprite.bitmap[1][:] = obj.bitmap[1]
    return newSprite
    
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
    return (a >> 6) * (b >> 6) >> 4

@micropython.viper
def fpmul_a(a:int, b:int) -> int:
    return (a >> 8) * (b >> 8)
    
@micropython.viper
def fpdiv(a:int, b:int) -> int:
    return ((a << 6) // (b >> 6)) << 4

@micropython.viper
def fpdiv_a(a:int, b:int) -> int:
    return ((a << 4) // (b >> 4)) << 8

# calc x,y on screen
@micropython.viper
def project(xy:int, z:int, center_xy:int) -> int:
    a:int = fpdiv(xy, z)
    b:int = int(a)>>16
    return b + center_xy

# calc x,y on screen
@micropython.viper
def project_a(xy:int, z:int, center_xy:int, sprite_wh:int=0) -> int:
    a:int = fpdiv_a(xy, abs(z))
    b:int = int(a)>>16
    c:int = sprite_wh >> 1
    return b + center_xy - c
    
sintab_sz = const(1024)
sintab_mask = const(sintab_sz - 1)
sintab_quart_mask = const(sintab_mask >> 2)
sintab_half_mask = const(sintab_mask >> 1)
sintab_sz_quart = const(sintab_sz >> 2)
sintab_sz_half = const(sintab_sz >> 1)
sintab:array = array('l', [ int(sin(i * ((2 * pi) / sintab_sz)) * 65536) for i in range(sintab_sz // 4)])

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
def rotate_z_x(x:int,y:int, angle:int) -> int:
    a:int = fpmul(x, fpcos(angle))
    b:int = fpmul(y, fpsin(angle))
    return int(a - b)

@micropython.viper
def rotate_z_x1(x:int,y:int, angle:int) -> int:
    a:int = fpmul_a(x, fpcos(angle))
    b:int = fpmul_a(y, fpsin(angle))
    return int(a - b)
    
@micropython.viper
def rotate_z_y(x:int,y:int, angle:int) -> int:    
    a:int = fpmul(x, fpsin(angle))
    b:int = fpmul(y, fpcos(angle))
    return int(a + b)

@micropython.viper
def rotate_z_y1(x:int,y:int, angle:int) -> int:
    a:int = fpmul_a(x, fpsin(angle))
    b:int = fpmul_a(y, fpcos(angle))
    return int(a + b)
    
def sign(x):
    return (x > 0) - (x < 0)

@micropython.native
def qsort(inlist):
    if inlist == []: 
        return []
    else:
        pivot = inlist[0]
        lesser = qsort([x for x in inlist[1:] if x[2] < pivot[2]])
        greater = qsort([x for x in inlist[1:] if x[2] >= pivot[2]])
        return greater + [pivot] + lesser

# Use lookup table for exp(-t/damping)
TABLE_SIZE = const(1024)
MIN_DAMPING = const(7)  # 0.0001 in fixed point
MAX_T_DAMPING = const(10<<16)  # Maximum t/damping ratio
EXP_TABLE = [float2fp(exp(-i * (MAX_T_DAMPING>>16) / TABLE_SIZE)) for i in range(TABLE_SIZE)]

@micropython.native
def apply_physics(damping: int, desired_vel: int, initial_vel: int, t: int) -> int:
    if damping < MIN_DAMPING:
        return desired_vel, (desired_vel * t) >> 16
    else:
        dv = initial_vel - desired_vel
        t_damping = fpdiv_a(t, damping)
        if t_damping >= MAX_T_DAMPING:
            e = 0
        else:
            idx = (t_damping * TABLE_SIZE * fpdiv_a(1<<16, MAX_T_DAMPING))>>16
            idx = min(TABLE_SIZE - 2, max(0, idx>>16))
            frac = ((t_damping * TABLE_SIZE * fpdiv_a(65536, MAX_T_DAMPING))>>16) & (65536 - 1)
            e = ((EXP_TABLE[idx] * (65536 - frac)) + (EXP_TABLE[idx + 1] * frac))>>16
        new_vel = ((dv * e)>>16) + desired_vel
        return new_vel
    
@micropython.native
def getSprite(z, shape):
        OBJECTS[shape].setScale(fpdiv((71<<16)-abs(z), 60<<16))
        return OBJECTS[shape]

#@micropython.native
def button_exists(button_char:int) -> bool:
    try:
        button_name = "button" + chr(button_char)
        return bool(button_name in globals())
    except:
        return False
        
def load_keymaps():
    try:
        with open(loc + "keymap.json", "r") as f:
            loaded_keys = json.loads(f.read())
            # Create a new array with default values
            complete_keys = array('B', DEFAULT_KEYS)
            
            # Update only valid keys
            if "FIRE" in loaded_keys and button_exists(ord(loaded_keys["FIRE"])):
                complete_keys[KEY_FIRE] = ord(loaded_keys["FIRE"])
            if "SHIFT" in loaded_keys and button_exists(ord(loaded_keys["SHIFT"])):
                complete_keys[KEY_SHIFT] = ord(loaded_keys["SHIFT"])
            if "MOVE_LEFT" in loaded_keys and button_exists(ord(loaded_keys["MOVE_LEFT"])):
                complete_keys[KEY_MOVE_LEFT] = ord(loaded_keys["MOVE_LEFT"])
            if "MOVE_RIGHT" in loaded_keys and button_exists(ord(loaded_keys["MOVE_RIGHT"])):
                complete_keys[KEY_MOVE_RIGHT] = ord(loaded_keys["MOVE_RIGHT"])
            if "MOVE_UP" in loaded_keys and button_exists(ord(loaded_keys["MOVE_UP"])):
                complete_keys[KEY_MOVE_UP] = ord(loaded_keys["MOVE_UP"])
            if "MOVE_DOWN" in loaded_keys and button_exists(ord(loaded_keys["MOVE_DOWN"])):
                complete_keys[KEY_MOVE_DOWN] = ord(loaded_keys["MOVE_DOWN"])
            if "AFTERBURNER" in loaded_keys and button_exists(ord(loaded_keys["AFTERBURNER"])):
                complete_keys[KEY_AFTERBURNER] = ord(loaded_keys["AFTERBURNER"])
            if "BREAK" in loaded_keys and button_exists(ord(loaded_keys["BREAK"])):
                complete_keys[KEY_BREAK] = ord(loaded_keys["BREAK"])
            if "TARGET_NEXT" in loaded_keys and button_exists(ord(loaded_keys["TARGET_NEXT"])):
                complete_keys[KEY_TARGET_NEXT] = ord(loaded_keys["TARGET_NEXT"])
            if "TARGET_PREV" in loaded_keys and button_exists(ord(loaded_keys["TARGET_PREV"])):
                complete_keys[KEY_TARGET_PREV] = ord(loaded_keys["TARGET_PREV"])
            
                return complete_keys
    except:
        return array('B', DEFAULT_KEYS)
        

def save_keymaps(keymap):
    try:
        # Convert array to dictionary for JSON serialization
        keymap_dict = {
            "FIRE": chr(keymap[KEY_FIRE]),
            "SHIFT": chr(keymap[KEY_SHIFT]),
            "MOVE_LEFT": chr(keymap[KEY_MOVE_LEFT]),
            "MOVE_RIGHT": chr(keymap[KEY_MOVE_RIGHT]),
            "MOVE_UP": chr(keymap[KEY_MOVE_UP]),
            "MOVE_DOWN": chr(keymap[KEY_MOVE_DOWN]),
            "AFTERBURNER": chr(keymap[KEY_AFTERBURNER]),
            "BREAK": chr(keymap[KEY_BREAK]),
            "TARGET_NEXT": chr(keymap[KEY_TARGET_NEXT]),
            "TARGET_PREV": chr(keymap[KEY_TARGET_PREV])
        }
        with open(loc + "keymap.json", "w") as f:
            f.write(json.dumps(keymap_dict))
    except:
        pass


# Global variable to store key mappings
KEYMAPS = load_keymaps()

class Stars:
    def __init__(self, num:int, scale_pos:int=4, stable=80):
        stars = array('O', [None] * num)
        for i in range(num):
            speed = 0 if (randint(0,100) <= stable) else randint(42598, 62258)
            if speed != 0:
                angle = randint(0, 4096)
                radius = int2fp(randint(WIDTH // scale_pos, WIDTH*2) * scale_pos)
                stars[i] = array('l', [fpmul(radius, fpcos(angle)),
                          fpmul(radius, fpsin(angle)),
                          randint(5, Z_DISTANCE)<<16,
                          randint(1,3),
                          speed])
            else:
                stars[i] = array('l', [randint(-200,200)<<16,
                          randint(-200,200)<<16,
                          7<<16,
                          randint(1,3),
                          0])    
        self.stars = stars
        self.scale = scale_pos

    @micropython.native
    def run(self, angle:int=0):
        global player_speed

        for s in self.stars:
            x = project(s[0], s[2], CENTER_X)
            y = project(s[1], s[2], CENTER_Y)
            size = 1 if s[4] == 0 else fp2int(fpdiv(Z_DISTANCE<<16, fpmul(72090, s[2])))
  
            if (-size < x < WIDTH + size) and (-size < y < HEIGHT + size):
                display.drawFilledRectangle(x, y, size, size, s[3])
            
            # move forward
            if s[4] == 0:
                for c in range(2):
                    s[c] += player_angle[c] + (player_speed-65536)
                    if (s[c] > (200<<16)) or (s[c] < -(200<<16)):
                        s[c] = -s[c]
            s[2]  -= fpmul(s[4], player_speed)
            
            # Rotate around z-axis
            if angle != 0:
                temp_x = fpmul(s[0], fpcos(angle)) - fpmul(s[1], fpsin(angle))
                temp_y = fpmul(s[0], fpsin(angle)) + fpmul(s[1], fpcos(angle))
                s[0] = temp_x
                s[1] = temp_y
         
            if s[2] < (1<<16):
                a = randint(0, 4096)
                radius = int2fp(randint(WIDTH // self.scale, WIDTH*2) * self.scale)
                s[0] = fpmul(radius, fpcos(a))
                s[1] = fpmul(radius, fpsin(a))
                s[2] = Z_DISTANCE<<16
    
class Astroids:
    def __init__(self, num:int=5):
        astroids = array('O', [None] * num)
        for i in range(num):
            astroids[i] = self.new_astroid()
        self.astroids = astroids
     
    @micropython.native
    def new_astroid(self):
        a = array('l', [randrange(-1000<<16, 1000<<16),      #0: x
                          randrange(-1000<<16, 1000<<16),    #1: y
                          60<<16,                            #2: z
                          randint(-655360,655360),           #3: x-velocity
                          randint(-655360,655360),           #4: y-velocity
                          randint(6554, 13107),              #5: z-velocity
                          choice(ASTROIDS),                  #6: sprite_shape
                          randint(2, 4),                     #7: rotationspeed
                          0])                                #8: step
        return a
        
    #@micropython.native
    def run(self, laser=[], mission_phase_complete=False):
        global player_speed, lifes, score
        
        self.astroids = qsort(self.astroids)
        
        for i in range(len(self.astroids)):
            if i >= len(self.astroids): return
            a = self.astroids[i]
            
            # move in x,y,z-axis forward
            for c in range(2):
                if (a[c] > (1000<<16)) or (a[c] < -(1000<<16)):
                    a[c+3] = -a[c+3]
                a[c] += a[c+3]
                a[c] += player_angle[c] + (player_speed-65536)
            a[2] -= fpmul(a[5], player_speed)
            
            # get sprite in correct size
            mySprite = getSprite(a[2],a[6])
            
            # calc x,y on screen
            x = project_a(a[0], a[2], CENTER_X, mySprite.scaledWidth)
            y = project_a(a[1], a[2], CENTER_Y, mySprite.scaledHeight)
            
            # collision detection        
            if a[2] < (8<<16):
                if (-28 < x < WIDTH) and (-20 < y < HEIGHT):
                    lifes -= 1
                    display.drawFilledRectangle(0,0,WIDTH, HEIGHT, 1)
                if not mission_phase_complete:
                    self.astroids[i] = self.new_astroid()
                else:
                    self.astroids.pop(i)
                    continue
                
            # Rotate around z-axis
            if player_angle[2] != 0:
                a[0] = rotate_z_x(a[0], a[1], player_angle[2])
                a[1] = rotate_z_y(a[0], a[1], player_angle[2])
                
            # Rotate sprite
            n = a[8] // a[7]
            if (n > 12):
                n = 0
                a[8] = 0
            else:
                a[8] += 1
            mySprite.setFrame(n)
            
            # draw sprite
            mySprite.x = x
            mySprite.y = y
            display.drawSpriteWithScale(mySprite)
            
            if (a[6] == 0):
                if (n == 6):
                    if not mission_phase_complete:
                        self.astroids[i] = self.new_astroid()
                    else:
                        self.astroids.pop(i)
                        continue
            else:
                for l in range(len(laser)):
                    if (abs(laser[l].z-a[2]) < (2<<16)) and (0 < (laser[l].screen_pos_x-x) < (mySprite.scaledWidth - (mySprite.scaledWidth >> 2))) and ( 0 < (laser[l].screen_pos_y-y) < (mySprite.scaledHeight - (mySprite.scaledHeight >> 2))):
                        del laser[l]
                        score += 1
                        player_speed += 1311
                        #set sprite to exposion, stop movement and reset to first bitmap
                        a[3] = a[4] = a[5] = a[6] = a[8] = 0
                        a[7] = 3
                        break

class Enemies:
    def __init__(self, num:int=1):
        enemies = array('O', [None] * num)
        for i in range(num):
            enemies[i] = self.new_enemy()
        self.shieldSprite = Sprite(70,70,(shield,shieldSHD),0,0,0)
        self.enemies = enemies
        self.last_time = 0
     
    @micropython.native
    def new_enemy(self):
        
        e = array('O', [randrange(-1000<<16, 1000<<16),      #0: x
                        randrange(-1000<<16, 1000<<16),      #1: y
                          45<<16,                            #2: z
                          randrange(0, 12),                  #3: x-orientation (0:-180, 6:0, 12:+180)
                          randrange(0, 12),                  #4: y-orientation (0:-180, 6:0, 12:+180)
                          randint(6<<16,12<<16),             #5: thrust
                          choice(SHIPS),                     #6: sprite_shape
                          5,                                 #7: health
                          0,                                 #8: selected
                          [],                                #9: Laser
                          None,                             #10: Pilot
                          0,                                #11: x-acceleartion
                          0,                                #12: y-acceleration
                          0])                               #13: z-acceleration
        e[10] = Pilot(e)
        e[11] = ((e[5] + (60<<16) - abs(e[2])) * fpcos(ORIENTATION[e[3]]))>>16
        e[12] = ((e[5] + (60<<16) - abs(e[2])) * (fpsin(ORIENTATION[e[3]]) * fpsin(ORIENTATION[e[4]]))) >> 32
        e[13] = (e[5] * (fpsin(ORIENTATION[e[3]]) * fpcos(ORIENTATION[e[4]]))) >> 38
        return e
        
    #@micropython.native
    def run(self, laser=[], mission_phase_complete=False):
        global player_speed, lifes, score, hudShip
        # ticks in ms passed since last call for body inertia calaculation
        new_time = ticks_us()
        t = (ticks_diff(new_time, self.last_time,)<<16)//1000000
        self.last_time = new_time
        
        self.enemies = qsort(self.enemies)
        
        for i in range(len(self.enemies)):
            if i >= len(self.enemies): return
            e = self.enemies[i]
            visible = True
            
            # move in x,y,z-axis forward
            for c in range(2):
                # xy displacement based on player_angle * player_speed
                e[c] += player_angle[c] + (player_speed-65536)
            e[2] -= fpmul(2048, player_speed)
                
            # calc displacement of ship form orientation & thrust if not exploding
            if e[6] != 0:
                # calc xyz velocity with thrust * COS/SIN X,Y,Z orientation incl. body inertia
                e[11] = apply_physics(4<<16,((e[5] + (60<<16) - abs(e[2])) * fpcos(ORIENTATION[e[3]]))>>16, e[11],t)
                e[12] = apply_physics(4<<16,((e[5] + (60<<16) - abs(e[2])) * (fpsin(ORIENTATION[e[3]]) * fpsin(ORIENTATION[e[4]]))) >> 32, e[12], t)
                e[13] = apply_physics(4<<16,(e[5] * (fpsin(ORIENTATION[e[3]]) * fpcos(ORIENTATION[e[4]]))) >> 38, e[13], t)
                e[0] += e[11]
                e[1] += e[12]
                e[2] += e[13]
            
            # rotate around z-axis
            if player_angle[2] != 0:
                e[0] = rotate_z_x1(e[0], e[1], player_angle[2])
                e[1] = rotate_z_y1(e[0], e[1], player_angle[2])
            
            # move though known space    
            if (e[0] > (6143<<16)): e[0] = -2047<<16
            elif (e[0] < -(6143<<16)): e[0] = 2047<<16
            if (e[0] > (2047<<16)) or (e[0] < -(2047<<16)): visible = False
            
            if (e[1] > (5600<<16)): e[1] = -1400<<16
            elif (e[1] < -(5600<<16)): e[1] = 1400<<16
            if (e[1] > (1400<<16)) or (e[1] < -(1400<<16)): visible = False
                
            # adjust x-y-z-axis if enemy moves behind and infront of me
            if (e[2] < 0) and ((e[2] + e[13]) > 0):
                e[2] += e[13]
                visible = True
                e[0] = e[0] % (2047<<16)
                e[1] = e[1] % (1400<<16)
            elif visible: e[2] = abs(e[2])
            else: e[2] = -abs(e[2])
            
            # if space in z axis is ending change ship's x-orientation by 180°
            if (e[2] > (70<<16)) or (e[2] < (-70<<16)):
                e[3] = (e[3]+6) % 12
                e[2] += sign(e[2])*(-5<<16)
            
           #e[4] =  (e[4]+1) % 12
            
            if visible or (e[8] == 1):
                # get sprite in correct size
                mySprite = getSprite(e[2],e[6])
                
                # Sprite is a ship
                if e[6] != 0:
                    #get Frame and mirror based ony X,Y Orientation
                    mySprite.setFrame(X_INDEX[e[3]] + Y_SHIFT[e[4]])
                    # set X mirrow
                    mySprite.mirrorX = X_MIRROR[e[3]]
                    # set Y mirrow
                    mySprite.mirrorY = Y_MIRROR[e[4]]
                # sprite is the explosion
                else:
                    mySprite.setFrame(e[5])
                    e[5] += 1
                if visible:
                    # calc x,y on screen
                    x = project_a(e[0], e[2], CENTER_X, mySprite.scaledWidth)
                    y = project_a(e[1], e[2], CENTER_Y, mySprite.scaledHeight)
                   
                    # draw sprite
                    mySprite.x = x
                    mySprite.y = y
                    display.drawSpriteWithScale(mySprite)
                    
                if e[8] == 1:
                    hudShip = copySprite(mySprite)
                    hudShip.setLifes(e[7])
                    #print("z:",e[2]/65535, " th:",e[13]/65536,"tx/ty: ", e[10].target_x,",",e[10].target_y)
                # explosion done - get new ship
                if (e[6] == 0):
                    if (e[5] == 6):
                        if not mission_phase_complete:
                            self.enemies[i] = self.new_enemy()
                        else:
                            self.enemies.pop(i)
                            continue
                else:
                    if (e[8] == 1) and visible:
                        display.drawRectangle(x-2, y-2, mySprite.scaledWidth+4, mySprite.scaledHeight+4, 1)
                    for l in range(len(laser)):
                        if (abs(laser[l].z-e[2]) < (2<<16)) and (laser[l].screen_pos_x > mySprite.x) and (laser[l].screen_pos_x < (mySprite.x+mySprite.scaledWidth)) and (laser[l].screen_pos_y > mySprite.y) and (laser[l].screen_pos_y < (mySprite.y+mySprite.scaledHeight)):
                            del laser[l]
                            e[7] -= 1
                            # Draw shield
                            self.shieldSprite.setScale(fpdiv((71<<16)-abs(e[2]), 60<<16))
                            self.shieldSprite.x = x-1
                            self.shieldSprite.y = y-1
                            display.drawSpriteWithScale(self.shieldSprite)
                            if e[7] == -1:
                                score += 1
                                #set sprite to exposion, stop movement and reset to first bitmap
                                e[5] = e[6] = 0
                            break
            # calc and draw radar
            x = (((abs(e[2])>>3) * fpcos((e[0]>>19)-256))>>32) + 63
            y = (((abs(e[2])>>3) * fpsin((e[0]>>19)-256))>>32) + 7
            height = (e[1]>>16) // 700
            color = 1 if e[8] == 1 else 3
            display.drawFilledRectangle(x,y,3,3,color)
            if (height < 0):
                display.drawFilledRectangle(x+1,y+height,1,abs(height),color)
            else:  
                display.drawFilledRectangle(x+1,y,1,abs(height),color)
            
            # if not exploded, let the pilot do it's thing
            if e[6] != 0: e[10].run()
            
            #let the lasers fly! 
            for myLaser in e[9]:
                if myLaser.run(): e[9].remove(myLaser)
                else:
                    if myLaser.z < (8<<16) and (-512<<16 < myLaser.x < 512<<16) and (-300<<16 < myLaser.y < 300<<16):
                        lifes -= 1
                        display.drawFilledRectangle(0,0,WIDTH, HEIGHT, 1)
                        e[9].remove(myLaser)

class Pilot:
    # manuevers
    NONE = const(0)
    ATTACK = const(1)
    CIRCLE = const(2)
    FLEE = const(3)
    CRAZYIVAN = const(4)
    
    def __init__(self,enemy):
        self.enemy = enemy
        self.timer = 0
        self.freq = randint(1,3)
        self.triggerhappy = randint(2,4)
        self.lucky = randint(4,8)
        self.manuver = Pilot.NONE
        self.target_x = 0
        self.target_y = 0
        self.target_d = 0
    
    @micropython.native    
    def run(self):
        self.timer += 1
        if ((self.timer*self.freq) >= FPS):
            self.timer = 0
            if (self.manuver == Pilot.ATTACK): self.do_attack()
            elif (self.manuver == Pilot.CIRCLE): self.do_circle()
            elif (self.manuver == Pilot.FLEE): self.do_flee()
            elif (self.manuver == Pilot.CRAZYIVAN): self.do_crazyivan()
            else: self.manuver = randint(0,20)
           
            #fire Laser
            if ((self.enemy[3] > 7) and (self.enemy[3] < 11) and (self.enemy[4] > 4) and (self.enemy[4] < 8) and (randint(0,self.triggerhappy) == 1) or (randint(0,self.lucky) == 1)):
                self.enemy[9].append(Laser(self.enemy[0], self.enemy[1], self.enemy[2], self.enemy[11]*2,self.enemy[12]*2,self.enemy[13]*3))
    
    @micropython.native    
    def do_attack(self):
        if (self.enemy[3] > 3) and (self.enemy[3] < 9): self.enemy[3] = (self.enemy[3]+1) % 12 
        elif (self.enemy[3] < 4) or (self.enemy[3] > 9): self.enemy[3] = (self.enemy[3]-1) % 12
        elif (self.enemy[4] > 0) and (self.enemy[4] < 6): self.enemy[4] = (self.enemy[4]-1) % 12
        elif (self.enemy[4] > 5): self.enemy[4] = (self.enemy[4]+1) % 12 
        elif ((self.enemy[2] < (21<<16))): self.manuver = Pilot.FLEE
    
    @micropython.native    
    def do_circle(self):
        if (self.enemy[3] > 8): self.enemy[3] = (self.enemy[3]+1) % 12 
        elif (self.enemy[3] < 9) and (self.enemy[3] > 6): self.enemy[3] = (self.enemy[3]-1) % 12
        elif (self.enemy[3] < 6) and (self.enemy[3] > 0): self.enemy[3] = (self.enemy[3]-1) % 12
        else: self.manuver = Pilot.NONE
    
    @micropython.native    
    def do_flee(self):
        self.enemy[5] = 20<<16
        if (self.target_x == 0): self.target_x = 3 #randint(2,4)
        #if (self.target_y == 0): self.target_y = choice([1,2,10,11])
        if (self.target_d == 0): self.target_d = choice([-1,1])
        if (self.enemy[3] != self.target_x): self.enemy[3] = (self.enemy[3]+self.target_d) % 12 
        elif (self.enemy[4] != self.target_y): self.enemy[4] = (self.enemy[4]+self.target_d) % 12
        elif (self.enemy[2] > (45<<16)): 
            self.manuver = choice
            self.enemy[5] = randint(6<<16,12<<16)
            self.target_x = self.target_y = self.target_d = 0
    
    @micropython.native    
    def do_crazyivan(self):
        if (self.target_x == 0): self.target_x = randint(1,11)
        if (self.target_y == 0): self.target_y = randint(1,11)
        if (self.target_d == 0): self.target_d = choice([-1,1])
        if (self.enemy[3] != self.target_x): self.enemy[3] = (self.enemy[3]+self.target_d) % 12 
        elif (self.enemy[4] != self.target_y): self.enemy[4] = (self.enemy[4]+self.target_d) % 12
        else: 
            self.manuver = Pilot.NONE
            self.target_x = self.target_y = self.target_d = 0
    
class Ship:
    def __init__(self):
        self.cockpit_sprite = Sprite(66,18,(cockpit,cockpitSHD),SHIP_X,SHIP_Y,1)
        self.target_sprite = Sprite(7,7,(target,targetSHD),CENTER_X-3, CENTER_Y-3,0)
        self.radar_sprite = Sprite(15,15,(radar,radarSHD),57,0,0)
        self.laser = []
        self.fire_couter = 0
        self.laser_energy = 5
        self.last_time = 0
        self.afterburner_time = 0
        display.setFont("/lib/font3x5.bin", 3, 5, 1)
    
    @micropython.native
    def run(self):
        global hudShip
        for laser in self.laser:
            if laser.run(): self.laser.remove(laser)
            
        display.drawSprite(self.cockpit_sprite)
        display.drawSprite(self.target_sprite)
        display.drawSprite(self.radar_sprite)
        display.setPixel(CENTER_X+(player_angle[0]>>16),1,1)
        display.setPixel(CENTER_X+(player_angle[0]>>16),2,3)
        display.setPixel(1,CENTER_Y+((player_angle[1]>>16)//2),1)
        display.setPixel(2,CENTER_Y+((player_angle[1]>>16)//2),3)
        
        for i in range(lifes):
            display.drawFilledRectangle(self.cockpit_sprite.x+19, self.cockpit_sprite.y+15-i*2, 2, 2, 1)
        for i in range(self.laser_energy):
            display.drawFilledRectangle(self.cockpit_sprite.x+45, self.cockpit_sprite.y+15-i*2, 2, 2, 1)
        if hudShip != None:
            hudShip.setScale(12000)
            hudShip.key = -1
            hudShip.x = self.cockpit_sprite.x + 27
            hudShip.y = self.cockpit_sprite.y + 8
            display.drawSpriteWithScale(hudShip)
            for i in range(hudShip.getLifes()):
                display.drawFilledRectangle(self.cockpit_sprite.x+40, self.cockpit_sprite.y+15-i*2, 2, 2, 1)
        else:
            display.drawText(f"{score:02d}", self.cockpit_sprite.x+30,self.cockpit_sprite.y+8, 1)
    
    @micropython.native
    def move_me(self, enemies):
        global player_angle, player_speed, player_target_speed, hudShip
        # ticks in ms passed since last call for body inertia calaculation
        new_time = ticks_us()
        t = (int(ticks_diff(new_time, self.last_time,))<<16)//1000000
        self.last_time = new_time
        
        if eval("button" + chr(KEYMAPS[KEY_SHIFT])).pressed():
            if eval("button" + chr(KEYMAPS[KEY_TARGET_NEXT])).justPressed():
                if enemies:
                    for i in range(len(enemies)):
                        e = enemies[i]
                        if e[8] == 1:
                            e[8] = 0
                            if (i+1) < len(enemies): enemies[i+1][8] = 1
                            else: hudShip = None
                            break
                    else:
                        if enemies[0] != None: enemies[0][8] = 1
            elif eval("button" + chr(KEYMAPS[KEY_TARGET_PREV])).justPressed():
                if enemies:
                    for i in range(len(enemies) -1, -1, -1):
                        e = enemies[i]
                        if e[8] == 1:
                            e[8] = 0
                            if ((i-1) > -1): enemies[i-1][8] = 1
                            else: hudShip = None
                            break
                    else:
                        if enemies[0] != None: enemies[len(enemies) -1][8] = 1
            elif eval("button" + chr(KEYMAPS[KEY_AFTERBURNER])).justPressed() and (self.afterburner_time == 0):
                player_target_speed = 7<<16;
                self.afterburner_time = new_time
            elif eval("button" + chr(KEYMAPS[KEY_BREAK])).justPressed():
                player_speed = 1<<16
        elif eval("button" + chr(KEYMAPS[KEY_MOVE_RIGHT])).pressed():
            player_angle[0] -= 1<<16
            player_angle[2] = -3
            self.cockpit_sprite.x = SHIP_X-1
        elif eval("button" + chr(KEYMAPS[KEY_MOVE_LEFT])).pressed():
            player_angle[0] += 1<<16
            player_angle[2] = 3
            self.cockpit_sprite.x = SHIP_X+1
        elif eval("button" + chr(KEYMAPS[KEY_MOVE_DOWN])).pressed():
            player_angle[1] -= 1<<16
            self.cockpit_sprite.y = SHIP_Y-1
        elif eval("button" + chr(KEYMAPS[KEY_MOVE_UP])).pressed():
            player_angle[1] += 1<<16
            self.cockpit_sprite.y = SHIP_Y+1
        elif eval("button" + chr(KEYMAPS[KEY_FIRE])).justPressed():
            if (self.laser_energy > 0):
                self.laser.append(Laser(player_angle[0], player_angle[1]))
                self.target_sprite = Sprite(7,7,(targetactive,targetactiveSHD),CENTER_X-3, CENTER_Y-3,0)
                self.fire_couter += 20
                self.laser_energy -= 1
        else:
            player_angle[2] = 0
            self.cockpit_sprite.x = SHIP_X
            self.cockpit_sprite.y = SHIP_Y

        if self.fire_couter == -1:
            self.target_sprite = Sprite(7,7,(target,targetSHD),CENTER_X-3, CENTER_Y-3,0)
            self.fire_couter = 0
            self.laser_energy += 1
            if (self.laser_energy > 5): self.laser_energy = 5
        else:
            self.fire_couter -= 1
            
        if player_angle[0] < -2293760: player_angle[0] = -2293760
        if player_angle[0] > 2293760: player_angle[0] = 2293760
        if player_angle[1] < -2162688: player_angle[1] = -2162688
        if player_angle[1] > 2162688: player_angle[1] = 2162688
        
        if self.afterburner_time != 0:
            ta = (int(ticks_diff(new_time, self.afterburner_time,))<<16)//1000000
            self.cockpit_sprite.x = SHIP_X + choice([1,0,-1])
            self.cockpit_sprite.y = SHIP_Y + choice([1,0,-1])
            if (ta > 250000):
                self.afterburner_time = 0
                player_target_speed = 1<<16
                
        player_speed = apply_physics(1<<16, player_target_speed, player_speed, t)
        inputJustPressed()
        
    
class Laser:
    def __init__(self,x:int,y:int,z:int=4<<16,vel_x:int=0,vel_y:int=0,vel_z:int=1<<16):
        self.x = x
        self.y = y
        self.z = z
        self.vel_x = vel_x
        self.vel_y = vel_y
        self.vel_z = vel_z
        self.screen_pos_x, self.screen_pos_y = 0,0
    
    @micropython.native    
    def run(self):
        # move in x,y,z-axis forward
        self.x += self.vel_x
        self.y += self.vel_y
        self.z += self.vel_z
        
        if (self.x > (6143<<16)): self.x = -2047<<16
        elif (self.x < -(6143<<16)): self.x = 2047<<16

        if (self.y > (5600<<16)): self.y = -1400<<16
        elif (self.y < -(5600<<16)): self.y = 1400<<16

        if (self.x > (2047<<16)) or (self.x < -(2047<<16)) or (self.y > (1400<<16)) or (self.y < -(1400<<16)):
            pass
        else:
            self.x += (player_angle[0] * player_speed) >> 16
            self.y += (player_angle[1] * player_speed) >> 16
                    
            self.screen_pos_x = project_a(self.x, self.z, CENTER_X, 0)
            self.screen_pos_y = project_a(self.y, self.z, CENTER_Y, 0)
            self.space = fp2int(fpdiv(Z_DISTANCE<<16, fpmul(13107, self.z)))
            self.size = fp2int(fpdiv(Z_DISTANCE<<16, fpmul(52429, self.z)))
            self.draw()
        return (self.z > (60<<16)) or (self.z < 0)
        
    @micropython.native    
    def draw(self):
        display.drawFilledRectangle(self.screen_pos_x-self.space, self.screen_pos_y, self.size, self.size, 1)
        display.drawFilledRectangle(self.screen_pos_x+self.space, self.screen_pos_y, self.size, self.size, 1)


def launch():
    display.fill(0)
    display.update()
    display.setFPS(20)
    launch_sprite = Sprite(74,30,(loc+"start1_74.BIT.bin",loc+"start1_74.SHD.bin"),0,5)
    for i in range(launch_sprite.frameCount):
        launch_sprite.setFrame(i)
        display.drawSprite(launch_sprite)
        display.update()
    display.fill(0) 
    display.update()
    launch_sprite = Sprite(74,30,(loc+"start2_74.BIT.bin",loc+"start2_74.SHD.bin"),0,5)
    for i in range(launch_sprite.frameCount):
        launch_sprite.setFrame(i)
        display.drawSprite(launch_sprite)
        display.update()
    sleep(0.25)
    
def die():
    display.setFPS(6)
    die_sprite = Sprite(74,40,(loc+"medie_74.BIT.bin",loc+"medie_74.SHD.bin"),0,0)
    display.fill(0)
    for i in range(die_sprite.frameCount):
        die_sprite.setFrame(i)
        display.drawSprite(die_sprite)
        display.update()
    
    sleep(0.3) 
    
def home():
    display.setFPS(10)
    home_sprite = Sprite(74,30,(loc+"home_74.BIT.bin",loc+"home_74.SHD.bin"),0,5)
    display.fill(0)
    for i in range(home_sprite.frameCount):
        home_sprite.setFrame(i)
        display.drawSprite(home_sprite)
        display.update()
    
    sleep(0.3) 
 
def game_over():
    display.fill(0)     
    display.setFont("/lib/font8x8.bin", 8, 8, 1)
    display.drawText("GAME",8,5,1)
    display.drawText("OVER",22,12,1)
    display.setFont("/lib/font3x5.bin", 3, 5, 1)
    display.drawText(f"Score: {score:02d}", 18,22,1)
    display.drawText("Press A/B: Restart", 1,32,1)
    display.update()
    sleep(1)
    while not buttonA.pressed() or buttonB.pressed():
        pass

def menu():
    display.setFPS(30)
    display.setFont("/lib/font3x5.bin", 3, 5, 1)
    menu_sprite = Sprite(71,40,(loc+"menu_71.BIT.bin",loc+"menu_71.SHD.bin"),2,0,0)
    background = Stars(20,4,0)
    display.fill(0)
    i = 0
    rot = 5
    sleep(0.5)
    while not buttonA.pressed():
        display.fill(0)
        background.run(rot)
        display.drawSprite(menu_sprite)
        if i==0:
            display.drawText("Asteroid Dodge",10,20,1)
            display.drawText("Dog Fight",21,30,3)
        elif i==1:
            display.drawText("Dog Fight",21,20,1)
            display.drawText("Campaigns",21,30,3)
        elif i==2:
            display.drawText("Campaigns",21,20,1)
            display.drawText("Settings",21,30,3)
        elif i==3:
            display.drawText("Settings",21,20,1)
            display.drawText("Exit Game",21,30,3)
        elif i==4:
            display.drawText("Settings",21,20,3)
            display.drawText("Exit Game",21,30,1)
        display.update()
        if buttonD.justPressed():
            i+=1
            if i > 4: i=4
            rot = -5
        elif buttonU.justPressed():
            i+=-1
            if i < 0: i=0
            rot = 5
    return i

class SettingsMenu:
    def __init__(self):
        self.update_menu()
        self.selected = 0
        self.remapping = False
        self.current_remap = 0  # Now using index instead of string
        self.background = Stars(20, 4, 0)
        display.setFont("/lib/font3x5.bin", 3, 5, 1)
    
    def update_menu(self):
        # Create menu items dynamically from key array
        self.settings_items = [
            "FIRE: " + chr(KEYMAPS[KEY_FIRE]),
            "SHIFT: " + chr(KEYMAPS[KEY_SHIFT]),
            "MOVE LEFT: " + chr(KEYMAPS[KEY_MOVE_LEFT]),
            "MOVE RIGHT: " + chr(KEYMAPS[KEY_MOVE_RIGHT]),
            "MOVE UP: " + chr(KEYMAPS[KEY_MOVE_UP]),
            "MOVE DOWN: " + chr(KEYMAPS[KEY_MOVE_DOWN]),
            "AFTERBURNER: " + chr(KEYMAPS[KEY_SHIFT])+"+"+chr(KEYMAPS[KEY_AFTERBURNER]),
            "BREAK: " + chr(KEYMAPS[KEY_SHIFT])+"+"+chr(KEYMAPS[KEY_BREAK]),
            "TGT NEXT: " + chr(KEYMAPS[KEY_SHIFT])+"+"+chr(KEYMAPS[KEY_TARGET_NEXT]),
            "TGT PREV: " + chr(KEYMAPS[KEY_SHIFT])+"+"+chr(KEYMAPS[KEY_TARGET_PREV]),
            "RESET DEFAULTS",
            "BACK"
        ]
        
    def run(self):
        global KEYMAPS
        display.setFPS(30)
        
        while True:
            display.fill(0)
            self.background.run(0)
            
            # Draw title
            display.drawText("SETTINGS", 22, 2, 1)
            display.drawLine(0, 9, 72, 9, 1)
            
            # If in remapping mode
            if self.remapping:
                display.fill(0)
                # Draw title
                display.drawText("PRESS NEW KEY FOR:", 2, 2, 1)
                display.drawLine(0, 9, 72, 9, 1)
                
                # Show which key is being remapped
                key_names = ["FIRE", "SHIFT", "MOVE LEFT", "MOVE RIGHT", 
                             "MOVE UP", "MOVE DOWN", "AFTERBURNER", 
                             "BREAK", "TARGET NEXT", "TARGET PREV"]
                display.drawText(key_names[self.current_remap], 16, 14, 3)
                display.update()
                
                # Wait for a button press
                while not (buttonA.pressed() or buttonB.pressed() or dpadPressed()):
                    pass
                
                # Determine which button was pressed
                new_key = 0  # Default value
                if buttonA.pressed(): new_key = ord('A')
                elif buttonB.pressed(): new_key = ord('B')
                elif buttonU.pressed(): new_key = ord('U')
                elif buttonD.pressed(): new_key = ord('D')
                elif buttonL.pressed(): new_key = ord('L')
                elif buttonR.pressed(): new_key = ord('R')
                
                # Update mapping if valid
                if new_key != 0:
                    KEYMAPS[self.current_remap] = new_key
                    self.update_menu()
                    
                # Wait for button release
                sleep(0.3)
                inputJustPressed()
                    
                self.remapping = False
                sleep(0.3)
                continue
            
            # Draw menu items
            start_idx = max(0, min(self.selected - 2, len(self.settings_items) - 5))
            for i in range(start_idx, min(start_idx + 5, len(self.settings_items))):
                y_pos = 12 + (i - start_idx) * 6
                text_color = 1 if i == self.selected else 3
                display.drawText(self.settings_items[i], 4, y_pos, text_color)
            
            # Draw scrollbar if needed
            if len(self.settings_items) > 5:
                scrollbar_height = min(35, 35 * 5 / len(self.settings_items))
                scrollbar_pos = 12 + (35 - scrollbar_height) * self.selected / (len(self.settings_items) - 1)
                display.drawFilledRectangle(70, int(scrollbar_pos), 2, int(scrollbar_height), 1)
            
            display.update()
            
            # Handle input
            if buttonU.justPressed():
                self.selected = (self.selected - 1) % len(self.settings_items)
                sleep(0.15)
            elif buttonD.justPressed():
                self.selected = (self.selected + 1) % len(self.settings_items)
                sleep(0.15)
            elif buttonA.justPressed():
                # Handle selection
                if self.selected < 10:  # Key remapping options
                    self.remapping = True
                    # Set current_remap to the index value instead of string
                    self.current_remap = self.selected
                elif self.selected == 10:  # Reset defaults
                    # Reset to default values
                    KEYMAPS = array('B', DEFAULT_KEYS)
                    # Update menu text
                    self.update_menu()
                    sleep(0.3)
                elif self.selected == 11:  # Back
                    save_keymaps(KEYMAPS)
                    return
                sleep(0.15)
            elif buttonB.justPressed():
                # Go back
                save_keymaps(KEYMAPS)
                return

def run_campaign(campaign_engine):
    global lifes, player_speed, player_target_speed, player_angle, score
    
    # Get current mission configuration
    mission_config = campaign_engine.get_mission_config()
    if not mission_config:
        return (0, False)  # Return score and success status
    
    # Get mission objectives
    mission_objectives = campaign_engine.get_mission_objectives()
    
    # Show mission briefing
    campaign_engine.show_mission_briefing(mission_config)
    
    # Reset game state
    lifes = 5
    player_speed = player_target_speed = float2fp(1)
    player_angle = [0, 0, 0]
    score = 0
    
    # Launch sequence
    launch()
    collect()
    display.setFPS(FPS)
    
    # Prepare game objects based on mission type
    stars = Stars(20, 5, 85)
    mission_type = mission_config.get("type", "mixed")
    
    # Create enemies and asteroids based on mission type and difficulty
    difficulty = mission_config.get("difficulty", 1)
    enemy_count = mission_config.get("enemies", 0)
    asteroid_count = mission_config.get("asteroids", 0)
    
    # Scale difficulty
    enemy_health = min(5, 3 + difficulty // 2)
    enemy_speed = 6554 + (difficulty * 1000)
    
    if mission_type == "dogfight" or mission_type == "mixed":
        enemies = Enemies(max(1, enemy_count))
        # Increase enemy health based on difficulty
        for enemy in enemies.enemies:
            enemy[7] = enemy_health  # Increase health
            enemy[5] = enemy_speed   # Increase speed
    else:
        enemies = None
    
    if mission_type == "asteroids" or mission_type == "mixed":
        astroids = Astroids(max(5, asteroid_count + (difficulty * 2)))
    else:
        astroids = None
    
    ship = Ship()
    
    # Initialize mission variables
    mission_start_time = ticks_ms()
    mission_duration = 0
    kills_needed = mission_objectives.get("kills", 0)
    survive_time = mission_objectives.get("survive_time", 0) * 1000  # Convert to ms
    has_time_objective = survive_time > 0
    has_kill_objective = kills_needed > 0
    total_kills = 0  # Track total kills across the mission
    mission_phase_complete = False
    mission_successful = False
    display.setFont("/lib/font3x5.bin", 3, 5, 1)
    
    # Main mission loop
    while lifes > 0:
        display.fill(0)
        
        # Check mission objectives
        current_time = ticks_ms()
        mission_duration = ticks_diff(current_time, mission_start_time)
        
        # Check if we've met the objectives
        time_objective_met = has_time_objective and mission_duration >= survive_time
        kill_objective_met = has_kill_objective and total_kills >= kills_needed
        
        # If both objectives are specified, both must be completed
        if has_time_objective and has_kill_objective:
            mission_phase_complete = time_objective_met and kill_objective_met
        # If only one objective is specified, just check that one
        elif has_time_objective:
            mission_phase_complete = time_objective_met
        elif has_kill_objective:
            mission_phase_complete = kill_objective_met
        
        # Exit mission if successful
        if mission_phase_complete:
            if enemies and len(enemies.enemies) > 0:
                pass
            elif astroids and len(astroids.astroids) > 0:
                pass    
            else:
                mission_successful = True
                break
        
        # Save current score to detect kills
        previous_score = score
        
        # Move player
        if enemies:
            ship.move_me(enemies.enemies)
        else:
            ship.move_me(None)
        
        # Update stars
        stars.run(player_angle[2])
  
        if enemies:
            enemies.run(ship.laser, mission_phase_complete)
        if astroids:
            astroids.run(ship.laser, mission_phase_complete)
        
        # Track kills by checking score difference
        # The score increases when enemies or asteroids are destroyed
        if score > previous_score:
            new_kills = score - previous_score
            total_kills += new_kills
        
        # Draw ship
        ship.run()
        
        # Draw mission objectives
        progress = ""
        if mission_phase_complete:
            progress += " CLEAR"
        else:
            if kills_needed > 0:
                progress = f"{total_kills}/{kills_needed}"
                progress += " *" if kill_objective_met else ""
            if survive_time > 0:
                time_remaining = max(0, (survive_time - mission_duration) // 1000)
                progress += f"  {time_remaining}s"
        display.drawText(f"STAT: {progress}", 2, 2, 1)
        display.update()
    
    # Mission ended - either player died or objectives completed
    if mission_successful:
        # Play success sequence
        home()
        display.setFPS(FPS)
        collect()
        campaign_engine.show_mission_success()
    else:
        # Player died - play death sequence
        die()
        collect()
    
    # Return mission score and success status
    return (score, mission_successful)
    
#Intro finished
Intro.finish()

while True:
    lifes = 5
    player_speed = player_target_speed = float2fp(1)
    player_angle = [0, 0, 0]
    score = 0
    # Show the Menu
    game = menu()
    
    inputJustPressed()
    if (game == 0):
        # show launch sequence
        launch()
        collect()
        display.setFPS(FPS)
        stars = Stars(20,5)
        astroids = Astroids(12)
        ship = Ship()
        hudShip = None
        while lifes > 0:
            display.fill(0)
            ship.move_me(None)
            stars.run(player_angle[2])
            astroids.run(ship.laser)
            ship.run()
            display.update()
        die()
        game_over()
    elif (game ==1):
        launch()
        collect()
        display.setFPS(FPS)
        stars = Stars(20,5,85)
        enemies = Enemies(3)
        ship = Ship()
        hudShip = None
        while lifes > 0:
            display.fill(0)
            ship.move_me(enemies.enemies)
            stars.run(player_angle[2])
            enemies.run(ship.laser)
            ship.run()
            display.update()
        die()    
        game_over()
    elif (game == 2):  # Campaigns
        campaign_engine = CampaignEngine()
        campaign = campaign_engine.run_campaign_menu(Stars(20,4,0))
        
        if campaign:
            current_mission_attempt = 0
            max_attempts = 3  # Maximum number of attempts per mission
            
            while True:
                # Run current mission and get score and success status
                hudShip = None
                mission_result = run_campaign(campaign)
                mission_score = mission_result[0]
                mission_success = mission_result[1]
                
                if mission_success:
                    # Mission successful, show debriefing and advance
                    action = campaign.run_post_mission_menu(mission_score)
                    current_mission_attempt = 0  # Reset attempt counter
                    
                    if action == "complete" or action == "exit":
                        break
                else:
                    # Mission failed
                    current_mission_attempt += 1
                    
                    if current_mission_attempt >= max_attempts:
                        # Too many failures, return to main menu
                        display.fill(0)
                        display.setFont("/lib/font5x7.bin", 5, 7, 1)
                        display.drawText("MISSION", 15, 10, 1)
                        display.drawText("FAILED", 18, 20, 1)
                        display.update()
                        sleep(2)
                        
                        display.setFont("/lib/font3x5.bin", 3, 5, 1)
                        display.fill(0)
                        display.drawText("Too many attempts.", 2, 10, 1)
                        display.drawText("Returning to menu.", 2, 20, 1)
                        display.update()
                        sleep(2)
                        break
                    else:
                        # Retry the mission
                        display.fill(0)
                        display.setFont("/lib/font5x7.bin", 5, 7, 1)
                        display.drawText("MISSION", 15, 10, 1)
                        display.drawText("FAILED", 18, 20, 1)
                        display.update()
                        sleep(1)
                        
                        display.setFont("/lib/font3x5.bin", 3, 5, 1)
                        display.fill(0)
                        display.drawText(f"Attempt {current_mission_attempt} of {max_attempts}", 2, 10, 1)
                        display.drawText("Press A to retry", 2, 20, 1)
                        display.update()
                        
                        # Wait for button press
                        while not buttonA.justPressed():
                            pass
                        sleep(0.2)
        
    elif (game == 3):  # Settings (was previously 2)
        settings = SettingsMenu()
        settings.run()
    else:  # Exit (was previously 3)
        reset()
