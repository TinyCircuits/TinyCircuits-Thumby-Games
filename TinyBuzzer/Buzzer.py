#### !!!! BLOCKLY EXPORT !!!! ####
from thumbyGraphics import display
from thumbySprite import Sprite
import time
Number = int
import random
import thumbyButton as buttons
from thumbyAudio import audio

title = None
counter = None

title = Sprite(1,1,bytearray([1]))


display.setFPS(1)
title = Sprite(72,40,bytearray([255,255,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,195,67,67,99,51,19,19,19,19,19,19,19,19,19,51,35,99,99,195,131,3,3,3,255,255,
           255,255,0,224,32,32,32,0,224,32,32,192,0,224,160,160,160,0,224,160,160,160,0,224,32,32,64,128,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,224,60,7,1,248,136,0,60,36,52,52,60,0,0,60,52,52,36,60,0,136,249,1,255,0,0,255,255,
           255,255,0,244,85,85,163,0,231,1,1,240,0,7,20,148,84,48,7,20,148,84,48,7,244,84,82,81,0,240,144,144,96,0,0,0,0,0,0,0,0,0,0,0,127,255,240,224,224,225,195,198,196,204,200,200,200,200,200,200,204,196,198,195,225,224,224,245,255,0,255,255,
           255,255,0,3,2,2,3,0,3,2,2,3,0,2,3,2,2,2,2,3,130,130,130,128,131,130,162,162,168,171,168,169,170,168,168,40,136,224,56,28,56,224,128,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,255,255,
           255,255,192,192,192,192,192,192,192,192,192,192,192,192,192,192,192,192,192,192,192,192,194,194,194,194,194,194,194,194,194,194,194,192,196,198,199,192,192,192,192,192,199,198,196,192,192,192,192,192,192,192,192,192,192,192,192,192,192,192,192,192,192,192,192,192,192,192,192,192,255,255]), title.x,title.y,title.key,title.mirrorX,title.mirrorY)
display.drawSprite(title)
display.update()
display.fill(0)
time.sleep(3)
while True:
  counter = (counter if isinstance(counter, Number) else 0) + 5
  if counter == 70:
    counter = 0
  display.drawText(str('^'), counter, 17, 1)
  display.drawText(str('X'), random.randint(64, 66), 10, 1)
  display.update()
  display.fill(0)
  if buttons.actionJustPressed():
    display.setFPS(display.frameRate + 1)
    if counter != 65:
      display.setFPS(1)
      audio.playBlocking(2000, 1000)
  audio.playBlocking(2000, 10)

#### !!!! BLOCKLY EXPORT !!!! ####