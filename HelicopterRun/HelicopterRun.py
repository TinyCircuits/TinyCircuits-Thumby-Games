#### !!!! BLOCKLY EXPORT !!!! ####
from thumbyGraphics import display
from thumbySprite import Sprite
Number = int
import time
import thumbyButton as buttons
import machine

block3 = None
block2 = None
block1 = None
helicopter = None
metres = None

block3 = Sprite(1,1,bytearray([1]))

block2 = Sprite(1,1,bytearray([1]))

block1 = Sprite(1,1,bytearray([1]))

helicopter = Sprite(1,1,bytearray([1]))

# Describe this function...
def level():
  global block3, block2, block1, helicopter, metres
  block3.x = 460
  block3.y = 18
  block1.x = 65
  block1.y = 25
  block2.x = 30
  block2.y = 15
  helicopter.y = 20
  helicopter.x = 0
  metres = 0


display.setFPS(5)
block3 = Sprite(5,7,bytearray([127,127,127,127,127]), block3.x,block3.y,block3.key,block3.mirrorX,block3.mirrorY)
block2 = Sprite(5,4,bytearray([15,15,15,15,15]), block2.x,block2.y,block2.key,block2.mirrorX,block2.mirrorY)
block1 = Sprite(5,4,bytearray([15,15,15,15,15]), block1.x,block1.y,block1.key,block1.mirrorX,block1.mirrorY)
helicopter = Sprite(8,5,bytearray([28,8,29,31,29,28,8,0]), helicopter.x,helicopter.y,helicopter.key,helicopter.mirrorX,helicopter.mirrorY)
level()
display.setFont("/lib/font3x5.bin", 3, 5, display.textSpaceWidth)
while True:
  metres = (metres if isinstance(metres, Number) else 0) + 1
  display.drawFilledRectangle(0, 0, 72, 5, 1)
  display.drawFilledRectangle(0, 33, 72, 7, 1)
  display.drawSprite(block1)
  display.drawSprite(block2)
  display.drawSprite(block3)
  display.drawText(str(metres), 1, 34, 0)
  if bool(display.getPixel(helicopter.x + 4, helicopter.y + -1)) or bool(display.getPixel(helicopter.x + 4, helicopter.y + 5)) or bool(display.getPixel(helicopter.x + 8, helicopter.y + 2)):
    display.setFont("/lib/font5x7.bin", 5, 7, display.textSpaceWidth)
    display.fill(0)
    display.drawText(str('you got to'), 0, 0, 1)
    display.drawText(str(metres), 0, 8, 1)
    display.drawText(str('metres'), 0, 16, 1)
    display.drawText(str('Restart?'), 0, 24, 1)
    display.drawText(str('B/A: Yes/No'), 0, 32, 1)
    display.update()
    display.fill(0)
    time.sleep(5)
    while True:
      if buttons.buttonA.pressed():
        machine.reset()
      if buttons.buttonB.pressed():
        break
    display.setFont("/lib/font3x5.bin", 3, 5, display.textSpaceWidth)
    level()
  display.drawSprite(helicopter)
  display.update()
  display.fill(0)
  block1.x += -2
  block2.x += -2
  block3.x += -2
  helicopter.y += 1
  if buttons.actionPressed():
    helicopter.y += -2
  if block1.x < -5:
    if metres < 180 or metres > 380:
      block1.x = 72
  if block2.x < -5:
    if metres < 180 or metres > 600:
      block2.x = 72
  if block3.x < -5:
    block3.x = 72

#### !!!! BLOCKLY EXPORT !!!! ####