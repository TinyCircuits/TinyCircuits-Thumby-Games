import thumby
import time
import random
import math
import machine

thumby.saveData.setName("GameData")

#Sprite Maps

# BITMAP: width: 8, height: 4
paddleMap = bytearray([6,15,13,15,15,13,15,6])

# BITMAP: width: 1, height: 1
blinkEyeMap = bytearray([1])

# BITMAP: width: 6, height: 6
ballMap = bytearray([12,18,33,33,18,12])

# BITMAP: width: 6, height: 6
powerBallMap = bytearray([12,30,63,63,30,12])

# BITMAP: width: 3, height: 3
arrowMap = bytearray([7,5,2])

# BITMAP: width: 8, height: 4
brickMap1 = bytearray([15,9,9,9,9,9,9,15])

# BITMAP: width: 8, height: 4
brickMap2 = bytearray([15,15,15,15,15,15,15,15])

# BITMAP: width: 8, height: 8
bugMap1 = bytearray([56,69,181,130,130,181,69,56])

# BITMAP: width: 8, height: 8
bugMap2 = bytearray([56,69,158,130,130,158,69,56])

# BITMAP: width: 10, height: 10
bossMap1_A = bytearray([254,1,5,57,137,137,57,5,1,254,
           1,2,2,2,2,2,2,2,2,1])

# BITMAP: width: 10, height: 10
bossMap1_B = bytearray([254,1,5,185,9,9,185,5,1,254,
           1,2,2,2,3,3,2,2,2,1])

# BITMAP: width: 10, height: 10
bossMap1_C = bytearray([254,1,85,211,163,163,211,85,1,254,
           1,2,3,2,2,2,2,3,2,1])

paddleX = 0
paddleY = 32

ballX = 0
ballY = 0
ballDir = 2

paddleBlink = False
paddleBlinkCheck = random.randint(30, 120)
paddleBlinkCounter = 0

ballSpawn = False
ballSpawnStart = True

paddleBounces = 0
paddleBouncesB = 0

brickSpawn = False
superBrickSpawn = False
bugSpawn = False
bugSpawnRight = False
bugFaceDown = True
bugRightFaceDown = True
bugFaceCounter = 0
bugFaceCounterRight = 0

bossReached = False

bossMode = False
bossChooser = 0
bossSpawn1 = False
bossSpawn1Complete = False
bossHealth = 0
bossDefeated = False
bossSpawnCounter = 0

boss1X = (0 - 10)
boss1Y = 2
boss1Face = 0
boss1FaceCounter = 0
boss1MovingRight = True


brickX = random.randint(2, 60)
prevBrickX = random.randint(2, 60)
brickChooser = random.randint(1, 2)
brickChooserLevel3 = random.randint(1, 3)
brickChooserLevel4 = random.randint(1, 6)
brickChooserLevel6 = random.randint(1, 9)
brickY = 10

bugX = (0 - 8)
bugRightX = 73
bugY = 10
bugRightY = 8

powerUp = False
poweredUp = False
powerUpJustUnlocked = False

level2Reach = 25
level3Reach = 50
level4Reach = 75
level5Reach = 125
level6Reach = 150
level7Reach = 175
bossLevel8Reach = 200

gameOver = False

gameState = 0
titleOption = 0
musicPlaying = False
musicMarker = 0
musicTracker = 0

gameSpeed = 1
paused = False

if (thumby.saveData.hasItem("music")):
    musicOption = int(thumby.saveData.getItem("music"))
else:
    musicOption = 0

currentScore = 0

if (thumby.saveData.hasItem("highscore")):
    highScore = int(thumby.saveData.getItem("highscore"))
else:
    highScore = 0

newHighScore = False

#set frames per second
thumby.display.setFPS(15)

