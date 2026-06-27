import thumby

repeat = 0

def whichButton():
    global repeat
    if repeat >= 4:
        if thumby.buttonU.pressed():
            return 'u'
        elif thumby.buttonD.pressed():
            return 'd'
        elif thumby.buttonL.pressed():
            return 'l'
        elif thumby.buttonR.pressed():
            return 'r'
        elif thumby.buttonA.pressed():
            return 'a'
        elif thumby.buttonB.pressed():
            return 'b'
        else:
            repeat = 0
    elif repeat > 0:
        if thumby.inputPressed():
            repeat = repeat + 1
        else:
            repeat = 0
    else:
        if thumby.buttonU.justPressed():
            repeat = 1
            return 'U'
        if thumby.buttonD.justPressed():
            repeat = 1
            return 'D'
        if thumby.buttonL.justPressed():
            repeat = 1
            return 'L'
        if thumby.buttonR.justPressed():
            repeat = 1
            return 'R'
        if thumby.buttonA.justPressed():
            repeat = 1
            return 'A'
        if thumby.buttonB.justPressed():
            repeat = 1
            return 'B'
    return None
