import time
import thumby
import math
import random

# Welcome to this very simple game
# Apologies for this mess, I'm getting the hang of it :)
# Thanks to all the people that have created games in the arcade because I wouldn't have known where to start without those programs 
# Regardless of my mess, I hope this code can be of use to anyone
# Espero mi jueguito pedorro les parezca al menos algo entretenido
# Que tengan un bonito 2024 y que encuentren lo que buscan este anio :D - Natalia


# BITMAPS: width: 11, height: 11
bombMap = bytearray([0,224,240,248,248,252,234,217,176,224,0,0,1,3,7,7,7,7,7,3,1,0])
heartMap = bytearray([28,62,127,255,254,252,254,255,127,62,28,0,0,0,0,1,3,1,0,0,0,0])
starMap = bytearray([24,40,200,12,50,1,50,12,200,40,24,0,3,4,3,1,1,1,3,4,3,0])
           
# BITMAPS: width: 60, height: 18
starBoxMap = bytearray([0,0,0,0,224,112,88,76,70,67,65,65,65,65,65,65,65,65,65,65,65,65,65,65,65,65,65,65,65,65,225,49,25,13,255,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,
           0,0,0,0,255,0,0,0,0,0,0,0,0,102,205,137,137,219,114,0,0,0,0,0,0,0,0,0,0,0,255,0,128,192,127,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,
           0,0,0,0,3,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,3,3,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0])          
heartBoxMap = bytearray([0,0,0,0,224,112,88,76,70,67,65,65,65,65,65,65,65,65,65,65,65,65,65,65,65,65,65,65,65,65,225,49,25,13,255,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,
           0,0,0,0,255,0,0,0,0,0,0,0,0,0,0,255,8,8,8,255,0,0,0,0,0,0,0,0,0,0,255,0,128,192,127,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,
           0,0,0,0,3,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,3,3,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0])

# BITMAP: width: 40, height: 40 
explosion0 = bytearray([0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,
           0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,
           0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,24,60,60,24,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,
           0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,
           0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0])
explosion1 = bytearray([0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,
           0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,
           0,0,0,0,0,0,0,0,0,0,0,0,0,0,32,144,18,232,57,124,188,216,5,32,140,38,0,0,0,0,0,0,0,0,0,0,0,0,0,0,
           0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,
           0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0])
explosion2 = bytearray([0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,
            0,0,0,0,0,0,0,0,0,0,0,0,0,32,0,0,48,24,0,0,8,0,32,0,80,0,32,16,0,0,0,0,0,0,0,0,0,0,0,0,
            0,0,0,0,0,0,0,0,0,0,32,16,1,6,44,144,18,232,9,64,128,192,5,32,140,46,28,20,225,4,0,0,0,0,0,0,0,0,0,0,
            0,0,0,0,0,0,0,0,0,0,0,0,5,2,8,2,4,0,16,1,4,8,16,0,0,4,0,9,2,0,0,0,0,0,0,0,0,0,0,0,
            0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0])
explosion3 = bytearray([0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,128,0,0,0,64,48,160,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,
            0,0,0,0,0,0,0,24,32,4,8,3,8,16,24,0,49,24,0,0,0,0,32,0,80,2,32,18,0,12,32,128,0,0,0,0,0,0,0,0,
            0,0,0,0,0,8,0,170,0,48,0,0,1,6,44,144,0,128,0,0,0,0,1,0,128,42,28,20,225,4,0,129,2,16,128,0,0,0,0,0,
            0,0,0,0,0,0,2,4,0,16,128,0,5,130,72,2,4,64,0,128,64,8,0,128,24,4,0,1,0,32,64,8,0,0,2,0,0,0,0,0,
            0,0,0,0,0,0,0,0,0,1,1,0,0,0,0,0,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0])
explosion4 = bytearray([0,0,0,0,0,0,0,128,32,64,0,0,32,16,0,0,0,128,8,0,0,64,16,160,0,0,32,0,64,0,0,0,0,128,0,0,0,0,0,0,
            0,0,0,132,0,0,2,24,32,4,8,3,8,16,8,0,1,0,0,0,0,0,0,0,16,2,32,18,0,4,32,130,1,36,0,128,0,0,0,0,
            0,8,0,0,128,8,0,170,0,48,0,0,0,4,0,128,0,0,0,0,0,0,0,0,0,0,0,20,97,4,0,129,2,16,128,16,0,0,0,0,
            0,0,0,0,0,32,146,4,0,16,128,0,1,128,72,0,0,64,0,128,64,8,0,128,24,4,0,1,0,34,64,8,0,0,2,0,0,0,0,0,
            0,0,0,0,0,2,0,0,4,1,1,8,0,0,0,0,0,33,8,0,80,0,0,0,0,8,0,2,0,0,0,0,1,0,0,0,0,0,0,0])
