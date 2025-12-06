# RexyRunner.py
# Rexy Runner for Thumby (72x40 OLED)
# Save to: /Games/RexyRunner/RexyRunner.py
# Run: execfile('/Games/RexyRunner/RexyRunner.py')

import thumby
import random

# Try to import ujson (MicroPython), fall back to json if needed
try:
    import ujson as jsonmod
except ImportError:
    import json as jsonmod

# -------------------------------
# Persistent High Score Storage
# -------------------------------
SAVE_FILE = "/Games/RexyRunner/RexyRunnerSave.json"

def load_hiscore():
    try:
        with open(SAVE_FILE, "r") as f:
            data = jsonmod.load(f)
        if isinstance(data, dict) and "hiscore" in data:
            return int(data["hiscore"])
    except:
        pass
    return 0

def save_hiscore(hiscore):
    try:
        with open(SAVE_FILE, "w") as f:
            jsonmod.dump({"hiscore": int(hiscore)}, f)
    except:
        # Fail silently if writing is not possible
        pass

# -------------------------------
# Display / Timing
# -------------------------------
SCREEN_W = 72
SCREEN_H = 40
WHITE = 1
BLACK = 0

FG_COLOR = WHITE
BG_COLOR = BLACK

def set_theme(night):
    global FG_COLOR, BG_COLOR
    if night:
        FG_COLOR = BLACK
        BG_COLOR = WHITE
    else:
        FG_COLOR = WHITE
        BG_COLOR = BLACK

thumby.display.setFPS(20)  # 20 FPS

# -------------------------------
# Screen States
# -------------------------------
STATE_LOADING = 0
STATE_TITLE = 1
STATE_PLAYING = 2
STATE_GAMEOVER_MENU = 3

# -------------------------------
# Gameplay Tuning
# -------------------------------
GROUND_PAD = 0
GROUND_Y = SCREEN_H - GROUND_PAD - 1

GRAVITY = 0.45
JUMP_VELOCITY = -6.0

# Game scroll speed: original pace, auto-accel with distance
SPEED_START = 1.55
SPEED_MAX = 3.6
ACCELERATION = 0.0009

MIN_GAP = 22
GAP_COEFF = 0.65
SPAWN_PROB = 0.035

ACHIEVEMENT_EVERY = 50

# -------------------------------
# Safe beep
# -------------------------------
def beep(freq=520, ms=50):
    try:
        thumby.audio.play(freq, ms)
    except:
        pass

# -------------------------------
# Draw helpers
# -------------------------------
def draw_rows(d, x, y, rows, color=None):
    if not rows:
        return
    if color is None:
        color = FG_COLOR
    h = len(rows)
    w = len(rows[0])
    for ry in range(h):
        yy = y + ry
        if yy < 0 or yy >= SCREEN_H:
            continue
        row = rows[ry]
        for rx in range(w):
            if row[rx] == '1':
                xx = x + rx
                if 0 <= xx < SCREEN_W:
                    d.setPixel(xx, yy, color)

def rows_size(rows):
    return (len(rows[0]), len(rows)) if rows else (0, 0)

def aabb(ax, ay, aw, ah, bx, by, bw, bh):
    return (ax < bx + bw and ax + aw > bx and ay < by + bh and ay + ah > by)

# -------------------------------
# Sprites - Dino (updated)
# -------------------------------
DINO_STAND = [
    "00000000000111111110",
    "00000000001100111111",
    "00000000001100111111",
    "00000000001111111111",
    "00000000001111111110",
    "00000000111111111000",
    "00000001111111110000",
    "00000011111111110000",
    "00000111111111111000",
    "11001111111110000000",
    "01111111111110000000",
    "00011111111110000000",
    "00000111001110000000",
    "00000110001110000000",
    "00000110000110000000",
    "00000111000111000000",
]

DINO_RUN_1 = [
    "00000000000111111110",
    "00000000001100111111",
    "00000000001100111111",
    "00000000001111111111",
    "00000000001111111110",
    "00000000111111111000",
    "00000001111111110000",
    "00000011111111110000",
    "00000111111111111000",
    "11001111111110000000",
    "01111111111110000000",
    "00011111111110000000",
    "00000111001110000000",
    "00000111001110000000",
    "00000000000110000000",
    "00000000000111000000",
]

