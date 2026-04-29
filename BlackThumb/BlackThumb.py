import thumby
import random
import time

# TRUE RANDOM
random.seed(time.ticks_ms())

# ---------------- SETTINGS ----------------

CARD_W = 13
CARD_H = 15
allIn = False
money = 100
HIGH_SCORE_FILE = "highscore.txt"
highScore = 0
streak = 0
bet = 0

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

# ---------------- RESULT ----------------
def playWinTune(step):
    notes = [523, 659, 784, 1046]
    thumby.audio.play(notes[step % 4], 80)
    
def playLoseTune(step):
    notes = [400, 350, 300, 200] 
    thumby.audio.play(notes[step % 4], 200)

def resultScreen(msg, win, dealer_total, player_total):
    global money, streak, bet, highScore


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

    if money > highScore:
        highScore = money
        saveHighScore()


    tuneStep = 0
    timer = 0

    while True:
        thumby.display.fill(0)

        thumby.display.drawText(msg, 0, 0, 1)
        thumby.display.drawText("You:"+str(player_total), 0, 11, 1)
        thumby.display.drawText("House:"+str(dealer_total), 0, 22, 1)

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
            return

# ---------------- TIPS SCREEN ----------------
def tipsScreen():
    page = 0

    while True:
        thumby.display.fill(0)

        if page == 0:
            thumby.display.drawText("TIPS 1/2", 0, 0, 1)
            thumby.display.drawText("2x or 0 =", 0, 10, 1)
            thumby.display.drawText("Down Button", 0, 20, 1)
            thumby.display.drawText("Auth Dylan R", 0, 33, 1)

        else:
            thumby.display.drawText("TIPS 2/2", 0, 0, 1)
            thumby.display.drawText("A: Hit", 0, 9, 1)
            thumby.display.drawText("B: Stand", 0, 17, 1)
            thumby.display.drawText("U: Bet(Menu)", 0, 25, 1)
            thumby.display.drawText("U: Dealer", 0, 33, 1)

        thumby.display.update()

        if pressR():
            page = (page + 1) % 2   # toggle pages

        if pressL():
            page = (page - 1) % 2   # optional back page toggle

        if pressB():
            return

# ---------------- STATS SCREEN ----------------
def statsScreen():
    while True:
        thumby.display.fill(0)

        thumby.display.drawText("STATS", 0, 0, 1)
        thumby.display.drawText("$"+str(money), 43, 0, 1)
        thumby.display.drawText("Best:"+str(highScore), 0, 12, 1)
        thumby.display.drawText("Streak:"+str(streak), 0, 22, 1)
        mult = 1 + (streak * 0.5)
        thumby.display.drawText("Mult:"+str(round(mult,1)), 0, 32, 1)

        thumby.display.update()

        if pressB():  # back
            return
        
# ---------------- BET SCREEN ----------------

def formatBet(val):
    return "$" + str(val)

def betScreen():
    blink = 0
    global bet, money

    options = ["NO", 10, 20, 30, 40, 50, "ALL"]
    i = 0

    while True:
        thumby.display.fill(0)

        thumby.display.drawText("< BETTINGS >", 0, 0, 1)
        thumby.display.drawText(formatBet(options[i]), 26, 16, 1)
        if blink < 80:
            thumby.display.drawText("^", 35, 26, 1)

        thumby.display.drawText("$"+str(money), 0, 32, 1)

        thumby.display.update()
        
        blink = (blink + 1) % 100
        
        if pressL():
            statsScreen()
            
        if pressR():
            tipsScreen()
            
        if pressU():
            i = (i + 1) % len(options)

        if pressA():
            if options[i] == "ALL":
                bet = money
                return
            elif options[i] == "NO":
                bet = 0
                return
            elif options[i] <= money:
                bet = options[i]
                return
        if pressB():  # back
            titleScreen()
# ---------------- TITLE ----------------
def titleScreen():
    blink = 0
    y = 12
    tuneStep = 0

    while True:
        thumby.display.fill(0)

        thumby.display.drawText("BLACKJACK", 9, 0, 1)
        thumby.display.drawText(" BEST:"+str(highScore), 0, 32, 1)
        thumby.display.drawRectangle(28, y-1, 14, 17, 1)
        thumby.display.drawText("J", 32, y + 4, 1)

        if blink < 80:
            thumby.display.drawText("A", 62, 32, 1)

        thumby.display.update()

        blink = (blink + 1) % 100

        if pressA():
            return

loadHighScore()

# ---------------- MAIN ----------------

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
            
                # draw the extra card
                player.append(newCard())
                pv = handValue(player)
            
                t = 0
                while t < 180:
                    thumby.display.fill(0)
            
                    thumby.display.drawText("DOUBLE!", 18, 0, 1)
                    thumby.display.drawText("OR NOTHING", 7, 10, 1)

                    drawHand(player)
            
                    thumby.display.update()
                    t += 1
            
                if pv > 21:
                    resultScreen("BUST", False, dv, pv)
                    break
            
                state = "dealer"

            if pressA():
                if len(player) < 10:
                    player.append(newCard())
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
    
                        player.append(newCard())
                        pv = handValue(player)  # recalc ONCE after draw
                        if pv > 21:
                            resultScreen("BUST", False, dv, pv)
                            break

            if pressB():
                state = "dealer"

        if state == "dealer":
            if dv < 17 and len(dealer) < 10:
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
