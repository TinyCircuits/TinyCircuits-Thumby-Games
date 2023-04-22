### DiscDungeon
## by PossiblyAxolotl
# https://possiblyaxolotl.itch.io

import thumby
import math
import random

thumby.saveData.setName("Disc Dungeon")
thumby.display.setFPS(60)

### GAME

# art
# sawMap: width: 16, height: 8
sawMap = bytearray([85,254,127,230,103,254,127,170,170,127,254,103,230,127,254,85])
# targetMap: width: 8, height: 8
targetMap = bytearray([126,129,189,165,165,189,129,126])
# playerMap: width: 8, height: 4
playerMap = bytearray([5,5,5,13,13,5,5,5])
sprPlayer = thumby.Sprite(4,4,playerMap,thumby.display.width/2-1,thumby.display.height/2-1)
sprPlayer.speed = 1

saws = []
targets = []
particles = []

score = 0
scoreY, scoreYlerp = -10, 3

thumby.display.setFont("/Games/DiscDungeon/numberFont.bin", 3, 5, 1)

frame = 0
loop = 0
looptime = 300

tarCountdown = random.randint(5, 15)

speed = 0.2
#amnt = 1

mode = 0 # 0=menu, 1=game

def lerp(a, b, t):
    return (1 - t) * a + t * b

def die():
    global mode, saws, targets
    thumby.audio.play(200,200)
    thumby.saveData.setItem("lastScore", score)
    if thumby.saveData.hasItem("highScore"):
        if thumby.saveData.getItem("highScore") < score:
            thumby.saveData.setItem("highScore", score)
    else:
        thumby.saveData.setItem("highScore", score)
    thumby.saveData.save()
    screenBurst()
    #for saw in saws:
    #    addParts(saw.x,saw.y,6)
    saws = []
    #for tar in targets:
    #    addParts(tar.x,tar.y,4)
    targets = []
    mode = 0
    #thumby.reset()

def screenBurst():
    for i in range(0, 20):
        direction = math.radians(random.randint(0, 359))
        part = [random.randint(0,thumby.display.width),random.randint(0,thumby.display.height),random.randint(1,6),math.sin(direction),-math.cos(direction)]
        particles.append(part)
        
def addParts(_x,_y, amount): # 0=x,1=y,2=size,3=dirx,4=diry
    for i in range(0, amount):
        direction = math.radians(random.randint(0, 359))
        part = [_x,_y,random.randint(1,6),math.sin(direction),-math.cos(direction)]
        particles.append(part)

def drawParticles():
    for part in particles:
        #if frame % 2 == 0:
        thumby.display.drawFilledRectangle(round(part[0]),round(part[1]),math.ceil(part[2]),math.ceil(part[2]),1)
        part[0] += part[3]
        part[1] += part[4]
        
        part[2] -= 0.2
        if part[2] <= 0:
            particles.remove(part)

def addSaws(amount):
    for i in range(0, amount):
        sprSaw = thumby.Sprite(8,8,sawMap,random.randint(2,thumby.display.width-10),random.randint(2,thumby.display.height-10))
        sprSaw.dir = math.radians(random.randint(0,359))
        sprSaw.aniCounter = random.randint(0,2)
        sprSaw.setFrame(random.randint(0,1))
        sprSaw.speed = speed
        sprSaw.lifespan = random.randint(5,20)
        sprSaw.active = 0
        sprSaw.xdir = math.sin(sprSaw.dir)
        sprSaw.ydir = math.cos(sprSaw.dir)
        saws.append(sprSaw)
        addParts(sprSaw.x,sprSaw.y,8)

def spawnTarget():
    sprTar = thumby.Sprite(8,8,targetMap,random.randint(2,thumby.display.width-10),random.randint(2,thumby.display.height-10))
    sprTar.lifespan = 600
    targets.append(sprTar)
    addParts(sprTar.x,sprTar.y,4)
    
