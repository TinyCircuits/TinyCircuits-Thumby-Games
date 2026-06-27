import thumby
import random
import time
from machine import ADC

adc = ADC(26)

charging = 38000
level_1 = 33700
level_2 = 34300
level_3 = 35400

batt0 = bytearray([31,17,17,17,17,17,17,17,17,27,14])
batt1 = bytearray([31,31,31,31,17,17,17,17,17,27,14])
batt2 = bytearray([31,31,31,31,31,31,31,17,17,27,14])
batt3 = bytearray([31,31,31,31,31,31,31,31,31,31,14])
charg = bytearray([31,31,27,27,9,0,18,27,27,31,14])
emula = bytearray([31,21,17,0,31,2,31,0,31,16,31])

random.seed(time.ticks_ms())

# ---------------- SETTINGS ----------------
debt = 0
loanCount = 0
MAX_LOANS = 3
debtRounds = 0
DEBT_LIMIT = 10
CARD_W = 13
CARD_H = 15
allIn = False
money = 100
HIGH_SCORE_FILE = "highscore.txt"
highScore = 0
bestStreak = 0
BEST_STREAK_FILE = "beststreak.txt"
streak = 0
bet = 0
difficulty = "NORMAL"  # or "HARD"
gameOver = False

# ---------------- HIGHSCORE ----------------
def loadHighScore():
    global highScore
    try:
        f = open(HIGH_SCORE_FILE, "r")
        highScore = int(f.read())
        f.close()
    except:
        highScore = 0

def saveHighScore():
    f = open(HIGH_SCORE_FILE, "w")
    f.write(str(highScore))
    f.close()
    
# ---------------- HIGHSTREAK ----------------
def loadBestStreak():
    global bestStreak
    try:
        f = open(BEST_STREAK_FILE, "r")
        bestStreak = int(f.read())
        f.close()
    except:
        bestStreak = 0

def saveBestStreak():
    f = open(BEST_STREAK_FILE, "w")
    f.write(str(bestStreak))
    f.close()

# ---------------- INPUT ----------------

prevA = False
prevB = False
prevU = False
prevD = False
prevL = False
prevR = False

def beep():
    thumby.audio.play(1000, 50)  # freq, duration (ms)

def pressA():
    global prevA
    a = thumby.buttonA.pressed()
    out = a and not prevA
    prevA = a
    if out:
        beep()
    return out

def pressB():
    global prevB
    b = thumby.buttonB.pressed()
    out = b and not prevB
    prevB = b
    if out:
        beep()
    return out

def pressU():
    global prevU
    u = thumby.buttonU.pressed()
    out = u and not prevU
    prevU = u
    if out:
        beep()
    return out

def pressD():
    global prevD
    d = thumby.buttonD.pressed()
    out = d and not prevD
    prevD = d
    if out:
        beep()
    return out

def pressL():
    global prevL
    l = thumby.buttonL.pressed()
    out = l and not prevL
    prevL = l
    if out:
        beep()
    return out

def pressR():
    global prevR
    l = thumby.buttonR.pressed()
    out = l and not prevR
    prevR = l
    if out:
        beep()
    return out
# ---------------- Battery ----------------
def animateCard(x, y, val):
    for i in range(-10, y + 1, 2):
        thumby.display.fill(0)
        drawCard(x, i, val)
        thumby.display.update()

# ---------------- Battery ----------------

def drawBattery():
    v = adc.read_u16()

    if v > charging:
        thumby.display.blit(charg, 61, 0, 11, 5, -1, 0, 0)
    elif v > level_3:
        thumby.display.blit(batt3, 61, 0, 11, 5, -1, 0, 0)
    elif v > level_2:
        thumby.display.blit(batt2, 61, 0, 11, 5, -1, 0, 0)
    elif v > level_1:
        thumby.display.blit(batt1, 61, 0, 11, 5, -1, 0, 0)
    else:
        thumby.display.blit(batt0, 61, 0, 11, 5, -1, 0, 0)

# ---------------- GAME LOGIC ----------------
def newCard():
    return random.randint(1, 13)

def handValue(hand):
    v = 0
    aces = 0

    for c in hand:
        if c == 1:
            v += 1
            aces += 1
        else:
            v += 10 if c >= 10 else c

    for _ in range(aces):
        if v + 10 <= 21:
            v += 10

    return v

# ---------------- DRAW ----------------

