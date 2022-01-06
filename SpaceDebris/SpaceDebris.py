# ROYALTY-FRIS SPACE DEBRIS!

# Navigate the cosmos, and clean up the eject from humanity's latter
# achievements and mining operations.

# Written by Mason Watmough for TinyCircuits.
# Last edited 09/09/2021

'''
    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with this program.  If not, see <https://www.gnu.org/licenses/>.
'''

import time
import uos
import random
import gc
import utime
import math
import thumby
import machine

#machine.freq(48000000) 
machine.freq(125000000) 

gc.enable() # This line helps make sure we don't run out of memory

from framebuf import FrameBuffer, MONO_VLSB # Graphics stuff

splash = (0,0,0,224,248,76,198,196,108,56,0,0,0,192,248,124,102,102,38,4,0,0,128,60,102,66,198,140,8,0,0,0,192,248,62,2,6,4,156,240,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,
           0,0,131,131,0,0,1,3,2,0,2,0,3,3,0,0,0,0,0,130,0,0,1,131,2,2,2,3,0,2,0,0,3,130,130,130,3,1,1,0,2,0,128,0,0,0,0,0,0,0,0,128,128,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,
           0,0,143,130,141,0,6,9,6,0,19,12,131,0,6,9,6,9,0,7,8,128,1,15,1,0,19,12,3,0,2,2,0,15,2,0,0,1,14,1,2,0,14,0,10,11,5,0,0,0,9,10,4,0,63,9,6,0,6,9,6,9,0,6,9,9,0,6,13,11,2,0,
           0,0,15,8,8,7,0,6,13,11,2,0,15,9,6,0,1,14,1,2,0,14,0,10,11,5,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,
           0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0)

# Sprite data

UpNeutral = (0,0,0,0,0,0,192,48,48,192,0,0,0,0,0,0,
           0,0,0,0,0,15,4,6,6,4,15,0,0,0,0,0)
UpMovingFrame1 = (0,0,0,0,0,0,192,48,48,192,0,0,0,0,0,0,
           0,0,0,0,0,15,36,86,246,36,15,0,0,0,0,0)
UpMovingFrame2 = (0,0,0,0,0,0,192,48,48,192,0,0,0,0,0,0,
           0,0,0,0,0,15,36,246,86,36,15,0,0,0,0,0)

UpRightNeutral = (0,0,0,0,128,128,64,64,32,96,224,0,0,0,0,0,
           0,0,0,1,1,3,6,28,12,3,0,0,0,0,0,0)
UpRightMovingFrame1 = (0,0,0,0,128,128,64,64,32,96,224,0,0,0,0,0,
           0,0,72,53,25,19,6,28,12,3,0,0,0,0,0,0)
UpRightMovingFrame2 = (0,0,0,0,128,128,64,64,32,96,224,0,0,0,0,0,
           0,32,16,29,41,19,6,28,12,3,0,0,0,0,0,0)
           
RightNeutral = (0,0,0,0,32,224,160,32,64,64,128,128,0,0,0,0,
           0,0,0,0,4,7,5,4,2,2,1,1,0,0,0,0)
RightMovingFrame1 = (0,128,64,128,32,224,160,32,64,64,128,128,0,0,0,0,
           1,1,3,1,4,7,5,4,2,2,1,1,0,0,0,0)
RightMovingFrame2 = (128,128,192,128,32,224,160,32,64,64,128,128,0,0,0,0,
           0,1,2,1,4,7,5,4,2,2,1,1,0,0,0,0)

BigAsteroid1 = (0,192,96,56,52,2,34,33,33,193,49,111,14,30,248,224,
           0,3,12,24,38,72,216,146,147,81,80,80,48,48,31,1)
BigAsteroid2 = (240,28,6,194,102,103,41,233,9,9,14,6,12,4,8,240,
           15,56,32,35,66,226,131,128,158,162,67,66,50,26,6,3)
BigAsteroid3 = (0,254,99,33,33,65,193,1,1,161,161,191,132,36,220,128,
           0,3,30,56,108,118,139,152,190,209,144,144,144,217,119,31)
BigAsteroid4 = (224,56,12,3,225,161,33,65,65,129,1,30,38,68,124,128,
                7,12,8,20,20,21,45,57,33,96,64,64,64,96,24,31)


