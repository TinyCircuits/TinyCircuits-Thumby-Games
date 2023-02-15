'''
This is the compressed version to keep storage space low.
To edit the code and learn what it does go here: https://github.com/BeepyDev/Zig/blob/83fdb03d417876b2140d280b3c3bdbf3c40a9ad8/Unoptimized.py
'''

import thumby
import math
import time
import random
thumby.display.setFPS(30)
logoImg = bytearray([252,254,255,255,192,222,210,210,210,82,146,210,114,50,18,130,194,126,128,255,192,222,210,210,210,210,210,18,242,2,2,242,18,210,210,210,210,210,222,192,255,0,254,2,2,242,18,210,210,210,210,210,210,210,222,192,255,0,51,153,204,102,51,102,204,153,51,0,255,255,254,252,
           255,255,255,255,15,247,27,13,6,227,177,152,172,182,187,189,190,191,63,255,63,191,191,191,191,191,191,128,255,0,0,255,128,191,191,191,191,191,191,63,255,0,255,0,0,255,128,129,189,165,165,229,5,5,253,1,255,0,51,153,204,102,51,102,204,153,51,0,255,255,255,255,
           3,7,15,15,0,7,4,4,4,4,4,4,4,4,4,4,4,7,0,15,0,7,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,7,0,15,0,7,4,4,4,4,4,4,4,4,4,4,4,7,0,15,0,3,9,12,6,3,6,12,9,3,0,15,15,7,3])
logo = thumby.Sprite(72, 20, logoImg, 0, 0, 0)
zig = bytearray([30,33,45,45,33,30])
frame = bytearray([252,6,3,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,3,6,252,
            255,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,255,
            255,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,255,
            255,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,255,
            63,96,192,128,128,128,128,128,128,128,128,128,128,128,128,128,128,128,128,128,128,128,128,128,128,128,128,128,128,128,128,128,128,128,128,128,128,128,128,128,128,128,128,128,128,128,128,128,128,128,128,128,128,128,128,128,128,128,128,128,128,128,128,128,128,128,128,128,128,192,96,63])
spikeImg = bytearray([153,126,126,255,255,126,126,153])
spike = thumby.Sprite(8, 8, spikeImg, 0, 0, 0)
spike2 = thumby.Sprite(8, 8, spikeImg, 0, 0, 0)
debug = 0
zigY = 200
score = 0
spikeTick = 0
screen = "menu"
moveSpeed = 4
highscore = 0
spikeSpeed = 0.6
thumby.saveData.setName("Zig")
if (thumby.saveData.hasItem("highscore")):
    highscore = int(thumby.saveData.getItem("highscore"))
while(1):
    thumby.display.fill(0)
    thumby.display.blit(frame, 0, 0, 72, 40, 0, 0, 0)
    if thumby.buttonD.pressed() and thumby.buttonA.pressed():
            debug = 1
    if screen == "menu":
        thumby.display.drawSprite(logo)
        thumby.display.drawText("Press A/B", 9, 30, 1)
        thumby.display.drawText("Hi: %d" % highscore, 9, 22, 1)
        if thumby.actionJustPressed():
            thumby.audio.play(300, 50)
            screen = "game"
    if screen == "game":
        score += 0.0175
        if moveSpeed <= 16:
            moveSpeed += 0.005
        thumby.display.drawText("%d" % score, 4, 30, 1)
        thumby.display.drawSprite(spike)
        thumby.display.drawSprite(spike2)
        if spikeTick < 200:
            spikeTick += 1
            spike.x -= spikeSpeed
            spike2.x -= spikeSpeed
            if spikeTick == 100:
                spike2.y = random.randint(5, 30)
                spike2.x = 80
        else:
            spikeTick = 0
            spike.y = random.randint(5, 30)
            spike.x = 80
        if thumby.actionPressed():
            thumby.display.blit(zig, 20, int(zigY/10), 6, 6, 0, 0, 0)
            zigY += moveSpeed
        else:
            thumby.display.blit(zig, 20, int(zigY/10), 6, 6, 0, 0, 0)
            zigY -= moveSpeed
        if zigY < -10 or zigY > 330:
            zigY = 200
            spikeTick = 0
            thumby.audio.playBlocking(500, 400)
            thumby.audio.playBlocking(400, 200)
            thumby.audio.playBlocking(200, 400)
            screen = "death"
        if (spike.y in range(int(zigY/10-4), int(zigY/10+4), 1) and spike.x < 26 and spike.x > 14) or (spike2.y in range(int(zigY/10-4), int(zigY/10+4), 1) and spike2.x < 26 and spike2.x > 14):
            zigY = 200
            spikeTick = 0
            spike.y = 100
            spike2.y = 100
            thumby.audio.playBlocking(500, 400)
            thumby.audio.playBlocking(400, 200)
            thumby.audio.playBlocking(200, 400)
            screen = "death"
        if debug == 1:
            thumby.display.drawText("Speed %d" % moveSpeed + "/16", 5, 3, 1)
    if screen == "death":
        if (thumby.saveData.hasItem("highscore")):
            highscore = int(thumby.saveData.getItem("highscore"))
        thumby.display.drawText("You died!", 9, 2, 1)
        thumby.display.drawText("Scr: %d" % score, 3, 14, 1)
        thumby.display.drawText("Hi:  %d" % highscore, 3, 22, 1)
        thumby.display.drawText("Press A&B", 9, 30, 1)
        if score > highscore:
            thumby.saveData.setItem("highscore", score)
            thumby.saveData.save()
        if thumby.buttonA.pressed() and thumby.buttonB.pressed():
            score = 0
            moveSpeed = 4
            spikeTick = 400
            thumby.audio.play(300, 50)
            screen = "game"
    thumby.display.update()
