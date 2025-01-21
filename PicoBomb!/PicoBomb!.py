#Created by Anthony! Hi Carson!
import time
import thumby
import math
import random
thumby.display.setFont("/lib/font5x7.bin", 5, 7, 1)
#((xL,xR),(yU,yD)),((xL,xR),(yU,yD))
Water = thumby.Sprite(7,4,bytearray([14,9,15,9,15,9,14])+bytearray([14,8,14,8,14,8,14]))
MadBomber = thumby.Sprite(8,12,bytearray([255,69,44,36,36,44,69,255,12,12,9,1,1,9,12,12]))
TitleScreen = thumby.Sprite(72,40,bytearray([255,131,0,0,0,0,0,0,0,0,0,0,0,0,192,224,240,224,228,198,142,158,62,126,252,252,252,248,248,224,0,0,0,254,18,18,12,0,0,232,0,0,96,144,144,0,0,96,144,144,96,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,
           255,255,255,255,255,254,254,254,252,252,252,120,120,127,240,193,131,7,15,31,27,49,51,62,188,109,41,15,15,7,6,4,12,0,0,0,0,0,0,0,0,0,0,0,0,254,146,146,108,0,0,96,144,144,96,0,0,240,32,16,224,16,224,0,0,254,144,144,96,0,190,0,
           0,0,1,1,3,195,211,63,127,115,249,229,192,128,129,3,3,215,7,175,254,254,255,253,248,248,240,224,224,192,128,0,0,0,252,18,18,252,0,0,72,0,0,254,18,18,12,0,0,254,0,0,96,144,144,248,0,0,24,32,192,32,24,0,128,128,192,192,96,96,96,192,
           0,0,64,40,248,127,28,191,56,122,240,241,225,227,231,207,199,191,231,2,0,1,1,3,7,15,15,31,31,63,127,127,254,252,124,56,16,16,16,16,48,192,0,0,2,2,12,56,96,192,128,0,0,0,0,0,0,0,242,249,252,142,7,3,33,49,156,4,130,194,4,8,
           0,0,125,255,127,6,14,15,30,28,28,29,57,57,59,59,127,255,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,1,1,1,1,1,1,1,0,0,0,0,0,15,31,127,125,125,121,57,62,0,0,6,15,25,49,99,131,135,14,28,25,57,113,96,64,198])+bytearray([255,131,0,0,0,0,0,0,0,0,0,0,0,0,192,224,240,224,228,198,142,158,62,126,252,252,252,248,248,224,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,
           255,255,255,255,255,254,254,254,252,252,252,120,120,127,240,193,131,7,15,31,27,49,51,62,188,109,41,15,15,7,6,4,12,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,
           0,0,1,1,3,195,211,63,127,115,249,229,192,128,129,3,3,215,7,175,254,254,255,253,248,248,240,224,224,192,128,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,128,128,192,192,96,96,96,192,
           0,0,64,40,248,127,28,191,56,122,240,241,225,227,231,207,199,191,231,2,0,1,1,3,7,15,15,31,31,63,127,127,254,252,124,56,16,16,16,16,48,192,0,0,2,2,12,56,96,192,128,0,0,0,0,0,0,0,240,248,252,142,7,3,33,49,156,4,130,194,4,8,
           0,0,125,255,127,6,14,15,30,28,28,29,57,57,59,59,127,255,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,1,1,1,1,1,1,1,0,0,0,0,0,15,31,127,125,125,121,57,62,0,0,6,15,25,49,99,131,135,14,28,25,57,113,96,64,198]))
while (1):
    thumby.display.drawSprite(TitleScreen)
    thumby.display.update()
    TitleScreen.setFrame(TitleScreen.currentFrame+1)
    if thumby.buttonA.pressed():
        break
Lives = 3
Score = 0
Bombs = []
BombSpeed = .75
MadBomber.x = 32
Water.y = 36
Water.x = 32
BombsDropped = 0
roundd = 0
pos = 0
wave = 0
BombExplode = 0
s = 0

thumby.display.setFPS(60)

def AABB(objCoords, miscCoords):
    if miscCoords[0][1] > objCoords[0][0] and miscCoords[0][0] < objCoords[0][1] and miscCoords[1][1] > objCoords[1][0] and miscCoords[1][0] < objCoords[1][1]:
        return True
    else:
        return False
  
