import math
import random
z = __import__('/Games/Micro2048/obnlib')

APP_CODE = "#H01"
APP_NAME = "MICRO 2048"
APP_RELEASE = "2022"
APP_VERSION = "V0.1"
APP_FPS = 50

#------------------------------------------------------------------------------

IMAGE_TITLE = z.Image(
    b"\x00\x07\x01\x07\x81\xC7\xE0\xF0\xF7\xF0\xF0\xF7\xF5\xE5\xC5\x05" \
    b"\x00\x87\xC1\xE1\xE1\xF1\xF0\xF7\xF5\xF5\xE5\xC7\x00\x00\x00\x00" \
    b"\x00\x00\x00\x00\x00\x80\xF0\xF0\xF0\xF0\xF0\x10\x00\x00\x80\xC0" \
    b"\xE0\xE0\xF0\xF0\xF0\xF0\xF0\xE0\xE0\x80\x00\x00\x00\x0A\x8B\xC3" \
    b"\xFF\xFF\xFF\x7F\xBF\x5F\x2F\x07\xF1\xFC\xFF\xFF\x7F\x0F\x17\x87" \
    b"\xFF\xFF\xFF\xFF\x3F\x0F\x00\x80\xE0\xF8\x7E\x3E\x9E\xE6\xF8\xFF" \
    b"\xFF\x7F\x1F\x03\x00\x00\xBC\xFF\xFF\xFF\xFF\xE3\xE5\xF1\xFF\xBF" \
    b"\x5F\x2F\x17\x01\xB0\xB8\xBC\xBF\xBF\xBF\xBB\xB9\x5A\x29\x00\x00" \
    b"\x00\x00\x2F\x5F\xBF\xBF\xBC\xBC\x5E\x2F\x2F\x17\x03\x00\x14\x16" \
    b"\x17\x17\x17\x17\xA7\xBF\xBF\xBF\xBF\x5F\x07\x17\x0B\x01\x2C\x5F" \
    b"\xBF\xBF\xBB\xB8\xBA\x5C\x5F\x2F\x17\x0B\x00\x00\x00\x00", 58, 24)

class TitleState:

    ID = 0

    def prepare(self):
        global continuable
        menu_items = [z.Menu.Item("CONTINUE", self.menu_continue),
                      z.Menu.Item("NEW GAME", self.menu_new_game),
                      z.Menu.Item(None,       self.menu_sound),
                      z.Menu.Item("CREDIT",   self.menu_credit)]
        self.menu_item_sound = menu_items[2]
        self.set_sound_menu_label()
        if not continuable:
            menu_items = menu_items[1:]
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
                z.blit(IMAGE_TITLE, 7, 0)
        if not self.credit and (self.dirty or self.menu.dirty):
            self.menu.draw()
        self.dirty = False

    def menu_continue(self):
        self.start = True

    def menu_new_game(self):
        global continuable
        continuable = False
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

FIELD_SIZE = 4
RAND_RANGE = 720720

