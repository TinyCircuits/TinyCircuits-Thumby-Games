import time
import thumby
import machine
import math, random

machine.freq(48000000)

# Global constants
caveXMax = 10000
caveHeightStart = 38
caveHeightMin = 24
caveSpeedStart = 2
caveSpeedMax = 5
period = 50
width = 4
gravity = 0.175
obstacleWidth = 6
obstacleHeight = 8
obstacleSpawnPeriodBase = 5000 # ms

# Global dynamics
heliSprite = thumby.Sprite(10, 6, "/Games/TinyHeli/heliSpr.bin", key=0)
missileSprite = thumby.Sprite(6, 3, "/Games/TinyHeli/missileSpr.bin", key=0)
caveX = None
caveHeight = None
caveSpeed = None
seed = None
heliYVelocity = None
score = None
showScoreCounter = None
framesSinceLastScore = None
currentSoundFreq = None
caveSegments = None
missileFired = None
obstaclePos = None
obstacleLastSpawnTime = None


def drawCave(caveX):
    while len(caveSegments) == 0 or caveSegments[-1]["x"] < thumby.display.width + width:
        x = None
        if len(caveSegments) > 0:
            x = caveSegments[-1]["x"] + width
        else:
            x = 0
    
        x1 = int((caveX+x) / period) * period
        x2 = x1 + period
        
        random.seed(x1 + seed)
        y1 = random.randint(0, 64)
        
        random.seed(x2 + seed)
        y2 = random.randint(0, 64)
        
        # Cosine interpolation
        mu2 = (1 - math.cos((((caveX+x) - x1) / (x2 - x1)) * math.pi))/2
        noise = (y1 * (1-mu2) + y2 * mu2) / 64
        
        y = 1 + math.floor((noise * (thumby.display.height - caveHeight-1)))
        # caveSegments.append((y, caveHeight-1))
        caveSegments.append({"x":x, "y":y, "h":caveHeight-1})
    
    while caveSegments[0]["x"] + width < 0:
        caveSegments.pop(0)
    
    for s in range(0, len(caveSegments), 1):
        caveSegments[s]["x"] -= caveSpeed
        thumby.display.drawFilledRectangle(caveSegments[s]["x"], caveSegments[s]["y"], width, caveSegments[s]["h"], 0)
    
    # Handle drawing or spawning the obstacle
    global obstacleLastSpawnTime
    global obstaclePos
    
    t = time.ticks_ms()
    if t - obstacleLastSpawnTime > obstacleSpawnPeriodBase + random.randint(0, 5000) and obstaclePos["x"] == -obstacleWidth:
        obstacleLastSpawnTime = t
        obstaclePos["x"] = thumby.display.width
        randomMargin = int((caveSegments[-1]["h"] - obstacleHeight)/2)
        obstaclePos["y"] = (caveSegments[-1]["y"] + caveSegments[-1]["h"]/2 - obstacleHeight/2) + random.randint(-randomMargin, randomMargin)
    elif obstaclePos["x"] > -obstacleWidth:
        obstaclePos["x"] -= caveSpeed
        thumby.display.drawFilledRectangle(int(obstaclePos["x"]), int(obstaclePos["y"]), obstacleWidth, obstacleHeight, 1)
    elif obstaclePos["x"] < -obstacleWidth:
        obstaclePos["x"] = -obstacleWidth


def showStartScreen():
    # Used for animating heli sprite on start screen
    justStarted = True
    
    # Run start screen main loop
    while thumby.buttonA.pressed() == False and thumby.buttonB.pressed() == False:
        thumby.display.fill(0)
        thumby.display.drawText("TinyHeli", 12, 1, 1)
        
        # Flicker start screen info
        if time.ticks_ms() % 1000 < 500:
            thumby.display.drawText("Press A/B", 9, 32, 1)
        else:
            thumby.display.drawFilledRectangle(8, 31, 55, 9, 1)
            thumby.display.drawText("Press A/B", 9, 32, 0)
            
        
        # If just started or the sprite as gone off the screen a random amount, place the sprite at the start
        if justStarted == True or heliSprite.x > thumby.display.width + random.randint(10, 150):
            justStarted = False
            heliSprite.x = -10
            randY = heliSprite.y
            while randY == heliSprite.y:
                randY = random.randint(9, 22)
            heliSprite.y = randY
        
        # Progress the sprite and show
        heliSprite.x += 0.5
        thumby.display.drawSprite(heliSprite)
        heliSprite.setFrame(heliSprite.currentFrame+1)
        
        
        thumby.display.update()


def showEndScreen():
    # Play death sound
    for f in range(500, 900, 1):
        thumby.audio.playBlocking(f, 1)
    thumby.audio.stop()
    
    # Wait for a button to not be pressed
    while thumby.buttonA.pressed() or thumby.buttonB.pressed():
        pass
    
    # Run the end screen
    while True:
        thumby.display.fill(0)
        thumby.display.drawText("You crashed!", 2, 1, 1)
        
        # Display the score nicely
        thumby.display.drawText("-Score-", 15, 12, 1)
        if(len(str(score)) == 3):
            thumby.display.drawText(str(score), 26, 21, 1)
        elif(len(str(score)) == 2):
            thumby.display.drawText(str(score), 29, 21, 1)
        else:
            thumby.display.drawText(str(score), 32, 21, 1)
        
        if time.ticks_ms() % 1000 < 500:
            thumby.display.drawText("Again? A", 12, 32, 1)
        else:
            thumby.display.drawFilledRectangle(11, 31, 49, 9, 1)
            thumby.display.drawText("Again? A", 12, 32, 0)
        thumby.display.update()
        
        if thumby.buttonA.pressed():
            return True
        elif thumby.buttonB.pressed():
            machine.reset()


