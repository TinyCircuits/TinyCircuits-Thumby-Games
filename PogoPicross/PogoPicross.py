#PogoPicross ver 1.0
#An attempt at a Picross Game for the Thumby by Pogostix in 2025
#ALWAYS OPEN TO CONSTRUCTIVE CRITIQUE! I'm @Pogostix in the Thumby Discord
#Questions or Comments are also welcome.
#Creative Commons Zero. Feel free to edit, just give me credit.

#FAQ
    #1. Can I make my own levels?
        #YES YOU CAN! I will make a guide in the future. For now, 
        #there's a blankLevel.json in /Games/PogoPicross/Levels 
        #if you can figure it out yourself.
    #2. Can I edit/adapt this?
        #YES, but be aware I'm 100% self taught and my code can be 
        #A Little Strange(tm) and Not Very Professional(tm)
        #Just give me credit for the original and keep the CC Zero
    #3. Your picross tutorial sucks.
        #I am aware, but if I wrote a bigger one, it would be like. 10+
        #screens of text to A through. If you want a better one: 
        #https://www.thonky.com/nonograms/
    #4. What is the 3x3 font you used for the grid numbers?
        #numbers3x3.bin is included in the /Games/PogoPicross file. 
        #Keep in mind it's literally just numbers 0-9
    #5. Can I play this on the code.thumby.us Emulator?
        #Yes, technically, but I DON'T RECOMMEND IT.
        #It's very laggy and you have to open all the files and designate 
        #them for emulation... and there's bugs. (See KNOWN BUGS below)
        #But IF YOU INSIST: the bare minimum you need open in the editor to get this to work is
            #/Games/PogoPicross/PogoPicross.py (tick both grey and red emulation boxes)
            #/Games/PogoPicross/numbers3x3.bin (tick grey emulation box)
            #/Saves/PogoPicross/persistent.json (tick grey emulation box). You will have to update the number in here to match the number of the level you want to play.
            #/Games/PogoPicross/Levels/level<number>.json (tick grey emulation box). There are 48 levels currently, Make sure the number matches the number in persistent.json.

#TO DO:
    #Make a guide to making/adding your own levels if you want.
    #Put it on GitHub and Itch.io
    #Go to bed before 3 AM for once

#KNOWN BUGS:
    #Grid Numbers draw all jumbled sometimes.
        #This appears to be limited to the emulator, something to do
        #with custom font files not playing happy with it. Never had
        #it happen on hardware. Not sure how to fix it.
        #Restart emulator and try again.
    #Pressing B to Check Solution sometimes does not work.
        #Won't print error count or beep, just... does nothing.
        #This one's probably my fault ._. If you know how to fix it,
        #please let me know, because I don't.

#Ok that's enough ramble, messy code below here.
#------------------------------------------------------------
import thumby
import time
import sys
import json
import gc
gc.enable() #not sure this will help with the emu lag but we will try

#yes I'm using the saveData as an external global variable here. It controls which level is loaded.
    #... originally it was because the level loading was a different
    #module but this wound up not working very well. I could probably
    #use a normal global variable now but... if it ain't broke...
        #I tried to 'fix' it and lol no that went badly, back to this nonsense.
        #Program doesn't work: Pogo doesn't know why.
        #Program works: Pogo doesn't know why.
sys.path.append('/Games/PogoPicross')
if (thumby.saveData.hasItem('temp')) == False:
    thumby.saveData.setName('PogoPicross')
    thumby.saveData.setItem('temp', 0)
    thumby.saveData.save()
if (thumby.saveData.hasItem('temp')) == True:
    temp = (thumby.saveData.getItem('temp'))
    print(temp)

#making some shortcuts for myself re: setting the font
def fontSmall():
    thumby.display.setFont("/lib/font3x5.bin", 3, 5, 1)
def fontMed():
    thumby.display.setFont("/lib/font5x7.bin", 5, 7, 1)
def fontBig():
    thumby.display.setFont("/lib/font8x8.bin", 8, 8, 1)
def fontCustom(): #NOTE: This font file only has numbers. If you need a good 3x3 font, ask @Auri in the discord :)
    thumby.display.setFont("/Games/PogoPicross/numbers3x3.bin", 3, 3, 1)

#This table keeps track of if a square is filled or not
global row0
global row1
global row2
global row3
global row4
row0 = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]# 0
row1 = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]# 1
row2 = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]# 2
row3 = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]# 3
row4 = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]# 4
#1 = Filled, 0 = Empty, compared to level data to check solution

#This one keeps track of what sprite is drawn in a square
global row0Sprs
global row1Sprs
global row2Sprs
global row3Sprs
global row4Sprs
row0Sprs = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
row1Sprs = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
row2Sprs = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
row3Sprs = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
row4Sprs = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
#1 = Filled, 2 = X'd, 0 = Empty, use to draw correct sprite in square

#sprites
#Filled Square
# BITMAP: width: 3, height: 3
fillMap = bytearray([7,7,7])
fillSpr = thumby.Sprite(3, 3, fillMap, key = 0)

#X'd Square
# BITMAP: width: 3, height: 3
xMap = bytearray([4,2,1])
xSpr = thumby.Sprite(3, 3, xMap, key = -1)

#Blank out square (the "oops" function, if you will)
# BITMAP: width: 3, height: 3
oopsMap = bytearray([0,0,0])
oopsSpr = thumby.Sprite(3, 3, oopsMap, key = 1)

# Puzzle cursor
# BITMAP: width: 5, height: 5
cursorMap = bytearray([4,14,31,14,4])
cursorSpr = thumby.Sprite(5, 5, cursorMap, key = 1)

