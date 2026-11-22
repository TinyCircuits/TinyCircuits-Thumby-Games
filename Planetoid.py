import thumby
import random
from math import sqrt, sin, cos, atan2, pi, floor

W = 72
H = 40

# ---- scale constants (original game ran on a 400x400 canvas, scale = 0.18) ----
PLAYER_H = 4.0            # player height in pixels
RUN_SPEED = 0.45          # px per frame along the planet surface
LAUNCH_SPEED = 0.54       # jump speed
PLANET_G = 0.0081         # planet <-> planet gravity
PLAYER_G = 1.0 / 1000.0   # planet -> player gravity
MAX_PLANETS = 6
START_R = 8.0
SUPER_R = 15.0

# options (menu toggles)
gravity = True
deterioration = False
super_planet = False

best = 0

thumby.display.setFPS(30)


# ------------------------------------------------------------------ helpers
def rnd(a, b):
    return a + (b - a) * random.random()


def rint(v):
    return int(floor(v + 0.5))


def draw_circle(cx, cy, r):
    r = rint(r)
    cx = rint(cx)
    cy = rint(cy)
    for dy in range(-r, r + 1):
        y = cy + dy
        if y < 0 or y >= H:
            continue
        dx = rint(sqrt(r * r - dy * dy))
        x0 = cx - dx
        x1 = cx + dx
        if x0 < 0:
            x0 = 0
        if x1 > W - 1:
            x1 = W - 1
        if x0 <= x1:
            thumby.display.drawLine(x0, y, x1, y, 1)


def put(x, y):
    x = rint(x)
    y = rint(y)
    if 0 <= x < W and 0 <= y < H:
        thumby.display.setPixel(x, y, 1)


def line(x0, y0, x1, y1):
    n = int(max(abs(x1 - x0), abs(y1 - y0)) + 1)
    for i in range(n + 1):
        t = i / n
        put(x0 + (x1 - x0) * t, y0 + (y1 - y0) * t)


def load_best():
    global best
    try:
        thumby.saveData.setName("Planetoid")
        if thumby.saveData.hasItem("best"):
            best = int(thumby.saveData.getItem("best"))
    except Exception:
        pass


def save_best():
    try:
        thumby.saveData.setItem("best", best)
        thumby.saveData.save()
    except Exception:
        pass


# ------------------------------------------------------------------ planets
class Planet:
    def __init__(self, x, y, vx, vy, r):
        self.x = x
        self.y = y
        self.vx = vx
        self.vy = vy
        self.r = r
        self.m = pi * r * r


def overlaps(planets, x, y, r):
    for p in planets:
        dx = p.x - x
        dy = p.y - y
        if sqrt(dx * dx + dy * dy) <= p.r + r:
            return True
    return False


def spawn(planets):
    r = rnd(W / 20, W / 10)
    for _ in range(20):
        vx = rnd(-1, 1)
        vy = rnd(-1, 1)
        mag = sqrt(vx * vx + vy * vy)
        if mag < 0.01:
            vx, vy, mag = 1.0, 0.0, 1.0
        speed = rnd(0.05, 0.2)
        vx = vx / mag * speed
        vy = vy / mag * speed
        if vy > abs(vx):
            x, y = rnd(-r, W + r), -r
        elif vx <= -abs(vy):
            x, y = W + r, rnd(-r, H + r)
        elif vy < -abs(vx):
            x, y = rnd(-r, W + r), H + r
        else:
            x, y = -r, rnd(-r, H + r)
        if not overlaps(planets, x, y, r):
            planets.append(Planet(x, y, vx, vy, r))
            return


