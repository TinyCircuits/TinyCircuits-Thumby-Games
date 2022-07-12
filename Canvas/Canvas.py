# Canvas

# Author: TPReal
# Last updated: 2022-07-11

__version__="1.2.0"

GAME_NAME="Canvas"
GAME_DIR="/Games/"+GAME_NAME

import thumby

with open(GAME_DIR+"/demos/Title_72x40.bin","b") as f:
    data=f.read()
thumby.display.blit(data,0,0,72,40,-1,False,False)
del data
thumby.display.setFont("/lib/font3x5.bin",3,6,1)
thumby.display.drawText("Loading...",30,4,1)
thumby.display.update()

__import__(GAME_DIR+"/"+GAME_NAME+"_main.py")
