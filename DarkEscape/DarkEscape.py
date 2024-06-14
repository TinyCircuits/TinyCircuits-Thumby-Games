# Dark Escape
###################################
# Respond to prompts by pressing the appropriate keys before the lights
# go out and the shadow monster gets you.
###################################
# Author Thomas Kline
# Version 1.0
# Date 03/13/24
###################################

import time
import thumby
import math
import random

thumby.display.setFPS(30)
thumby.saveData.setName("DarkEscape")
highScore = 0

if (thumby.saveData.hasItem("highscore")):
    highScore = int(thumby.saveData.getItem("highscore"))

# BITMAP: width: 25, height: 40
deviceBitmap = bytearray([255,255,3,251,251,27,27,27,27,27,27,27,27,27,27,27,27,27,27,27,251,251,3,255,255,
           255,255,0,255,255,192,192,192,192,192,192,192,192,192,192,192,192,192,192,192,255,127,128,255,255,
           255,255,127,126,126,14,14,14,126,126,126,254,254,254,254,254,254,254,254,62,30,31,63,255,255,
           255,255,252,252,252,224,224,224,252,252,252,255,255,255,255,249,240,240,249,255,254,254,255,255,255,
           255,255,255,255,255,255,255,255,255,253,252,254,255,253,252,254,255,255,255,255,255,207,207,255,127])
deviceSprite = thumby.Sprite(25,40,deviceBitmap,key=0)

# BITMAP: width: 9, height: 9
upBitmap = bytearray([48,56,28,14,255,14,28,56,48,
           0,0,0,0,1,0,0,0,0])
upSprite = thumby.Sprite(9,9,upBitmap,key=0)

# BITMAP: width: 9, height: 9
downBitmap = bytearray([28,56,112,224,255,224,112,56,28,
           0,0,0,0,1,0,0,0,0])
downSprite = thumby.Sprite(9,9,downBitmap,key=0)

# BITMAP: width: 9, height: 9
leftBitmap = bytearray([16,56,124,254,215,147,17,16,16,
           0,0,0,0,1,1,1,0,0])
leftSprite = thumby.Sprite(9,9,leftBitmap,key=0)

# BITMAP: width: 9, height: 9
rightBitmap = bytearray([16,16,17,147,215,254,124,56,16,
           0,0,1,1,1,0,0,0,0])
rightSprite = thumby.Sprite(9,9,rightBitmap,key=0)

# BITMAP: width: 30, height: 40
roomBitmap = bytearray([255,255,255,255,255,255,255,255,0,255,255,255,255,255,255,255,255,255,1,125,229,196,229,125,1,255,255,255,255,255,
           255,255,255,255,255,255,255,255,0,255,255,255,255,255,255,255,255,255,252,253,252,252,252,253,252,255,255,255,255,255,
           255,255,127,191,223,239,247,251,252,253,253,253,253,253,253,253,253,253,253,253,253,253,253,253,253,253,61,61,13,5,
           253,254,255,255,255,255,255,255,255,255,255,255,255,63,31,31,31,63,255,255,255,255,255,255,255,215,231,199,231,230,
           255,255,255,255,255,255,255,255,255,255,255,255,127,59,201,224,201,59,127,255,255,255,255,255,255,255,255,255,255,255])
roomSprite = thumby.Sprite(30,40,roomBitmap,key=0)

# BITMAP: width: 30, height: 40
roomBitmap2 = bytearray([255,255,255,255,255,255,255,255,0,255,255,255,255,255,255,255,255,255,1,125,229,196,229,125,1,255,255,255,255,255,
           255,255,255,255,255,255,255,255,0,255,255,255,255,255,255,255,255,255,252,253,252,252,252,253,252,255,255,255,255,255,
           255,255,127,191,223,239,247,251,252,253,253,253,253,253,253,253,253,253,253,253,253,253,157,29,5,21,1,5,13,61,
           253,254,255,255,255,255,255,255,255,255,255,255,255,63,31,31,31,63,255,255,255,255,175,207,143,199,231,230,128,0,
           255,255,255,255,255,255,255,255,255,255,255,255,127,59,201,224,201,59,127,255,255,255,255,255,255,255,207,195,193,248])
roomSprite2 = thumby.Sprite(30,40,roomBitmap2,key=0)

# BITMAP: width: 30, height: 40
roomBitmap3 = bytearray([255,255,255,255,255,255,255,255,0,255,255,255,255,255,255,255,255,255,1,125,229,196,229,125,1,255,255,255,255,255,
           255,255,255,255,255,255,255,255,0,255,255,255,255,255,255,255,255,255,252,253,252,252,252,253,252,255,255,255,255,255,
           255,255,127,191,223,239,247,251,252,253,253,253,253,253,253,253,253,253,61,29,141,165,13,29,29,61,125,253,253,253,
           253,254,255,255,255,255,255,255,255,255,255,255,255,255,15,15,15,255,254,95,153,92,174,207,130,0,0,1,1,227,
           255,255,255,255,255,255,255,255,255,255,255,255,255,124,13,224,13,124,255,255,255,255,243,241,252,252,200,192,194,255])
roomSprite3 = thumby.Sprite(30,40,roomBitmap3,key=0)

deviceSprite.x = 10
deviceSprite.y = 0

upSprite.x = 18
upSprite.y = 6
downSprite.x = 18
downSprite.y = 6
leftSprite.x = 18
leftSprite.y = 6
rightSprite.x = 18
rightSprite.y = 6

roomSprite.x = 40
roomSprite.y = 0
roomSprite2.x = 40
roomSprite2.y = 0
roomSprite3.x = 40
roomSprite3.y = 0
count = 1
brightness = 127
fade = False
lose = False
randomSet = False
buttonSuccess = False
win = False
holdBright = False
score = 0
randomButton = 0

