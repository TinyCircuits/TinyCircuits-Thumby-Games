from array import array
from ssd1306 import display
from time import sleep_ms, ticks_ms
from utils import ihash

# Font by Auri (@Auri#8401)
_font = (
    bytearray([0,0,0]) # Space needs to be at the start.
    + # Alphabet # BITMAP: width: 78, height: 8
    bytearray([240,72,248,240,168,88,240,136,152,248,136,112,240,168,136,248,40,8,112,136,200,248,64,248,136,248,136,64,136,248,248,96,152,120,136,128,248,56,248,248,8,240,240,136,248,240,72,56,112,200,248,240,72,184,176,168,200,8,248,8,120,128,248,248,192,56,248,224,248,216,96,216,152,160,120,200,168,152])
    + # Numbers # BITMAP: width: 30, height: 8
    bytearray([120,136,240,144,248,192,208,136,176,136,168,88,32,48,248,88,136,104,112,168,200,8,200,56,88,168,208,56,40,240])
    + # Symbols # BITMAP: width: 57, height: 8
    bytearray([184,0,184,16,136,48,216,216,0,152,216,0,0,24,0,24,0,24,128,96,24,136,80,32,32,80,136,240,136,0,0,136,120,112,136,0,0,136,112,192,192,0,128,192,0,32,112,32,80,32,80,32,32,32])
    )
_font_index = " ABCDEFGHIJKLMNOPQRSTUVWXYZ"+"0123456789"+"!?:;'\"/><[]().,+*-"

# Setup basic display access
_FPS = const(60)

# Setup emulator, if running
EMULATED = False
@micropython.viper
def ptr(buf) -> int:
    return int(ptr16(buf))
try:
    import emulator
    emulator.screen_breakpoint(ptr(display.buffer))
    EMULATED = True
except ImportError:
    pass

# Setup the display
_display_buffer = display.buffer
timer = ticks_ms()
_fwait = 1000//(_FPS if EMULATED else _FPS*2)
@micropython.native
def display_update():
    global timer
    t = ticks_ms()
    nwait = timer - ticks_ms()
    sleep_ms(0 if nwait <= 0 else nwait if nwait < _fwait else _fwait)
    display.write_data(_display_buffer)
    timer = ticks_ms() + _fwait

def _gen_bang(blast_x, blast_y, blast_size, invert):
    @micropython.viper
    def p(x: int, oY: int) -> int:
        s = int(blast_size)
        f = int(invert)
        _by = int(blast_y)
        tx = x-int(blast_x)
        v = 0
        for y in range(oY, oY+32):
            ty = y-_by
            a = 0 if tx*tx+ty*ty < s*s else 1
            v |= (
                a if f == 0 else (0 if a else 1)
            ) << (y-oY)
        return v
    return p

