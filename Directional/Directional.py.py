#### !!!! BLOCKLY EXPORT !!!! ####
Number = int
from thumbySprite import Sprite
import random
from thumbyGraphics import display
import thumbyButton as buttons
import math
import time

l = None
indx = None
playerX = None
j = None
Rects = None
playerY = None
curX = None
curY = None
currentDir = None
playerDir = None
i = None
speed = None

# Describe this function...
def drawNextTrack(l):
  global indx, playerX, j, Rects, playerY, curX, curY, currentDir, playerDir, i, speed
  Rects.append([curX, curY])
  if currentDir:
    curX = (curX if isinstance(curX, Number) else 0) + 0
    curY = (curY if isinstance(curY, Number) else 0) + 15
  else:
    curX = (curX if isinstance(curX, Number) else 0) + 15
    curY = (curY if isinstance(curY, Number) else 0) + 0

j = Sprite(1,1,bytearray([1]))

def upRange(start, stop, step):
  while start <= stop:
    yield start
    start += abs(step)

def downRange(start, stop, step):
  while start >= stop:
    yield start
    start -= abs(step)

def __print_to_display__(message):
      message = str(message)
      display.fill(0)
      txt = [""]
      for line in message.split("\n"):
          for word in line.split(" "):
              next_len = len(txt[-1]) + len(word) + 1
              if next_len*display.textWidth + (next_len-1) > display.width:
                  txt += [""]
              txt[-1] += (" " if txt[-1] else "") + word
          txt += [""]
      for ln, line in enumerate(txt):
          display.drawText(line, 0, (display.textHeight+1)*ln, 1)
      display.display.show()


# Describe this function...
def renderTrack(indx):
  global l, playerX, j, Rects, playerY, curX, curY, currentDir, playerDir, i, speed
  display.drawFilledRectangle(Rects[int(indx - 1)][0] - int(playerX), Rects[int(indx - 1)][1] - int(playerY), 15, 15, 1)


playerX = 0
j = Sprite(15,15,bytearray([255,255,3,251,11,235,43,43,43,235,11,251,3,255,255,
            127,127,96,111,104,107,106,106,106,107,104,111,96,127,127]), j.x,j.y,j.key,j.mirrorX,j.mirrorY)
playerY = 0
curX = 24
curY = 8
currentDir = False
Rects = []
for count in range(1250):
  if random.randint(1, 2) == 2:
    if currentDir:
      currentDir = False
    else:
      currentDir = True
  drawNextTrack(5)
j.key = 1
j.x = 24
j.y = 8
display.setFPS(20)
playerDir = False
display.fill(0)
for i in range(21):
  renderTrack(i)
display.drawText(str('Press R/D'), 0, 0, 1)
display.drawSprite(j)
display.update()
while True:
  if buttons.buttonR.justPressed():
    currentDir = True
    break
  if buttons.buttonD.justPressed():
    currentDir = False
    break
speed = 200
while True:
  speed = (speed if isinstance(speed, Number) else 0) + 1
  if buttons.buttonR.justPressed():
    currentDir = True
  if buttons.buttonD.justPressed():
    currentDir = False
  if buttons.actionJustPressed():
    currentDir = not currentDir
  if currentDir:
    playerX = (playerX if isinstance(playerX, Number) else 0) + math.ceil(speed / 300)
  else:
    playerY = (playerY if isinstance(playerY, Number) else 0) + math.ceil(speed / 300)
  i_start = (playerX + playerY) / 15 - 3
  i_end = round((playerX + playerY) / 15 + 7)
  for i in (i_start <= i_end) and upRange(i_start, i_end, 1) or downRange(i_start, i_end, 1):
    renderTrack(i)
  if not bool(display.getPixel(33, 13)):
    break
  display.drawSprite(j)
  display.drawText(str(round((playerX + playerY) / 15)), 0, 0, 1)
  display.update()
  display.fill(0)
display.fill(0)
__print_to_display__(str('Game over!' + '\n' +
'Score: ') + str(round((playerX + playerY) / 15)))
time.sleep(3)

#### !!!! BLOCKLY EXPORT !!!! ####