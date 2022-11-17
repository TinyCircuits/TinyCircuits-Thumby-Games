#HEMLOCKMAY on discord saved this game! This game would not exist without him
#By Anthony
import time
import thumby
import math
import random
import machine
from machine import freq
machine.freq(100000000)
thumby.display.setFont("/lib/font5x7.bin", 5, 7, 1)

TitleScreen = thumby.Sprite(72,40,bytearray([28,140,236,252,124,62,63,63,31,159,255,255,255,243,241,248,252,254,255,255,239,223,31,63,62,60,124,120,120,48,0,0,0,0,254,18,18,12,0,0,232,0,0,96,144,144,0,0,96,144,144,96,0,0,32,32,32,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,
           254,255,255,255,254,30,30,255,191,223,223,255,239,143,15,7,7,7,3,15,25,63,63,126,124,120,120,248,176,128,192,192,192,0,132,252,132,0,240,32,16,16,224,0,16,96,128,96,16,0,96,144,144,248,0,96,144,144,252,0,96,176,176,32,0,240,16,32,0,160,176,80,
           0,3,31,63,63,126,56,0,225,225,255,255,127,127,15,128,192,192,224,240,248,248,252,252,254,255,63,31,143,135,195,227,241,248,254,254,254,0,124,18,18,18,124,0,0,0,36,0,0,0,126,18,18,12,0,126,64,0,0,48,72,72,124,0,0,8,176,64,48,8,0,0,
           0,0,0,0,0,0,0,0,0,0,224,248,252,254,255,255,63,31,143,135,195,241,249,253,255,255,255,255,255,255,191,159,207,199,195,255,253,124,127,63,0,0,32,224,192,128,128,0,0,0,0,0,0,0,1,15,31,31,62,120,115,103,239,223,184,122,121,24,8,0,0,0,
           0,0,0,0,0,0,0,0,0,0,0,3,7,15,15,15,15,15,15,255,247,247,247,255,7,5,5,6,6,7,7,7,7,7,3,3,1,0,0,0,0,0,0,0,0,1,1,3,2,2,0,28,28,46,102,252,252,248,240,240,224,224,64,48,248,252,254,254,254,126,143,240])+bytearray([28,140,236,252,124,62,63,63,31,159,255,255,255,243,241,248,252,254,255,255,239,223,31,63,62,60,124,120,120,48,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,
           254,255,255,255,254,30,30,255,191,223,223,255,239,143,15,7,7,7,3,15,25,63,63,126,124,120,120,248,176,128,192,192,192,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,
           0,3,31,63,63,126,56,0,225,225,255,255,127,127,15,128,192,192,224,240,248,248,252,252,254,255,63,31,143,135,195,227,241,248,254,254,254,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,
           0,0,0,0,0,0,0,0,0,0,224,248,252,254,255,255,63,31,143,135,195,241,249,253,255,255,255,255,255,255,191,159,207,199,195,255,253,124,127,63,0,0,32,224,192,128,128,0,0,0,0,0,0,0,1,15,31,31,62,120,115,103,239,223,184,120,120,24,8,0,0,0,
           0,0,0,0,0,0,0,0,0,0,0,3,7,15,15,15,15,15,15,255,247,247,247,255,7,5,5,6,6,7,7,7,7,7,3,3,1,0,0,0,0,0,0,0,0,1,1,3,2,2,0,28,28,46,102,252,252,248,240,240,224,224,64,48,248,252,254,254,254,126,143,240]))
while(1):
    thumby.display.drawSprite(TitleScreen)
    TitleScreen.setFrame(TitleScreen.currentFrame+1)
    thumby.display.update()
    if thumby.buttonA.pressed():
        break
Cannon = thumby.Sprite(7,5,bytearray([24,28,28,31,28,28,24]))
Laser = thumby.Sprite(1,4,bytearray([15]))
AlienBitmap = (bytearray([128,88,180,94,94,180,88,128,0,88,180,62,62,180,88,0]),
        bytearray([156,121,54,60,60,54,121,156,112,57,118,188,188,118,57,112]),
        bytearray([156,84,118,190,190,118,84,156,92,244,54,94,94,54,244,92]))