SmallAsteroid1 = (60,102,122,218,147,141,67,62)
SmallAsteroid2 = (31,225,129,129,249,203,220,112)
SmallAsteroid3 = (60,82,211,141,225,209,211,126)

BigAsteroidSprites = (BigAsteroid1, BigAsteroid2, BigAsteroid3, BigAsteroid4)
SmallAsteroidSprites = (SmallAsteroid1, SmallAsteroid2, SmallAsteroid3)

# Game parameters and player state

GameRunning = True
direction = 0
CurSpr = UpNeutral
XMirror = False
YMirror = False
XPos = random.randint(-10000, 10000)
YPos = random.randint(-10000, 10000)
XVel = 0
YVel = 0
Accel = 0.05
BulletVel = 1.75
AnimTime = 100000
StarDensity = 0.05
MaxFps = 60
ReloadTimer = 0
MaxShipVel = 10

# Asteroid object

class Asteroid:
    def __init__(self):
        self.size = 2
        self.sprite = BigAsteroidSprites[random.randint(0, len(BigAsteroidSprites)-1)]
        if(random.randint(0, 1) == 1):
            self.x = random.randint(round(XPos + 200), round(XPos + 600))
        else:
            self.x = random.randint(round(XPos - 600), round(XPos - 200))
        if(random.randint(0, 1) == 1):
            self.y = random.randint(round(YPos + 200), round(YPos + 600))
        else:
            self.y = random.randint(round(YPos - 600), round(YPos - 200))
        self.xv = random.randint(-300, 300) / 1000.0
        self.yv = random.randint(-300, 300) / 1000.0
        self.xm = True if(random.randint(0, 1) == 1) else False
        self.ym = True if(random.randint(0, 1) == 1) else False
        
# Ship projectile

class ShipBullet:
    def __init__(self, _xp, _yp, _xv, _yv):
        self.XPos = _xp
        self.YPos = _yp
        self.XVel = _xv
        self.YVel = _yv
        self.Life = 240

# Very fast pseudorandom function

@micropython.viper
def qrandom(qrseed: int) -> int:
    #qrseed ^= (qrseed << 10)
    # qrseed ^= (qrseed >> 17)
    #qrseed ^= (qrseed << 2)
    return qrseed
    

