import thumbyButton as b
from time import ticks_ms, ticks_diff

REPEAT_TIMEOUT_MS = 750
REPEAT_THRESHOLD_MS = 500
REPEAT_MIN_GAP_MS = 160
NORMAL = 'normal'
PRESSED = 'pressed'
REPEATING = 'repeating'

keyMode = NORMAL
baseTicks = ticks_ms()

def actionJustPressed():
    return b.actionJustPressed()

def resetTimeCounter():
    global baseTicks
    baseTicks = ticks_ms()

def normalPress():
    if b.buttonU.justPressed(): return 'U'
    if b.buttonD.justPressed(): return 'D'
    if b.buttonL.justPressed(): return 'L'
    if b.buttonR.justPressed(): return 'R'
    if b.buttonA.justPressed(): return 'A'
    if b.buttonB.justPressed(): return 'B'
    return None

def clear():
    b.buttonU.justPressed()
    b.buttonD.justPressed()
    b.buttonL.justPressed()
    b.buttonR.justPressed()
    b.buttonA.justPressed()
    b.buttonB.justPressed()

def repeatPress( abOk ):
    if b.buttonU.pressed(): return 'u'
    if b.buttonD.pressed(): return 'd'
    if b.buttonL.pressed(): return 'l'
    if b.buttonR.pressed(): return 'r'
    if abOk and b.buttonA.pressed(): return 'a'
    if abOk and b.buttonB.pressed(): return 'b'
    return None

def which( abOk = True ):
    global keyMode
    timePassed = ticks_diff( ticks_ms(), baseTicks )
    result = None
    if keyMode == REPEATING:
        if timePassed > REPEAT_TIMEOUT_MS:
            keyMode = NORMAL
            resetTimeCounter()
            result = normalPress()
        elif timePassed > REPEAT_MIN_GAP_MS:
            resetTimeCounter()
            result = repeatPress( abOk )
            if not result:
                keyMode = NORMAL
                resetTimeCounter()
        else:
            result = None
    elif keyMode == PRESSED:
        if timePassed > REPEAT_THRESHOLD_MS:
            keyMode = REPEATING
            result = repeatPress( abOk )
            if not result:
                keyMode = NORMAL
                resetTimeCounter()
    else:
        resetTimeCounter()
        result = normalPress()
        if result:
            keyMode = PRESSED
    return result