Cannons = thumby.Sprite(12,2,bytearray([0,0,0,0,0,0,0,0,0,0,0,0])+bytearray([2,3,2,0,0,0,0,0,0,0,0,0])+bytearray([2,3,2,0,2,3,2,0,0,0,0,0])+bytearray([2,3,2,0,2,3,2,0,2,3,2,0]))
SpaceShip = thumby.Sprite(12,6,bytearray([8,28,58,30,11,31,31,11,30,58,28,8]))
Sheild1 = thumby.Sprite(10,5,bytearray([30,31,31,15,7,7,15,31,31,30]),6,29)
Sheild2 = thumby.Sprite(10,5,bytearray([30,31,31,15,7,7,15,31,31,30]),22,29)
Sheild3 = thumby.Sprite(10,5,bytearray([30,31,31,15,7,7,15,31,31,30]),39,29)
Sheild4 = thumby.Sprite(10,5,bytearray([30,31,31,15,7,7,15,31,31,30]),55,29)
SpaceShip.x = -12
Cannons.y = 38
multiplier = 1
Sheilds = []
Score = 0
Lives = 3
Aliens = []
Lasers = []
AlienSpeed = .0125
Dir = 1
Frame = 0
LaserSpeed = 0
s = 0
Laser.y = 1000
Cannon.y = 35
Cannon.x = 29
Collision = 0
def createSheild():
    Sheilds.append([[0,1,1,1,1,1,1,1,1,0],
                    [1,1,1,1,1,1,1,1,1,1],
                    [1,1,1,1,1,1,1,1,1,1],
                    [1,1,1,1,0,0,1,1,1,1],
                    [1,1,1,0,0,0,0,1,1,1]])
def AABB(objCoords, miscCoords):
    #((xL,xR),(yU,yD)),((xL,xR),(yU,yD))
    if miscCoords[0][1] > objCoords[0][0] and miscCoords[0][0] < objCoords[0][1] and miscCoords[1][1] > objCoords[1][0] and miscCoords[1][0] < objCoords[1][1]:
        return True
    else:
        return False
def createLaser():
    Lasers.append(thumby.Sprite(2,4,bytearray([10,5])+bytearray([5,10])))
    Lasers[len(Lasers)-1].y = 1000
def shootLaser(Invader):
    if Lasers[Aliens.index(Invader)].y > 36:
        Lasers[Aliens.index(Invader)].x = Aliens[Aliens.index(Invader)].x+3
        Lasers[Aliens.index(Invader)].y = Aliens[Aliens.index(Invader)].y
def LaserOperations():
    global Lives
    global LaserCol
    global Collision
    for i in Lasers:
        i.setFrame(i.currentFrame+1)
    for i in Lasers:
        i.y += .9
        if AABB(((i.x,i.x+2),(i.y,i.y+4)),((Cannon.x,Cannon.x+7),(Cannon.y,Cannon.y+5))):
            LaserCol = 1
            Lives -= 1
            Cannon.x = 29
            thumby.audio.playBlocking(138, 100)
            thumby.audio.playBlocking(138, 100)
            thumby.audio.playBlocking(138, 100)
            time.sleep(2)
        if AABB(((Laser.x,Laser.x+1),(Laser.y,Laser.y+4)),((i.x-1,i.x+3),(i.y,i.y+4))):
            LaserCol = 1
            thumby.audio.play(130, 50)
            Collision = 1
        if i.y > 36:
            LaserCol = 1
        if i.y < 36 and i.y+4 > 29:
            index = 0
            for s in Sheilds:
                x = 0
                y = 29
                for ind in s:
                    x = int(6.4*(index+1)+index*10)
                    for inde in ind:
                        if x == int(i.x) and y == int(i.y+4) and inde:
                            Sheilds[index][y-29][x-int(6.4*(index+1)+index*10)] = 0
                            LaserCol = 1
                        x += 1
                    y += 1
                index += 1
        if LaserCol:
            i.y = 1000
            LaserCol = 0
        thumby.display.drawSprite(i)

def SheildOperations():
    global Collision
    global LaserCol
    index = 0
    for i in Sheilds:
        x = 0
        y = 29
        for ind in i:
            x = int(6.4*(index+1)+index*10)
            for inde in ind:
                if not inde:
                    thumby.display.setPixel(x, y, inde)
                if x == int(Laser.x) and y == int(Laser.y) and inde:
                    Sheilds[index][y-29][x-int(6.4*(index+1)+index*10)] = 0
                    Collision = 1
                x += 1
            y += 1
        index += 1
def createInvader(type):
    Aliens.append(thumby.Sprite(8,8,AlienBitmap[type-1]))
    Aliens[len(Aliens)-1].x += 9*(len(Aliens)%6)-1
    Aliens[len(Aliens)-1].y += 8*(math.ceil(len(Aliens)/6)-1)
    createLaser()