def updateSaws():
    for saw in saws:
        # lifespan
        if saw.lifespan < 0:
            global scoreY
            global score
            #scoreY -= 2
            #score += 1
            addParts(saw.x,saw.y, 3)
            saws.remove(saw)
            continue
        
        # move in direction
        saw.x += saw.speed * saw.xdir
        saw.y -= saw.speed * saw.ydir
        
        # collide with walls
        if saw.x < 1: 
            saw.xdir *= -1
            saw.x = 1
            saw.lifespan -= 1
            thumby.audio.play(200,20)
        elif saw.x > thumby.display.width-8: 
            saw.xdir *= -1
            saw.lifespan -= 1
            saw.x = thumby.display.width-8
            thumby.audio.play(200,20)
        if saw.y < 1: 
            saw.ydir *= -1
            saw.y = 1
            saw.lifespan -= 1
            thumby.audio.play(200,20)
        elif saw.y > thumby.display.height-8: 
            saw.ydir *= -1
            saw.y = thumby.display.height-8
            saw.lifespan -= 1
            thumby.audio.play(200,20)
        
        # animate
        saw.aniCounter += 1
        if saw.aniCounter > 3:
            saw.setFrame(saw.getFrame()+1)
            saw.aniCounter = 0

        if saw.active < 60: # if inactive then add to active timer
            saw.active += 1
        # player death
        elif saw.x-2 <= math.floor(sprPlayer.x) and saw.x + 7 >= math.ceil(sprPlayer.x) and saw.y-2 <= math.floor(sprPlayer.y) and saw.y + 7 >= math.ceil(sprPlayer.y):
            die()

        # draw
        thumby.display.drawSprite(saw)

def updateTargets():
    for tar in targets:
        tar.lifespan -= 1
        if tar.lifespan <= 0:
            targets.remove(tar)
            continue
        if tar.x-2 <= math.floor(sprPlayer.x) and tar.x + 7 >= math.ceil(sprPlayer.x) and tar.y-2 <= math.floor(sprPlayer.y) and tar.y + 7 >= math.ceil(sprPlayer.y):
            global score
            score += 10
            thumby.audio.play(300,100)
            targets.remove(tar)
            addParts(tar.x,tar.y,2)
        
        if frame % 2 == 0:
            thumby.display.drawSprite(tar)

#addSaws(1)
    
def processGame():
    global frame, loop, looptime, tarCountdown, scoreY, scoreYlerp, score, speed
    thumby.display.fill(0)
    
    # Input
    if thumby.actionPressed():
        sprPlayer.speed = 0.5
    else:
        sprPlayer.speed = 1
        
    if thumby.buttonU.pressed():
        sprPlayer.y -= sprPlayer.speed
    elif thumby.buttonD.pressed():
        sprPlayer.y += sprPlayer.speed
    if thumby.buttonL.pressed():
        sprPlayer.x -= sprPlayer.speed
    elif thumby.buttonR.pressed():
        sprPlayer.x += sprPlayer.speed
        
    # Bounds
    if sprPlayer.x < 2: sprPlayer.x = 2
    if sprPlayer.x > thumby.display.width-6: sprPlayer.x = thumby.display.width-6
    if sprPlayer.y < 2: sprPlayer.y = 2
    if sprPlayer.y > thumby.display.height-6: sprPlayer.y = thumby.display.height-6
    
    # Score
    if sprPlayer.y < 10 and sprPlayer.x < 3 + 4*len(str(score)): 
        scoreYlerp = -10 
    else: 
        scoreYlerp = 3
    
    if frame >= 60:
        frame = 0
        score += 1
        scoreY -= 2
        speed += 0.01
        looptime -= 1
        #amnt += 0.02
        #if amnt > 3: amnt = 5
        if looptime < 30: looptime = 30
        if speed > 1: speed = 1
        tarCountdown -= 1
    if loop >= looptime:
        loop = 0
        addSaws(1)
    if tarCountdown <= 0:
        tarCountdown = random.randint(5, 15)
        spawnTarget()
    
    scoreY = lerp(scoreY,scoreYlerp,0.1)
    
    # Drawing
    if frame % 3 ==0:
        sprPlayer.setFrame(sprPlayer.getFrame()+1)
    updateTargets()
    updateSaws()
    drawParticles()
    
    thumby.display.drawSprite(sprPlayer)
    
    #if frame %2 == 1:
    thumby.display.drawRectangle(0,0,thumby.display.width, thumby.display.height, 1)
    
    thumby.display.drawText(str(score),3,round(scoreY),1)
    
    frame += 1
    loop += 1

### MENU
# Art
# logoMap: width: 59, height: 18
logoMap = bytearray([0,0,0,0,0,0,0,0,0,0,0,0,0,255,255,131,131,199,255,254,0,0,131,131,243,255,159,131,131,0,0,206,223,155,187,179,247,230,0,0,254,255,131,131,131,199,198,0,0,0,0,0,0,0,0,0,0,0,0,
           168,240,248,176,248,240,168,0,0,248,8,8,8,241,1,249,1,1,1,248,0,248,49,65,129,249,1,241,9,8,136,144,1,249,73,73,9,8,0,240,8,9,9,241,1,249,48,64,128,248,0,0,168,240,248,176,248,240,168,
           2,1,3,1,3,1,2,0,0,3,2,2,2,1,0,1,2,2,2,1,0,3,0,0,1,3,0,1,2,2,2,1,0,3,2,2,2,2,0,1,2,2,2,1,0,3,0,0,1,3,0,0,2,1,3,1,3,1,2])
