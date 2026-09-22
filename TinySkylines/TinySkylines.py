import gc
import random
import thumby
import machine

# Safely overclock the RP2040 chip to 125MHz to guarantee a solid 30 FPS
machine.freq(125000000)

# =====================================================================
# TINY SKYLINES (Ultimate Edition: Auto-Tiler, News & Tutorial)
# =====================================================================

TILE_W, TILE_H = 12, 8
VIEW_COLS = thumby.display.width // TILE_W
VIEW_ROWS = (thumby.display.height - 8) // TILE_H
HUD_Y = VIEW_ROWS * TILE_H
MAP_COLS, MAP_ROWS = 18, 8

EMPTY = 0
RESIDENTIAL, COMMERCIAL, POWERPLANT, PARK = 1, 2, 3, 4
RESIDENTIAL_HI, COMMERCIAL_HI = 5, 6
ROAD = 7
ROAD_TYPES = (ROAD,)

BUILD_ORDER = [RESIDENTIAL, COMMERCIAL, POWERPLANT, PARK, ROAD]
BUILD_COSTS = {1: 10, 2: 15, 3: 20, 4: 8, 7: 2, 5: 30, 6: 45}
BUILD_HINTS = {1: "HOUSE $10", 2: "STORE $15", 3: "PYLON $20", 4: "TREE $8", 7: "ROAD $2"}

thumby.display.setFPS(30)
SAVE_FILE = "save.txt"

def safeSetPixel(x, y, color):
    if 0 <= x < 72 and 0 <= y < 40: thumby.display.setPixel(x, y, color)

# =====================================================================
# RAW BYTEARRAY PIXEL ART
# =====================================================================
B_H1 = bytearray([0, 240, 248, 156, 254, 159, 158, 252, 152, 240, 224, 0])
B_H2 = bytearray([0, 240, 248, 157, 254, 159, 158, 252, 152, 240, 224, 0])
B_S1 = bytearray([255, 189, 141, 173, 141, 189, 189, 141, 173, 141, 189, 255])
B_S2 = bytearray([247, 189, 141, 173, 141, 189, 189, 141, 173, 141, 189, 247])
B_A1 = bytearray([0, 255, 129, 213, 213, 129, 129, 213, 213, 129, 255, 0])
B_A2 = bytearray([0, 255, 129, 215, 215, 129, 129, 215, 215, 129, 255, 0])
B_P1 = bytearray([0, 252, 135, 209, 135, 132, 132, 135, 209, 135, 252, 0])
B_P2 = bytearray([0, 252, 135, 217, 135, 132, 132, 135, 217, 135, 252, 0])
B_Y1 = bytearray([0, 240, 136, 140, 255, 255, 140, 136, 240, 0, 0, 0])
B_Y2 = bytearray([0, 240, 136, 254, 255, 255, 254, 136, 240, 0, 0, 0])
B_K1 = bytearray([0, 0, 8, 44, 62, 255, 255, 62, 44, 8, 0, 0])
B_K2 = bytearray([0, 8, 44, 62, 63, 207, 204, 8, 0, 0, 0, 0])

B_RH = bytearray([153, 153, 129, 129, 153, 153, 129, 129, 153, 153, 129, 129])
B_RV = bytearray([0, 0, 255, 0, 0, 51, 51, 0, 0, 255, 0, 0]) 
B_RX = bytearray([0, 0, 0, 0, 0, 24, 24, 0, 0, 0, 0, 0])          
B_SC = bytearray([129, 66, 36, 24, 0, 0, 0, 0, 24, 36, 66, 129])
B_G1 = bytearray([0, 0, 0, 64, 2, 0, 0, 0, 0, 8, 0, 0])
B_G2 = bytearray([0, 0, 0, 0, 64, 2, 0, 0, 8, 0, 0, 0])

F_ECS_1 = bytearray([60, 78, 173, 205, 205, 173, 78, 60])
F_ECS_2 = bytearray([60, 78, 173, 205, 205, 173, 78, 60]) 
F_HAP_1 = bytearray([60, 66, 165, 193, 193, 165, 66, 60]) 
F_HAP_2 = bytearray([60, 66, 169, 193, 193, 165, 66, 60]) 
F_NEU_1 = bytearray([60, 66, 137, 161, 161, 137, 66, 60]) 
F_NEU_2 = bytearray([60, 74, 129, 161, 169, 129, 66, 60]) 
F_SAD_1 = bytearray([60, 66, 201, 161, 161, 201, 66, 60]) 
F_SAD_2 = bytearray([60, 72, 201, 161, 161, 201, 66, 60]) 

