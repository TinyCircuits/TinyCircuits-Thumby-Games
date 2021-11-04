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
thumby.display.drawText("Tiny", 16, 0, 1)
thumby.display.drawText("Annelid", 8, 8, 1)
thumby.display.drawText("Press A/B", 0, 32, 1)
thumby.display.update()

    # Wait for the user to start
while(thumby.actionPressed() == True):
    pass
while(thumby.actionPressed() == False):
    pass

    # Declare game variables
worm = [[random.randint(int(thumby.DISPLAY_W*0.0625), int(thumby.DISPLAY_W*0.1875)), random.randint(int(thumby.DISPLAY_H*0.0625), int(thumby.DISPLAY_H*0.1875))]]
food = [random.randint(0, int(thumby.DISPLAY_W * 0.25)-1), random.randint(0, int(thumby.DISPLAY_H * 0.25)-1)]
dx = 0
dy = 0

gameRunning = True
MAX_FPS = 7

    # Draws the worm
def drawWorm():
    for tile in worm:
        thumby.display.rect(tile[0]*4, tile[1]*4, 4, 4, 1)

    # Updates the state of the worm
def updateWorm():
    global food
    
        # Is the worm's head at some food?
    if(worm[0][0] == food[0] and worm[0][1] == food[1]):
            # Ate food, extend worm
        thumby.audio.play(440, 150)
        food = [random.randint(0, int(thumby.DISPLAY_W * 0.25)-1), random.randint(0, int(thumby.DISPLAY_H * 0.25)-1)]
        worm.append(worm[len(worm)-1])
    
        # Update each segment
    for k in range(len(worm)-1, 0, -1):
            worm[k] = list(worm[k-1])
            
        # Update worm head
    worm[0][0] += dx
    worm[0][1] += dy
    
    global gameRunning
        # Check collisions with walls and segments
    if((worm[0][0] < 0) or (worm[0][0] >= thumby.DISPLAY_W * 0.25) or (worm[0][1] < 0) or (worm[0][1] >= thumby.DISPLAY_H * 0.25)):
        thumby.audio.play(100, 250)
        gameRunning = False
    for k in range(1, len(worm)):
        if(worm[0][0] == worm[k][0] and worm[0][1] == worm[k][1]):
            thumby.audio.play(100, 250)
            gameRunning = False

while(gameRunning == True):
    t0 = time.ticks_ms()
    
        # Update logic
    updateWorm()
    if(gameRunning == False):
        thumby.display.fill(0)
        thumby.display.drawText("Game", 16, 0, 1)
        thumby.display.drawText("over!", 16, 8, 1)
        thumby.display.drawText("Again?", 16, 16, 1)
        thumby.display.drawText("A:N B:Y", 8, 32, 1)
        thumby.display.update()
        while(thumby.actionPressed() == False):
            pass # Wait for the user to give us something
        if(thumby.buttonA.pressed() == True):
            while(thumby.buttonA.pressed() == True):
                    pass
            machine.reset()
        elif(thumby.buttonB.pressed() == True):
            gameRunning = True
            worm = [[random.randint(int(thumby.DISPLAY_W*0.0625), int(thumby.DISPLAY_W*0.1875)), random.randint(int(thumby.DISPLAY_H*0.0625), int(thumby.DISPLAY_H*0.1875))]]
            food = [random.randint(0, int(thumby.DISPLAY_W * 0.25)-1), random.randint(0, int(thumby.DISPLAY_H * 0.25)-1)]
            dx = 0
            dy = 0
        
        # Draw
    thumby.display.fill(0)
    drawWorm()
    if(time.ticks_ms() % 1000 < 500):
        thumby.display.fillRect(food[0]*4, food[1]*4, 4, 4, 1)
    else:
        thumby.display.fillRect(food[0]*4+1, food[1]*4+1, 2, 2, 1)
    thumby.display.update()
    
        # Handle input while waiting for next frame
    while(time.ticks_diff(time.ticks_ms(), t0) < 1000 / MAX_FPS):
        if(thumby.buttonL.pressed() and (dx != 1)):
            dx = -1
            dy = 0
        if(thumby.buttonR.pressed() and (dx != -1)):
            dx = 1
            dy = 0
        if(thumby.buttonU.pressed() and (dy != 1)):
            dx = 0
            dy = -1
        if(thumby.buttonD.pressed() and (dy != -1)):
            dx = 0
            dy = 1