UNIT_W = 16
UNIT_H = 10
PANEL_W = UNIT_W - 1
PANEL_H = UNIT_H - 1
IMAGE_PANEL = z.Image([
    b"\x00\x00\x00\x00\xC6\xE7\xF3\xB3\xB3\xBF\x9E\x00\x00\x00\x00" \
    b"\x00\x00\x00\x00\x01\x01\x01\x01\x01\x01\x01\x00\x00\x00\x00",
    b"\x00\x00\x00\x00\x70\x7C\x6E\x67\xFF\xFF\x60\x00\x00\x00\x00" \
    b"\x00\x00\x00\x00\x00\x00\x00\x00\x01\x01\x00\x00\x00\x00\x00",
    b"\x00\x00\x00\x00\xEE\xFF\x9B\x9B\x9B\xFF\xEE\x00\x00\x00\x00" \
    b"\x00\x00\x00\x00\x00\x01\x01\x01\x01\x01\x00\x00\x00\x00\x00",
    b"\x00\x00\x04\xFE\xFF\x00\xFE\xFF\x9B\x9B\xFB\xF0\x00\x00\x00" \
    b"\x00\x00\x00\x01\x01\x00\x00\x01\x01\x01\x01\x00\x00\x00\x00",
    b"\x00\xC6\xC7\x93\xBB\xFF\xEE\x00\xC6\xE7\xF3\xBB\x9F\x8E\x00" \
    b"\x00\x00\x01\x01\x01\x01\x00\x00\x01\x01\x01\x01\x01\x01\x00",
    b"\x00\xFE\xFF\x9B\x9B\xFB\xF0\x00\x70\x78\x6C\x66\xFF\xFF\x60" \
    b"\x00\x00\x01\x01\x01\x01\x00\x00\x00\x00\x00\x00\x01\x01\x00",
    b"\x00\x04\xFE\xFF\x00\xCC\xE6\xBE\x9C\x00\xEC\xB6\xFE\xEC\x00" \
    b"\x00\x00\x01\x01\x00\x01\x01\x01\x01\x00\x00\x01\x01\x00\x00",
    b"\x00\xC6\xE7\xB3\x9F\x8E\x00\xBE\xB6\xF6\x00\xFC\x96\xF6\x00" \
    b"\x00\x01\x01\x01\x01\x01\x00\x01\x01\x00\x00\x01\x01\x00\x00",
    b"\x00\x9F\x9F\x9B\xFB\xF3\x08\xFC\xFE\x00\xCC\xE6\xBE\x9C\x00" \
    b"\x00\x01\x01\x01\x01\x00\x00\x01\x01\x00\x01\x01\x01\x01\x00",
    b"\x04\xFE\xFF\x00\xF8\x98\xF8\x00\xEC\xAC\xBC\x00\xE0\xD8\xFC" \
    b"\x00\x01\x01\x00\x01\x01\x01\x00\x01\x01\x01\x00\x00\x00\x01",
    b"\xF3\xBB\x9F\x00\xF8\x98\xF8\x00\xE0\xD8\xFC\x00\xFC\xAC\xFC" \
    b"\x01\x01\x01\x00\x01\x01\x01\x00\x00\x00\x01\x00\x01\x01\x01",
    b"\x78\x66\xFF\x00\xF8\x98\xF8\x00\xBC\xAC\xFC\x00\xFC\xAC\xEC" \
    b"\x00\x00\x01\x00\x01\x01\x01\x00\x01\x01\x01\x00\x01\x01\x01",
    b"\x00\xFF\x9B\xFF\x00\xFC\x00\xBC\xAC\xFC\x00\xEC\xAC\xBC\x00" \
    b"\x00\x01\x01\x01\x00\x01\x00\x01\x01\x01\x00\x01\x01\x01\x00",
    b"\x55\x00\x01\x00\x01\x00\x01\x00\x01\x00\x01\x00\x01\x00\x55" \
    b"\x01\x00\x01\x00\x01\x00\x01\x00\x01\x00\x01\x00\x01\x00\x01",
    b"\xAA\x01\x00\x01\x00\x01\x00\x01\x00\x01\x00\x01\x00\x01\xAA" \
    b"\x00\x01\x00\x01\x00\x01\x00\x01\x00\x01\x00\x01\x00\x01\x00"],
    PANEL_W, PANEL_H)

UP_MML = ["O5Q8S1DF+",
          "O5Q8S1FA>C+",
          "O5Q8S1A+>D+G+>C+",
          "O5Q8S2<A>A>A<C>C>C<<F>F>F",
          "O5Q8S2<B>B>B<D>D>D<<G>G>G",
          "O5Q8S2C>C>C<<E>E>E<<G>G>G<C>C>C",
          "O5Q8S3<G>C<A>D<B>ECF",
          "O5Q8S3<A>C+EA<B>DF+B",
          "O5Q8S3<B>D+F+FD+FF+",
          "O5Q8S4CGEGAFBG>C6",
          "O5Q8S4DFAFDGBG>D6",
          "O5Q8S4EF+A+>E<EGB>F+E6",
          "O5Q8S4FF+DD+AA+GG+>D+6"]

