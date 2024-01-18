import time
import thumby
import math
import random

# BITMAP: width: 15, height 15
hole = bytearray([0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,
           28,54,99,65,65,65,65,65,65,65,65,65,99,54,28])
snake = bytearray([0,0,28,34,193,89,129,129,129,89,193,34,28,0,0,
           28,54,99,65,127,64,68,67,68,64,127,65,99,54,28])
hit = bytearray([126,10,10,14,0,60,66,66,60,0,62,64,112,64,62,
           28,54,99,113,73,101,69,69,69,101,73,113,99,54,28])
emptyHit = bytearray([7,4,7,0,7,2,7,0,112,80,112,0,112,32,112,
           28,54,99,65,65,65,65,65,65,65,65,65,99,54,28])
           
snakeSprite1 = thumby.Sprite(15,15,hole+snake+hit+emptyHit,28,0) # UP
snakeSprite2 = thumby.Sprite(15,15,hole+snake+hit+emptyHit,28,24) # DOWN
snakeSprite3 = thumby.Sprite(15,15,hole+snake+hit+emptyHit,8,12) # LEFT
snakeSprite4 = thumby.Sprite(15,15,hole+snake+hit+emptyHit,48,12) # RIGHT
snakeSprites = [snakeSprite1, snakeSprite2, snakeSprite3, snakeSprite4]
titleSnake = thumby.Sprite(15,15,hole+snake+hit,52,6) 
scoreSnake = thumby.Sprite(15,15,snake,46,22)

# CONSTANTS
constantScore = 0
constantTurnTime = 3000 # THREE SECONDS TO CLICK 
constantGameTime = 60000 # ONE MINUTE TO PLAY
constantDecrease = 0 # TO DECREASE TURN TIME
constantWhacks = 0 # TO CALCULATE ACCURACY IN GAME TWO
constantAccuracy = 0 # TO CALCULATE ACCURACY IN GAME TWO

# VARIABLES
score = constantScore
turnTime = constantTurnTime
gameTime = time.ticks_ms() + constantGameTime
decrease = constantDecrease
breakLoop = False
whacks = constantWhacks
accuracy = constantAccuracy
strAccuracy = "0%"

# FUNCTIONS TO SHOW FINAL SCORE
def showFinalScore1():
    thumby.display.fill(0)
    thumby.display.setFont("/lib/font5x7.bin",5,7,1) 
    thumby.display.drawText("SCORE: ",14,6,1)
    thumby.display.drawText(str(score),14,18,1)
    thumby.display.drawSprite(scoreSnake)
    thumby.display.update()
    time.sleep(2)
    playAgain()
    
def showFinalScore2():
    thumby.display.fill(0)
    thumby.display.setFont("/lib/font5x7.bin",5,7,1) 
    thumby.display.drawText("SCORE: ",12,0,1)
    thumby.display.drawText(str(score),12,8,1)
    thumby.display.drawText("ACCURACY: ",12,22,1)
    thumby.display.drawText(strAccuracy,12,30,1)
    thumby.display.update()
    time.sleep(2)
    playAgain()

# GAME OVER
def gameOver():
    thumby.display.fill(0)
    thumby.display.setFont("/lib/font8x8.bin",8,8,1) 
    thumby.display.drawText("GAME",18,18,1)
    thumby.display.update()
    time.sleep(1)
    thumby.display.fill(0)
    thumby.display.drawText("OVER",18,18,1)
    thumby.display.update()
    time.sleep(1) 
    showFinalScore1()
    
# FUNCTION FOR WHEN GAME TIME HAS RUN OUT
def timesUp():
    thumby.display.fill(0)
    thumby.display.setFont("/lib/font8x8.bin",8,8,1) 
    thumby.display.drawText("TIME'S",10,18,1)
    thumby.display.update()
    time.sleep(1)
    thumby.display.fill(0)
    thumby.display.drawText("UP",28,18,1)
    thumby.display.update()
    time.sleep(1) 
    showFinalScore2()

# FUNCTION TO PLAY AGAIN
def playAgain():
    # RESETTING VARIABLES
    global score  
    global turnTime
    global gameTime
    global decrease
    global breakLoop
    global whacks
    global accuracy
    global strAccuracy
    score = constantScore
    turnTime = constantTurnTime
    gameTime = time.ticks_ms() * 2 
    decrease = constantDecrease
    whacks = constantWhacks
    accuracy = constantAccuracy
    strAccuracy = "0%"
    
    thumby.display.fill(0)
    thumby.display.setFont("/lib/font3x5.bin", 3, 5, 1)
    thumby.display.drawText("Play Again?", 15, 14, 1)
    thumby.display.drawText("A: Yes   B: No", 8, 21, 1)
    thumby.display.update()
    while not thumby.buttonA.pressed() or not thumby.buttonB.pressed():
        if thumby.buttonB.pressed():
            breakLoop = True # TO BREAK OUT OF ALL LOOPS AND RESTART
            break
        if thumby.buttonA.pressed():
            break

