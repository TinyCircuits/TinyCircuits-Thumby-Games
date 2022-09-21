from machine import Pin, reset
from math import sqrt, floor
from audio import *
from utils import sinco

_FPS = const(60)

# Button functions. Note they return the inverse pressed state
bU = Pin(4, Pin.IN, Pin.PULL_UP).value
bD = Pin(6, Pin.IN, Pin.PULL_UP).value
bL = Pin(3, Pin.IN, Pin.PULL_UP).value
bR = Pin(5, Pin.IN, Pin.PULL_UP).value
bB = Pin(24, Pin.IN, Pin.PULL_UP).value
bA = Pin(27, Pin.IN, Pin.PULL_UP).value

## Umby and Glow artwork ##
# BITMAP: width: 3, height: 8, frames: 6
_u_art = bytearray([1,6,0,0,7,0,0,6,1,0,7,0,3,7,4,4,7,3])
_u_sdw = bytearray([51,127,0,0,255,0,0,127,51,0,255,0,35,127,28,28,127,35])
_u_sdw_air = bytearray([3,15,0,0,15,0,0,15,3,0,15,0,3,15,12,12,15,3]) # When falling
# BITMAP: width: 3, height: 8, frames: 6
_g_art = bytearray([16,76,0,0,92,0,0,76,16,0,92,0,24,92,4,4,92,24])
_g_sdw = bytearray([89,159,64,64,159,64,64,159,89,64,159,64,89,159,70,70,159,89])
# BITMAP: width: 9, height: 8
_ug_back_mask = bytearray([120,254,254,255,255,255,254,254,120])
# BITMAP: width: 3, height: 8
_aim = bytearray([64,224,64])
 # BITMAP: width: 3, height: 8
_aim_fore_mask = bytearray([224,224,224])
# BITMAP: width: 5, height: 8
_aim_back_mask = bytearray([112,248,248,248,112])

def _draw_trail(draw_func, x, y, rdir):
    @micropython.viper
    def trail(x: int, oY: int) -> int:
        ry = int(y)
        return 3 << ry-oY-1
    for i in range(x-rdir*2, x, rdir):
        draw_func(2, i, trail, None)

