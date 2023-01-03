from thumbySprite import Sprite
import thumbyButton as buttons
from thumbyGraphics import display
import io

result = None
equation = None
Auris3x3 = None
selChar = None
selX = None
selY = None

Auris3x3 = Sprite(0,0,[])

def __setFontFromBytes__(width, height, data):
    if width > len(data) or height > 8:
        return
    display.textBitmapFile = io.BytesIO(data)
    display.textWidth = width
    display.textHeight = height
    display.textSpaceWidth = 1
    display.textBitmap = bytearray(width)
    display.textCharCount = len(data) // width

# update and send frame to the screen
def display2():
  global result, equation, Auris3x3, selChar, selX, selY
  display.drawFilledRectangle(48, 0, 19, 11, 1)
  __setFontFromBytes__(3, 3, Auris3x3.bitmap)
  display.drawText('TINY', 50, 2, 0)
  display.drawText('CALC', 50, 6, 0)
  display.drawText('7890.%', 10, 1, 1)
  display.drawText('456*/(', 10, 5, 1)
  display.drawText('123+-)', 10, 9, 1)
  display.drawRectangle((selX * 4 + 9), (selY * 4), 5, 5, 1)
  display.drawText((equation[-35 : -17]), 0, 14, 1)
  display.drawText((str(equation[-17 : ]) + '='), 0, 18, 1)
  display.setFont("/lib/font8x8.bin", 8, 8, 1)
  display.drawText(selChar, 0, 2, 1)
  display.setFont("/lib/font5x7.bin", 5, 7, 1)
  if len(result) <= 24:
    display.drawText((result[-24 : -12]), 0, 24, 1)
    display.drawText((result[-12 : ]), 0, 32, 1)
  else:
    display.drawText((str((eval((''.join([str(x) for x in ['"{:e}".format(', result, ')']])))))), 0, 32, 1)
  display.update()
  display.fill(0)


result = '?'
equation = ''
selChar = '1'
selX = 0
selY = 2
Auris3x3 = Sprite(57,40,bytearray([0,0,0,4,3,3,3,0,3,5,1,7,6,0,3,6,2,3,2,7,2,0,3,0,2,2,5,5,2,2,3,3,0,2,7,2,4,6,0,2,2,2,4,0,0,4,2,1,3,5,6,5,7,4,6,5,4,
           5,7,2,3,2,7,3,5,1,7,6,6,1,5,3,3,7,6,3,3,7,0,5,0,4,5,0,2,5,0,5,5,5,0,5,2,5,3,3,6,6,2,6,3,7,7,7,6,6,5,5,7,5,2,7,7,5,
           7,3,1,7,1,5,7,2,7,5,7,5,2,4,7,7,2,5,7,4,4,7,3,7,7,1,6,7,5,7,7,3,3,7,5,3,7,3,5,4,7,1,1,7,1,3,4,7,3,4,3,7,6,7,5,2,5,
           5,6,7,1,7,4,7,5,0,1,2,4,0,5,7,2,1,2,4,4,4,1,2,0,6,3,7,7,7,6,6,5,5,7,5,2,7,7,5,7,3,1,7,1,5,7,2,7,5,7,5,2,4,7,7,2,5,
           7,4,4,7,3,7,7,1,6,7,5,7,7,3,3,7,5,3,7,3,5,4,7,1,1,7,1,3,4,7,3,4,3,7,6,7,5,2,5,5,6,7,1,7,4,5,0,2,0,7,0,2,0,5,6,2,3]), Auris3x3.x,Auris3x3.y,Auris3x3.key,Auris3x3.mirrorX,Auris3x3.mirrorY)
while True:
  display2()
  if buttons.buttonL.justPressed():
    selX = (selX - 1) % 6
  elif buttons.buttonR.justPressed():
    selX = (selX + 1) % 6
  elif buttons.buttonU.justPressed():
    selY = (selY - 1) % 3
  elif buttons.buttonD.justPressed():
    selY = (selY + 1) % 3
  selChar = '7890.%456*/(123+-)'[int(((selY * 6 + selX) + 1) - 1)]
  if buttons.buttonA.justPressed():
    equation = str(equation) + str(selChar)
    try:
      result = str((eval(equation)))
    except:
      result = '?'

  elif buttons.buttonB.justPressed():
    equation = equation[ : -1]
    try:
      result = str((eval(equation)))
    except:
      result = '?'
