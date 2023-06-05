### Simon
# by PossiblyAxolotl
# https://possiblyaxolotl.itch.io

import thumby
import math
import time
import random

thumby.saveData.setName("Simon")
thumby.display.setFPS(60)
thumby.display.setFont("/Games/Simon/numberFont.bin", 3, 5, 1)
thumby.audio.setEnabled(True)
snd = True

# game art
# simon board: width: 34, height: 34
simonBoard = bytearray([0,0,0,128,192,96,240,216,152,12,12,6,6,3,3,3,3,3,3,3,3,6,6,12,12,152,216,240,96,192,128,0,0,0,
           224,248,30,7,0,0,0,1,3,7,14,28,56,112,224,192,128,128,192,224,112,56,28,14,7,3,1,0,0,1,7,30,248,224,
           31,127,224,128,0,0,0,0,0,128,192,224,112,56,28,15,7,7,15,28,56,112,224,192,128,0,0,0,0,0,128,224,127,31,
           0,0,1,7,14,24,60,110,103,195,193,128,128,0,0,0,0,0,0,0,0,128,128,193,195,103,110,60,24,14,7,1,0,0,
           0,0,0,0,0,0,0,0,0,0,0,1,1,3,3,3,3,3,3,3,3,1,1,0,0,0,0,0,0,0,0,0,0,0])
sprSimonBoard = thumby.Sprite(34,34,simonBoard,34-15,3)
# BITMAP: width: 38, height: 38
simonBG = bytearray([255,255,255,255,127,63,31,15,7,7,3,3,1,1,0,0,0,0,0,0,0,0,0,0,1,1,3,3,7,7,15,31,63,127,255,255,255,255,
           63,15,3,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,3,15,63,
           0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,
           255,252,240,192,128,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,128,192,240,252,255,
           63,63,63,63,63,63,62,60,56,56,48,48,32,32,0,0,0,0,0,0,0,0,0,0,32,32,48,48,56,56,60,62,63,63,63,63,63,63])
sprSimonBG = thumby.Sprite(38,38,simonBG,34-17,1)
# sDown, sUp: width: 14, height: 10
sDown = bytearray([192,224,240,248,252,254,255,255,254,252,248,240,224,192,
           0,0,1,1,3,3,3,3,3,3,1,1,0,0])
sUp = bytearray([12,28,62,126,255,255,255,255,255,255,126,62,28,12,
           0,0,0,0,0,1,3,3,1,0,0,0,0,0])

# sLeft, sRight: width: 10, height: 14
sLeft = bytearray([240,252,255,255,254,252,248,240,224,192,
           3,15,63,63,31,15,7,3,1,0])
sRight = bytearray([192,224,240,248,252,254,255,255,252,240,
           0,1,3,7,15,31,63,63,15,3])

# title art
# logotext: width: 72, height: 40
logotext = bytearray([0,0,0,0,0,0,0,0,0,0,0,0,0,0,56,124,108,108,108,108,236,204,0,12,12,12,252,252,12,12,12,0,252,252,56,112,112,56,252,252,0,248,252,12,12,12,12,252,248,0,252,252,56,112,224,192,252,252,0,0,0,0,0,0,0,0,0,0,0,0,0,0,
           160,160,160,160,160,160,160,160,160,160,160,160,160,160,163,163,163,163,163,163,163,161,160,163,163,163,163,163,163,163,163,160,163,163,160,160,160,160,163,163,160,161,163,163,163,163,163,163,161,160,163,163,160,160,160,161,163,163,160,160,160,160,160,160,160,160,160,160,160,160,160,160,
           1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,249,249,241,241,97,97,1,1,97,97,249,249,97,97,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,
           88,88,88,88,88,88,88,88,88,88,88,88,88,88,88,88,88,88,88,88,88,88,88,88,88,89,89,88,88,88,88,88,88,88,88,89,89,88,88,88,88,88,88,88,88,88,88,88,88,88,88,88,88,88,88,88,88,88,88,88,88,88,88,88,88,88,88,88,88,88,88,88,
           0,124,16,124,0,68,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,68,0,124,64,64,0])# logobrackets: width: 72, height: 10
logobrackets = bytearray([0,0,252,0,252,252,0,252,252,12,12,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,12,12,252,252,0,252,252,0,252,0,0,
           0,0,3,0,3,3,0,3,3,3,3,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,3,3,3,3,0,3,3,0,3,0,0])
sprLogoText = thumby.Sprite(72,40,logotext,0,0,0)
sprLogoBrackets = thumby.Sprite(72,10,logobrackets,0,0,0)
# sound: width: 20, height: 6
sound = bytearray([30,30,63,63,0,33,30,0,33,30,30,30,63,63,0,33,18,12,18,33])
sprSound = thumby.Sprite(10,6,sound,41,19)
# controls: width: 32, height: 8
controls = bytearray([44,44,52,0,60,44,36,0,60,32,32,0,60,44,36,0,60,36,36,0,4,60,4,0,60,36,231,129,129,231,36,60])
sprControls = thumby.Sprite(32,8,controls,thumby.display.width/2-16,thumby.display.height/2-4)

