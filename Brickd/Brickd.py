import time
import thumby
import math

# Bitmaps
ballMap = bytearray([6,15,15,6]) # BITMAP: width: 4, height: 4
padMap = bytearray([1,3,7,7,7,7,7,7,3,1]) # BITMAP: width: 10, height: 3
brickMap  = bytearray([7,7,7,7,7,7]) # BITMAP: width: 6, height: 3
brickW = 6
brickH = 3

# Initial ball direction and movement 
ballDir = 2
ballMove = 1

# Sprite data
brickSprite = thumby.Sprite(brickW, brickH, brickMap, key=0) # w, h, bitmapData, key
ballSprite = thumby.Sprite(4, 4, ballMap, key=0)
padSprite = thumby.Sprite(10, 3, padMap, key=0)
ballSprite.x = 33 # Initial placement of ball and movable game pad
ballSprite.y = 31
padSprite.x = 31
padSprite.y = 36

# Game global variables
lose = False  
gameScore = 0 # keeps track of the number of bricks collided with
loopCtr = 0 # used to control the speed of the ball
thumby.display.setFPS(35) # standardize display speed

# Brick class to keep track of placement, collisions and delete (move off screen) state
class Brick:
    def __init__(self, x, y, collisions):
        self.x = x
        self.y = y
        self.collisions = collisions
        
    def delete(self):
        self.x = -100
        self.y = -100

# Create a list of bricks that covers three rows across the screen
listOfBricks = []
for i in range (0, 10):
    listOfBricks.append(Brick(1 + (i*7), 1, 0))
    listOfBricks.append(Brick(1 + (i*7), 5, 0))
    listOfBricks.append(Brick(1 + (i*7), 9, 0))

# TITLE SCREEN 
thumby.display.fill(0)
thumby.display.drawRectangle(12, 4, 48, 12, 1) # x, y, w, h, color
thumby.display.drawText("Brick'd", 16, 6, 1) # string, x, y, color

for i in range(0, 5): # bricks across the screen for flare 
    thumby.display.drawFilledRectangle(1 + (i*14), 20, brickW, brickH, 1) # x, y, w, h, color
    thumby.display.drawFilledRectangle(8 + (i*14), 24, brickW, brickH, 1) 

thumby.display.update()

# Flashing line under Press A/B
thumby.display.drawText("Press A/B", 10, 32, 1)
while(thumby.buttonA.pressed() == False and thumby.buttonB.pressed() == False):
    if(time.ticks_ms() % 1000 < 500):
        thumby.display.drawLine(10, 39, 62, 39, 0)
    else:
        thumby.display.drawLine(10, 39, 62, 39, 1)
        
    thumby.display.update()
    pass

# Game Instructions
thumby.display.fill(0)
thumby.display.drawText("Game Instr:", 0, 0, 1) # string, x, y, color
thumby.display.drawLine(0, 8, 62, 8, 1)
thumby.display.drawText("Hit Ball &", 0, 10, 1)
thumby.display.drawText("Break Bricks", 0, 19, 1)
thumby.display.update()
time.sleep(4) # delay game for a few seconds so player can read instructions

# Begin main game loop
while(1):
    thumby.display.fill(0) # Fill canvas to black

    # MOVE BALL PADDLE
    if (thumby.buttonL.pressed() == True and padSprite.x > 0 ):
        padSprite.x -= 1
    if (thumby.buttonR.pressed() == True and padSprite.x < 62 ): #72-width
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
    elif ballSprite.x <= 0 and ballDir == 3: 
        ballDir = 2
    elif (ballSprite.x + 4) >= 72 and ballDir == 1: # right side of screen 
        ballDir = 0
    elif (ballSprite.x + 4) >= 72 and ballDir == 2: 
        ballDir = 3
    elif ballSprite.y <= 0 and ballDir == 2: # top of screen
        ballDir = 1
    elif ballSprite.y <= 0 and ballDir == 3: 
        ballDir = 0
    
    # DETECT BALL COLLISION WITH MOVING PAD
    if (((ballSprite.y + 4) == padSprite.y) and ((ballSprite.x<= padSprite.x + 10) and (ballSprite.x + 4 >= padSprite.x))):
        if ballDir == 0:
            ballDir = 3
        if ballDir == 1:
            ballDir = 2
    
    # CHECK IF LOST GAME ;/
    if ballSprite.y >= 38: 
        lose = True
    
    # DETECT BALL COLLISION WITH BRICK
    for brick in listOfBricks:    
        # if ball at ballX * ballY checked against Brick.x + width, Brick y + height
        if (((ballSprite.x < brick.x + brickH) and (ballSprite.x + 4 > brick.x)) and ((brick.y < ballSprite.y + 4) and (brick.y + brickW > ballSprite.y))):
            brick.collisions = 1
            gameScore += 1
            # Play a sound at 440 hz for 300ms
            thumby.audio.play(440, 300) # play happy sound when brick is deleted
            
            if ballDir == 0: ballDir = 1
            if ballDir == 1: ballDir = 0
            if ballDir == 2: ballDir = 1
            if ballDir == 3: ballDir = 0
            
        if brick.collisions == 0:
            # thumby.display.blit(brickMap, brick.x, brick.y, brickW, brickH, 0, 0, 0)
            brickSprite.x = brick.x
            brickSprite.y = brick.y
            thumby.display.drawSprite(brickSprite) 
        else:
            brick.delete()
    
    # GAME OVER SCREEN
    if lose == True or gameScore == 30:
        thumby.display.fill(0)
        # CHECK IF WON GAME
        if gameScore == 30:
            thumby.display.drawText("You won!", 10, 5, 1) # text, x, y, color
        elif lose == True: # OR LOST...
            thumby.audio.play(260, 250) # losing sound
            thumby.display.drawText("Game Over", 10, 5,1)
        
        thumby.display.drawText("Replay?", 15, 20, 1)
        thumby.display.drawText("A:N B:Y", 15, 30, 1)
        
        if time.ticks_ms() % 1000 < 500:
            thumby.display.drawLine(15, 37, 55, 37, 1) # (x1, y1, x2, y2, color)
        else:
            thumby.display.drawLine(15, 37, 55, 37, 0)
        
        if thumby.buttonA.pressed(): # go back to game menu
            thumby.reset() 
            
        elif thumby.buttonB.pressed(): # Re-initialize values of variables to play again
            lose = False  
            gameScore = 0 
            loopCtr = 0 
            ballDir = 2
            ballMove = 1
            ballSprite.x = 33
            ballSprite.y = 31
            padSprite.x = 31
            padSprite.y = 36
        
            # Re-init list of bricks
            listOfBricks = []
            for i in range (0, 10):
                listOfBricks.append(Brick(1 + (i*7), 1, 0))
                listOfBricks.append(Brick(1 + (i*7), 5, 0))
                listOfBricks.append(Brick(1 + (i*7), 9, 0))
            
    else:
        # DISPLAY IT ALL
        thumby.display.drawSprite(ballSprite)
        thumby.display.drawSprite(padSprite)

    # UPDATE SCREEN
    thumby.display.update()