#Menu Pointer (different copies for different menus... tried using the same one for all, Weird Stuff(tm) happened)
# BITMAP: width: 5, height: 5
pointerMap = bytearray([31,14,4,0,0])
pointerSpr = thumby.Sprite(5, 5, pointerMap, key = 0)
pointerSprMirror = thumby.Sprite(5, 5, pointerMap, key = -1, mirrorX = 1)
pointerSpr2 = thumby.Sprite(5, 5, pointerMap, key = 0)
pointerSpr3 = thumby.Sprite(5, 5, pointerMap, key = 0)

#Title Screen (maybe one day I'll make an actual font file...)
# BITMAP: width: 71, height: 26
titleMap = bytearray([0,0,0,0,0,0,0,240,16,16,16,255,241,241,241,255,0,0,254,1,1,237,45,33,18,12,0,124,130,1,125,125,1,130,124,0,124,130,1,125,109,9,138,116,0,124,130,1,125,125,1,130,124,0,0,255,241,241,241,255,16,16,16,240,0,0,0,0,0,0,0,
           0,0,0,0,0,240,8,9,105,105,9,145,97,1,17,233,8,8,232,17,1,224,16,8,232,40,72,80,32,1,241,9,9,104,104,8,144,96,1,225,17,9,232,232,8,16,224,1,97,145,9,104,104,72,208,33,1,97,145,9,105,105,73,209,32,0,0,0,0,0,0,
           0,224,32,32,32,231,232,232,231,225,33,32,32,224,228,235,232,232,43,36,32,227,228,232,235,234,41,37,34,224,231,232,232,230,36,41,42,228,224,227,228,232,43,43,40,228,227,224,226,229,41,43,43,232,228,227,224,226,37,41,43,235,232,228,227,224,32,32,32,224,0,
           0,3,2,2,2,3,3,3,3,3,2,2,2,3,3,3,3,3,2,2,2,3,3,3,3,3,2,2,2,3,3,3,3,3,2,2,2,3,3,3,3,3,2,2,2,3,3,3,3,3,2,2,2,3,3,3,3,3,2,2,2,3,3,3,3,3,2,2,2,3,0])
titleSpr = thumby.Sprite(71, 26, titleMap, key = -1)

#Menu decorations
# 3 squares
# BITMAP: width: 13, height: 5
decoMap1 = bytearray([31,17,17,17,31,31,31,31,31,17,17,17,31])
decoSpr1 = thumby.Sprite(13, 5, decoMap1, key = -1)
decoSpr2 = thumby.Sprite(13, 5, decoMap1, key = -1)

#2 squares
# BITMAP: width: 9, height: 5
decoMap2 = bytearray([31,17,17,17,31,31,31,31,31])
decoSpr3 = thumby.Sprite(9, 5, decoMap2, key = -1)
decoSpr4 = thumby.Sprite(9, 5, decoMap2, key = -1, mirrorX = 1)

#sound on or off
# BITMAP: width: 12, height: 12
soundOnMap = bytearray([0,0,240,240,0,248,252,254,0,40,36,32,
           0,0,0,0,0,1,3,7,0,1,2,0])
soundOnSpr = thumby.Sprite(12, 12, soundOnMap, 18, 9)
# BITMAP: width: 12, height: 12
soundOffMap = bytearray([2,7,110,156,248,240,244,250,156,14,7,2,
           4,14,7,3,1,0,2,5,3,7,14,4])
soundOffSpr = thumby.Sprite(12, 12, soundOffMap, 42, 9)

#Audio... this was SUPPOSED to all be one function but that didn't work right. Also doing it this way lets me make exceptions.
def buttonAsound():
    thumby.audio.play(622, 100)

def buttonBsound():
    thumby.audio.play(523, 100)

def buttonMoveSound():
    thumby.audio.play(261, 100)

def happyNoise():
    thumby.audio.setEnabled(True)
    thumby.audio.play(1661, 100)
    time.sleep(0.2)
    thumby.audio.play(1661, 100)
    time.sleep(0.1)
    thumby.audio.play(1046, 100)
    time.sleep(0.1)
    thumby.audio.play(2093, 100)
    time.sleep(0.2)
    thumby.audio.play(1661, 100)
    time.sleep(0.2)
    thumby.audio.play(2093, 100)

def errorNoise():
    thumby.audio.play(783, 100)
    time.sleep(0.1)
    thumby.audio.play(739, 100)
    time.sleep(0.1)
    thumby.audio.play(698, 100)

#Ok actual program script starts here

#Sound On/Off Menu
def soundOnOff():
    waiting2 = True
    pointerSpr3.x = 16
    pointerSpr3.y = 22
    moveNum = 21
    while(waiting2):
        thumby.display.fill(0)
        thumby.display.setFPS(60)
        fontMed()
        decoSpr1.x = 6
        decoSpr1.y = 1
        decoSpr2.x = 52
        decoSpr2.y = 1
        thumby.display.drawSprite(decoSpr1)
        thumby.display.drawSprite(decoSpr2)
        thumby.display.drawText("SOUND", 20, 0, 1)
        thumby.display.drawSprite(soundOnSpr)
        thumby.display.drawSprite(soundOffSpr)
        fontSmall()
        thumby.display.drawText("ON", 21, 22, 1)
        thumby.display.drawText("OFF", 42, 22, 1)
        thumby.display.drawText("B:Back to Menu", 8, 35, 1)
        thumby.display.drawSprite(pointerSpr3)
        thumby.display.update()
        if thumby.buttonR.justPressed():
            buttonMoveSound()
            pointerSpr3.x += moveNum
        if thumby.buttonL.justPressed():
            buttonMoveSound()
            pointerSpr3.x -= moveNum
        if pointerSpr3.x < 16:
            pointerSpr3.x = 16
        if pointerSpr3.x > 37:
            pointerSpr3.x = 37
        if thumby.buttonB.justPressed():
            buttonBsound()
            waiting2 = False
            break
        if thumby.buttonA.justPressed():
            if pointerSpr3.x == 16:
                thumby.audio.setEnabled(1)
                buttonAsound()
            if pointerSpr3.x == 37:
                thumby.audio.setEnabled(0)

