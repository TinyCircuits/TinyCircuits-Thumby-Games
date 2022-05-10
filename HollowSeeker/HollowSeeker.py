import math
import random
z = __import__('/Games/HollowSeeker/obnlib')

APP_CODE = "#H02"
APP_NAME = "HOLLOW SEEKER"
APP_RELEASE = "2022"
APP_VERSION = "V0.1"
APP_FPS = 50

last_score = 0

#------------------------------------------------------------------------------

IMAGE_TITLE = z.Image(\
    b"\xFF\xFF\xFF\x30\x30\x30\x30\xFF\xFF\xFF\x00\xE0\xF0\xF8\x18\x18" \
    b"\x18\xF8\xF0\xE0\x00\xFF\xFF\xFF\x00\xFF\xFF\xFF\x00\xE0\xF0\xF8" \
    b"\x18\x18\x18\xF8\xF0\xE0\x00\x18\xF8\xF8\xF8\x00\xF0\x38\xF8\xF8" \
    b"\xC0\xF0\xF8\x18\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00" \
    b"\x00\x00\x00\x00\x00\x00\x07\x87\xC7\xE0\xE0\xE0\xF0\xF7\xF7\xF7" \
    b"\xF0\xF1\xE3\xC7\x06\x06\x06\x07\x03\x01\x00\xC7\xE7\xF7\x30\x37" \
    b"\x77\x07\x00\x01\x03\x87\x86\x86\x86\x07\x03\x01\x00\x00\x81\x87" \
    b"\x87\x87\x01\x00\x01\xF7\xF7\xF7\x01\x80\x80\x80\x80\x00\x00\x80" \
    b"\x80\x80\x80\x00\x00\x00\x80\x80\x80\x00\x80\x80\x00\x03\x07\x1F" \
    b"\x7F\xFF\xFF\xFF\x71\x3F\x3F\x7F\x78\x7F\x3F\x00\x00\x00\x00\x00" \
    b"\x00\x71\x63\x67\x67\x7F\x3E\x1C\x00\x1E\x3F\x7F\x6D\x6D\x6F\x6F" \
    b"\x0E\x00\x1E\x3F\x7F\x6D\x6D\x6F\x6F\x0E\x00\x7F\x7F\x7F\x0C\x7F" \
    b"\x7F\x73\x40\x1E\x3F\x7F\x6D\x6D\x6F\x6F\x0E\x00\x7F\x7F\x7F\x01" \
    b"\x01\x01", 70, 24)

class TitleState:

    ID = 0

    def prepare(self):
        menu_items = [z.Menu.Item("START GAME", self.menu_start_game),
                      z.Menu.Item(None,         self.menu_sound),
                      z.Menu.Item("CREDIT",     self.menu_credit)]
        self.menu_item_sound = menu_items[1]
        self.set_sound_menu_label()
        self.menu = z.Menu(menu_items)
        self.start = False
        self.credit = False
        self.dirty = True

    def update(self):
        if self.credit:
            if z.btn_d(z.BTN_A|z.BTN_B):
                self.credit = False
                self.dirty = True
                z.click()
        else:
            self.menu.update()
        return GameState.ID if self.start else self.ID

    def draw(self):
        if self.dirty:
            z.cls()
            if self.credit:
                z.credit(APP_NAME, APP_RELEASE)
            else:
                z.blit(IMAGE_TITLE, 1, 0)
                global last_score
                if last_score > 0:
                    z.text(str(last_score), z.SCRN_W + 1, 0, z.TEXT_R, 1, True)

        if not self.credit and (self.dirty or self.menu.dirty):
            self.menu.draw()
        self.dirty = False

    def menu_start_game(self):
        self.start = True

    def menu_sound(self):
        z.sound(not z.sound_on)
        self.set_sound_menu_label()
        z.click()

    def menu_credit(self):
        self.credit = True
        self.dirty = True
        z.click()

    def set_sound_menu_label(self):
        label = "SOUND " + ("ON" if z.sound_on else "OFF") 
        self.menu_item_sound.label = label


#------------------------------------------------------------------------------

UNIT = 5

IMAGE_PLAYER = z.Image([
    b"\x03\x1F\x0F\x19\x0E",
    b"\x13\x0F\x0F\x09\x1E",
    b"\x16\x1E\x1E\x12\x1C",
    b"\x03\x1F\x0F\x1B\x0E",
    b"\x03\x0F\x1F\x09\x0E"], 5, 5)

