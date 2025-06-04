from thumbyGraphics import display as d
import thumbyButton as b
from thumbyAudio import audio as a
from thumby import Sprite as S
from time import ticks_ms as t

# BITMAP: width: 9, height: 8
bitmap1 = bytearray([0,66,165,153,129,153,165,66,0])
timerSprite = S(9, 8, bitmap1, 0, 1)

# BITMAP: width: 9, height: 8
bitmap2 = bytearray([0,56,68,131,155,131,68,58,0])
stopwatchSprite = S(9, 8, bitmap2, 0, 1)

# BITMAP: width: 3, height: 5
bitmap3 = bytearray([4,14,31])
leftSprite = S(3, 5, bitmap3, 0, 3)

# BITMAP: width: 3, height: 5
bitmap4 = bytearray([31,14,4])
rightSprite = S(3, 5, bitmap4, 0, 3)

# BITMAP: width: 5, height: 3
bitmap5 = bytearray([4,6,7,6,4])
upSprite = S(5, 3, bitmap5, 0, 10)

# BITMAP: width: 5, height: 3
bitmap6 = bytearray([1,3,7,3,1])
downSprite = S(5, 3, bitmap6, 0, 20)

# BITMAP: width: 10, height: 7
bitmap7 = bytearray([28,62,67,117,67,62,28,0,54,54])
ASprite = S(10, 7, bitmap7, 1, 32)

# BITMAP: width: 10, height: 7
bitmap8 = bytearray([28,62,65,85,75,62,28,0,54,54])
BSprite = S(10, 7, bitmap8, 55, 32)

playSprite = S(3, 5, bitmap4, 13, 33)

# BITMAP: width: 5, height: 5
bitmap11 = bytearray([31,31,0,31,31])
pauseSprite = S(5, 5, bitmap11, 13, 33)

# BITMAP: width: 5, height: 5
bitmap12 = bytearray([14,25,21,19,14])
noneSprite = S(5, 5, bitmap12, 66, 33)

# BITMAP: width: 5, height: 5
bitmap13 = bytearray([31,31,31,31,31])
stopSprite = S(5, 5, bitmap13, 66, 33)

# BITMAP: width: 5, height: 5
bitmap14 = bytearray([0,31,7,2,0])
flagSprite = S(5, 5, bitmap14, 66, 33)

# BITMAP: width: 5, height: 5
bitmap15 = bytearray([14,17,23,25,14])
timeSprite = S(5, 5, bitmap15, 66, 33)

# BITMAP: width: 5, height: 5
bitmap16 = bytearray([2,30,19,30,2])
deleteSprite = S(5, 5, bitmap16, 66, 33)

# BITMAP: width: 5, height: 5
bitmap17 = bytearray([14,17,16,22,14])
resetSprite = S(5, 5, bitmap17, 66, 33)

# BITMAP: width: 5, height: 5
bitmap18 = bytearray([21,5,29,1,31])
scaleSprite = S(5, 5, bitmap18, 66, 33)

# BITMAP: width: 5, height: 5
bitmap19 = bytearray([8,16,8,4,2])
checkSprite = S(5, 5, bitmap19, 13, 33)

# BITMAP: width: 3, height: 5
bitmap20 = bytearray([18,23,18])
PMSprite = S(3, 5, bitmap20, 28, 33)

framecounter = 0
xScroll = xScrollTar = 0
yScroll = yScrollTar = 0

d.setFPS(60)

def printlist(listtoprint, selection, yOffset):
    d.drawText(listtoprint[selection-1] if selection > 0 else '', 7, 49-yOffset, 1)
    d.drawText('>', 0, 57-yOffset, 1)
    d.drawText(listtoprint[selection], 7, 57-yOffset, 1)
    d.drawText(listtoprint[selection+1] if selection < len(listtoprint) - 1 else '', 7, 65-yOffset, 1)

timerM = timerS = timerMS = 0
stopwatchM = stopwatchS = stopwatchMS = 0
isStopwatch = isTimer = 0
stopwatchData = ''
timerData = ''
startTimerData = [timerM, timerS, timerMS]
flags = []
flagSel = 0
lastStopwatchTime = 0
isSettingTimer = 0
timeScale = 0
timerSel = 0
timerDone = 0
flash = 0

