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
thumby.display.update()

__import__(GAME_DIR+"/"+GAME_NAME+"_main.py")
