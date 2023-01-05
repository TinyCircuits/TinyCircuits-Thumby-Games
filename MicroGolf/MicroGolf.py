import thumby
import time
from math import pow, sqrt, cos, sin

from sys import path
path.append("/Games/MicroGolf")

import course

thumby.display.setFPS(60)

holeNum = 1
holeScore = [-1, -1, -1, -1, -1, -1]

ball, hole, walls = course.load(holeNum)
ballSpeed = [0.0, 0.0]

ballSpr = thumby.Sprite(4, 4, bytearray([6,15,15,6]), 0, 0, 0)
holeSpr = thumby.Sprite(5, 5, bytearray([14,17,17,17,14]), 0, 0, 0)

hitDir = 0.0
hitPower = 0
hitCount = 0

mode = "putt" # putt, wait

#title
logo = bytearray([0,0,0,0,224,224,224,128,0,0,0,128,224,224,224,0,0,176,176,0,0,0,128,128,128,0,0,128,128,128,128,0,0,128,128,128,128,0,0,0,0,0,0,128,192,96,32,32,32,32,64,0,0,0,128,128,128,128,0,0,0,240,240,0,128,224,240,144,16,0,0,0,
           0,0,0,0,63,63,0,7,62,48,62,7,0,63,63,0,0,63,63,0,0,31,63,32,32,17,0,63,63,0,0,0,31,63,32,32,63,31,0,0,0,0,0,15,31,48,32,34,34,62,30,0,0,31,63,32,32,63,31,0,0,63,63,0,0,63,63,0,0,0,0,0,
           0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,128,128,128,128,192,192,64,32,24,142,192,126,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,
           0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,112,248,252,252,252,248,112,0,0,2,142,206,206,206,206,238,238,231,103,103,103,115,51,51,51,25,25,8,12,12,6,2,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,
           0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,1,1,0,0,0,0,0,1,1,1,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,30,33,33,41,26,0,30,51,33,33,51,30,0,0,33,51,63,63,30,12,0,0])
logoSpr = thumby.Sprite(72, 40, logo, 0, 0, 0)

thumby.display.fill(0)
thumby.display.drawSprite(logoSpr)
thumby.display.update()

while(thumby.actionPressed() == False):
    pass
while(thumby.actionPressed() == True):
    pass
del logoSpr
del logo

thumby.saveData.setName("MicroGolf")

def showCard(end:bool):
    thumby.display.fill(0)
    thumby.display.setFont("/lib/font5x7.bin", 5, 7, 1)
    
    if end:
        score = sum(holeScore)
        best = -1
        if thumby.saveData.hasItem("best"):
            best = thumby.saveData.getItem("best")
        else:
            best = score + 1
            
        bestText = "Best:" + str(min(score, best))
            
        if score < best:
            thumby.saveData.setItem("best", score)
            thumby.saveData.save()
            thumby.display.setFont("/lib/font3x5.bin", 3, 5, 1)
            thumby.display.drawText("new", 4 + len(bestText) * 6, 29, 1)
            thumby.display.setFont("/lib/font5x7.bin", 5, 7, 1)
            
        
        thumby.display.drawText("Total:" + str(score), 3, 3, 1)
        thumby.display.drawText(bestText, 3, 30, 1)
    else:
        thumby.display.drawText("Hole " + str(holeNum), 3, 3, 1)
        thumby.display.drawText("Go>", 52, 30, 1)
    
    thumby.display.drawLine(6, 13, 66, 13, 1)
    thumby.display.drawLine(6, 25, 66, 25, 1)
    thumby.display.drawLine(66, 13, 66, 25, 1)
    
    for n in range(6):
        thumby.display.drawLine(6 + 10 * n, 13, 6 + 10 * n, 25, 1)
        
        if holeScore[n] > 0 and holeScore[n] < 10:
            thumby.display.setFont("/lib/font5x7.bin", 5, 7, 1)
            thumby.display.drawText(str(holeScore[n]), 9 + 10 * n, 16, 1)
        elif holeScore[n] > 0:
            thumby.display.setFont("/lib/font3x5.bin", 3, 5, 1)
            thumby.display.drawText(str(holeScore[n]), 7 + 10 * n, 17, 1)
    
    thumby.display.update()
    
    while(thumby.actionPressed() == False):
        pass
    while(thumby.actionPressed() == True):
        pass