#Loading Level Data json
def loadLevel():
    import json
    temp = thumby.saveData.getItem('temp')
    levelString = "/Games/PogoPicross/Levels/level"+str(temp)+".json"
    x = open(str(levelString))
    levelData = json.load(x)
    global levelName
    global levelSize
    levelName = str(levelData["levelName"])
    levelSize = int(levelData["levelSize"])
    global levelSprMap 
    levelSprMap = bytearray (levelData["levelSprite"])
    global lvlRow0
    global lvlRow1
    global lvlRow2
    global lvlRow3
    global lvlRow4
    lvlRow0 = (levelData["lvlRow0"])
    lvlRow1 = (levelData["lvlRow1"])
    lvlRow2 = (levelData["lvlRow2"])
    lvlRow3 = (levelData["lvlRow3"])
    lvlRow4 = (levelData["lvlRow4"])
    print(lvlRow0)
    print(lvlRow1)
    print(lvlRow2)
    print(lvlRow3)
    print(lvlRow4)
    print("Loaded ", levelName)
    global rowNum0
    global rowNum1
    global rowNum2
    global rowNum3
    global rowNum4
    rowNum0 = (levelData["rowNum0"])
    rowNum1 = (levelData["rowNum1"])
    rowNum2 = (levelData["rowNum2"])
    rowNum3 = (levelData["rowNum3"])
    rowNum4 = (levelData["rowNum4"])
    global colNum0
    global colNum1
    global colNum2
    colNum0 = (levelData["colNum0"])
    colNum1 = (levelData["colNum1"])
    colNum2 = (levelData["colNum3"])
    x.close()

#Drawing puzzle grids to screen
def drawGrid(): #Due to size limits, only 5 rows will fit on screen.
    if int(levelSize) == 5:
        thumby.display.drawRectangle(0, 0, 21, 21, 1)#rectangle
        thumby.display.drawLine(4, 0, 4, 20, 1)#vertical
        thumby.display.drawLine(8, 0, 8, 20, 1)
        thumby.display.drawLine(12, 0, 12, 20, 1)
        thumby.display.drawLine(16, 0, 16, 20, 1)
        thumby.display.drawLine(0, 4, 20, 4, 1)#Horizontal
        thumby.display.drawLine(0, 8, 20, 8, 1)
        thumby.display.drawLine(0, 12, 20, 12, 1)
        thumby.display.drawLine(0, 16, 20, 16, 1)
        thumby.display.update()
    if int(levelSize) == 6:
        thumby.display.drawRectangle(0, 0, 25, 21, 1)#rectangle
        thumby.display.drawLine(4, 0, 4, 20, 1)#vertical
        thumby.display.drawLine(8, 0, 8, 20, 1)
        thumby.display.drawLine(12, 0, 12, 20, 1)
        thumby.display.drawLine(16, 0, 16, 20, 1)
        thumby.display.drawLine(20, 0, 20, 20, 1)
        thumby.display.drawLine(0, 4, 24, 4, 1)#Horizontal
        thumby.display.drawLine(0, 8, 24, 8, 1)
        thumby.display.drawLine(0, 12, 24, 12, 1)
        thumby.display.drawLine(0, 16, 24, 16, 1)
        thumby.display.update()
    if int(levelSize) == 7:
        thumby.display.drawRectangle(0, 0, 29, 21, 1)#rectangle
        thumby.display.drawLine(4, 0, 4, 20, 1)#vertical
        thumby.display.drawLine(8, 0, 8, 20, 1)
        thumby.display.drawLine(12, 0, 12, 20, 1)
        thumby.display.drawLine(16, 0, 16, 20, 1)
        thumby.display.drawLine(20, 0, 20, 20, 1)
        thumby.display.drawLine(24, 0, 24, 20, 1)
        thumby.display.drawLine(0, 4, 28, 4, 1)#Horizontal
        thumby.display.drawLine(0, 8, 28, 8, 1)
        thumby.display.drawLine(0, 12, 28, 12, 1)
        thumby.display.drawLine(0, 16, 28, 16, 1)
        thumby.display.update()
    if int(levelSize) == 8:
        thumby.display.drawRectangle(0, 0, 33, 21, 1)#rectangle
        thumby.display.drawLine(4, 0, 4, 20, 1)#vertical
        thumby.display.drawLine(8, 0, 8, 20, 1)
        thumby.display.drawLine(12, 0, 12, 20, 1)
        thumby.display.drawLine(16, 0, 16, 20, 1)
        thumby.display.drawLine(20, 0, 20, 20, 1)
        thumby.display.drawLine(24, 0, 24, 20, 1)
        thumby.display.drawLine(28, 0, 28, 20, 1)
        thumby.display.drawLine(0, 4, 32, 4, 1)#Horizontal
        thumby.display.drawLine(0, 8, 32, 8, 1)
        thumby.display.drawLine(0, 12, 32, 12, 1)
        thumby.display.drawLine(0, 16, 32, 16, 1)
        thumby.display.update()
    if int(levelSize) == 9:
        thumby.display.drawRectangle(0, 0, 37, 21, 1)#rectangle
        thumby.display.drawLine(4, 0, 4, 20, 1)#vertical
        thumby.display.drawLine(8, 0, 8, 20, 1)
        thumby.display.drawLine(12, 0, 12, 20, 1)
        thumby.display.drawLine(16, 0, 16, 20, 1)
        thumby.display.drawLine(20, 0, 20, 20, 1)
        thumby.display.drawLine(24, 0, 24, 20, 1)
        thumby.display.drawLine(28, 0, 28, 20, 1)
        thumby.display.drawLine(32, 0, 32, 20, 1)
        thumby.display.drawLine(0, 4, 36, 4, 1)#Horizontal
        thumby.display.drawLine(0, 8, 36, 8, 1)
        thumby.display.drawLine(0, 12, 36, 12, 1)
        thumby.display.drawLine(0, 16, 36, 16, 1)
        thumby.display.update()
    if int(levelSize) == 10:
        thumby.display.drawRectangle(0, 0, 41, 21, 1)#rectangle
        thumby.display.drawLine(4, 0, 4, 20, 1)#vertical
        thumby.display.drawLine(8, 0, 8, 20, 1)
        thumby.display.drawLine(12, 0, 12, 20, 1)
        thumby.display.drawLine(16, 0, 16, 20, 1)
        thumby.display.drawLine(20, 0, 20, 20, 1)
        thumby.display.drawLine(24, 0, 24, 20, 1)
        thumby.display.drawLine(28, 0, 28, 20, 1)
        thumby.display.drawLine(32, 0, 32, 20, 1)
        thumby.display.drawLine(36, 0, 36, 20, 1)
        thumby.display.drawLine(0, 4, 40, 4, 1)#Horizontal
        thumby.display.drawLine(0, 8, 40, 8, 1)
        thumby.display.drawLine(0, 12, 40, 12, 1)
        thumby.display.drawLine(0, 16, 40, 16, 1)
        thumby.display.update()

