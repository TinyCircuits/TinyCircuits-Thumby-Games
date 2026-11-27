import thumby

# Cat bitmaps 8x8
catFootForward = bytearray([243,133,135,231,231,128,193,184])
catFeetForward = bytearray([243,133,199,167,231,128,193,184])
catSplit = bytearray([177,199,199,167,231,128,225,152])
catFrontSplit =bytearray([179,197,135,231,167,192,193,184])
catFeetBack = bytearray([179,197,135,231,167,192,129,248])
catBackFootTail = bytearray([179,197,197,167,167,192,129,248])


# BITMAP: width: 72, height: 30
bg = bytearray([0,0,0,0,0,0,0,0,0,0,0,4,0,0,0,0,0,0,0,0,128,0,0,0,0,0,0,0,0,0,0,0,0,0,64,0,0,0,0,0,0,0,0,0,0,0,0,128,0,0,0,0,0,0,0,0,0,0,0,4,0,0,0,0,0,0,0,0,0,64,0,0,
            0,0,0,0,0,8,20,8,0,0,0,128,128,128,128,128,128,128,128,128,128,128,128,128,0,0,0,0,64,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,2,1,0,0,0,0,128,192,224,224,240,240,248,248,252,252,252,252,252,252,252,252,248,248,240,
            224,240,240,248,248,252,252,254,254,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,254,252,248,248,240,224,224,224,192,192,192,192,192,192,192,192,192,192,192,224,224,224,240,248,252,252,254,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,
            63,63,63,63,63,63,63,63,63,63,63,63,63,63,63,63,63,63,63,63,63,63,63,63,63,63,63,63,63,63,63,63,63,63,63,63,63,63,63,63,63,63,63,63,63,63,63,63,63,63,63,63,63,63,63,63,63,63,63,63,63,63,63,63,63,63,63,63,63,63,63,63])

bg2 = bytearray([0,0,0,2,0,0,0,16,64,0,0,0,0,128,64,128,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,16,0,0,0,0,0,0,0,0,0,0,16,40,16,0,0,0,0,0,0,0,0,0,0,0,0,0,32,0,0,0,0,0,0,0,0,64,160,64,2,0,
            240,224,192,128,128,128,0,8,0,0,0,0,0,0,1,0,0,0,0,0,0,0,0,8,0,128,128,128,192,224,240,240,248,248,248,252,252,252,254,254,254,255,255,255,255,255,254,254,254,254,252,252,252,248,248,240,240,225,224,192,192,128,128,0,0,0,0,0,32,0,0,0,
            255,255,255,255,255,255,255,255,254,254,254,254,252,252,252,252,252,252,252,254,254,254,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,254,252,252,248,240,240,224,224,
            63,63,63,63,63,63,63,63,63,63,63,63,63,63,63,63,63,63,63,63,63,63,63,63,63,63,63,63,63,63,63,63,63,63,63,63,63,63,63,63,63,63,63,63,63,63,63,63,63,63,63,63,63,63,63,63,63,63,63,63,63,63,63,63,63,63,63,63,63,63,63,63])


# Make a sprite object including all the walking cat frames
catSpr = thumby.Sprite(8, 8, catFootForward+catFeetForward+catSplit+catFrontSplit+catFeetBack+catBackFootTail, 28, 32)

# Background sprites & initial x positions
bgSpr = thumby.Sprite(72, 30, bg)
bg2Spr = thumby.Sprite(72, 30, bg2)
bgSpr.x = 0
bg2Spr.x = 72

# Set the FPS (without this call, the default fps is 30)
thumby.display.setFPS(60)

# You can set the FPS lower, or you can alter the timing of the animations
# and movement using simple counters and the modulo operator
scrollCtr = 0
catSprCtr = 0

while(True):
    thumby.display.fill(1) # Fill canvas to white

    # Scrolling background
    scrollCtr += 1
    if(scrollCtr % 8 == 0): # Move the background every 8 loops
        bgSpr.x -= 1
        bg2Spr.x -= 1

        catSprCtr += 1
        if(catSprCtr >= 5): # There are 6 frames in the list, in the placement 0-5
            catSprCtr = 0

    # Re-place the x coordinate of backgrounds when they're unseen
    if (bg2Spr.x == 0):
        bgSpr.x = 72
    if (bg2Spr.x == -72):
        bg2Spr.x = 72

    # Draw sprites and update display
    thumby.display.drawSprite(bgSpr)
    thumby.display.drawSprite(bg2Spr)
    catSpr.setFrame(catSprCtr)
    thumby.display.drawSprite(catSpr)
    thumby.display.update()