class GameState:

    ID = 1

    def __init__(self):
        global continuable
        continuable = False

    def prepare(self):
        global continuable
        if not continuable:
            self.field = Field()
            self.field.add_new_panel()
            self.field.add_new_panel()
            self.work = None
            self.backup = None
            self.anim = 0
            self.gameover = False
            continuable = True
        self.idle = 0
        self.undo_msg = 0
        self.shake = 0.0
        z.play("O4S6CDEFG12", 20)

    def update(self):
        next_state = self.ID
        self.idle += 1
        if self.undo_msg > 0:
            self.undo_msg -= 1
        if self.shake > 0.0:
            self.shake -= 0.25
        if self.anim == 0:
            vx = z.btn_d(z.BTN_R) - z.btn_d(z.BTN_L)
            vy = z.btn_d(z.BTN_D) - z.btn_d(z.BTN_U)
            if z.btn_d(z.BTN_A) and self.backup is not None:
                self.field = self.backup
                self.backup = None
                self.anim = 5
                self.gameover = False
                self.undo_msg = 25
                self.shake = 0.0
                z.play("O4S4>C<GE", 15)
            elif z.btn_d(z.BTN_B):
                global continuable
                continuable = not self.gameover
                next_state = TitleState.ID
                z.click()
            elif (vx != 0 and vy == 0) or (vx == 0 and vy != 0):
                f = self.idle < APP_FPS*3 and not self.gameover
                self.idle = 0
                if f:
                    self.work = self.field.get_slid_field(vx, vy)
                    if self.work is not None:
                        self.anim = 1
                        self.undo_msg = 0
                        z.tick()
        else:
            self.idle = 0
            self.anim += 1
            if self.anim == 5:
                self.backup = self.field
                self.field = self.work
                self.work = None
                self.field.add_new_panel()
                value, high = self.field.upgrade_panels()
                if value >= 0:
                    z.play(UP_MML[value], value)
                    if high and value >= 6:
                        self.shake = value - 4
            elif self.anim == 8:
                if not self.field.is_playable():
                    self.gameover = True
                    self.idle = APP_FPS
                    z.play("O4S6ED+DS8C+C<BS12A+A", 20)
                self.anim = 0
        return next_state

    def draw(self):
        z.cls()
        self.field.draw_panels(self.anim, self.shake)
        if self.idle >= APP_FPS*3 or (self.gameover and self.idle >= APP_FPS):
            s = str(self.field.score)
            z.box(0, 0, len(s)*6 + 1, 7, 1, 1)
            z.text(s, 1, 1, color=0)
            if self.gameover:
                z.box(23, 33, 49, 7, 1, 1)
                z.text("GAMEOVER", 24, 34, color=0)
        if self.undo_msg > 0:
            z.box(47, 33, 25, 7, 1, 1)
            z.text("UNDO", 48, 34, color=0)


class Panel:

    VALUE_MAX = 13

    def __init__(self, value, up=False, fresh=False):
        self.value = value
        self.up = up
        self.fresh = fresh
        self.move = 0