#Printing the Row and Column numbers to screen
def printRowNumbers():
    if int(levelSize) == 5:
        offset = 22
    if int(levelSize) == 6:
        offset = 26
    if int(levelSize) == 7:
        offset = 30
    if int(levelSize) == 8:
        offset = 34
    if int(levelSize) == 9:
        offset = 38
    if int(levelSize) == 10:
        offset = 42
    fontCustom()
    thumby.display.drawText(str(rowNum0), offset, 0, 1)
    thumby.display.drawText(str(rowNum1), offset, 4, 1)
    thumby.display.drawText(str(rowNum2), offset, 8, 1)
    thumby.display.drawText(str(rowNum3), offset, 12, 1)
    thumby.display.drawText(str(rowNum4), offset, 16, 1)
    thumby.display.update()
def printColNumbers():
    fontCustom()
    thumby.display.drawText(str(colNum0), 1, 22, 1)
    thumby.display.drawText(str(colNum1), 1, 27, 1)
    thumby.display.drawText(str(colNum2), 1, 32, 1)
    thumby.display.update()

#Logic for the pointer in levelMenu()
def levelPointerMovement():
    if thumby.buttonU.justPressed():
        buttonMoveSound()
        pointerSpr.y -= moveNumY
    if thumby.buttonD.justPressed():
        buttonMoveSound()
        pointerSpr.y += moveNumY
    if thumby.buttonR.justPressed():
        buttonMoveSound()
        if pointerSpr.y < 33: 
            moveNumX = 12
            pointerSpr.x += moveNumX
        if pointerSpr.y == 33:
            moveNumX = 24
            pointerSpr.x += moveNumX
    if thumby.buttonL.justPressed():
        buttonMoveSound()
        if pointerSpr.y < 33: 
            moveNumX = 12
            pointerSpr.x -= moveNumX
        if pointerSpr.y == 33:
            moveNumX = 24
            pointerSpr.x -= moveNumX
    if pointerSpr.y < 33:
        if pointerSpr.x < 1:
            pointerSpr.x = 61
        if pointerSpr.x > 61:
            pointerSpr.x = 1
    if pointerSpr.y == 33:
        if pointerSpr.x < 1:
            pointerSpr.x = 25
        if pointerSpr.x > 25:
            pointerSpr.x = 1
    if pointerSpr.y < 9:
        pointerSpr.y = 33
    if pointerSpr.y >33:
        pointerSpr.y = 9
    thumby.display.drawSprite(pointerSpr)
    thumby.display.update()