# vars
possibleMoves = [thumby.buttonU, thumby.buttonD, thumby.buttonL, thumby.buttonR]
movesKey = {
    thumby.buttonU:thumby.Sprite(14,10,sUp,29,6,0),
    thumby.buttonD:thumby.Sprite(14,10,sDown,29,24,0),
    thumby.buttonL:thumby.Sprite(10,14,sLeft,22,13,0),
    thumby.buttonR:thumby.Sprite(10,14,sRight,40,13,0)
}
sndKey = {
    thumby.buttonU:1000,
    thumby.buttonR:400,
    thumby.buttonD:600,
    thumby.buttonL:800
}

prevMoves = []
moves = []

resetTime = 120
timeLeft = 120

score = -1

mode = False # False = menu, True = game

particles = []

# particles
def screenBurst():
    for i in range(0, 20):
        direction = math.radians(random.randint(0, 359))
        part = [random.randint(0,thumby.display.width),random.randint(0,thumby.display.height),random.randint(1,6),math.sin(direction),-math.cos(direction)]
        particles.append(part)
        
def addParts(_x,_y, amount):
    for i in range(0, amount):
        direction = math.radians(random.randint(0, 359))
        part = [_x,_y,random.randint(1,6),math.sin(direction),-math.cos(direction)]
        particles.append(part)

def drawParticles():
    for part in particles:
        #if frame % 2 == 0:
        thumby.display.drawFilledRectangle(round(part[0]),round(part[1]),math.ceil(part[2]),math.ceil(part[2]),1)

def updateParticles():
    for part in particles:
        part[0] += part[3]
        part[1] += part[4]
            
        part[2] -= 0.2
        if part[2] <= 0:
            particles.remove(part)

while thumby.inputJustPressed() != True:
    thumby.display.fill(0)
    thumby.display.drawSprite(sprControls)
    thumby.display.update()

thumby.display.fill(0)
thumby.display.update()

time.sleep(0.5)

screenBurst()

# gameloop
while True:
    thumby.display.fill(0)
    updateParticles()
    
    if mode: # if game is playing
        while len(particles) > 0:
            thumby.display.fill(0)
            thumby.display.drawSprite(sprSimonBoard)
            drawParticles()
            updateParticles()
            thumby.display.update()
            
        
        timeLeft -= 1
        
        if timeLeft < 1:
            mode = False
            screenBurst()
            thumby.saveData.setItem("lastScore", score)
            if thumby.saveData.hasItem("highScore"):
                if thumby.saveData.getItem("highScore") < score:
                    thumby.saveData.setItem("highScore", score)
            else:
                thumby.saveData.setItem("highScore", score)
            thumby.saveData.save()
        
        drawParticles()
        #thumby.display.drawSprite(sprSimonBG)
        thumby.display.drawSprite(sprSimonBoard)

        if len(moves) < 1: # if all moves are done, add a new button to the end and reset the list
            thumby.display.update()
            time.sleep(0.5)
            prevMoves.append(random.choice(possibleMoves))
            moves = prevMoves.copy()
            print(moves)
            score += 1
            
            for move in moves:
                thumby.display.drawSprite(movesKey[move])
                thumby.audio.play(sndKey[move],1000)
                thumby.display.update()
                time.sleep(1)
                thumby.display.fill(0)
                drawParticles()
                #thumby.display.drawSprite(sprSimonBG)
                thumby.display.drawSprite(sprSimonBoard)
                thumby.display.update()
                time.sleep(0.5)
        else:
            thumby.display.drawLine(36,0,math.ceil(36+(36 * (timeLeft / resetTime))),0,1)
            thumby.display.drawLine(35,0,math.floor(35-(36 * (timeLeft / resetTime))),0,1)
        
        if thumby.dpadJustPressed():
            move = moves.pop(0)
            if move.pressed(): # correct button
                print("yes")
                
                timeLeft = resetTime
                
                thumby.display.drawSprite(movesKey[move])
                thumby.audio.play(sndKey[move],500)
                thumby.display.update()
                time.sleep(0.5)
            else: # incorrect button
                print("no")
                mode = False
                screenBurst()
                thumby.saveData.setItem("lastScore", score)
                if thumby.saveData.hasItem("highScore"):
                    if thumby.saveData.getItem("highScore") < score:
                        thumby.saveData.setItem("highScore", score)
                else:
                    thumby.saveData.setItem("highScore", score)
                thumby.saveData.save()
    else:
        thumby.display.drawSprite(sprLogoText)
        thumby.display.drawSprite(sprLogoBrackets)
        thumby.display.drawSprite(sprSound)
        sprLogoBrackets.x = math.sin(timeLeft)*2
        timeLeft += 0.05

        if thumby.saveData.hasItem("highScore"):
            thumby.display.drawText(str(thumby.saveData.getItem("highScore")),7,34,1)
        else:
            thumby.display.drawText("0",7,34,1)
        if thumby.saveData.hasItem("lastScore"):
            thumby.display.drawText(str(thumby.saveData.getItem("lastScore")),66 - 4* len(str(thumby.saveData.getItem("lastScore"))),34,1)
        else:
            thumby.display.drawText("0",62,34,1)
        
        if thumby.buttonL.justPressed():
            screenBurst()
            mode = True
            timeLeft = 120
            prevMoves = []
            moves = []
            score = -1
        if thumby.buttonR.justPressed():
            snd = not snd
            thumby.audio.setEnabled(snd)
            sprSound.setFrame(int(snd == False))
            addParts(45,22,5)

        drawParticles()
    
    thumby.display.update()