#### !!!! BLOCKLY EXPORT !!!! ####
from thumbySprite import Sprite
import random
from thumbyGraphics import display
import thumbyButton as buttons
Number = int

test = None
banana = None
score = None

test = Sprite(1,1,bytearray([1]))

banana = Sprite(1,1,bytearray([1]))


test = Sprite(16,16,bytearray([0,192,192,192,128,142,145,241,241,145,142,128,192,192,192,0,
           0,1,1,193,240,12,2,3,3,2,12,240,193,1,1,0]), test.x,test.y,test.key,test.mirrorX,test.mirrorY)
banana = Sprite(16,16,bytearray([0,0,0,0,0,0,0,0,0,128,192,224,248,30,0,0,
           0,32,32,48,48,24,28,30,15,15,7,3,0,0,0,0]), banana.x,banana.y,banana.key,banana.mirrorX,banana.mirrorY)
score = 0
banana.x = random.randint(1, 60)
banana.y = random.randint(1, 20)
display.setFPS(30)
test.x = 30
test.y = 10
display.drawSprite(test)
while 1 == 1:
  if buttons.buttonR.pressed():
    test.x += 1
    display.drawSprite(test)
  if buttons.buttonL.pressed():
    test.x += -1
    display.drawSprite(test)
  if buttons.buttonD.pressed():
    test.y += 1
    display.drawSprite(test)
  if buttons.buttonU.pressed():
    test.y += -1
    display.drawSprite(test)
  if test.x < banana.x + 5 and test.x > banana.x - 5 and test.y < banana.y + 5 and test.y > banana.y - 5:
    score = (score if isinstance(score, Number) else 0) + 1
    banana.y = random.randint(1, 20)
    banana.x = random.randint(1, 60)
  display.drawText(str(score), 0, 0, 1)
  display.drawSprite(banana)
  display.drawSprite(test)
  display.update()
  display.fill(0)

#### !!!! BLOCKLY EXPORT !!!! ####