#Cursor Movement for puzzleTime()
thumby.display.setFPS(60)
cursorSpr.x = 0
cursorSpr.y = 0
moveNum = 4
frameCount = 1
sprFrame = frameCount // 12
def cursorMovement():#movement
    thumby.display.setFPS(60)
    if thumby.buttonU.justPressed():
        buttonMoveSound()
        cursorSpr.y -= moveNum
        drawGrid()
    if thumby.buttonD.justPressed():
        buttonMoveSound()
        cursorSpr.y += moveNum
        drawGrid()
    if thumby.buttonL.justPressed():
        buttonMoveSound()
        cursorSpr.x -= moveNum
        drawGrid()
    if thumby.buttonR.justPressed():
        buttonMoveSound()
        cursorSpr.x += moveNum
        drawGrid()
    if cursorSpr.y < 0: #bounding y
        cursorSpr.y = 16
    if cursorSpr.y > 16:
        cursorSpr.y = 0
    if levelSize == 5: #bounding x
        if cursorSpr.x < 0: 
            cursorSpr.x = 16
        if cursorSpr.x > 16:
            cursorSpr.x = 0
    if levelSize == 6:
        if cursorSpr.x < 0:
            cursorSpr.x = 20
        if cursorSpr.x > 20:
            cursorSpr.x = 0
    if levelSize == 7:
        if cursorSpr.x < 0: 
            cursorSpr.x = 24
        if cursorSpr.x > 24:
            cursorSpr.x = 0
    if levelSize == 8:
        if cursorSpr.x < 0: 
            cursorSpr.x = 28
        if cursorSpr.x > 28:
            cursorSpr.x = 0
    if levelSize == 9:
        if cursorSpr.x < 0: 
            cursorSpr.x = 32
        if cursorSpr.x > 32:
            cursorSpr.x = 0
    if levelSize == 10:
        if cursorSpr.x < 0: 
            cursorSpr.x = 36
        if cursorSpr.x > 36:
            cursorSpr.x = 0
    cursorSpr.setFrame(sprFrame)
    thumby.display.drawSprite(cursorSpr)
    thumby.display.update()

#What goes on in squares, writing it to the tables at the top, etc.
def cellLogic():
    rowNum = int(cursorSpr.y) / 4
    columnNum = int(cursorSpr.x) / 4
    fillSpr.x = int(cursorSpr.x) + 1
    fillSpr.y = int(cursorSpr.y) + 1
    xSpr.x = int(cursorSpr.x) + 1
    xSpr.y = int(cursorSpr.y) + 1 
    oopsSpr.x = int(cursorSpr.x) + 1
    oopsSpr.y = int(cursorSpr.y) + 1
    if rowNum == 0:
        if row0Sprs[int(columnNum)] == 0: #if a cell is empty
            if thumby.buttonA.justPressed():
                buttonAsound()
                row0Sprs[int(columnNum)] = 1
                row0[int(columnNum)] = 1
                thumby.display.drawSprite(fillSpr)
                drawGrid()
                thumby.display.update()
        if row0Sprs[int(columnNum)] == 1: #if a cell is filled
            if thumby.buttonA.justPressed():
                buttonAsound()
                row0Sprs[int(columnNum)] = 2
                row0[int(columnNum)] = 0
                thumby.display.drawSprite(xSpr)
                drawGrid()
                thumby.display.update()
        if row0Sprs[int(columnNum)] == 2: #if a cell is x'd
            if thumby.buttonA.justPressed():
                buttonAsound()
                row0Sprs[int(columnNum)] = 0
                thumby.display.drawSprite(oopsSpr)
                drawGrid()
                thumby.display.update()
    if rowNum == 1:
        if row1Sprs[int(columnNum)] == 0: #if a cell is empty
            if thumby.buttonA.justPressed():
                buttonAsound()
                row1Sprs[int(columnNum)] = 1
                row1[int(columnNum)] = 1
                thumby.display.drawSprite(fillSpr)
                drawGrid()
                thumby.display.update()
        if row1Sprs[int(columnNum)] == 1: #if a cell is filled
            if thumby.buttonA.justPressed():
                buttonAsound()
                row1Sprs[int(columnNum)] = 2
                row1[int(columnNum)] = 0
                thumby.display.drawSprite(xSpr)
                drawGrid()
                thumby.display.update()
        if row1Sprs[int(columnNum)] == 2: #if a cell is x'd
            if thumby.buttonA.justPressed():
                buttonAsound()
                row1Sprs[int(columnNum)] = 0
                thumby.display.drawSprite(oopsSpr)
                drawGrid()
                thumby.display.update()
    if rowNum == 2:
        if row2Sprs[int(columnNum)] == 0: #if a cell is empty
            if thumby.buttonA.justPressed():
                buttonAsound()
                row2Sprs[int(columnNum)] = 1
                row2[int(columnNum)] = 1
                thumby.display.drawSprite(fillSpr)
                drawGrid()
                thumby.display.update()
        if row2Sprs[int(columnNum)] == 1: #if a cell is filled
            if thumby.buttonA.justPressed():
                buttonAsound()
                row2Sprs[int(columnNum)] = 2
                row2[int(columnNum)] = 0
                thumby.display.drawSprite(xSpr)
                drawGrid()
                thumby.display.update()
        if row2Sprs[int(columnNum)] == 2: #if a cell is x'd
            if thumby.buttonA.justPressed():
                buttonAsound()
                row2Sprs[int(columnNum)] = 0
                thumby.display.drawSprite(oopsSpr)
                drawGrid()
                thumby.display.update()
    if rowNum == 3:
        if row3Sprs[int(columnNum)] == 0: #if a cell is empty
            if thumby.buttonA.justPressed():
                buttonAsound()
                row3Sprs[int(columnNum)] = 1
                row3[int(columnNum)] = 1
                thumby.display.drawSprite(fillSpr)
                drawGrid()
                thumby.display.update()
        if row3Sprs[int(columnNum)] == 1: #if a cell is filled
            if thumby.buttonA.justPressed():
                buttonAsound()
                row3Sprs[int(columnNum)] = 2
                row3[int(columnNum)] = 0
                thumby.display.drawSprite(xSpr)
                drawGrid()
                thumby.display.update()
        if row3Sprs[int(columnNum)] == 2: #if a cell is x'd
            if thumby.buttonA.justPressed():
                buttonAsound()
                row3Sprs[int(columnNum)] = 0
                thumby.display.drawSprite(oopsSpr)
                drawGrid()
                thumby.display.update()
    if rowNum == 4:
        if row4Sprs[int(columnNum)] == 0: #if a cell is empty
            if thumby.buttonA.justPressed():
                buttonAsound()
                row4Sprs[int(columnNum)] = 1
                row4[int(columnNum)] = 1
                thumby.display.drawSprite(fillSpr)
                drawGrid()
                thumby.display.update()
        if row4Sprs[int(columnNum)] == 1: #if a cell is filled
            if thumby.buttonA.justPressed():
                buttonAsound()
                row4Sprs[int(columnNum)] = 2
                row4[int(columnNum)] = 0
                thumby.display.drawSprite(xSpr)
                drawGrid()
                thumby.display.update()
        if row4Sprs[int(columnNum)] == 2: #if a cell is x'd
            if thumby.buttonA.justPressed():
                buttonAsound()
                row4Sprs[int(columnNum)] = 0
                thumby.display.drawSprite(oopsSpr)
                drawGrid()
                thumby.display.update()

