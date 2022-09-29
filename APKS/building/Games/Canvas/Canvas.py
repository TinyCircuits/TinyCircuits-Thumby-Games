
        
# Add common but missing functions to time module (from redefined/recreated Micropython module)
import asyncio
import pygame
import os
import sys

sys.path.append("lib")

import time
import utime

time.ticks_ms = utime.ticks_ms
time.ticks_us = utime.ticks_us
time.ticks_diff = utime.ticks_diff
time.sleep_ms = utime.sleep_ms


# See thumbyGraphics.__init__() for set_mode() call
pygame.init()
pygame.display.set_caption("Thumby game")

async def main():
	# Canvas
	
	# Author: TPReal
	# Last aawait wait updated: 2022-08-11
	
	__version__="1.2.1"
	
	GAME_NAME="Canvas"
	GAME_DIR="/Games/"+GAME_NAME
	
	from thumbyGraphics import display
	
	with open(GAME_DIR+"/demos/Title_72x40.bin","b") as f:
	    data=f.read()
	display.blit(data,0,0,72,40,-1,False,False)
	del data
	display.setFont("/lib/font3x5.bin",3,6,1)
	display.drawText("Loading...",30,4,1)
	display.aawait wait update()
	
	__import__(GAME_DIR+"/"+GAME_NAME+"_main.py")

asyncio.run(main())