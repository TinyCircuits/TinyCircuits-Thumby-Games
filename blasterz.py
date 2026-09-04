import thumby

# BITMAP: width: 8, height: 8
shipMap = bytearray([195,231,189,219,102,36,60,24])
asteroidMap = bytearray([28,122,126,223,175,223,118,60])
beamMap = bytearray([1,1])

# Make a sprite object 
shipSpr = thumby.Sprite(8, 8, shipMap, 5, 20)
asteroidSpr = thumby.Sprite(8, 8, asteroidMap, 60,20)
beamSpr = thumby.Sprite(2, 1, beamMap)
beamSpr.x = 11 # place beam so it's hidden at the tip of the ship
beamSpr.y = 24

# Set the FPS (without this call, the default fps is 30)
thumby.display.setFPS(30)

# Game state variables
score = 0
shootBeam = False

while(True):
    # Fill canvas to black
    thumby.display.fill(0)

    if thumby.buttonA.justPressed():
        shootBeam = True
    if shootBeam == True:
        thumby.display.fill(0)
        beamSpr.x += 1

        # Check if beam has collided with asteroid
        if(beamSpr.x >= asteroidSpr.x):
            beamSpr.x = 11 # Reload beam after hitting asteroid
            score += 1     # Increase score and change game state
            shootBeam = False

    # Draw the score and sprites
    thumby.display.drawText("Score: ", 15, 3, 1)
    thumby.display.drawText(str(score), 55, 3, 1)
    thumby.display.drawSprite(shipSpr)
    thumby.display.drawSprite(asteroidSpr)
    thumby.display.drawSprite(beamSpr)
    thumby.display.update()