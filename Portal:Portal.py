import time
import thumby
import math

# BITMAP: width: 3, height: 7
Man = bytearray([40,64,40])

# BITMAP: width: 4, height: 8
Portal1 = bytearray([0,0,0,0])

# BITMAP: width: 4, height: 8
Portal2 = bytearray([0,0,0,0])

# BITMAP: width: 72, height: 40
Map1 = bytearray([255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,
            255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,
            255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,
            255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,
            15,15,15,15,15,15,15,15,15,15,15,15,15,15,15,15,15,15,15,15,15,15,15,15,15,15,15,15,15,15,15,15,15,15,15,15,15,15,15,15,15,255,255,255,255,255,255,255,255,255,255,255,255,255,15,15,15,15,15,15,15,15,15,15,15,15,15,15,15,15,15,15])

# BITMAP: width: 34, height: 4
Map2 = bytearray([0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0])

# BITMAP: width: 7, height: 4
Spike1 = bytearray([7,3,1,0,1,3,7])

# BITMAP: width: 7, height: 4
Spike2 = bytearray([7,3,1,0,1,3,7])

Map1 = thumby.Sprite(72, 40, Map1)
Map1.x = 0
Map1.y = 0

Map2 = thumby.Sprite(31, 4, Map2)
Map2.x = 41
Map2.y = 24

Man = thumby.Sprite(3, 7, Man)
Man.x = 15
Man.y = 29

Portal1 = thumby.Sprite(4, 8, Portal1)
Portal1.x = 24
Portal1.y = 28

Portal2 = thumby.Sprite(4, 8, Portal2)
Portal2.x = 48
Portal2.y = 16

Spike1 = thumby.Sprite(7, 3, Spike1)
Spike1.x = 41
Spike1.y = 37

Spike2 = thumby.Sprite(7, 3, Spike2)
Spike2.x = 47
Spike2.y = 37

moveNum = 1
fallSpeed = 1
jump = 13
thumby.display.setFPS(60)

collision = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
             0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
             0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
             0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
             0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0,
             0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0,
             0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1,
             0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
             0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
             1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0, 1, 1, 1, 1]

while(True):
    thumby.display.fill(1)
    # left and right buttons
    if thumby.buttonL.pressed():
        Man.x -= moveNum
    if thumby.buttonR.pressed():
        Man.x += moveNum
    
    # jump and fall
    if thumby.buttonA.justPressed():
        for i in range (0, 13):
            Man.y -= moveNum
    else:
        thumby.display.drawSprite(Man)
        Man.y += moveNum
    
    if thumby.buttonB.justPressed():
        for i in range (0, 13):
            Man.y -= moveNum
    else:
        thumby.display.drawSprite(Man)
        Man.y += moveNum 
       
    if 1 <= Man.x < 71 and 0 <= Man.y < 34:    
        #Floor collision
        ccol = (Man.x + 1) // 4
        crow = (Man.y + 6) // 4
        ctile = collision[crow * 18 + ccol]
        if ctile:
            Man.y = crow * 4 - 7
        
        # Left Wall Collision
        ccol = (Man.x) // 4
        crow = (Man.y + 6) // 4
        ctile = collision[crow * 18 + ccol]
        if ctile:
            Man.x = ccol * 4 + 4
    
        # Right Wall Collision
        ccol = (Man.x + 2) // 4
        crow = (Man.y + 6) // 4
        ctile = collision[crow * 18 + ccol]
        if ctile:
            Man.x = ccol * 4 - 3  
        
    thumby.display.drawSprite(Map1)
    thumby.display.drawSprite(Map2)
    thumby.display.drawSprite(Portal1)
    thumby.display.drawSprite(Portal2)
    thumby.display.drawSprite(Spike1)
    thumby.display.drawSprite(Spike2)
    thumby.display.drawSprite(Man)
    thumby.display.update()