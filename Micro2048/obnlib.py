import thumby
import re

__VERSION__ = "0.01"

TEXT_LEFT = 0
TEXT_CENTER = 1
TEXT_RIGHT = 2

BTN_U = 0b000001
BTN_D = 0b000010
BTN_L = 0b000100
BTN_R = 0b001000
BTN_A = 0b010000
BTN_B = 0b100000

class Image:

    def __init__(self, data, w, h, cx=0, cy=0):
        if isinstance(data, list):
            self.data = data
        else:
            self.data = [data]
        self.w = w
        self.h = h
        self.cx = cx
        self.cy = cy

class Menu:

    IMAGE_MARK = Image(b"\x04\x06\x07\x06\x04", 5, 3)

    class Item:
        def __init__(self, label, func):
            self.label = label
            self.func = func

    def __init__(self, items, pos=0, border=False):
        self.items = items
        self.pos = pos
        self.border = border
        self.gap = 0
        self.dirty = True

    def update(self):
        v = btn_d(BTN_D) - btn_d(BTN_U)
        if v == 0:
            if self.gap != 0:
                self.gap += 1 if self.gap < 0 else -1
                self.dirty = True
        else:
            self.pos += v
            pos_max = len(self.items) - 1
            if self.pos < 0:
                self.pos = pos_max
            elif self.pos > pos_max:
                self.pos = 0
            self.gap = v * 2
            self.dirty = True
            tick()
        if btn_d(BTN_A):
            self.items[self.pos].func()
            self.dirty = True
        if frames % 8 == 0:
            self.dirty = True

    def draw(self):
        box(-1, 24, 130, 17, self.border, 0)
        text(self.items[self.pos].label, 36, 30 + self.gap, TEXT_CENTER)
        if frames % 16 < 8:
            for i in range(3):
                blit(self.IMAGE_MARK, 33, 26)
                blit(self.IMAGE_MARK, 33, 36, mirrorY=True)
        self.dirty = False

class MmlPlayer:

    FREQ_TABLE = [3951, 4186, 4434, 4698, 4978, 5274, 5588,
                  5920, 6272, 6645, 7040, 7459, 7902, 8372]

    def __init__(self, fps):
        self.fps = fps
        self.playing = False
        self.priority = 0
        self.o = 4
        self.s = 16
        self.q = 1.0

    def play(self, mml, priority):
        if self.playing and priority < self.priority:
            return
        self.priority = priority
        self.playing = True
        self.mml = mml.upper()
        self.cnt = 0

    def update(self):
        if not self.playing:
            return
        self.cnt -= 1
        if self.cnt > 0:
            return
        loop = True
        while loop and len(self.mml) > 0:
            c = self.get_mml_token()
            if c in "CDEFGAB":
                a = ord(c)-67
                a = a*2 + (a<3) + (a<0)*13
                if len(self.mml) > 0 and self.mml[0] in "+-":
                    a += 1 if self.get_mml_token() == "+" else -1
                freq = self.FREQ_TABLE[a] / (2**(8-self.o))
                n = self.get_mml_number()
                self.cnt = self.s if n == 0 else n
                duration = self.cnt*self.q*1000/self.fps - 1
                tone(int(freq), int(duration))
                loop = False
            elif c == "R":
                n = self.get_mml_number()
                self.cnt = self.s if n == 0 else n
                loop = False
            elif c == "O":
                self.o = self.get_mml_number()
            elif c == ">":
                self.o += 1
            elif c == "<":
                self.o -= 1
            elif c == "S":
                self.s = self.get_mml_number()
            elif c == "Q":
                self.q = self.get_mml_number() / 8
        self.playing = len(self.mml) > 0

    def get_mml_token(self):
        c = self.mml[0]
        self.mml = self.mml[1:]
        return c

    def get_mml_number(self):
        n = re.search(r"^\d+", self.mml)
        if n is None:
            return 0
        else:
            self.mml = self.mml[n.end():]
            return int(n.group(0))

#------------------------------------------------------------------------------

