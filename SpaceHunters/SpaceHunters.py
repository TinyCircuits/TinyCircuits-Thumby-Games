#### !!!! BLOCKLY EXPORT !!!! ####
import thumbyButton as buttons
from thumbySprite import Sprite
from thumbyAudio import audio
from thumbyGraphics import display
import time
import random
Number = int
import machine
import math
from thumbySaves import saveData

logo = None
counter = None
xCollision = None
goodGuySprite = None
tagged = None
badGuyDirectionX = None
yCollision = None
badGuyDirectionY = None
badGuySprite = None
score = None
spriteCollision = None

goodGuySprite = Sprite(1,1,bytearray([1]))

# Describe this function...
def Move_Good_Guy():
  global logo, counter, xCollision, goodGuySprite, tagged, badGuyDirectionX, yCollision, badGuyDirectionY, badGuySprite, score, spriteCollision
  if buttons.buttonU.pressed() and goodGuySprite.y >= 0:
    goodGuySprite.y += -1
    audio.play(2500, 50)
  if buttons.buttonD.pressed() and goodGuySprite.y <= 31:
    goodGuySprite.y += 1
    audio.play(500, 50)
  if buttons.buttonR.pressed() and goodGuySprite.x <= 63:
    goodGuySprite.x += 1
    audio.play(3500, 50)
  if buttons.buttonL.pressed() and goodGuySprite.x >= 0:
    goodGuySprite.x += -1
    audio.play(150, 50)

logo = Sprite(1,1,bytearray([1]))

# Describe this function...
def Setup_Good_Guy():
  global logo, counter, xCollision, goodGuySprite, tagged, badGuyDirectionX, yCollision, badGuyDirectionY, badGuySprite, score, spriteCollision
  goodGuySprite = Sprite(8,8,bytearray([0,128,126,65,201,65,126,128]), goodGuySprite.x,goodGuySprite.y,goodGuySprite.key,goodGuySprite.mirrorX,goodGuySprite.mirrorY)
  display.drawSprite(goodGuySprite)

badGuySprite = Sprite(1,1,bytearray([1]))

# Describe this function...
def Setup_Bad_Guy():
  global logo, counter, xCollision, goodGuySprite, tagged, badGuyDirectionX, yCollision, badGuyDirectionY, badGuySprite, score, spriteCollision
  counter = 0
  print('Setup Bad Guy')
  badGuySprite = Sprite(8,8,bytearray([0,16,151,126,126,151,16,0]), badGuySprite.x,badGuySprite.y,badGuySprite.key,badGuySprite.mirrorX,badGuySprite.mirrorY)
  badGuySprite.x = random.randint(10, 60)
  badGuySprite.y = random.randint(15, 30)
  print(badGuySprite.x)
  badGuyDirectionX = -2
  badGuyDirectionY = -2
  display.drawSprite(badGuySprite)

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
def Play_Game():
  global logo, counter, xCollision, goodGuySprite, tagged, badGuyDirectionX, yCollision, badGuyDirectionY, badGuySprite, score, spriteCollision
  tagged = False
  while tagged == False:
    Move_Bad_Guy()
    checkCollision()
    if spriteCollision:
      tagged = True
      score = (score if isinstance(score, Number) else 0) + 1
      __print_to_display__(score)
      time.sleep(3)
    Move_Good_Guy()
    if buttons.buttonB.justPressed():
      saveHighScore()
      machine.reset()
    display.drawSprite(goodGuySprite)
    display.update()
    display.fill(0)