# ANIMATION
def snakeHit(sprite): 
    sprite.setFrame(2)
    thumby.display.drawSprite(sprite)
    thumby.display.update()
    
# ANIMATION
def emptyHit(sprite): 
    sprite.setFrame(3)
    thumby.display.drawSprite(sprite)
    thumby.display.update()
    time.sleep(0.8)

while(True):
    # LOOP VARIABLES
    breakLoop = False
    
    # TITLE SCREEN
    thumby.display.fill(0)
    thumby.display.setFont("/lib/font8x8.bin",8,8,1)
    thumby.display.drawText("Whack",2,0,1)
    thumby.display.drawText("-A-",11,9,1)
    thumby.display.setFont("/lib/font8x8.bin",8,8,1)
    thumby.display.drawText("Snake",2,18,1)
    thumby.display.update()
    
    frameCtr = 0
    loopCtr = 0
    while(not thumby.buttonA.pressed() and not thumby.buttonB.pressed()):
        thumby.display.setFont("/lib/font3x5.bin",3,5,1)
        thumby.display.drawText("A:Play  B:Quit",9,35,1)
        titleSnake.setFrame(frameCtr)
        thumby.display.drawSprite(titleSnake)
        if (loopCtr > 20): # ANIMATION IN TITLE SCREEN
            frameCtr += 1
            loopCtr = 0
        thumby.display.update()
        if thumby.buttonB.pressed():
            thumby.reset() # QUIT GAME
        if thumby.buttonA.pressed():
            break # PLAY
        loopCtr += 1
        
    # GAME MENU
    time.sleep(0.1)
    while(not thumby.buttonA.pressed() and not thumby.buttonB.pressed()):
        thumby.display.fill(0)
        thumby.display.setFont("/lib/font5x7.bin",5,7,1)
        thumby.display.drawText("GAME MENU:",0,0,1)
        thumby.display.drawLine(0, 8, 72, 8, 1)
        thumby.display.setFont("/lib/font3x5.bin",3,5,1)
        thumby.display.drawText("A: HIT OR LOSE",2,18,1)
        thumby.display.drawText("B: QUICK WHACKS",2,28,1)
        thumby.display.update()
        
# *************************** GAME ONE *************************** 
        if thumby.buttonA.pressed(): 
            # INSTRUCTIONS 
            thumby.display.fill(0)
            thumby.display.setFont("/lib/font5x7.bin",5,7,1)
            thumby.display.drawText("Rules:",0,0,1)
            thumby.display.drawLine(0, 8, 72, 8, 1)
            thumby.display.setFont("/lib/font3x5.bin",3,5,1)
            thumby.display.drawText("Whack the snakes!",0,12,1)
            thumby.display.drawText("Use the trackpad", 0, 19, 1)
            thumby.display.drawText("and do not hit", 0, 26, 1)
            thumby.display.drawText("empty holes!!", 0, 33, 1)
            thumby.display.update()
            time.sleep(3)
            
            while (True):
                if (turnTime > 1600):
                    turnTime -= decrease # DECREASING TURN TIME
                    decrease += 2
                    print(turnTime)
                
                thumby.display.fill(0) 
                for sprite in snakeSprites:
                    sprite.setFrame(0)
                    thumby.display.drawSprite(sprite) # DRAWING HOLES
                thumby.display.update()
                
                now = time.ticks_ms() 
                future = now + turnTime
                
                # SPAWNING SNAKES
                random.seed(time.ticks_ms())
                num1 = random.randint(0, 1)
                num2 = random.randint(0, 1)
                num3 = random.randint(0, 1)
                num4 = random.randint(0, 1)
                nums = [num1, num2, num3, num4]
                snakesToHit = [0,0,0,0]
            
                if (num1 == 0 and num2 == 0 and num3 == 0 and num4 == 0):
                    continue
                
                counter = 0
                for sprite in snakeSprites:
                    sprite.setFrame(nums[counter])
                    thumby.display.drawSprite(sprite) # DRAWING SNAKES
                    counter += 1
                thumby.display.drawText("%d" % score,0,0,1)
                thumby.display.update()
                
                # LOOP FOR EACH TURN
                while (time.ticks_ms()  <= future):
                    if (num1 == 1 and thumby.buttonU.justPressed()):
                        snakesToHit[0] = 1
                        snakeHit(snakeSprites[0])
                       
                    if (num2 == 1 and thumby.buttonD.justPressed()):
                        snakesToHit[1] = 1
                        snakeHit(snakeSprites[1])
                       
                    if (num3 == 1 and thumby.buttonL.justPressed()):
                        snakesToHit[2] = 1
                        snakeHit(snakeSprites[2])
                        
                    if (num4 == 1 and thumby.buttonR.justPressed()):
                        snakesToHit[3] = 1
                        snakeHit(snakeSprites[3])
                      
                    if (nums == snakesToHit):
                        score+=1
                        time.sleep(0.3)
                        break
                    
                    # IF EMPTY WHOLES ARE HIT
                    if (num1 == 0 and thumby.buttonU.justPressed()):
                        emptyHit(snakeSprites[0])
                        gameOver()
                        break
    
                    if (num2 == 0 and thumby.buttonD.justPressed()):
                        emptyHit(snakeSprites[1])
                        gameOver()
                        break
                        
                    if (num3 == 0 and thumby.buttonL.justPressed()):
                        emptyHit(snakeSprites[2])
                        gameOver()
                        break
                        
                    if (num4 == 0 and thumby.buttonR.justPressed()):
                        emptyHit(snakeSprites[3])
                        gameOver()
                        break
                    
                    if (time.ticks_ms() + 5 > future):
                        print("Ya lost!")
                        gameOver()
                        
                    if (breakLoop == True):
                        break
                if (breakLoop == True):
                    break
            if (breakLoop == True):
                print("Breaking out of loop")
                time.sleep(0.4)
                break
                
            
