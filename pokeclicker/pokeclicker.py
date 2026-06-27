#### !!!! BLOCKLY EXPORT !!!! ####
from thumbySprite import Sprite
from thumbySaves import saveData
from thumbyGraphics import display
import thumbyButton as buttons
Number = int

gameSprite = None
score = None

gameSprite = Sprite(1,1,bytearray([1]))

saveData.setName(globals().get('__file__', 'FAST_EXECUTE').replace('/Games/','').strip('/').split('/')[0].split('.')[0])


gameSprite = Sprite(29,28,bytearray([255,255,255,31,31,3,3,131,131,224,224,224,128,128,0,0,0,0,3,3,3,3,3,31,31,255,255,255,255,
           1,1,1,0,0,0,0,1,1,15,15,15,193,193,192,192,0,0,0,0,0,0,0,0,0,1,1,255,255,
           248,248,248,135,135,120,120,120,120,248,248,248,231,231,231,231,248,248,120,120,120,120,120,135,135,248,248,255,255,
           15,15,15,15,15,14,14,14,14,1,1,1,1,1,1,1,1,1,14,14,14,14,14,15,15,15,15,15,15]), gameSprite.x,gameSprite.y,gameSprite.key,gameSprite.mirrorX,gameSprite.mirrorY)
score = saveData.getItem('score')
while not False:
  display.fill(1)
  display.drawSprite(gameSprite)
  gameSprite.x = 20
  gameSprite.y = 7
  if buttons.actionJustPressed():
    score = saveData.getItem('score')
    gameSprite.mirrorX = 0 if gameSprite.mirrorX else 1
    score = (score if isinstance(score, Number) else 0) + 1
    saveData.setItem('score', score)
    saveData.save()
    display.drawText(str(score), 0, 32, 0)
    display.update()

display.update()

#### !!!! BLOCKLY EXPORT !!!! ####