def update_planets(planets, frame):
    if len(planets) <= 1:
        spawn(planets)
    chance = frame / 100000
    if chance < 0.01:
        chance = 0.01
    if len(planets) < MAX_PLANETS and random.random() < chance:
        spawn(planets)

    for p in planets:
        p.m = pi * p.r * p.r

    # gravity between planets
    if gravity:
        for a in planets:
            for b in planets:
                if a is b:
                    continue
                dx = b.x - a.x
                dy = b.y - a.y
                d = sqrt(dx * dx + dy * dy)
                if d < 1:
                    d = 1
                acc = PLANET_G * b.m / (d * a.m)
                a.vx += dx / d * acc
                a.vy += dy / d * acc

    # collisions
    n = len(planets)
    for i in range(n):
        a = planets[i]
        for j in range(i + 1, n):
            b = planets[j]
            dx = b.x - a.x
            dy = b.y - a.y
            d = sqrt(dx * dx + dy * dy)
            rs = a.r + b.r
            if d >= rs:
                continue
            if d < 0.001:
                dx, dy, d = 1.0, 0.0, 1.0
            nx = dx / d
            ny = dy / d
            over = rs - d
            tm = a.m + b.m
            a.x -= nx * over * b.m / tm
            a.y -= ny * over * b.m / tm
            b.x += nx * over * a.m / tm
            b.y += ny * over * a.m / tm
            rel = (a.vx - b.vx) * nx + (a.vy - b.vy) * ny
            if rel > 0:
                j_imp = 2 * rel / (1 / a.m + 1 / b.m)
                a.vx -= j_imp / a.m * nx
                a.vy -= j_imp / a.m * ny
                b.vx += j_imp / b.m * nx
                b.vy += j_imp / b.m * ny

    # move + cull
    i = 0
    while i < len(planets):
        p = planets[i]
        p.x += p.vx
        p.y += p.vy
        m = p.r + PLAYER_H
        if p.x < -m or p.y < -m or p.x > W + m or p.y > H + m:
            planets.pop(i)
        else:
            i += 1


# ------------------------------------------------------------------ player
class Player:
    def __init__(self, planet):
        self.planet = planet
        self.ang = -pi / 2
        self.x = planet.x
        self.y = planet.y - planet.r
        self.vx = 0.0
        self.vy = 0.0
        self.run = 0
        self.moving = False
        self.flying = False
        self.launch = False
        self.dead = False
        self.score = 0


def inside(x, y, p):
    dx = x - p.x
    dy = y - p.y
    return dx * dx + dy * dy <= p.r * p.r


def attach(pl, planet, ang):
    pl.planet = planet
    pl.ang = ang
    pl.flying = False


def update_player(pl, planets, left, right, jump):
    if pl.dead:
        return

    ux = cos(pl.ang)
    uy = sin(pl.ang)
    hx = pl.x + ux * PLAYER_H
    hy = pl.y + uy * PLAYER_H

    # landing / being crushed
    if pl.planet is not None:
        if pl.planet not in planets:
            pl.dead = True
            return
        for o in planets:
            if o is pl.planet:
                continue
            if inside(pl.x, pl.y, o) or inside(hx, hy, o):
                pl.dead = True
                return
    else:
        for o in planets:
            if inside(pl.x, pl.y, o):
                attach(pl, o, atan2(pl.y - o.y, pl.x - o.x))
                break
            if inside(hx, hy, o):
                attach(pl, o, atan2(hy - o.y, hx - o.x))
                break

    p = pl.planet
    if p is not None:
        # deterioration
        if deterioration:
            if p.r > 1.0:
                p.r -= 0.036
            else:
                planets.remove(p)
                pl.launch = True

        pl.moving = False
        if left and not right:
            pl.ang -= RUN_SPEED / p.r
            pl.moving = True
        elif right and not left:
            pl.ang += RUN_SPEED / p.r
            pl.moving = True
        if pl.moving:
            pl.run = (pl.run + 1) % 12
        else:
            pl.run = 0

        pl.x = p.x + p.r * cos(pl.ang)
        pl.y = p.y + p.r * sin(pl.ang)

        if jump or pl.launch:
            sp = 0.18 if pl.launch else LAUNCH_SPEED
            pl.vx = cos(pl.ang) * sp + p.vx
            pl.vy = sin(pl.ang) * sp + p.vy
            pl.x += pl.vx
            pl.y += pl.vy
            pl.planet = None
            pl.flying = True
            pl.launch = False
    else:
        if gravity:
            mx = pl.x + cos(pl.ang) * PLAYER_H / 2
            my = pl.y + sin(pl.ang) * PLAYER_H / 2
            for o in planets:
                dx = o.x - mx
                dy = o.y - my
                d = sqrt(dx * dx + dy * dy)
                if d < 1:
                    d = 1
                acc = o.m * PLAYER_G / d
                pl.vx += dx / d * acc
                pl.vy += dy / d * acc
        pl.x += pl.vx
        pl.y += pl.vy
        pl.score += 2
        if left and not right:
            pl.ang -= 0.07
        if right and not left:
            pl.ang += 0.07

    if pl.x < -5 or pl.y < -5 or pl.x > W + 5 or pl.y > H + 5:
        pl.dead = True

    pl.score += 1


