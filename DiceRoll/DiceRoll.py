import time
import thumby
import random
import math

# BITMAP: width: 30, height: 30
template = bytearray([252,6,243,249,253,253,253,253,253,253,253,253,253,253,253,253,253,253,253,253,253,253,253,253,253,253,249,243,6,252,
           255,0,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,0,255,
           255,0,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,0,255,
           15,24,51,39,47,47,47,47,47,47,47,47,47,47,47,47,47,47,47,47,47,47,47,47,47,47,39,51,24,15])

# BITMAP: width: 30, height: 30
die6 = bytearray([252,6,243,249,253,29,29,29,29,253,253,253,253,253,253,253,253,253,253,253,253,29,29,29,29,253,249,243,6,252,
           255,0,255,255,255,30,30,30,30,255,255,255,255,255,255,255,255,255,255,255,255,30,30,30,30,255,255,255,0,255,
           255,0,255,255,255,30,30,30,30,255,255,255,255,255,255,255,255,255,255,255,255,30,30,30,30,255,255,255,0,255,
           15,24,51,39,47,46,46,46,46,47,47,47,47,47,47,47,47,47,47,47,47,46,46,46,46,47,39,51,24,15])
           
# BITMAP: width: 30, height: 30
die5 = bytearray([252,6,243,249,253,29,29,29,29,253,253,253,253,253,253,253,253,253,253,253,253,29,29,29,29,253,249,243,6,252,
           255,0,255,255,255,254,254,254,254,255,255,255,255,31,31,31,31,255,255,255,255,254,254,254,254,255,255,255,0,255,
           255,0,255,255,255,31,31,31,31,255,255,255,255,254,254,254,254,255,255,255,255,31,31,31,31,255,255,255,0,255,
           15,24,51,39,47,46,46,46,46,47,47,47,47,47,47,47,47,47,47,47,47,46,46,46,46,47,39,51,24,15])

# BITMAP: width: 30, height: 30
die4 = bytearray([252,6,243,249,253,29,29,29,29,253,253,253,253,253,253,253,253,253,253,253,253,29,29,29,29,253,249,243,6,252,
           255,0,255,255,255,254,254,254,254,255,255,255,255,255,255,255,255,255,255,255,255,254,254,254,254,255,255,255,0,255,
           255,0,255,255,255,31,31,31,31,255,255,255,255,255,255,255,255,255,255,255,255,31,31,31,31,255,255,255,0,255,
           15,24,51,39,47,46,46,46,46,47,47,47,47,47,47,47,47,47,47,47,47,46,46,46,46,47,39,51,24,15])

# BITMAP: width: 30, height: 30
die3 = bytearray([252,6,243,249,253,253,253,253,253,253,253,253,253,253,253,253,253,253,253,253,253,29,29,29,29,253,249,243,6,252,
           255,0,255,255,255,255,255,255,255,255,255,255,255,31,31,31,31,255,255,255,255,254,254,254,254,255,255,255,0,255,
           255,0,255,255,255,31,31,31,31,255,255,255,255,254,254,254,254,255,255,255,255,255,255,255,255,255,255,255,0,255,
           15,24,51,39,47,46,46,46,46,47,47,47,47,47,47,47,47,47,47,47,47,47,47,47,47,47,39,51,24,15])

# BITMAP: width: 30, height: 30
die2 = bytearray([252,6,243,249,253,253,253,253,253,253,253,253,253,253,253,253,253,253,253,253,253,29,29,29,29,253,249,243,6,252,
           255,0,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,254,254,254,254,255,255,255,0,255,
           255,0,255,255,255,31,31,31,31,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,0,255,
           15,24,51,39,47,46,46,46,46,47,47,47,47,47,47,47,47,47,47,47,47,47,47,47,47,47,39,51,24,15])

# BITMAP: width: 30, height: 30
die1 = bytearray([252,6,243,249,253,253,253,253,253,253,253,253,253,253,253,253,253,253,253,253,253,253,253,253,253,253,249,243,6,252,
           255,0,255,255,255,255,255,255,255,255,255,255,255,31,31,31,31,255,255,255,255,255,255,255,255,255,255,255,0,255,
           255,0,255,255,255,255,255,255,255,255,255,255,255,254,254,254,254,255,255,255,255,255,255,255,255,255,255,255,0,255,
           15,24,51,39,47,47,47,47,47,47,47,47,47,47,47,47,47,47,47,47,47,47,47,47,47,47,39,51,24,15])

# Setup
diceRoll = False
setupRollStart = False
startRollTimerMax = 50
startRollTimer = 1
rollSpeed = 10
howManyTurns = random.randint(5, 15)
currentDieNumber = random.randint(0, 5)
buttonPressed = False
textX = 50
textY = 16
bitmapX = 10
bitmapY = 4

# Limit game refresh rate to 30 times a second, max
thumby.display.setFPS(30)
thumby.display.setFont("/lib/font8x8.bin", 8, 8, 1)

# Set up a new roll
def setupRoll():
    global setupRollStart, startRollTimer
    setupRollStart = True
    startRollTimer = 1

# Begin main game loop that runs for the course of the game
while(True):
    thumby.display.fill(0) # Fill canvas to black

    theNumber = currentDieNumber
    theTime = time.ticks_ms()
    textYBob = int(math.sin(theTime / 200) * 5)
    
    if thumby.buttonA.pressed() or thumby.buttonB.pressed():
        if not buttonPressed:
            buttonPressed = True
    
    if buttonPressed:
        if not diceRoll:
            diceRoll = True
            startDieNumber = random.randint(0, 5)
            howManyTurns = random.randint(5, 15)
        
        else:
            if not setupRollStart:
                setupRoll()
    
            else:
                if howManyTurns > 0:
                    # Start counter to show next number
                    startRollTimer += rollSpeed
            
                    # Timer done, get new number and reset timers
                    if startRollTimer >= startRollTimerMax:
                        howManyTurns -= 1
                        currentDieNumber = random.randint(0, 5)
                        startRollTimer = 1
                            
                else:
                    buttonPressed = False
                    diceRoll = False
    
    # Get correct die to display
    if currentDieNumber == 0:
        bitmap = die1
    elif currentDieNumber == 1:
        bitmap = die2
    elif currentDieNumber == 2:
        bitmap = die3
    elif currentDieNumber == 3:
        bitmap = die4
    elif currentDieNumber == 4:
        bitmap = die5
    else:
        bitmap = die6
    
    if diceRoll:
        # Draw the current random die value while rolling
        thumby.display.drawText(str(currentDieNumber + 1), textX, textY, 1)
        thumby.display.blit(bitmap, bitmapX, bitmapY, 30, 30, -1, 0, 0)
        
    else:
        # Else draw the last landed number
        thumby.display.drawText(str(theNumber + 1), textX, textY + textYBob, 1)
        thumby.display.blit(bitmap, bitmapX, bitmapY, 30, 30, -1, 0, 0)
    
    # Update screen
    thumby.display.update()