explosion5 = bytearray([0,0,0,0,0,16,0,128,32,64,0,0,32,16,0,0,0,128,8,0,0,0,16,32,2,0,32,0,64,8,0,0,0,128,0,0,0,0,0,0,
            0,0,0,132,0,0,2,24,0,0,0,1,0,0,0,0,0,0,0,0,0,0,0,0,16,0,0,0,0,4,32,0,1,36,0,128,0,0,0,0,
            0,8,0,0,128,8,0,130,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,128,2,16,128,16,0,0,0,0,
            0,0,0,16,0,32,146,4,0,64,0,0,0,0,64,0,0,0,0,0,0,0,0,128,0,0,0,0,0,34,64,8,0,0,34,0,0,0,0,0,
            0,0,0,0,0,0,8,4,0,0,0,8,0,0,0,0,0,33,8,0,16,0,0,0,0,8,0,2,0,8,0,0,1,0,0,0,0,0,0,0])
explosion6 = bytearray([0,0,0,0,0,16,0,128,0,64,0,0,0,16,0,0,0,0,8,0,0,0,0,0,2,0,0,0,64,8,0,0,0,0,0,0,0,0,0,0,
            0,0,0,128,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,4,0,0,0,4,0,0,0,0,0,0,
            0,0,0,0,0,8,0,128,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,128,2,16,0,0,0,0,0,0,
            0,0,0,16,0,0,128,0,0,64,0,0,0,0,64,0,0,0,0,0,0,0,0,128,0,0,0,0,0,2,0,0,0,0,32,0,0,0,0,0,
            0,0,0,0,0,0,8,0,0,0,0,0,0,0,0,0,0,0,0,0,16,0,0,0,0,8,0,0,0,0,0,0,1,0,0,0,0,0,0,0])            
            
# SPRITES 
heartSprite = thumby.Sprite(11,11,heartMap,15,29)
starSprite = thumby.Sprite(11,11,starMap,31,29)
bombSprite = thumby.Sprite(11,11,bombMap,47,29)
heartBoxSprite = thumby.Sprite(60,18,heartBoxMap,-2,22)
starBoxSprite = thumby.Sprite(60,18,starBoxMap,34,22)
explosionSprite = thumby.Sprite(40,40,explosion0+explosion1+explosion2+explosion3+explosion4+explosion5+explosion6,18,0)
sortSprites = [heartSprite,starSprite,bombSprite] # ARRAY
thumby.display.setFPS(60) 

# TITLE SCREEN
thumby.display.fill(0)
thumby.display.setFont("/lib/font8x8.bin",8,8,1)
thumby.display.drawText("TinySort",1,0,1)
thumby.display.drawSprite(sortSprites[0])
thumby.display.drawSprite(sortSprites[1])
thumby.display.drawSprite(sortSprites[2])
thumby.display.update()

while(not thumby.buttonA.pressed() and not thumby.buttonB.pressed()):
    thumby.display.setFont("/lib/font3x5.bin",3,5,1)
    thumby.display.drawText("A:Play",25,12,1)
    thumby.display.drawText("B:Quit",25,19,1)
    thumby.display.update()
    if thumby.buttonB.pressed():
        thumby.reset()
    if thumby.buttonA.pressed():
        break
   
# INSTRUCTIONS 
thumby.display.fill(0)
thumby.display.setFont("/lib/font5x7.bin",5,7,1)
thumby.display.drawText("Controls:",0,0,1)
thumby.display.drawLine(0, 8, 72, 8, 1)
thumby.display.setFont("/lib/font3x5.bin",3,5,1)
thumby.display.drawText("L:Put in heart box",0,12,1)
thumby.display.drawText("R:Put in star box", 0, 19, 1)
thumby.display.drawText("U/D:Discard", 0, 26, 1)
thumby.display.drawText("Discard bombs only", 0, 33, 1)

thumby.display.update()
time.sleep(3)

# CONSTANTS
constantScore = 0
constantTurnTime = 3000 # THREE SECONDS TO CLICK 
constantGameTime = 60000 # ONE MINUTE TO PLAY

# VARIABLES
score = constantScore
turnTime = constantTurnTime
gameTime = time.ticks_ms() + constantGameTime 

# CHANGING SPRITE POSITIONS
heartSprite .x = 32
heartSprite .y = -5

starSprite .x = 32
starSprite .y = -5

bombSprite .x = 32
bombSprite .y = -5

# FUNCTION TO SHOW EXPLOSION
def showExplosion():
    frameCtr = 0
    thumby.display.setFPS(3)
    while (True):
        thumby.display.fill(0)
        explosionSprite.setFrame(frameCtr)
        thumby.display.drawSprite(explosionSprite)
        frameCtr += 1
        thumby.display.update()
        if (frameCtr > 6):
            break
    