def drawCard(x, y, val, hidden=False):
    thumby.display.drawRectangle(x, y, CARD_W, CARD_H, 1)

    if hidden: #ahhhh whatever
        thumby.display.drawLine(x+1, y+1, x+CARD_W-2, y+CARD_H-2, 1)
        thumby.display.drawLine(x+1, y+CARD_H-2, x+CARD_W-2, y+1, 1)
        return

    if val == 1:
        s = "A"
        ox = 4
    elif val == 11:
        s = "J"
        ox = 4
    elif val == 12:
        s = "Q"
        ox = 4
    elif val == 13:
        s = "K"
        ox = 4
    else:
        s = str(val)

        if val == 10:
            ox = 1  # shift left so it fits clean
        else:
            ox = 4

    thumby.display.drawText(s, x + ox, y + 4, 1)


# TWO ROW HAND (MAX 10 CARDS)
def drawHand(hand, hidden_second=False):
    start_x = 0
    bottom_y = 25
    top_y = 10

    for i, c in enumerate(hand[:10]):  # max 10 cards
        if i < 5:
            x = start_x + (i * (CARD_W + 1))
            y = bottom_y
        else:
            x = start_x + ((i - 5) * (CARD_W + 1))
            y = top_y

        drawCard(x, y, c, hidden_second and i == 1)

# ---------------- SHAKE ----------------
def shake():
    return random.randint(0, 2)
# ---------------- RESULT ----------------

def playWinTune(step):
    notes = [523, 659, 784, 1046]
    thumby.audio.play(notes[step % 4], 80)
    
def playLoseTune(step):
    notes = [400, 350, 300, 200] 
    thumby.audio.play(notes[step % 4], 200)
    
def shutdownTune():
    notes = [200, 180, 160, 140, 120]
    for n in notes:
        thumby.audio.play(n, 200)
        time.sleep(0.25)

