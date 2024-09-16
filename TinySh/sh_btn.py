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
    result = None
    if   b.buttonU.justPressed(): result = 'U'
    elif b.buttonD.justPressed(): result = 'D'
    elif b.buttonL.justPressed(): result = 'L'
    elif b.buttonR.justPressed(): result = 'R'
    elif b.buttonA.justPressed(): result = 'A'
    elif b.buttonB.justPressed(): result = 'B'
    clear()
    return result

def clear():
    b.buttonU.justPressed()
    b.buttonD.justPressed()
    b.buttonL.justPressed()
    b.buttonR.justPressed()
    b.buttonA.justPressed()
    b.buttonB.justPressed()

def repeatPress( abOk ):
    result = None
    if   b.buttonU.pressed(): result = 'u'
    elif b.buttonD.pressed(): result = 'd'
    elif b.buttonL.pressed(): result = 'l'
    elif b.buttonR.pressed(): result = 'r'
    elif abOk and b.buttonA.pressed(): result = 'a'
    elif abOk and b.buttonB.pressed(): result = 'b'
    return result

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
            resetTimeCounter()
            clear()
            result = repeatPress( abOk )
            if not result:
                keyMode = NORMAL
    else:
        resetTimeCounter()
        result = normalPress()
        if result:
            keyMode = PRESSED
    return result
