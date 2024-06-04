#### !!!! BLOCKLY EXPORT !!!! ####
from thumbyGraphics import display
from thumbySprite import Sprite
import thumbyButton as buttons
Number = int
from thumbyAudio import audio
import time
from thumbySaves import saveData

round2 = None
score = None
scoreLevel = None
gnome = None
titleGnome = None
hand = None
direction = None
roundScore = None
currentRound = None

gnome = Sprite(1,1,bytearray([1]))

titleGnome = Sprite(1,1,bytearray([1]))

hand = Sprite(1,1,bytearray([1]))

saveData.setName(globals().get('__file__', 'FAST_EXECUTE').replace('/Games/','').strip('/').split('/')[0].split('.')[0])


round2 = 1
score = 0
scoreLevel = 0
display.setFPS(30)
gnome = Sprite(32,32,bytearray([0,0,0,0,0,0,0,0,0,0,128,192,64,127,1,1,1,125,69,197,133,5,29,113,65,67,126,0,0,0,0,0,
           224,48,16,24,12,4,4,6,3,1,1,0,0,0,0,0,0,0,0,0,1,1,3,6,4,12,8,24,16,48,32,224,
           255,252,252,252,132,132,132,4,4,132,132,4,6,114,82,82,82,114,2,2,130,134,4,4,4,4,4,4,252,252,252,255,
           3,7,15,15,15,31,31,30,62,60,61,125,125,121,249,249,249,121,125,125,61,60,62,30,31,31,15,15,15,7,7,3]), gnome.x,gnome.y,gnome.key,gnome.mirrorX,gnome.mirrorY)
titleGnome = Sprite(32,32,bytearray([0,0,0,0,0,0,0,0,0,0,0,0,0,0,192,126,3,1,249,133,5,5,29,113,65,67,126,0,0,0,0,0,
           0,0,0,0,0,0,128,64,32,24,8,12,6,3,1,0,0,0,0,1,7,12,24,48,224,0,0,0,0,0,0,0,
           0,0,0,0,0,0,255,252,252,4,4,132,4,116,86,82,82,114,2,130,2,6,252,252,255,0,0,0,0,0,0,0,
           0,0,0,0,0,0,3,7,15,31,60,60,125,121,249,249,249,121,125,60,60,31,15,7,3,0,0,0,0,0,0,0]), titleGnome.x,titleGnome.y,titleGnome.key,titleGnome.mirrorX,titleGnome.mirrorY)
titleGnome.x = -3
titleGnome.y = 8
hand = Sprite(32,27,bytearray([128,64,32,32,32,64,128,248,4,2,2,2,4,252,2,1,1,1,2,252,8,4,4,4,8,240,16,8,8,8,16,224,
           255,0,0,0,0,0,0,15,0,0,0,0,0,15,0,0,0,0,0,15,0,0,0,0,0,15,0,0,0,0,0,255,
           7,12,56,96,192,128,128,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,128,192,96,48,31,
           0,0,0,0,0,0,7,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,7,0,0,0,0]), hand.x,hand.y,hand.key,hand.mirrorX,hand.mirrorY)
hand.x = 20
hand.y = 12
while not buttons.actionJustPressed():
  display.drawSprite(titleGnome)
  display.drawText(str('SLAP A GNOME'), 0, 0, 1)
  display.drawText(str('A/B to'), 28, 12, 1)
  display.drawText(str('Start'), 28, 22, 1)
  display.drawText(str('& Slap'), 28, 32, 1)
  display.update()
  display.fill(0)
