import asyncio
import pygame
import os
import sys

sys.path.append("lib")

# Common overrides to get scripts working in the browsers. This should be prepended to each file in the game

# Re-define the open function to create a directory for a file if it doesn't already exist (mimic MicroPython)
def open(path, mode):
    import builtins
    from pathlib import Path
    
    filename = Path(path)
    filename.parent.mkdir(parents=True, exist_ok=True)

    return builtins.open(path, mode)

os.chdir(sys.path[0])


async def main():
	# Canvas
	
	# Author: TPReal
	# Last updated: 2022-08-11
	
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
	display.update()
	
	__import__(GAME_DIR+"/"+GAME_NAME+"_main.py")

asyncio.run(main())