DINO_RUN_2 = [
    "00000000000000000000",
    "00000000000111111110",
    "00000000001100111111",
    "00000000001100111111",
    "00000000001111111111",
    "00000000001111111110",
    "00000000111111111000",
    "00000011111111110000",
    "00000111111111111000",
    "11001111111110000000",
    "01111111111110000000",
    "00011111111110000000",
    "00000111001110000000",
    "00000110000111000000",
    "00000110000000000000",
    "00000111000000000000",
]

# Crash sprite widened to 17x16 to match run width
DINO_CRASH = [
    "01111111000000010",
    "01111110001111110",
    "01111110100111100",
    "01111111111111100",
    "01111111111111100",
    "01011110111111010",
    "00011100111000010",
    "00100011111111110",
    "00110111111011110",
    "00111111111001110",
    "01111111111011110",
    "01011111111111110",
    "01111111100111110",
    "01110110100111110",
    "01110111101111110",
    "01110101110111110",
]

# Wider, shorter duck sprites (24x10)
DINO_DUCK_1 = [
    "000000000000000000000000",
    "000000000000000000000000",
    "000000000000000000000000",
    "111100111111110111111110",
    "111111111111111111111111",
    "011111111111111111111111",
    "000111111111111111111111",
    "000001111111111011111100",
    "000011111100111100000000",
    "000000011100000000000000",
]

DINO_DUCK_2 = [
    "000000000000000000000000",
    "000000000000000000000000",
    "111101111111110111111110",
    "111111111111111111111110",
    "111111111111111111111110",
    "011111111111111111111110",
    "000111111111111111111110",
    "000011111111111000000000",
    "000011100001111000000000",
    "000011100000000000000000",
]

# -------------------------------
# Sprites - Cacti (updated small variants)
# -------------------------------
CACTUS_SMALL_1 = [
    "00100",
    "00100",
    "10100",
    "10101",
    "11111",
    "01110",
    "01110",
    "00110",
    "00110",
    "00110",
]

CACTUS_SMALL_2 = [
    "0010000100",
    "0010000100",
    "1010000101",
    "1010100101",
    "1011010101",
    "1111011101",
    "1111001111",
    "0011000110",
    "0011000110",
    "0011000110",
]

CACTUS_SMALL_3 = [
    "001000010000100",
    "001000010000100",
    "101010011000101",
    "101101011010101",
    "101101011010101",
    "011101111010101",
    "011111111101111",
    "001100011000110",
    "001100011000110",
    "001100011000110",
]

CACTUS_LARGE_1 = [
    "001100",
    "001100",
    "001100",
    "001100",
    "101101",
    "101101",
    "011110",
    "011111",
    "011110",
    "001100",
    "001100",
    "001100",
]

CACTUS_LARGE_2 = [
    "000110001100",
    "000110001100",
    "000110001100",
    "000110001100",
    "100110101101",
    "110111111101",
    "011110011111",
    "101110111110",
    "111111011100",
    "000110001100",
    "000110001100",
    "000110001100",
]

CACTUS_LARGE_3 = [
    "000010000010000",
    "000011000010000",
    "000011000110000",
    "000011000110000",
    "100011010110001",
    "010011010111001",
    "011011110111011",
    "011111111111111",
    "001111111111110",
    "000011000110000",
    "000011000110000",
    "000011000110000",
]

# Extra ultra-thin cacti
CACTUS_THIN_1 = [
    "010",
    "010",
    "010",
    "111",
    "010",
    "010",
    "010",
    "110",
]

CACTUS_THIN_2 = [
    "101",
    "101",
    "101",
    "111",
    "010",
    "010",
    "010",
    "111",
]

# -------------------------------
# Sprites - Clouds
# -------------------------------
CLOUD = [
    "00000000011111000000",
    "00000001100001000000",
    "00000001000001011000",
    "00011110000000000110",
    "00100000000000000011",
    "10001111111111111111",
]

CLOUD_SMALL = [
    "00000111110000",
    "00011000001100",
    "00100000000010",
    "01000000000001",
    "11111111111111",
]

# -------------------------------
# Sprites - Ground tiles
# -------------------------------
GROUND_TILE_1 = [
    "000000000010000000000",
    "000001000000001000000",
    "000000000000000010000",
    "111111111111111111111",
]

GROUND_TILE_2 = [
    "000000100000000100000",
    "000000000010000000000",
    "000010000000000000000",
    "111111111111111111111",
]

