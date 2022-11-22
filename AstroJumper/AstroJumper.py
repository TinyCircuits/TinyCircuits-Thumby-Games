import time
import thumby
import math
import random

# Get saveData for high score
thumby.saveData.setName("AstroJumper")
    
while(1):
    # Set the FPS and font
    thumby.display.setFPS(60)
    thumby.display.setFont("/lib/font5x7.bin", 5, 7, 1)
    
    # Splash Screen setup
    astro = bytearray([0,240,240,252,254,230,230,230,230,252,0,0,254,130,130,130,130,0,0,2,2,254,2,2,0,0,254,130,130,130,254,0,0,254,2,2,2,254,0,0,
                0,7,7,63,63,15,15,15,63,63,0,0,32,32,32,32,63,0,0,0,0,63,0,0,0,0,63,1,3,12,48,0,0,63,32,32,32,63,0,0])
    
    jumper = bytearray([0,4,4,4,252,4,0,0,252,0,0,0,252,0,0,252,8,16,8,252,0,0,252,132,132,132,252,0,0,252,132,132,132,132,0,0,252,132,132,132,252,0,0,252,252,
                14,16,16,16,15,0,0,0,15,16,16,16,15,0,0,31,0,0,0,31,0,0,31,0,0,0,0,0,0,31,16,16,16,16,0,0,31,1,3,6,24,0,0,27,27])
    
    starsSprite = bytearray([0,0,0,8,0,42,0,8,0,0,0,0,132,14,4,0,0,0,0,64,64,0,88,0,64,64,0,0,0,0,0,0,16,0,0,0,0,0,0,0,10,4,10,0,0,
                0,0,16,40,16,0,0,0,0,0,2,2,13,2,2,0,0,0,0,0,0,0,3,0,0,0,0,0,1,0,0,0,17,0,0,0,1,0,0,0,0,0,0,0,0])
    
    powerUp = bytearray([36,0,153,36,36,153,0,36])

    astroSprite = thumby.Sprite(40, 15, astro)
    stars1Sprite = thumby.Sprite(45, 15, starsSprite)
    stars2Sprite = thumby.Sprite(45, 15, starsSprite)
    stars2Sprite.mirrorX = 1
    stars2Sprite.mirrorY = 1
    
    jumperSprite = thumby.Sprite(45, 15, jumper)
    astroSprite.x = 5
    stars1Sprite.x = 45
    stars2Sprite.y = 14
    jumperSprite.x = 20
    jumperSprite.y = 14
    
    astronaut= bytearray([28,254,59,59,254])
    astronautSprite = thumby.Sprite(8, 8, astronaut)
    
    platform = bytearray([1,3,7,7,7,7,3,1])
    platformSprite = thumby.Sprite(8, 2, platform)
    
    astronautSprite.x = int((thumby.display.width/2) - (8/2))
    astronautSprite.y = int(thumby.display.height - 10)
    
    platformSprite.x = int((thumby.display.width/2) - (8/2))
    platformSprite.y = thumby.display.height - 2
    
    thumby.display.fill(0) # Fill canvas to black
    thumby.display.drawSprite(astronautSprite)
    thumby.display.drawSprite(platformSprite)
    thumby.display.drawSprite(astroSprite)
    thumby.display.drawSprite(stars1Sprite)
    thumby.display.drawSprite(stars2Sprite)
    thumby.display.drawSprite(jumperSprite)
    thumby.display.update()
    
    def bounce(start):
        isFalling = True
        now = time.ticks_ms()
        x = ((now-start) / 150)
        if x >= 5:
            isFalling = True
        else:
            isFalling = False
        return (-((x-5) ** 2) + 25), isFalling
    
    
    def renderSprites(sprites):
        for i in range(0, len(sprites)):
            thumby.display.drawSprite(sprites[i])
    
    def checkPlatformJump(sprite, platforms):
        for platform in platforms:
            if (sprite.y >= platform.y - 7 and sprite.y <= platform.y - 6 and platform.x - 5 <= sprite.x <= platform.x + 5):
                thumby.audio.play(500, 100)
                thumby.audio.play(1000, 10)
                thumby.audio.play(1500, 10)
                return True
        return False
    
    def movePlatformsDown(sprites, stars, height):
        global lastMovement
        for star in stars:
            star.y = star.y - (height - lastMovement) * (random.uniform(.3, .5))
            if star.y >= thumby.display.height + 10:
                stars.remove(star)
                newStar = thumby.Sprite(1,1, bytearray([1]))
                newStar.y = 0
                newStar.x = random.randint(0, thumby.display.width)
                stars.append(newStar)
        
        for sprite in sprites:
            sprite.y = sprite.y - (height - lastMovement)
            if sprite.y >= thumby.display.height + 5:
                sprites.remove(sprite)
                newPlat = thumby.Sprite(8,2, platform)
                if (time.ticks_ms() % 2 == 0):
                    newPlat.x = random.randint(thumby.display.width - int(thumby.display.width / 2), thumby.display.width - 8)
                else: 
                    newPlat.x = random.randint(0, thumby.display.width - int(thumby.display.width /2))
                newPlat.y = 2
                sprites.append(newPlat)
        lastMovement = height
                
        return sprites, stars
    
    # Animate splash screen
    while(1):
        t0 = time.ticks_ms()   # Get time (ms)
        
        bobRate = 150
        bobRange = 2
        
        bobOffset = math.sin(t0 / bobRate) * bobRange
        
        astronautSprite.y = int(thumby.display.height - 10) + bobOffset
        
        thumby.display.fill(0) # Fill canvas to black
        thumby.display.drawSprite(platformSprite)
        thumby.display.drawSprite(astroSprite)
        thumby.display.drawSprite(stars1Sprite)
        thumby.display.drawSprite(stars2Sprite)
        thumby.display.drawSprite(jumperSprite)
        thumby.display.drawSprite(astronautSprite)
        thumby.display.update()
        
        # Start game on input
        if (thumby.inputPressed() == True):
            break
        
        
    # Initialize game
    platforms = []
    stars = []
    parallaxStars = []
    thumby.display.fill(0)
    bounceStart = time.ticks_ms()
    isFalling = False
    totalScore = 0
    astronautHeight = thumby.display.height - 10
    poweredUp = False
    powerUps = 1
    powerUpTracker = 3
    
    lastMovement = 0
    
    for i in range(0, 4):
        platforms.append(thumby.Sprite(8,2,platform))
        platforms[i].y = i * 9
        platforms[i].x = random.randint(0, thumby.display.width - 8)
    platforms.append(platformSprite)
    
    for i in range(0, 10):
        stars.append(thumby.Sprite(1,1,bytearray([1])))
        stars[i].y = random.randint(0, thumby.display.height)
        stars[i].x = random.randint(0, thumby.display.width)
        
    for i in range(0, 6):
        parallaxStars.append(thumby.Sprite(1,1,bytearray([1])))
        parallaxStars[i].y = random.randint(0, thumby.display.height)
        parallaxStars[i].x = random.randint(0, thumby.display.width)
    
    # Main game loop
    while(1):
        # Clear the screen
        thumby.display.fill(0)
        
        # If the astronaut falls below the screen, game over
        if (astronautSprite.y >= thumby.display.height + 50) and not poweredUp:
            break
        if (astronautSprite.y >= thumby.display.height + 4 and poweredUp):
            bounceStart = time.ticks_ms()
            astronautHeight = astronautSprite.y
            lastMovement = 0
            poweredUp = False
            thumby.audio.play(500, 100)
            thumby.audio.play(1000, 10)
            thumby.audio.play(1500, 10)
        
        # Check if the astronaut bounces on an random platform
        if isFalling:
            isBounce = checkPlatformJump(astronautSprite, platforms)
            if isBounce:
                bounceStart = time.ticks_ms()
                astronautHeight = astronautSprite.y
                lastMovement = 0
                poweredUp = False
    
        # Move the astronaut left or right
        if (thumby.buttonL.pressed()):
            newX = astronautSprite.x - 1
            if newX <= -4:
                astronautSprite.x = thumby.display.width - 8
            else:
                astronautSprite.x = newX
            astronautSprite.mirrorX = True
        if (thumby.buttonR.pressed()):
            newX = astronautSprite.x + 1
            if newX >= thumby.display.width - 4:
                astronautSprite.x = 0
            else:
                astronautSprite.x = newX
            astronautSprite.mirrorX = False
    
        # Get the bounce offset based on last jump
        bounceOffset, isFalling = bounce(bounceStart)
        height = astronautHeight - bounceOffset
        
        if poweredUp:
            totalScore = totalScore + 1
            lastMovement = 5
            freq = time.ticks_ms() - bounceStart
            thumby.audio.play(freq, 50)
        
        # Power up saves a player from dying and bounces them far into the sky!
        if not poweredUp and powerUps > 0 and thumby.buttonB.pressed():
            poweredUp = True
            powerUps = powerUps - 1
            bounceStart = time.ticks_ms()
            astronautHeight = astronautSprite.y
            lastMovement = 5
   
        # If the height is above the screen move the platforms down
        if height <= 0: 
            platforms, stars = movePlatformsDown(platforms, stars, height)
            if not isFalling:
                astronautSprite.y = 0
                totalScore = totalScore + 1
        else:
            astronautSprite.y = height
            
        if totalScore - powerUpTracker > random.randint(1200, 55000):
            powerUpTracker = totalScore
            powerUps = powerUps + 1
                
        thumby.display.drawSprite(astronautSprite)
        renderSprites(platforms)
        renderSprites(stars)
        thumby.display.drawText(str(totalScore), 0, thumby.display.height - 7, 1)
        thumby.display.drawText("PWR" + str(powerUps), thumby.display.width - 25, thumby.display.height - 7, 1)
        thumby.display.update()
        
    # End game loop
    thumby.display.fill(0)
    while(1):
        thumby.display.fill(0)
        i =- 1
        lastMovement = 0
        thumby.display.drawText("Final Score!", 2, 7, 1)
        pixelLength = len(str(totalScore)) * 5
        offset = int((thumby.display.width - pixelLength) / 2)
        thumby.display.drawText(str(totalScore), offset, thumby.display.height - 25, 1)
        movePlatformsDown([], stars, i)
        renderSprites(stars)
        if (thumby.saveData.hasItem("highscore")):
            highScore = int(thumby.saveData.getItem("highscore"))
            if totalScore > highScore:
                thumby.saveData.setItem("record", totalScore)
                thumby.saveData.save()
                thumby.display.drawText("New Record!", 5, thumby.display.height - 7, 1)
            else:
                record = "Record: " + str(highScore)
                thumby.display.drawText(record, 0, thumby.display.height - 7, 1)
        thumby.display.update()
        if (thumby.inputPressed() == True):
            break
    
    
    
    
    