def Wav():
    global wave, Score, BombsDropped, BombSpeed, roundd
    if BombsDropped%25 == 0 and BombsDropped > 0 and roundd:
        wave += 1
        BombsDropped += 1
        BombSpeed = .75+wave*.125
        roundd = 0
    if thumby.buttonA.pressed():
        roundd = 1

def createbomb():
    Bombs.append(thumby.Sprite(4,4,bytearray([0,12,14,1])+bytearray([2,14,7,9])+bytearray([11,6,5,10])))
    Bombs[len(Bombs)-1].y = 1000
    thumby.display.drawSprite(Bombs[len(Bombs)-1])
    thumby.display.update()

def dropbomb(bomb):
    global BombsDropped
    BombsDropped += 1
    if not bomb.y < 36:
        bomb.y = MadBomber.y+10
        bomb.x = MadBomber.x+2

def defused():
    global Bombs, Score, MadBomber, BombSpeed, Water, Lives
    for i in Bombs:
        if AABB(((Water.x,Water.x+7),(Water.y-4,Water.y)),((i.x,i.x+4),(i.y-4,i.y))):
            if Score%25 == 0 and not Score == 0:
                s = 130
                while (1):
                    thumby.audio.playBlocking(s, 50)
                    s += 1
                    if s == 174:
                        break
                Score += 5
            thumby.audio.play(261, 100)
            i.y = 1000
            i.x = MadBomber.x+2
            Score += 1
            thumby.display.drawSprite(i)
        elif i.y-2 > 36 and i.y-2 < 100:
            i.y = 1000
            for i in range(3):
                thumby.audio.playBlocking(138, 100)
            explodeBomb()
            MadBomber.x = 32
            Water.x = 32
            BombSpeed -= .0625
            Score -= 1
            if Score < 0:
                Score += 1
            Lives -= 1

def explodeBomb():
    global Lives
    BombExplode = 1
    for i in range(2):
        for i in Bombs:
            i.setFrame(i.currentFrame+1)
            thumby.display.drawSprite(MadBomber)
            thumby.display.drawSprite(i)
            thumby.display.update()
    for i in Bombs:
        i.setFrame(0)
        thumby.display.drawSprite(i)
        thumby.display.update()
    BombExplode = 0

def MadBomberScript():
    global pos, MadBomber
    if roundd:
        if MadBomber.x == pos:
            pos = random.randint(0,64)
        if pos > MadBomber.x:
            MadBomber.x += 1
        elif MadBomber.x > pos:
            MadBomber.x -= 1
    else:
        if 32 > MadBomber.x:
            MadBomber.x += 1
        elif MadBomber.x > 32:
            MadBomber.x -= 1

def operations():
    global BombExplode
    for i in Bombs:
        if not BombExplode:
            i.y += .25*BombSpeed
        if random.randint(0,450) == 44 and roundd:
            dropbomb(i)
        thumby.display.drawSprite(i)
    MadBomberScript()
    defused()
for i in range(30):
    createbomb()

while(1):
    thumby.display.fill(1)
    thumby.display.drawFilledRectangle(0, 10, 72, 30, 0)
    if thumby.buttonR.pressed() and Water.x < 65:
        Water.x += 2*BombSpeed
    if thumby.buttonL.pressed() and Water.x > 0:
        Water.x -= 2*BombSpeed
    operations()
    Wav()
    Water.setFrame(Water.currentFrame+1)
    if Lives == 0:
        while (1):
            thumby.display.fill(0)
            thumby.display.drawText('Game Over!',6,0,1)
            thumby.display.drawText('A:Play Again',0,14,1)
            thumby.display.drawText('B:Quit',0,28,1)
            thumby.display.update()
            if thumby.buttonA.pressed():
                Lives = 3
                Score = 0
                BombSpeed = .75
                MadBomber.x = 32
                Water.y = 36
                Water.x = 32
                BombsDropped = 0
                roundd = 0
                pos = 0
                wave = 0
                BombExplode = 0
                s = 0
                for i in Bombs:
                    i.y = 1000
                time.sleep(.5)
                break
            if thumby.buttonB.pressed():
                thumby.reset()
    thumby.display.drawText(str(Lives),0,0,0)
    thumby.display.drawText(str(Score), 72-(6*len(str(Score))), 0, 0)
    thumby.display.drawSprite(Water)
    thumby.display.drawSprite(MadBomber)
    thumby.display.update()