C_1 = bytearray([30, 63, 61, 63, 61, 30]) 
C_2 = bytearray([0, 30, 63, 63, 30, 0])   
C_3 = bytearray([0, 0, 63, 63, 0, 0])     
P_1 = bytearray([12, 63, 63, 4, 0, 0])    
P_2 = bytearray([24, 126, 126, 8, 0, 0])  
B_1 = bytearray([0, 36, 22, 31, 13, 0])   
B_2 = bytearray([36, 22, 31, 13, 0, 0])   

DIGIT_FONT = {
    0: bytearray([31, 17, 31]), 1: bytearray([18, 31, 16]), 2: bytearray([29, 21, 23]),
    3: bytearray([21, 21, 31]), 4: bytearray([7, 4, 31]), 5: bytearray([23, 21, 29]),
    6: bytearray([31, 21, 29]), 7: bytearray([1, 1, 31]), 8: bytearray([31, 21, 31]),
    9: bytearray([7, 5, 31]), "k": bytearray([31, 4, 26]), "+": bytearray([4, 14, 4]), "-": bytearray([4, 4, 4]),
}

B_ICONS = {
    RESIDENTIAL: (B_H1, B_H2), COMMERCIAL: (B_S1, B_S2),
    POWERPLANT: (B_Y1, B_Y2), PARK: (B_K1, B_K2),
    RESIDENTIAL_HI: (B_A1, B_A2), COMMERCIAL_HI: (B_P1, B_P2),
}

TWINKLE_POINT = {
    RESIDENTIAL: (4, 5), COMMERCIAL: (2, 4), RESIDENTIAL_HI: (3, 2), COMMERCIAL_HI: (3, 3),
}

SPARKLES = [(0, -2), (8, -1), (0, 6), (8, 6), (4, -2), (4, 6)]
MELODY = [(262, 4), (330, 4), (392, 6), (330, 4), (440, 6), (392, 4), (330, 6), (262, 8)]
MELODY_TOT = sum(d for _, d in MELODY)
CHARS = "0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ"

def playSound(freq, dur):
    try: thumby.audio.play(freq, dur)
    except: pass 

def drawReticle(x, y, w, h):
    thumby.display.drawLine(x, y, x+2, y, 1); thumby.display.drawLine(x, y, x, y+2, 1)
    thumby.display.drawLine(x+w-3, y, x+w-1, y, 1); thumby.display.drawLine(x+w-1, y, x+w-1, y+2, 1)
    thumby.display.drawLine(x, y+h-1, x+2, y+h-1, 1); thumby.display.drawLine(x, y+h-3, x, y+h-1, 1)
    thumby.display.drawLine(x+w-3, y+h-1, x+w-1, y+h-1, 1); thumby.display.drawLine(x+w-1, y+h-3, x+w-1, y+h-1, 1)