#YOU'RE WINNER! 
def victory():
        thumby.display.fill(0)
        thumby.display.setFPS(60)
        fontMed()
        thumby.display.drawText("YOU DID IT!", 5, 0, 1)
        happyNoise()
        fontSmall()
        thumby.display.drawText(str(levelName), 0, 9, 1 )
        if int(levelSize) == 5:
            levelSpr = thumby.Sprite(5, 5, levelSprMap, 33, 17, 0)
            thumby.display.drawSprite(levelSpr)
            thumby.display.update()
        if int(levelSize) == 6:
            levelSpr = thumby.Sprite(6, 5, levelSprMap, 33, 17, 0)
            thumby.display.drawSprite(levelSpr)
            thumby.display.update
        if int(levelSize) == 7:
            levelSpr = thumby.Sprite(7, 5, levelSprMap, 32, 17, 0)
            thumby.display.drawSprite(levelSpr)
            thumby.display.update
        if int(levelSize) == 8:
            levelSpr = thumby.Sprite(8, 5, levelSprMap, 32, 17, 0)
            thumby.display.drawSprite(levelSpr)
            thumby.display.update
        if int(levelSize) == 9:
            levelSpr = thumby.Sprite(9, 5, levelSprMap, 31, 17, 0)
            thumby.display.drawSprite(levelSpr)
            thumby.display.update
        if int(levelSize) == 10:
            levelSpr = thumby.Sprite(10, 5, levelSprMap, 31, 17, 0)
            thumby.display.drawSprite(levelSpr)
            thumby.display.update
        victoryScreen = True
        while(victoryScreen):
            thumby.display.drawText("A: Next",24, 35, 1)
            thumby.display.update()
            if thumby.buttonA.justPressed():
                buttonAsound()
                thumby.saveData.setItem('temp', 0)
                victoryScreen = False
                gameRunning = False
                waiting = False
                break

#Compare player input to level data
def checkSolution():
    print(row0)
    print(row1)
    print(row2)
    print(row3)
    print(row4)
    global errorCount
    errorCount = 0
    if row0[0] == lvlRow0[0] and row0[1] == lvlRow0[1] and row0[2] == lvlRow0[2] and row0[3] == lvlRow0[3] and row0[4] == lvlRow0[4] and row0[5] == lvlRow0[5] and row0[6] == lvlRow0[6] and row0[7] == lvlRow0[7] and row0[8] == lvlRow0[8] and row0[9] == lvlRow0[9]:
        print("Row 0 good")
    else:
        print ("Row 0 has error")
        errorCount = errorCount + 1
    if row1[0] == lvlRow1[0] and row1[1] == lvlRow1[1] and row1[2] == lvlRow1[2] and row1[3] == lvlRow1[3] and row1[4] == lvlRow1[4] and row1[5] == lvlRow1[5] and row1[6] == lvlRow1[6] and row1[7] == lvlRow1[7] and row1[8] == lvlRow1[8] and row1[9] == lvlRow1[9]:
        print ("Row 1 good")
    else:
        print("Row 1 has error")
        errorCount = errorCount + 1
    if row2[0] == lvlRow2[0] and row2[1] == lvlRow2[1] and row2[2] == lvlRow2[2] and row2[3] == lvlRow2[3] and row2[4] == lvlRow2[4] and row2[5] == lvlRow2[5] and row2[6] == lvlRow2[6] and row2[7] == lvlRow2[7] and row2[8] == lvlRow2[8] and row2[9] == lvlRow2[9]:
        print("Row 2 good")
    else:
        print ("Row 2 has error")
        errorCount = errorCount + 1
    if row3[0] == lvlRow3[0] and row3[1] == lvlRow3[1] and row3[2] == lvlRow3[2] and row3[3] == lvlRow3[3] and row3[4] == lvlRow3[4] and row3[5] == lvlRow3[5] and row3[6] == lvlRow3[6] and row3[7] == lvlRow3[7] and row3[8] == lvlRow3[8] and row3[9] == lvlRow3[9]:
        print("Row 3 good")
    else:
        print ("Row 3 has error")
        errorCount = errorCount + 1
    if row4[0] == lvlRow4[0] and row4[1] == lvlRow4[1] and row4[2] == lvlRow4[2] and row4[3] == lvlRow4[3] and row4[4] == lvlRow4[4] and row4[5] == lvlRow4[5] and row4[6] == lvlRow4[6] and row4[7] == lvlRow4[7] and row4[8] == lvlRow4[8] and row4[9] == lvlRow4[9]:
        print("Row 4 good")
    else:
        print ("Row 4 has error")
        errorCount = errorCount + 1
    print("Errors in ", errorCount, "rows.")
    if errorCount == 0:
        print("Puzzle Solved!")
        victory()
    if errorCount > 1:
        fontSmall()
        errorNoise()
        thumby.display.drawText(str(errorCount) + " err", 54, 35, 1)

