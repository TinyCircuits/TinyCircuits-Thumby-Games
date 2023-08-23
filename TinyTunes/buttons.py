import thumby

def whichButton():
    if thumby.buttonU.justPressed():
        return 'U'
    if thumby.buttonD.justPressed():
        return 'D'
    if thumby.buttonL.justPressed():
        return 'L'
    if thumby.buttonR.justPressed():
        return 'R'
    if thumby.buttonA.justPressed():
        return 'A'
    if thumby.buttonB.justPressed():
        return 'B'
    return None