def AlienOperations():
    global Dir
    global Frame
    global AlienSpeed
    global Collision
    global Score
    global multiplier
    global Lives
    thumby.display.fill(0)
    for i in Aliens:
        i.setFrame(int(Frame))
    Frame += len(Aliens)*(AlienSpeed/16)
    LaserOperations()
    for i in Aliens:
        if i.x > 64 and Dir == 1:
            Dir = -1
            for i in Aliens:
                i.y += 1
        if i.x < 0 and Dir == -1:
            Dir = 1
            for i in Aliens:
                i.y += 1
        if random.randint(0,350) == 1:
            thumby.audio.play(329, 100)
            shootLaser(i)
        if int(Cannon.x) in range(int(i.x-4),int(i.x+12)) and random.randint(0,75) == 16:
            thumby.audio.play(329, 100)
            shootLaser(i)
        i.x += Dir*AlienSpeed
        thumby.display.drawSprite(i)
        if i.y > 30:
            Lives -= 1
            Cannon.x = 29
            thumby.audio.playBlocking(138, 100)
            thumby.audio.playBlocking(138, 100)
            thumby.audio.playBlocking(138, 100)
            time.sleep(2)
            Aliens.remove(i)
        if AABB(((i.x,i.x+8),(i.y,i.y+8)),((Laser.x,Laser.x),(Laser.y,Laser.y))):
            Collision = 1
            Lasers.remove(Lasers[Aliens.index(i)])
            Aliens.remove(i)
            Score += 1
            AlienSpeed += .0375*multiplier
            if len(Aliens) == 2:
                AlienSpeed = 1.25*multiplier
                break
            if len(Aliens) == 1:
                AlienSpeed = 1.5*multiplier
                break
        thumby.display.drawSprite(Cannon)
def SpaceShipScript():
    global SpaceShip
    if random.randint(0,550) == 1 and SpaceShip.x == -12:
        SpaceShip.x = 0
    if AABB(((Laser.x,Laser.x),(Laser.y,Laser.y)),((SpaceShip.x,SpaceShip.x+12),(SpaceShip.y,SpaceShip.y+6))):
        SpaceShip.x = -12
    if SpaceShip.x > 72:
        SpaceShip.x = -12
    if not SpaceShip.x == -12:
        SpaceShip.x += .9
for i in range(4):
    createSheild()
for i in range(6):
    createInvader(1)
for i in range(6):
    createInvader(2)
for i in range(6):
    createInvader(3)

while(1):
    thumby.display.fill(0)
    if thumby.buttonR.pressed() and Cannon.x < 65:
        Cannon.x += 1
    if thumby.buttonL.pressed() and Cannon.x > 0:
        Cannon.x -= 1
    if Laser.y > 0 and Laser.y < 40 and not Collision:
        Laser.y -= LaserSpeed
        thumby.audio.play(s, 100)
        s += 4
        if AABB(((Laser.x,Laser.x),(Laser.y,Laser.y)),((SpaceShip.x,SpaceShip.x+12),(SpaceShip.y,SpaceShip.y+6))):
            Collision = 1
            s = 207
            while(1):
                thumby.audio.play(s,100)
                s += 1
                if s == 261:
                    break
            Score += 5
    else:
        Collision = 0
        LaserSpeed = 0
        Laser.y = 1000000
        if thumby.buttonA.pressed():
            s = 391
            Laser.x = Cannon.x+3
            Laser.y = 34
            LaserSpeed = 1
    AlienOperations()
    thumby.display.drawSprite(Sheild1)
    thumby.display.drawSprite(Sheild2)
    thumby.display.drawSprite(Sheild3)
    thumby.display.drawSprite(Sheild4)
    SheildOperations()
    if Lives == -1:
        while (1):
            thumby.display.fill(0)
            thumby.display.drawText('Game Over!',6,0,1)
            thumby.display.drawText('A:Play Again',0,14,1)
            thumby.display.drawText('B:Quit',0,28,1)
            thumby.display.update()
            if thumby.buttonA.pressed():
                SpaceShip.x = -12
                Cannons.y = 38
                multiplier = 1
                Sheilds = []
                Score = 0
                Lives = 3
                Aliens = []
                Lasers = []
                AlienSpeed = .0125
                Dir = 1
                Frame = 0
                LaserSpeed = 0
                s = 0
                Laser.y = 1000
                Cannon.y = 35
                Cannon.x = 29
                Collision = 0
                for i in range(4):
                    createSheild()
                for i in range(6):
                    createInvader(1)
                for i in range(6):
                    createInvader(2)
                for i in range(6):
                    createInvader(3)
                break
            if thumby.buttonB.pressed():
                thumby.reset()
    if len(Aliens) == 0:
        Cannons.y = 38
        Sheilds = []
        multiplier += .0625
        Score += 10
        Aliens = []
        Lasers = []
        AlienSpeed = .0125*multiplier
        Dir = 1
        Frame = 0
        LaserSpeed = 0
        s = 0
        Laser.y = 1000
        Cannon.y = 35
        Cannon.x = 29
        Collision = 0
        for i in range(4):
            createSheild()
        for i in range(6):
            createInvader(1)
        for i in range(6):
            createInvader(2)
        for i in range(6):
            createInvader(3)
    
    SpaceShipScript()
    thumby.display.drawText(str(Score),72-len(str(Score))*6,33,1)
    Cannons.setFrame(Lives)
    thumby.display.drawSprite(SpaceShip)
    thumby.display.drawSprite(Cannons)
    thumby.display.drawSprite(Cannon)
    thumby.display.drawSprite(Laser)
    thumby.display.update()