gnome.y = 0
gnome.x = 0
while True:
  gnome.x = 0
  direction = round2
  while not buttons.actionJustPressed():
    gnome.x += direction
    if gnome.x >= 72:
      direction = round2 * -1
    elif gnome.x <= -32:
      direction = round2
    display.drawSprite(gnome)
    display.update()
    display.fill(0)
  display.drawSprite(gnome)
  display.drawSprite(hand)
  if gnome.x >= 5 and gnome.x <= 35:
    display.drawLine(hand.x + 15, 10, hand.x + 15, 0, 1)
    display.drawLine(hand.x + 9, 10, hand.x + 4, 2, 1)
    display.drawLine(hand.x + 8, 10, hand.x + 3, 2, 1)
    display.drawLine(hand.x + 0, 14, hand.x - 7, 8, 1)
    display.drawLine(hand.x - -1, 14, hand.x - 8, 8, 1)
    display.drawLine(hand.x + 25, 10, hand.x + 30, 2, 1)
    display.drawLine(hand.x + 26, 10, hand.x + 31, 2, 1)
    display.drawLine(hand.x + 31, 14, hand.x + 38, 8, 1)
    display.drawLine(hand.x + 32, 14, hand.x + 39, 8, 1)
    display.update()
    display.fill(0)
    roundScore = gnome.x - 4 if gnome.x <= 20 else (gnome.x - (gnome.x - 20) * 2) - 4
    if roundScore == 16:
      roundScore = roundScore + 4
    currentRound = round2
    round2 = (round2 if isinstance(round2, Number) else 0) + 1
    score = (score if isinstance(score, Number) else 0) + roundScore
    if roundScore != 20:
      audio.playBlocking(590, 100)
      audio.stop()
      time.sleep_ms(25)
      audio.playBlocking(615, 100)
      audio.stop()
      time.sleep_ms(25)
      audio.playBlocking(640, 100)
      audio.stop()
      time.sleep_ms(25)
      audio.playBlocking(665, 100)
      audio.stop()
      time.sleep_ms(25)
      audio.playBlocking(690, 100)
      audio.stop()
      time.sleep_ms(25)
      audio.playBlocking(715, 100)
      audio.stop()
      time.sleep_ms(25)
      audio.playBlocking(740, 500)
    else:
      audio.playBlocking(740, 100)
      audio.stop()
      time.sleep_ms(25)
      audio.playBlocking(765, 100)
      audio.stop()
      time.sleep_ms(25)
      audio.playBlocking(790, 100)
      audio.stop()
      time.sleep_ms(25)
      audio.playBlocking(815, 100)
      audio.stop()
      time.sleep_ms(25)
      audio.playBlocking(840, 100)
      audio.stop()
      time.sleep_ms(25)
      audio.playBlocking(865, 100)
      audio.stop()
      time.sleep_ms(25)
      audio.playBlocking(890, 500)
      audio.stop()
    while not buttons.actionJustPressed():
      if roundScore == 20:
        display.drawText(str('*'), 0, 0, 1)
        display.drawText(str('*FULL'), 5, 0, 1)
        display.drawText(str(' SLAP*'), 32, 0, 1)
        display.drawText(str('*'), 67, 0, 1)
      else:
        display.setFont("/lib/font8x8.bin", 8, 8, display.textSpaceWidth)
        display.drawText(str('!!SLAP!!'), 0, 0, 1)
        display.setFont("/lib/font5x7.bin", 5, 7, display.textSpaceWidth)
      display.drawText(str('Gnome'), 0, 13, 1)
      display.drawText(str(currentRound), 36, 13, 1)
      display.drawText(str(':'), 48, 13, 1)
      display.drawText(str(roundScore), 55, 13, 1)
      display.drawText(str('Total:'), 18, 23, 1)
      display.drawText(str(score), 55, 23, 1)
      display.drawText(str('A/B:Gnome'), 2, 33, 1)
      display.drawText(str(round2), 59, 33, 1)
      display.update()
      display.fill(0)
  else:
    display.update()
    display.fill(0)
    audio.playBlocking(250, 500)
    audio.stop()
    time.sleep_ms(100)
    audio.playBlocking(200, 500)
    audio.stop()
    time.sleep_ms(100)
    audio.playBlocking(150, 500)
    audio.stop()
    time.sleep_ms(100)
    audio.playBlocking(100, 500)
    audio.stop()
    round2 = (round2 if isinstance(round2, Number) else 0) + -1
    if saveData.hasItem('high score'):
      if score > saveData.getItem('high score'):
        saveData.setItem('high score', score)
        saveData.save()
    else:
      saveData.setItem('high score', score)
      saveData.save()
    if saveData.hasItem('high round'):
      if round2 > saveData.getItem('high round'):
        saveData.setItem('high round', round2)
        saveData.save()
    else:
      saveData.setItem('high round', round2)
      saveData.save()
    display.drawText(str('MISSED GNOME'), 1, 0, 1)
    display.drawText(str('He ate all'), 0, 11, 1)
    display.drawText(str('your food!'), 15, 22, 1)
    display.drawLine(0, 36, 7, 36, 1)
    display.drawText(str('GAME'), 11, 33, 1)
    display.drawText(str('OVER'), 39, 33, 1)
    display.drawLine(64, 36, 71, 36, 1)
    display.update()
    display.fill(0)
    time.sleep(5)
    while True:
      display.drawText(str('Gnome'), 0, 0, 1)
      display.drawText(str(round2), 33, 0, 1)
      display.drawText(str('Hi'), 48, 0, 1)
      display.drawText(str(saveData.getItem('high round')), 61, 0, 1)
      display.drawText(str('Score'), 18, 10, 1)
      display.drawText(str(score), 54, 10, 1)
      display.drawText(str('Hi Score'), 0, 20, 1)
      display.drawText(str(saveData.getItem('high score')), 54, 20, 1)
      display.drawText(str('A:Slap'), 0, 30, 1)
      display.drawText(str('B:Quit'), 39, 30, 1)
      display.update()
      display.fill(0)
      if buttons.buttonA.justPressed():
        round2 = 1
        score = 0
        break
      elif buttons.buttonB.justPressed():
        display.setFont("/lib/font5x7.bin", 5, 7, display.textSpaceWidth)
        display.drawText(str('Credits'), 16, 0, 1)
        display.drawLine(15, 9, 57, 9, 1)
        display.drawText(str('Kiki & Neil'), 4, 12, 1)
        display.drawText(str('Hennessy'), 13, 22, 1)
        display.setFont("/lib/font3x5.bin", 3, 5, display.textSpaceWidth)
        display.drawText(str('Thanks for playing'), 0, 32, 1)
        display.update()
        display.fill(0)
        time.sleep(3)
        exec('import thumbyHardware' + '\n' +
        'thumbyHardware.reset()')

audio.stop()

#### !!!! BLOCKLY EXPORT !!!! ####