class GameState:

    ID = 1

    def prepare(self):
        global last_score
        last_score = 0
        self.cave = Cave()
        self.player = Player()
        self.dots = Dots()
        self.pause = False
        self.gameover = False
        self.counter = APP_FPS * 2
        self.dirty = True
        z.play("O4S6CDEFG12", 3)

    def update(self):
        next_state = self.ID
        dir = 0
        forward = 0.0
        if self.counter == 0:
            dir = (z.btn(z.BTN_R) or z.btn(z.BTN_A)) - z.btn(z.BTN_L)
            forward = 1.0
            if z.btn_d(z.BTN_B):
                self.pause = not self.pause
                self.dirty = True
        else:
            self.counter -= 1
            if self.gameover:
                forward = 0.5
                if z.btn_d(z.BTN_A):
                    self.prepare()
                elif z.btn_d(z.BTN_B) or self.counter == 0:
                    next_state = TitleState.ID
            else:
                dir = 1
        if not self.pause and z.frames & 1:
            self.dirty = True
            self.cave.update(forward)
            self.player.update(self.cave, dir)
            if forward > 0:
                self.dots.update(self.cave)
            if self.cave.phase >= Cave.PHASE_SHAKE:
                z.tone(random.randint(40, 100), 40)
            if self.player.move == UNIT - 1 and self.counter == 0:
                z.play("O6S1DBF", 1)
            if not self.gameover and self.player.dead:
                global last_score
                last_score = self.cave.score
                self.gameover = True
                self.counter = APP_FPS * 8
                z.play("O4S6ED+DS8C+C<BS12A+A", 2)
        return next_state

    def draw(self):
        if not self.dirty:
            return
        z.cls()
        self.cave.draw()
        self.player.draw(self.cave)
        self.dots.draw()
        if self.gameover:
            z.text("GAMEOVER", 36, 0, z.TEXT_C, 1, True)
            z.text("SCORE " + str(self.cave.score), 36, 35, z.TEXT_C, 1, True)
        elif self.counter > 0:
            z.text("READY?", 36, 10, z.TEXT_C, 1, True)
        elif self.pause:
            z.text("PAUSE", 36, 10, z.TEXT_C, 1, True)
        elif self.player.pos >= Cave.COLUMN_MID - 1:
            z.text(str(self.cave.score), 0, 0, z.TEXT_L, 1, True)
        self.dirty = False


