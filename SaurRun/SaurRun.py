# Tinysaur Run.

# Enter the mindset of a high-velocity reptile in a less-than-temperate
# environment for as long as possible.

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

import ssd1306
import machine
import time
import uos
import random
import gc
import utime
import thumby
import os

machine.freq(125000000)

gc.enable() # This line helps make sure we don't run out of memory

from framebuf import FrameBuffer, MONO_VLSB # Graphics stuff

# Sensitive game parameters

XVel = 0.05
YVel = 0
Distance = 0
YPos = 0
Gravity = 0.15
MaxFPS = 60
Points = 0
GameRunning = True
CactusPos = random.randint(72, 300)
CloudPos = random.randint(60, 200)
JumpSoundTimer = 0

# Sprite data

PlayerSpr = bytearray([0x04 ^ 0xFF, 0x08 ^ 0xFF, 0xC8 ^ 0xFF, 0xBC ^ 0xFF, 0x1C ^ 0xFF, 0x0E ^ 0xFF, 0x1A ^ 0xFF, 0x2C ^ 0xFF])
PlayerRunFrame1 = bytearray([0xFF, 0xFF, 0xFF, 0xFD, 0xF9, 0xBB, 0xBB, 0xD3, 0xE1, 0xF1, 0xC1, 0xB3, 0x61, 0xD5, 0xF3, 0xFF])
PlayerRunFrame2 = bytearray([0xFF, 0xFF, 0xF7, 0xFB, 0xFB, 0xFB, 0x3B, 0x93, 0xE3, 0x71, 0x03, 0xE7, 0xC3, 0xAB, 0xE7, 0xFF]) 
CactusSpr1 = bytearray([0x00 ^ 0xFF, 0xFC ^ 0xFF, 0x86 ^ 0xFF, 0x92 ^ 0xFF, 0xC2 ^ 0xFF, 0xFC ^ 0xFF, 0x00 ^ 0xFF, 0x00 ^ 0xFF])
CactusSpr2 = bytearray([0x00 ^ 0xFF, 0x1E ^ 0xFF, 0x10 ^ 0xFF, 0xFE ^ 0xFF, 0xE4 ^ 0xFF, 0x20 ^ 0xFF, 0x78 ^ 0xFF, 0x00 ^ 0xFF])
CloudSpr = bytearray([0x9F, 0x4F, 0x63, 0x59, 0xBD, 0x73, 0x73, 0x65, 0x5C, 0x7E, 0x7E, 0x51, 0x57, 0x4F, 0x1F, 0xBF])

CactusSpr = CactusSpr1

thumby.display.fill(0)
thumby.display.drawText("Tinysaur", 12, 0, 1)
thumby.display.drawText("  Run", 15, 9, 1)
thumby.display.update()

thumby.display.setFPS(60)

while(thumby.buttonA.pressed() == True or thumby.buttonB.pressed() == True):
    if(time.ticks_ms() % 1000 < 500):
        thumby.display.drawFilledRectangle(0, 32, 72, 8, 0)
        thumby.display.drawText("Press A/B", 9, 32, 1)
    else:
        thumby.display.drawFilledRectangle(0, 32, 72, 8, 1)
        thumby.display.drawText("Press A/B", 9, 32, 0)
    thumby.display.update()
    pass
while(thumby.buttonA.pressed() == False and thumby.buttonB.pressed() == False):
    if(time.ticks_ms() % 1000 < 500):
        thumby.display.drawFilledRectangle(0, 32, 72, 8, 0)
        thumby.display.drawText("Press A/B", 9, 32, 1)
    else:
        thumby.display.drawFilledRectangle(0, 32, 72, 8, 1)
        thumby.display.drawText("Press A/B", 9, 32, 0)
    thumby.display.update()
    pass
while(thumby.buttonA.pressed() == True or thumby.buttonB.pressed() == True):
    if(time.ticks_ms() % 1000 < 500):
        thumby.display.drawFilledRectangle(0, 32, 72, 8, 0)
        thumby.display.drawText("Press A/B", 9, 32, 1)
    else:
        thumby.display.drawFilledRectangle(0, 32, 72, 8, 1)
        thumby.display.drawText("Press A/B", 9, 32, 0)
    thumby.display.update()
    pass

