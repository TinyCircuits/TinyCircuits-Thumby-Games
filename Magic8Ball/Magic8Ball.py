#### !!!! BLOCKLY EXPORT !!!! ####
from thumbyGraphics import display
from thumbySprite import Sprite
import thumbyButton as buttons
import time
import random

# BITMAP: width: 27, height: 23
gameSprite = None

gameSprite = Sprite(1,1,bytearray([1]))


gameSprite = Sprite(27,23,bytearray([255,255,127,15,15,7,135,135,65,65,97,65,65,129,49,49,103,71,7,15,15,127,255,255,255,255,255,
           255,255,128,0,22,62,255,255,128,128,182,128,128,255,127,62,0,0,0,0,0,128,254,255,255,255,255,
           127,127,127,124,120,112,112,112,65,65,65,65,65,64,64,64,112,112,112,120,124,127,127,127,127,127,127]), gameSprite.x,gameSprite.y,gameSprite.key,gameSprite.mirrorX,gameSprite.mirrorY)
responses = ' "IT IS CERTAIN",     "IT IS DECIDEDLY SO",     "WITHOUT A DOUBT",     "DEFINITELY",     "YOU MAY RELY ON IT",      "MOST LIKELY",     "OUTLOOK GOOD",    "REPLY HAZY TRY AGAIN",     "ASK AGAIN LATER",     "BETTER NOT TELL YOU NOW",     "CANNOT PREDICT NOW"     "CONCENTRATE AND ASK AGAIN",     "DONT COUNT ON IT",     "OUTLOOK NOT SO GOOD",     "VERY DOUBTFUL"'.split(',')

# Describe this function...
def Draw_Splash():
  global gameSprite, response, responses
  display.drawSprite(gameSprite)
  gameSprite.x = 20
  gameSprite.y = 5
  display.update()
  display.fill(1)

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
def Draw_Response():
  global gameSprite, response, responses
  __print_to_display__(response)
  display.update()
  display.fill(0)
  time.sleep(2)




while True:
  Draw_Splash()
  if buttons.buttonA.justPressed():
    response = random.choice(responses)
    Draw_Response()
  if buttons.buttonB.justPressed():
     thumby.reset()

#### !!!! BLOCKLY EXPORT !!!! ####