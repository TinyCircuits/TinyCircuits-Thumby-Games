# ==============================================
# ThumbySurf.py
# Endless surfing game for the Original Thumby
# ==============================================

import thumby
import random
import time

# ---- Display Constants ----
W = 72
H = 40
thumby.display.setFPS(30)

# ---- Enable Audio Safely ----
try:
    thumby.audio.setEnabled(True)
except:
    pass

# ---- Persistent High Score ----
SAVE_NAME = "ThumbySurf"

def loadHiScore():
    global hiScore
    try:
        thumby.saveData.setName(SAVE_NAME)
        if thumby.saveData.hasItem("hi"):
            hiScore = int(thumby.saveData.getItem("hi"))
        else:
            hiScore = 0
    except:
        hiScore = 0

def saveHiScore(val):
    global hiScore
    hiScore = val
    try:
        thumby.saveData.setName(SAVE_NAME)
        thumby.saveData.setItem("hi", val)
        thumby.saveData.save()
    except:
        pass

hiScore = 0
loadHiScore()

# ---- Safe Audio Helpers ----
def sPlay(freq, dur_ms):
    try:
        if freq > 0:
            thumby.audio.play(freq, dur_ms)
        else:
            thumby.audio.stop()
    except:
        pass

def sStop():
    try:
        thumby.audio.stop()
    except:
        pass

# ---- Heart Bitmap (5x5, VLSB) ----
HEART = bytearray([6, 15, 30, 15, 6])

# ---- Surfer Bitmap (5x8, VLSB) ----
SURFER = bytearray([8, 22, 126, 22, 8])

# ---- Obstacle Sizes ----
OB_W = [5, 10, 6, 3]
OB_H = [4, 6, 8, 3]

# ---- Wave LUT ----
WAVE_LUT = [0, 0, 1, 1, 2, 2, 1, 1, 0, 0, -1, -1, -2, -2, -1, -1]
WAVE_LEN = len(WAVE_LUT)
#Music
TITLE_TUNE = [
    (659, 6), (784, 6), (880, 6), (988, 12),
    (880, 6), (784, 6), (659, 6), (587, 12),
    (659, 6), (784, 6), (880, 12),
    (784, 6), (659, 6), (587, 6), (523, 12),
    (1047, 8), (988, 8), (880, 8), (784, 16),
    (0, 16),
]

OVER_TUNE = [
    (784, 8), (0, 3), (659, 8), (0, 3),
    (523, 10), (0, 4), (392, 14), (0, 20),
]

def waitBtnRelease():
    while thumby.buttonA.pressed():
        thumby.display.update()
    thumby.buttonA.justPressed()
#Draw
def drawHeart(x, y):
    thumby.display.blit(HEART, x, y, 5, 5, 0, 0, 0)

def drawPlayer(x, y, boosting, frame):
    thumby.display.blit(SURFER, x, y, 5, 8, 0, 0, 0)
    if boosting:
        thumby.display.setPixel(x + 1, y + 8, 1)
        thumby.display.setPixel(x + 3, y + 8, 1)
        if frame % 3 == 0:
            thumby.display.setPixel(x, y + 9, 1)
            thumby.display.setPixel(x + 4, y + 9, 1)

def drawObstacle(x, y, kind):
    if kind == 0:
        thumby.display.drawFilledRectangle(x + 1, y, 3, 4, 1)
        thumby.display.drawFilledRectangle(x, y + 1, 5, 2, 1)
    elif kind == 1:
        thumby.display.drawFilledRectangle(x + 2, y, 6, 6, 1)
        thumby.display.drawFilledRectangle(x, y + 1, 10, 4, 1)
        thumby.display.drawFilledRectangle(x + 1, y + 5, 8, 1, 1)
        thumby.display.setPixel(x + 4, y + 1, 0)
        thumby.display.setPixel(x + 5, y + 2, 0)
        thumby.display.setPixel(x + 3, y + 2, 0)
    elif kind == 2:
        thumby.display.drawFilledRectangle(x, y, 6, 8, 1)
        for i in range(0, 8, 2):
            thumby.display.drawLine(x, y + i, x + 5, y + i, 0)
    else:
        thumby.display.drawFilledRectangle(x, y, 3, 3, 1)
        thumby.display.setPixel(x + 1, y + 1, 0)