showCard(False)

#game

def updatePutt():
    global hitDir
    global mode
    global hitPower
    global hitCount
    
    # controls
    if thumby.buttonU.pressed() or thumby .buttonL.pressed():
        hitDir -= 0.02
    if thumby.buttonD.pressed() or thumby .buttonR.pressed():
        hitDir += 0.02
    if thumby.actionPressed():
        hitPower += 0.02
        hitPower = min(hitPower, 1)
    elif hitPower > 0:
        mode = "wait"
        ballSpeed[0] = cos(hitDir) * (hitPower * 2)
        ballSpeed[1] = sin(hitDir) * (hitPower * 2)
        hitPower = 0
        hitCount += 1


def updateWait():
    global mode
    
    ball[0] += ballSpeed[0]
    ball[1] += ballSpeed[1]
    
    if ball[0] < 2:
        ball[0] = 2
        ballSpeed[0] = abs(ballSpeed[0])
    if ball[0] > thumby.display.width - 2:
        ball[0] = thumby.display.width - 2
        ballSpeed[0] = -abs(ballSpeed[0])
    if ball[1] < 2:
        ball[1] = 2
        ballSpeed[1] = abs(ballSpeed[1])
    if ball[1] > thumby.display.height - 2:
        ball[1] = thumby.display.height - 2
        ballSpeed[1] = -abs(ballSpeed[1])
    
    for w in walls:
        if ball[0] < w[0] - 2 or ball[0] > w[0] + w[2] + 2:
            continue
        if ball[1] < w[1] - 2 or ball[1] > w[1] + w[3] + 2:
            continue
        
        px = ball[0] - ballSpeed[0]
        py = ball[1] - ballSpeed[1]
        
        if px < w[0] - 2 or px > w[0] + w[2] + 2:
            ball[0] = px
            ballSpeed[0] = -ballSpeed[0]
        if py < w[1] - 2 or py > w[1] + w[3] + 2:
            ball[1] = py
            ballSpeed[1] = -ballSpeed[1]
    
    ballSpeed[0] *= 0.99
    ballSpeed[1] *= 0.99
    if abs(ballSpeed[0]) < 0.02 and abs(ballSpeed[1]) < 0.02:
        mode = "putt"

def draw():
    thumby.display.fill(0)
    
    for w in walls:
        thumby.display.drawFilledRectangle(w[0], w[1], w[2], w[3], 1)
    
    ballSpr.x = int(ball[0]-1.5)
    ballSpr.y = int(ball[1]-1.5)
    thumby.display.drawSprite(ballSpr)
    
    holeSpr.x = int(hole[0]-2)
    holeSpr.y = int(hole[1]-2)
    thumby.display.drawSprite(holeSpr)
    
    if mode == "putt":
        fx = int(ball[0] + cos(hitDir) * 5)
        fy = int(ball[1] + sin(hitDir) * 5)
        tx = int(ball[0] + cos(hitDir) * 10)
        ty = int(ball[1] + sin(hitDir) * 10)
        thumby.display.drawLine(fx, fy, tx, ty, 1)
        
        th = int(thumby.display.height - thumby.display.height * hitPower)
        thumby.display.drawLine(0, thumby.display.height, 0, th, 1)
        thumby.display.drawLine(thumby.display.width-1, thumby.display.height, thumby.display.width-1, th, 1)
        
    
    thumby.display.update()

while(True):
    if sqrt(pow(ball[0] - hole[0], 2) + pow(ball[1] - hole[1], 2)) < 4:
        holeScore[holeNum - 1] = hitCount
        holeNum += 1
        hitCount = 0
        hitDir = 0.0
        hitPower = 0
        
        ball, hole, walls = course.load(holeNum)
        ballSpeed = [0.0, 0.0]
        
        end = len(ball) == 0
        showCard(end)
        
        if end:
            holeNum = 1
            holeScore = [-1, -1, -1, -1, -1, -1]
            showCard(False)
            ball, hole, walls = course.load(holeNum)

    if mode == "putt":
        updatePutt()
    elif mode == "wait":
        updateWait()
    
    draw()
