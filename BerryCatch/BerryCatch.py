import thumby
import random
import time

W = 72
H = 40
PLAYER_Y = H - 11  # sprite is 10 tall, the shore is the last row

# 12x10 croc facing right. Two rows of column bytes (top 8 px, then the rest), bit 0 on top.
croc = thumby.Sprite(12, 10, bytearray([
    8, 28, 224, 254, 255, 255, 159, 203, 159, 206, 158, 12,
    2, 1, 1, 3, 3, 1, 3, 3, 0, 0, 0, 0,
]))

thumby.display.setFPS(30)
thumby.display.setFont("/lib/font5x7.bin", 5, 7, 1)
thumby.saveData.setName("BerryCatch")


def load_best():
    if thumby.saveData.hasItem("best"):
        return int(thumby.saveData.getItem("best"))
    return 0


class Game:
    def __init__(self):
        self.phase = "ready"
        self.score = 0
        self.best = load_best()

    def start(self):
        self.phase = "playing"
        self.score = 0
        self.px = W / 2
        self.fallers = []  # [x, y, vy, rock]
        self.lives = 3
        self.spawn_in = 0
        croc.mirrorX = 0

    def over(self):
        self.phase = "over"
        if self.score > self.best:
            self.best = self.score
            thumby.saveData.setItem("best", self.best)
            thumby.saveData.save()

    def step(self, dt):
        speed = 1 + self.score / 15
        move = thumby.buttonR.pressed() - thumby.buttonL.pressed()
        self.px = max(6, min(W - 6, self.px + move * 40 * dt))
        if move:
            croc.mirrorX = 1 if move < 0 else 0  # face where you're walking

        self.spawn_in -= dt
        if self.spawn_in <= 0:
            self.spawn_in = max(0.35, 1.1 - self.score / 40)
            rock = random.randint(0, 99) < min(35, 15 + self.score * 100 // 120)
            vy = (8 + random.randint(0, 5)) * speed
            self.fallers.append([random.randint(3, W - 4), -3, vy, rock])

        keep = []
        for f in self.fallers:
            f[1] += f[2] * dt
            caught = PLAYER_Y < f[1] < H - 1 and abs(f[0] - self.px) < 7
            if caught and f[3]:
                self.lives -= 1
            elif caught:
                self.score += 1
            if not caught and f[1] < H + 3:
                keep.append(f)
        self.fallers = keep
        if self.lives <= 0:
            self.over()

    def banner(self, top, bottom):
        d = thumby.display
        d.drawFilledRectangle(0, 11, W, 18, 0)
        d.drawText(top, (W - len(top) * 6) // 2, 12, 1)
        d.drawText(bottom, (W - len(bottom) * 6) // 2, 21, 1)

    def draw_title(self):
        d = thumby.display
        t = time.ticks_ms()
        d.drawText("BERRY CATCH", 3, 0, 1)
        d.drawLine(3, 8, 68, 8, 1)
        # berries drifting down on both sides
        for i, x in enumerate((8, 20, 52, 64)):
            y = 11 + (t // 40 + i * 7) % 18
            d.drawFilledRectangle(x - 1, y - 1, 3, 3, 1)
            d.setPixel(x, y - 2, 1)
        croc.mirrorX = (t // 1500) % 2  # looks around
        croc.x = 30
        croc.y = 18 - 2 * ((t // 250) % 2)  # hops
        d.drawSprite(croc)
        line = "A TO START" if (t // 1200) % 2 == 0 else "BEST %03d" % self.best
        d.drawText(line, (W - len(line) * 6) // 2, 32, 1)

    def draw(self):
        d = thumby.display
        d.fill(0)
        if self.phase == "ready":
            self.draw_title()
            return
        d.drawLine(0, H - 1, W - 1, H - 1, 1)  # the shore

        for x, y, _, rock in self.fallers:
            y = int(y)
            if rock:
                d.drawRectangle(x - 2, y - 2, 4, 4, 1)
            else:
                d.drawFilledRectangle(x - 1, y - 1, 3, 3, 1)
                d.setPixel(x, y - 2, 1)  # the leaf
        croc.x = int(self.px) - 6
        croc.y = PLAYER_Y
        d.drawSprite(croc)

        d.drawText("%03d" % self.score, 0, 0, 1)
        if self.phase == "playing":
            for i in range(self.lives):
                d.drawFilledRectangle(W - 4 - i * 4, 1, 3, 3, 1)

        if self.phase == "over":
            self.banner("GAME OVER", "BEST %03d" % self.best)


game = Game()
last = time.ticks_ms()
while True:
    now = time.ticks_ms()
    dt = min(0.05, time.ticks_diff(now, last) / 1000)
    last = now

    if game.phase == "playing":
        game.step(dt)
    elif thumby.buttonA.justPressed():
        game.start()

    game.draw()
    thumby.display.update()