# FUNCTION TO SHOW FINAL SCORE
def showFinalScore():
    thumby.display.fill(0)
    thumby.display.setFont("/lib/font5x7.bin",5,7,1) 
    thumby.display.drawText("SCORE: %d" % score,11,18,1)
    thumby.display.update()
    time.sleep(2)
    playAgain()
    
# FUNCTION IF PLAYER LOSES
def gameOver():
    thumby.audio.play(220,1000)
    thumby.display.fill(0)
    thumby.display.setFont("/lib/font8x8.bin",8,8,1) 
    thumby.display.drawText("GAME",18,18,1)
    thumby.audio.play(295,1000)
    thumby.display.update()
    thumby.audio.play(330,1000)
    time.sleep(1)
    thumby.display.fill(0)
    thumby.display.drawText("OVER",18,18,1)
    thumby.display.update()
    time.sleep(1) 
    showFinalScore()
    
# FUNCTION FOR WHEN GAME TIME HAS RUN OUT
def timesUp():
    thumby.audio.play(500,1000)
    thumby.display.fill(0)
    thumby.display.setFont("/lib/font8x8.bin",8,8,1) 
    thumby.display.drawText("TIME'S",10,18,1)
    thumby.audio.play(580,1000)
    thumby.display.update()
    thumby.audio.play(670,1000)
    time.sleep(1)
    thumby.display.fill(0)
    thumby.display.drawText("UP",28,18,1)
    thumby.display.update()
    time.sleep(1) 
    showFinalScore()

def playAgain():
    # RESETTING VARIABLES
    global score  
    global turnTime
    global gameTime
    score = constantScore
    turnTime = constantTurnTime
    gameTime = time.ticks_ms() * 2  # CHANGING HERE SO GAME LOOP IS NEVER EXITED
    
    thumby.display.fill(0)
    thumby.display.setFont("/lib/font3x5.bin", 3, 5, 1)
    thumby.display.drawText("Play Again?", 15, 14, 1)
    thumby.display.drawText("A: Yes   B: No", 8, 21, 1)
    thumby.display.update()
    while not thumby.buttonA.pressed() or not thumby.buttonB.pressed():
        if thumby.buttonB.pressed():
            thumby.reset()
        if thumby.buttonA.pressed():
            break

# LOOP TO PLAY AGAIN
while (True):
    
    # LOOP FOR THE ENTIRE GAME
    while (time.ticks_ms()  <= gameTime):
        random.seed(time.ticks_ms())
        num = random.randint(0, 2)
        thumby.audio.play(1000,50)
       
        # LOOP TO DISPLAY SPRITE ANIMATION 
        for i in range (0, 10):
            thumby.display.fill(0) 
            thumby.display.drawSprite(heartBoxSprite)
            thumby.display.drawSprite(starBoxSprite)
            thumby.display.drawText("%d" % score,0,0,1)
            sortSprites[num].y += 1 
            thumby.display.drawSprite(sortSprites[num]) 
            thumby.display.update() 
        
        now = time.ticks_ms() 
        future = now + turnTime
        lost = False
        
        # LOOP FOR EACH TURN
        while (time.ticks_ms()  <= future):
            
            if (num == 0 and thumby.buttonL.justPressed()):
                score += 1
                break
            elif (num == 0 and (thumby.buttonR.justPressed() or thumby.buttonU.justPressed() or thumby.buttonD.justPressed())):
                lost = True
                break
            if (num == 1 and thumby.buttonR.justPressed()):
                score += 1
                break
            elif (num == 1 and (thumby.buttonL.justPressed() or thumby.buttonU.justPressed() or thumby.buttonD.justPressed())):
                lost = True
                break
            if (num == 2 and (thumby.buttonU.justPressed() or thumby.buttonD.justPressed())):
                score += 1
                break
            elif (num == 2 and (thumby.buttonR.justPressed() or thumby.buttonL.justPressed())):
                lost = True
                showExplosion()
                thumby.display.setFPS(60) 
                break
            if (time.ticks_ms() + 5  > future): # IF TIME RUNS OUT DURING THE TURN
                lost = True
                break
            
        if lost == True:
            gameOver()
            gameTime = time.ticks_ms() + constantGameTime  
            
        turnTime -= 40 # MAKING TURNS 40 MS FASTER EACH ITERATION
        sortSprites[num] .y = -5 # RESETTING SPRITE POSITION IN Y
        thumby.display.update()
        
    timesUp() # CALLED IF 60 SECONDS PASS 
    gameTime = time.ticks_ms() + constantGameTime
    