class Cave:

    HEIGHT = z.SCRN_H
    GAP_MAX_INIT = HEIGHT / 2
    COLUMN_MAX = 16
    COLUMN_MID = COLUMN_MAX // 2
    PHASE_MAX = 256
    PHASE_SHAKE = PHASE_MAX - 12

    def __init__(self):
        self.score = 0
        self.hollow_cnt = 2
        self.columns = []
        top = self.HEIGHT/2
        bottom = top + Player.HEIGHT
        for _ in range(self.COLUMN_MID):
            self.columns.append(Column(top, bottom))
        for _ in range(self.COLUMN_MID, self.COLUMN_MAX):
            self.add_column()
        self.phase = 0
        self.gap_max = self.GAP_MAX_INIT
        self.gap = 0
        self.base_top = 0
        self.base_bottom = 0
        self.offset = 0

    def update(self, forward):
        self.gap = int((1.0 - math.cos(self.phase*math.pi*2.0/self.PHASE_MAX))
                       * self.gap_max / 2.0)
        self.base_bottom = self.gap // 2
        self.base_top = self.base_bottom - self.gap
        self.phase += forward
        if self.phase >= self.PHASE_MAX:
            self.phase = 0
            self.gap_max += 0.5
        elif self.phase >= self.PHASE_SHAKE and self.phase % 2 < 1:
            self.base_top += 1
            self.base_bottom += 1

    def add_column(self):
        c = self.columns[-1]
        last_diff = c.bottom - c.top
        diff = random.randrange(2)
        self.hollow_cnt -= 1
        if self.hollow_cnt <= 0:
            diff = Player.HEIGHT - diff
            self.hollow_cnt = random.randint(2 + self.score//128,
                                             2 + self.score//64)
        adjust = (c.bottom - (self.HEIGHT+Player.HEIGHT)/2 + 1.5) // 3
        r = Player.HEIGHT*2 + 1 - abs(diff - last_diff) - abs(adjust)
        bottom = c.bottom + random.randrange(int(r)) - Player.HEIGHT
        if diff > last_diff:
            bottom += diff - last_diff
        if adjust < 0:
            bottom -= adjust
        self.columns.append(Column(bottom - diff, bottom))

    def draw(self):
        for i, c in enumerate(self.columns):
            x = int(i*UNIT - self.offset)
            top = int(self.base_top + c.top - 1)
            bottom = int(self.base_bottom + c.bottom)
            if i > 0:
                if top < last_top:
                    z.line(x - 1, top, x - 1, last_top)
                if top > last_top:
                    z.line(x, last_top, x, top)
                if bottom < last_bottom:
                    z.line(x, bottom, x, last_bottom)
                if bottom > last_bottom:
                    z.line(x - 1, last_bottom, x - 1, bottom)
            z.line(x, top, x + 4, top)
            z.line(x, bottom, x + 4, bottom)
            z.pset(x + c.tx, top - c.ty)
            z.pset(x + c.bx, bottom + c.by)
            last_top = top
            last_bottom = bottom


class Column:

    def __init__(self, top, bottom):
        self.top = top
        self.bottom = bottom
        self.tx = random.randrange(UNIT)
        self.ty = random.randrange(Cave.HEIGHT // 2)
        self.bx = random.randrange(UNIT)
        self.by = random.randrange(Cave.HEIGHT // 2)


class Player:

    HEIGHT = IMAGE_PLAYER.h

    def __init__(self):
        self.dir = 0
        self.pos = 0
        self.jump = 0
        self.move = 0
        self.dead = False

    def update(self, cave, dir):
        if self.dead:
            return
        c = cave.columns[self.pos]
        if dir != 0 and self.move == 0 and self.pos + dir >= 0:
            self.dir = dir
            c = cave.columns[self.pos]
            n = cave.columns[self.pos + dir]
            diff = min(c.bottom, n.bottom) - max(c.top, n.top)
            if diff + cave.gap >= Player.HEIGHT:
                self.pos += dir
                self.move = UNIT
                self.jump = c.bottom - n.bottom
                c = n
        if self.move > 0:
            self.move -= 1
            if self.pos >= Cave.COLUMN_MID:
                cave.offset += 1
                if self.move == 0:
                    cave.score += 1
                    cave.offset -= UNIT
                    cave.columns.pop(0)
                    cave.add_column()
                    self.pos -= 1
        if cave.phase == 0 and c.bottom - c.top < self.HEIGHT/2:
            self.dead = True

    def draw(self, cave):
        c = cave.columns[self.pos]
        x = self.pos*UNIT - self.move*self.dir - cave.offset
        if self.dead:
            y = cave.base_bottom + c.top
        else:
            y = cave.base_bottom + c.bottom + self.jump*self.move/UNIT + 0.5
            if y > z.SCRN_H:
                y = z.SCRN_H
            y -= self.HEIGHT
            if cave.base_top + c.top > y:
                y = cave.base_top + c.top
        z.blit(IMAGE_PLAYER, int(x), int(y), self.move, 0, self.dir<0)


class Dots:

    def __init__(self):
        self.dots = []
        self.offset = 0

    def update(self, cave):
        scroll = 1 if self.offset != cave.offset else 0
        self.offset = cave.offset
        base = cave.base_bottom
        for d in reversed(self.dots):
            if d.update(scroll, base):
                self.dots.remove(d)
        if random.random() > cave.phase/Cave.PHASE_MAX + 0.25:
            x = random.randrange(z.SCRN_W)
            c = cave.columns[(x+cave.offset) // UNIT]
            self.dots.append(Dot(x, c.top + cave.base_top - 1, c.bottom))

    def draw(self):
        for d in self.dots:
            d.draw()


class Dot:

    def __init__(self, x, y, b):
        self.x = x
        self.y = y
        self.b = b
        self.v = 0

    def update(self, scroll, base):
        self.x -= scroll
        self.y += self.v
        self.v += 0.125
        return self.x < 0 or self.y >= self.b + base

    def draw(self):
        z.pset(self.x, int(self.y))

#------------------------------------------------------------------------------

if z.check(0.02):
    z.start(APP_FPS, APP_CODE, APP_VERSION, [TitleState(), GameState()])