class Player:
    def __init__(self, tape, mons, name, x, y, ai=False, coop=False):
        self.mode = 0
        self.name = name # Umby, Glow, or Clip
        self._ai = ai
        self.coop = coop
        self.dir = 1
        self.respawn_loc = 0 # custom respawn point
        self.x = x; self.y = y # Unit is 1 pixel
        self.rocket_on = 0
        self.rocket_x = self.rocket_y = 0 # Unit is 1 pixel
        self.space = 0 # Low gravity mode
        # Internal properties
        self._tp = tape
        self._mons = mons
        self._x = x*256; self._y = y*256 # Unit is 256th of a pixel
        self._rdir = 0
        self._moving = 0
        self._x_vel = self._y_vel = 0 # Unit is 65536 of a pixel
        self._hx = self._hy = 0 # Position where hook attaches ceiling
        self._topt = 0 # Amount of ticks Umby is being cheeky above roof
        # Internal hook parameters (resolved to player x, y in tick)
        self._hook_ang = 0 # Unit is 65536th of a radian
        self._hook_vel = 0
        self._hook_len = 0 # Unit is 256th of a pixel
        self._c = 0 # Button bits: up(1)|down(2)|left(4)|right(8)|b(16)|a(32)
        self._hold = 0
        self._aim_ang = 163840 # Unit is 65536th of a radian
        self._aim_pow = 256
        if name == "Glow": # Glow's starting behaviors
            self._aim_ang = -32768
            # Shoot hook straight up to spawn roof
            self._launch_hook(0)
            self._hy = 3
        elif name == "Clip": # Test mode starting behaviors
            self.mode = 199
        self._aim_x = (sinco[(self._aim_ang//1024+200)%400]-128)*10//128
        self._aim_y = (sinco[(self._aim_ang//1024-100)%400]-128)*10//128
        self._boom_x = self._boom_y = 0 # recent explosion
        self._trail = 0 # Currently making platform from rocket trail
        self._air = 0 # Currently in jump

    @micropython.viper
    def port_out(self, buf: ptr8):
        px = int(self._tp.x[0]) - 72
        buf[0] = px>>24
        buf[1] = px>>16
        buf[2] = px>>8
        buf[3] = px
        buf[4] = int(self.mode)
        buf[5] = int(self.x) - px
        buf[6] = int(self.y)
        buf[7] = int(self.rocket_x) - px
        buf[8] = int(self.rocket_y)
        buf[9] = int(self._hx) - px
        buf[10] = int(self._hy)
        boom = 1 if self._boom_x or self._boom_y else 0
        buf[11] = (# dir, rocket_on, rdir, moving, boom (0,1,2,3,4))
            (1 if int(self.dir) > 0 else 0)
            | int(self.rocket_on)*2
            | (4 if int(self._rdir) > 0 else 0)
            | int(self._moving)*8
            | boom*16
            | int(self._trail)*32
            | int(self._air)*64)
        buf[12] = int(self._boom_x) - px
        buf[13] = int(self._boom_y)
        self._boom_x = self._boom_y = 0 <<1|1 # reset last explosion (consumed)

    @micropython.viper
    def port_in(self, buf: ptr8) -> int:
        px = buf[0]<<24 | buf[1]<<16 | buf[2]<<8 | buf[3]
        m = buf[11]
        if m&16:
            self.rocket_x = buf[12] + px <<1|1
            self.rocket_y = buf[13] <<1|1
            self.detonate(buf[12])
        self.mode = buf[4] <<1|1
        self.x = buf[5] + px <<1|1
        self.y = buf[6] <<1|1
        rx = buf[7] + px
        ry = buf[8]
        self.rocket_x = rx <<1|1
        self.rocket_y = ry <<1|1
        self._hx = buf[9] + px <<1|1
        self._hy = buf[10] <<1|1
        self.dir = (1 if m&1 else -1) <<1|1
        self.rocket_on = (m&2) <<1|1
        rdir = 1 if m&4 else -1
        self._rdir = rdir <<1|1
        self._moving = (m&8) <<1|1
        self._air = (m&64) <<1|1
        if m&32: # Leave rocket trail
            _draw_trail(self._tp.draw_tape, rx, ry, rdir)
        return px + 72

    @property
    @micropython.viper
    def immune(self) -> int:
        return 1 if 199 <= int(self.mode) <= 202 or self._ai or self.coop else 0

    @micropython.native
    def die(self, death_message, respawn=None):
        if self.immune:
            return
        self._x_vel = 0 # Reset speed
        self._y_vel = 0 # Reset fall speed
        self.mode = 201 if 0 <= self.mode <= 9 else 202
        if self.respawn_loc:
            respawn = self.respawn_loc*256
        if respawn == None:
            respawn = self._x - 90000
        self._respawn_x = respawn
        self._tp.message(0, death_message + " \n \n Continue? \n 5", 3)
        self._death_message = death_message
        self._continue = 300
        self._cacc = 0 # Continue acceptance 0=held, 1=released, 2=accepted
        self._air = 1
        play(death, 240, True)

    @micropython.native
    def detonate(self, t):
        play(rocket_bang, 40)
        rx = self.rocket_x; ry = self.rocket_y
        self._boom_x = rx; self._boom_y = ry # Store for sending to coop
        self._tp.blast(t, rx, ry)
        # DEATH: Check for death by rocket blast
        dx = rx-self.x; dy = ry-self.y
        if dx*dx + dy*dy < 48:
            self.die(self.name + " kissed a rocket!")
        # Get ready to end rocket
        self.rocket_on = 0

    @micropython.viper
    def _tick_ai(self, t: int) -> int:
        ### Consult with the digital oracle for button presses ###
        mode = int(self.mode)
        x = int(self.x); y = int(self.y)
        d = int(self.dir) * 10
        p = int(self._tp.x[0]) + 36 # Horizontal middle
        m = int(bool(self._mons.num))
        # Horizontal super powers
        if x < p-50:
            self._x = (p-50)*256 <<1|1
        # Vertical super powers
        if y < 3:
            self._y = 2304 <<1|1
        elif y > 63:
            self._y = 16128 <<1|1
        if mode == 0: # Umby
            # Vertical jump super powers
            if y > 63:
                self._y_vel = -65536 <<1|1
            # Horizontal walking, rocket, and jump
            return ((4 if x > p+d else 0) | (8 if x < p+d else 0)
                | (16 if m and t%512<48 else 0) | (32 if y >= 50 else 0))
        elif mode == 12: # Glow (roof-walk)
            # Super hook
            if y > 55:
                self._launch_hook(0)
                # Apply super grapple hook parameters
                self._hx = x <<1|1
                self._hy = 1 <<1|1
                self._hook_len = ((y-1)<<8) <<1|1
            # Horizongal roof walking, rocket, and fall/grapple.
            return ((4 if x > p+d else 0) | (8 if x < p+d else 0)
                | (16 if m and t%256<5 else 0)
                | (32 if (t%16 and int(self._air) or t%512<8) else 0))
        else: # Glow (grappling swing)
            self._aim_ang = -52428 <<1|1
            if y < 0:
                self.mode = 12 <<1|1
            # Climb rope including when off screen so super powers work,
            # swing left/right towards center,
            # Fire rockets if monsters about, and
            # grapple when at end of swing if going in intended direction.
            a = int(self._hook_ang)
            return ((1 if int(self._hook_len)>3840 or x < p-50 else 0)
                | (4 if x>p else 0) | (8 if x<p else 0)
                | (16 if m and t%256<4 else 0)
                 | (32 if d*65536 > a > 32768 or d*65536 < a < -32768 else 0))

    @micropython.viper
    def tick(self, t: int):
        mode = int(self.mode)
        y = int(self._y)
        # If repesentation of coop Thumby, skip tick
        if self.coop:
            return
        # Update button press states
        if self._ai:
            c = int(self._tick_ai(t))
        else:
            c = 63^(int(bU()) | int(bD())<<1 | int(bL())<<2 | int(bR())<<3
                | int(bB())<<4 | int(bA())<<5)
        self._c = c <<1|1

        # Update directional states
        l = c&4; r = c&8
        m = 0
        if l or r:
            self.dir = (-1 if l else 1) <<1|1
            m = 1
        self._moving = m <<1|1

        # Normal Play modes
        if mode < 199:
            # Normal play modes
            if mode == 0: # Crawl mode (Umby)
                self._tick_play_ground(t)
            else: # Roof climbing modes (Glow)
                self._tick_play_roof(t)
            # Check for common death conditions:
            # DEATH: Check for falling into the abyss
            # Grappling can go further below the screen
            if y > 17920 and (mode != 11 or y > 32768):
                self.die(self.name + " fell into the abyss!")
        # Respawn mode
        elif 201 <= mode <= 202:
            self._tick_respawn()
        # Testing mode
        elif mode == 199:
            self._tick_testing()
        # Update the viper friendly variables.
        self.x = (int(self._x)>>8) <<1|1
        self.y = (int(self._y)>>8) <<1|1

    @micropython.viper
    def _tick_play_ground(self, t: int):
        xf = int(self._x); yf = int(self._y)
        x = xf>>8; y = yf>>8
        yv = int(self._y_vel)
        c = int(self._c)
        ch = self._tp.check_tape
        cl = int(ch(x-1, y))
        cr = int(ch(x+1, y))
        grounded = int(ch(x, y+1)) | cl | cr
        self._air = (0 if grounded else 1) <<1|1
        lwall = int(ch(x-1, y-3)) | cl
        rwall = int(ch(x+1, y-3)) | cr
        # Apply gravity and ground check
        if not grounded:
            self._y = (yf + (yv>>(10 if self.space else 8))) <<1|1
        # Stop gravity when hit ground but keep some fall speed ready
        self._y_vel = (32768 if grounded else yv + 2730) <<1|1
        # CONTROLS: Apply movement
        if t%3: # Movement
            self._x = (xf + (-256 if c&4 and not lwall else
                256 if c&8 and not rwall else 0)) <<1|1
        if t%3==0 and not ch(x, y-3) and ((c&4 and lwall) or (c&8 and rwall)):
            self._y = (yf-256) <<1|1 # Climbing
        # CONTROLS: Apply jump - allow continual jump until falling begins
        if y < 0:
            topt = int(self._topt)
            topt += 1
            if topt > 120:
                self.die(self.name + " flew too close to the sun!")
            self._topt = topt <<1|1
        elif self._topt:
            self._topt = 0 <<1|1
        if c&32 and y > -32 and (yv < 0 or grounded or self.space):
            if grounded: # detatch from ground grip
                self._y = (yf-256) <<1|1
                play(worm_jump, 15)
            self._y_vel = -52428 <<1|1
        # DEATH: Check for head smacking
        if ch(x, y-4) and c&32:
            # Only actually die if the platform hit is largish
            if ch(x, y-5) and ch(x, y-4) and ch(x-1, y-4) and ch(x+1, y-4):
                self.die(self.name + " face-planted the roof!")

        # Umby's rocket.
        ron = int(self.rocket_on)
        u = c&1; d = c&2; b = c&16
        # Apply rocket dynamics if it is active
        if ron:
            rxf = int(self._rocket_x); ryf = int(self._rocket_y)
            ryv = int(self._rocket_y_vel)
            # Apply rocket motion
            rxf += int(self._rocket_x_vel)
            ryf += ryv
            ryv += 1 if self.space else 11 # Apply gravity
            # Update stored properties
            rx = rxf>>8; ry = ryf>>8
            self.rocket_x = rx <<1|1
            self.rocket_y = ry <<1|1
            self._rocket_x = rxf <<1|1
            self._rocket_y = ryf <<1|1
            self._rocket_y_vel = ryv <<1|1
            if b: # Create trail platform when activated
                _draw_trail(self._tp.draw_tape, rx, ry, self._rdir)
            self._trail = (1 if b else 0)<<1|1
            # Defuse if fallen through ground or outer space
            if ry > 69 or (self.space and ry < -5) or not (
                    -30<=rx-int(self._tp.x[0])<=102):
                self.rocket_on = 0 <<1|1
            if ch(rx, ry): # Explode rocket if hit the ground
                self.detonate(t)
        elif b==0:
            self._hold = 0 <<1|1

        # Aiming and launching
        a_pow = int(self._aim_pow)
        if (u | d | b) or a_pow > 256:
            snco = ptr8(sinco)
            # CONTROLS: Aim rocket
            a_ang = int(self._aim_ang)
            if u | d:
                a_ang += 1310 if u else -1310
                self._aim_ang = a_ang <<1|1
            if b and ron==0 and (not self._hold or a_pow > 256):
                a_pow += 10
            # CONTROLS: Launch the rocket when button is released
            elif b==0 and ron==0 and a_pow > 256:
                play(rocket_flight, 180)
                self.rocket_on = 1 <<1|1
                self._rocket_x = xf <<1|1
                self._rocket_y = yf-512 <<1|1
                self.rocket_x = xf>>8 <<1|1
                self.rocket_y = (yf+512)>>8 <<1|1
                self._rocket_x_vel = (
                    (snco[((a_ang>>10)+200)%400]-128)*a_pow>>8) <<1|1
                self._rocket_y_vel = (
                    (snco[((a_ang>>10)-100)%400]-128)*a_pow>>8) <<1|1
                a_pow = 256
                self._rdir = (1 if int(self._aim_x) > 0 else -1) <<1|1
                # Wait until the rocket button is released before firing another
                self._hold = 1 <<1|1
            # Resolve rocket aim to the x by y vector form
            self._aim_x = ((snco[((a_ang>>10)+200)%400]-128)*a_pow//3360) <<1|1
            self._aim_y = ((snco[((a_ang>>10)-100)%400]-128)*a_pow//3360) <<1|1
            self._aim_pow = a_pow <<1|1

    @micropython.viper
    def _launch_hook(self, angle: int):
        ### Activate grappling hook in given aim ###
        ch = self._tp.check_tape
        snco = ptr8(sinco)
        x = int(self.x); y = int(self.y)
        xl = x<<8; yl = y<<8
        self._hook_ang = angle <<1|1
        # Find hook landing position
        xs = 128-snco[((angle>>10)+200)%400]
        ys = 128-snco[((angle>>10)-100)%400]
        xh = xl; yh = yl
        d = int(self.dir)
        while (yh >= -1 and (xl-xh)*d < 10240 and not int(ch(xh>>8, yh>>8))):
            xh += xs
            yh += ys
        # Apply grapple hook parameters
        self._hx = (xh>>8) <<1|1; self._hy = (yh>>8) <<1|1
        x1 = xl-xh; y1 = yl-yh
        self._hook_len = int(floor(sqrt(x1*x1+y1*y1))) <<1|1
        # Now get the velocity in the grapple angle
        xv = int(self._x_vel)>>8; yv = int(self._y_vel)>>8
        self._hook_vel = 0-(int(floor(sqrt(xv*xv+yv*yv)))*(1-xv*y1+yv*x1)
            >>5)//(int(self._hook_len) or 1) <<1|1
        # Start normal grappling hook mode
        self.mode = 11 <<1|1
        self._hold = 1 <<1|1
        play(grapple_launch, 6)

    @micropython.viper
    def _tick_play_roof(self, t: int):
        ### Handle one game tick for roof climbing play controls ###
        mode = int(self.mode)
        snco = ptr8(sinco)
        x = int(self.x); y = int(self.y)
        xf = int(self._x); yf = int(self._y)
        dr = int(self.dir)
        ch = self._tp.check_tape
        c = int(self._c)
        u = c&1; d = c&2; l = c&4; r = c&8; b = c&16; a = c&32
        cd = int(ch(x, y-1))
        crd = int(ch(x+1, y-1))
        cld = int(ch(x-1, y-1))
        cl = int(ch(x-1, y))
        cr = int(ch(x+1, y))
        cu = int(ch(x, y+3))
        falling = 0 if (cd | cld | crd | cl | cr) else 1
        self._air = falling <<1|1
        if falling and not a:
            self._hold = 0 <<1|1
        hold = int(self._hold)
        # CONTROLS: Grappling hook swing
        if mode == 11:
            ang = int(self._hook_ang)
            vel = int(self._hook_vel)
            leng = int(self._hook_len)
            hx = int(self._hx); hy = int(self._hy)
            g = (ang>>8)*(ang>>8)>>9
            vel = (# Swing speed limit
                (3584 if vel > 3584 else -3584 if vel < -3584 else vel)
                # Air friction
                - (((vel*vel>>9)*vel)>>21)
                # Apply gravity
                + (g if ang < 0 else 0-g)
                # CONTROLS: swing
                + (40 if r else -40 if l else 0))
            # CONTROLS: climb/extend rope
            leng += -128 if u and leng > 0 else 128 if d and not cu else 0
            # Check land interaction conditions
            if cu or (not falling and vel*ang > 0):
                # Rebound off ceiling
                vel = 0-vel
                ang += vel*2
            elif not (falling or a): # Stick to ceiling if touched
                self.mode = 12 <<1|1
                self._x_vel = self._y_vel = 0 <<1|1
            # Release grappling hook with button or within a second
            # when not connected to solid roof.
            elif (hold==0 and a or (hy < 0 and t%_FPS==0)):
                self.mode = 12 <<1|1
                # Convert angular momentum to free falling momentum
                self._x_vel = (
                    (snco[((ang>>10)-100)%400]-128)*leng>>15)*vel <<1|1
                self._y_vel = 0-(
                    (snco[((ang>>10)+200)%400]-128)*leng>>15)*vel <<1|1
                self._hold = 1 <<1|1
            # Calculate the worm position
            self._x = (hx<<8) + ((snco[((ang>>10)+200)%400]-128)*leng>>7) <<1|1
            self._y = (hy<<8) + ((snco[((ang>>10)-100)%400]-128)*leng>>7) <<1|1
            # Update motion and position variables based on swing
            self._hook_ang = ang+vel <<1|1
            self._hook_vel = vel <<1|1
            self._hook_len = leng <<1|1
        elif mode == 12: # Clinging movement (without grappling hook)
            x_vel = int(self._x_vel); y_vel = int(self._y_vel)
            # CONTROLS: Activate hook
            if falling and a and hold==0 and y < 64:
                # Activate grappling hook in aim direction
                self._launch_hook(int(self._aim_ang)*dr)
            # CONTROLS: Fall (force when jumping)
            elif falling or a:
                if not falling:
                    x_vel = -32768 if l else 32768 if r else 0
                    self._hold = 1 <<1|1
                # Apply gravity to vertical speed
                y_vel += 256 if self.space else 1638
                # Update positions with momentum
                xf += x_vel>>8
                yf += y_vel>>8
            else:
                # Stop falling when attached to roof
                y_vel = 0
            self._x_vel = x_vel <<1|1; self._y_vel = y_vel <<1|1
            # CONTROLS: Apply movement
            if t%2 and y < 64:
                clu = int(ch(x-1, y+3))
                cru = int(ch(x+1, y+3))
                climb = (cd==0 and ((l and crd) or (r and cld)))
                descend = cu==0 and (((cl | clu) and l) or ((cr | cru) and r))
                lsafe = ((cld | cd | int(ch(x-2, y-1)) | int(ch(x-2, y)))
                    and l and (cl | clu)==0)
                rsafe = ((crd | cd | int(ch(x+2, y-1)) | int(ch(x+2, y)))
                    and r and (cr | cru)==0)
                xf += -256 if lsafe else 256 if rsafe else 0
                yf += 256 if descend else -256 if climb else 0
            self._x = xf <<1|1; self._y = yf <<1|1

        # Glow's rocket.
        # Apply rocket dynamics if it is active
        if self.rocket_on:
            rdir = int(self._rdir)
            rxf = int(self._rocket_x); ryf = int(self._rocket_y)
            rxv = int(self._rocket_x_vel); ryv = int(self._rocket_y_vel)
            # Apply rocket motion
            rxf += rxv
            ryf += ryv
            # Apply flight boosters
            rxv += 10*rdir
            if rxv*rdir > 0:
                ryv = ryv * 9 // 10
            # Update stored properties
            rx = rxf>>8; ry = ryf>>8
            self.rocket_x = rx <<1|1
            self.rocket_y = ry <<1|1
            self._rocket_x = rxf <<1|1
            self._rocket_y = ryf <<1|1
            self._rocket_x_vel = rxv <<1|1
            self._rocket_y_vel = ryv <<1|1
            # Defuse if out of range
            if not (80>=ry>=-1) or not (-30<=rx-int(self._tp.x[0])<=102):
                self.rocket_on = 0 <<1|1
            if ch(rx, ry): # Explode rocket if hit the ground
                self.detonate(t)

        # Aiming and launching
        a_pow = int(self._aim_pow)
        if (u | d | b) or (not b and a_pow > 256):
            # CONTROLS: Aim rocket
            a_ang = int(self._aim_ang)
            # aiming (while not grappling)
            if (u | d) and int(self.mode) != 11 and not falling:
                a_ang += 1310 if u else -1310
                # Cap the aim angle
                a_ang = (-131072 if a_ang < -131072 else
                    0 if a_ang > 0 else a_ang)
                self._aim_ang = a_ang <<1|1
            if b: # Power rocket
                a_pow += 8
            # CONTROLS: Launch the rocket when button is released
            elif not b and a_pow > 256:
                play(rocket_flight, 180)
                self.rocket_on = 1 <<1|1
                self._rocket_x = xf <<1|1
                self._rocket_y = yf+512 <<1|1
                self.rocket_x = xf>>8 <<1|1
                self.rocket_y = (yf+512)>>8 <<1|1
                self._rocket_x_vel = (
                    (snco[((a_ang>>10)+200)%400]-128)*a_pow>>8)*dr <<1|1
                self._rocket_y_vel = (
                    (snco[((a_ang>>10)-100)%400]-128)*a_pow>>8) <<1|1
                a_pow = 256
                self._rdir = dr <<1|1
            # Resolve roscket aim to the x by y vector form
            self._aim_x = (
                (snco[((a_ang>>10)+200)%400]-128)*a_pow//3360)*dr <<1|1
            self._aim_y = ((snco[((a_ang>>10)-100)%400]-128)*a_pow//3360) <<1|1
            self._aim_pow = a_pow <<1|1
        aim_x = int(self._aim_x)
        if (l | r) and aim_x*dr > 0:
            self._aim_x = 0-aim_x <<1|1

    @micropython.viper
    def _tick_respawn(self):
        ### After the player dies, a respawn process begins,
        # showing a death message, while taking Umby back
        # to a respawn point on a new starting platform.
        # This handles a game tick when a respawn process is
        # active.
        ###
        tape = self._tp
        xf = int(self._x)
        yf = int(self._y)
        rex = int(self._respawn_x)
        cont = int(self._continue)
        c = int(self._c)
        cacc = int(self._cacc)

        # Update continue question
        if cont%60==0 and cacc != 2:
            if cont >= 0:
                tape.clear_overlay()
                tape.message(0, self._death_message
                    + " \n \n Continue? \n " + str(cont//60), 3)
            else:
                reset()
        self._continue = cont-1 <<1|1
        if cacc==0 and c&(16|32)==0:
            cacc = 1
        elif cacc==1 and c&(16|32):
            tape.clear_overlay()
            tape.message(0, self._death_message, 3)
            cacc = 2
        self._cacc = cacc <<1|1

        # Move player towards the respawn location
        if xf//256 != rex//256 or cacc != 2:
            self._x = xf + (256 if xf<rex else -256 if xf>rex else 0) <<1|1
            self._y = (yf + 0 if (yf>>8) == 20 else
                yf+256 if (yf>>8) < 20 else yf-256) <<1|1
            @micropython.viper
            def fill(x: int, oY: int) -> int:
                return -1
            @micropython.viper
            def ptrn(x: int, oY: int) -> int:
                return -128 if oY else 7
            # Draw the starting platform
            if rex <= xf < rex + 4000:
                tape.redraw_tape(2, (xf>>8)-5, ptrn, fill)
            elif rex - 4000 < xf <= rex:
                tape.redraw_tape(2, (xf>>8)+5, ptrn, fill)
        else:
            # Cancel any rocket powering
            self._aim_pow = 256 <<1|1
            # Hide any death message
            tape.clear_overlay()
            # Return to normal play modes
            if int(self.mode) == 201:
                self.mode = 0 <<1|1
            else:
                # Shoot hook straight up
                self._x_vel = self._y_vel = 0 <<1|1
                self._launch_hook(0)
            tape.write(1, "DONT GIVE UP!", int(tape.midx[0])+8, 26)

    @micropython.native
    def _tick_testing(self):
        ### Handle one game tick for when in test mode.
        # Test mode allows you to explore the level by flying,
        # free of interactions.
        ###
        self._y += -256 if self._c&1 else 256 if self._c&2 else 0
        self._x += -256 if self._c&4 else 256 if self._c&8 else 0
        # Switch to characters if buttons are pressed
        if not self._c&1:
            self.mode = 0 if self._c&16 else 12 if self._c&32 else 199
            if self.mode == 12:
                self._aim_ang = -32768
                self._launch_hook(0)

    @micropython.viper
    def draw(self, t: int):
        mode = int(self.mode)
        tape = self._tp
        p = int(tape.x[0])
        py = int(tape.x[1])
        x_pos = int(self.x) - p; y_pos = int(self.y)
        m = int(self._moving)
        d = int(self.dir)
        air = int(self._air)
        # Get animation frame
        # Steps through 0,1,2,3 every half second for animation
        # of looking left and right, and changes to movement art of
        # 4 when moving left and 5 when moving right.
        f = t*2//_FPS%4 if not m else 4 if d < 0 else 5
        abl = t*6//_FPS%2 # aim blinker
        # Draw rocket, if active
        if self.rocket_on:
            hx = int(self.rocket_x); hy = int(self.rocket_y)
            rdir = int(self._rdir)
            tape.draw(1, hx-p-1, hy-7, _aim, 3, 0)#head
            tape.draw(0, hx-p+(-3 if rdir>0 else 1), hy-7, _aim, 3, 0)#tail
        # Test mode or offscreen
        if mode == 199 or not (-2 < x_pos < 73 and -1 < y_pos-py < 42):
            hx = 0 if x_pos < -1 else 69 if x_pos > 72 else x_pos-1
            hy = py-5 if y_pos < py else py+32 if y_pos > py + 41 else y_pos-6
            tape.draw(abl, hx, hy, _aim, 3, 0)
            tape.mask(1, hx, hy, _aim_fore_mask, 3, 0)
        else: # Draw the worm
            # Select the character specifics
            umby = mode == 0 or mode == 201
            sdw = (_u_sdw if not air else _u_sdw_air) if umby else _g_sdw
            art = _u_art if umby else _g_art
            hy = y_pos-2
            by = y_pos-6 if umby else y_pos-1
            # Draw Umby's or Glow's layers and masks
            tape.draw(0, x_pos-1, hy, sdw, 3, f) # Shadow
            tape.draw(1, x_pos-1, hy, art, 3, f) # Umby
            tape.mask(1, x_pos-1, hy, sdw, 3, f)
            tape.mask(0, x_pos-4, by, _ug_back_mask, 9, 0)
        # Aims and hooks
        if mode == 11: # Activated grappling hook rope
            hook_x = int(self._hx); hook_y = int(self._hy)
            # Draw Glow's grappling hook rope
            for i in range(0, 8):
                sx = x_pos + (hook_x-(x_pos+p))*i//8
                sy = y_pos + (hook_y-y_pos)*i//8
                tape.draw(1, sx-1, sy-6, _aim, 3, 0)
            hx = hook_x-p-1; hy = hook_y-6
        aim_x = int(self._aim_x); aim_y = int(self._aim_y)
        # Aiming (only main player has aiming)
        if mode != 199 and not self._ai and not self.coop:
            # Rocket aim
            hx = x_pos+aim_x-1
            hy = y_pos+aim_y-6
            tape.draw(abl, hx, hy, _aim, 3, 0)
            tape.mask(1, hx, hy, _aim_fore_mask, 3, 0)
            tape.mask(0, hx-1, hy+1, _aim_back_mask, 5, 0)