def drawBolt(x, y):
    thumby.display.setPixel(x + 1, y, 1)
    thumby.display.setPixel(x + 2, y, 1)
    thumby.display.setPixel(x, y + 1, 1)
    thumby.display.setPixel(x + 1, y + 1, 1)
    thumby.display.setPixel(x, y + 2, 1)
    thumby.display.setPixel(x + 1, y + 2, 1)
    thumby.display.setPixel(x + 2, y + 2, 1)
    thumby.display.setPixel(x, y + 3, 1)
    thumby.display.setPixel(x + 1, y + 3, 1)
    thumby.display.setPixel(x, y + 4, 1)

def drawBoltHUD(x, y):
    thumby.display.setPixel(x + 1, y, 1)
    thumby.display.setPixel(x, y + 1, 1)
    thumby.display.setPixel(x + 1, y + 1, 1)
    thumby.display.setPixel(x, y + 2, 1)

MILE_MSG = "You have made it this far, now, share it to the world, take pictures, EVERYTHING, you are one of the only ones having achived this. Now... SAX SAVEN!   "

def showMilestone():
    sStop()
    sPlay(1319, 200)
    msgW = len(MILE_MSG) * 6
    scrollX = W

    while scrollX > -msgW:
        thumby.display.fill(0)

        thumby.display.drawText("*10000m*", 12, 2, 1)
        thumby.display.drawLine(0, 10, W - 1, 10, 1)

        thumby.display.drawText(MILE_MSG, scrollX, 16, 1)

        thumby.display.drawLine(0, 28, W - 1, 28, 1)

        if (scrollX // 15) % 2 == 0:
            thumby.display.drawText("B:SKIP", 18, 32, 1)

        thumby.display.update()
        scrollX -= 1

        if thumby.buttonB.justPressed() or thumby.buttonA.justPressed():
            break

    sStop()
    time.sleep(0.2)
#Title
def titleScreen():
    waitBtnRelease()
    f = 0
    nIdx = 0
    nTimer = 0
    while True:
        if nTimer <= 0:
            if nIdx >= len(TITLE_TUNE):
                nIdx = 0
            freq, dur = TITLE_TUNE[nIdx]
            sPlay(freq, dur * 32)
            nTimer = dur
            nIdx += 1
        nTimer -= 1

        thumby.display.fill(0)

        for x in range(0, W, 2):
            yOff = WAVE_LUT[(x + f * 3) % WAVE_LEN]
            py = 3 + yOff
            if 0 <= py < H:
                thumby.display.setPixel(x, py, 1)

        thumby.display.drawText("THUMBY", 18, 8, 1)
        thumby.display.drawText("~SURF~", 18, 18, 1)

        for x in range(0, W, 2):
            yOff = WAVE_LUT[(x + f * 2) % WAVE_LEN]
            py = 28 + yOff
            if 0 <= py < H:
                thumby.display.setPixel(x, py, 1)

        if (f // 12) % 2 == 0:
            thumby.display.drawText("A:START", 15, 33, 1)

        thumby.display.update()
        f += 1

        if thumby.buttonA.justPressed():
            sStop()
            return

def deathFreeze():
    sStop()
    thumby.display.fill(1)
    thumby.display.update()
    time.sleep(0.15)
    thumby.display.fill(0)
    thumby.display.drawText("CRASH!", 18, 16, 1)
    thumby.display.update()
    time.sleep(0.6)
#Over
def gameOverScreen(runScore, bestScore):
    waitBtnRelease()
    isNew = runScore >= bestScore and runScore > 0
    minFrames = 30
    f = 0
    nIdx = 0
    nTimer = 0
    melodyDone = False
    while True:
        if not melodyDone:
            if nTimer <= 0:
                if nIdx >= len(OVER_TUNE):
                    melodyDone = True
                    sStop()
                else:
                    freq, dur = OVER_TUNE[nIdx]
                    sPlay(freq, dur * 32)
                    nTimer = dur
                    nIdx += 1
            nTimer -= 1

        thumby.display.fill(0)
        thumby.display.drawText("GAME", 24, 0, 1)
        thumby.display.drawText("OVER", 24, 9, 1)
        thumby.display.drawLine(2, 18, 70, 18, 1)
        thumby.display.drawText("RUN:" + str(runScore), 1, 21, 1)
        thumby.display.drawText("HI:" + str(bestScore), 1, 30, 1)

        if isNew:
            if (f // 8) % 2 == 0:
                thumby.display.drawText("NEW!", 48, 21, 1)

        if f >= minFrames and (f // 10) % 2 == 0:
            thumby.display.drawText("A", 64, 33, 1)

        thumby.display.update()
        f += 1

        if f >= minFrames and thumby.buttonA.justPressed():
            sStop()
            return
#Main loop
def runGame():
    global hiScore

    waitBtnRelease()
    sStop()

    px = W // 2 - 2
    pY = H - 11
    pW = 5
    pH = 8

    hearts = 3
    dist = 0.0
    score = 0
    speed = 0.8

    obs = []
    spawnAcc = 0.0
    spawnGap = 18.0

    invTimer = 0
    frame = 0
    waveOff = 0.0

    # ---- Lightning Bolt System ----
    bolts = 0
    boltActive = 0
    boltItems = []
    boltSpawnAcc = 0.0
    boltSpawnGap = 45.0

    # ---- Milestone ----
    hit10k = False

    while True:
        accel = thumby.buttonA.pressed()

        # Lightning boost activation
        if thumby.buttonB.justPressed() and bolts > 0 and boltActive <= 0:
            bolts -= 1
            boltActive = 60
            sPlay(1500, 100)

        if thumby.buttonL.pressed():
            px -= 1
        if thumby.buttonR.pressed():
            px += 1

        if px < 2:
            px = 2
        if px > W - pW - 2:
            px = W - pW - 2

        baseSpd = 1.0 + dist / 2000.0
        if baseSpd > 3.0:
            baseSpd = 3.0

        if boltActive > 0:
            speed += (baseSpd * 3.0 - speed) * 0.15
            boltActive -= 1
        elif accel:
            speed += (baseSpd * 1.6 - speed) * 0.1
        else:
            speed += (baseSpd * 0.4 - speed) * 0.15
        if speed < 0.3:
            speed = 0.3

        dist += speed
        score = int(dist / 2.5)

        # 10K milestone check
        if not hit10k and score >= 10000:
            hit10k = True
            showMilestone()

        # ---- Spawn Obstacles ----
        spawnAcc += speed
        if spawnAcc >= spawnGap:
            spawnAcc -= spawnGap

            n = 1 if random.randint(0, 99) < 55 else 2
            placed = []
            for _ in range(n):
                k = random.choice([0, 0, 0, 1, 2, 3, 3])
                w = OB_W[k]
                h = OB_H[k]
                ox = random.randint(3, W - w - 3)

                retries = 0
                while retries < 6:
                    good = True
                    for (bx, bw) in placed:
                        if abs(ox - bx) < bw + 4:
                            good = False
                            break
                    if good:
                        break
                    ox = random.randint(3, W - w - 3)
                    retries += 1

                placed.append((ox, w))
                obs.append([ox, float(-h), k])

            spawnGap = max(10.0, 18.0 - dist / 800.0)

        # ---- Spawn Bolt Pickups ----
        boltSpawnAcc += speed
        if boltSpawnAcc >= boltSpawnGap:
            boltSpawnAcc -= boltSpawnGap
            if len(boltItems) < 2:
                bx = random.randint(6, W - 9)
                boltItems.append([bx, -6.0])

        # ---- Move Everything ----
        for o in obs:
            o[1] += speed
        for b in boltItems:
            b[1] += speed

        # ---- Cleanup Off-Screen ----
        i = 0
        while i < len(obs):
            if obs[i][1] > H + 5:
                obs.pop(i)
            else:
                i += 1

        i = 0
        while i < len(boltItems):
            if boltItems[i][1] > H + 5:
                boltItems.pop(i)
            else:
                i += 1

        # ---- Collect Bolts ----
        i = 0
        while i < len(boltItems):
            bx = boltItems[i][0]
            by = int(boltItems[i][1])
            if (px < bx + 3 and px + pW > bx and
                pY < by + 5 and pY + pH > by):
                if bolts < 3:
                    bolts += 1
                    sPlay(1200, 50)
                boltItems.pop(i)
            else:
                i += 1

        # ---- Collision ----
        if invTimer > 0:
            invTimer -= 1
        else:
            if boltActive <= 0:
                for o in obs:
                    ox = o[0]
                    oy = int(o[1])
                    ok = o[2]
                    ow = OB_W[ok]
                    oh = OB_H[ok]

                    if (px + 1 < ox + ow and
                        px + pW - 1 > ox and
                        pY + 1 < oy + oh and
                        pY + pH - 2 > oy):
                        hearts -= 1
                        sPlay(200, 80)
                        invTimer = 25

                        if hearts <= 0:
                            if score > hiScore:
                                saveHiScore(score)
                            deathFreeze()
                            return score
                        break

        # ======== RENDER ========
        thumby.display.fill(0)

        # Water dots
        waveOff += speed
        wo = int(waveOff) % 12
        for wy in range(wo - 12, H + 6, 12):
            for wx in range(4, W - 4, 16):
                if 7 <= wy < H:
                    thumby.display.setPixel(wx, wy, 1)
                wy2 = wy + 6
                if 7 <= wy2 < H:
                    thumby.display.setPixel(wx + 8, wy2, 1)

        # Shore lines
        so = int(waveOff) % 8
        for sy in range(so - 8, H, 8):
            if 0 <= sy < H:
                thumby.display.setPixel(0, sy, 1)
                thumby.display.setPixel(1, sy, 1)
                thumby.display.setPixel(W - 1, sy, 1)
                thumby.display.setPixel(W - 2, sy, 1)
            sy2 = sy + 1
            if 0 <= sy2 < H:
                thumby.display.setPixel(0, sy2, 1)
                thumby.display.setPixel(W - 1, sy2, 1)

        # Draw obstacles
        for o in obs:
            drawObstacle(o[0], int(o[1]), o[2])

        # Draw bolt pickups (blink so they stand out)
        if (frame // 4) % 2 == 0:
            for b in boltItems:
                by = int(b[1])
                if -6 <= by < H:
                    drawBolt(b[0], by)

        # Draw player
        showP = True
        if boltActive > 0:
            showP = (frame % 2) == 0
        elif invTimer > 0:
            showP = (frame % 4) < 2

        if showP:
            drawPlayer(px, pY, accel or boltActive > 0, frame)

        # Lightning trail
        if boltActive > 0:
            for ty in range(pY + pH, min(pY + pH + 4, H)):
                if frame % 2 == 0:
                    thumby.display.setPixel(px + 1, ty, 1)
                    thumby.display.setPixel(px + 3, ty, 1)
                else:
                    thumby.display.setPixel(px, ty, 1)
                    thumby.display.setPixel(px + 2, ty, 1)
                    thumby.display.setPixel(px + 4, ty, 1)

        # ======== HUD ========
        thumby.display.drawFilledRectangle(0, 0, W, 7, 0)

        # Hearts
        for i in range(hearts):
            drawHeart(i * 7 + 1, 1)

        # Bolt count icons in HUD
        bHx = hearts * 7 + 3
        for i in range(bolts):
            drawBoltHUD(bHx + i * 4, 1)

        # Boost bar when active
        if boltActive > 0:
            bW = int((boltActive / 60.0) * 16)
            if bW > 0:
                thumby.display.drawLine(bHx, 5, bHx + bW, 5, 1)

        # Score
        ss = str(score)
        thumby.display.drawText(ss, W - len(ss) * 6 - 1, 0, 1)

        thumby.display.update()
        frame += 1

while True:
    titleScreen()
    sc = runGame()
    gameOverScreen(sc, hiScore)