def draw_player(pl):
    ux = cos(pl.ang)
    uy = sin(pl.ang)
    tx = -uy
    ty = ux
    x = pl.x
    y = pl.y
    hipx = x + ux * 1.5
    hipy = y + uy * 1.5
    shx = x + ux * 3.0
    shy = y + uy * 3.0

    # body + head
    line(hipx, hipy, shx, shy)
    put(x + ux * 4.2, y + uy * 4.2)

    if pl.flying:
        # arms up, legs out
        put(shx + tx * 1.5 + ux, shy + ty * 1.5 + uy)
        put(shx - tx * 1.5 + ux, shy - ty * 1.5 + uy)
        put(x + tx, y + ty)
        put(x - tx, y - ty)
    elif pl.moving:
        sw = 1.5 if pl.run < 6 else -1.5
        line(hipx, hipy, x + tx * sw, y + ty * sw)
        line(hipx, hipy, x - tx * sw, y - ty * sw)
        put(shx + tx * -sw * 0.7, shy + ty * -sw * 0.7)
    else:
        put(x + tx, y + ty)
        put(x - tx, y - ty)


# ------------------------------------------------------------------ screens
def new_game():
    r = SUPER_R if super_planet else START_R
    start = Planet(W / 2, H / 2, 0.0, 0.0, r)
    return [start], Player(start)


def draw_game(planets, pl):
    thumby.display.fill(0)
    for p in planets:
        draw_circle(p.x, p.y, p.r)
    if not pl.dead:
        draw_player(pl)
    txt = str(pl.score // 30)
    thumby.display.drawFilledRectangle(0, 0, len(txt) * 6 + 1, 8, 0)
    thumby.display.drawText(txt, 0, 0, 1)
    thumby.display.update()


def draw_dead(score):
    thumby.display.fill(0)
    thumby.display.drawText("YOU DIED", 12, 2, 1)
    thumby.display.drawText("Score:" + str(score), 0, 12, 1)
    thumby.display.drawText("Best:" + str(best), 0, 21, 1)
    thumby.display.drawText("A:retry B:menu", 0, 31, 1)
    thumby.display.update()


def onoff(v):
    return "ON" if v else "OFF"


def draw_menu(sel):
    global gravity, deterioration, super_planet
    thumby.display.fill(0)
    thumby.display.drawText("PLANETOID", 9, 0, 1)
    items = [
        "Play",
        "Grav:" + onoff(gravity),
        "Decay:" + onoff(deterioration),
        "Super:" + onoff(super_planet),
    ]
    for i in range(4):
        prefix = ">" if i == sel else " "
        thumby.display.drawText(prefix + items[i], 4, 9 + i * 8, 1)
    thumby.display.update()


# ------------------------------------------------------------------ main loop
load_best()

state = 0  # 0 = menu, 1 = playing, 2 = dead
sel = 0
planets, player = new_game()
frame = 0
prev = [False] * 6  # L, R, U, D, A, B

while True:
    cur = [
        thumby.buttonL.pressed(),
        thumby.buttonR.pressed(),
        thumby.buttonU.pressed(),
        thumby.buttonD.pressed(),
        thumby.buttonA.pressed(),
        thumby.buttonB.pressed(),
    ]
    L, R, U, D, A, B = cur
    pressedL = L and not prev[0]
    pressedR = R and not prev[1]
    pressedU = U and not prev[2]
    pressedD = D and not prev[3]
    pressedA = A and not prev[4]
    pressedB = B and not prev[5]
    prev = cur

    if state == 0:
        if pressedU:
            sel = (sel - 1) % 4
        if pressedD:
            sel = (sel + 1) % 4
        if pressedA or pressedL or pressedR:
            if sel == 0:
                if pressedA:
                    planets, player = new_game()
                    frame = 0
                    state = 1
            elif sel == 1:
                gravity = not gravity
            elif sel == 2:
                deterioration = not deterioration
            elif sel == 3:
                super_planet = not super_planet
        draw_menu(sel)

    elif state == 1:
        frame += 1
        update_planets(planets, frame)
        update_player(player, planets, L, R, pressedU or pressedA or pressedB)
        draw_game(planets, player)
        if player.dead:
            final = player.score // 30
            # only default modifiers (gravity only) count for the high score
            if gravity and not deterioration and not super_planet and final > best:
                best = final
                save_best()
            state = 2

    else:
        draw_dead(player.score // 30)
        if pressedA:
            planets, player = new_game()
            frame = 0
            state = 1
        elif pressedB:
            state = 0