# Begin main game loop that runs for the course of the game
while(1):
    #starting screen
    thumby.display.fill(0) # Fill canvas to black
    thumby.display.setFont("/lib/font3x5.bin", 3, 5, 1)
    
    if (gameState == 0):
        thumby.display.drawText("New Bouncer", 14, 0, 1)
        thumby.display.drawText("Play", 10, 16, 1)
        thumby.display.drawText("Music", 10, 22, 1)
        thumby.display.drawText("Score", 10, 28, 1)
        thumby.display.drawText("Exit", 10, 34, 1)
        if (titleOption == 0):
            arrowSprite = thumby.Sprite(8, 4, arrowMap, 2, 18)
            if (thumby.buttonD.justPressed() == True):
                titleOption = 1
            if (thumby.buttonA.pressed() == True):
                paddleX = 0
                paddleY = 32
            
                ballDir = 2
                
                paddleBounces = 0
                brickSpawn = False
                
                ballSpawn = False
                ballSpawnStart = True
                gameOver = False
                gameState = 9
                
                musicMarker = 0
                
                bugSpawn = False
                bugSpawnRight = False
                bugFaceDown = True
                bugRightFaceDown = True
                bugFaceCounter = 0
                bugFaceCounterRight = 0
                
                bossReached = False

                bossMode = False
                
                bossSpawn1 = False
                bossDefeated = False
                bossSpawnCounter = 0
                bossHealth = 0
                bossSpawn1Complete = False
                
                boss1X = (0 - 10)
                boss1Y = 2
                
                boss1Face = 0
                boss1FaceCounter = 0
                boss1MovingRight = True
                
                powerUp = False
                powerUpJustUnlocked = False
            if (thumby.buttonB.pressed() == True):
                paddleX = 0
                paddleY = 32
                
                ballDir = 2
                
                paddleBounces = 0
                brickSpawn = False
                
                ballSpawn = False
                ballSpawnStart = True
                gameOver = False
                gameState = 9
                
                musicMarker = 0
                
                bugSpawn = False
                bugSpawnRight = False
                bugFaceDown = True
                bugRightFaceDown = True
                bugFaceCounter = 0
                bugFaceCounterRight = 0
                
                bossReached = False

                bossMode = False
                
                bossSpawn1 = False
                bossDefeated = False
                bossSpawnCounter = 0
                bossHealth = 0
                bossSpawn1Complete = False
                
                boss1X = (0 - 10)
                boss1Y = 2
                
                boss1Face = 0
                boss1FaceCounter = 0
                boss1MovingRight = True
                
                powerUp = False
                powerUpJustUnlocked = False
        elif (titleOption == 1):
            arrowSprite = thumby.Sprite(8, 4, arrowMap, 2, 24)
            if (thumby.buttonU.justPressed() == True):
                titleOption = 0
            if (thumby.buttonD.justPressed() == True):
                titleOption = 2
            
            if (thumby.buttonA.pressed() == True):
                gameState = 3
            if (thumby.buttonB.pressed() == True):
                gameState = 3
        elif (titleOption == 2):
            arrowSprite = thumby.Sprite(8, 4, arrowMap, 2, 30)
            if (thumby.buttonU.justPressed() == True):
                titleOption = 1
            if (thumby.buttonD.justPressed() == True):
                titleOption = 3
                
            if (thumby.buttonA.pressed() == True):
                gameState = 6
            if (thumby.buttonB.pressed() == True):
                gameState = 6
        elif (titleOption == 3):
            arrowSprite = thumby.Sprite(8, 4, arrowMap, 2, 36)
            if (thumby.buttonU.justPressed() == True):
                titleOption = 2
            
            if (thumby.buttonA.pressed() == True):
                machine.reset()
            if (thumby.buttonB.pressed() == True):
                machine.reset()
        
        thumby.display.drawSprite(arrowSprite)
    elif (gameState == 1 and gameOver == False):
        if (currentScore < level3Reach):
            gameSpeed = 1
        elif (currentScore >= level3Reach and currentScore < level4Reach):
            gameSpeed = 2
        elif (currentScore >= level5Reach and currentScore < level6Reach):
            gameSpeed = 2
        elif (currentScore >= level7Reach and currentScore < bossLevel8Reach):
            gameSpeed = 2
        elif (currentScore >= bossLevel8Reach and bossSpawnCounter >= 50 and bossSpawnCounter < 60):
            gameSpeed = 2
        elif (currentScore >= bossLevel8Reach and bossSpawnCounter >= 100 and bossSpawnCounter < 110):
            gameSpeed = 2
        else:
            gameSpeed = 1
            
        if (bossMode == True):
            gameSpeed = 1
        
        bugSprite1 = thumby.Sprite(8, 8, bugMap1, bugX, bugY)
        bugSprite2 = thumby.Sprite(8, 8, bugMap2, bugX, bugY)
        bugSprite3 = thumby.Sprite(8, 8, bugMap1, bugRightX, bugRightY)
        bugSprite4 = thumby.Sprite(8, 8, bugMap2, bugRightX, bugRightY)
        bossSprite1_A = thumby.Sprite(10, 10, bossMap1_A, boss1X, boss1Y)
        bossSprite1_B = thumby.Sprite(10, 10, bossMap1_B, boss1X, boss1Y)
        bossSprite1_C = thumby.Sprite(10, 10, bossMap1_A, boss1X, boss1Y)
        
        
        if (bossMode == True):
            bossDefeated = False
            thumby.display.drawText("Boss: %d" % bossHealth, 0, 25, 1)
        
        #SPAWN BOSS 1
        if (bossSpawn1 == True):
            if (bossHealth > 0):
                bossMode = True
            elif (bossHealth <= 0):
                bossMode = False
                bossDefeated = True
                paddleBounces = 0
                paddleBouncesB = 0
                bossSpawn1 = False
            if (boss1Face == 0):
                thumby.display.drawSprite(bossSprite1_A)
            elif (boss1Face == 1):
                thumby.display.drawSprite(bossSprite1_B)
            elif (boss1Face == 2):
                boss1X += 0
                thumby.display.drawSprite(bossSprite1_C)
            if (boss1FaceCounter < 10 and boss1Face != 2):
                boss1FaceCounter += 1
            elif (boss1FaceCounter >= 10 and boss1Face != 2):
                if (boss1Face == 0):
                    boss1Face = 1
                elif (boss1Face == 1):
                    boss1Face == 0
                boss1FaceCounter = 0
            elif (boss1FaceCounter <= 15 and boss1Face == 2):
                boss1FaceCounter += 1
            elif (boss1FaceCounter > 15 and boss1Face == 2):
                boss1FaceCounter = 0
                boss1Face = 0
            
            if (bossSpawn1Complete == False and boss1X < 1 and boss1Face != 2):
                boss1X += 2
            elif (bossSpawn1Complete == False and boss1X >= 1 and boss1Face != 2):
                bossSpawn1Complete = True
            
            if (bossSpawn1Complete == True and boss1X < 61 and boss1MovingRight == True and boss1Face != 2):
                boss1X += 2
            elif (bossSpawn1Complete == True and boss1X >= 61 and boss1MovingRight == True and boss1Face != 2):
                boss1MovingRight = False
            elif (bossSpawn1Complete == True and boss1X > 1 and boss1MovingRight == False and boss1Face != 2):
                boss1X -= 2
            elif (bossSpawn1Complete == True and boss1X <= 1 and boss1MovingRight == False and boss1Face != 2):
                boss1MovingRight = True
        
        #BUG SPAWN ALONGSIDE BRICKS
        if (bugSpawnRight == True):
            if (bugRightFaceDown == True):
                thumby.display.drawSprite(bugSprite3)
            else:
                thumby.display.drawSprite(bugSprite4)
            if (bugRightX > (0 - 8)):
                if (paused == False):
                    bugFaceCounterRight += 1
                    bugRightX -= 1
                if (bugFaceCounterRight >= 10):
                    bugFaceCounterRight = 0
                    if (bugRightFaceDown == True):
                        bugRightFaceDown = False
                    else:
                        bugRightFaceDown = True
            else:
                bugRightFaceDown = True
                bugFaceCounterRight = 0
                bugRightX = 73
                paddleBouncesB = 0
                bugSpawnRight = False
        
        #BUG SPAWN INSTEAD OF BRICKS
        if (bugSpawn == True):
            brickSpawn = False
            superBrickSpawn = False
            if (bugFaceDown == True):
                thumby.display.drawSprite(bugSprite1)
            else:
                thumby.display.drawSprite(bugSprite2)
            if (bugX < 73):
                if (paused == False):
                    bugFaceCounter += 1
                    bugX += 1
                if (bugFaceCounter >= 10):
                    bugFaceCounter = 0
                    if (bugFaceDown == True):
                        bugFaceDown = False
                    else:
                        bugFaceDown = True
            else:
                bugFaceDown = True
                bugFaceCounter = 0
                bugX = (0 - 8)
                paddleBounces = 0
                bugSpawn = False
        
        if (superBrickSpawn == True):
            brickSpawn = False
        
        #Music Settings
        if (musicPlaying == True and musicOption == 1):
            musicTracker = time.ticks_ms()
            if (musicTracker > 0):
                musicMarker += (time.ticks_ms() % 1000)
            
            if (musicMarker >= 0):
                    if (musicMarker <= 50):
                        thumby.audio.play(150, 50)
                    elif (musicMarker > 100 and musicMarker < 150):
                        thumby.audio.play(100, 50)
                    elif (musicMarker >= 200 and musicMarker < 250):
                        thumby.audio.play(150, 50)
                    elif (musicMarker >= 250 and musicMarker < 300):
                        thumby.audio.play(100, 50)
                    elif (musicMarker > 400):
                        musicMarker = 0
        elif (musicPlaying == True and musicOption == 2):
            musicTracker = time.ticks_ms()
            if (musicTracker > 0):
                musicMarker += (time.ticks_ms() % 1000)
                
            if (musicMarker >= 0):
                if (musicMarker <= 50):
                    thumby.audio.play(100, 50)
                elif (musicMarker >= 100 and musicMarker < 150):
                    thumby.audio.play(100, 50)
                elif (musicMarker >= 200 and musicMarker < 250):
                    thumby.audio.play(150, 50)
                elif (musicMarker >= 275):
                    musicMarker = 0
        
        if (ballSpawn == False):
            thumby.display.drawText("Up to Start", 14, 0, 1)
        elif (ballSpawn == True):
            thumby.display.drawText("S: %d" % currentScore, 0, 0, 1)
            
        if (powerUpJustUnlocked == True):
            thumby.display.drawText("Power Up Unlocked!", 0, 10, 1)
            thumby.display.drawText("Press B!", 0, 15, 1)
            if ((thumby.buttonB.pressed() == True) and paused == False):
                powerUpJustUnlocked = False
        
        if (paused == True):
            thumby.display.drawText("Paused", 4, 25, 1)
    
        #Sprite Data

        paddleSprite = thumby.Sprite(8, 4, paddleMap, paddleX, paddleY)
        blinkSprite1 = thumby.Sprite(1, 1, blinkEyeMap, (paddleX + 2), (paddleY + 1))
        blinkSprite2 = thumby.Sprite(1, 1, blinkEyeMap, (paddleX + 5), (paddleY + 1))
        ballSprite = thumby.Sprite(6, 6, ballMap, ballX, ballY)
        powerBallSprite = thumby.Sprite(6, 6, powerBallMap, ballX, ballY)
        brickSprite1 = thumby.Sprite(8, 4, brickMap1, prevBrickX, brickY)
        brickSprite2 = thumby.Sprite(8, 4, brickMap2, brickX, brickY)
        
        if (paddleBlinkCounter < paddleBlinkCheck and paddleBlink == False):
            paddleBlinkCounter += 1
        elif (paddleBlinkCounter == paddleBlinkCheck and paddleBlink == False):
            paddleBlink = True
            paddleBlinkCounter = 0
        
        thumby.display.drawSprite(paddleSprite)
        
        if (paddleBlink == True):
            thumby.display.drawSprite(blinkSprite1)
            thumby.display.drawSprite(blinkSprite2)
            paddleBlink = False
        
        if (ballSpawn == True and ballSpawnStart == True):
            ballX = (paddleX + 2)
            ballY = (paddleY - 6)
            thumby.display.drawSprite(ballSprite)
            thumby.audio.play(200, 200)
            ballSpawnStart = False
        elif (ballSpawn == True and ballSpawnStart == False):
            if (poweredUp == True):
                thumby.display.drawSprite(powerBallSprite)
            else:
                thumby.display.drawSprite(ballSprite)
            if (ballDir == 0 and paused == False):
                ballX -= (1 * gameSpeed)
                ballY += (1 * gameSpeed)
            elif (ballDir == 1 and paused == False):
                ballX += (1 * gameSpeed)
                ballY += (1 * gameSpeed)
            elif (ballDir == 2 and paused == False):
                ballX += (1 * gameSpeed)
                ballY -= (1 * gameSpeed)
            elif (ballDir == 3 and paused == False):
                ballX -= (1 * gameSpeed)
                ballY -= (1 * gameSpeed)
            
            #DETECT BALL COLLISSION
            if (ballX <= 0 and ballDir == 0):
                ballDir = 1
                thumby.audio.play(200, 200)
            elif (ballX <= 0 and ballDir == 3):
                ballDir = 2
                thumby.audio.play(200, 200)
            elif ((ballX + 6) >= 72 and ballDir == 1):
                ballDir = 0
                thumby.audio.play(200, 200)
            elif ((ballX + 6) >= 72 and ballDir == 2):
                ballDir = 3
                thumby.audio.play(200, 200)
            elif (ballY <= 0 and ballDir == 2):
                ballDir = 1
                thumby.audio.play(200, 200)
            elif (ballY <= 0 and ballDir == 3):
                ballDir = 0
                thumby.audio.play(200, 200)
            elif ((ballY + 6) >= 40 and ballDir == 1):
                ballDir = 2
                gameOver = True
            elif ((ballY + 6) >= 40 and ballDir == 0):
                ballDir = 2
                gameOver = True
            
            #DETECT BALL COLLISSION WITH PADDLE
            if (((ballY + 6) == paddleY and ballX <= (paddleX + 8)) and (ballX + 6) >= paddleX):
                if (currentScore >= bossLevel8Reach):
                    bossReached = True
                if (bossReached == True and bossDefeated == False and powerUp == True):
                    if (bossChooser <= 1):
                        if (bossSpawn1 == False):
                            bossHealth = 4
                            bossSpawn1 = True
                elif (bossReached == True and bossDefeated == True and powerUp == True):
                    if (bossSpawnCounter <= 150):
                        bossSpawnCounter += 1
                    else:
                        bossSpawnCounter = 0
                        bossDefeated = False
                if (ballDir == 0):
                    if (paddleBounces <= 2):
                        currentScore += 1
                        paddleBounces += 1
                    elif (paddleBounces == 3):
                        currentScore += 1
                        paddleBounces += 1
                        if (currentScore < level2Reach):
                            brickSpawn = True
                        elif (currentScore >= level2Reach and currentScore < level3Reach):
                            if (brickChooser == 2):
                                superBrickSpawn = True
                            else:
                                brickSpawn = True
                        elif (currentScore >= level3Reach and currentScore < level4Reach):
                            if (brickChooserLevel3 == 2):
                                superBrickSpawn = True
                            else:
                                brickSpawn = True
                        elif (currentScore >= level4Reach and currentScore < level6Reach):
                            if (brickChooserLevel4 == 2):
                                superBrickSpawn = True
                            elif (brickChooserLevel4 == 4):
                                bugSpawn = True
                            else:
                                brickSpawn = True
                        elif (currentScore >= level6Reach and currentScore < bossLevel8Reach):
                            if (brickChooserLevel6 == 2):
                                superBrickSpawn = True
                            elif (brickChooserLevel6 == 4):
                                bugSpawn = True
                            else:
                                brickSpawn = True
                        elif (currentScore >= bossLevel8Reach and bossDefeated == True and powerUp == True):
                            if (brickChooserLevel6 == 2):
                                superBrickSpawn = True
                            elif (brickChooserLevel6 == 4):
                                bugSpawn = True
                            else:
                                brickSpawn = True
                        elif (currentScore >= bossLevel8Reach and powerUp == False):
                            if (brickChooserLevel6 == 2):
                                superBrickSpawn = True
                            elif (brickChooserLevel6 == 4):
                                bugSpawn = True
                            else:
                                brickSpawn = True
                    else:
                        currentScore += 1
                    
                    if (paddleBouncesB < 5):
                        paddleBouncesB += 1
                    elif (paddleBouncesB == 5):
                        if (currentScore < bossLevel8Reach):
                            bugSpawnRight = True
                            paddleBouncesB += 1
                        elif (currentScore >= bossLevel8Reach and bossDefeated == True and powerUp == True):
                            bugSpawnRight = True
                            paddleBouncesB += 1
                        elif (currentScore >= bossLevel8Reach and powerUp == False):
                            bugSpawnRight = True
                            paddleBouncesB += 1
                    else:
                        paddleBouncesB += 1
                    
                    ballDir = 3
                    thumby.audio.play(440, 200)
                elif (ballDir == 1):
                    if (paddleBounces <= 2):
                        currentScore += 1
                        paddleBounces += 1
                    elif (paddleBounces == 3):
                        currentScore += 1
                        paddleBounces += 1
                        if (currentScore < level2Reach):
                            brickSpawn = True
                        elif (currentScore >= level2Reach and currentScore < level3Reach):
                            if (brickChooser == 2):
                                superBrickSpawn = True
                            else:
                                brickSpawn = True
                        elif (currentScore >= level3Reach and currentScore < level4Reach):
                            if (brickChooserLevel3 == 2):
                                superBrickSpawn = True
                            else:
                                brickSpawn = True
                        elif (currentScore >= level4Reach and currentScore < level6Reach):
                            if (brickChooserLevel4 == 2):
                                superBrickSpawn = True
                            elif (brickChooserLevel4 == 4):
                                bugSpawn = True
                            else:
                                brickSpawn = True
                        elif (currentScore >= level6Reach and currentScore < bossLevel8Reach):
                            if (brickChooserLevel6 == 2):
                                superBrickSpawn = True
                            elif (brickChooserLevel6 == 4):
                                bugSpawn = True
                            else:
                                brickSpawn = True
                        elif (currentScore >= bossLevel8Reach and bossDefeated == True and powerUp == True):
                            if (brickChooserLevel6 == 2):
                                superBrickSpawn = True
                            elif (brickChooserLevel6 == 4):
                                bugSpawn = True
                            else:
                                brickSpawn = True
                        elif (currentScore >= bossLevel8Reach and powerUp == False):
                            if (brickChooserLevel6 == 2):
                                superBrickSpawn = True
                            elif (brickChooserLevel6 == 4):
                                bugSpawn = True
                            else:
                                brickSpawn = True
                    else:
                        currentScore += 1
                    
                    if (paddleBouncesB < 5):
                        paddleBouncesB += 1
                    elif (paddleBouncesB == 5):
                        if (currentScore < bossLevel8Reach):
                            bugSpawnRight = True
                            paddleBouncesB += 1
                        elif (currentScore >= bossLevel8Reach and bossDefeated == True and powerUp == True):
                            bugSpawnRight = True
                            paddleBouncesB += 1
                        elif (currentScore >= bossLevel8Reach and powerUp == False):
                            bugSpawnRight = True
                            paddleBouncesB += 1
                    else:
                        paddleBouncesB += 1
                    
                    ballDir = 2
                    thumby.audio.play(440, 200)
            
            #DETECT BALL COLLISSION WITH SIDES OF PADDLE
            if ((ballX + 6) == paddleX and (ballY + 6) >= paddleY and ballY <= paddleY + 4):
                if (ballDir == 0):
                    ballDir = 3
                if (ballDir == 1):
                    ballDir = 3
                currentScore += 1
                thumby.audio.play(440, 200)
            
            if (ballX == (paddleX + 8) and (ballY + 6) >= paddleY and ballY <= paddleY + 4):
                if (ballDir == 0):
                    ballDir = 2
                if (ballDir == 1):
                    ballDir = 2
                currentScore += 1
                thumby.audio.play(440, 200)
            
            #DETECT BALL COLLISSION WITH STANDARD BRICKS, SUPER BRICKS, AND BUGS
            if (gameSpeed == 1):
                #DETECT BALL COLLISSION WITH STANDARD BRICK
                if (brickSpawn == True and ((ballY + 6) == brickSprite1.y) and (ballX <= (brickSprite1.x + 8)) and ((ballX + 6) >= brickSprite1.x)):
                    brickX = brickSprite1.x
                    paddleBounces = 0
                    brickSpawn = False
                    currentScore += 2
                    thumby.audio.play(440, 200)
                    if (poweredUp == False):
                        if ballDir == 0:
                            ballDir = 3
                        if ballDir == 1:
                            ballDir = 2
            
                if (brickSpawn == True and (ballY == (brickSprite1.y + 4)) and (ballX <= brickSprite1.x + 8) and (ballX + 6 >= brickSprite1.x)):
                    brickX = brickSprite1.x
                    paddleBounces = 0
                    brickSpawn = False
                    currentScore += 2
                    thumby.audio.play(440, 200)
                    if (poweredUp == False):
                        if ballDir == 3:
                            ballDir = 0
                        if ballDir == 2:
                            ballDir = 1
            
                if (brickSpawn == True and ((ballX + 6) == brickSprite1.x) and ((ballY + 6) >= (brickSprite1.y)) and (ballY <= (brickSprite1.y + 4))):
                    brickX = brickSprite1.x
                    paddleBounces = 0
                    brickSpawn = False
                    currentScore += 2
                    thumby.audio.play(440, 200)
                    if (poweredUp == False):
                        if (ballDir == 2):
                            ballDir = 3
                        if (ballDir == 1):
                            ballDir = 0
            
                if (brickSpawn == True and ((ballX == (brickSprite1.x + 8)) and (ballY + 6) >= brickSprite1.y) and (ballY <= (brickSprite1.y + 4))):
                    brickX = brickSprite1.x
                    paddleBounces = 0
                    brickSpawn = False
                    currentScore += 2
                    thumby.audio.play(440, 200)
                    if (poweredUp == False):
                        if (ballDir == 0):
                            ballDir = 1
                        if (ballDir == 3):
                            ballDir = 2
            
                #DETECT BALL COLLISSION WITH SUPER BRICK
                if (superBrickSpawn == True and ((ballY + 6) == brickSprite2.y) and (ballX <= (brickSprite2.x + 8)) and ((ballX + 6) >= brickSprite2.x)):
                    prevBrickX = brickSprite2.x
                    superBrickSpawn = False
                    brickSpawn = True
                    currentScore += 4
                    thumby.audio.play(440, 200)
                    if (poweredUp == False):
                        if ballDir == 0:
                            ballDir = 3
                        if ballDir == 1:
                            ballDir = 2
            
                if (superBrickSpawn == True and (ballY == (brickSprite2.y + 4)) and (ballX <= brickSprite2.x + 8) and (ballX + 6 >= brickSprite2.x)):
                    prevBrickX = brickSprite2.x
                    superBrickSpawn = False
                    brickSpawn = True
                    currentScore += 4
                    thumby.audio.play(440, 200)
                    if (poweredUp == False):
                        if ballDir == 3:
                            ballDir = 0
                        if ballDir == 2:
                            ballDir = 1
            
                if (superBrickSpawn == True and ((ballX + 6) == brickSprite2.x) and ((ballY + 6) >= (brickSprite2.y)) and (ballY <= (brickSprite2.y + 4))):
                    prevBrickX = brickSprite2.x
                    superBrickSpawn = False
                    brickSpawn = True
                    currentScore += 4
                    thumby.audio.play(440, 200)
                    if (poweredUp == False):
                        if (ballDir == 2):
                            ballDir = 3
                        if (ballDir == 1):
                            ballDir = 0
            
                if (superBrickSpawn == True and ((ballX == (brickSprite2.x + 8)) and (ballY + 6) >= brickSprite2.y) and (ballY <= (brickSprite2.y + 4))):
                    prevBrickX = brickSprite2.x
                    paddleBounces = 0
                    superBrickSpawn = False
                    brickSpawn = True
                    currentScore += 4
                    thumby.audio.play(440, 200)
                    if (poweredUp == False):
                        if (ballDir == 0):
                            ballDir = 1
                        if (ballDir == 3):
                            ballDir = 2
                
                #DETECT BALL COLLISSION WITH STANDARD BUG
                if (bugSpawn == True and ((ballY + 6) == bugY) and (ballX <= bugX + 8) and ((ballX + 6) >= bugX)):
                    bugFaceDown = True
                    bugFaceCounter = 0
                    bugX = (0 - 8)
                    paddleBounces = 0
                    bugSpawn = False
                    currentScore += 8
                    thumby.audio.play(800, 200)
                    if (powerUp == False):
                        powerUp = True
                        powerUpJustUnlocked = True
                    if (poweredUp == False):
                        if ballDir == 0:
                            ballDir = 3
                        if ballDir == 1:
                            ballDir = 2
                        
                if (bugSpawn == True and (ballY == (bugY + 8)) and (ballX <= bugX + 8) and ((ballX + 6) >= bugX)):
                    bugFaceDown = True
                    bugFaceCounter = 0
                    bugX = (0 - 8)
                    paddleBounces = 0
                    bugSpawn = False
                    currentScore += 8
                    thumby.audio.play(800, 200)
                    if (powerUp == False):
                        powerUp = True
                        powerUpJustUnlocked = True
                    if (poweredUp == False):
                        if ballDir == 3:
                            ballDir = 0
                        if ballDir == 2:
                            ballDir = 1
                
                if (bugSpawn == True and ((ballX + 6) == bugX) and ((ballY + 6) >= (bugY)) and (ballY <= (bugY + 8))):
                    bugFaceDown = True
                    bugFaceCounter = 0
                    bugX = (0 - 8)
                    paddleBounces = 0
                    bugSpawn = False
                    currentScore += 8
                    thumby.audio.play(800, 200)
                    if (poweredUp == False):
                        if (ballDir == 2):
                            ballDir = 3
                        if (ballDir == 1):
                            ballDir = 0
            
                if (bugSpawn == True and ((ballX == (bugX + 8)) and (ballY + 6) >= bugY) and (ballY <= (bugY + 8))):
                    bugFaceDown = True
                    bugFaceCounter = 0
                    bugX = (0 - 8)
                    paddleBounces = 0
                    bugSpawn = False
                    currentScore += 8
                    thumby.audio.play(800, 200)
                    if (poweredUp == False):
                        if (ballDir == 0):
                            ballDir = 1
                        if (ballDir == 3):
                            ballDir = 2
                
                #DETECT BALL COLLISSION WITH RIGHT-TO-LEFT BUG
                if (bugSpawnRight == True and ((ballY + 6) == bugRightY) and (ballX <= bugRightX + 8) and ((ballX + 6) >= bugRightX)):
                    bugFaceDown = True
                    bugFaceCounter = 0
                    bugX = 73
                    paddleBouncesB = 0
                    bugSpawnRight = False
                    currentScore += 8
                    thumby.audio.play(800, 200)
                    if (powerUp == False):
                        powerUp = True
                        powerUpJustUnlocked = True
                    if (poweredUp == False):
                        if ballDir == 0:
                            ballDir = 3
                        if ballDir == 1:
                            ballDir = 2
                        
                if (bugSpawnRight == True and (ballY == (bugRightY + 8)) and (ballX <= bugRightX + 8) and ((ballX + 6) >= bugRightX)):
                    bugRightFaceDown = True
                    bugFaceCounterRight = 0
                    bugRightX = 73
                    paddleBouncesB = 0
                    bugSpawnRight = False
                    currentScore += 8
                    thumby.audio.play(800, 200)
                    if (powerUp == False):
                        powerUp = True
                        powerUpJustUnlocked = True
                    if (poweredUp == False):
                        if ballDir == 3:
                            ballDir = 0
                        if ballDir == 2:
                            ballDir = 1
                
                if (bugSpawnRight == True and ((ballX + 6) == bugRightX) and ((ballY + 6) >= (bugRightY)) and (ballY <= (bugRightY + 8))):
                    bugRightFaceDown = True
                    bugFaceCounterRight = 0
                    bugRightX = 73
                    paddleBouncesB = 0
                    bugSpawnRight = False
                    currentScore += 8
                    thumby.audio.play(800, 200)
                    if (poweredUp == False):
                        if (ballDir == 2):
                            ballDir = 3
                        if (ballDir == 1):
                            ballDir = 0
            
                if (bugSpawnRight == True and ((ballX == (bugRightX + 8)) and (ballY + 6) >= bugRightY) and (ballY <= (bugRightY + 8))):
                    bugRightFaceDown = True
                    bugFaceCounterRight = 0
                    bugRightX = 73
                    paddleBouncesB = 0
                    bugSpawnRight = False
                    currentScore += 8
                    thumby.audio.play(800, 200)
                    if (poweredUp == False):
                        if (ballDir == 0):
                            ballDir = 1
                        if (ballDir == 3):
                            ballDir = 2
                
                #DETECT BALL COLLISSION WITH BOSS 1
                if (bossSpawn1 == True and ((ballY + 6) == boss1Y) and (ballX <= boss1X + 10) and ((ballX + 6) >= boss1X)):
                    if (poweredUp == True):
                        bossHealth -= 1
                        boss1Face = 2
                        currentScore += 10
                        thumby.audio.play(700, 200)
                        if ballDir == 0:
                            ballDir = 3
                        if ballDir == 1:
                            ballDir = 2
                    elif (poweredUp == False):
                        boss1Face = 2
                        thumby.audio.play(200, 200)
                        if ballDir == 0:
                            ballDir = 3
                        if ballDir == 1:
                            ballDir = 2
                        
                if (bossSpawn1 == True and (ballY == (boss1Y + 10)) and (ballX <= boss1X + 10) and ((ballX + 6) >= boss1X)):
                    if (poweredUp == True):
                        bossHealth -= 1
                        boss1Face = 2
                        currentScore += 10
                        thumby.audio.play(700, 200)
                        if ballDir == 3:
                            ballDir = 0
                        if ballDir == 2:
                            ballDir = 1
                    elif (poweredUp == False):
                        boss1Face = 2
                        thumby.audio.play(200, 200)
                        if ballDir == 3:
                            ballDir = 0
                        if ballDir == 2:
                            ballDir = 1
                
                if (bossSpawn1 == True and ((ballX + 6) == boss1X) and ((ballY + 6) >= (boss1Y)) and (ballY <= (boss1Y + 10))):
                    if (poweredUp == True):
                        bossHealth -= 1
                        boss1Face = 2
                        currentScore += 10
                        thumby.audio.play(700, 200)
                        if (ballDir == 2):
                            ballDir = 3
                        if (ballDir == 1):
                            ballDir = 0
                    elif (poweredUp == False):
                        boss1Face = 2
                        thumby.audio.play(200, 200)
                        if (ballDir == 2):
                            ballDir = 3
                        if (ballDir == 1):
                            ballDir = 0
            
                if (bossSpawn1 == True and ((ballX == (boss1X + 10)) and (ballY + 6) >= boss1Y) and (ballY <= (boss1Y + 10))):
                    if (poweredUp == True):
                        bossHealth -= 1
                        boss1Face = 2
                        currentScore += 10
                        thumby.audio.play(700, 200)
                        if (ballDir == 0):
                            ballDir = 1
                        if (ballDir == 3):
                            ballDir = 2
                    elif (poweredUp == False):
                        boss1Face = 2
                        thumby.audio.play(200, 200)
                        if (ballDir == 0):
                            ballDir = 1
                        if (ballDir == 3):
                            ballDir = 2
                
            elif (gameSpeed == 2):
                #DETECT BALL COLLISSION WITH STANDARD BRICK
                if (brickSpawn == True and (((ballY + 6) >= (brickSprite1.y - 1)) and ((ballY + 6) <= (brickSprite1.y + 1))) and (ballX <= (brickSprite1.x + 9)) and ((ballX + 6) >= (brickSprite1.x - 1))):
                    brickX = brickSprite1.x
                    paddleBounces = 0
                    brickSpawn = False
                    currentScore += 2
                    thumby.audio.play(440, 200)
                    if (poweredUp == False):
                        if ballDir == 0:
                            ballDir = 3
                        if ballDir == 1:
                            ballDir = 2
            
                if (brickSpawn == True and (ballY >= (brickSprite1.y + 3)) and (ballY <= (brickSprite1.y + 5)) and (ballX <= brickSprite1.x + 9) and (ballX + 6 >= (brickSprite1.x - 1))):
                    brickX = brickSprite1.x
                    paddleBounces = 0
                    brickSpawn = False
                    currentScore += 2
                    thumby.audio.play(440, 200)
                    if (poweredUp == False):
                        if ballDir == 3:
                            ballDir = 0
                        if ballDir == 2:
                            ballDir = 1
            
                if (brickSpawn == True and ((ballX + 6) >= (brickSprite1.x - 1)) and ((ballX + 6) <= (brickSprite1.x + 1)) and ((ballY + 6) >= (brickSprite1.y - 1)) and (ballY <= (brickSprite1.y + 5))):
                    brickX = brickSprite1.x
                    paddleBounces = 0
                    brickSpawn = False
                    currentScore += 2
                    thumby.audio.play(440, 200)
                    if (poweredUp == False):
                        if (ballDir == 2):
                            ballDir = 3
                        if (ballDir == 1):
                            ballDir = 0
            
                if (brickSpawn == True and ((ballX >= (brickSprite1.x + 7)) and ((ballX >= (brickSprite1.x + 9)) and (ballY + 6) >= (brickSprite1.y - 1)) and (ballY <= (brickSprite1.y + 5)))):
                    brickX = brickSprite1.x
                    paddleBounces = 0
                    brickSpawn = False
                    currentScore += 2
                    thumby.audio.play(440, 200)
                    if (poweredUp == False):
                        if (ballDir == 0):
                            ballDir = 1
                        if (ballDir == 3):
                            ballDir = 2
            
                #DETECT BALL COLLISSION WITH SUPER BRICK
                if (superBrickSpawn == True and ((ballY + 6) >= (brickSprite2.y - 1)) and ((ballY + 6) <= (brickSprite2.y + 1)) and (ballX <= (brickSprite2.x + 9)) and ((ballX + 6) >= (brickSprite2.x - 1))):
                    prevBrickX = brickSprite2.x
                    superBrickSpawn = False
                    brickSpawn = True
                    currentScore += 4
                    thumby.audio.play(440, 200)
                    if (poweredUp == False):
                        if ballDir == 0:
                            ballDir = 3
                        if ballDir == 1:
                            ballDir = 2
            
                if (superBrickSpawn == True and (ballY >= (brickSprite2.y + 3)) and (ballY <= (brickSprite2.y + 5)) and (ballX <= brickSprite2.x + 9) and (ballX + 6 >= (brickSprite2.x - 1))):
                    prevBrickX = brickSprite2.x
                    superBrickSpawn = False
                    brickSpawn = True
                    currentScore += 4
                    thumby.audio.play(440, 200)
                    if (poweredUp == False):
                        if ballDir == 3:
                            ballDir = 0
                        if ballDir == 2:
                            ballDir = 1
            
                if (superBrickSpawn == True and ((ballX + 6) >= (brickSprite2.x - 1)) and ((ballX + 6) <= (brickSprite2.x + 1)) and ((ballY + 6) >= (brickSprite2.y - 1)) and (ballY <= (brickSprite2.y + 5))):
                    prevBrickX = brickSprite2.x
                    superBrickSpawn = False
                    brickSpawn = True
                    currentScore += 4
                    thumby.audio.play(440, 200)
                    if (poweredUp == False):
                        if (ballDir == 2):
                            ballDir = 3
                        if (ballDir == 1):
                            ballDir = 0
            
                if (superBrickSpawn == True and ((ballX >= (brickSprite2.x + 7)) and ((ballX <= (brickSprite2.x + 9))) and (ballY + 6) >= (brickSprite2.y - 1)) and (ballY <= (brickSprite2.y + 5))):
                    prevBrickX = brickSprite2.x
                    paddleBounces = 0
                    superBrickSpawn = False
                    brickSpawn = True
                    currentScore += 4
                    thumby.audio.play(440, 200)
                    if (poweredUp == False):
                        if (ballDir == 0):
                            ballDir = 1
                        if (ballDir == 3):
                            ballDir = 2
                
                #DETECT BALL COLLISSION WITH STANDARD BUG
                if (bugSpawn == True and ((ballY + 6) >= bugY - 1) and ((ballY + 6) <= bugY + 1) and (ballX <= bugX + 9) and ((ballX + 6) >= (bugX - 1))):
                    bugFaceDown = True
                    bugFaceCounter = 0
                    bugX = (0 - 8)
                    paddleBounces = 0
                    bugSpawn = False
                    currentScore += 8
                    thumby.audio.play(800, 200)
                    if (powerUp == False):
                        powerUp = True
                        powerUpJustUnlocked = True
                    if (poweredUp == False):
                        if ballDir == 0:
                            ballDir = 3
                        if ballDir == 1:
                            ballDir = 2
                        
                if (bugSpawn == True and (ballY >= (bugY + 7)) and (ballY <= (bugY + 9)) and (ballX <= bugX + 9) and ((ballX + 6) >= (bugX - 1))):
                    bugFaceDown = True
                    bugFaceCounter = 0
                    bugX = (0 - 8)
                    paddleBounces = 0
                    bugSpawn = False
                    currentScore += 8
                    thumby.audio.play(800, 200)
                    if (powerUp == False):
                        powerUp = True
                        powerUpJustUnlocked = True
                    if (poweredUp == False):
                        if ballDir == 3:
                            ballDir = 0
                        if ballDir == 2:
                            ballDir = 1
                
                if (bugSpawn == True and ((ballX + 6) >= (bugX - 1)) and ((ballX + 6) <= (bugX + 1)) and ((ballY + 6) >= (bugY - 1)) and (ballY <= (bugY + 9))):
                    bugFaceDown = True
                    bugFaceCounter = 0
                    bugX = (0 - 8)
                    paddleBounces = 0
                    bugSpawn = False
                    currentScore += 8
                    thumby.audio.play(800, 200)
                    if (poweredUp == False):
                        if (ballDir == 2):
                            ballDir = 3
                        if (ballDir == 1):
                            ballDir = 0
            
                if ((bugSpawn == True) and (ballX >= (bugX + 7)) and (ballX <= (bugX + 9)) and ((ballY + 6) >= (bugY - 1)) and (ballY <= (bugY + 7))):
                    bugFaceDown = True
                    bugFaceCounter = 0
                    bugX = (0 - 8)
                    paddleBounces = 0
                    bugSpawn = False
                    currentScore += 8
                    thumby.audio.play(800, 200)
                    if (poweredUp == False):
                        if (ballDir == 0):
                            ballDir = 1
                        if (ballDir == 3):
                            ballDir = 2
                
                #DETECT BALL COLLISSION WITH RIGHT-TO-LEFT BUG
                if (bugSpawnRight == True and ((ballY + 6) >= bugRightY - 1) and ((ballY + 6) <= bugRightY + 1) and (ballX <= bugRightX + 9) and ((ballX + 6) >= (bugRightX - 1))):
                    bugRightFaceDown = True
                    bugFaceCounterRight = 0
                    bugRightX = 73
                    paddleBouncesB = 0
                    bugSpawnRight = False
                    currentScore += 8
                    thumby.audio.play(800, 200)
                    if (powerUp == False):
                        powerUp = True
                        powerUpJustUnlocked = True
                    if (poweredUp == False):
                        if ballDir == 0:
                            ballDir = 3
                        if ballDir == 1:
                            ballDir = 2
                        
                if (bugSpawnRight == True and (ballY >= (bugRightY + 7)) and (ballY <= (bugRightY + 9)) and (ballX <= bugRightX + 9) and ((ballX + 6) >= (bugRightX - 1))):
                    bugRightFaceDown = True
                    bugFaceCounterRight = 0
                    bugRightX = 73
                    paddleBouncesB = 0
                    bugSpawnRight = False
                    currentScore += 8
                    thumby.audio.play(800, 200)
                    if (powerUp == False):
                        powerUp = True
                        powerUpJustUnlocked = True
                    if (poweredUp == False):
                        if ballDir == 3:
                            ballDir = 0
                        if ballDir == 2:
                            ballDir = 1
                
                if (bugSpawnRight == True and ((ballX + 6) >= (bugRightX - 1)) and ((ballX + 6) <= (bugRightX + 1)) and ((ballY + 6) >= (bugRightY - 1)) and (ballY <= (bugRightY + 9))):
                    bugRightFaceDown = True
                    bugFaceCounterRight = 0
                    bugRightX = 73
                    paddleBouncesB = 0
                    bugSpawnRight = False
                    currentScore += 8
                    thumby.audio.play(800, 200)
                    if (poweredUp == False):
                        if (ballDir == 2):
                            ballDir = 3
                        if (ballDir == 1):
                            ballDir = 0
            
                if ((bugSpawn == True) and (ballX >= (bugRightX + 7)) and (ballX <= (bugRightX + 9)) and ((ballY + 6) >= (bugRightY - 1)) and (ballY <= (bugRightY + 7))):
                    bugRightFaceDown = True
                    bugFaceCounterRight = 0
                    bugRightX = 73
                    paddleBouncesB = 0
                    bugSpawnRight = False
                    currentScore += 8
                    thumby.audio.play(800, 200)
                    if (poweredUp == False):
                        if (ballDir == 0):
                            ballDir = 1
                        if (ballDir == 3):
                            ballDir = 2
    
        if (brickSpawn == True):
            thumby.display.drawSprite(brickSprite1)
        
        if (superBrickSpawn == True):
            thumby.display.drawSprite(brickSprite2)
    
        if (thumby.buttonL.pressed() == True and paddleX > 0 and paused == False):
            paddleX -= (2 * gameSpeed)
    
        if (thumby.buttonR.pressed() == True and paddleX < 64 and paused == False):
            paddleX += (2 * gameSpeed)
    
        if (paddleX < 0):
            paddleX = 0
        
        if (paddleX > 64):
            paddleX = 64
        
        if (thumby.buttonU.pressed() == True and ballSpawn == False):
            ballSpawn = True
        
        if (thumby.buttonA.justPressed() == True and ballSpawn == True):
            if (paused == False):
                paused = True
            else:
                paused = False
        
        if (thumby.buttonB.pressed() == True and powerUp == True):
            poweredUp = True
        
        if (thumby.buttonB.pressed() == False):
            poweredUp = False
        
    elif (gameState == 1 and gameOver == True):
        thumby.display.drawText("Game Over", 16, 0, 1)
        thumby.display.drawText("B = Try Again", 8, 10, 1)
        thumby.display.drawText("A = Title", 8, 16, 1)
        if (currentScore > highScore):
            thumby.saveData.setItem("highscore", currentScore)
            thumby.saveData.save()
            highScore = currentScore
            newHighScore = True
        
        if (newHighScore == True):
            thumby.display.drawText("New High Score!", 4, 24, 1)
        
        if (thumby.buttonA.pressed() == True):
            newHighScore = False
            currentScore = 0
            gameState = 2
        if (thumby.buttonB.pressed() == True):
            newHighScore = False
            currentScore = 0
            paddleX = 0
            paddleY = 32
            
            ballDir = 2
            
            paddleBounces = 0
            brickSpawn = False
            
            ballSpawn = False
            ballSpawnStart = True
            musicMarker = 0
            
            bugSpawn = False
            bugSpawnRight = False
            bugFaceDown = True
            bugRightFaceDown = True
            bugFaceCounter = 0
            bugFaceCounterRight = 0
            
            bossReached = False
    
            bossMode = False
                
            bossSpawn1 = False
            bossDefeated = False
            bossSpawnCounter = 0
            bossHealth = 0
            bossSpawn1Complete = False
                
            boss1X = (0 - 10)
            boss1Y = 11
                
            boss1Face = 0
            boss1FaceCounter = 0
            boss1MovingRight = True
            
            powerUp = False
            powerUpJustUnlocked = False
            
            gameOver = False
    elif (gameState == 2):
        time.sleep(1) # delay game for a second so player can read closing message
        titleOption = 0
        gameState = 0
    elif (gameState == 3):
        time.sleep(1) # delay game for a second so player can read closing message
        gameState = 4
    elif (gameState == 4):
        thumby.display.drawText("Music Options", 12, 0, 1)
        if (thumby.buttonA.pressed() == True):
            gameState = 5
        if (thumby.buttonB.pressed() == True):
            gameState = 5
        
        if (musicOption == 0):
            musicMarker = 0
            musicTracker = 0
            thumby.display.drawText("No Music >", 8, 10, 1)
            if (thumby.buttonR.justPressed() == True):
                musicOption = 1
                musicPlaying = True
        
        if (musicOption == 1):
            thumby.display.drawText("< Theme A >", 8, 10, 1)
            if (thumby.buttonL.justPressed() == True):
                musicOption = 0
                musicPlaying = False
            if (thumby.buttonR.justPressed() == True):
                musicOption = 2
                musicMarker = 0
                musicTracker = 0
                
        
        if (musicOption == 2):
            thumby.display.drawText("< Theme B", 8, 10, 1)
            if (thumby.buttonL.justPressed() == True):
                musicOption = 1
                musicMarker = 0
                musicTracker = 0
        
        if (musicPlaying == True):
            if (musicOption == 1):
                musicTracker = time.ticks_ms()
                if (musicTracker > 0):
                    musicMarker += (time.ticks_ms() % 1000)
                
                if (musicMarker >= 0):
                    if (musicMarker <= 50):
                        thumby.audio.play(150, 50)
                    elif (musicMarker >= 100 and musicMarker < 150):
                        thumby.audio.play(100, 50)
                    elif (musicMarker >= 200 and musicMarker < 250):
                        thumby.audio.play(150, 50)
                    elif (musicMarker >= 250 and musicMarker < 300):
                        thumby.audio.play(100, 50)
                    elif (musicMarker > 400):
                        musicMarker = 0
            elif (musicOption == 2):
                musicTracker = time.ticks_ms()
                if (musicTracker > 0):
                    musicMarker += (time.ticks_ms() % 1000)
                
                if (musicMarker >= 0):
                    if (musicMarker <= 50):
                        thumby.audio.play(100, 50)
                    elif (musicMarker >= 100 and musicMarker < 150):
                        thumby.audio.play(100, 50)
                    elif (musicMarker >= 200 and musicMarker < 250):
                        thumby.audio.play(150, 50)
                    elif (musicMarker >= 275):
                        musicMarker = 0
        
        thumby.saveData.setItem("music", musicOption)
        thumby.saveData.save()
    elif (gameState == 5):
        time.sleep(1) # delay game for a second so player can read closing message
        gameState = 0
    elif (gameState == 6):
        time.sleep(1) # delay game for a second so player can read closing message
        gameState = 7
    elif (gameState == 7):
        thumby.display.drawText("High Score", 12, 0, 1)
        thumby.display.drawText("S: %d" % highScore, 8, 10, 1)
        if (thumby.inputPressed() == True):
            gameState = 8
    elif (gameState == 8):
        time.sleep(1)
        gameState = 0
    elif (gameState == 9):
        time.sleep(1)
        gameState = 1
    
    thumby.display.update()
