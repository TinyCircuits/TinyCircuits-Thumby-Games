# # Version 1.0
# I still have an issue with the way the game restarts after death. The sliderate is not resetting correctly..

import time
import thumby
import math
import random
import machine

# BITMAP: width: 72, height: 40
splash = bytearray([96,96,96,96,96,224,224,0,0,0,0,0,0,0,0,0,128,128,128,128,128,128,0,0,0,0,0,0,0,0,0,0,224,224,96,96,96,96,96,96,96,96,96,96,96,96,96,96,96,96,96,96,96,96,96,96,224,224,224,224,96,96,96,96,96,96,96,96,96,96,96,96,
           48,48,48,48,48,63,63,128,224,248,28,12,198,231,115,51,25,25,25,1,1,1,3,3,7,6,12,28,248,224,128,0,63,63,48,48,48,48,48,48,48,48,48,48,48,48,48,48,48,48,48,48,48,48,48,48,63,63,63,63,48,48,48,48,48,48,48,48,48,48,48,48,
           0,0,0,0,0,0,0,63,255,224,0,3,3,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,224,255,63,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,
           0,0,0,0,0,0,0,0,0,3,7,14,12,28,24,56,48,48,48,48,48,48,56,24,28,12,14,7,3,0,0,0,0,254,254,198,198,198,198,198,198,4,0,255,255,0,0,128,192,96,96,96,192,128,0,128,192,224,96,96,224,224,0,96,96,252,252,96,96,0,0,0,
           0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,31,31,0,0,0,0,0,0,0,0,31,31,0,0,7,15,24,24,24,15,7,0,15,31,24,24,24,15,31,16,0,0,31,31,0,0,0,0,0])

splashScreen = thumby.Sprite(72, 40, splash)


# BITMAP: width: 8, height: 8
bitmap0 = bytearray([60,66,141,133,129,129,66,60])

# BITMAP: width: 73, height: 4
bitmap1 = bytearray([4,2,1,2,4,8,4,2,1,2,4,8,4,2,1,2,4,8,4,2,1,2,4,8,4,2,1,2,4,8,4,2,1,2,4,8,4,2,1,2,4,8,4,2,1,2,4,8,4,2,1,2,4,8,4,2,1,2,4,8,4,2,1,2,4,8,4,2,1,2,4])

# BITMAP: width: 8, height: 3
bitmap2 = bytearray([7,5,5,5,5,5,5,7])

# Make a sprite object using bytearray (a path to binary file from 'IMPORT SPRITE' is also valid)
bubbleSprite = thumby.Sprite(8, 8, bitmap0)
bubbleSprite.x = int((thumby.display.width/2) - (8/2))
bubbleSprite.y = int((thumby.display.height/2) - (8/2))

# Make a sprite for Spikes
spikesSprite = thumby.Sprite(73, 4, bitmap1)
spikesSprite.x = 0
spikesSprite.y = 37

# Set the FPS (without this call, the default fps is 30)
maxFPS = 60
thumby.display.setFPS(maxFPS)

# Bubble Variables
floatRate = .5
slideRate = .75

# Bar Variables
barRate = 200
barDelay = 3000
newBar = True
barsInRow = range(9)
numBarMoves = 0

# collision stuff
isHeld = False
gameRunning = True

# Time Stuff
timeStart = time.ticks_ms()
timeSplash = timeStart + 1000
timeLastMove = timeStart
timeDifficulty = timeStart

# Score
score = 0
timeScore = timeStart
scoreDelay = 500


class IterRegistry(type):
    def __iter__(cls):
        return iter(cls._registry)
        
class bar(thumby.Sprite):
    __metaclass__ = IterRegistry
    __registry = []
    def __init__(self,x):
        self.__registry.append(self)
        self.Sprite = thumby.Sprite(8, 3, bitmap2)
        self.Sprite.x = x
        self.Sprite.y = -2
        #thumby.display.drawSprite(self.Sprite)
        
    def remove(self):
        self.__registry.remove(self)
        del self
        
# Splash Screen

