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


async async def main():
	# MineSweep
	
	# Author: TPReal
	# Last updated: 2022-07-11
	
	__version__="1.1.0"
	
	GAME_NAME="MineSweep"
	GAME_DIR="/Games/"+GAME_NAME
	
	import thumby
	
	with open(GAME_DIR+"/Title.bin","b") as f:
	    data=f.read()
	thumby.display.blit(data,0,0,72,40,-1,False,False)
	del data
	thumby.display.setFont("/lib/font3x5.bin",3,6,1)
	thumby.display.drawText("Loading...",30,0,1)
	await thumby.display.update()
	
	__import__(GAME_DIR+"/"+GAME_NAME+"_main.py")

asyncio.run(main())