class Tape:
    def __init__(self):
        self._tape = array('l', (0 for i in range(72*3*2*5+72*2*2)))
        self._tape_scroll = array('l', [0, 0, 0, 0, 0, 0, 0])
        self.x = memoryview(self._tape_scroll)[3:5]
        self.midx = memoryview(self._tape_scroll)[1:2]
        self.bx = memoryview(self._tape_scroll)[0:1]
        # Alphabet for writing text - 3x5 text size (4x6 with spacing)
        # Custom emojis: @ = Umby and ^ = Glow
        self._abc = _font + bytearray([128,240,48,0,248,192])
        self._abc_i = dict((v, i) for i, v in enumerate(_font_index+"@^"))
        # The patterns to feed into each tape section
        self.feed = [None, None, None, None, None]
        self.cam_shake = 0
        self._stage = array('l', (0 for i in range(72*2*3+132*2)))
        self.spawner = (bytearray([]), bytearray([]))
        def _pass(*arg):
            pass
        self.mons_clear = _pass
        self.mons_add = _pass
        # How far along the tape spawning has completed
        self._x = array('l', [0])
        self.player = None # Player at this device
        self.players = [] # Player register for interactions
        self.clear_overlay()
        self.clear_stage()

    @micropython.viper
    def reset(self, p: int):
        self.mons_clear()
        # Scroll each layer
        scroll = ptr32(self._tape_scroll)
        scroll[0] = p//4
        scroll[1] = p//2
        scroll[3] = p
        # Reset the tape buffers for all layers and fill with the current feed.
        scroll = ptr32(self._tape_scroll)
        for i in range(3):
            layer = 3 if i == 2 else i
            tapePos = scroll[layer]
            for x in range(tapePos-72, tapePos+144):
                self.redraw_tape(i, x, self.feed[layer], self.feed[layer+1])

    @micropython.viper
    def check(self, x: int, y: int, b: int) -> bool:
        if x < -30 or x >= 102:
            return False # Out of buffer range is always False
        stage = ptr32(self._stage)
        p = (x+30)%132*2+432
        h = y - 8 # y position is from bottom of text
        img1 = b >> 0-h if h < 0 else b << h
        img2 = b >> 32-h if h-32 < 0 else b << h-32
        return bool((stage[p] & img1) | stage[p+1] & img2)

    @micropython.viper
    def draw(self, layer: int, x: int, y: int, img: ptr8, w: int, f: int):
        o = x-f*w
        p = (layer+2)*144 + (60 if layer == 1 else 0)
        r1 = -30 if layer == 1 else 0
        r2 = 101 if layer == 1 else 71
        draw = ptr32(self._stage)
        for i in range(x if x >= r1 else r1, x+w if x+w <= r2 else r2):
            b = uint(img[i-o])
            draw[p+i*2] |= (b << y) if y >= 0 else (b >> 0-y)
            draw[p+i*2+1] |= (b << y-32) if y >= 32 else (b >> 32-y)

    @micropython.viper
    def mask(self, layer: int, x: int, y: int, img: ptr8, w: int, f: int):
        o = x-f*w
        p = layer*144
        draw = ptr32(self._stage)
        for i in range(x if x >= 0 else 0, x+w if x+w < 72 else 71):
            b = uint(img[i-o])
            draw[p+i*2] &= -1 ^ ((b<<y) if y >= 0 else (b>>0-y))
            draw[p+i*2+1] &= -1 ^ ((b<<y-32) if y >= 32 else (b>>32-y))

    @micropython.viper
    def comp(self):
        tape = ptr32(self._tape)
        scroll = ptr32(self._tape_scroll)
        stg = ptr32(self._stage)
        frame = ptr8(_display_buffer)
        scroll[2] += 1 # Counter (increment)
        y_pos = scroll[4]
        # Loop through each column of pixels
        for x in range(72):
            # Compose the first 32 bits vertically.
            p0 = (x+scroll[0])%216*2
            p1 = (x+scroll[1])%216*2
            p3 = (x+scroll[3])%216*2
            dimshift = (scroll[2]+x+y_pos+p1)%2 # alternating dimmer modifier
            dim = int(1431655765) << dimshift
            xdimshift = (scroll[2]+x+y_pos+p1)%8 # darker dither modifier
            xdim = (int(-2004318072) if xdimshift == 0 else
                int(1145324612) if xdimshift == 4 else
                int(572662306) if xdimshift == 2 else
                int(286331153) if xdimshift == 6 else 0)
            x2 = x*2
            overlay_mask = uint(tape[x2+2160] << y_pos)
            a = uint(((
                        # Back/mid layer (with monster mask and fill)
                        ((tape[p0] | tape[p1+432]) & stg[x2]
                            & stg[x2+144] & tape[p1+864] & tape[p3+1728])
                        # Background (non-interactive) monsters
                        | stg[x2+288])
                    # Dim all mid and background layers
                    & dim & overlay_mask
                    # Foreground monsters (and players)
                    | stg[x2+492]
                    # Foreground (with monster mask and fill)
                    | (tape[p3+1296] & stg[x2+144] & tape[p3+1728]))
                # Now apply the overlay mask and draw layers.
                & (overlay_mask | xdim)
                | (tape[x2+2304] << y_pos))
            # Now compose the second 32 bits vertically.
            overlay_mask = uint((uint(tape[x2+2160]) >> 32-y_pos)
                    | (tape[x2+2161] << y_pos))
            b = uint(((
                        # Back/mid layer (with monster mask and fill)
                        ((tape[p0+1] | tape[p1+433]) & stg[x2+1]
                        & stg[x2+145] & tape[p1+865] & tape[p3+1729])
                        # Background (non-interactive) monsters
                        | stg[x2+289])
                    # Dim all mid and background layers
                    & dim & overlay_mask
                    # Foreground monsters (and players)
                    | stg[x2+493]
                    # Foreground (with monster mask and fill)
                    | (tape[p3+1297] & stg[x2+145] & tape[p3+1729]))
                # Now apply the overlay mask and draw layers.
                & (overlay_mask | xdim)
                | (uint(tape[x2+2304]) >> 32-y_pos) | (tape[x2+2305] << y_pos))
            # Apply the relevant pixels to next vertical column of the display
            # buffer, while also accounting for the vertical offset.
            frame[x] = a >> y_pos
            frame[72+x] = (a >> 8 >> y_pos) | (b << (32 - y_pos) >> 8)
            frame[144+x] = (a >> 16 >> y_pos) | (b << (32 - y_pos) >> 16)
            frame[216+x] = (a >> 24 >> y_pos) | (b << (32 - y_pos) >> 24)
            frame[288+x] = b >> y_pos

    @micropython.viper
    def clear_stage(self):
        stg = ptr32(self._stage)
        for i in range(288, 696):
            stg[i] = 0
        for i in range(288):
            stg[i] = -1

    @micropython.viper
    def check_tape(self, x: int, y: int) -> bool:
        tape = ptr32(self._tape)
        p = x%216*2+1296
        return bool(tape[p] & (1 << y) if y < 32 else tape[p+1] & (1 << y-32))
    
    @micropython.viper
    def scroll_tape(self, back_move: int, mid_move: int, fore_move: int):
        tape = ptr32(self._tape)
        scroll = ptr32(self._tape_scroll)
        feed = self.feed
        for i in range(3):
            layer = 3 if i == 2 else i
            move = fore_move if i == 2 else mid_move if i == 1 else back_move
            if not move:
                continue
            # Advance the tape_scroll position for the layer
            tapePos = scroll[layer] + move
            scroll[layer] = tapePos
            # Find the tape position for the column that needs to be filled
            x = tapePos + 143 if move == 1 else tapePos - 72
            offX = layer*432 + x%216*2
            # Update 2 words of vertical pattern for the tape
            # (the top 32 bits, then the bottom 32 bits)
            pattern = feed[layer]
            tape[offX] = int(pattern(x, 0))
            tape[offX+1] = int(pattern(x, 32))
            if layer != 0:
                fill_pattern = feed[layer + 1]
                tape[offX+432] = int(fill_pattern(x, 0))
                tape[offX+433] = int(fill_pattern(x, 32))
        # Spawn new monsters
        xp = ptr32(self._x)
        p = scroll[3]
        # Only spawn when scrolling into unseen tape
        if xp[0] >= p:
            return
        spawner = self.spawner
        rates = ptr8(spawner[1])
        types = ptr8(spawner[0])
        r = int(uint(ihash(p))>>3)
        # Loop through each monster type, randomly spawning at configured rate
        for i in range(0, int(len(spawner[0]))):
            if r%2057 < rates[i]:
                self.mons_add(types[i], p+72+36, r%64)
            r = r >> 1
        xp[0] = p 

    @micropython.viper
    def redraw_tape(self, layer: int, x: int, pattern, fill_pattern):
        tape = ptr32(self._tape)
        l = 3 if layer == 2 else layer
        offX = l*432 + x%216*2
        tape[offX] = int(pattern(x, 0))
        tape[offX+1] = int(pattern(x, 32))
        if l != 0 and fill_pattern:
            tape[offX+432] = int(fill_pattern(x, 0))
            tape[offX+433] = int(fill_pattern(x, 32))

    @micropython.viper
    def scratch_tape(self, layer: int, x: int, pattern, fill_pattern):
        tape = ptr32(self._tape)
        l = 3 if layer == 2 else layer
        p = ptr32(self._tape_scroll)[l]
        if -72 <= x - p < 144:
            offX = l*432 + x%216*2
            tape[offX] &= int(pattern(x, 0))
            tape[offX+1] &= int(pattern(x, 32))
            if l != 0 and fill_pattern:
                tape[offX+432] |= int(fill_pattern(x, 0))
                tape[offX+433] |= int(fill_pattern(x, 32))

    @micropython.viper
    def draw_tape(self, layer: int, x: int, pattern, fill_pattern):
        tape = ptr32(self._tape)
        l = 3 if layer == 2 else layer
        offX = l*432 + x%216*2
        tape[offX] |= int(pattern(x, 0))
        tape[offX+1] |= int(pattern(x, 32))
        if l != 0 and fill_pattern:
            tape[offX+432] &= int(fill_pattern(x, 0))
            tape[offX+433] &= int(fill_pattern(x, 32))
        
    @micropython.viper
    def offset_vertically(self, offset: int):
        ptr32(self._tape_scroll)[4] = (
            offset if offset >= 0 else 0) if offset <= 24 else 24

    @micropython.viper
    def auto_camera(self, x: int, y: int, d: int, t: int):
        c = ptr32(self._tape_scroll)[3] # Current camera position
        # Tape scroll
        n = (-1 if x<c+10 or (d == -1 and x<c+40 and t%8==0) else
            1 if x>c+62 or (d == 1 and x>=c+12 and (1 if x>c+40 else
                t%2 if x>c+30 else t%4==3 if x>c+20 else t%8==7)) else 0)
        if n != 0:
            self.scroll_tape(n if c % 4 == 0 else 0, n*(c % 2), n)
        # Vertical offset
        y -= 20
        ptr32(self._tape_scroll)[4] = ((y if y >= 0 else 0) if y <= 24
            else 24) + t//2%(int(self.cam_shake)+1)*(1 if y<12 else -1)

    @micropython.viper
    def write(self, layer: int, text, x: int, y: int):
        text = text.upper()
        tape = ptr32(self._tape)
        abc_b = ptr8(self._abc)
        abc_i = self._abc_i
        h = y - 8 # y position is from bottom of text
        mask = 864 if layer == 1 else 1728 if layer == 2 else 2160
        draw = 432 if layer == 1 else 1296 if layer == 2 else 2304
        w = 216 if layer == 1 or layer == 2 else 72
        b = 0xFE
        for i in range(int(len(text))*4+1): # Clear space on mask layer
            xi = x-1+i
            if layer != 1 and layer != 2 and (xi < 0 or xi >= 72): continue
            p = xi%w*2+mask
            tape[p] ^= tape[p] & (b >> -1-h if h+1 < 0 else b << h+1)
            tape[p+1] ^= tape[p+1] & (b >> 31-h if h-31 < 0 else b << h-31)
        for i in range(int(len(text))):
            for o in range(3):
                p = (x+o+i*4)%w*2
                b = abc_b[int(abc_i.get(text[i], 0))*3+o]
                img1 = b >> 0-h if h < 0 else b << h
                img2 = b >> 32-h if h-32 < 0 else b << h-32
                # Draw to the draw layer
                tape[p+draw] |= img1
                tape[p+draw+1] |= img2
                # Stencil text out of the clear background mask layer
                tape[p+mask] |= img1
                tape[p+mask+1] |= img2

    @micropython.viper
    def message(self, position: int, text, layer: int):
        lines = [""] # Split into lines
        for word in text.split(' '):
            lenn = int(len(lines[-1]))
            if (lenn + int(len(word)) + 1)*4 > 72 or word=="\n":
                if lenn and lenn*4 < 72 and position:
                    lines[-1] += " "
                lines.append("")
            if word == "\n":
                continue
            lines[-1] += (" " if lines[-1] else "") + word
        lenn = int(len(lines[-1]))
        if lenn and lenn*4 < 72 and position:
            lines[-1] += " "
        leng = int(len(lines))
        if position == 0: # Centered
            x = 36
            y = 25-leng*3
            if layer == 1:
                x += ptr32(self._tape_scroll)[1] + 36
                y += 10
            for i in range(leng):
                line = lines[i]
                if line:
                    self.write(layer, line, x-(int(len(line))*2), y)
                y += 6
        else:
            if position == 1: # Top
                y = 5
            if position == 2: # Bottom
                y = 46 - 6*leng
            for i in range(leng):
                self.write(layer, lines[i], 0, y)
                y += 6

    @micropython.viper
    def tag(self, text, x: int, y: int):
        scroll = ptr32(self._tape_scroll)
        p = x-scroll[3]+scroll[1] # Translate position to mid background
        self.write(1, text, p-int(len(text))*2, y+3)

    @micropython.viper
    def blast(self, t: int, x: int, y: int):
        scratch = self.scratch_tape
        # Tag the wall with an explostion mark
        tag = t%4
        self.tag("<BANG!>" if tag==0 else "<POW!>" if tag==1 else
            "<WHAM!>" if tag==3 else "<BOOM!>", x, y)
        # Carve blast hole out of foreground
        pattern = _gen_bang(x, y, 8, 0)
        fill = _gen_bang(x, y, 10, 1)
        for i in range(x-10, x+10):
            scratch(2, i, pattern, fill)

    @micropython.viper
    def clear_overlay(self):
        tape = ptr32(self._tape)
        for i in range(2160, 2304): # Overlay mask
            tape[i] = -1
        for i in range(2304, 2448):
            tape[i] = 0