while(gameRunning == True):
    t0 = time.ticks_ms()   # Get time (ms)
    while time.ticks_ms() < timeSplash:
        thumby.display.fill(0)
        thumby.display.drawSprite(splashScreen)
        thumby.display.update()
    thumby.display.fill(0) # Fill canvas to black
    
    # Move all bars down
    if t0 - timeLastMove >= barRate:
        for tile in bar.__registry:
            tile.Sprite.y += 1
        if tile.Sprite.y >= 35:
            tile.remove()
        timeLastMove = t0
        numBarMoves += 1
    
    
    # Generate Row of Bars
    if newBar == True:
        newBar = False
        blank1 = random.randint(0,8)
        blank2 = random.randint(0,8)
        for i in barsInRow:
            if i != blank1 and i != blank2:
                bar(i*8)
                timeLastbar = t0
                
    # New bar trigger
    if numBarMoves >= 15:
        newBar = True
        numBarMoves = 0
    
    
    # Collision Check
    isHeld = False
    stopL = False
    stopR = False
    caughtXPos = 0
    
    for tile in bar.__registry:
        if (bubbleSprite.y <= tile.Sprite.y + 3 and bubbleSprite.y >= tile.Sprite.y) and (bubbleSprite.x <= tile.Sprite.x + 6 and bubbleSprite.x >= tile.Sprite.x - 6):
            isHeld = True
            bubbleSprite.y = tile.Sprite.y + 3
        if (bubbleSprite.y <= tile.Sprite.y + 1 and bubbleSprite.y >= tile.Sprite.y - 6) and (bubbleSprite.x <= tile.Sprite.x and bubbleSprite.x >= tile.Sprite.x - 8):
            stopR = True
            caughtXPos = tile.Sprite.x - 8
        if (bubbleSprite.y <= tile.Sprite.y + 1 and bubbleSprite.y >= tile.Sprite.y - 6) and (bubbleSprite.x <= tile.Sprite.x + 8 and bubbleSprite.x >= tile.Sprite.x):
            stopL = True
            caughtXPos = tile.Sprite.x + 8

    # NEW Handle up/down position of bubble
    if bubbleSprite.y <= 0 and isHeld == False:
        bubbleSprite.y = 0
    elif isHeld == False:
        bubbleSprite.y -= floatRate
    
    # Handle Left/right position of bubble
    if(stopL == False and thumby.buttonL.pressed() == True and bubbleSprite.x >= 1):
        bubbleSprite.x -= slideRate
    if(stopR == False and thumby.buttonR.pressed() == True and bubbleSprite.x <= 63):
        bubbleSprite.x += slideRate
        
    # Watch for Dead
    if bubbleSprite.y >= 30:
        gameRunning = False
        print("Game Over")
        
    # Draw the sprites
    thumby.display.drawSprite(bubbleSprite)    
    for tile in bar.__registry:
        thumby.display.drawSprite(tile.Sprite)
    thumby.display.drawSprite(spikesSprite)
    thumby.display.update()
    
    # Keep Score
    if t0 - timeScore >= scoreDelay:
        score += 1
        timeScore = t0
        print("score:",str(score))
    
    # Increase difficulty over time
    if t0 - timeDifficulty >= 3000 and barRate > 25:
        barRate -= barRate * .1
        print("barRate:",str(barRate))
        slideRate += slideRate*.05
        timeDifficulty = t0
        
    # Does nothing?
    #while (time.ticks_ms() - t0 < 1000 / maxFPS):
    #    pass
    
    if(gameRunning == False):
        thumby.display.fill(0)
        thumby.display.drawText("Game over!", 7, 1, 1)
        thumby.display.drawText("Score:", 1, 10, 1)
        thumby.display.drawText(str(score), 40, 10, 1)
        thumby.display.drawText("Again?", 18, 22, 1)
        thumby.display.drawText("A:N B:Y", 15, 32, 1)
        thumby.display.update()
        while(thumby.actionPressed() == False):
            pass # Wait for the user to give us something
        if(thumby.buttonA.pressed() == True):
            machine.reset()
        elif(thumby.buttonB.pressed() == True):
            for tile in bar.__registry:
                tile.Sprite.y = 40
            bubbleSprite.x = int((thumby.display.width/2) - (8/2))
            bubbleSprite.y = int((thumby.display.height/2) - (8/2))
            score = 0
            barRate = 200
            barDelay = 3000
            slideRate = .75
            timeDifficulty = t0
            newBar = True
            numBarMoves = 0
            timeStart = time.ticks_ms()
            timeLastMove = timeStart
            timeDifficulty = timeStart
            timeScore = timeStart
            gameRunning = True
            
