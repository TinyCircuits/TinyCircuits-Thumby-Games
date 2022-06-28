import time
import thumby
import math
import random
import machine

# Code Taken From https://thumby.us/Code-Editor/Making-a-game/
# Made Additions to the Original Code
# Game Based on BOUNCER, a PC game I made in Game Maker Studio 2

ballMap = bytearray([6,15,15,6]) # BITMAP: width: 4, height: 4
padMap = bytearray([7,7,7,7,7,7,7,7,7,7]) # BITMAP: width: 10, height: 3
brickMap  = bytearray([7,7,7,7]) # BITMAN: width: 6, height: 4

# Sprite data
ballSprite = thumby.Sprite(4, 4, ballMap, key=0)
padSprite = thumby.Sprite(10, 3, padMap, key=0)
brickSprite = thumby.Sprite(6, 4, brickMap, key=0)
ballSprite.x = 33 # Initial placement of ball and movable game pad
ballSprite.y = 31
padSprite.x = 31
padSprite.y = 36
brickSprite.x = random.randint(2, 60)
brickSprite.y = 20

# Initial ball direction and movement 
ballDir = 2
ballMove = 1

# Game global variables
lose = False  
gamePlay = False
paddleBounce = 0 # keeps track of the number of bounces off of Paddle
totalBounce = 0 # keeps track of the number of bounces off of everything
loopCtr = 0 # used to control the speed of the ball
thumby.display.setFPS(35) # standardize display speed

# Begin main game loop that runs for the course of the game
while(1):
    thumby.display.fill(0) # Fill canvas to black
    
    # Title Screen
    if (gamePlay == False and lose == False):
        thumby.display.fill(0)
        thumby.display.drawText("Bouncer", 15, 0, 1)
        thumby.display.drawText("Press A/B", 9, 32, 1)
        thumby.display.update()
        
        while(thumby.actionPressed() == True):
            pass
        while(thumby.actionPressed() == False):
            pass
        
        if(thumby.buttonA.pressed() == True or thumby.buttonB.pressed() == True):
            gamePlay = True
        
    elif (gamePlay == True and lose == False):
        thumby.display.drawText("P %d" % paddleBounce, 5, 0, 1)
        thumby.display.drawText("T %d" % totalBounce, 5, 10, 1)
        
        # MOVE BALL PADDLE
        if (thumby.buttonL.pressed() == True and padSprite.x > 0 ):
            padSprite.x -= 1
        if (thumby.buttonR.pressed() == True and padSprite.x < 62 ): # 72 - width of ball paddle Sprite (10)
            padSprite.x += 1
        
        # MOVE BALL W/ MATH-GIC at half speed of game pad
        loopCtr += 1
        if(loopCtr % 2 == 0):
            # Ball movement directions following the pattern:
            #   3 \/ 2
            #   0 /\ 1
            if ballDir == 0: 
                ballSprite.x -= ballMove # left-down
                ballSprite.y += ballMove
            if ballDir == 1:
                ballSprite.x += ballMove # right-down
                ballSprite.y += ballMove
            if ballDir == 2:
                ballSprite.x += ballMove # right-up
                ballSprite.y -= ballMove
            if ballDir == 3:
                ballSprite.x -= ballMove # left-up
                ballSprite.y -= ballMove

        # DETECT BALL COLLISION WITH WALL & REDIRECT BALL
        if ballSprite.x <= 0 and ballDir == 0: # left side of screen |/ 0-ld, 2-ru
            ballDir = 1                        #                     |\ 1-rd, 3-lu
            totalBounce += 1
            thumby.audio.play(200, 200)
        elif ballSprite.x <= 0 and ballDir == 3: 
            ballDir = 2
            totalBounce += 1
            thumby.audio.play(200, 200)
        elif (ballSprite.x + 4) >= 72 and ballDir == 1: # right side of screen 
            ballDir = 0
            totalBounce += 1
            thumby.audio.play(200, 200)
        elif (ballSprite.x + 4) >= 72 and ballDir == 2: 
            ballDir = 3
            totalBounce += 1
            thumby.audio.play(200, 200)
        elif ballSprite.y <= 0 and ballDir == 2: # top of screen
            ballDir = 1
            totalBounce += 1
            thumby.audio.play(200, 200)
        elif ballSprite.y <= 0 and ballDir == 3: 
            ballDir = 0
            totalBounce += 1
            thumby.audio.play(200, 200)
        elif (ballSprite.y + 4) >= 40 and ballDir == 1:  # bottom of screen 
            ballDir = 2
            lose = True
        elif (ballSprite.y + 4) >= 40 and ballDir == 0: 
            ballDir = 3
            lose = True

        # DETECT BALL COLLISION WITH MOVING PAD
        if (((ballSprite.y + 4) == padSprite.y) and ((ballSprite.x<= padSprite.x + 10) and (ballSprite.x + 4 >= padSprite.x))):
            if ballDir == 0:
                ballDir = 3
                paddleBounce += 1
                totalBounce += 1
                thumby.audio.play(440, 200)
            if ballDir == 1:
                ballDir = 2
                paddleBounce += 1
                totalBounce += 1
                thumby.audio.play(440, 200)
         
         # DETECT BALL COLLISION WITH BRICK
        if (((ballSprite.y - 4) == brickSprite.y) and ((ballSprite.x<= brickSprite.x + 6) and (ballSprite.x + 4 >= brickSprite.x))):
            brickSprite.x = random.randint(2, 60)
            totalBounce += 1
            thumby.audio.play(440, 200)
            if ballDir == 3:
                ballDir = 0
            if ballDir == 2:
                ballDir = 1
        if (((ballSprite.y + 4) == brickSprite.y) and ((ballSprite.x<= brickSprite.x + 6) and (ballSprite.x + 4 >= brickSprite.x))):
            brickSprite.x = random.randint(2, 60)
            totalBounce += 1
            thumby.audio.play(440, 200)
            if ballDir == 0:
                ballDir = 3
            if ballDir == 1:
                ballDir = 2
        
        # DISPLAY SPRITES & UPDATE SCREEN
        thumby.display.drawSprite(padSprite)
        thumby.display.drawSprite(ballSprite)
        thumby.display.drawSprite(brickSprite)
        thumby.display.update()
        
    elif (gamePlay == True and lose == True):
        thumby.display.fill(0)
        thumby.display.drawText("Game over!", 7, 1, 1)
        thumby.display.drawText("P %d" % paddleBounce, 10, 10, 1)
        thumby.display.drawText("T %d" % totalBounce, 40, 10, 1)
        thumby.display.drawText("Again?", 18, 22, 1)
        thumby.display.drawText("A:N B:Y", 15, 32, 1)
        thumby.display.update()
        
        while(thumby.actionPressed() == True):
            pass
        while(thumby.actionPressed() == False):
            pass
        
        if(thumby.buttonA.pressed() == True):
            machine.reset() 
            
        elif(thumby.buttonB.pressed() == True):
            lose = False
            paddleBounce = 0
            totalBounce = 0
            ballSprite.x = 33
            ballSprite.y = 31
            padSprite.x = 31
            padSprite.y = 36
            brickSprite.x = random.randint(2, 60)
            thumby.display.update()