def drawNum(n, x, y, is_power=False):
    if n < 0:
        thumby.display.blit(DIGIT_FONT["-"], x, y, 3, 5, 0, 0, 0); x += 4; n = -n
    elif is_power and n >= 0:
        thumby.display.blit(DIGIT_FONT["+"], x, y, 3, 5, 0, 0, 0); x += 4

    suffix = False
    if n >= 10000: n //= 1000; suffix = True
        
    if n == 0: thumby.display.blit(DIGIT_FONT[0], x, y, 3, 5, 0, 0, 0)
    else:
        divisor = 1000
        started = False
        while divisor > 0:
            d = (n // divisor) % 10
            if d > 0 or started:
                thumby.display.blit(DIGIT_FONT[d], x, y, 3, 5, 0, 0, 0); x += 4; started = True
            divisor //= 10
            
    if suffix: thumby.display.blit(DIGIT_FONT["k"], x, y, 3, 5, 0, 0, 0)

def drawSparkle(baseX, baseY, framesLeft):
    idx = framesLeft % len(SPARKLES)
    for i in (idx, (idx + 3) % len(SPARKLES)):
        dx, dy = SPARKLES[i]
        safeSetPixel(baseX + dx, baseY + dy, 1)

def getRoadIcon(r, c):
    n = (r > 0 and grid[r-1][c] == ROAD)
    s = (r < MAP_ROWS - 1 and grid[r+1][c] == ROAD)
    e = (c < MAP_COLS - 1 and grid[r][c+1] == ROAD)
    w = (c > 0 and grid[r][c-1] == ROAD)
    if (n or s) and not (e or w): return B_RV
    if (e or w) and not (n or s): return B_RH
    if not n and not s and not e and not w: return B_RH
    return B_RX

def countNbrs(r, c):
    parks = pwr = com = res = rds = 0; dirs = []
    if r > 0: dirs.append(grid[r-1][c])
    if r < MAP_ROWS - 1: dirs.append(grid[r+1][c])
    if c > 0: dirs.append(grid[r][c-1])
    if c < MAP_COLS - 1: dirs.append(grid[r][c+1])
    
    for n in dirs:
        if n == PARK: parks += 1
        elif n == POWERPLANT: pwr += 1
        elif n in (2, 6): com += 1
        elif n in (1, 5): res += 1
        elif n == ROAD: rds += 1
    return parks, pwr, com, res, rds

def updCam():
    global v_c, v_r
    if c_c < v_c: v_c = c_c
    elif c_c >= v_c + VIEW_COLS: v_c = c_c - VIEW_COLS + 1
    if c_r < v_r: v_r = c_r
    elif c_r >= v_r + VIEW_ROWS: v_r = c_r - VIEW_ROWS + 1
    if v_c < 0: v_c = 0
    if v_c > MAP_COLS - VIEW_COLS: v_c = MAP_COLS - VIEW_COLS
    if v_r < 0: v_r = 0
    if v_r > MAP_ROWS - VIEW_ROWS: v_r = MAP_ROWS - VIEW_ROWS

def loadGame():
    global grid, thriveTicks, money, pop, hScore
    try:
        with open(SAVE_FILE, "r") as f:
            hsLine = f.readline().strip()
            mpLine = f.readline().strip()
            gridLine = f.readline().strip()
            thriveLine = f.readline().strip()
            
        pts = mpLine.split(",")
        m, p = int(pts[0]), int(pts[1])
        if len(gridLine) != MAP_ROWS * MAP_COLS or len(thriveLine) != MAP_ROWS * MAP_COLS: return False
        nG, nT = [], []
        idx = 0
        for r in range(MAP_ROWS):
            gRow, tRow = [], []
            for c in range(MAP_COLS):
                c_val = CHARS.index(gridLine[idx])
                if c_val in (8, 9, 10): c_val = ROAD 
                gRow.append(c_val)
                tRow.append(CHARS.index(thriveLine[idx]))
                idx += 1
            nG.append(gRow); nT.append(tRow)
        grid, thriveTicks = nG, nT
        money, pop, hScore = m, p, max(hScore, int(hsLine))
        gc.collect()
        return True
    except Exception: return False

def saveGame():
    try:
        with open(SAVE_FILE, "w") as f:
            f.write(str(hScore) + "\n")
            f.write(str(money) + "," + str(pop) + "\n")
            for r in range(MAP_ROWS):
                f.write("".join([CHARS[grid[r][c]] for c in range(MAP_COLS)]))
            f.write("\n")
            for r in range(MAP_ROWS):
                f.write("".join([CHARS[thriveTicks[r][c]] for c in range(MAP_COLS)]))
            f.write("\n")
        gc.collect()
    except OSError: pass

def resetCity():
    global grid, thriveTicks, money, pop, happy, pBalance, tkTmr, tkCnt, tkPulse
    global ev_r, ev_c, evFrames, celFrames, winFrames, hudMsgTimer, news_lines
    global c_c, c_r, v_c, v_r
    grid = [[EMPTY] * MAP_COLS for _ in range(MAP_ROWS)]
    thriveTicks = [[0] * MAP_COLS for _ in range(MAP_ROWS)]
    money, pop, happy, pBalance = 100, 0, 50, 0
    tkTmr = tkCnt = 0; tkPulse = False
    ev_r = ev_c = -1
    evFrames = celFrames = winFrames = hudMsgTimer = 0
    news_lines = []
    c_c, c_r = MAP_COLS // 2, MAP_ROWS // 2
    v_c = v_r = 0
    updCam()
    gc.collect()

def runTutorial():
    pages = [
        ["TINY", "SKYLINES", "Grow a huge,", "happy city!"],
        ["CONTROLS:", "DPAD: Camera", "A: Build/Del", "B: Select", "A+B: Restart"],
        ["RULES:", "Homes need", "power & jobs", "Roads boost", "income/happy"],
        ["DANGER:", "Low happy =", "Fires! Keep", "power green.", "Good luck!"]
    ]
    for p in pages:
        while thumby.buttonA.pressed(): thumby.display.update()
        fr = 0
        while True:
            thumby.display.fill(0)
            for i, line in enumerate(p):
                thumby.display.drawText(line, 1, i * 8, 1)
                
            if (fr // 10) % 2 == 0:
                thumby.display.drawText(">", 65, 32, 1)
                
            thumby.display.update()
            fr += 1
            if thumby.buttonA.justPressed(): break
            
    while thumby.buttonA.pressed(): thumby.display.update()
    gc.collect()

def triggerEv():
    global money, happy, ev_r, ev_c, evFrames, winFrames, news_lines
    roll = random.randint(1, 250)
    
    if roll == 1:
        news_lines = ["EARTHQUAKE!", "City ruins", "-3 Bldgs"]
        for _ in range(3):
            r, c = random.randint(0, MAP_ROWS-1), random.randint(0, MAP_COLS-1)
            if grid[r][c] not in (EMPTY, ROAD):
                grid[r][c] = EMPTY; thriveTicks[r][c] = 0
                ev_r, ev_c, evFrames = r, c, 40
        playSound(100, 800)
        
    elif roll == 2:
        news_lines = ["ELECTION!", "New Mayor", "+20 Happy"]
        happy += 20; playSound(400, 200)
        
    elif roll == 3:
        news_lines = ["WALL ST.", "Tech rally", "+$50"]
        money += 50; playSound(800, 200)
        
    elif roll == 4:
        news_lines = ["RECESSION", "Economy down", "-$30"]
        money -= 30; playSound(150, 400)
        
    elif happy <= 30 and roll <= 15:
        cds = [(r, c) for r in range(MAP_ROWS) for c in range(MAP_COLS) if grid[r][c] not in (EMPTY, ROAD)]
        if cds:
            r, c = cds[random.randint(0, len(cds) - 1)]
            grid[r][c] = EMPTY; thriveTicks[r][c] = 0
            ev_r, ev_c, evFrames = r, c, 40
            news_lines = ["ARSON!", "Block burns", "-1 Bldg"]
            playSound(60, 400)
            
    elif happy >= 70 and roll <= 25:
        gain = random.randint(15, 40)
        money += gain; winFrames = 40
        news_lines = ["FESTIVAL!", "Tourists in", "+$" + str(gain)]
        playSound(900, 150)

def simTick():
    global money, pop, happy, pBalance, hScore, tkPulse
    global tkCnt, celFrames, grid, thriveTicks

    rHap = rCnt = tInc = tJob = tUpk = 0
    tCap = tDem = tSup = occ = 0
    upgrades = False

    for r in range(MAP_ROWS):
        for c in range(MAP_COLS):
            cl = grid[r][c]
            if cl == EMPTY or cl in ROAD_TYPES: continue
                
            pN, pwN, cN, rsN, rdN = countNbrs(r, c)

            if cl in (1, 5):
                occ += 1; hi = (cl == 5)
                tCap += 8 if hi else 4
                tDem += 1
                if hi: tUpk += 1 

                lHap = (50 + pN * 6 - pwN * 5 + cN * 2 + rdN * 3)
                rHap += lHap; rCnt += 1

                if not hi:
                    if lHap >= 58:
                        thriveTicks[r][c] += 1
                        if thriveTicks[r][c] >= 8:
                            grid[r][c] = 5; thriveTicks[r][c] = 0; upgrades = True
                    else: thriveTicks[r][c] = 0

            elif cl in (2, 6):
                occ += 1; hi = (cl == 6)
                tJob += 8 if hi else 4
                tDem += 1
                if hi: tUpk += 1 

                bs = 6 if hi else 3
                tInc += (bs * (100 + rsN * 15 + rdN * 10)) // 100

                if not hi:
                    if rsN >= 1:
                        thriveTicks[r][c] += 1
                        if thriveTicks[r][c] >= 8:
                            grid[r][c] = 6; thriveTicks[r][c] = 0; upgrades = True
                    else: thriveTicks[r][c] = 0

            elif cl == 3:
                tSup += 6; tUpk += 2 
        
    if upgrades: playSound(700, 100)

    aHap = (rHap // rCnt) if rCnt > 0 else 50
    pBalance = tSup - tDem - ((occ // 3) if isNight else 0)

    unem = max(0, pop - tJob)
    unemPen = min(25, unem // 3)
    cPen = pop // 25
    pwPen = 20 if pBalance < 0 else 0 
    dbPen = 15 if money < 0 else 0 

    happy = aHap - unemPen - cPen - pwPen - dbPen
    if happy < 0: happy = 0
    if happy > 100: happy = 100

    if pBalance >= 0:
        gap = tCap - pop
        if gap > 0 and happy > 15:
            pop += max(1, (gap * 20 * happy) // 10000)
            if pop > tCap: pop = tCap
        elif gap < 0:
            pop = max(0, pop - max(1, (-gap) // 3))
        money += (tInc * happy) // 100 + ((pop + 1) // 2)
    else:
        pop = max(0, pop - max(1, (pop * 15) // 100))
        money += (pop + 1) // 4
        
    money -= tUpk

    if pop > hScore:
        hScore = pop; celFrames = 40; playSound(1000, 150)

    triggerEv()
    tkCnt += 1; tkPulse = not tkPulse
    if upgrades or tkCnt % 10 == 0: saveGame()

def hasSav():
    if pop > 0: return True
    for row in grid:
        for cell in row:
            if cell != EMPTY: return True
    return False

def playMenuMusic(frame):
    pos = frame % MELODY_TOT; acc = 0
    for f, d in MELODY:
        if pos < acc + d:
            if pos == acc: playSound(f, int(d * 100))
            return
        acc += d

def showTitle():
    opts = ["CONTINUE", "NEW GAME"] if hasSav() else ["NEW GAME"]
    mIdx = fr = 0
    SUN_W = [11, 10, 10, 10, 10, 9, 9, 8, 7, 6, 4, 2]
    
    while True:
        if thumby.buttonU.justPressed(): mIdx = (mIdx - 1) % len(opts)
        if thumby.buttonD.justPressed(): mIdx = (mIdx + 1) % len(opts)
        if thumby.buttonA.justPressed(): break

        playMenuMusic(fr); thumby.display.fill(0)

        for i in range(15): safeSetPixel((i * 17 - fr // 2) % 72, (i * 9) % 18, 1)

        for dy in range(-11, 12):
            w = SUN_W[abs(dy)]; y = 18 + dy
            if y > 8 and (y + fr // 3) % 4 <= (y - 8) // 3: continue
            thumby.display.drawLine(36 - w, y, 36 + w, y, 1)

        offset = (fr // 2) % 30
        b_idx = (fr // 2) // 30
        draw_x = -offset
        
        for i in range(b_idx, b_idx + 10):
            w = ((i * 11) % 6) + 6; h = ((i * 23) % 14) + 4
            thumby.display.drawFilledRectangle(draw_x, 20 - h, w, h, 0)
            thumby.display.drawRectangle(draw_x, 20 - h, w, h, 1)
            if h > 6 and w > 4:
                safeSetPixel(draw_x + 2, 20 - h + 2, 1)
                safeSetPixel(draw_x + w - 3, 20 - h + 5, 1)
            draw_x += w

        for i in range(-5, 6): thumby.display.drawLine(36 + i * 4, 20, 36 + i * 20, 40, 1)

        speed_int = fr % 10
        for i in range(1, 5):
            z = (i * 10) - speed_int
            if z > 0:
                y = 20 + (200 // z)
                if y < 40: thumby.display.drawLine(0, y, 72, y, 1)

        thumby.display.drawFilledRectangle(0, 0, 72, 7, 1)
        thumby.display.drawText("TINY SKYLINES", 0, 1, 0)
        thumby.display.drawFilledRectangle(0, 33, 72, 7, 0)
        thumby.display.drawText(opts[mIdx], 2, 33, 1)

        if fr % 20 < 10:
            safeSetPixel(65, 34, 1); safeSetPixel(66, 35, 1); safeSetPixel(65, 36, 1)

        fr += 1; thumby.display.update()

    if opts[mIdx] == "NEW GAME": 
        resetCity()
        saveGame()
        runTutorial()

# --- GLOBALS INIT ---
hScore = money = pop = happy = pBalance = tkTmr = tkCnt = 0
grid = thriveTicks = []
isNight = tkPulse = False
ev_r = ev_c = -1
evFrames = celFrames = winFrames = hudMsgTimer = 0
news_lines = []
c_c = c_r = v_c = v_r = 0

if not loadGame(): resetCity(); saveGame()
updCam()

selIdx = cmb = elp = move_tmr = 0
showTitle()

input_cd = 15 

# --- MAIN LOOP ---
while True:
    elp = (elp + 1) % 10000

    # The Newspaper Event Overlay Intercepts the Loop
    if news_lines:
        thumby.display.fill(0)
        thumby.display.drawFilledRectangle(2, 2, 68, 36, 1)
        thumby.display.drawFilledRectangle(3, 3, 66, 34, 0)
        thumby.display.drawText("TINY TIMES", 6, 5, 1)
        thumby.display.drawLine(4, 13, 67, 13, 1)
        
        y_pos = 15
        for line in news_lines:
            thumby.display.drawText(line, 6, y_pos, 1)
            y_pos += 7
            
        if (elp // 10) % 2 == 0:
            thumby.display.drawFilledRectangle(58, 27, 9, 9, 1)
            thumby.display.drawText("A", 60, 28, 0)
            
        thumby.display.update()
        
        if thumby.buttonA.justPressed():
            news_lines = []
            input_cd = 15
        continue # Freezes game simulation while reading paper!

    tkTmr += 1
    isNight = (tkCnt // 12) % 2 == 1

    if input_cd > 0: input_cd -= 1

    if thumby.buttonA.pressed() and thumby.buttonB.pressed():
        cmb += 1
        if cmb == 30:
            resetCity(); saveGame(); playSound(200, 200); cmb = 0
    else:
        cmb = 0
        dx = thumby.buttonR.pressed() - thumby.buttonL.pressed()
        dy = thumby.buttonD.pressed() - thumby.buttonU.pressed()
        
        if dx != 0 or dy != 0:
            if move_tmr == 0:
                c_c = (c_c + dx) % MAP_COLS
                c_r = (c_r + dy) % MAP_ROWS
                updCam(); move_tmr = 3 
            else: move_tmr -= 1
        else: move_tmr = 0

        if thumby.buttonB.justPressed() and input_cd == 0:
            selIdx = (selIdx + 1) % len(BUILD_ORDER)
            hudMsgTimer = 40; input_cd = 6

        if thumby.buttonA.justPressed() and input_cd == 0:
            input_cd = 6
            cl = grid[c_r][c_c]
            if cl == EMPTY:
                bt = BUILD_ORDER[selIdx]; cst = BUILD_COSTS[bt]
                if money >= cst:
                    money -= cst; grid[c_r][c_c] = bt; thriveTicks[c_r][c_c] = 0
                    playSound(600, 60); saveGame()
                else: playSound(120, 150)
            else:
                money += BUILD_COSTS[cl] // 4
                grid[c_r][c_c] = EMPTY; thriveTicks[c_r][c_c] = 0
                playSound(350, 60); saveGame()

    if tkTmr >= 60:
        tkTmr = 0; simTick()

    # --- Draw Map ---
    thumby.display.fill(0) 
    aFr = (elp // 10) % 2

    for vr in range(VIEW_ROWS):
        for vc in range(VIEW_COLS):
            r, c = v_r + vr, v_c + vc
            cl = grid[r][c]
            x, y = vc * TILE_W, vr * TILE_H
            
            if cl == ROAD:
                thumby.display.blit(getRoadIcon(r, c), x, y, TILE_W, TILE_H, 0, 0, 0)
                if isNight and (r * MAP_COLS + c + elp // 20) % 10 == 0: safeSetPixel(x + 5, y + 4, 1)

            elif cl != EMPTY:
                thumby.display.blit(B_ICONS[cl][aFr], x, y, TILE_W, TILE_H, 0, 0, 0)
                if isNight and cl in TWINKLE_POINT:
                    if (r * MAP_COLS + c + elp // 20) % 10 == 0:
                        tx, ty = TWINKLE_POINT[cl]
                        safeSetPixel(x + tx, y + ty, 1)
                        
            elif r == ev_r and c == ev_c and evFrames > 0:
                thumby.display.blit(B_SC, x, y, TILE_W, TILE_H, 0, 0, 0)
            else:
                if (r * 7 + c * 11) % 5 == 1: 
                    icon = B_G1 if aFr == 0 else B_G2
                    thumby.display.blit(icon, x, y, TILE_W, TILE_H, 0, 0, 0)

    if evFrames > 0: evFrames -= 1

    cxPix, cyPix = (c_c - v_c) * TILE_W, (c_r - v_r) * TILE_H
    drawReticle(cxPix, cyPix, TILE_W, TILE_H)
    
    cursorOnEvent = (c_r == ev_r and c_c == ev_c and evFrames > 0)
    if grid[c_r][c_c] == EMPTY and not cursorOnEvent:
        bt = BUILD_ORDER[selIdx]
        if money >= BUILD_COSTS[bt]:
            if elp % 2 == 0:
                g_icon = getRoadIcon(c_r, c_c) if bt == ROAD else B_ICONS[bt][aFr]
                thumby.display.blit(g_icon, cxPix, cyPix, TILE_W, TILE_H, 0, 0, 0)

    # --- LIVING HUD ---
    if cmb > 0:
        thumby.display.drawFilledRectangle(0, HUD_Y, int(72 * cmb / 30), 8, 1)
        
    elif hudMsgTimer > 0:
        hudMsgTimer -= 1
        bt = BUILD_ORDER[selIdx]
        thumby.display.drawFilledRectangle(0, HUD_Y, 72, 8, 0) 
        thumby.display.drawText(BUILD_HINTS[bt], 0, HUD_Y + 1, 1)
        
    else:
        thumby.display.drawLine(0, 31, 72, 31, 1)
        
        f_y = 32
        if happy >= 80:
            fc = F_ECS_1 if (elp // 8) % 2 == 0 else F_ECS_2
            f_y -= ((elp % 8) // 4) 
        elif happy >= 50:
            fc = F_HAP_2 if (elp % 40) < 5 else F_HAP_1
        elif happy >= 30:
            fc = F_NEU_2 if (elp % 30) < 10 else F_NEU_1
        else:
            fc = F_SAD_1 if (elp // 4) % 2 == 0 else F_SAD_2
        thumby.display.blit(fc, 0, f_y, 8, 8, 0, 0, 0)

        coin_frs = [C_1, C_2, C_3, C_2]
        thumby.display.blit(coin_frs[(elp // 5) % 4], 9, 33, 6, 6, 0, 0, 0)
        drawNum(money, 16, 34, False)
        if winFrames > 0: drawSparkle(9, 33, winFrames); winFrames -= 1

        thumby.display.blit((P_2 if aFr == 0 else P_1), 31, 33, 6, 6, 0, 0, 0)
        drawNum(pop, 38, 34, False)
        if celFrames > 0: drawSparkle(31, 33, celFrames); celFrames -= 1

        if pBalance < 0:
            b_ic = B_1 if (elp % 4) < 2 else B_2
        else:
            b_ic = B_1 if (elp // 10) % 2 == 0 else B_2
        thumby.display.blit(b_ic, 52, 33, 6, 6, 0, 0, 0)
        drawNum(pBalance, 59, 34, True)
        
        if tkPulse: thumby.display.drawFilledRectangle(70, 35, 2, 2, 1)

    thumby.display.update()