def resultScreen(msg, win, dealer_total, player_total):
    global money, streak, bet, highScore, bestStreak, debt, debtRounds, loanCount, gameOver

    if gameOver:
        shutdownTune()
    
        while True:
            thumby.display.fill(0)
            thumby.display.drawText("LONESHARK", shake(), 5, 1)
            thumby.display.drawText("GOT YOU!", shake(), 15, 1)
            thumby.display.drawText("A: Quit", 0, 30, 1)
            thumby.display.update()
    
            if pressA():
                import sys
                sys.exit()


    mult = 1 + (streak * 0.5)
    
    if msg == "DRAW":
        pass
    
    else:
        if allIn:
            if win:
                money *= 2
                streak += 1
            else:
                money = 0
                streak = 0
        else:
            if win:
                winnings = int(bet * mult)
                money += winnings
                streak += 1
            else:
                money -= max(0, bet)
                streak = 0
                
    if debt > 0 and money > 0:
        debt = max(0, debt)
        debtRounds = max(0, debtRounds)

    if debt > 0:
        debtRounds += 1
    else:
        debtRounds = 0
        
    if debt > 0 and debtRounds >= DEBT_LIMIT:
        if money >= debt:
            money -= debt
            debt = 0
            debtRounds = 0
            gameOver = False
        else:
            gameOver = True


    if money > highScore:
        highScore = money
        saveHighScore()
    if streak > bestStreak:
        bestStreak = streak
        saveBestStreak()

    tuneStep = 0
    timer = 0
    time.sleep(0.15)

    while True:
        thumby.display.fill(0)

        if msg == "WIN":
            size = (timer // 10) % 2
            offset = 2 if size == 0 else 1
            thumby.display.drawText("WIN", 1 + offset, 0 + offset, 1)
            thumby.display.drawText("You:"+str(player_total), 0, 11, 1)
            thumby.display.drawText("House:"+str(dealer_total), 0, 22, 1)
        elif msg == "DRAW":
            thumby.display.drawText("DRAW", 0, 0, 1)
            thumby.display.drawText("You:"+str(player_total), 0, 11, 1)
            thumby.display.drawText("House:"+str(dealer_total), 0, 22, 1)
        else:
            thumby.display.drawText(msg, 0 + shake(), 0 + shake(), 1)
            thumby.display.drawText("You:"+str(player_total), 0 + shake(), 11 + shake(), 1)
            thumby.display.drawText("House:"+str(dealer_total), 0 + shake(), 22 + shake(), 1)

        thumby.display.drawText("$"+str(money), 40, 0, 1)
        thumby.display.drawText("x"+str(round(mult,1)), 45, 11, 1)
        thumby.display.drawText("Streak:"+str(streak), 0, 33, 1)

        if msg == "WIN":
            if timer % 12 == 0:
                playWinTune(tuneStep)
                tuneStep += 1
        
        elif msg == "LOSE" or msg == "BUST":
            if timer % 50 == 0:
                playLoseTune(tuneStep)
                tuneStep += 1

        thumby.display.update()
        
        timer += 1

        if pressA():
            if gameOver:
                shutdownTune()
                while True:
                    thumby.display.fill(0)
                    thumby.display.drawText("LONESHARK", shake(), 5, 1)
                    thumby.display.drawText("GOT YOU!", shake(), 15, 1)
                    thumby.display.drawText("A: Quit", 0, 30, 1)
                    thumby.display.update()
        
                    if pressA():
                        import sys
                        sys.exit()
            return

# ---------------- TIPS SCREEN ----------------
def tipsScreen():
    page = 0

    while True:
        thumby.display.fill(0)

        drawBattery()

        if page == 0:
            thumby.display.drawText("TIPS 1/4", 0, 0, 1)
            thumby.display.drawText("A: Hit", 0, 9, 1)
            thumby.display.drawText("B: Stand", 0, 17, 1)
            thumby.display.drawText("U: Dealer", 0, 25, 1)
            thumby.display.drawText("D: Pay Debts", 0, 33, 1)
        elif page == 1:
            thumby.display.drawText("TIPS 2/4", 0, 0, 1)
            thumby.display.drawText("D: Double or", 0, 9, 1)
            thumby.display.drawText("   Nothing", 0, 17, 1)
            thumby.display.drawText("   At start", 0, 25, 1)
            thumby.display.drawText("   of hand", 0, 33, 1)
        elif page == 2:
            thumby.display.drawText("TIPS 3/4", 0, 0, 1)
            thumby.display.drawText("Take Loan on", 0, 12, 1)
            thumby.display.drawText("HIGHSCORE pg", 0, 22, 1)
            thumby.display.drawText("Auth Dylan R", 0, 33, 1)
        else:
            thumby.display.drawText("TIPS 4/4", 0, 0, 1)
            thumby.display.drawText("You have 10", 0, 12, 1)
            thumby.display.drawText("hands to pay", 0, 22, 1)
            thumby.display.drawText("your debt!", 0, 33, 1)
        thumby.display.update()

        if pressR():
            page = (page + 1) % 4
                
        if pressL():
            page = (page - 1) % 4

        if pressB():
            return

# ---------------- STATS SCREEN ----------------
def statsScreen():
    global money, debt, debtRounds, loanCount
    page = 0

    hold = 0

    while True:
        thumby.display.fill(0)
        if page == 0:
            thumby.display.drawText("HIGHSCORE >", 0, 0, 1)
            thumby.display.drawText("Money:", 0, 9, 1)
            thumby.display.drawText("$"+str(highScore), 0, 17, 1)
            thumby.display.drawText("Streak:", 0, 25, 1)
            thumby.display.drawText(""+str(bestStreak), 0, 33, 1)
        else:
            thumby.display.drawText("LOANS: "+str(loanCount)+"/3", 0, 0, 1)
            thumby.display.drawText("HOLD D TO", 0, 13, 1)
            thumby.display.drawText("TAKE LOAN", 0, 23, 1)
            thumby.display.drawText("IF UR BROKE", 0, 33, 1)

        thumby.display.update()
        
        if pressR():
            page = (page + 1) % 2
                
        if pressL():
            page = (page - 1) % 2


        if thumby.buttonD.pressed() and money < 10:
            hold += 1
        
            if hold > 120:
        
                if loanCount < MAX_LOANS:
                    loan = 100
                    money += loan
                    debt += int(loan * 1.5)
                    debtRounds = 0
                    loanCount += 1
                    beep()
                else:
                    thumby.audio.play(200, 100)
        
                hold = 0

        else:
            if hold > 0:
                hold = 0
            if pressB():
                return

# ---------------- BET SCREEN ----------------

def formatBet(val):
    return "$" + str(val)

def betScreen():
    blink = 0
    global bet, money, debt, debtRounds, loanCount

    options = ["NO", 5, 10, 20, 30, 40, 50, "ALL!"]
    i = 0

    while True:
        thumby.display.fill(0)

        thumby.display.drawText("BET", 7, 0, 1)
        thumby.display.drawText("<", 0, 0, 1)
        thumby.display.drawText(">", 26, 0, 1)
        thumby.display.drawText(formatBet(options[i]), 26, 16, 1)
        if blink < 80:
            thumby.display.drawText("^", 35, 26, 1)

        thumby.display.drawText("$"+str(money), 0, 32, 1)
        if debt > 0:
            thumby.display.drawText("D:"+str(debt), 43, 0, 1)
            remaining = DEBT_LIMIT - debtRounds
            if remaining == 2:
                x_off = random.randint(0, 1)
                y_off = random.randint(0, 1)
            
            elif remaining == 1:
                x_off = random.randint(-2, 2)
                y_off = random.randint(-2, 2)
            
            else:
                x_off = 0
                y_off = 0
            
            thumby.display.drawText(str(remaining), 60 + x_off, 32 + y_off, 1)

        thumby.display.update()
        
        blink = (blink + 1) % 100
        
        if pressL():
            statsScreen()
            
        if pressR():
            tipsScreen()
            
        if pressU():
            i = (i + 1) % len(options)
            
        if pressD() and debt > 0 and money >= 10:
            money -= 10
            debt -= 10
            if debt < 0:
                debt = 0

        if pressA():
            if options[i] == "NO":
                bet = 0
                return
            elif options[i] == "ALL!":
                bet = money
                return
            elif options[i] <= money:
                bet = options[i]
                return
        if pressB():  # back
            titleScreen()
# ---------------- TITLE ----------------
def titleScreen():
    global difficulty

    blink = 0

    # 0 = NORMAL (+), 1 = HARD (++)
    i = 0
    if difficulty == "HARD":
        i = 1

    while True:
        thumby.display.fill(0)

        thumby.display.drawText("BLACKJACK", 9, 0, 1)
        thumby.display.drawText("HI:"+str(highScore), 0, 32, 1)

        # card visual (unchanged)
        thumby.display.drawRectangle(28, 11, 14, 17, 1)
        thumby.display.drawText("J", 32, 15, 1)

        # --- STACKED OPTIONS ---
        y1 = 12   # "+"
        y2 = 22   # "++"

        thumby.display.drawText("+", 54, y1, 1)
        thumby.display.drawText("++", 54, y2, 1)

        # --- MOVING ARROW ---
        if blink < 80:
            arrow_y = y1 if i == 0 else y2
            thumby.display.drawText(">", 46, arrow_y, 1)

        thumby.display.update()
        blink = (blink + 1) % 100

        # move selection
        if pressU() or pressD():
            i = (i + 1) % 2
            difficulty = "HARD" if i == 1 else "NORMAL"

        if pressA():
            return
        if pressB():
            return
# ---------------- MAIN ----------------
loadHighScore()
loadBestStreak()

titleScreen()

while True:

    betScreen()
    allIn = False

    while True:
        player = [newCard(), newCard()]
        if handValue(player) <= 11:
            break

    dealer = [newCard(), newCard()]
    state = "play"
    view = "player"

    while True:
        thumby.display.fill(0)

        pv = handValue(player)
        dv = handValue(dealer)

        if pressU():
            view = "dealer" if view == "player" else "player"

        if view == "player":
            thumby.display.drawText("YOUR HAND:"+str(pv), 0, 0, 1)
            drawHand(player)
        else:
            thumby.display.drawText("DEALERS HAND", 0, 0, 1)
            drawHand(dealer, hidden_second=(state == "play"))

        if state == "play":

            if pressD() and not allIn and len(player) == 2:
            
                allIn = True
                bet *= 2
            
                c = newCard()
                player.append(c)
                animateCard(0, 25, c)
                pv = handValue(player)
            
                t = 0
                while t < 300:
                    thumby.display.fill(0)
            
                    thumby.display.drawText("DOUBLE!", 18, 0, 1)
                    thumby.display.drawText("OR NOTHING!", 4, 10, 1)

                    drawHand(player)
            
                    thumby.display.update()
                    t += 1
            
                if pv > 21:
                    resultScreen("BUST", False, dv, pv)
                    break
            
                state = "dealer"

            if pressA():
                if len(player) < 10:
                    c = newCard()
                    player.append(c)
                    animateCard(0, 25, c)
                    pv = handValue(player)

                    if pv > 21:
                        t = 0
                        while t < 240:
                            thumby.display.fill(0)
                            thumby.display.drawLine(0, 0, 72, 33, 1)
                            thumby.display.drawLine(72, 0, 0, 33, 1)
                            thumby.display.drawText("YOUR HAND:"+str(pv), 0, 00, 1)
                            drawHand(player)
    
                            thumby.display.update()
                            t += 1
    
                        resultScreen("BUST", False, dv, pv)
                        break
    
                        c = newCard()
                        player.append(c)
                        animateCard(0, 25, c)
                        pv = handValue(player)  # recalc ONCE after draw
                        if pv > 21:
                            resultScreen("BUST", False, dv, pv)
                            break

            if pressB():
                state = "dealer"

        if state == "dealer":
            limit = 17 if difficulty == "NORMAL" else 19
            if dv < limit and len(dealer) < 10:
                dealer.append(newCard())
            else:
                if dv > 21 or pv > dv:
                    resultScreen("WIN", True, dv, pv)
                elif pv == dv:
                    resultScreen("DRAW", False, dv, pv)
                else:
                    resultScreen("LOSE", False, dv, pv)
                break

        thumby.display.update()