#Reset the square data in preperation for the next level (kina ugly code, could probably be done better if I knew how)
def resetLists():
    #resetting lvlRows
    row0[0] = 0
    row0[1] = 0
    row0[2] = 0
    row0[3] = 0
    row0[4] = 0
    row0[5] = 0
    row0[6] = 0
    row0[7] = 0
    row0[8] = 0
    row0[9] = 0
    row1[0] = 0
    row1[1] = 0
    row1[2] = 0
    row1[3] = 0
    row1[4] = 0
    row1[5] = 0
    row1[6] = 0
    row1[7] = 0
    row1[8] = 0
    row1[9] = 0
    row2[0] = 0
    row2[1] = 0
    row2[2] = 0
    row2[3] = 0
    row2[4] = 0
    row2[5] = 0
    row2[6] = 0
    row2[7] = 0
    row2[8] = 0
    row2[9] = 0
    row3[0] = 0
    row3[1] = 0
    row3[2] = 0
    row3[3] = 0
    row3[4] = 0
    row3[5] = 0
    row3[6] = 0
    row3[7] = 0
    row3[8] = 0
    row3[9] = 0
    row4[0] = 0
    row4[1] = 0
    row4[2] = 0
    row4[3] = 0
    row4[4] = 0
    row4[5] = 0
    row4[6] = 0
    row4[7] = 0
    row4[8] = 0
    row4[9] = 0
    #resetting sprite values
    row0Sprs[0] = 0
    row0Sprs[1] = 0
    row0Sprs[2] = 0
    row0Sprs[3] = 0
    row0Sprs[4] = 0
    row0Sprs[5] = 0
    row0Sprs[6] = 0
    row0Sprs[7] = 0
    row0Sprs[8] = 0
    row0Sprs[9] = 0
    row1Sprs[0] = 0
    row1Sprs[1] = 0
    row1Sprs[2] = 0
    row1Sprs[3] = 0
    row1Sprs[4] = 0
    row1Sprs[5] = 0
    row1Sprs[6] = 0
    row1Sprs[7] = 0
    row1Sprs[8] = 0
    row1Sprs[9] = 0
    row2Sprs[0] = 0
    row2Sprs[1] = 0
    row2Sprs[2] = 0
    row2Sprs[3] = 0
    row2Sprs[4] = 0
    row2Sprs[5] = 0
    row2Sprs[6] = 0
    row2Sprs[7] = 0
    row2Sprs[8] = 0
    row2Sprs[9] = 0
    row3Sprs[0] = 0
    row3Sprs[1] = 0
    row3Sprs[2] = 0
    row3Sprs[3] = 0
    row3Sprs[4] = 0
    row3Sprs[5] = 0
    row3Sprs[6] = 0
    row3Sprs[7] = 0
    row3Sprs[8] = 0
    row3Sprs[9] = 0
    row4Sprs[0] = 0
    row4Sprs[1] = 0
    row4Sprs[2] = 0
    row4Sprs[3] = 0
    row4Sprs[4] = 0
    row4Sprs[5] = 0
    row4Sprs[6] = 0
    row4Sprs[7] = 0
    row4Sprs[8] = 0
    row4Sprs[9] = 0

#Actual gameplay loop    
def puzzleTime():
    thumby.display.fill(0)
    gameRunning = True
    thumby.display.setFPS(60)
    resetLists()
    drawGrid()
    while(gameRunning):
        cursorMovement()
        printRowNumbers()
        printColNumbers()
        cellLogic()
        if thumby.buttonB.justPressed():
            checkSolution()
            if errorCount == 0:
                break
        if thumby.buttonA.pressed() and thumby.buttonB.pressed():
            gameRunning = False
            resetLists()
            break

#Printing the numbers in LevelMenu()
def printLevelNumbers():
    global pageOffset
    pageOffset = 1
    if levelPage == 1:
        pageOffset = 1 #this should match the top left level number on the screen for later math to work
        fontSmall()
        thumby.display.drawText("1  2  3  4  5  6", 5, 9, 1)
        thumby.display.drawText("7  8  9  10 11 12", 5, 15, 1)
        thumby.display.drawText("13 14 15 16 17 18", 5, 21, 1)
        thumby.display.drawText("19 20 21 22 23 24", 5, 27, 1)
    if levelPage == 2:
        pageOffset = 25
        fontSmall()
        thumby.display.drawText("25 26 27 28 29 30", 5, 9, 1)
        thumby.display.drawText("31 32 33 34 35 36", 5, 15, 1)
        thumby.display.drawText("37 38 39 40 41 42", 5, 21, 1)
        thumby.display.drawText("43 44 45 46 47 48", 5, 27, 1)
    #if levelPage == 3: #blank page, uncomment to add it back into game.
        #pageOffset = 49
        #fontSmall()
        #thumby.display.drawText("49 50 51 52 53 54", 5, 9, 1)
        #thumby.display.drawText("55 56 57 58 59 60", 5, 15, 1)
        #thumby.display.drawText("61 62 63 64 65 66", 5, 21, 1)
        #thumby.display.drawText("67 68 69 70 71 72", 5, 27, 1)
    #Feel free to add more pages here as needed in the same fashion, just remember to update the variable I pointed out in levelMenu()