@micropython.viper
def DrawStars():
    yp:int = int(round(YPos)) | 0x1
    xp:int = int(round(XPos)) | 0x1
    ptr = ptr8(thumby.display.display.buffer)
    y:int = 0
    seed:int = 0
    yOffset:int = 0
    while(y < int(40)):
        x:int = 0
        while(x < int(72)):
            seed = (int(((xp+x)*(yp+y))) << 10)
            seed ^= (seed << 10)
            seed ^= (seed << 2)
            if(seed & 0xFFFFFF < 192000//3):
                ptr[(y >> 3) * int(72) + x] |= 1 << (y & 0x07)
                #display.pixel(x, y, 1)
                #pass
            seed = (int(((xp+x//2)*(yp+y//2))) << 10)
            seed ^= (seed << 10)
            seed ^= (seed << 2)
            if(seed & 0xFFFFFF < 192000//2):
                ptr[(y >> 3) * int(72) + x] |= 1 << (y & 0x07)
                #display.pixel(x, y, 1)
                #pass
            x += 2
        #print(y)
        y += 2
        
asteroids = []
# Generate asteroids
for i in range(0, 5):
    asteroids.append(Asteroid())

bullets = []

def UpdateBullets():
    # Bullet dynamics and drawing
    for bullet in bullets:
        thumby.display.drawFilledRectangle(round(bullet.XPos-XPos+72*0.5), round(bullet.YPos-YPos+40*0.5), 2, 2, 1)
        bullet.XPos += bullet.XVel
        bullet.YPos += bullet.YVel
        for asteroid in asteroids:
            if(asteroid.size == 2):
                if(bullet.XPos > asteroid.x and bullet.XPos < asteroid.x + 16 and bullet.YPos > asteroid.y and bullet.YPos < asteroid.y + 16):
                    # Bullet hit big asteroid, break into two little ones
                    asteroid.size = 1
                    asteroid.sprite = SmallAsteroidSprites[random.randint(0, len(SmallAsteroidSprites)-1)]
                    asteroid.xv += random.randint(-1, 1)
                    asteroid.yv += random.randint(-1, 1)
                    asteroids.append(Asteroid())
                    asteroids[len(asteroids)-1].size = 1
                    asteroids[len(asteroids)-1].x = asteroid.x + random.randint(-8, 8)
                    asteroids[len(asteroids)-1].y = asteroid.y + random.randint(-8, 8)
                    asteroids[len(asteroids)-1].sprite = SmallAsteroidSprites[random.randint(0, len(SmallAsteroidSprites)-1)]
                    bullets.remove(bullet)
                    break
            if(asteroid.size == 1):
                if(bullet.XPos > asteroid.x and bullet.XPos < asteroid.x + 8 and bullet.YPos > asteroid.y and bullet.YPos < asteroid.y + 8):
                    # Bullet hit small asteroid, delete it
                    asteroids.remove(asteroid)
                    bullets.remove(bullet)
                    break
        bullet.Life -= 1
        if(bullet.Life <= 0):
            bullets.remove(bullet)
            
def UpdateAsteroids():
    # Draw/update asteroids or the markers to them
    for asteroid in asteroids:
        dx = (asteroid.x + 8-XPos)
        dy = (asteroid.y + 8-YPos)
        dx -= 4 if(asteroid.size == 1) else 0
        dy -= 4 if(asteroid.size == 1) else 0
        if(dx*dx+dy*dy>24*24):
            l = math.sqrt(dx*dx+dy*dy)
            nx = dx / l
            ny = dy / l
            if(asteroid.size == 2):
                thumby.display.drawLine(int(round(72/2+nx*12)), int(round(40/2+ny*12)), int(round(72/2+nx*18)), int(round(40/2+ny*18)), 1)
            else:
                thumby.display.drawLine(int(round(72/2+nx*15)), int(round(40/2+ny*15)), int(round(72/2+nx*18)), int(round(40/2+ny*18)), 1)
        if(asteroid.size == 2):
            thumby.display.blit(bytearray(asteroid.sprite), int(asteroid.x - XPos + 72 * 0.5), int(asteroid.y - YPos + 40 * 0.5), 16, 16, 2, asteroid.xm, asteroid.ym)
        elif(asteroid.size == 1):
            thumby.display.blit(bytearray(asteroid.sprite), int(asteroid.x - XPos + 72 * 0.5), int(asteroid.y - YPos + 40 * 0.5), 8, 8, 2, asteroid.xm, asteroid.ym)
        asteroid.x += asteroid.xv
        asteroid.y += asteroid.yv

thrusterFreq = 150
bulletNoiseDuration = 0
thumby.audio.stop()
thumby.display.blit(bytearray(splash), 0, 0, 72, 40, 0, 0, 0)
thumby.display.update()

while(thumby.buttonA.pressed() == True or thumby.buttonB.pressed() == True):
    if(time.ticks_ms() % 1000 < 500):
        thumby.display.drawFilledRectangle(0, 32, 72, 8, 0)
        thumby.display.drawText("Press A/B", 0, 32, 1)
    else:
        thumby.display.drawFilledRectangle(0, 32, 72, 8, 1)
        thumby.display.drawText("Press A/B", 0, 32, 0)
    thumby.display.update()
    pass
while(thumby.buttonA.pressed() == False and thumby.buttonB.pressed() == False):
    if(time.ticks_ms() % 1000 < 500):
        thumby.display.drawFilledRectangle(0, 32, 72, 8, 0)
        thumby.display.drawText("Press A/B", 0, 32, 1)
    else:
        thumby.display.drawFilledRectangle(0, 32, 72, 8, 1)
        thumby.display.drawText("Press A/B", 0, 32, 0)
    thumby.display.update()
    pass
while(thumby.buttonA.pressed() == True or thumby.buttonB.pressed() == True):
    if(time.ticks_ms() % 1000 < 500):
        thumby.display.drawFilledRectangle(0, 32, 72, 8, 0)
        thumby.display.drawText("Press A/B", 0, 32, 1)
    else:
        thumby.display.drawFilledRectangle(0, 32, 72, 8, 1)
        thumby.display.drawText("Press A/B", 0, 32, 0)
    thumby.display.update()
    pass

startTime = time.ticks_ms()

while(GameRunning == True):
    t0 = utime.ticks_us()
    thumby.audio.stop()
    # Figure out the direction of the D-pad
    if(thumby.buttonR.pressed() == True):
        if(thumby.buttonU.pressed() == True):
            direction = 1
            thumby.audio.set(thrusterFreq)
        elif(thumby.buttonD.pressed() == True):
            direction = 3
            thumby.audio.set(thrusterFreq)
        else:
            direction = 2
            thumby.audio.set(thrusterFreq)
    elif(thumby.buttonL.pressed() == True):
        if(thumby.buttonU.pressed() == True):
            direction = 7
            thumby.audio.set(thrusterFreq)
        elif(thumby.buttonD.pressed() == True):
            direction = 5
            thumby.audio.set(thrusterFreq)
        else:
            direction = 6
            thumby.audio.set(thrusterFreq)
    elif(thumby.buttonD.pressed() == True):
        direction = 4
        thumby.audio.set(thrusterFreq)
    elif(thumby.buttonU.pressed() == True):
        direction = 0
        thumby.audio.set(thrusterFreq)
        
    # Draw the correct orientation and state, also dynaaaaaamics
    if(direction == 0):
        CurSpr = UpNeutral
        XMirror = False
        YMirror = False
        if(thumby.buttonU.pressed() == True):
            if(t0 % AnimTime < AnimTime / 2):
                CurSpr = UpMovingFrame1
            else:
                CurSpr = UpMovingFrame2
            YVel -= Accel
        if(thumby.buttonB.pressed() == True and ReloadTimer == 0):
            bulletNoiseDuration = 200
            bullets.append(ShipBullet(XPos-1, YPos - 8, XVel, YVel-BulletVel))
            ReloadTimer = MaxFps * 0.5
            
    elif(direction == 1):
        CurSpr = UpRightNeutral
        XMirror = False
        YMirror = False
        if(thumby.buttonU.pressed() == True and thumby.buttonR.pressed() == True):
            if(t0 % AnimTime < AnimTime / 2):
                CurSpr = UpRightMovingFrame1
            else:
                CurSpr = UpRightMovingFrame2
            YVel -= Accel * 0.707106
            XVel += Accel * 0.707106
        if(thumby.buttonB.pressed() == True and ReloadTimer == 0):
            bulletNoiseDuration = 200
            bullets.append(ShipBullet(XPos+7, YPos - 7, XVel+BulletVel*0.707106, YVel-BulletVel*0.707106))
            ReloadTimer = MaxFps * 0.5
            
    elif(direction == 2):
        CurSpr = RightNeutral
        XMirror = False
        YMirror = False
        if(thumby.buttonR.pressed() == True):
            if(t0 % AnimTime < AnimTime / 2):
                CurSpr = RightMovingFrame1
            else:
                CurSpr = RightMovingFrame2
            XVel += Accel
        if(thumby.buttonB.pressed() == True and ReloadTimer == 0):
            bulletNoiseDuration = 200
            bullets.append(ShipBullet(XPos+8, YPos-1, XVel+BulletVel, YVel))
            ReloadTimer = MaxFps * 0.5
            
    elif(direction == 3):
        CurSpr = UpRightNeutral
        XMirror = False
        YMirror = True
        if(thumby.buttonR.pressed() == True and thumby.buttonD.pressed() == True):
            if(t0 % AnimTime < AnimTime / 2):
                CurSpr = UpRightMovingFrame1
            else:
                CurSpr = UpRightMovingFrame2
            YVel += Accel * 0.707106
            XVel += Accel * 0.707106
        if(thumby.buttonB.pressed() == True and ReloadTimer == 0):
            bulletNoiseDuration = 200
            bullets.append(ShipBullet(XPos+7, YPos+7, XVel+BulletVel*0.707106, YVel+BulletVel*0.707106))
            ReloadTimer = MaxFps * 0.5
            
    elif(direction == 4):
        CurSpr = UpNeutral
        XMirror = False
        YMirror = True
        if(thumby.buttonD.pressed() == True):
            if(t0 % AnimTime < AnimTime / 2):
                CurSpr = UpMovingFrame1
            else:
                CurSpr = UpMovingFrame2
            YVel += Accel
        if(thumby.buttonB.pressed() == True and ReloadTimer == 0):
            bulletNoiseDuration = 200
            bullets.append(ShipBullet(XPos-1, YPos+8, XVel, YVel+BulletVel))
            ReloadTimer = MaxFps * 0.5
            
    elif(direction == 5):
        CurSpr = UpRightNeutral
        XMirror = True
        YMirror = True
        if(thumby.buttonD.pressed() == True and thumby.buttonL.pressed() == True):
            if(t0 % AnimTime < AnimTime / 2):
                CurSpr = UpRightMovingFrame1
            else:
                CurSpr = UpRightMovingFrame2
            YVel += Accel * 0.707106
            XVel -= Accel * 0.707106
        if(thumby.buttonB.pressed() == True and ReloadTimer == 0):
            bulletNoiseDuration = 200
            bullets.append(ShipBullet(XPos-7, YPos+7, XVel-BulletVel*0.707106, YVel+BulletVel*0.707106))
            ReloadTimer = MaxFps * 0.5
            
    elif(direction == 6):
        CurSpr = RightNeutral
        XMirror = True
        YMirror = False
        if(thumby.buttonL.pressed() == True):
            if(t0 % AnimTime < AnimTime / 2):
                CurSpr = RightMovingFrame1
            else:
                CurSpr = RightMovingFrame2
            XVel -= Accel
        if(thumby.buttonB.pressed() == True and ReloadTimer == 0):
            bulletNoiseDuration = 200
            bullets.append(ShipBullet(XPos-8, YPos-1, XVel-BulletVel, YVel))
            ReloadTimer = MaxFps * 0.5
            
    elif(direction == 7):
        CurSpr = UpRightNeutral
        XMirror = True
        YMirror = False
        if(thumby.buttonU.pressed() == True and thumby.buttonL.pressed() == True):
            if(t0 % AnimTime < AnimTime / 2):
                CurSpr = UpRightMovingFrame1
            else:
                CurSpr = UpRightMovingFrame2
            YVel -= Accel * 0.707106
            XVel -= Accel * 0.707106
        if(thumby.buttonB.pressed() == True and ReloadTimer == 0):
            bulletNoiseDuration = 200
            bullets.append(ShipBullet(XPos-7, YPos-7, XVel-BulletVel*0.707106, YVel-BulletVel*0.707106))
            ReloadTimer = MaxFps * 0.5
    
    if(XVel*XVel+YVel*YVel >= MaxShipVel * MaxShipVel):
        ilen = (1.0/math.sqrt(XVel*XVel+YVel*YVel))*MaxShipVel
        XVel *= ilen
        YVel *= ilen
        
    
    if(bulletNoiseDuration != 0):
        thumby.audio.set(bulletNoiseDuration+50)
        
    elif(thumby.buttonU.pressed() == False and thumby.buttonD.pressed() == False and thumby.buttonL.pressed() == False and thumby.buttonR.pressed() == False):
        thumby.audio.stop()
        
    bulletNoiseDuration -= 15;
    if(bulletNoiseDuration < 0):
        bulletNoiseDuration = 0
            
    # Update position
    XPos += XVel
    YPos += YVel
        
    thumby.display.fill(0)
    
    UpdateBullets()
    
    ReloadTimer = ReloadTimer - 1 if ReloadTimer > 0 else 0
        
    #Draw random but position-dependent stars
    DrawStars()
    
    UpdateAsteroids()
        
    # Draw the ship
    thumby.display.blit(bytearray(CurSpr), round(72/2-8), round(40/2-8), 16, 16, 0, XMirror, YMirror)
    #display.text(str(1000000/(utime.ticks_us()-t0)), 0, 0, 1)
    thumby.display.update()
    if(len(asteroids) == 0):
        GameRunning = False
    #print(utime.ticks_us() - t0)
    while(utime.ticks_us() - t0 < 1000000 / MaxFps):
        pass
    
endTime = time.ticks_ms()

thumby.audio.stop()
thumby.display.fill(0)
if(time.ticks_diff(endTime, startTime) < 100000):
    thumby.display.drawText("How?!", 0, 0)
elif(time.ticks_diff(endTime, startTime) < 150000):
    thumby.display.drawText("Nice!", 0, 0)
elif(time.ticks_diff(endTime, startTime) < 200000):
    thumby.display.drawText("Done!", 0, 0)
elif(time.ticks_diff(endTime, startTime) < 300000):
    thumby.display.drawText("C'mon!", 0, 0)
thumby.display.drawText(str(time.ticks_diff(endTime, startTime) / 1000) + "s", 0, 8)
thumby.display.update()

time.sleep_ms(3000)

machine.reset()
#exec(open("/main.py").read())