GROUND_TILE_3 = [
    "000000000000000000000",
    "000000000000001000000",
    "000000000000001000000",
    "111111111111111111111",
]

GROUND_TILES = [GROUND_TILE_1, GROUND_TILE_2, GROUND_TILE_3]
GTW, GTH = rows_size(GROUND_TILES[0])

# -------------------------------
# Sprites - Pterodactyl
# -------------------------------
PTERO_1 = [
    "0000000000000000",
    "0000100000000000",
    "0011101111111100",
    "1111111111111111",
    "0000011111111100",
    "0000001110001100",
    "0000000110000000",
    "0000000000000000",
]

PTERO_2 = [
    "0000000000000000",
    "0000000011000000",
    "0000000111100000",
    "0000101111110000",
    "0011101111111100",
    "1111111111111111",
    "0000000001111100",
    "0000000000110000",
]

# -------------------------------
# Player Class
# -------------------------------
class Trex:
    START_X = 10

    def __init__(self):
        self.x = Trex.START_X
        self.y = GROUND_Y - rows_size(DINO_STAND)[1]
        self.vy = 0.0
        self.jumping = False
        self.ducking = False
        self.crashed = False
        self.tick = 0

        self.run_frames = [DINO_RUN_1, DINO_RUN_2]
        self.duck_frames = [DINO_DUCK_1, DINO_DUCK_2]
        self.jump_rows = DINO_STAND
        self.crash_rows = DINO_CRASH

    def current_rows(self):
        if self.crashed:
            return self.crash_rows

        # Shared frame index so run and duck animate at the same rate
        idx = (self.tick // 5) % len(self.run_frames)

        if self.jumping:
            # Allow duck animation while jumping if duck is held
            if self.ducking:
                return self.duck_frames[idx]
            return self.jump_rows

        # On the ground: duck vs run
        if self.ducking:
            return self.duck_frames[idx]
        return self.run_frames[idx]

    def current_size(self):
        return rows_size(self.current_rows())

    def ground_top_y(self, h):
        return GROUND_Y - h

    def start_jump(self):
        if not self.jumping and not self.crashed:
            self.jumping = True
            self.vy = JUMP_VELOCITY
            beep(650, 40)

    def end_jump_early(self):
        if self.jumping and self.vy < -2.0:
            self.vy = -2.0

    def speed_drop(self):
        if self.jumping:
            self.vy = max(self.vy, 2.6)
            beep(400, 40)

    def set_duck(self, pressed):
        self.ducking = pressed and not self.crashed

    def update(self, run_speed):
        if self.crashed:
            return
        _, h = self.current_size()
        if self.jumping:
            self.y += self.vy
            self.vy += GRAVITY
            gy = self.ground_top_y(h)
            if self.y >= gy:
                self.y = gy
                self.vy = 0.0
                self.jumping = False
        else:
            self.y = self.ground_top_y(h)
            # Animation tick: starts a bit faster now, speeds up further as run_speed grows
            extra = max(0.0, run_speed - SPEED_START)
            anim_step = 2 + int(extra * 1.5)  # 2 at start, higher as speed increases
            self.tick = (self.tick + anim_step) & 0xFF

    def draw(self, d):
        draw_rows(d, int(self.x), int(self.y), self.current_rows())

    def bbox(self):
        w, h = self.current_size()
        return (int(self.x), int(self.y), w, h)

    def reset(self):
        self.vy = 0.0
        self.jumping = False
        self.ducking = False
        self.crashed = False
        self.tick = 0
        self.y = self.ground_top_y(rows_size(DINO_STAND)[1])

# -------------------------------
# Obstacles, Clouds, Ground, Fliers
# -------------------------------
class Obstacle:
    def __init__(self, small=True, multi=1, thin=False):
        if thin:
            self.rows = CACTUS_THIN_1 if random.random() < 0.5 else CACTUS_THIN_2
        else:
            self.rows = (
                CACTUS_SMALL_1 if small and multi == 1 else
                CACTUS_SMALL_2 if small and multi == 2 else
                CACTUS_SMALL_3 if small and multi == 3 else
                CACTUS_LARGE_1 if (not small and multi == 1) else
                CACTUS_LARGE_2 if (not small and multi == 2) else
                CACTUS_LARGE_3
            )
        self.w, self.h = rows_size(self.rows)
        self.x = SCREEN_W
        self.y = GROUND_Y - self.h
        self.remove = False

    def update(self, speed):
        self.x -= speed
        if self.x + self.w < 0:
            self.remove = True

    def draw(self, d):
        draw_rows(d, int(self.x), int(self.y), self.rows)

    def bbox(self):
        return (int(self.x), int(self.y), self.w, self.h)

class Cloud:
    def __init__(self):
        if random.random() < 0.45:
            self.rows = CLOUD_SMALL
        else:
            self.rows = CLOUD
        self.w, self.h = rows_size(self.rows)
        self.x = SCREEN_W
        self.y = random.randint(6, 18)
        self.remove = False

    def update(self, speed):
        self.x -= max(0.30, speed * 0.35)
        if self.x + self.w < 0:
            self.remove = True

    def draw(self, d):
        draw_rows(d, int(self.x), int(self.y), self.rows)

class Pterodactyl:
    def __init__(self, y_level):
        self.frames = [PTERO_1, PTERO_2]
        self.tick = 0
        self.rows = self.frames[0]
        self.w, self.h = rows_size(self.rows)
        self.x = SCREEN_W
        self.y = y_level
        self.remove = False

    def update(self, speed):
        self.x -= speed * 1.05
        self.tick = (self.tick + 1) & 0x07
        self.rows = self.frames[(self.tick // 4) % 2]
        if self.x + self.w < 0:
            self.remove = True

    def draw(self, d):
        draw_rows(d, int(self.x), int(self.y), self.rows)

    def bbox(self):
        return (int(self.x), int(self.y), self.w, self.h)

def draw_ground(d, scroll):
    start_x = -(int(scroll) % GTW)
    y = GROUND_Y - GTH + 1
    x = start_x
    tile_index = int(scroll // GTW)
    num_tiles = len(GROUND_TILES)

    while x < SCREEN_W:
        rows = GROUND_TILES[tile_index % num_tiles]
        draw_rows(d, x, y, rows)
        x += GTW
        tile_index += 1

# -------------------------------
# Game Class
# -------------------------------
class Game:
    def __init__(self, hiscore=0):
        self.trex = Trex()
        self.obstacles = []
        self.clouds = []
        self.fliers = []
        self.speed = SPEED_START
        self.distance = 0.0
        self.score = 0
        self.hiscore = hiscore

        self.started = False
        self.crashed = False
        self.achievement_next = ACHIEVEMENT_EVERY
        self.ground_scroll = 0.0
        self.night = False
        self.next_theme = 100   # color swap every 100
        set_theme(self.night)

    def reset(self):
        # Preserve hiscore
        self.__init__(self.hiscore)

    def maybe_spawn_cloud(self):
        if len(self.clouds) < 4 and random.random() < 0.025:
            self.clouds.append(Cloud())

    def maybe_spawn_ptero(self):
        if self.score < 80 or self.speed < 2.0:
            return
        if len(self.fliers) >= 1:
            return
        if random.random() < 0.012:
            low_y = GROUND_Y - 16
            high_y = GROUND_Y - 24
            y_level = random.choice([low_y, high_y])
            self.fliers.append(Pterodactyl(y_level))

    def compute_gap(self):
        base = max(MIN_GAP, int((MIN_GAP + 14) * GAP_COEFF + self.speed * 12))
        jitter = random.randint(-6, 10)
        return max(12, base + jitter)

    def update(self):
        if not self.started or self.crashed:
            return

        # Auto speed-up with distance (not player controlled)
        if self.speed < SPEED_MAX:
            self.speed += ACCELERATION

        # Distance & score
        self.distance += self.speed
        new_score = int(self.distance * 0.08)
        if new_score > self.score:
            self.score = new_score
            if self.score >= self.achievement_next:
                self.achievement_next += ACHIEVEMENT_EVERY
                beep(900, 30)

            # Day/night theme swap every 100 points
            if self.score >= self.next_theme:
                self.night = not self.night
                self.next_theme += 100
                set_theme(self.night)

        # Scroll ground
        self.ground_scroll += self.speed

        # Obstacles
        for ob in self.obstacles:
            ob.update(self.speed)
        self.obstacles = [o for o in self.obstacles if not o.remove]

        need = (len(self.obstacles) == 0) or \
               (self.obstacles[-1].x + self.obstacles[-1].w + self.compute_gap() < SCREEN_W)
        if need and random.random() < SPAWN_PROB:
            r = random.random()
            if r < 0.15:
                self.obstacles.append(Obstacle(small=True, multi=1, thin=True))
            elif r < 0.6:
                self.obstacles.append(Obstacle(small=True, multi=random.randint(1, 3)))
            else:
                self.obstacles.append(Obstacle(small=False, multi=random.randint(1, 3)))

        # Clouds
        for cl in self.clouds:
            cl.update(self.speed)
        self.clouds = [c for c in self.clouds if not c.remove]
        self.maybe_spawn_cloud()

        # Pterodactyls
        for f in self.fliers:
            f.update(self.speed)
        self.fliers = [f for f in self.fliers if not f.remove]
        self.maybe_spawn_ptero()

        # Player (pass current speed so animation scales with it)
        self.trex.update(self.speed)

        # Ground obstacle collision
        if self.obstacles:
            o = self.obstacles[0]
            ax, ay, aw, ah = self.trex.bbox()
            bx, by, bw, bh = o.bbox()
            if aabb(ax + 1, ay + 1, aw - 2, ah - 2, bx + 1, by + 1, bw - 2, bh - 2):
                self.crash()

        # Pterodactyl collision
        ax, ay, aw, ah = self.trex.bbox()
        for f in self.fliers:
            bx, by, bw, bh = f.bbox()
            if aabb(ax + 1, ay + 1, aw - 2, ah - 2, bx + 1, by + 1, bw - 2, bh - 2):
                self.crash()
                break

    def crash(self):
        self.crashed = True
        self.trex.crashed = True
        beep(220, 120)
        if self.score > self.hiscore:
            self.hiscore = self.score
            save_hiscore(self.hiscore)

    def draw(self, d):
        d.fill(BG_COLOR)
        for cl in self.clouds:
            cl.draw(d)
        draw_ground(d, self.ground_scroll)
        for ob in self.obstacles:
            ob.draw(d)
        for f in self.fliers:
            f.draw(d)
        self.trex.draw(d)

        s = str(self.score)
        hs = "H:" + str(self.hiscore)
        d.drawText(s, SCREEN_W - (len(s) * 6) - 2, 2, FG_COLOR)
        d.drawText(hs, 2, 2, FG_COLOR)

        d.update()

# -------------------------------
# Screen draw functions
# -------------------------------
def draw_loading_screen(d, ticks):
    d.fill(BG_COLOR)

    scroll = ticks * 0.4
    draw_ground(d, scroll)

    frame = DINO_RUN_1 if ((ticks // 5) % 2) == 0 else DINO_RUN_2
    dw, dh = rows_size(frame)
    dino_x = 6
    dino_y = GROUND_Y - dh
    draw_rows(d, dino_x, dino_y, frame)

    base_text = "Loading"
    num_dots = (ticks // 10) % 4
    text = base_text + ("." * num_dots)

    text_w = len(text) * 6
    text_x = (SCREEN_W - text_w) // 2
    text_y = 4  # near top, away from dino

    d.drawText(text, text_x, text_y, FG_COLOR)

    d.update()

def draw_title_screen(d, hiscore, ticks):
    d.fill(BG_COLOR)

    # Small moving cloud in mid-sky
    cw, ch = rows_size(CLOUD_SMALL)
    cloud_speed = 0.4
    cloud_x = -cw + int((ticks * cloud_speed) % (SCREEN_W + cw))
    cloud_y = 12
    draw_rows(d, cloud_x, cloud_y, CLOUD_SMALL)

    # Scrolling ground (0.6 per tick, chill preview)
    ground_scroll = ticks * 0.6
    draw_ground(d, ground_scroll)

    # Running dino near bottom-left, slower title animation (every 5 ticks)
    frame = DINO_RUN_1 if ((ticks // 5) % 2) == 0 else DINO_RUN_2
    dw, dh = rows_size(frame)
    dino_x = 4
    dino_y = GROUND_Y - dh
    draw_rows(d, dino_x, dino_y, frame)

    # Title at top-center
    title = "Rexy Runner"
    t_w = len(title) * 6
    title_x = (SCREEN_W - t_w) // 2
    title_y = 0
    d.drawText(title, title_x, title_y, FG_COLOR)

    # High score on next line, right-aligned
    hs_text = "Hi:" + str(hiscore)
    hs_w = len(hs_text) * 6
    hs_x = SCREEN_W - hs_w - 2
    if hs_x < 0:
        hs_x = 0
    hs_y = 8
    d.drawText(hs_text, hs_x, hs_y, FG_COLOR)

    # Blinking A=Start at bottom-right (menu remains A-only)
    if (ticks // 20) % 2 == 0:
        prompt = "A=Start"
        p_w = len(prompt) * 6
        p_x = SCREEN_W - p_w - 2
        p_y = SCREEN_H - 10
        d.drawText(prompt, p_x, p_y, FG_COLOR)

    d.update()

def draw_gameover_menu(d, score, hiscore, ticks):
    d.fill(BG_COLOR)

    # Centered "GAME OVER"
    title = "GAME OVER"
    t_w = len(title) * 6
    t_x = (SCREEN_W - t_w) // 2
    d.drawText(title, t_x, 2, FG_COLOR)

    # Centered score + hi-score line
    score_text = "S:" + str(score) + " H:" + str(hiscore)
    s_w = len(score_text) * 6
    s_x = (SCREEN_W - s_w) // 2
    if s_x < 0:
        s_x = 0
    d.drawText(score_text, s_x, 12, FG_COLOR)

    # Blinking A=Restart (flashes)
    if (ticks // 10) % 2 == 0:
        d.drawText("A=Restart", 4, 22, FG_COLOR)

    # Static B=Title
    d.drawText("B=Title", 4, 30, FG_COLOR)

    d.update()

# -------------------------------
# Main loop (state machine)
# -------------------------------
initial_hiscore = load_hiscore()
game = Game(initial_hiscore)
prevJump = False  # tracks A or B for variable jump

screen_state = STATE_LOADING
loading_ticks = 0
title_ticks = 0
gameover_ticks = 0

while True:
    if screen_state == STATE_LOADING:
        loading_ticks += 1

        if thumby.buttonA.justPressed():
            screen_state = STATE_TITLE
            title_ticks = 0
        elif loading_ticks > 40:
            screen_state = STATE_TITLE
            title_ticks = 0

        draw_loading_screen(thumby.display, loading_ticks)

    elif screen_state == STATE_TITLE:
        game.started = False
        game.crashed = False

        title_ticks += 1

        # Menu: still A=Start only
        if thumby.buttonA.justPressed():
            game.reset()
            game.started = True
            screen_state = STATE_PLAYING
            prevJump = False

        draw_title_screen(thumby.display, game.hiscore, title_ticks)

    elif screen_state == STATE_PLAYING:
        # --- Jump on A or B ---
        jump_just_pressed = thumby.buttonA.justPressed() or thumby.buttonB.justPressed()
        jump_pressed = thumby.buttonA.pressed() or thumby.buttonB.pressed()

        if jump_just_pressed:
            if not game.started:
                game.started = True
            game.trex.start_jump()

        # Variable jump height: release of either cuts jump short
        if prevJump and not jump_pressed:
            game.trex.end_jump_early()

        prevJump = jump_pressed

        # --- Duck on any D-pad direction ---
        duck_pressed = (
            thumby.buttonU.pressed() or
            thumby.buttonD.pressed() or
            thumby.buttonL.pressed() or
            thumby.buttonR.pressed()
        )

        # Keep speed-drop on D-pad Down justPressed (affects fall, not game scroll)
        if thumby.buttonD.justPressed():
            game.trex.speed_drop()

        game.trex.set_duck(duck_pressed)

        # Update and draw game
        game.update()
        game.draw(thumby.display)

        if game.crashed:
            screen_state = STATE_GAMEOVER_MENU
            gameover_ticks = 0  # reset game over animation timer

    elif screen_state == STATE_GAMEOVER_MENU:
        gameover_ticks += 1

        # A = restart run (menu still uses A)
        if thumby.buttonA.justPressed():
            game.reset()
            game.started = True
            screen_state = STATE_PLAYING
            prevJump = False
            gameover_ticks = 0

        # B = back to title screen
        if thumby.buttonB.justPressed():
            screen_state = STATE_TITLE
            title_ticks = 0
            gameover_ticks = 0

        draw_gameover_menu(thumby.display, game.score, game.hiscore, gameover_ticks)


