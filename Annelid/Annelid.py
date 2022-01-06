# Tiny Annelid.

# Crawl around and collect food! This is the most
# comprehensive and short game source on the Thumby
# by default; its implementation should serve
# as a tutorial for beginner programming
# with Thumby features.

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

import thumby
import random
import time
import machine

# Draw the game splash
thumby.display.fill(0)
thumby.display.drawText("Tiny", 24, 0, 1)
thumby.display.drawText("Annelid", 15, 9, 1)
thumby.display.drawText("Press A/B", 9, 32, 1)
thumby.display.update()

# Wait for the user to start
while(thumby.actionPressed() == True):
    pass
while(thumby.actionPressed() == False):
    pass

thumby.DISPLAY_W = 72
thumby.DISPLAY_H = 40

blockSize = 4
maxXcoordinate = thumby.display.width // blockSize
maxYcoordinate = thumby.display.height // blockSize

# Declare game variables
worm = [[random.randint(int(thumby.DISPLAY_W*0.0625), int(thumby.DISPLAY_W*0.1875)), random.randint(int(thumby.DISPLAY_H*0.0625), int(thumby.DISPLAY_H*0.1875))]]
food = [random.randint(0, maxXcoordinate-1), random.randint(0, maxYcoordinate-1)]
dx = 0
dy = 0

gameRunning = True
startFPS = 3.0

    # Draws the worm
def drawWorm():
    for tile in worm:
        thumby.display.drawRectangle(tile[0]*4, tile[1]*4, 4, 4, 1)
        print(tile[0]*4)

    # Updates the state of the worm
def updateWorm():
    global food
    
        # Is the worm's head at some food?
    if(worm[0][0] == food[0] and worm[0][1] == food[1]):
            # Ate food, extend worm
        thumby.audio.play(440, 150)
        food = [random.randint(0, maxXcoordinate-1), random.randint(0, maxYcoordinate-1)]
        worm.append(worm[len(worm)-1])
    
        # Update each segment
    for k in range(len(worm)-1, 0, -1):
            worm[k] = list(worm[k-1])
            
        # Update worm head
    worm[0][0] += dx
    worm[0][1] += dy
    
    global gameRunning
        # Check collisions with walls and segments
    if((worm[0][0] < 0) or (worm[0][0] >= maxXcoordinate) or (worm[0][1] < 0) or (worm[0][1] >= maxYcoordinate)):
        thumby.audio.play(100, 250)
        gameRunning = False
    for k in range(1, len(worm)):
        if(worm[0][0] == worm[k][0] and worm[0][1] == worm[k][1]):
            thumby.audio.play(100, 250)
            gameRunning = False

startTime=time.ticks_ms()

while(gameRunning == True):
    if(thumby.buttonL.justPressed() and (dx != 1)):
        dx = -1
        dy = 0
    if(thumby.buttonR.justPressed() and (dx != -1)):
        dx = 1
        dy = 0
    if(thumby.buttonU.justPressed() and (dy != 1)):
        dx = 0
        dy = -1
    if(thumby.buttonD.justPressed() and (dy != -1)):
        dx = 0
        dy = 1
    
    # Update logic
    updateWorm()
    if(gameRunning == False):
        thumby.display.fill(0)
        thumby.display.drawText("Game over!", 7, 1, 1)
        thumby.display.drawText("Again?", 18, 22, 1)
        thumby.display.drawText("A:N B:Y", 15, 32, 1)
        thumby.display.update()
        while(thumby.actionPressed() == False):
            pass # Wait for the user to give us something
        if(thumby.buttonA.pressed() == True):
            machine.reset()
        elif(thumby.buttonB.pressed() == True):
            gameRunning = True
            worm = [[random.randint(int(thumby.DISPLAY_W*0.0625), int(thumby.DISPLAY_W*0.1875)), random.randint(int(thumby.DISPLAY_H*0.0625), int(thumby.DISPLAY_H*0.1875))]]
            food = [random.randint(0, int(thumby.DISPLAY_W * 0.25)-1), random.randint(0, int(thumby.DISPLAY_H * 0.25)-1)]
            dx = 0
            dy = 0
            startTime=time.ticks_ms()
        
    # Draw
    thumby.display.fill(0)
    thumby.display.drawRectangle(0, 0, 72, 40, 1)
    drawWorm()
    if(time.ticks_ms() % 1000 < 500):
        thumby.display.drawFilledRectangle(food[0]*4, food[1]*4, 4, 4, 1)
    else:
        thumby.display.drawFilledRectangle(food[0]*4+1, food[1]*4+1, 2, 2, 1)
    
    thumby.display.setFPS(startFPS + (time.ticks_ms()-startTime)/10000) # increase FPS by 1 every 10 seconds
    thumby.display.update()