# *************************** GAME TWO *************************** 
        if thumby.buttonB.pressed(): 
            # INSTRUCTIONS 
            thumby.display.fill(0)
            thumby.display.setFont("/lib/font5x7.bin",5,7,1)
            thumby.display.drawText("Rules:",0,0,1)
            thumby.display.drawLine(0, 8, 72, 8, 1)
            thumby.display.setFont("/lib/font3x5.bin",3,5,1)
            thumby.display.drawText("You have one",0,12,1)
            thumby.display.drawText("minute to whack", 0, 19, 1)
            thumby.display.drawText("all the snakes", 0, 26, 1)
            thumby.display.drawText("that you can!!", 0, 33, 1)
            thumby.display.update()
            time.sleep(3)
            
            while (True):
                gameTime = time.ticks_ms() + constantGameTime
                while (time.ticks_ms()  <= gameTime):
                    thumby.display.fill(0) 
                    for sprite in snakeSprites:
                        sprite.setFrame(0)
                        thumby.display.drawSprite(sprite)
                    thumby.display.update()
                    
                    now = time.ticks_ms() 
                    future = now + turnTime
                    
                    random.seed(time.ticks_ms())
                    num1 = random.randint(0, 1)
                    num2 = random.randint(0, 1)
                    num3 = random.randint(0, 1)
                    num4 = random.randint(0, 1)
                    nums = [num1, num2, num3, num4]
                    snakesToHit = [0,0,0,0]
                
                    if (num1 == 0 and num2 == 0 and num3 == 0 and num4 == 0):
                        continue
                    
                    counter = 0
                    for sprite in snakeSprites:
                        sprite.setFrame(nums[counter])
                        thumby.display.drawSprite(sprite)
                        counter += 1
                    thumby.display.drawText("%d" % score,0,0,1)
                    thumby.display.drawText(strAccuracy,57,0,1) # here 
                    thumby.display.update()
                    
                    # LOOP FOR EACH TURN
                    while (time.ticks_ms()  <= future):
                        if (num1 == 1 and thumby.buttonU.justPressed()):
                            snakesToHit[0] = 1
                            snakeHit(snakeSprites[0])
                            score+=1
                           
                        if (num2 == 1 and thumby.buttonD.justPressed()):
                            snakesToHit[1] = 1
                            snakeHit(snakeSprites[1])
                            score+=1
                           
                        if (num3 == 1 and thumby.buttonL.justPressed()):
                            snakesToHit[2] = 1
                            snakeHit(snakeSprites[2])
                            score+=1
                            
                        if (num4 == 1 and thumby.buttonR.justPressed()):
                            snakesToHit[3] = 1
                            snakeHit(snakeSprites[3])
                            score+=1
                          
                        if (nums == snakesToHit):
                            time.sleep(0.3)
                            break
                        
                        # IF EMPTY WHOLES ARE HIT
                        if (num1 == 0 and thumby.buttonU.justPressed()):
                            whacks+=1
        
                        if (num2 == 0 and thumby.buttonD.justPressed()):
                            whacks+=1
                            
                        if (num3 == 0 and thumby.buttonL.justPressed()):
                            whacks+=1
                            
                        if (num4 == 0 and thumby.buttonR.justPressed()):
                            whacks+=1
                        
                    if (whacks+score != 0):
                        accuracy = int(score/(whacks+score) * 100) # CALCULATING ACCURACY
                        strAccuracy = str(accuracy) + "%"
                
                    if (turnTime > 900):
                        turnTime-=decrease
                    print("Game time: " + str(gameTime - now))
                    print("Turn time: " + str(turnTime))
                    print("\n")
                    decrease+=2
            
                timesUp() # 60 SECONDS ARE UP
                if (breakLoop == True):
                    break
            if (breakLoop == True):
                print("Breaking out of loop")
                time.sleep(0.4)
                break
            
            