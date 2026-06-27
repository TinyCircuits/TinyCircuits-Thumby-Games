# MineSweep

# Author: TPReal
# Last updated: 2023-03-28

__version__="1.2.2"

GAME_NAME="MineSweep"
GAME_DIR="/Games/"+GAME_NAME

from thumbyGraphics import display

with open(GAME_DIR+"/Title.bin","b") as f:
    data=f.read()
display.blit(data,0,0,72,40,-1,False,False)
del data
display.setFont("/lib/font3x5.bin",3,6,1)
display.drawText("Loading...",30,0,1)
display.update()

__import__(GAME_DIR+"/"+GAME_NAME+"_main.py")