thumby.display.brightness(brightness)
thumby.display.fill(0)
thumby.display.drawRectangle(0,0,71,39,1)
thumby.display.drawText("Dark Escape", 2, 7, 1)
thumby.display.update()


while ((thumby.buttonA.pressed() == False) and (thumby.buttonB.pressed() == False)):
    if (time.ticks_ms() % 1000 < 500):
        thumby.display.drawText("Start: A/B", 2, 20, 1)
    else:
        thumby.display.drawText("Start: A/B", 2, 20, 0)
    thumby.display.update()
    pass
thumby.display.fill(0)
thumby.display.drawText("Instructions:",0,0,1)
thumby.display.drawLine(0,10,72,10,1)
thumby.display.drawText("Don't let it",0,20,1)
thumby.display.drawText("get dark!",4,30,1)
thumby.display.update()
time.sleep(3)
thumby.display.fill(0)
thumby.display.drawText("Press button",0,0,1)
thumby.display.drawText("displayed on",0,10,1)
thumby.display.drawText("the screen ",2,20,1)
thumby.display.update()
time.sleep(4)
thumby.display.fill(0)
thumby.display.drawText("to increase",0,10,1)
thumby.display.drawText("the light.",0,20,1)
thumby.display.update()
time.sleep(4)
thumby.display.fill(0)
thumby.display.update()
time.sleep(2)
thumby.display.drawText("Good Luck!",0,5,1)
thumby.display.drawText("The shadow",0,20,1)
thumby.display.drawText("is waiting..",0,30,1)
thumby.display.update()
time.sleep(3)
while(brightness >= 0):
    if (holdBright == True):
        holdBright = False
    else:
        brightness -= 1
    thumby.display.brightness(brightness)
    thumby.display.update()
brightness = 127
time.sleep(1)

while(1):
    thumby.display.fill(0)
    thumby.display.brightness(brightness)
    thumby.display.drawSprite(deviceSprite)
    if (brightness > 87):
        thumby.display.drawSprite(roomSprite)
    elif (brightness <= 87 and brightness > 42):
        thumby.display.drawSprite(roomSprite2)
    else:
        thumby.display.drawSprite(roomSprite3)
    count += 1
    if (count >= 120):
        if (randomSet == False):
            randomButton = random.randint(0, 5)
            randomSet = True
        if (randomButton == 0):
            thumby.display.drawSprite(upSprite)
            if ((thumby.buttonU.pressed() == True) and (fade == True)):
                buttonSuccess = True
        elif (randomButton == 1):
            thumby.display.drawSprite(downSprite)
            if ((thumby.buttonD.pressed() == True) and (fade == True)):
                buttonSuccess = True
        elif (randomButton == 2):
            thumby.display.drawSprite(leftSprite)
            if ((thumby.buttonL.pressed() == True) and (fade == True)):
                buttonSuccess = True
        elif (randomButton == 3):
            thumby.display.drawSprite(rightSprite)
            if ((thumby.buttonR.pressed() == True) and (fade == True)):
                buttonSuccess = True
        elif (randomButton == 4):
            thumby.display.drawText("A",20,6,1)
            if ((thumby.buttonA.pressed() == True) and (fade == True)):
                buttonSuccess = True
        elif (randomButton == 5):
            thumby.display.drawText("B",20,6,1)
            if ((thumby.buttonB.pressed() == True) and (fade == True)):
                buttonSuccess = True
        fade = True
    if (buttonSuccess == True):
        thumby.audio.play(420,300)
        buttonSuccess = False
        count = 1
        fade = False
        randomSet = False
        score += 1
        if (score == 50): win = True
        brightness += 50
        if (brightness >= 127):
            brightness = 127
    if (fade == True):
        if ((score > 0) and (score < 6)):
            brightness -= 1
        elif ((score > 5) and (score < 11)):
            brightness -= 2
        elif ((score > 10) and (score < 16)):
            brightness -= random.randint(2,3)
        elif ((score > 15) and (score < 21)):
            brightness -= random.randint(2,4)
        elif ((score > 20) and (score < 31)):
            brightness -= random.randint(2,5)
        elif ((score > 30) and (score < 41)):
            brightness -= random.randint(3,5)
        elif (score > 40):
            brightness -= random.randint(3,6)
        
    if (brightness <= 0):
        lose = True
        fade = False
        count = 1
        thumby.audio.play(260, 250)
    
    if (lose == True):
        if (score > highScore):
            thumby.saveData.setItem("highscore", score)
            thumby.saveData.save()
            highscore = score
        brightness = 127
        thumby.display.fill(0)
        if (count <= 120):
            thumby.display.drawText("Game Over", 10, 5, 1)
            thumby.display.drawText("Score: " + str(score),10, 15, 1) 
            thumby.display.drawText("High: " + str(highScore),5,30,1)
        else:
            thumby.display.drawText("Replay? [B]", 0, 5, 1)
            thumby.display.drawText("  Quit? [A]", 0, 15, 1)
        if (thumby.buttonA.pressed() == True):
            machine.reset()
        elif (thumby.buttonB.pressed() == True):
            lose = False
            count = 1
            randomSet = False
            score = 0
            buttonSuccess = True
        
    if (win == True):
        brightness = 127
        thumby.display.fill(0)
        thumby.display.drawText("YOU ARE",0,0,1)
        thumby.display.drawText("TRULY A",0,10,1)
        thumby.display.drawText("WINNER!!",0,20,1)
        thumby.display.drawText("^^ 50 ^^",10,30,1)
        thumby.saveData.setItem("highscore", score)
        thumby.saveData.save()
        time.sleep(6)
        machine.reset()
    
    thumby.display.update()