# Describe this function...
def Bad_Guy_Run_Away():
  global logo, counter, xCollision, goodGuySprite, tagged, badGuyDirectionX, yCollision, badGuyDirectionY, badGuySprite, score, spriteCollision
  print('Bad Guy Run Away')
  print('X delta')
  print(goodGuySprite.x - badGuySprite.x)
  print('Y delta')
  print(goodGuySprite.y - badGuySprite.y)
  if math.fabs(goodGuySprite.x - badGuySprite.x) < 20 and math.fabs(goodGuySprite.y - badGuySprite.y) < 20:
    print('Bad Guy Close!!')
    badGuyDirectionX = random.randint(1, 1) if goodGuySprite.x < badGuySprite.x else random.randint(-1, -1)
    badGuyDirectionY = random.randint(1, 1) if goodGuySprite.y < badGuySprite.y else random.randint(-1, -1)

# Describe this function...
def Move_Bad_Guy():
  global logo, counter, xCollision, goodGuySprite, tagged, badGuyDirectionX, yCollision, badGuyDirectionY, badGuySprite, score, spriteCollision
  if counter % 12 == 0:
    badGuyDirectionX = random.randint(-1, 1)
    badGuyDirectionY = random.randint(-1, 1)
  Bad_Guy_Run_Away()
  badGuySprite.x += badGuyDirectionX
  badGuySprite.y += badGuyDirectionY
  if badGuySprite.x < -2:
    badGuySprite.x = 65
  if badGuySprite.x > 65:
    badGuySprite.x = -2
  if badGuySprite.y < -2:
    badGuySprite.y = 33
  if badGuySprite.y > 33:
    badGuySprite.y = -2
  display.drawSprite(badGuySprite)
  counter = (counter if isinstance(counter, Number) else 0) + 1

saveData.setName(globals().get('__file__', 'FAST_EXECUTE').replace('/Games/','').strip('/').split('/')[0].split('.')[0])

# Describe this function...
def saveHighScore():
  global logo, counter, xCollision, goodGuySprite, tagged, badGuyDirectionX, yCollision, badGuyDirectionY, badGuySprite, score, spriteCollision
  if not saveData.hasItem('high score'):
    saveData.setItem('high score', 0)
    saveData.save()
  if score > saveData.getItem('high score'):
    saveData.setItem('high score', score)
    saveData.save()
    __print_to_display__('HIGH SCORE!!!!!')

# Describe this function...
def checkCollision():
  global logo, counter, xCollision, goodGuySprite, tagged, badGuyDirectionX, yCollision, badGuyDirectionY, badGuySprite, score, spriteCollision
  xCollision = True
  yCollision = True
  if badGuySprite.x + 4 < goodGuySprite.x - 4:
    xCollision = False
  if badGuySprite.x - 4 > goodGuySprite.x + 4:
    xCollision = False
  if badGuySprite.y + 4 < goodGuySprite.y - 4:
    yCollision = False
  if badGuySprite.y - 4 > goodGuySprite.y + 4:
    yCollision = False
  spriteCollision = xCollision and yCollision


logo = Sprite(60,33,bytearray([0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,128,64,32,16,16,8,8,248,12,103,231,231,6,56,136,8,16,16,32,64,192,128,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,
           0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,192,56,6,1,0,0,0,0,0,0,192,255,0,0,240,0,0,192,223,128,0,0,0,0,0,13,2,12,224,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,
           0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,15,32,0,0,0,0,0,0,24,31,15,7,6,52,63,20,4,7,15,31,62,0,0,0,0,0,0,0,31,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,
           108,90,82,52,0,126,18,22,12,0,124,38,124,0,60,70,66,102,0,0,126,82,82,0,0,126,16,16,16,126,0,126,64,64,126,0,126,12,48,126,0,2,2,126,2,0,126,82,90,66,0,126,18,54,76,0,78,90,118,0,
           0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]), logo.x,logo.y,logo.key,logo.mirrorX,logo.mirrorY)
logo.x = 6
logo.y = 4
display.drawSprite(logo)
display.update()
time.sleep(4)
display.fill(0)
print('DID IT!!!')
display.setFPS(30)
while True:
  Setup_Good_Guy()
  Setup_Bad_Guy()
  display.update()
  Play_Game()
  tagged = False

#### !!!! BLOCKLY EXPORT !!!! ####