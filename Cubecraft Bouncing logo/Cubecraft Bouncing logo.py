import time
import thumby
import math


# BITMAP: width: 16, height: 16
cubelogo = bytearray([31,239,175,119,123,251,253,254,254,253,251,123,119,175,239,31,
            248,247,247,239,223,222,190,97,97,190,222,223,239,247,247,248])
            

# BITMAP: width: 38, height: 12
cubetitle = bytearray([224,238,238,238,255,224,239,239,32,191,160,170,245,127,160,106,234,106,191,96,174,110,255,32,186,165,255,97,186,161,191,160,250,250,255,254,224,254,
            15,15,15,15,15,15,15,15,8,11,10,8,15,8,14,8,15,8,15,8,15,8,15,8,10,10,15,11,10,10,10,13,15,15,15,15,15,15])            


# BITMAP: width: 32, height: 8
version = bytearray([192,191,127,191,192,255,63,63,249,57,0,0,63,255,63,63,255,0,126,126,126,0,255,63,63,249,57,0,0,63,255,255])

# BITMAP: width: 50, height: 10
bbfichetitle = bytearray([0,206,49,255,240,15,240,255,49,255,0,206,49,255,0,206,49,255,0,246,246,254,255,254,0,254,255,0,254,254,254,255,0,207,207,0,255,0,206,206,206,206,255,255,183,255,253,123,135,255,
            0,1,2,3,3,0,3,3,2,3,0,1,2,3,0,1,2,3,0,3,3,3,3,1,0,1,3,0,1,1,1,3,0,3,3,0,3,0,1,1,1,1,3,3,3,3,2,3,3,3])

thumbySprite = thumby.Sprite(16, 16, cubelogo)
thumby.display.setFPS(60)
y = 0
x = 0
yy = 30
xx = 30
ydir = 'up'
xdir = 'right'
yydir = 'down'
xxdir = 'left'

vx = 35
vy = 30
bbx = 15
bby = 15
thumby.display.fill(1)
thumby.display.blit(version,vx ,vy ,32 ,8 ,1 ,0 ,0)
thumby.display.blit(bbfichetitle,bbx ,bby ,50 ,10 ,1 ,0 ,0)
thumby.display.update()
time.sleep(5)
del version


while(1):
    thumby.display.fill(1)
    print(xdir, ydir, x, y)
    if y <= 0:
        ydir = 'down'
    if y >= 25:
        ydir = 'up'
    if x <= 0:
        xdir = 'right'
    if x >= 57:
        xdir = 'left'
    if ydir == 'down':
        y += 1
    if ydir == 'up':
        y -= 1
    if xdir == 'left':
        x -= 1
    if xdir == 'right':
        x += 1
    print(xxdir, yydir, x, y)
    if yy <= 0:
        yydir = 'down'
    if yy >= 30:
        yydir = 'up'
    if xx <= 0:
        xxdir = 'right'
    if xx >= 35:
        xxdir = 'left'
    if yydir == 'down':
        yy += 1
    if yydir == 'up':
        yy -= 1
    if xxdir == 'left':
        xx -= 1
    if xxdir == 'right':
        xx += 1
    time.sleep(0.05)
    thumby.display.blit(cubetitle, xx, yy, 38, 12, 1, 0, 0)
    thumby.display.blit(cubelogo, x, y, 16, 16, 1, 0, 0)
    thumby.display.update()
    