IMAGE_LOGO = Image(
    b"\x00\x80\xC0\x60\x20\xE0\x20\x20\x40\x80\x00\x00\xFF\x57\xAB\x57" \
    b"\x01\xFF\x20\x20\x40\x80\x00\x00\x00\x80\xC0\x60\x20\xE0\x20\x20" \
    b"\x40\x80\x00\x1F\x37\x6A\x95\xA8\x97\xAC\x94\x4C\x24\x1F\x00\x1F" \
    b"\x35\x6A\x95\xA8\x97\xAC\x94\x4C\x24\x1F\x00\xFF\x97\xAA\x95\x80" \
    b"\xBF\xAC\x94\xAC\x84\xFF", 35, 16)

frames = 0
cur_buttons = 0
last_buttons = 0
sound_on = thumby.audio.enabled
mml_player = None

def start(fps, app_code, app_version, func_table):
    global frames, cur_buttons, last_buttons, mml_player
    thumby.display.setFPS(fps)
    thumby.display.setFont("/Games/Micro2048/obnfont.bin", 5, 6, 1)
    mml_player = MmlPlayer(fps)
    cls()
    blit(IMAGE_LOGO, 18, 12)
    text(app_code, 6, 32)
    text(app_version, 66, 32, TEXT_RIGHT)

    logo_cnt = fps
    state = 0
    prepare = True
    while True:
        last_buttons = cur_buttons
        cur_buttons = thumby.buttonU.pressed()*BTN_U \
                    | thumby.buttonD.pressed()*BTN_D \
                    | thumby.buttonL.pressed()*BTN_L \
                    | thumby.buttonR.pressed()*BTN_R \
                    | thumby.buttonA.pressed()*BTN_A \
                    | thumby.buttonB.pressed()*BTN_B
        if logo_cnt == 0:
            if prepare:
                func_table[state].prepare()
            next_state = func_table[state].update()
            func_table[state].draw()
            prepare = state != next_state
            state = next_state
        else:
            logo_cnt -= 1
        mml_player.update()
        thumby.display.update()
        frames += 1

def cls(color=0):
    thumby.display.fill(color)

def pget(x, y):
    return thumby.display.getPixel(x, y)

def pset(x, y, color=1):
    thumby.display.setPixel(x, y, color)

def line(x1, y1, x2, y2, color=1):
    thumby.display.drawLine(x1, y1, x2, y2, color)

def box(x, y, w, h, color=1, fill=-1):
    if fill != -1:
        thumby.display.drawFilledRectangle(x, y, w, h, fill)
    if color != fill:
        thumby.display.drawRectangle(x, y, w, h, color)

def blit(image, x, y, index=0, key=-1, mirrorX=False, mirrorY=False):
    thumby.display.blit(image.data[index], x - image.cx, y - image.cy, image.w,
                        image.h, key, mirrorX, mirrorY)

def text(str, x, y, align=TEXT_LEFT, color=1):
    thumby.display.drawText(str, x - align*len(str)*3, y, color)

def btn(bits):
    global cur_buttons
    return True if cur_buttons & bits else False

def btn_d(bits):
    global cur_buttons, last_buttons
    return True if cur_buttons & ~last_buttons & bits else False

def btn_u(bits):
    global cur_buttons, last_buttons
    return True if ~cur_buttons & last_buttons & bits else False

def sound(on):
    global sound_on
    sound_on = on
    thumby.audio.set_enabled(on)

def tick():
    tone(440, 10)

def click():
    tone(587, 20)

def tone(freq, ms):
    thumby.audio.play(freq, ms)

def play(mml, priority=0):
    global mml_player
    mml_player.play(mml, priority)

def credit(name, year):
    if len(name) > 12:
        words = name.split(maxsplit=2)
        text(words[0], 6, 6, TEXT_LEFT)
        text(words[1], 66, 12, TEXT_RIGHT)
        y = 22
    else:
        text(name, 36, 9, TEXT_CENTER)
        y = 19
    text(year + "(C)OBONO", 36, y, TEXT_CENTER)
    text("MIT LICENSE", 36, y + 6, TEXT_CENTER)