def handleInput():
    if thumby.buttonA.pressed() or thumby.buttonB.pressed():
        global heliYVelocity
        
        # When button pressed, make responce instant
        if heliYVelocity > 0:
            heliYVelocity = gravity/2
        
        # Accelerate up
        heliYVelocity -= gravity*1.85
    
    # Let the user slide the helicopter left or right
    if thumby.buttonR.pressed() and heliSprite.x + 23 < thumby.display.width:
        heliSprite.x = heliSprite.x + 1
    elif thumby.buttonL.pressed() and heliSprite.x -1 > 0:
        heliSprite.x = heliSprite.x - 1
    
    # Spawn a missile
    global missileFired
    if thumby.buttonD.pressed() and missileFired == False:
        missileSprite.x = heliSprite.x+11
        missileSprite.y = heliSprite.y+2
        missileFired = True


def checkCollision():
    # Check if the helicopter hit a white pixel (cave or obstacle) or went out of bound on y
    if thumby.display.getPixel(heliSprite.x, heliSprite.y) == 1 or thumby.display.getPixel(heliSprite.x+9, heliSprite.y) == 1 or thumby.display.getPixel(heliSprite.x, heliSprite.y+5) == 1 or thumby.display.getPixel(heliSprite.x+9, heliSprite.y+5) == 1:
        return showEndScreen()
    elif heliSprite.y < 0 or heliSprite.y+8 > thumby.display.height:
        return showEndScreen()
    return False


def handleMissile():
    global missileFired
    if missileFired == True:
        # Check that missile is in thge bounds of the screen then check if inside the bounds of an obstacle
        if thumby.display.getPixel(heliSprite.x+6, heliSprite.y) == 1 or thumby.display.getPixel(heliSprite.x+6, heliSprite.y+3) == 1:
            missileFired = False
            return
        elif missileSprite.x+6 >= obstaclePos["x"] and missileSprite.x+6 <= obstaclePos["x"]+obstacleWidth:
            if (missileSprite.y >= obstaclePos["y"] and missileSprite.y <= obstaclePos["y"]+obstacleHeight) or (missileSprite.y+3 >= obstaclePos["y"] and missileSprite.y+3 <= obstaclePos["y"]+obstacleHeight):
                missileFired = False
                
                # Set the obstacle to its offscreen position (signifies another can be spawned)
                obstaclePos["x"] = -obstacleWidth
                return
        
        # Handle missile animation and despawn if offscreen
        missileSprite.setFrame(missileSprite.currentFrame+1)
        thumby.display.drawSprite(missileSprite)
        if missileSprite.x <= thumby.display.width:
            missileSprite.x += 2
        else:
            missileFired = False

    
    
thumby.display.setFPS(60)
showStartScreen()


# Main loop that restarts game if player crashes and decides to play again
while True:
    # Reset/set all game parameters each time game starts
    heliSprite.x = 0
    heliSprite.y = 16
    caveX = 0
    lastCaveX = -thumby.display.width
    caveSpeed = 1
    random.seed(time.ticks_ms())
    seed = random.randint(0, 1000)
    heliYVelocity = 0
    score = 0
    showScoreCounter = 0
    framesSinceLastScore = 0
    currentSoundFreq = 0
    caveSegments = []
    missileFired = False
    obstaclePos = {"x": -obstacleWidth, "y": 0}
    obstacleLastSpawnTime = time.ticks_ms()
    
    # Start the main game loop
    while True:
        thumby.display.fill(1)
        
        # Interpolate from starting cave height to min cave
        # height using current x and level x max for percentage
        if caveX < caveXMax:
            mu = caveX/caveXMax
            caveHeight = int(caveHeightStart*(1-mu)+caveHeightMin*mu)
            caveSpeed = int(caveSpeedStart*(1-mu)+caveSpeedMax*mu)
        
        # Draw cave and then check if the helicopter bounding box touches the cave
        drawCave(caveX)
        handleInput()
        if checkCollision() == True:
            break
        
        # Progress the cave and apply dynamics to helicopter sprite
        caveX += caveSpeed
        heliSprite.y += int(heliYVelocity)
        heliYVelocity += gravity
        
        handleMissile()
        
        # Keep track of user score
        if framesSinceLastScore < 100:
            framesSinceLastScore += 1
        else:
            score += 1
            showScoreCounter = 0
            framesSinceLastScore = 0
        
        # Show the score pop-up for a certain amount of time
        if showScoreCounter < 20:
            thumby.display.drawFilledRectangle(53, 31, 19, 9, 1)
            thumby.display.drawText(str(score), 54, 32, 0)
            showScoreCounter += 1
        
        # Play helicopter sound
        if currentSoundFreq < 130:
            currentSoundFreq += 30
            thumby.audio.play(currentSoundFreq, 100)
        else:
            currentSoundFreq = 30
        
        # Draw helicopter and update screen
        thumby.display.drawSprite(heliSprite)
        heliSprite.setFrame(heliSprite.currentFrame+1)
        thumby.display.update()