class Field:

    def __init__(self, src=None):
        self.panels = [[None]*FIELD_SIZE for i in self.field_range()]
        self.vx = 0
        self.vy = 0
        self.empty = FIELD_SIZE ** 2
        self.playable = True
        if src is None:
            self.score = 0
            self.value_max = 0
            self.add_pos = random.randrange(RAND_RANGE)
            self.add_4 = False
        else:
            self.score = src.score
            self.value_max = src.value_max
            self.add_pos =  src.add_pos
            self.add_4 = src.add_4

    def field_range(self, reverse=False):
        if reverse:
            return range(FIELD_SIZE-1, -1, -1)
        else:
            return range(FIELD_SIZE)

    def is_inside(self, x, y):
        return 0 <= x < FIELD_SIZE and 0 <= y < FIELD_SIZE

    def is_playable(self):
        for py in self.field_range():
            for px in self.field_range():
                p = self.panels[py][px]
                if p is None:
                    return True
                else:
                    for vx, vy in zip([-1,1,0,0], [0,0,-1,1]):
                        x = px + vx
                        y = py + vy
                        if self.is_inside(x, y):
                            n = self.panels[y][x]
                            if n is None or p.value == n.value:
                                return True
        return False

    def get_slid_field(self, vx, vy):
        self.vx = vx
        self.vy = vy
        result = Field(self)
        moved = False
        for py in self.field_range(vy > 0):
            for px in self.field_range(vx > 0):
                p = self.panels[py][px]
                if p is not None:
                    p.move = result.put_slid_panel(px, py, vx, vy, p.value)
                    moved = moved or p.move > 0
        return result if moved else None

    def put_slid_panel(self, px, py, vx, vy, value):
        move = 0
        up = False
        loop = True
        while loop:
            x = px + vx*(move+1)
            y = py + vy*(move+1)
            if self.is_inside(x, y):
                n = self.panels[y][x]
                if n is None:
                    move += 1
                else:
                    loop = False
                    if n.value == value and not n.up:
                        move += 1
                        up = True
            else:
                loop = False
        self.panels[py + vy*move][px + vx*move] = Panel(value, up)
        if not up:
            self.empty -= 1
        return move

    def add_new_panel(self):
        x = 0
        y = 0
        count = self.add_pos % self.empty
        while count > 0 or self.panels[y][x] is not None:
            if self.panels[y][x] is None:
                count -= 1
            x += 1
            if x == FIELD_SIZE:
                y += 1
                x = 0
        self.panels[y][x] = Panel(1 if self.add_4 else 0, fresh=True)
        self.empty -= 1
        self.add_pos = random.randrange(RAND_RANGE)
        self.add_4 = random.random() < 0.1

    def upgrade_panels(self):
        value = -1
        high = False
        for py in self.field_range():
            for px in self.field_range():
                p = self.panels[py][px]
                if p is not None and p.up:
                    self.score += 2 ** (p.value+2)
                    if value < p.value:
                        value = p.value
                    if p.value < Panel.VALUE_MAX - 1:
                        p.value += 1
                    if self.value_max < p.value:
                        self.value_max = p.value
                        high = True
        return value, high

    def draw_panels(self, anim=0, shake=0.0):
        d = random.random() * math.pi * 2.0
        sx = math.cos(d) * shake
        sy = math.sin(d) * shake
        m = 1 - (5-anim)**2/25 if 0 < anim < 5 else 0
        u = anim == 5
        f = 8 - anim if 5 <= anim <= 7 else 0
        for py in self.field_range():
            for px in self.field_range():
                p = self.panels[py][px]
                if p is not None:
                    coeff = p.move * m
                    x = int((px+self.vx*coeff)*UNIT_W + sx + 0.5) + 4
                    y = int((py+self.vy*coeff)*UNIT_H + sy + 0.5)
                    if p.up and u:
                        z.box(x - 1, y - 1, PANEL_W + 2, PANEL_H + 2, 1, 1)
                    elif p.fresh and f > 0:
                        z.box(x + f, y + f, PANEL_W - f*2, PANEL_H - f*2)
                    else:
                        self.draw_panel(x, y, p.value)

    def draw_panel(self, x, y, value):
        z.blit(IMAGE_PANEL, x, y, value)
        z.blit(IMAGE_PANEL, x, y, Panel.VALUE_MAX + (z.frames+x+y)%2, 0)

#------------------------------------------------------------------------------

z.start(APP_FPS, APP_CODE, APP_VERSION, [TitleState(), GameState()])
