# ThumbCommander.py - Complete updated version with dynamic resolution support
from sys import path
from time import sleep
loc = "/Games/ThumbCommander/"
path.insert(0, '/Games/ThumbCommander')

from platform_loader import display, IS_THUMBY_COLOR, Sprite, PC, create_sprite, play_cutscene_animation, create_cancel_callback, audio_load, audio_play, audio_stop, audio_set_loop, audio_set_volume, audio_get_position, rumble, buttonA, buttonB, buttonU, buttonD, buttonL, buttonR, buttonLB, buttonRB, buttonMENU, dpadPressed, inputJustPressed
display.enableGrayscale()

from fpmath import int2fp, fp2int, fp2float, float2fp, fpmul, fpdiv, project, fpsin, fpcos, rotate_z_x, rotate_z_y, sign, sort_by_z, apply_physics

# Set platform-appropriate frequency
if not IS_THUMBY_COLOR:
    from machine import freq
    freq(200_000_000)
    hud_fb = None
    # Show intro while loading
    import Intro
    Intro.__init__()
    Intro.start()
else:
    from engine import freq
    from framebuf import FrameBuffer, RGB565
    hud_buffer = bytearray(24 * 24 * 2)
    hud_fb = FrameBuffer(hud_buffer, 24, 24, RGB565)
    freq(300_000_000)
    play_cutscene_animation(loc+"intro_128_80.COL.bin", 21, create_cancel_callback())

# Sprites - using platform-aware loading
OBJECTS = [None, None, None, None]

# Load sprites with platform-appropriate versions
OBJECTS[0] = create_sprite(56, 54, (loc+"explode_56_54.BIT.bin", loc+"explode_56_54.SHD.bin"), 0, 0, 0)
OBJECTS[1] = create_sprite(56, 47, (loc+"astroid1_56_47.BIT.bin", loc+"astroid1_56_47.SHD.bin"), 0, 0, 0)
OBJECTS[2] = create_sprite(56, 47, (loc+"astroid2_56_47.BIT.bin", loc+"astroid2_56_47.SHD.bin"), 0, 0, 0)
OBJECTS[3] = create_sprite(70, 59, (loc+"enemy1_70_59.BIT.bin", loc+"enemy1_70_59.SHD.bin"), 0, 0, 0)

# Import game modules
from thumbyHardware import reset
from random import randint, randrange, choice
from time import sleep
from utime import ticks_us, ticks_ms, ticks_diff
from array import array
from gc import collect, mem_free
import json
from campaign_engine import CampaignEngine

# Game constants
ORIENTATION = [-512,-427,-341,-256,-171,-85,0,85,171,256,341,427,512]
X_INDEX = [24,25,26,27,26,25,24,23,22,21,22,23,24]
X_MIRROR = [False,False,False,False,True,True,True,True,True,False,False,False,False]
Y_SHIFT = [0,-7,-14,-21,-14,-7,0,7,14,21,14,7,0]
Y_MIRROR = [True,False,False,False,False,False,True,True,True,True,True,True,True]
ASTROIDS = [1, 2]
SHIPS = [3]

# Player properties
player_speed = 65536
player_target_speed = 65536
lifes = 5
player_angle = [0, 0, 0]
score = 0
hudShip = None

DEFAULT_KEYS = array('O', ['A','B','L','R','D','U','U','D','RB' if IS_THUMBY_COLOR else 'R','LB' if IS_THUMBY_COLOR else 'L','A'])
SHIFT_REQUIRED = array('B', [False,False,False,False,False,False,True,True,not IS_THUMBY_COLOR,not IS_THUMBY_COLOR,True])

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
KEY_EJECT = const(10)

# Helper functions
def copySprite(obj:Sprite):
    if (IS_THUMBY_COLOR):
        newSprite = Sprite(obj.width, obj.height,obj.frame_data,0,0,obj.key,obj.mirrorX,obj.mirrorY)
    else:
        newSprite = Sprite(obj.width, obj.height,(bytearray(obj.bitmapByteCount), bytearray(obj.bitmapByteCount)),0,0,obj.key,obj.mirrorX,obj.mirrorY)
        newSprite.bitmap[0][:] = obj.bitmap[0]
        newSprite.bitmap[1][:] = obj.bitmap[1]
        newSprite.setFrame(obj.currentFrame)
    return newSprite

@micropython.native
def getSprite(z, shape):
    OBJECTS[shape].setScale(fpdiv((71<<16)-abs(z), 60<<16))
    return OBJECTS[shape]

def button_exists(button) -> bool:
    try:
        button_name = "button" + button
        return bool(button_name in globals())
    except:
        return False

def load_keymaps():
    global SHIFT_REQUIRED
    try:
        with open(loc + "keymap.json", "r") as f:
            loaded_keys = json.loads(f.read())
            complete_keys = array('O', DEFAULT_KEYS)
            
            if "FIRE" in loaded_keys and button_exists(loaded_keys["FIRE"]):
                complete_keys[KEY_FIRE] = loaded_keys["FIRE"]
            if "SHIFT" in loaded_keys and button_exists(loaded_keys["SHIFT"]):
                complete_keys[KEY_SHIFT] = loaded_keys["SHIFT"]
            if "MOVE_LEFT" in loaded_keys and button_exists(loaded_keys["MOVE_LEFT"]):
                complete_keys[KEY_MOVE_LEFT] = loaded_keys["MOVE_LEFT"]
            if "MOVE_RIGHT" in loaded_keys and button_exists(loaded_keys["MOVE_RIGHT"]):
                complete_keys[KEY_MOVE_RIGHT] = loaded_keys["MOVE_RIGHT"]
            if "MOVE_UP" in loaded_keys and button_exists(loaded_keys["MOVE_UP"]):
                complete_keys[KEY_MOVE_UP] = loaded_keys["MOVE_UP"]
            if "MOVE_DOWN" in loaded_keys and button_exists(loaded_keys["MOVE_DOWN"]):
                complete_keys[KEY_MOVE_DOWN] = loaded_keys["MOVE_DOWN"]
            if "AFTERBURNER" in loaded_keys and button_exists(loaded_keys["AFTERBURNER"]):
                complete_keys[KEY_AFTERBURNER] = loaded_keys["AFTERBURNER"]
            if "BREAK" in loaded_keys and button_exists(loaded_keys["BREAK"]):
                complete_keys[KEY_BREAK] = loaded_keys["BREAK"]
            if "TARGET_NEXT" in loaded_keys and button_exists(loaded_keys["TARGET_NEXT"]):
                complete_keys[KEY_TARGET_NEXT] = loaded_keys["TARGET_NEXT"]
            if "TARGET_PREV" in loaded_keys and button_exists(loaded_keys["TARGET_PREV"]):
                complete_keys[KEY_TARGET_PREV] = loaded_keys["TARGET_PREV"]
            if "EJECT" in loaded_keys and button_exists(loaded_keys["EJECT"]):
                complete_keys[KEY_EJECT] = loaded_keys["EJECT"]
            if "SHIFT_REQ" in loaded_keys and len(loaded_keys["SHIFT_REQ"]) == 11:
                SHIFT_REQUIRED = array('B', loaded_keys["SHIFT_REQ"])
              
            return complete_keys
    except:
        return array('O', DEFAULT_KEYS)

def save_keymaps(keymap):
    try:
        keymap_dict = {
            "FIRE": keymap[KEY_FIRE],
            "SHIFT": keymap[KEY_SHIFT],
            "MOVE_LEFT": keymap[KEY_MOVE_LEFT],
            "MOVE_RIGHT": keymap[KEY_MOVE_RIGHT], 
            "MOVE_UP": keymap[KEY_MOVE_UP],
            "MOVE_DOWN": keymap[KEY_MOVE_DOWN],
            "AFTERBURNER": keymap[KEY_AFTERBURNER],
            "BREAK": keymap[KEY_BREAK],
            "TARGET_NEXT": keymap[KEY_TARGET_NEXT],
            "TARGET_PREV": keymap[KEY_TARGET_PREV],
            "EJECT": keymap[KEY_EJECT],
            "SHIFT_REQ": list(SHIFT_REQUIRED)  # Save shift requirements
        }
        with open(loc + "keymap.json", "w") as f:
            f.write(json.dumps(keymap_dict))
    except:
        pass