while(GameRunning):
    t0 = utime.ticks_us() # Check the time

    # Is the player on the ground and trying to jump?
    if(JumpSoundTimer < 0):
        JumpSoundTimer = 0
    if((thumby.buttonA.pressed() == True or thumby.buttonB.pressed() == True) and YPos == 0.0):
        # Jump!
        JumpSoundTimer = 200
        YVel = -2.5

    # Handle "dynamics"
    YPos += YVel
    YVel += Gravity
    Distance += XVel
    JumpSoundTimer -= 15
    
    if(JumpSoundTimer > 0):
        thumby.audio.set(500-JumpSoundTimer)
    else:
        thumby.audio.stop()

    # Accelerate the player just a little bit
    XVel += 0.000025

    # Make sure we haven't fallen below the groundW
    if(YPos > 0):
        YPos = 0.0
        YVel = 0.0

    # Has the player hit a cactus?
    if(CactusPos < 8 and CactusPos > -8 and YPos > -8):
        # Stop the game and give a prompt
        GameRunning = False
        thumby.display.fill(1)
        thumby.audio.stop()
        thumby.display.drawText("Oh no!", 18, 1, 0)
        thumby.display.drawText(str(int(Distance))+"m", 26, 13, 0)
        thumby.display.drawText("Again?", 19, 24, 0)
        thumby.display.drawText("A:N B:Y", 16, 32, 0) 
        thumby.display.update()
        thumby.audio.playBlocking(300, 250)
        thumby.audio.play(260, 250)

        while(thumby.inputPressed() == False):
            pass # Wait for the user to give us something

        while(GameRunning == False):
            if(thumby.buttonB.pressed() == True == 1):
                # Restart the game
                XVel = 0.05
                YVel = 0
                Distance = 0
                YPos = 0
                Points = 0
                GameRunning = True
                CactusPos = random.randint(72, 300)
                CloudPos = random.randint(60, 200)

            elif(thumby.buttonA.pressed() == True):
                # Quit
                machine.reset()

    # Is the cactus out of view?
    if(CactusPos < -24):
        # "spawn" another one (Set its position some distance ahead and change the sprite)
        Points += 10
        thumby.audio.play(440, 300)
        CactusPos = random.randint(72, 500)
        if(random.randint(0, 1) == 0):
            CactusSpr = CactusSpr1
        else:
            CactusSpr = CactusSpr2

    # Is the cloud out of view?
    if(CloudPos < -32):
        # "spawn" another one
        CloudPos = random.randint(40, 200)

    # More dynaaaaaaaaaaaamics
    CactusPos -= XVel * 16
    CloudPos -= XVel * 2

    # Draw game state
    thumby.display.fill(1)
    thumby.display.blit(CactusSpr, int(16 + CactusPos), 24, 8, 8, 1, 0, 0)
    thumby.display.blit(CloudSpr, int(16 + CloudPos), 8, 16, 8, 1, 0, 0)

    if(t0 % 250000 < 125000 or YPos != 0.0):
        # Player is in first frame of run animation
        thumby.display.blit(PlayerRunFrame1, 8, int(23 + YPos), 16, 8, 1, 0, 0)
    else:
        # Player is in second frame of run animation
        thumby.display.blit(PlayerRunFrame2, 8, int(24 + YPos), 16, 8, 1, 0, 0)

    thumby.display.drawFilledRectangle(0, 31, thumby.display.width, 9, 0) # Ground
    thumby.display.drawText(str(int(Points)), 0, 0, 0) # Current points
    thumby.display.drawText("pts", len(str(int(Points))) * 8, 0, 0)
    thumby.display.drawText(str(int(Distance)), 0, 32, 1) # Current distance
    thumby.display.drawText("m", len(str(int(Distance))) * 8, 32, 1)
    thumby.display.update()

    # Spin wheels until we've used up one frame's worth of time
    while(utime.ticks_us() - t0 < 1000000.0 / MaxFPS):
        pass