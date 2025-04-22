#Credits for PogoPicross (currently unimplemented)
import thumby
import time

def buttonAsound():
    thumby.audio.play(622, 100)

def buttonBsound():
    thumby.audio.play(523, 100)

def creditsGo():
    #Luna Sprites
    # BITMAP: width: 25, height: 18
    lunaMap1 = bytearray([14,81,169,5,2,26,66,66,26,2,5,169,81,14,0,0,64,160,160,16,32,16,32,64,128,
               0,0,0,1,250,134,6,14,254,142,7,0,241,1,2,4,8,240,80,145,78,128,64,41,22,
               0,0,0,0,1,3,3,3,1,3,3,3,1,2,2,2,2,1,0,0,0,0,0,0,0])
    
    # BITMAP: width: 25, height: 18
    lunaMap2 = bytearray([14,81,169,5,2,26,66,66,26,2,5,169,81,14,20,20,34,196,2,4,40,208,0,0,0,
               0,0,0,1,250,134,6,14,254,142,7,0,241,1,2,6,10,241,16,8,5,2,0,0,0,
               0,0,0,0,1,3,3,3,1,3,3,3,1,2,2,2,2,1,0,0,0,0,0,0,0])
               
    lunaSpr = thumby.Sprite(25, 18, lunaMap1+lunaMap2, key = -1)
    thumby.display.fill(0)
    thumby.display.setFPS(60)
    thumby.display.setFont("/lib/font5x7.bin", 5, 7, 1)
    creditsDisplayed = True
    frameCount = 1
    sprFrame = 1
    thumby.display.drawText("CREDITS", 15, 0, 1)
    thumby.display.setFont("/lib/font3x5.bin", 3, 5, 1)
    thumby.display.drawText("Code and Art:", 0, 9, 1)
    thumby.display.drawText("Pogostix", 5, 15, 1)
    thumby.display.drawText("Extra Help:", 0, 21, 1)
    thumby.display.drawText("Thumby", 5, 27, 1)
    thumby.display.drawText("Discord", 5, 33, 1)
    while(creditsDisplayed):
        frameCount += 1
        sprFrame = frameCount // 12
        lunaSpr.x = 47
        lunaSpr.y = 22
        lunaSpr.setFrame(sprFrame)
        thumby.display.drawSprite(lunaSpr)
        thumby.display.update()
        if thumby.buttonA.justPressed():
            buttonAsound()
            creditsDisplayed2 = True
            thumby.display.fill(0)
            thumby.display.setFPS(60)
            thumby.display.setFont("/lib/font5x7.bin", 5, 7, 1)
            frameCount = 1
            sprFrame = 1
            thumby.display.drawText("CREDITS", 15, 0, 1)
            thumby.display.setFont("/lib/font3x5.bin", 3, 5, 1)
            thumby.display.drawText("Extra Thanks To:", 0, 9, 1)
            thumby.display.drawText("Luna,", 5, 15, 1)
            thumby.display.drawText("Mom,", 5, 21, 1)
            thumby.display.drawText("and You!", 5, 27, 1)
            while(creditsDisplayed2):
                frameCount += 1
                sprFrame = frameCount // 12
                lunaSpr.x = 47
                lunaSpr.y = 22
                lunaSpr.setFrame(sprFrame)
                thumby.display.drawSprite(lunaSpr)
                thumby.display.update()
                if thumby.buttonA.justPressed():
                    buttonAsound()
                    creditsDisplayed3 = True
                    thumby.display.fill(0)
                    thumby.display.setFPS(60)
                    thumby.display.setFont("/lib/font5x7.bin", 5, 7, 1)
                    frameCount = 1
                    sprFrame = 1
                    thumby.display.drawText("CREDITS", 15, 0, 1)
                    thumby.display.drawText("THANK YOU", 0, 9, 1)
                    thumby.display.drawText("  FOR", 0, 17, 1)
                    thumby.display.drawText("PLAYING!", 0, 25, 1)
                    thumby.display.setFont("/lib/font3x5.bin", 3, 5, 1)
                    thumby.display.drawText("B: Back", 0, 35, 1)
                    while(creditsDisplayed3):
                        frameCount += 1
                        sprFrame = frameCount // 12
                        lunaSpr.x = 47
                        lunaSpr.y = 22
                        lunaSpr.setFrame(sprFrame)
                        thumby.display.drawSprite(lunaSpr)
                        thumby.display.update()
                        if thumby.buttonB.justPressed():
                            buttonBsound()
                            creditsDisplayed = False
                            creditsDisplayed2 = False
                            creditsDisplayed3 = False
                            break