# Global variable to store key mappings
KEYMAPS = load_keymaps()

# Game classes
class Stars:
    def __init__(self, num=None, scale_pos=4, stable=80):
        if num is None:
            num = PC.STAR_COUNT
        stars = array('O', [None] * num)
        for i in range(num):
            speed = 0 if (randint(0,100) <= stable) else randint(42598, 62258)
            if speed != 0:
                angle = randint(0, 4096)
                radius = int2fp(randint(PC.WIDTH // scale_pos, PC.WIDTH*2) * scale_pos)
                stars[i] = array('l', [fpmul(radius, fpcos(angle)),
                          fpmul(radius, fpsin(angle)),
                          randint(5, PC.Z_DISTANCE)<<16,
                          choice(PC.STARCOLORS),
                          speed])
            else:
                stars[i] = array('l', [randint(-200*PC.SCREEN_SCALE,200*PC.SCREEN_SCALE)<<16,
                          randint(-200*PC.SCREEN_SCALE,200*PC.SCREEN_SCALE)<<16,
                          7<<16,
                          choice(PC.STARCOLORS),
                          0])    
        self.stars = stars
        self.scale = scale_pos

    @micropython.native
    def run(self, angle=0):
        global player_speed

        for s in self.stars:
            x = project(s[0], s[2], PC.CENTER_X,0)
            y = project(s[1], s[2], PC.CENTER_Y,0)
            size = 1 if s[4] == 0 else fp2int(fpdiv(PC.Z_DISTANCE<<16, fpmul(72090, s[2])))
  
            if (-size < x < PC.WIDTH + size) and (-size < y < PC.HEIGHT + size):
                display.drawFilledRectangle(x, y, size, size, s[3])
            
            # move forward
            if s[4] == 0:
                for c in range(2):
                    s[c] += player_angle[c] + (player_speed-65536)
                    if (s[c] > (PC.SPACE_STARS<<16)) or (s[c] < -(PC.SPACE_STARS<<16)): 
                        s[c] = -s[c]
            s[2]  -= fpmul(s[4], player_speed)
            
            # Rotate around z-axis
            if angle != 0:
                s[0] = rotate_z_x(s[0], s[1], angle)
                s[1] = rotate_z_y(s[0], s[1], angle)
         
            if s[2] < (1<<16):
                a = randint(0, 4096)
                radius = int2fp(randint(PC.WIDTH // self.scale, PC.WIDTH*2) * self.scale)
                s[0] = fpmul(radius, fpcos(a))
                s[1] = fpmul(radius, fpsin(a))
                s[2] = PC.Z_DISTANCE<<16

class Astroids:
    def __init__(self, num=5):
        astroids = list([None] * num)
        for i in range(num):
            astroids[i] = self.new_astroid()
        self.astroids = astroids
     
    @micropython.native
    def new_astroid(self):
        a = array('l', [randrange(-PC.SPACE_WIDTH<<16, PC.SPACE_WIDTH<<16),      #0: x
                          randrange(-PC.SPACE_HEIGHT<<16, PC.SPACE_HEIGHT<<16),    #1: y
                          60<<16,                            #2: z
                          randint(-655360,655360),           #3: x-velocity
                          randint(-655360,655360),           #4: y-velocity
                          randint(6554, 13107),              #5: z-velocity
                          choice(ASTROIDS),                  #6: sprite_shape
                          randint(2, 4),                     #7: rotationspeed
                          0])                                #8: step
        return a
        
    @micropython.native
    def _update_astroid(self, a):
        """Update asteroid position and return screen coordinates"""
        for c in range(2):
            if (a[c] > (PC.SPACE_WIDTH<<16)) or (a[c] < -(PC.SPACE_WIDTH<<16)):
                a[c+3] = -a[c+3]
            a[c] += a[c+3]
            a[c] += player_angle[c] + (player_speed-65536)
        a[2] -= fpmul(a[5], player_speed)
        if player_angle[2] != 0:
            a[0] = rotate_z_x(a[0], a[1], player_angle[2])
            a[1] = rotate_z_y(a[0], a[1], player_angle[2])

    @micropython.native
    def _check_laser_hit(self, a, x, y, sw, sh, laser, fx):
        """Check laser collision with asteroid, return True if hit"""
        global score, player_speed
        for l in range(len(laser)):
            if (abs(laser[l].z-a[2]) < (2<<16)) and (0 < (laser[l].screen_pos_x-x) < (sw - (sw >> 2))) and (0 < (laser[l].screen_pos_y-y) < (sh - (sh >> 2))):
                del laser[l]
                score += 1
                player_speed += 1311
                a[3] = a[4] = a[5] = a[6] = a[8] = 0
                a[7] = 3
                if fx: fx.play(FXEngine.EXPLODE_AS)
                return True
        return False

    @micropython.native
    def run(self, laser=[], fx=None, mission_phase_complete=False):
        global lifes
        sort_by_z(self.astroids)

        i = 0
        while i < len(self.astroids):
            a = self.astroids[i]
            self._update_astroid(a)
            mySprite = getSprite(a[2], a[6])
            x = project(a[0], a[2], PC.CENTER_X, mySprite.scaledWidth)
            y = project(a[1], a[2], PC.CENTER_Y, mySprite.scaledHeight)

            # Collision with player
            if a[2] < (8<<16):
                if (-28 < x < PC.WIDTH) and (-20 < y < PC.HEIGHT):
                    lifes -= 1
                    display.drawFilledRectangle(0, 0, PC.WIDTH, PC.HEIGHT, PC.HIT_COLOR)
                    if rumble: rumble(200)
                    if fx: fx.play(FXEngine.SHIELD)
                if not mission_phase_complete:
                    self.astroids[i] = self.new_astroid()
                else:
                    self.astroids.pop(i)
                    continue
                i += 1
                continue

            # Rotate sprite animation
            n = a[8] // a[7]
            if n > 12:
                n = 0
                a[8] = 0
            else:
                a[8] += 1
            mySprite.setFrame(n)
            mySprite.x = x
            mySprite.y = y
            display.drawSpriteWithScale(mySprite)

            # Explosion done - respawn
            if a[6] == 0:
                if n == 6:
                    if not mission_phase_complete:
                        self.astroids[i] = self.new_astroid()
                    else:
                        self.astroids.pop(i)
                        continue
            else:
                self._check_laser_hit(a, x, y, mySprite.scaledWidth, mySprite.scaledHeight, laser, fx)
            i += 1

class Enemies:
    def __init__(self, num=1):
        enemies = list([None] * num)
        for i in range(num):
            enemies[i] = self.new_enemy()
        
        # Create shield sprite with platform awareness
        self.shieldSprite = create_sprite(70, 70, (loc+"shield_70_70.BIT.bin", loc+"shield_70_70.SHD.bin"), 0, 0, 0)
        
        self.enemies = enemies
        self.last_time = 0
     
    @micropython.native
    def new_enemy(self):
        e = array('O', [randrange(-PC.SPACE_WIDTH<<16, PC.SPACE_WIDTH<<16),      #0: x
                        randrange(-PC.SPACE_HEIGHT<<16, PC.SPACE_HEIGHT<<16),    #1: y
                        45<<16,                            #2: z
                        randrange(0, 12),                  #3: x-orientation (0:-180, 6:0, 12:+180)
                        randrange(0, 12),                  #4: y-orientation (0:-180, 6:0, 12:+180)
                        randint(6<<16,12<<16),             #5: thrust
                        choice(SHIPS),                     #6: sprite_shape
                        5,                                 #7: health
                        0,                                 #8: selected
                        [],                                #9: Laser
                        None,                             #10: Pilot
                        0,                                #11: x-acceleration
                        0,                                #12: y-acceleration
                        0,                                #13: z-acceleration
                        True])                            #14: visible
        e[10] = Pilot(e)
        e[11] = ((e[5] + (60<<16) - abs(e[2])) * fpcos(ORIENTATION[e[3]]))>>16
        e[12] = ((e[5] + (60<<16) - abs(e[2])) * (fpsin(ORIENTATION[e[3]]) * fpsin(ORIENTATION[e[4]]))) >> 32
        e[13] = (e[5] * (fpsin(ORIENTATION[e[3]]) * fpcos(ORIENTATION[e[4]]))) >> 38
        return e
        
    @micropython.native
    def _update_enemy_position(self, e, t, z_old):
        """Update enemy position, physics, and boundaries"""
        for c in range(2):
            e[c] += player_angle[c] + (player_speed-65536)
        e[2] -= fpmul(2048, player_speed)

        if e[6] != 0:
            e[11] = apply_physics(4<<16,((e[5] + (60<<16) - abs(e[2])) * fpcos(ORIENTATION[e[3]]))>>16, e[11],t)
            e[12] = apply_physics(4<<16,((e[5] + (60<<16) - abs(e[2])) * (fpsin(ORIENTATION[e[3]]) * fpsin(ORIENTATION[e[4]]))) >> 32, e[12], t)
            e[13] = apply_physics(4<<16,(e[5] * (fpsin(ORIENTATION[e[3]]) * fpcos(ORIENTATION[e[4]]))) >> 38, e[13], t)
            e[0] += e[11]
            e[1] += e[12]
            e[2] += e[13]

        if player_angle[2] != 0:
            e[0] = rotate_z_x(e[0], e[1], player_angle[2])
            e[1] = rotate_z_y(e[0], e[1], player_angle[2])

        if (e[0] > (PC.SPACE_WIDTH*3<<16)): e[0] = -(PC.SPACE_WIDTH<<16)
        elif (e[0] < -(PC.SPACE_WIDTH*3<<16)): e[0] = PC.SPACE_WIDTH<<16
        if (e[1] > (PC.SPACE_HEIGHT*3<<16)): e[1] = -(PC.SPACE_HEIGHT<<16)
        elif (e[1] < -(PC.SPACE_HEIGHT*3<<16)): e[1] = PC.SPACE_HEIGHT<<16

        if (z_old > 0) != (e[2] > 0):
            if e[2] <= 0:
                if abs(e[0]) <= (PC.SPACE_WIDTH<<16):
                    e[0] -= (PC.SPACE_WIDTH*2<<16) if e[0] >= 0 else -(PC.SPACE_WIDTH*2<<16)
            else:
                if abs(e[0]) > (PC.SPACE_WIDTH<<16):
                    e[0] -= (PC.SPACE_WIDTH*2<<16) if e[0] >= 0 else -(PC.SPACE_WIDTH*2<<16)
                if abs(e[1]) > (PC.SPACE_HEIGHT<<16):
                    e[1] -= (PC.SPACE_HEIGHT*2<<16) if e[1] >= 0 else -(PC.SPACE_HEIGHT*2<<16)

        e[14] = abs(e[0]) <= (PC.SPACE_WIDTH<<16) and abs(e[1]) <= (PC.SPACE_HEIGHT<<16)
        e[2] = abs(e[2]) if e[14] else -abs(e[2])

        if (e[2] > (70<<16)) or (e[2] < (-70<<16)):
            e[3] = (e[3]+6) % 12
            e[2] += sign(e[2])*(-5<<16)

    @micropython.native
    def _check_enemy_laser_hit(self, e, mySprite, x, y, laser, fx):
        """Check laser collision with enemy, return True if hit"""
        global score
        for l in range(len(laser)):
            if (abs(laser[l].z-e[2]) < (2<<16)) and (laser[l].screen_pos_x > mySprite.x) and (laser[l].screen_pos_x < (mySprite.x+mySprite.scaledWidth)) and (laser[l].screen_pos_y > mySprite.y) and (laser[l].screen_pos_y < (mySprite.y+mySprite.scaledHeight)):
                del laser[l]
                e[7] -= 1
                self.shieldSprite.setScale(fpdiv((71<<16)-abs(e[2]), 60<<16))
                self.shieldSprite.x = x-1
                self.shieldSprite.y = y-1
                display.drawSpriteWithScale(self.shieldSprite)
                if e[7] == -1:
                    score += 1
                    e[5] = e[6] = 0
                    if fx: fx.play(FXEngine.EXPLODE_SH)
                return True
        return False

    @micropython.native
    def _draw_enemy_radar(self, e):
        """Draw enemy on radar"""
        zd = abs(e[2]) + 1
        rd = (zd >> 10) + 1
        rd = (rd + zd//rd) >> 1
        rd = (rd + zd//rd) >> 1
        rd = (rd + zd//rd) >> 1
        ra = ((e[0] * 6554) >> 32) - 256
        x = (((rd << 8) * fpcos(ra))>>32) + 7
        y = (((rd << 8) * fpsin(ra))>>32) + 7
        height = (e[1]>>16) // 700
        color = PC.HUD_SELECT if e[8] == 1 else PC.HUD_UNSELECT
        if IS_THUMBY_COLOR:
            x += 2
            y += 2
            size = 5 if e[8] == 1 else 3
            hud_fb.rect(x,y,size,size,color,True)
            if height < 0:
                hud_fb.rect(x+1,y+height,2,abs(height),color,True)
            else:
                hud_fb.rect(x+1,y,1,abs(height),color,True)
        else:
            x += PC.RADAR_X
            y += PC.RADAR_Y
            display.drawFilledRectangle(x,y,3,3,color)
            if height < 0:
                display.drawFilledRectangle(x+1,y+height,1,abs(height),color)
            else:
                display.drawFilledRectangle(x+1,y,1,abs(height),color)

    @micropython.native
    def _process_enemy_lasers(self, e, fx):
        """Process enemy lasers"""
        global lifes
        for myLaser in e[9]:
            if myLaser.run():
                e[9].remove(myLaser)
            else:
                if 0 < myLaser.z < (8<<16) and (-512<<16 < myLaser.x < 512<<16) and (-300<<16 < myLaser.y < 300<<16):
                    lifes -= 1
                    display.drawFilledRectangle(0,0,PC.WIDTH, PC.HEIGHT, PC.HIT_COLOR)
                    if rumble: rumble(200)
                    if fx: fx.play(FXEngine.SHIELD)
                    e[9].remove(myLaser)

    @micropython.native
    def run(self, laser=[], fx=None, mission_phase_complete=False):
        global hudShip, hud_fb
        new_time = ticks_us()
        t = (ticks_diff(new_time, self.last_time,)<<16)//1000000
        self.last_time = new_time

        if IS_THUMBY_COLOR:
            hud_fb.fill(0)
        sort_by_z(self.enemies)

        i = 0
        while i < len(self.enemies):
            e = self.enemies[i]
            e[14] = True
            z_old = e[2]

            self._update_enemy_position(e, t, z_old)

            if e[14] or e[8] == 1:
                mySprite = getSprite(e[2], e[6])

                if e[6] != 0:
                    mySprite.setFrame(X_INDEX[e[3]] + Y_SHIFT[e[4]])
                    mySprite.mirrorX = X_MIRROR[e[3]]
                    mySprite.mirrorY = Y_MIRROR[e[4]]
                else:
                    mySprite.setFrame(e[5])
                    e[5] += 1

                x, y = 0, 0
                if e[14]:
                    x = project(e[0], e[2], PC.CENTER_X, mySprite.scaledWidth)
                    y = project(e[1], e[2], PC.CENTER_Y, mySprite.scaledHeight)
                    mySprite.x = x
                    mySprite.y = y
                    display.drawSpriteWithScale(mySprite)

                if e[8] == 1:
                    hudShip = copySprite(mySprite)
                    hudShip.setLifes(e[7])
                    if e[14]:
                        display.drawRectangle(x-2, y-2, mySprite.scaledWidth+4, mySprite.scaledHeight+4, PC.HUD_COLOR)

                if e[6] == 0:
                    if e[5] == 6:
                        if not mission_phase_complete:
                            self.enemies[i] = self.new_enemy()
                        else:
                            self.enemies.pop(i)
                            continue
                else:
                    self._check_enemy_laser_hit(e, mySprite, x, y, laser, fx)

            self._draw_enemy_radar(e)
            if e[6] != 0: e[10].run()
            self._process_enemy_lasers(e, fx)
            i += 1

class Pilot:
    _EVADE = ((2,3), (6,9), (10,3), (6,9))

    def __init__(self, enemy):
        self.enemy = enemy
        self.timer = self.state_timer = self.state = self.damage_timer = 0
        self.tx = 3 if enemy[2] > 0 else 9
        self.ty = 6
        self.last_hp = enemy[7]
        self.skill = 39322 + randint(0, 26214)
        self.flank = randint(0, 1)

    @micropython.native
    def _do_state(self, z):
        """Execute state behavior - set target orientation and thrust"""
        e, s, st = self.enemy, self.state, self.state_timer
        if s == 0:  # Patrol
            if st % 20 == 0: self.tx, self.ty = randint(3,9), randint(4,8)
            e[5] = 8<<16
        elif s == 1:  # Intercept
            self.tx, self.ty, e[5] = (3 if z > 0 else 9), 6, 15<<16
        elif s == 2:  # Engage
            self.tx = (5 if self.flank else 7) if z < (18<<16) else 3
            self.ty, e[5] = 6, 14<<16
        elif s == 3:  # Evade
            self.tx, self.ty = Pilot._EVADE[(st // 15) % 4]
            e[5] = 18<<16
        elif s == 4:  # Get behind
            self.tx, self.ty = (6, 5 if self.flank else 7) if z > (20<<16) and abs(e[0]) < (PC.SPACE_WIDTH//2<<16) else (3, 6)
            e[5] = 8<<16 if z <= 0 else 18<<16
        else:  # Chase
            d, xo, yo = abs(z), abs(e[0])>>16, abs(e[1])>>16
            if d < (15<<16): self.tx, e[5] = 3, 6<<16
            elif d > (25<<16): self.tx, e[5] = 9, 14<<16
            else: self.tx, e[5] = ((8 if e[0] > 0 else 10) if xo > (PC.SPACE_WIDTH//4) else 9), 10<<16
            self.ty = (8 if e[1] > 0 else 4) if yo > (PC.SPACE_HEIGHT//4) else 6

    @micropython.native
    def _do_fire(self, z):
        """Check and execute firing"""
        if self.state_timer % 10 != 0: return
        az, s = abs(z), self.state
        if (s == 5 and randint(0,2) < 2) or (s in (1,2) and (10<<16) < az < (35<<16) and randint(0,5) < 3) or (az < (30<<16) and randint(0,20) == 0):
            ef = (1<<16) - self.skill
            e = self.enemy
            e[9].append(Laser(e[0], e[1], e[2], e[11]*2 + fpmul(ef, randint(-32768,32768)), e[12]*2 + fpmul(ef, randint(-32768,32768)), e[13]*4))

    @micropython.native
    def run(self):
        self.timer += 1
        if self.timer < (PC.FPS // 10): return
        self.timer = 0
        self.state_timer += 1
        e, z, st = self.enemy, self.enemy[2], self.state_timer

        # Threat check
        threat = 0
        if e[7] < self.last_hp: threat, self.damage_timer, self.last_hp = 3, 30, e[7]
        elif self.damage_timer > 0: self.damage_timer -= 1; threat = 2
        elif 0 < z < (20<<16): threat = 2

        # State transitions
        old, hp = self.state, e[7]
        if hp < 3 and threat > 1 and old != 3 and st > 10: self.state = 3
        elif z > (8<<16):
            if z > (50<<16): self.state = 1
            elif z > (25<<16) and (old == 0 or st > 50): self.state = 2
            elif old in (1,2) and st > 30: self.state = 4
        elif z <= 0:
            d = abs(z)
            self.state = 1 if d > (30<<16) else (4 if d < (10<<16) else 5)
        if old == 0 and st > 60: self.state = 1
        elif old == 3 and st > 50: self.state = 4 if z > 0 else 5
        elif old == 4 and st > 100: self.state = 2
        if old != self.state: self.state_timer = 0

        self._do_state(z)

        # Turn toward target
        for ax, tgt in ((3, self.tx), (4, self.ty)):
            if e[ax] != tgt: e[ax] = (e[ax] + (1 if (tgt - e[ax] + 6) % 12 > 6 else -1)) % 12

        self._do_fire(z)

class Ship:
    def __init__(self):
        self.cockpit_sprite_x = PC.SHIP_X
        self.cockpit_sprite_y = PC.SHIP_Y
        # Platform-specific cockpit sprite
        if IS_THUMBY_COLOR:
            # Load color versions
            self.cockpit_sprite = loc+"cockpit_118_53.COL.bin"
            self.cockpit_top_sprite = loc+"cockpit_top_118_8.COL.bin"
            self.cockpit_top_sprite_x = PC.SHIP_X
            self.stick_left_sprite = create_sprite(28, 16,loc+"stick_left_28_16.COL.bin", PC.SHIP_X+44, PC.SHIP_Y+37, 0)
            self.stick_right_sprite = create_sprite(28, 16,loc+"stick_right_28_16.COL.bin", PC.SHIP_X+46, PC.SHIP_Y+37, 0)
            self.stick_back_sprite = create_sprite(28, 16,loc+"stick_back_28_16.COL.bin", PC.SHIP_X+45, PC.SHIP_Y+38, 0)
            self.stick_forward_sprite = create_sprite(28, 16,loc+"stick_forward_28_16.COL.bin", PC.SHIP_X+45, PC.SHIP_Y+36, 0)
            self.target_sprite = create_sprite(24, 24, loc+"target_24_24.COL.bin",PC.CENTER_X-12, PC.CENTER_Y-12, 0)
            self.target_active_sprite = create_sprite(24, 24, loc+"targetactive_24_24.COL.bin",PC.CENTER_X-12, PC.CENTER_Y-12, 0)
            self.radar_sprite = create_sprite(24, 24,loc+"radar_24_24.COL.bin", PC.SHIP_X + PC.RADAR_X, PC.SHIP_Y + PC.RADAR_Y, 0)
            self.radar_frame = 0
            self.radar_framecount = self.radar_sprite.frameCount - 1
            self.fx = FXEngine()
        else:
            # Load Grayscale sprites
            self.cockpit_sprite = create_sprite(66, 18, (loc+"cockpit_66_18.BIT.bin", loc+"cockpit_66_18.SHD.bin"), PC.SHIP_X, PC.SHIP_Y, 1)
            self.target_sprite = create_sprite(7, 7, (loc+"target_7_7.BIT.bin", loc+"target_7_7.SHD.bin"), PC.CENTER_X-3, PC.CENTER_Y-3, 0)
            self.target_active_sprite = create_sprite(7, 7, (loc+"targetactive_7_7.BIT.bin", loc+"targetactive_7_7.SHD.bin"), PC.CENTER_X-3, PC.CENTER_Y-3, 0)
            self.radar_sprite = create_sprite(15, 15, (loc+"radar_15_15.BIT.bin", loc+"radar_15_15.SHD.bin"), PC.RADAR_X, PC.RADAR_Y, 0)
            self.fx = None
        
        self.laser = []
        self.fire_time = 0
        self.laser_energy = 5
        self.last_time = 0
        self.afterburner_time = 0
        # Cache button references (avoid repeated eval() calls)
        self._button_states = [eval("button" + KEYMAPS[i]) for i in range(len(KEYMAPS))]
        display.setFont(PC.FONT_FILE, PC.FONT_WIDTH, PC.FONT_HEIGHT, PC.FONT_SPACE)

    @micropython.native
    def _run_hud(self):
        """Draw HUD ship and score"""
        global hudShip
        if hudShip:
            hudShip.setScale(PC.HUD_SCALE)
            hudShip.key = -1
            hudShip.x = self.cockpit_sprite_x + PC.HUD_X
            hudShip.y = self.cockpit_sprite_y + PC.HUD_Y
            display.drawSpriteWithScale(hudShip)
            hl = hudShip.getLifes()
            if IS_THUMBY_COLOR:
                for i in range(hl): display.drawFilledRectangle(hudShip.x + 4 + i*4, hudShip.y + 20, 3, 3, PC.RED)
            else:
                cy = self.cockpit_sprite.y + PC.COCKPIT_HEIGHT - 3
                for i in range(hl): display.drawFilledRectangle(self.cockpit_sprite.x + 40, cy - i*3, 2, 2, PC.WHITE)
        if not hudShip or IS_THUMBY_COLOR:
            display.drawText(f"{score:02d}", self.cockpit_sprite_x + PC.COUNTER_X, self.cockpit_sprite_y + PC.COUNTER_Y, PC.WHITE)

    @micropython.native
    def run(self):
        for laser in self.laser:
            if laser.run(): self.laser.remove(laser)
        if IS_THUMBY_COLOR:
            display.draw_sprite_from_file(self.cockpit_sprite, self.cockpit_sprite_x, self.cockpit_sprite_y, 0)
        else:
            self.cockpit_sprite.x = self.cockpit_sprite_x
            self.cockpit_sprite.y = self.cockpit_sprite_y
            display.drawSprite(self.cockpit_sprite)
        display.drawSprite(self.target_active_sprite if self.laser_energy == 0 else self.target_sprite)
        if IS_THUMBY_COLOR:
            display.draw_sprite_from_file(self.cockpit_top_sprite, self.cockpit_top_sprite_x, 0, 0)
            draw_hull_status(display, lifes)
            draw_half_circle_energy(display, self.cockpit_sprite_x + 59, self.cockpit_sprite_y + 26, 13, self.laser_energy, 5)
            self.radar_sprite.x = self.cockpit_sprite_x + PC.RADAR_X
            self.radar_sprite.y = self.cockpit_sprite_y + PC.RADAR_Y
            self.radar_sprite.setFrame(self.radar_frame)
            self.radar_frame = (self.radar_frame + 1) % self.radar_framecount
            display.drawSprite(self.radar_sprite)
            dx, dy = self.cockpit_sprite_x - PC.SHIP_X, self.cockpit_sprite_y - PC.SHIP_Y
            if dx == 1: display.drawSprite(self.stick_left_sprite)
            elif dx == -1: display.drawSprite(self.stick_right_sprite)
            elif dy == 1: display.drawSprite(self.stick_back_sprite)
            elif dy == -1: display.drawSprite(self.stick_forward_sprite)
            display.internal_fb.blit(hud_fb, self.radar_sprite.x, self.radar_sprite.y, 0)
        else:
            cy = self.cockpit_sprite.y + PC.COCKPIT_HEIGHT - 3
            for i in range(lifes): display.drawFilledRectangle(self.cockpit_sprite.x + 19, cy - i*3, 2, 2, PC.WHITE)
            for i in range(self.laser_energy): display.drawFilledRectangle(self.cockpit_sprite.x + 45, cy - i*3, 2, 2, PC.WHITE)
            display.drawSprite(self.radar_sprite)
        px = PC.CENTER_X + (fpmul(player_angle[0], PC.SPRITE_SCALE)>>16)
        py = PC.CENTER_Y + (fpmul(player_angle[1], PC.SPRITE_SCALE)>>17)
        display.setPixel(px, 1, PC.WHITE); display.setPixel(px, 2, PC.LIGHTGRAY)
        display.setPixel(PC.WIDTH-1, py, PC.WHITE); display.setPixel(PC.WIDTH-2, py, PC.LIGHTGRAY)
        self._run_hud()

    @micropython.native
    def _cycle_target(self, enemies, direction):
        """Cycle through enemy targets. direction: 1=next, -1=prev"""
        global hudShip
        if not enemies: return
        n = len(enemies)
        rng = range(n) if direction == 1 else range(n-1, -1, -1)
        for i in rng:
            if enemies[i][8] == 1:
                enemies[i][8] = 0
                ni = i + direction
                if 0 <= ni < n: enemies[ni][8] = 1
                else: hudShip = None
                return
        if enemies[0]: enemies[n-1 if direction == -1 else 0][8] = 1

    @micropython.native
    def move_me(self, enemies):
        global player_angle, player_speed, player_target_speed
        new_time = ticks_us()
        t = (int(ticks_diff(new_time, self.last_time))<<16)//1000000
        self.last_time = new_time
        b = self._button_states
        sr = SHIFT_REQUIRED
        shift = b[KEY_SHIFT].pressed()
        cx = PC.SHIP_X 
        cy = PC.SHIP_Y

        if b[KEY_TARGET_NEXT].justPressed() and sr[KEY_TARGET_NEXT] == shift: self._cycle_target(enemies, 1)
        elif b[KEY_TARGET_PREV].justPressed() and sr[KEY_TARGET_PREV] == shift: self._cycle_target(enemies, -1)
        elif b[KEY_AFTERBURNER].justPressed() and sr[KEY_AFTERBURNER] == shift and self.afterburner_time == 0:
            player_target_speed = 7<<16; self.afterburner_time = new_time
            if self.fx: self.fx.play(FXEngine.AFTERBURNER)
        elif b[KEY_BREAK].justPressed() and sr[KEY_BREAK] == shift: player_speed = 1<<16
        elif b[KEY_EJECT].pressed() and sr[KEY_EJECT] == shift: return False
        elif b[KEY_MOVE_RIGHT].pressed(): player_angle[0] -= 1<<16; player_angle[2] = -3; cx = PC.SHIP_X-1
        elif b[KEY_MOVE_LEFT].pressed(): player_angle[0] += 1<<16; player_angle[2] = 3; cx = PC.SHIP_X+1
        elif b[KEY_MOVE_DOWN].pressed(): player_angle[1] -= 1<<16; cy = PC.SHIP_Y-1
        elif b[KEY_MOVE_UP].pressed(): player_angle[1] += 1<<16; cy = PC.SHIP_Y+1
        elif b[KEY_FIRE].justPressed() and self.laser_energy > 0:
            self.laser.append(Laser(player_angle[0], player_angle[1]))
            self.fire_time = new_time; self.laser_energy -= 1
            if self.fx: self.fx.play(FXEngine.LASER)
        else: player_angle[2] = 0

        self.cockpit_sprite_x = cx
        self.cockpit_sprite_y = cy

        if ((int(ticks_diff(new_time, self.fire_time))<<16)//1000000) > (1000*PC.FPS):
            if self.laser_energy < 5: self.laser_energy += 1
            self.fire_time = new_time

        player_angle[0] = max(-2293760, min(2293760, player_angle[0]))
        player_angle[1] = max(-2162688, min(2162688, player_angle[1]))
        if self.afterburner_time != 0:
            self.cockpit_sprite_x += choice([1,0,-1])
            self.cockpit_sprite_y += choice([1,0,-1])
            if rumble: rumble(20)
            if ((int(ticks_diff(new_time, self.afterburner_time))<<16)//1000000) > 250000:
                self.afterburner_time = 0; player_target_speed = 1<<16
        player_speed = apply_physics(1<<16, player_target_speed, player_speed, t)
        if IS_THUMBY_COLOR: self.cockpit_top_sprite_x = self.cockpit_sprite_x
        inputJustPressed()
        return True

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
        z_old = self.z
        # move in x,y,z-axis forward
        self.x += self.vel_x
        self.y += self.vel_y
        self.z += self.vel_z
        
        self.x += (player_angle[0] * player_speed) >> 16
        self.y += (player_angle[1] * player_speed) >> 16

        # wrap X,Y at boundaries
        if (self.x > (PC.SPACE_WIDTH*3<<16)): self.x = -(PC.SPACE_WIDTH<<16)
        elif (self.x < -(PC.SPACE_WIDTH*3<<16)): self.x = PC.SPACE_WIDTH<<16
        if (self.y > (PC.SPACE_HEIGHT*4<<16)): self.y = -(PC.SPACE_HEIGHT>>1<<16)
        elif (self.y < -(PC.SPACE_HEIGHT*4<<16)): self.y = PC.SPACE_HEIGHT>>1<<16

        # z crossed → adjust coordinates
        if (z_old > 0) != (self.z > 0):
            if self.z <= 0:  # to back: only X shifts
                if abs(self.x) <= (PC.SPACE_WIDTH<<16):
                    self.x -= (PC.SPACE_WIDTH*2<<16) if self.x >= 0 else -(PC.SPACE_WIDTH*2<<16)
            else:  # to front: X and Y shift if in back
                if abs(self.x) > (PC.SPACE_WIDTH<<16):
                    self.x -= (PC.SPACE_WIDTH*2<<16) if self.x >= 0 else -(PC.SPACE_WIDTH*2<<16)
                if abs(self.y) > (PC.SPACE_HEIGHT<<16):
                    self.y -= (PC.SPACE_HEIGHT*2<<16) if self.y >= 0 else -(PC.SPACE_HEIGHT*2<<16)

        if (self.x > (PC.SPACE_WIDTH<<16)) or (self.x < -(PC.SPACE_WIDTH<<16)) or (self.y > (PC.SPACE_HEIGHT>>1<<16)) or (self.y < -(PC.SPACE_HEIGHT>>1<<16)):
            pass
        else:     
            self.screen_pos_x = project(self.x, self.z, PC.CENTER_X, 0)
            self.screen_pos_y = project(self.y, self.z, PC.CENTER_Y, 0)
            self.space = fp2int(fpdiv(PC.Z_DISTANCE<<16, fpmul(13107, self.z)))
            self.size = fp2int(fpdiv(PC.Z_DISTANCE<<16, fpmul(52429, self.z)))
            self.draw()
        return (self.z > (60<<16)) or (self.z < -(60<<16))
        
    @micropython.native    
    def draw(self):
        display.drawFilledRectangle(self.screen_pos_x-self.space, self.screen_pos_y, self.size, self.size, PC.LASER_COLOR)
        display.drawFilledRectangle(self.screen_pos_x+self.space, self.screen_pos_y, self.size, self.size, PC.LASER_COLOR)

# UI functions  
def launch():
    display.fill(PC.BLACK)
    display.update()
    if IS_THUMBY_COLOR:
        play_cutscene_animation(loc+"start_128_56.COL.bin", 10, create_cancel_callback())
    else:
        play_cutscene_animation(loc+"start1_74_30.BIT.bin", 20, create_cancel_callback())
        display.fill(PC.BLACK) 
        display.update()
        play_cutscene_animation(loc+"start2_74_30.BIT.bin", 20, create_cancel_callback())
    sleep(0.25)
    collect()  # Clean up after animations
    
def die():
    display.fill(PC.BLACK)
    if IS_THUMBY_COLOR:
        play_cutscene_animation(loc+"medie_128_110.COL.bin", 15, create_cancel_callback())
    else:
        play_cutscene_animation(loc+"medie_74_40.BIT.bin", 6, create_cancel_callback())
    sleep(0.3)
    collect()  # Clean up after animation
    
def home():
    display.fill(PC.BLACK)
    if IS_THUMBY_COLOR:
        play_cutscene_animation(loc+"home_128_80.COL.bin", 20, create_cancel_callback())
    else:
        play_cutscene_animation(loc+"home_74_30.BIT.bin", 10, create_cancel_callback())
    sleep(0.3)
    collect()  # Clean up after animation

def eject():
    display.fill(PC.BLACK)
    if IS_THUMBY_COLOR:
        play_cutscene_animation(loc+"eject_128_80.COL.bin", 20, create_cancel_callback())
    else:
        play_cutscene_animation(loc+"eject_72_40.BIT.bin", 10, create_cancel_callback())
    sleep(0.3)
    collect()  # Clean up after animation
  
def game_over():
    display.fill(PC.BLACK)     
    display.setFont("/lib/font8x8.bin", 8, 8, 1)
    display.drawText("GAME", 8 * PC.SCREEN_SCALE, 5 * PC.SCREEN_SCALE, PC.WHITE)
    display.drawText("OVER", 22 * PC.SCREEN_SCALE, 12 * PC.SCREEN_SCALE, PC.WHITE)
    display.setFont(PC.FONT_FILE, PC.FONT_WIDTH, PC.FONT_HEIGHT, PC.FONT_SPACE)
    display.drawText(f"Score: {score:02d}", 18 * PC.SCREEN_SCALE, 22 * PC.SCREEN_SCALE, PC.WHITE)
    display.drawText("Press A/B: Restart", 1 * PC.SCREEN_SCALE, 32 * PC.SCREEN_SCALE, PC.WHITE)
    display.update()
    while not (buttonA.justPressed() or buttonB.justPressed()):
        display.update()
    inputJustPressed()
  
def menu():
    display.setFPS(30)
    display.setFont(PC.FONT_FILE, PC.FONT_WIDTH, PC.FONT_HEIGHT, PC.FONT_SPACE)
    
    if IS_THUMBY_COLOR:
        audio_load(loc+"menu_background.ima")
        audio_play()
        audio_set_loop(True, 150496, 759838)
        menu_sprite = loc+"menu_128_120.COL.bin"
    else:
        menu_sprite = create_sprite(71, 40, (loc+"menu_71_40.BIT.bin", loc+"menu_71_40.SHD.bin"), 2, 0, 0)
    background = Stars(20, 4, 0)
    
    display.fill(PC.BLACK)
    i = 0
    rot = 5
    
    try:
        while not buttonA.justPressed():
            display.fill(PC.BLACK)
            background.run() 
            if IS_THUMBY_COLOR:
                display.draw_sprite_from_file(menu_sprite,y=4,key=0)
                if i==0:
                    display.drawText("Asteroid Dodge", 9, 56, PC.SELECT)
                    display.drawText("Dog Fight", 32, 82, PC.UNSELECT)
                    display.drawText("Campaigns", 31, 109, PC.UNSELECT)
                    display.drawRectangle(1,49,125,25,PC.ORANGE)
                elif i==1:
                    display.drawText("Asteroid Dodge", 10, 56, PC.UNSELECT)
                    display.drawText("Dog Fight", 32, 82, PC.SELECT)
                    display.drawText("Campaigns", 31, 109, PC.UNSELECT)
                    display.drawRectangle(1,74,125,25,PC.ORANGE)
                elif i==2:
                    display.drawText("Asteroid Dodge", 10, 56, PC.UNSELECT)
                    display.drawText("Dog Fight", 32, 82, PC.UNSELECT)
                    display.drawText("Campaigns", 31, 109, PC.SELECT)
                    display.drawRectangle(1,100,125,25,PC.ORANGE)
                elif i==3:
                    display.drawText("Dog Fight", 32, 56, PC.UNSELECT)
                    display.drawText("Campaigns", 31, 82, PC.UNSELECT)
                    display.drawText("Settings", 32, 109, PC.SELECT)
                    display.drawRectangle(1,100,125,25,PC.ORANGE)
                elif i==4:
                    display.drawText("Campaigns", 32, 56, PC.UNSELECT)
                    display.drawText("Settings", 32, 82, PC.UNSELECT)
                    display.drawText("Exit Game", 31, 110, PC.SELECT)
                    display.drawRectangle(1,100,125,25,PC.ORANGE)
            else:
                display.drawSprite(menu_sprite)
                if i==0:
                    display.drawText("Asteroid Dodge", 10, 20, PC.SELECT)
                    display.drawText("Dog Fight", 21, 30, PC.UNSELECT)
                elif i==1:
                    display.drawText("Dog Fight", 21 , 20, PC.SELECT)
                    display.drawText("Campaigns", 21 , 30, PC.UNSELECT)
                elif i==2:
                    display.drawText("Campaigns", 21, 20, PC.SELECT)
                    display.drawText("Settings", 21, 30, PC.UNSELECT)
                elif i==3:
                    display.drawText("Settings", 21, 20, PC.SELECT)
                    display.drawText("Exit Game", 21, 30, PC.UNSELECT)
                elif i==4:
                    display.drawText("Settings", 21, 20, PC.UNSELECT)
                    display.drawText("Exit Game", 21, 30, PC.SELECT)
            
            display.update()
            
            if buttonD.justPressed():
                i+=1
                if i > 4: i=4
                rot = -5
                if (rumble): rumble(20)
            elif buttonU.justPressed():
                i+=-1
                if i < 0: i=0
                rot = 5
                if (rumble): rumble(20)
    finally:
        # Clean up menu sprite and background
        del menu_sprite, background
        collect()
        if IS_THUMBY_COLOR:
            audio_stop()
    
    return i

class SettingsMenu:
    def __init__(self):
        self.settings_items = self.get_menu_items()
        self.selected = 0
        self.remapping = False
        self.current_remap = 0
        self.background = Stars(20, 4, 0)
        display.setFont(PC.FONT_FILE, PC.FONT_WIDTH, PC.FONT_HEIGHT, PC.FONT_SPACE)
    
    def get_menu_items(self):
        return [
            "FIRE: " + KEYMAPS[KEY_FIRE],
            "SHIFT: " + KEYMAPS[KEY_SHIFT], 
            "MOVE LEFT: " + KEYMAPS[KEY_MOVE_LEFT],
            "MOVE RIGHT: " + KEYMAPS[KEY_MOVE_RIGHT],
            "MOVE UP: " + KEYMAPS[KEY_MOVE_UP],
            "MOVE DOWN: " + KEYMAPS[KEY_MOVE_DOWN],
            "ABURNER: " + ("SHIFT+" if SHIFT_REQUIRED[KEY_AFTERBURNER] else "") + KEYMAPS[KEY_AFTERBURNER],
            "BREAK: " + ("SHIFT+" if SHIFT_REQUIRED[KEY_BREAK] else "") + KEYMAPS[KEY_BREAK],
            "TGT NEXT: " + ("SHIFT+" if SHIFT_REQUIRED[KEY_TARGET_NEXT] else "") + KEYMAPS[KEY_TARGET_NEXT],
            "TGT PREV: " + ("SHIFT+" if SHIFT_REQUIRED[KEY_TARGET_PREV] else "") + KEYMAPS[KEY_TARGET_PREV],
            "EJECT: " + ("SHIFT+" if SHIFT_REQUIRED[KEY_EJECT] else "") + KEYMAPS[KEY_EJECT],
            "RESET DEFAULTS",
            "BACK"
        ]
    
    def update_menu(self):
        self.settings_items = self.get_menu_items()
    
    def get_pressed_key(self):
        if buttonA.pressed(): return 'A'
        elif buttonB.pressed(): return 'B'
        elif buttonU.pressed(): return 'U'
        elif buttonD.pressed(): return 'D'
        elif buttonL.pressed(): return 'L'
        elif buttonR.pressed(): return 'R'
        return ''
    
    def handle_special_action(self, i):
        return None  # None = not handled, True = handled, False = exit
    
    def run(self):
        global KEYMAPS, SHIFT_REQUIRED
        display.setFPS(30)
        
        while True:
            display.fill(PC.BLACK)
            self.background.run()
          
            display.drawText("SETTINGS", 22 * PC.SCREEN_SCALE, 2 * PC.SCREEN_SCALE, PC.WHITE)
            display.drawLine(0, 9 * PC.SCREEN_SCALE, PC.WIDTH, 9 * PC.SCREEN_SCALE, PC.WHITE)
            
            if self.remapping:
                display.fill(PC.BLACK)
                display.drawText("PRESS NEW KEY FOR:", 2 * PC.SCREEN_SCALE, 2 * PC.SCREEN_SCALE, PC.WHITE)
                display.drawLine(0, 9 * PC.SCREEN_SCALE, PC.WIDTH, 9 * PC.SCREEN_SCALE, PC.WHITE)
                
                key_names = ["FIRE", "SHIFT", "MOVE LEFT", "MOVE RIGHT", 
                             "MOVE UP", "MOVE DOWN", "AFTERBURNER", 
                             "BREAK", "TARGET NEXT", "TARGET PREV", "EJECT"]
                display.drawText(key_names[self.current_remap], 16 * PC.SCREEN_SCALE, 14 * PC.SCREEN_SCALE, PC.SELECT)
                
                while not inputJustPressed():
                    display.update()
                
                new_key = self.get_pressed_key()
                if new_key:
                    KEYMAPS[self.current_remap] = new_key
                    self.update_menu()
                    
                sleep(0.3)
                inputJustPressed()
                self.remapping = False
                sleep(0.3)
                continue
            
            display.drawText("A:Remap L:Shift B:Save", 1 * PC.SCREEN_SCALE, PC.HEIGHT - 6 * PC.SCREEN_SCALE, PC.LIGHTGRAY)
            
            start_idx = max(0, min(self.selected - 2, len(self.settings_items) - PC.SETTING_ITEMS))
            for i in range(start_idx, min(start_idx + PC.SETTING_ITEMS, len(self.settings_items))):
                y_pos = 12 * PC.SCREEN_SCALE + (i - start_idx) * 6 * PC.SCREEN_SCALE
                text_color = PC.SELECT if i == self.selected else PC.UNSELECT
                prefix = "> " if (i == self.selected and 6 <= i <= 10) else "  "
                display.drawText(prefix + self.settings_items[i], 2 * PC.SCREEN_SCALE, y_pos, text_color)
            
            if len(self.settings_items) > PC.SETTING_ITEMS:
                scrollbar_height = min(35, 35 * PC.SETTING_ITEMS / len(self.settings_items))
                scrollbar_pos = 12 * PC.SCREEN_SCALE + (35 * PC.SCREEN_SCALE - scrollbar_height) * self.selected / (len(self.settings_items) - 1)
                display.drawFilledRectangle(PC.WIDTH - 2, int(scrollbar_pos), 2, int(scrollbar_height), PC.WHITE)
            
            display.update()
            
            if buttonU.justPressed():
                self.selected = (self.selected - 1) % len(self.settings_items)
                sleep(0.15)
            elif buttonD.justPressed():
                self.selected = (self.selected + 1) % len(self.settings_items)
                sleep(0.15)
            elif buttonA.justPressed():
                # Check for platform-specific action first
                result = self.handle_special_action(self.selected)
                if result is True:
                    pass  # Handled by platform
                elif result is False:
                    return  # Exit requested
                elif self.selected < 11:
                    self.remapping = True
                    self.current_remap = self.selected
                elif self.selected == 11:  # Reset defaults
                    KEYMAPS = array('O', DEFAULT_KEYS)
                    SHIFT_REQUIRED = array('B', [False,False,False,False,False,False,True,True,not IS_THUMBY_COLOR,not IS_THUMBY_COLOR,True])
                    self.update_menu()
                    sleep(0.3)
                elif self.selected == 12:  # Back
                    save_keymaps(KEYMAPS)
                    return
                sleep(0.15)
            elif buttonL.justPressed():
                if 6 <= self.selected <= 10:
                    SHIFT_REQUIRED[self.selected] = not SHIFT_REQUIRED[self.selected]
                    self.update_menu()
                    sleep(0.2)
            elif buttonB.justPressed():
                save_keymaps(KEYMAPS)
                return

def run_campaign(campaign_engine):
    global lifes, player_speed, player_target_speed, player_angle, score
    
    mission_config = campaign_engine.get_mission_config()
    if not mission_config:
        return (0, False)
    
    mission_objectives = campaign_engine.get_mission_objectives()
    
    campaign_engine.show_mission_briefing(mission_config)
    
    lifes = 5
    player_speed = player_target_speed = float2fp(1)
    player_angle = [0, 0, 0]
    score = 0
    hudShip = None
    if hud_fb: hud_fb.fill(0)
    
    launch()
    collect()
    display.setFPS(PC.FPS)
    
    stars = Stars(PC.STAR_COUNT, 5, 85)
    mission_type = mission_config.get("type", "mixed")
    
    difficulty = mission_config.get("difficulty", 1)
    enemy_count = mission_config.get("enemies", 0)
    asteroid_count = mission_config.get("asteroids", 0)
    
    enemy_health = min(5, 3 + difficulty // 2)
    enemy_speed = 6554 + (difficulty * 1000)
    
    if mission_type == "dogfight" or mission_type == "mixed":
        enemies = Enemies(max(1, enemy_count))
        for enemy in enemies.enemies:
            enemy[7] = enemy_health
            enemy[5] = enemy_speed
    else:
        enemies = None
    
    if mission_type == "asteroids" or mission_type == "mixed":
        astroids = Astroids(max(5, asteroid_count + (difficulty * 2)))
    else:
        astroids = None
    
    ship = Ship()
    
    mission_start_time = ticks_ms()
    mission_duration = 0
    kills_needed = mission_objectives.get("kills", 0)
    survive_time = mission_objectives.get("survive_time", 0) * 1000
    has_time_objective = survive_time > 0
    has_kill_objective = kills_needed > 0
    total_kills = 0
    mission_phase_complete = False
    mission_successful = False
    display.setFont(PC.FONT_FILE, PC.FONT_WIDTH, PC.FONT_HEIGHT, PC.FONT_SPACE)
    
    while lifes > 0:
        display.fill(PC.BLACK)
        
        current_time = ticks_ms()
        mission_duration = ticks_diff(current_time, mission_start_time)
        
        time_objective_met = has_time_objective and mission_duration >= survive_time
        kill_objective_met = has_kill_objective and total_kills >= kills_needed
        
        if has_time_objective and has_kill_objective:
            mission_phase_complete = time_objective_met and kill_objective_met
        elif has_time_objective:
            mission_phase_complete = time_objective_met
        elif has_kill_objective:
            mission_phase_complete = kill_objective_met
        
        if mission_phase_complete:
            if enemies and len(enemies.enemies) > 0:
                pass
            elif astroids and len(astroids.astroids) > 0:
                pass    
            else:
                mission_successful = True
                break
        
        previous_score = score
        
        if enemies:
            if not ship.move_me(enemies.enemies): break
        else:
            if not ship.move_me(None): break
        
        stars.run(player_angle[2])
  
        if enemies:
            enemies.run(ship.laser, ship.fx, mission_phase_complete)
        if astroids:
            astroids.run(ship.laser, ship.fx, mission_phase_complete)
        
        if score > previous_score:
            new_kills = score - previous_score
            total_kills += new_kills
        
        ship.run()
        
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
        display.drawText(f"STAT: {progress}", 2 * PC.SCREEN_SCALE, 2 * PC.SCREEN_SCALE, PC.WHITE)
        display.update()

    del ship, stars, enemies, astroids
    collect()
    if mission_successful:
        home()
        display.setFPS(PC.FPS)
        collect()
        campaign_engine.show_mission_success()
    else:
        eject() if lifes > 0 else die()
        collect()
    
    return (score, mission_successful)

class CampaignBackground:
    def __init__(self):
        self.backgounrd = Stars(20, 4, 0)
    def run(self, num):
        if (self.backgounrd):
            self.backgounrd.run(num) 
    def __del__(self):
        del self.backgounrd

collect()
# Load color enhancements if on ThumbyColor
if IS_THUMBY_COLOR:
    print(f"Memory before: {mem_free()}")
    with open(loc + 'color_enhancements.py', 'r') as f:
        code = f.read()
    exec(code)
    del code
    collect()
    print(f"After cleanup: {mem_free()}")
    play_cutscene_animation(loc+"title_128_80.COL.bin", 21, create_cancel_callback())
else:
    # Intro finished
    Intro.finish()
  
# Main game loop
while True:
    lifes = 5
    player_speed = player_target_speed = float2fp(1)
    player_angle = [0, 0, 0]
    score = 0
    game = menu()
    inputJustPressed()
   
    if (game == 0):
        print(f"Free memory before launch: {mem_free()}")
        launch()
        collect()
        print(f"Free memory after launch: {mem_free()}")
        display.setFPS(PC.FPS)
        stars = Stars(PC.STAR_COUNT, 5)
        astroids = Astroids(12)
        ship = Ship()
        hudShip = None
        print(f"Free memory before flight: {mem_free()}")
        if hud_fb: hud_fb.fill(0)
        while lifes > 0:
            display.fill(0)
            if not ship.move_me(None): break
            stars.run(player_angle[2])
            astroids.run(ship.laser, ship.fx)
            ship.run()
            display.update()
        del stars, astroids, hudShip, ship
        collect()
        print(f"Free memory after flight: {mem_free()}")
        eject() if lifes > 0 else die() 
        print(f"Free memory after die: {mem_free()}")
        game_over()
        print(f"Free memory after gameover: {mem_free()}")
    elif (game == 1):
        launch()
        collect()
        display.setFPS(PC.FPS)
        stars = Stars(PC.STAR_COUNT, 5, 85)
        enemies = Enemies(3)
        ship = Ship()
        hudShip = None
        if hud_fb: hud_fb.fill(0)
        while lifes > 0:
            display.fill(0)
            if not ship.move_me(enemies.enemies): break
            stars.run(player_angle[2])
            enemies.run(ship.laser, ship.fx)
            ship.run()
            display.update()
        del stars, ship, enemies, hudShip
        collect()
        eject() if lifes > 0 else die()    
        game_over()
    elif (game == 2):
        collect()
        campaign_engine = CampaignEngine()
        campaign = campaign_engine.run_campaign_menu(CampaignBackground())
        collect()
        if campaign:
            current_mission_attempt = 0
            max_attempts = 3
            
            while True:
                hudShip = None
                if hud_fb: hud_fb.fill(0)
                collect()
                mission_result = run_campaign(campaign)
                mission_score = mission_result[0]
                mission_success = mission_result[1]
                
                if mission_success:
                    action = campaign.run_post_mission_menu(mission_score)
                    current_mission_attempt = 0
                    
                    if action == "complete" or action == "exit":
                        campaign_engine = None
                        campaign = None
                        collect()
                        break
                else:
                    current_mission_attempt += 1
                    
                    if current_mission_attempt >= max_attempts:
                        display.fill(PC.BLACK)
                        display.setFont("/lib/font5x7.bin", 5, 7, 1)
                        display.drawText("MISSION", 15 * PC.SCREEN_SCALE, 10 * PC.SCREEN_SCALE, PC.WHITE)
                        display.drawText("FAILED", 18 * PC.SCREEN_SCALE, 20 * PC.SCREEN_SCALE, PC.WHITE)
                        display.update()
                        sleep(2)
                        
                        display.setFont(PC.FONT_FILE, PC.FONT_WIDTH, PC.FONT_HEIGHT, PC.FONT_SPACE)
                        display.fill(PC.BLACK)
                        display.drawText("Too many attempts.", 2 * PC.SCREEN_SCALE, 10 * PC.SCREEN_SCALE, PC.WHITE)
                        display.drawText("Returning to menu.", 2 * PC.SCREEN_SCALE, 20 * PC.SCREEN_SCALE, PC.WHITE)
                        display.update()
                        sleep(2)
                        break
                    else:
                        display.fill(PC.BLACK)
                        display.setFont("/lib/font5x7.bin", 5, 7, 1)
                        display.drawText("MISSION", 15 * PC.SCREEN_SCALE, 10 * PC.SCREEN_SCALE, PC.WHITE)
                        display.drawText("FAILED", 18 * PC.SCREEN_SCALE, 20 * PC.SCREEN_SCALE, PC.WHITE)
                        display.update()
                        sleep(1)
                        
                        display.setFont(PC.FONT_FILE, PC.FONT_WIDTH, PC.FONT_HEIGHT, PC.FONT_SPACE)
                        display.fill(PC.BLACK)
                        display.drawText(f"Attempt {current_mission_attempt} of {max_attempts}", 2 * PC.SCREEN_SCALE, 10 * PC.SCREEN_SCALE, PC.WHITE)
                        display.drawText("Press A to retry", 2 * PC.SCREEN_SCALE, 20 * PC.SCREEN_SCALE, PC.WHITE)
                        display.update()
                        
                        while not buttonA.justPressed():
                            display.update()
                        sleep(0.2)
        del campaign, campaign_engine
        collect()
    elif (game == 3):
        settings = SettingsMenu()
        settings.run()
        del settings
        collect()
    else:
        reset()