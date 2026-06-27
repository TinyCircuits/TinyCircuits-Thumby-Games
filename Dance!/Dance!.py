#Dance!

import thumby
import random

game = True
speed = 3
close = True
newScore = 0
thumby.saveData.setName("Dance")
if (thumby.saveData.hasItem("highscore")):
    highScore = int(thumby.saveData.getItem("highscore"))
else:
    highScore = 0
if(newScore > highScore):
    thumby.saveData.setItem("highscore", newScore)
    thumby.saveData.save()
scene = bytearray([4,4,4,6,6,6,6,7,7,7,7,7,7,7,7,7,7,7,7,7,7,7,7,7,7,7,7,7,7,6,6,6,6,4,4,4])
sceneSprite = thumby.Sprite(36, 3, scene)
line = bytearray([255,255,255,255,
           255,255,255,255,
           255,255,255,255,
           255,255,255,255,
           255,255,255,255,
           255,255,255,255,
           255,255,255,255,
           255,255,255,255,
           255,255,255,255,
           255,255,255,255])
dancer1 = bytearray([0,0,0,0,0,158,161,225,225,161,158,0,0,0,0,0,
           0,0,0,2,3,193,32,31,31,32,193,3,2,0,0,0])
dancer2 = bytearray([0,0,0,0,0,158,161,225,225,161,222,96,32,0,0,0,
           0,0,0,2,3,193,32,31,31,32,192,0,0,0,0,0])
dancer3 = bytearray([0,0,0,32,96,222,161,225,225,161,158,0,0,0,0,0,
           0,0,0,0,0,192,32,31,31,32,193,3,2,0,0,0])
logo = bytearray([15,15,15,15,240,240,240,240,15,15,15,15,
           0,0,0,0,0,0,0,0,0,0,0,0])
logoSprite = thumby.Sprite(12, 12, logo)
dancer1Sprite = thumby.Sprite(16, 16, dancer1)
dancer2Sprite = thumby.Sprite(16, 16, dancer2)
dancer3Sprite = thumby.Sprite(16, 16, dancer3)
lineSprite = thumby.Sprite(4, 80, line)
lineSprite2 = thumby.Sprite(4, 80, line)
lineSprite.y = random.randint(-500, -100)
lineSprite2.y = random.randint(-500, -100)
logoSprite.x = 3
logoSprite.y = 3
dancer1Sprite.x = 10
dancer1Sprite.y = 20
dancer2Sprite.x = 10
dancer2Sprite.y = 20
dancer3Sprite.x = 10
dancer3Sprite.y = 20
thumby.display.setFPS(60)

while True:
    if game == False:
        if thumby.inputJustPressed():
            newScore = 0
            speed = 3
            close = True
            game = True
            lineSprite.y = random.randint(-500, -100)
            lineSprite2.y = random.randint(-500, -100)
            if (thumby.saveData.hasItem("highscore")):
                highScore = int(thumby.saveData.getItem("highscore"))
            thumby.audio.play(200, 3)
    else:
        if close == True:
            thumby.display.fill(1)
            thumby.display.drawSprite(logoSprite)
            thumby.display.drawText("PRESS ANY", 2, 18, 0)
            thumby.display.drawText("BUTTON", 2, 28, 0)
            if thumby.inputJustPressed():
                close = False
                thumby.audio.play(200, 3)
        else:
            thumby.display.fill(0)
            sceneSprite.x = 0
            sceneSprite.y = 37
            lineSprite.x = 54
            lineSprite.y = lineSprite.y + speed
            lineSprite2.x = 68
            lineSprite2.y = lineSprite2.y + speed
            if thumby.buttonA.justPressed() == True and lineSprite2.y > -30 and lineSprite2.y < 40:
                thumby.display.drawSprite(dancer3Sprite)
                lineSprite2.y = random.randint(-500, -100)
                thumby.audio.play(2000, 1)
                newScore = newScore + 1
                speed = speed+(newScore//10+1)*0.01
            elif thumby.buttonB.justPressed() == True and lineSprite.y > -30 and lineSprite.y < 40:
                thumby.display.drawSprite(dancer2Sprite)
                lineSprite.y = random.randint(-500, -100)
                thumby.audio.play(2000, 1)
                newScore = newScore + 1
                speed = speed+(newScore//10+1)*0.01
            elif thumby.buttonA.pressed() == True:
                thumby.display.drawSprite(dancer3Sprite)
            elif thumby.buttonB.pressed() == True:
                thumby.display.drawSprite(dancer2Sprite)
            elif lineSprite2.y > 40 or lineSprite.y > 40:
                if(newScore > highScore):
                    thumby.saveData.setItem("highscore", newScore)
                    thumby.saveData.save()
                thumby.display.drawText("YOU LOSE!", 0, 17, 1)
                game = False
            else:
                thumby.display.drawSprite(dancer1Sprite)
            thumby.display.drawText("HS:" + str(highScore) + "S:" + str(newScore), 0, 0, 1)
            thumby.display.drawSprite(sceneSprite)
            thumby.display.drawSprite(lineSprite)
            thumby.display.drawSprite(lineSprite2)
    thumby.display.update()