while(1):
    framecounter += 1
    d.fill(flash)
    if isStopwatch:
        stopwatchTime = t()-stopwatchStart+lastStopwatchTime
        stopwatchMS = (stopwatchTime % 1000) // 10
        stopwatchS = (stopwatchTime // 1000) % 60
        stopwatchM = stopwatchTime // 60000
    if isTimer:
        timerTime = t()-timerStart
        timerRemaining = timerTotal-timerTime
        timerMS = (timerRemaining % 1000) // 10
        timerS = (timerRemaining // 1000) % 60
        timerM = timerRemaining // 60000
        if (timerM or timerS or timerMS) < 0:
            isTimer = 0
            timerDone = 1
    if timerDone:
        if framecounter % 30 == 0:
            flash = not flash
        a.play(1500 if flash else 500, 30)
        timerM, timerS, timerMS = 0, 0, 0
        yScrollTar, yScroll = 0, 0
        xScrollTar, xScroll = 72, 72
    if xScroll in range(0, 72):
        stopwatchData = f'{stopwatchM:02}:{stopwatchS:02}.{stopwatchMS:02}'
        d.drawText(stopwatchData, stopwatchSprite.x-19, 17-yScroll, not flash)
        d.drawFilledRectangle(0, 0, 72, 10, 0)
        if flags:
            if yScroll in range(0, 21):
                downSprite.y = stopwatchSprite.y + 4
                downSprite.x = stopwatchSprite.x - 5
                d.drawSprite(downSprite)
            elif yScroll in range(21, 41):
                upSprite.y = stopwatchSprite.y + 2
                upSprite.x = stopwatchSprite.x - 5
                d.drawSprite(upSprite)
            if yScroll:
                printlist(flags, flagSel, yScroll)
        d.drawSprite(stopwatchSprite)
        if not yScroll:
            rightSprite.x = stopwatchSprite.x + 9
            d.drawSprite(rightSprite)
    if xScroll in range(1, 73):
        d.drawSprite(timerSprite)
        if timerDone:
            d.drawRectangle(timerSprite.x, timerSprite.y-1, 9, 10, 0)
        leftSprite.x = timerSprite.x - 3
        if not isSettingTimer:
            if not timerDone:
                d.drawSprite(leftSprite)
        else:
            upSprite.y = 13
            downSprite.y = 25
            upSprite.x = 15 + 18*timerSel
            downSprite.x = 15 + 18*timerSel
            d.drawSprite(upSprite)
            d.drawSprite(downSprite)
            d.drawSprite(PMSprite)
            d.drawText('1'+'0'*timeScale, 33-2*timeScale, 32, 1)
        timerData = f'{timerM:02}:{timerS:02}.{timerMS:02}' if not isSettingTimer else f'{startTimerData[0]:02}:{startTimerData[1]:02}.{startTimerData[2]:02}'
        d.drawText(timerData, timerSprite.x-20-(6 if startTimerData[0]>99 else 0), 17, not flash)
    if (xScroll == 0 or xScroll == 72) and (yScroll == 0 or yScroll == 40):
        if not timerDone:
            d.drawSprite(ASprite)
            d.drawSprite(BSprite)
            if not xScroll:
                if not yScroll:
                    d.drawSprite(pauseSprite if isStopwatch else playSprite)
                    if not isStopwatch:
                        noneSprite.x = 66
                        d.drawSprite(stopSprite if stopwatchMS else noneSprite)
                    else:
                        d.drawSprite(flagSprite)
                else:
                    noneSprite.x = 13
                    d.drawSprite(noneSprite)
                    d.drawSprite(deleteSprite)
            else:
                if not isSettingTimer:
                    if timerM or timerS or timerMS:
                        d.drawSprite(pauseSprite if isTimer else playSprite)
                    else:
                        noneSprite.x = 13
                        d.drawSprite(noneSprite)
                    if timerMS or timerS or timerM:
                        if timerData != f'{startTimerData[0]:02}:{startTimerData[1]:02}.{startTimerData[2]:02}':
                            if isTimer:
                                noneSprite.x = 66
                                d.drawSprite(noneSprite)
                            else:
                                d.drawSprite(resetSprite)
                        else:
                            d.drawSprite(stopSprite)
                    else:
                        d.drawSprite(timeSprite)
                else:
                    d.drawSprite(checkSprite)
                    d.drawSprite(scaleSprite)
    timerSprite.x = 72-xScroll+32
    stopwatchSprite.x = -xScroll+32
    d.update()
    if b.buttonL.justPressed():
        if timerDone:
            flash = 0
            timerDone = 0
        else:
            if not yScroll:
                if not isSettingTimer:
                    xScrollTar = max(0, xScrollTar-72)
                else:
                    timerSel = max(0, timerSel-1)
    elif b.buttonR.justPressed():
        if not yScroll:
            if not isSettingTimer:
                xScrollTar = min(72, xScrollTar+72)
            else:
                timerSel = min(2, timerSel+1)
    if b.buttonU.justPressed():
        if timerDone:
            flash = 0
            timerDone = 0
        else:
            if not xScroll:
                if flagSel == 0:
                    yScrollTar = max(0, yScrollTar-40)
                else:
                    flagSel = max(0, flagSel-1)
            else:
                if isSettingTimer:
                    startTimerData[timerSel] += 10 if timeScale else 1
                    if startTimerData[0] > 119:
                        startTimerData[0] = 0
                    if startTimerData[1] > 59:
                        startTimerData[1] = 0
                    if startTimerData[2] > 99:
                        startTimerData[2] = 0
    elif b.buttonD.justPressed():
        if timerDone:
            flash = 0
            timerDone = 0
        else:
            if not xScroll:
                if flags:
                    if not yScroll:
                        yScrollTar = min(40, yScrollTar+40)
                    else:
                        flagSel = min(len(flags)-1, flagSel+1)
            else:
                if isSettingTimer:
                    startTimerData[timerSel] -= 10 if timeScale else 1
                    if startTimerData[0] < 0:
                        startTimerData[0] = 119
                    if startTimerData[1] < 0:
                        startTimerData[1] = 59
                    if startTimerData[2] < 0:
                        startTimerData[2] = 99
    if b.buttonA.justPressed():
        if timerDone:
            flash = 0
            timerDone = 0
        else:
            if not xScroll:
                if not yScroll:
                    if not isStopwatch:
                        if stopwatchMS or stopwatchS or stopwatchM: lastStopwatchTime = stopwatchTime
                        stopwatchStart = t()
                    isStopwatch = not isStopwatch
            else:
                if isSettingTimer:
                    timerM, timerS, timerMS = startTimerData
                    isSettingTimer = 0
                elif timerM or timerS or timerMS:
                    timerStart = t()
                    timerTotal = (timerM*60+timerS)*1000+timerMS
                    isTimer = not isTimer
    if b.buttonB.justPressed():
        if timerDone:
            flash = 0
            timerDone = 0
        else:
            if not xScroll:
                if not yScroll:
                    if not isStopwatch and stopwatchMS:
                        stopwatchM = stopwatchS = stopwatchMS = 0
                        lastStopwatchTime = 0
                        flags = []
                    elif isStopwatch:
                        flags.insert(0, stopwatchData)
                elif yScroll == 40:
                    flags.pop(flagSel)
                    if not flags:
                        yScrollTar = 0
                        yScroll = 30
                    flagSel = min(0, len(flags))
            elif xScroll == 72:
                if not isSettingTimer:
                    if timerM or timerS or timerMS:
                        if not isTimer:
                            if timerData != f'{startTimerData[0]:02}:{startTimerData[1]:02}.{startTimerData[2]:02}':
                                timerM, timerS, timerMS = startTimerData
                                isTimer = 0
                            else:
                                timerM, timerS, timerMS = 0, 0, 0
                                startTimerData = [timerM, timerS, timerMS]
                    else:
                        isSettingTimer = 1
                else:
                    timeScale = not timeScale
    if xScrollTar < xScroll:
        xScroll -= 4
    elif xScrollTar > xScroll:
        xScroll += 4
    if yScrollTar < yScroll:
        yScroll -= 2
    elif yScrollTar > yScroll:
        yScroll += 2