# cursorMap: width: 1, height: 3
cursorMap = bytearray([15])
# ctrlMap: width: 25, height: 15
#ctrlMap = bytearray([60,12,60,0,60,36,60,0,28,32,28,0,60,44,36,0,0,60,36,231,129,129,231,36,60,
#           0,0,44,52,0,60,32,0,60,36,60,0,60,48,60,0,0,48,72,72,48,12,18,18,12])
# playMap: width: 15, height: 4
playMap = bytearray([15,5,7,0,15,8,8,0,15,5,15,0,3,14,3])
# soundMap: width: 25, height: 4
soundMap = bytearray([11,13,0,15,9,15,0,15,8,15,0,15,1,15,0,15,9,6,0,6,15,0,9,6,0,11,13,0,15,9,15,0,15,8,15,0,15,1,15,0,15,9,6,0,6,15,0,9,6,9])
# plusMap: width: 6, height: 6
#plusMap = bytearray([12,12,63,63,12,12])
# scoreMap: width: 21, height: 4
scoreMap = bytearray([15,8,0,15,5,15,0,1,15,1,0,15,11,9,0,11,13,0,1,15,1,0,0,0,15,4,15,0,9,15,9,0,15,9,13,0,15,4,15,0,0,0])

sprLogo = thumby.Sprite(59,18,logoMap,thumby.display.width/2-29,2)
sprSound = thumby.Sprite(25,4,soundMap,3,33)
sprPlay = thumby.Sprite(15,4,playMap,3,26)
sprCursor = thumby.Sprite(1,4,cursorMap,1,26)
sprScore = thumby.Sprite(21,4,scoreMap,thumby.display.width-24, 26)

cursorSel = 0

# set audio sprite up
thumby.audio.setEnabled(0)
sprSound.setFrame(1)

def processMenu():
    global cursorSel, frame, score, loop, looptime, tarCountdown, speed, mode
    thumby.display.fill(0)
    thumby.display.drawSprite(sprLogo)
    thumby.display.drawSprite(sprSound)
    thumby.display.drawSprite(sprPlay)
    thumby.display.drawSprite(sprCursor)
    thumby.display.drawSprite(sprScore)
    
    if cursorSel == 0:
        sprPlay.x = lerp(sprPlay.x, 5, 0.2)
        sprSound.x = lerp(sprSound.x, 3, 0.2)
    else:
        sprPlay.x = lerp(sprPlay.x, 3, 0.2)
        sprSound.x = lerp(sprSound.x, 5, 0.2)
    
    if thumby.buttonU.justPressed() or thumby.buttonD.justPressed():
        thumby.audio.play(250,30)
        cursorSel+=1
        sprScore.setFrame(sprScore.getFrame() + 1)
        if cursorSel > 1: cursorSel = 0
        sprScore.x = thumby.display.width-24+(3*cursorSel)
    
    if thumby.actionJustPressed():
        if cursorSel == 1:
            thumby.audio.setEnabled(sprSound.getFrame())
            sprSound.setFrame(sprSound.getFrame()+1)
        else:
            score = 0
            frame = 0
            loop = 0
            looptime = 300

            tarCountdown = random.randint(5, 15)

            speed = 0.2
            mode = 1
            sprPlayer.x = thumby.display.width/2-1
            sprPlayer.y = thumby.display.height/2-1
            
            addSaws(1)
            screenBurst()
        thumby.audio.play(300,50)
    
    if cursorSel == 1:
        if thumby.saveData.hasItem("highScore"):
            thumby.display.drawText(str(thumby.saveData.getItem("highScore")), 70-4*len(str(thumby.saveData.getItem("highScore"))), 33,1)
    else:
        if thumby.saveData.hasItem("lastScore"):
            thumby.display.drawText(str(thumby.saveData.getItem("lastScore")), 70-4*len(str(thumby.saveData.getItem("lastScore"))), 33,1)   
    sprCursor.y = lerp(sprCursor.y, 26 + 8*cursorSel, 0.1)
    #thumby.display.drawSprite(sprPlus)
    
    drawParticles()

while True:
    if mode == 1:
        processGame()
    else:
        processMenu()
    
    thumby.display.update() 