#Level selection menu
def levelMenu(): #Level selection menu
    waiting2 = True
    pointerSpr.x = 1
    pointerLevel = 0
    pointerSpr.y = 9
    global moveNumY
    moveNumY = 6
    global levelPage
    levelPage = 1
    while(waiting2):
        thumby.display.fill(0)#draw text
        thumby.display.setFPS(60)
        decoSpr3.y = 1
        decoSpr3.x = 8
        thumby.display.drawSprite(decoSpr3)
        decoSpr4.y = 1
        decoSpr4.x = 56
        thumby.display.drawSprite(decoSpr4)
        fontMed()
        thumby.display.drawText("LEVELS", 19, 0, 1)
        fontSmall()
        thumby.display.drawText("Next", 5, 33, 1)
        thumby.display.drawText("Prev", 30, 33, 1)
        thumby.display.drawText("B:Menu", 48, 33, 1)
        printLevelNumbers()
        levelPointerMovement()
        thumby.display.update()
        if thumby.buttonB.justPressed(): #Back to Menu
            buttonBsound()
            waiting2 = False
            break
        if thumby.buttonA.justPressed():
            if pointerSpr.y == 9: #Row 1
                pointerLevel = (pointerSpr.x // 12) + int(pageOffset)
            if pointerSpr.y == 15: #Row 2
                pointerLevel = (pointerSpr.x // 12) + (int(pageOffset) + 6)
            if pointerSpr.y == 21: #row 3
                pointerLevel = (pointerSpr.x // 12) + (int(pageOffset) + 12)
            if pointerSpr.y == 27: #row 4
                pointerLevel = (pointerSpr.x // 12) + (int(pageOffset) +18)
            if pointerSpr.y > 27:
                pointerLevel = 0
            print(pointerLevel)
            thumby.saveData.setItem('temp', pointerLevel)
            thumby.saveData.save()
            if pointerLevel > 0:
                try: 
                    loadLevel()
                    buttonAsound()
                    puzzleTime()
                except:
                    errorNoise()
            #bottom options
            if pointerSpr.x ==25 and pointerSpr.y ==33:
                if levelPage == 1:
                    errorNoise()
                else:
                    levelPage += 1 #Previous page
                    thumby.display.update()
            if pointerSpr.x == 1 and pointerSpr.y ==33:
                if levelPage == 2: #<----------- THIS VARIABE RIGHT HERE. Increase to add more pages.
                    errorNoise()
                else:
                    levelPage += 1 #Next page
                    thumby.display.update()
                
#Main Menu
def mainMenu(): #Main Menu Options
    waiting = True
    pointerSpr2.x = 10
    pointerSpr2.y = 9
    moveNum = 6
    while(waiting): #Draw menu
        thumby.display.fill(0)
        thumby.display.setFPS(60)
        decoSpr1.x = 8
        decoSpr1.y = 1
        thumby.display.drawSprite(decoSpr1)
        decoSpr2.x = 50
        decoSpr2.y = 1
        thumby.display.drawSprite(decoSpr2)
        fontMed()
        thumby.display.drawText("MENU", 24, 0, 1)
        fontSmall()
        thumby.display.drawText("Levels", 16, 9, 1)
        thumby.display.drawText("How to Play", 16, 15, 1)
        thumby.display.drawText("Sound On/Off", 16, 21, 1)
        thumby.display.drawText("Credits", 16, 27, 1)
        thumby.display.drawText("Quit", 16, 33, 1)
        if thumby.buttonU.justPressed():#pointer movement
            buttonMoveSound()
            pointerSpr2.y -= moveNum
        if thumby.buttonD.justPressed():
            buttonMoveSound()
            pointerSpr2.y += moveNum
        if pointerSpr2.y < 9: #pointer bounding
            pointerSpr2.y = 9
        if pointerSpr2.y > 33:
            pointerSpr2.y = 33
        if pointerSpr2.x != 10:
            pointerSpr2.x = 10
        thumby.display.drawSprite(pointerSpr2)
        thumby.display.update()
        if thumby.buttonA.justPressed():
            if pointerSpr2.y == 9: #Level selection
                buttonAsound()
                levelMenu()
            if pointerSpr2.y == 15: #how to play
                buttonAsound()
                import howToPlay
                howToPlay.howToPlayGo()
            if pointerSpr2.y == 27: #credits
                import creditScreen
                happyNoise()
                creditScreen.creditsGo()
            if pointerSpr2.y == 33: #quit game
                thumby.reset()
            if pointerSpr2.y == 21:
                buttonAsound()
                soundOnOff()

#Title screen when you start the game            
def titleScreen():
    thumby.display.fill(0)
    thumby.display.setFPS(60)
    thumby.display.drawSprite(titleSpr)
    fontSmall()
    thumby.display.drawText("Press A to Start", 5, 28, 1)
    thumby.display.update()
    waiting = True
    while(waiting):
        pointerSpr.x = 0
        pointerSpr.y = 28
        thumby.display.drawSprite(pointerSpr)
        pointerSprMirror.x = 67
        pointerSprMirror.y = 28
        thumby.display.drawSprite(pointerSprMirror)
        thumby.display.update()
        if thumby.buttonA.justPressed():
            happyNoise()
            waiting = False
            thumby.display.fill(0)
            mainMenu()

#I find it kind of fascinating that you have to set ALL the variables and functions before you start.
#Because it means that the code kind of winds up running bottom to top, instead of top to bottom.
#IDK maybe I'm just a nerd.
titleScreen()
