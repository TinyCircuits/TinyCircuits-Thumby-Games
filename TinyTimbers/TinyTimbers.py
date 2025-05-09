#### !!!! BLOCKLY EXPORT !!!! ####
from thumbyGraphics import display
import time
import random
from thumbySprite import Sprite
import io
import thumbyButton as buttons
Number = int
import math
from thumbySaves import saveData

TreeTrunk5Y = None
TreeTrunk = None
TreeTrunk4Y = None
TTLogo = None
TreeTrunk5Left_r_Right = None
TreeTrunk3Y = None
A_B_buttons = None
TreeTrunk2Y = None
D_pad = None
TreeTrunk1Y = None
A_B_buttons_mask = None
D_pad_mask = None
TreeTrunk4Left_r_Right = None
TTLogo_mask = None
TreeTrunk3Left_r_Right = None
TreeTrunk2Left_r_Right = None
TreeTrunk1Left_r_Right = None
Knock_out_by_branch = None
Y_N = None
NotChopTimer = None
Chop_ = None
Chops = None
BottomBranch = None
ChopStop = None
ManLeft_r_Right = None
SwingAxe = None
SwingAxeTimer = None
man_in_swing = None
TimeBar = None
Thumby_on_its_side = None
Thumby = None
Spining_arrows_frame_1 = None
Spining_arrows_frame_2 = None
SidewaysFont = None
man = None
KnockOut = None
KnockOutCover = None
smoke = None
TimeBarCover = None

TreeTrunk = Sprite(1,1,bytearray([1]))

man_in_swing = Sprite(1,1,bytearray([1]))

TimeBar = Sprite(1,1,bytearray([1]))

TTLogo = Sprite(1,1,bytearray([1]))

D_pad = Sprite(1,1,bytearray([1]))

A_B_buttons = Sprite(1,1,bytearray([1]))

Thumby_on_its_side = Sprite(1,1,bytearray([1]))

Thumby = Sprite(1,1,bytearray([1]))

Spining_arrows_frame_1 = Sprite(1,1,bytearray([1]))

Spining_arrows_frame_2 = Sprite(1,1,bytearray([1]))

TTLogo_mask = Sprite(1,1,bytearray([1]))

D_pad_mask = Sprite(1,1,bytearray([1]))

A_B_buttons_mask = Sprite(1,1,bytearray([1]))

SidewaysFont = Sprite(1,1,bytearray([1]))

man = Sprite(1,1,bytearray([1]))

KnockOut = Sprite(1,1,bytearray([1]))

KnockOutCover = Sprite(1,1,bytearray([1]))

smoke = Sprite(1,1,bytearray([1]))

TimeBarCover = Sprite(1,1,bytearray([1]))

def __setFontFromBytes__(width, height, data):
    if width > len(data) or height > 8:
        return
    display.textBitmapFile = io.BytesIO(data)
    display.textWidth = width
    display.textHeight = height
    display.textBitmap = bytearray(width)
    display.textCharCount = len(data) // width

saveData.setName(globals().get('__file__', 'FAST_EXECUTE').replace('/Games/','').strip('/').split('/')[0].split('.')[0])

# Describe this function...
def draw_tree():
  global TreeTrunk5Y, TreeTrunk, TreeTrunk4Y, TTLogo, TreeTrunk5Left_r_Right, TreeTrunk3Y, A_B_buttons, TreeTrunk2Y, D_pad, TreeTrunk1Y, A_B_buttons_mask, D_pad_mask, TreeTrunk4Left_r_Right, TTLogo_mask, TreeTrunk3Left_r_Right, TreeTrunk2Left_r_Right, TreeTrunk1Left_r_Right, Knock_out_by_branch, Y_N, NotChopTimer, Chop_, Chops, BottomBranch, ChopStop, ManLeft_r_Right, SwingAxe, SwingAxeTimer, man_in_swing, TimeBar, Thumby_on_its_side, Thumby, Spining_arrows_frame_1, Spining_arrows_frame_2, SidewaysFont, man, KnockOut, KnockOutCover, smoke, TimeBarCover
  if TreeTrunk5Left_r_Right == 1:
    TreeTrunk.mirrorY = 0 if TreeTrunk.mirrorY else 1
  TreeTrunk.x = TreeTrunk5Y
  display.drawSprite(TreeTrunk)
  if TreeTrunk5Left_r_Right == 1:
    TreeTrunk.mirrorY = 0 if TreeTrunk.mirrorY else 1
  if TreeTrunk4Left_r_Right == 1:
    TreeTrunk.mirrorY = 0 if TreeTrunk.mirrorY else 1
  TreeTrunk.x = TreeTrunk4Y
  display.drawSprite(TreeTrunk)
  if TreeTrunk4Left_r_Right == 1:
    TreeTrunk.mirrorY = 0 if TreeTrunk.mirrorY else 1
  if TreeTrunk3Left_r_Right == 1:
    TreeTrunk.mirrorY = 0 if TreeTrunk.mirrorY else 1
  TreeTrunk.x = TreeTrunk3Y
  display.drawSprite(TreeTrunk)
  if TreeTrunk3Left_r_Right == 1:
    TreeTrunk.mirrorY = 0 if TreeTrunk.mirrorY else 1
  if TreeTrunk2Left_r_Right == 1:
    TreeTrunk.mirrorY = 0 if TreeTrunk.mirrorY else 1
  TreeTrunk.x = TreeTrunk2Y
  display.drawSprite(TreeTrunk)
  if TreeTrunk2Left_r_Right == 1:
    TreeTrunk.mirrorY = 0 if TreeTrunk.mirrorY else 1
  if TreeTrunk1Left_r_Right == 1:
    TreeTrunk.mirrorY = 0 if TreeTrunk.mirrorY else 1
  TreeTrunk.x = TreeTrunk1Y
  display.drawSprite(TreeTrunk)
  if TreeTrunk1Left_r_Right == 1:
    TreeTrunk.mirrorY = 0 if TreeTrunk.mirrorY else 1

# Describe this function...
def do_something():
  global TreeTrunk5Y, TreeTrunk, TreeTrunk4Y, TTLogo, TreeTrunk5Left_r_Right, TreeTrunk3Y, A_B_buttons, TreeTrunk2Y, D_pad, TreeTrunk1Y, A_B_buttons_mask, D_pad_mask, TreeTrunk4Left_r_Right, TTLogo_mask, TreeTrunk3Left_r_Right, TreeTrunk2Left_r_Right, TreeTrunk1Left_r_Right, Knock_out_by_branch, Y_N, NotChopTimer, Chop_, Chops, BottomBranch, ChopStop, ManLeft_r_Right, SwingAxe, SwingAxeTimer, man_in_swing, TimeBar, Thumby_on_its_side, Thumby, Spining_arrows_frame_1, Spining_arrows_frame_2, SidewaysFont, man, KnockOut, KnockOutCover, smoke, TimeBarCover
  pass

# Describe this function...
def Draw_start_screen():
  global TreeTrunk5Y, TreeTrunk, TreeTrunk4Y, TTLogo, TreeTrunk5Left_r_Right, TreeTrunk3Y, A_B_buttons, TreeTrunk2Y, D_pad, TreeTrunk1Y, A_B_buttons_mask, D_pad_mask, TreeTrunk4Left_r_Right, TTLogo_mask, TreeTrunk3Left_r_Right, TreeTrunk2Left_r_Right, TreeTrunk1Left_r_Right, Knock_out_by_branch, Y_N, NotChopTimer, Chop_, Chops, BottomBranch, ChopStop, ManLeft_r_Right, SwingAxe, SwingAxeTimer, man_in_swing, TimeBar, Thumby_on_its_side, Thumby, Spining_arrows_frame_1, Spining_arrows_frame_2, SidewaysFont, man, KnockOut, KnockOutCover, smoke, TimeBarCover
  draw_tree()
  TTLogo.x += 2
  A_B_buttons.y += 2
  D_pad.y += -2
  if A_B_buttons.width == A_B_buttons_mask.width and A_B_buttons.height == A_B_buttons_mask.height:
      display.drawSpriteWithMask(A_B_buttons, A_B_buttons_mask)
  if D_pad.width == D_pad_mask.width and D_pad.height == D_pad_mask.height:
      display.drawSpriteWithMask(D_pad, D_pad_mask)
  if TTLogo.width == TTLogo_mask.width and TTLogo.height == TTLogo_mask.height:
      display.drawSpriteWithMask(TTLogo, TTLogo_mask)

# Describe this function...
def move_tree_down_by_3():
  global TreeTrunk5Y, TreeTrunk, TreeTrunk4Y, TTLogo, TreeTrunk5Left_r_Right, TreeTrunk3Y, A_B_buttons, TreeTrunk2Y, D_pad, TreeTrunk1Y, A_B_buttons_mask, D_pad_mask, TreeTrunk4Left_r_Right, TTLogo_mask, TreeTrunk3Left_r_Right, TreeTrunk2Left_r_Right, TreeTrunk1Left_r_Right, Knock_out_by_branch, Y_N, NotChopTimer, Chop_, Chops, BottomBranch, ChopStop, ManLeft_r_Right, SwingAxe, SwingAxeTimer, man_in_swing, TimeBar, Thumby_on_its_side, Thumby, Spining_arrows_frame_1, Spining_arrows_frame_2, SidewaysFont, man, KnockOut, KnockOutCover, smoke, TimeBarCover
  TreeTrunk5Y = (TreeTrunk5Y if isinstance(TreeTrunk5Y, Number) else 0) + -3
  TreeTrunk4Y = (TreeTrunk4Y if isinstance(TreeTrunk4Y, Number) else 0) + -3
  TreeTrunk3Y = (TreeTrunk3Y if isinstance(TreeTrunk3Y, Number) else 0) + -3
  TreeTrunk2Y = (TreeTrunk2Y if isinstance(TreeTrunk2Y, Number) else 0) + -3
  TreeTrunk1Y = (TreeTrunk1Y if isinstance(TreeTrunk1Y, Number) else 0) + -3


display.setFont("/lib/font8x8.bin", 8, 8, display.textSpaceWidth)
display.textSpaceWidth = 0
display.drawText(str('A game by:'), 0, 9, 1)
display.drawText(str('MrGiraffe'), 0, 18, 1)
display.update()
display.fill(0)
time.sleep(3)
display.drawText(str('Game idea'), 0, 0, 1)
display.drawText(str('by:'), 0, 9, 1)
display.drawText(str('MrGiraffe'), 0, 18, 1)
display.drawText(str('-Jr'), 0, 27, 1)
display.update()
display.fill(0)
time.sleep(3)
display.drawText(str('pixel art '), 0, 0, 1)
display.drawText(str('by:'), 0, 9, 1)
display.drawText(str('Ayre-'), 0, 18, 1)
display.drawText(str('Guitar'), 0, 27, 1)
display.update()
display.fill(0)
time.sleep(3.4)
display.drawText(str('this side'), 0, 9, 1)
display.drawText(str('up ---->'), 0, 18, 1)
display.update()
display.fill(0)
time.sleep(3)
while True:
  Knock_out_by_branch = 1
  Y_N = 1
  NotChopTimer = 18
  Chop_ = 0
  Chops = 0
  BottomBranch = 1
  ChopStop = 0
  ManLeft_r_Right = 0
  SwingAxe = 0
  SwingAxeTimer = 0
  TreeTrunk1Y = 0
  TreeTrunk2Y = 18
  TreeTrunk3Y = 36
  TreeTrunk4Y = 54
  TreeTrunk5Y = 72
  TreeTrunk1Left_r_Right = random.randint(0, 1)
  TreeTrunk2Left_r_Right = random.randint(0, 1)
  TreeTrunk3Left_r_Right = random.randint(0, 1)
  TreeTrunk4Left_r_Right = random.randint(0, 1)
  TreeTrunk5Left_r_Right = random.randint(0, 1)
  TreeTrunk.y = 0
  man_in_swing.x = 0
  man_in_swing.y = 5
  TimeBar.x = 60
  TimeBar.y = 10
  TTLogo.x = 54
  TTLogo.y = 0
  D_pad.y = 1
  D_pad.x = 13
  A_B_buttons.y = 26
  A_B_buttons.x = 13
  Thumby_on_its_side.x = 40
  Thumby_on_its_side.y = 3
  Thumby.x = 40
  Thumby.y = 3
  Spining_arrows_frame_1.x = 25
  Spining_arrows_frame_1.y = 12
  Spining_arrows_frame_2.x = 25
  Spining_arrows_frame_2.y = 12
  # Width: 18
  # Hight: 40
  TTLogo = Sprite(18,40,bytearray([0,0,136,136,136,136,8,136,136,128,190,0,0,0,0,0,0,0,
              0,0,130,130,130,130,130,146,170,68,130,0,0,64,64,64,64,224,
              0,0,138,146,162,146,138,146,162,146,138,0,0,170,42,42,170,154,
              0,0,22,16,16,144,86,144,16,144,86,0,0,1,2,3,2,2,
              0,0,17,41,69,32,16,8,69,40,16,0,0,0,0,0,0,0]), TTLogo.x,TTLogo.y,TTLogo.key,TTLogo.mirrorX,TTLogo.mirrorY)
  # Width: 18
  # Hight: 40
  TTLogo_mask = Sprite(18,40,bytearray([0,255,255,255,255,255,255,255,255,255,255,255,0,0,0,0,0,0,
              0,255,255,255,255,255,255,255,255,255,255,255,240,240,240,240,240,240,
              0,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,
              0,255,255,255,255,255,255,255,255,255,255,255,7,7,7,7,7,7,
              0,255,255,255,255,255,255,255,255,255,255,255,0,0,0,0,0,0]), TTLogo_mask.x,TTLogo_mask.y,TTLogo_mask.key,TTLogo_mask.mirrorX,TTLogo_mask.mirrorY)
  # Width: 13
  # Hight: 13
  D_pad = Sprite(13,13,bytearray([64,224,240,64,68,230,255,230,68,64,240,224,64,
             0,0,1,0,4,12,31,12,4,0,1,0,0]), D_pad.x,D_pad.y,D_pad.key,D_pad.mirrorX,D_pad.mirrorY)
  # Width: 13
  # Hight: 13
  D_pad_mask = Sprite(13,13,bytearray([224,248,248,244,254,255,255,255,238,244,248,240,224,
              2,5,3,5,14,31,31,31,14,5,3,1,0]), D_pad_mask.x,D_pad_mask.y,D_pad_mask.key,D_pad_mask.mirrorX,D_pad_mask.mirrorY)
  # Width: 13
  # Hight: 13
  A_B_buttons = Sprite(13,13,bytearray([128,192,192,192,192,192,190,107,107,99,107,119,62,
              15,28,26,28,26,28,15,0,0,0,0,0,0]), A_B_buttons.x,A_B_buttons.y,A_B_buttons.key,A_B_buttons.mirrorX,A_B_buttons.mirrorY)
  # Width: 13
  # Hight: 13
  A_B_buttons_mask = Sprite(13,13,bytearray([192,224,224,224,224,254,255,255,255,255,255,255,127,
              31,31,31,31,31,31,31,15,0,0,0,0,0]), A_B_buttons_mask.x,A_B_buttons_mask.y,A_B_buttons_mask.key,A_B_buttons_mask.mirrorX,A_B_buttons_mask.mirrorY)
  # Width: 70
  # Hight: 56
  SidewaysFont = Sprite(70,56,bytearray([0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,
             0,0,0,0,0,0,0,0,0,0,14,25,21,19,14,7,2,2,3,2,15,1,14,8,7,7,8,7,8,7,4,4,7,5,5,7,8,15,1,15,6,9,15,1,6,1,2,4,8,15,6,9,6,9,6,4,4,7,5,7,0,0,0,0,0,0,0,0,0,0,
             0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,
             0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,
             0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,
             0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,
             0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]), SidewaysFont.x,SidewaysFont.y,SidewaysFont.key,SidewaysFont.mirrorX,SidewaysFont.mirrorY)
  # Width: 18
  # Hight: 40
  TreeTrunk = Sprite(18,40,bytearray([0,0,0,0,0,0,0,0,0,0,0,0,0,0,112,128,192,48,
             128,128,128,128,128,128,128,128,128,128,128,128,128,194,228,254,203,128,
             2,82,82,68,10,42,42,34,34,34,8,104,106,10,66,74,74,64,
             1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,
             0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]), TreeTrunk.x,TreeTrunk.y,TreeTrunk.key,TreeTrunk.mirrorX,TreeTrunk.mirrorY)
  # Width: 10
  # Hight: 10
  man = Sprite(10,10,bytearray([220,216,248,0,254,254,140,116,55,119,
             1,0,0,0,0,0,0,0,0,0]), man.x,man.y,man.key,man.mirrorX,man.mirrorY)
  # Width: 10
  # Hight: 10
  man_in_swing = Sprite(10,10,bytearray([220,216,248,0,248,248,136,112,48,112,
             1,0,0,0,3,0,0,0,0,0]), man_in_swing.x,man_in_swing.y,man_in_swing.key,man_in_swing.mirrorX,man_in_swing.mirrorY)
  # Width: 10
  # Hight: 10
  KnockOut = Sprite(10,10,bytearray([248,248,248,248,112,32,112,32,0,0,
             0,0,0,0,0,0,0,0,0,0]), KnockOut.x,KnockOut.y,KnockOut.key,KnockOut.mirrorX,KnockOut.mirrorY)
  # Width: 10
  # Hight: 10
  KnockOutCover = Sprite(10,10,bytearray([252,252,252,252,248,112,248,112,32,0,
             1,1,1,1,0,0,0,0,0,0]), KnockOutCover.x,KnockOutCover.y,KnockOutCover.key,KnockOutCover.mirrorX,KnockOutCover.mirrorY)
  # Width: 10
  # Hight: 10
  smoke = Sprite(10,10,bytearray([16,134,198,56,184,58,128,140,172,0,
             0,1,1,0,1,0,1,1,1,0]), smoke.x,smoke.y,smoke.key,smoke.mirrorX,smoke.mirrorY)
  # Width: 10
  # Hight: 20
  TimeBar = Sprite(10,20,bytearray([254,1,1,1,1,1,1,1,1,254,
             255,0,0,0,0,0,0,0,0,255,
             7,8,8,8,8,8,8,8,8,7]), TimeBar.x,TimeBar.y,TimeBar.key,TimeBar.mirrorX,TimeBar.mirrorY)
  # Width: 10
  # Hight: 20
  TimeBarCover = Sprite(10,20,bytearray([255,255,255,255,255,255,255,255,255,255,
             255,255,255,255,255,255,255,255,255,255,
             15,15,15,15,15,15,15,15,15,15]), TimeBarCover.x,TimeBarCover.y,TimeBarCover.key,TimeBarCover.mirrorX,TimeBarCover.mirrorY)
  # Width: 32
  # Hight: 32
  Thumby = Sprite(32,32,bytearray([0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,
             0,0,0,255,1,33,65,1,1,1,49,49,253,253,49,49,1,1,253,5,5,5,5,5,5,5,253,1,255,0,0,0,
             0,0,0,127,64,65,66,64,64,64,64,70,70,64,88,88,64,64,95,80,80,80,80,80,80,80,95,64,127,0,0,0,
             0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]), Thumby.x,Thumby.y,Thumby.key,Thumby.mirrorX,Thumby.mirrorY)
  display.textSpaceWidth = 1
  __setFontFromBytes__(5, 5, SidewaysFont.bitmap)
  while True:
    draw_tree()
    man.y = 25
    man.mirrorY = 0 if man.mirrorY else 1
    display.drawSprite(man)
    man.mirrorY = 0 if man.mirrorY else 1
    man.y = 5
    display.drawSprite(man)
    if A_B_buttons.width == A_B_buttons_mask.width and A_B_buttons.height == A_B_buttons_mask.height:
        display.drawSpriteWithMask(A_B_buttons, A_B_buttons_mask)
    if D_pad.width == D_pad_mask.width and D_pad.height == D_pad_mask.height:
        display.drawSpriteWithMask(D_pad, D_pad_mask)
    if TTLogo.width == TTLogo_mask.width and TTLogo.height == TTLogo_mask.height:
        display.drawSpriteWithMask(TTLogo, TTLogo_mask)
    if buttons.actionJustPressed():
      man.y = 25
      man_in_swing.y = 25
      for count in range(9):
        Draw_start_screen()
        display.drawSprite(man)
        time.sleep(0.01)
        display.update()
        display.fill(0)
      ManLeft_r_Right = 1
      SwingAxe = 1
      break
    if buttons.dpadJustPressed():
      man.y = 5
      man_in_swing.y = 5
      for count2 in range(9):
        Draw_start_screen()
        display.drawSprite(man)
        time.sleep(0.01)
        display.update()
        display.fill(0)
      ManLeft_r_Right = 0
      SwingAxe = 1
      break
    display.update()
    display.fill(0)
  while True:
    draw_tree()
    if buttons.dpadJustPressed() and SwingAxeTimer == 0:
      if NotChopTimer < 18:
        NotChopTimer = (NotChopTimer if isinstance(NotChopTimer, Number) else 0) + 1
      ManLeft_r_Right = 0
      SwingAxe = 1
      man.y = 5
      man_in_swing.y = 5
    if buttons.actionJustPressed() and SwingAxeTimer == 0:
      if NotChopTimer < 18:
        NotChopTimer = (NotChopTimer if isinstance(NotChopTimer, Number) else 0) + 1
      ManLeft_r_Right = 1
      SwingAxe = 1
      man.y = 25
      man_in_swing.y = 25
    if ManLeft_r_Right == 1:
      man.mirrorY = 0 if man.mirrorY else 1
      man_in_swing.mirrorY = 0 if man_in_swing.mirrorY else 1
    if SwingAxe == 1:
      SwingAxeTimer = (SwingAxeTimer if isinstance(SwingAxeTimer, Number) else 0) + 1
    if SwingAxeTimer < 20 and SwingAxe == 1:
      if SwingAxeTimer > 8:
        display.drawSprite(man_in_swing)
        Chop_ = 1
      else:
        display.drawSprite(man)
    else:
      display.drawSprite(man)
      SwingAxe = 0
      SwingAxeTimer = 0
    if ManLeft_r_Right == 1:
      man.mirrorY = 0 if man.mirrorY else 1
      man_in_swing.mirrorY = 0 if man_in_swing.mirrorY else 1
    if ChopStop >= 1:
      Chop_ = 0
      ChopStop = 0
    if Chop_ == 1:
      move_tree_down_by_3()
      ChopStop = (ChopStop if isinstance(ChopStop, Number) else 0) + 1
      # Tree Branch detection system
      if BottomBranch == 1:
        if ManLeft_r_Right == TreeTrunk1Left_r_Right:
          break
      if BottomBranch == 2:
        if ManLeft_r_Right == TreeTrunk2Left_r_Right:
          break
      if BottomBranch == 3:
        if ManLeft_r_Right == TreeTrunk3Left_r_Right:
          break
      if BottomBranch == 4:
        if ManLeft_r_Right == TreeTrunk4Left_r_Right:
          break
      if BottomBranch == 5:
        if ManLeft_r_Right == TreeTrunk5Left_r_Right:
          break
    if TreeTrunk5Y == -18:
      TreeTrunk5Y = 72
      TreeTrunk5Left_r_Right = random.randint(0, 1)
      BottomBranch = 1
      Chops = (Chops if isinstance(Chops, Number) else 0) + 1
    if TreeTrunk4Y == -18:
      TreeTrunk4Y = 72
      TreeTrunk4Left_r_Right = random.randint(0, 1)
      BottomBranch = 5
      Chops = (Chops if isinstance(Chops, Number) else 0) + 1
    if TreeTrunk3Y == -18:
      TreeTrunk3Y = 72
      TreeTrunk3Left_r_Right = random.randint(0, 1)
      BottomBranch = 4
      Chops = (Chops if isinstance(Chops, Number) else 0) + 1
    if TreeTrunk2Y == -18:
      TreeTrunk2Y = 72
      TreeTrunk2Left_r_Right = random.randint(0, 1)
      BottomBranch = 3
      Chops = (Chops if isinstance(Chops, Number) else 0) + 1
    if TreeTrunk1Y == -18:
      TreeTrunk1Y = 72
      TreeTrunk1Left_r_Right = random.randint(0, 1)
      BottomBranch = 2
      Chops = (Chops if isinstance(Chops, Number) else 0) + 1
    display.drawText(str(Chops), 72 - len(str(Chops)) * 5, 0, 1)
    if TimeBar.width == TimeBarCover.width and TimeBar.height == TimeBarCover.height:
        display.drawSpriteWithMask(TimeBar, TimeBarCover)
    if time.ticks_ms() % 40 == 0:
      NotChopTimer = (NotChopTimer if isinstance(NotChopTimer, Number) else 0) + -1
    display.drawFilledRectangle(61, 11, 8, round(NotChopTimer), 1)
    if round(NotChopTimer) <= 0:
      Knock_out_by_branch = 0
      break
    display.update()
    display.fill(0)
  KnockOut.x = man.x
  KnockOut.y = man.y
  smoke.x = man.x
  smoke.y = man.y
  if random.randint(0, 1) == 0:
    KnockOut.mirrorY = 0 if KnockOut.mirrorY else 1
  if random.randint(0, 1) == 0:
    smoke.mirrorY = 0 if smoke.mirrorY else 1
  draw_tree()
  display.drawSprite(smoke)
  if TimeBar.width == TimeBarCover.width and TimeBar.height == TimeBarCover.height:
      display.drawSpriteWithMask(TimeBar, TimeBarCover)
  display.drawText(str(Chops), 60, 0, 1)
  display.drawFilledRectangle(61, 11, 8, round(NotChopTimer), 1)
  display.update()
  display.fill(0)
  time.sleep(0.13)
  for count3 in range(3):
    if Knock_out_by_branch == 1:
      move_tree_down_by_3()
    draw_tree()
    display.drawText(str(Chops), 60, 0, 1)
    if TimeBar.width == TimeBarCover.width and TimeBar.height == TimeBarCover.height:
        display.drawSpriteWithMask(TimeBar, TimeBarCover)
    display.drawFilledRectangle(61, 11, 8, round(NotChopTimer), 1)
    if KnockOut.width == KnockOutCover.width and KnockOut.height == KnockOutCover.height:
        display.drawSpriteWithMask(KnockOut, KnockOutCover)
    display.drawText(str(Chops), 60, 0, 1)
    display.update()
    display.fill(0)
    time.sleep(0.1)
  time.sleep(2)
  if not saveData.hasItem('high score'):
    saveData.setItem('high score', 0)
    saveData.save()
  if Chops > saveData.getItem('high score'):
    saveData.setItem('high score', Chops)
    saveData.save()
  display.setFont("/lib/font8x8.bin", 8, 8, display.textSpaceWidth)
  display.textSpaceWidth = 0
  display.drawText(str('Game Over!'), 0, 0, 1)
  display.setFont("/lib/font5x7.bin", 5, 7, display.textSpaceWidth)
  display.textSpaceWidth = 1
  display.drawText(str('Score:' + str(Chops)), 0, 9, 1)
  display.drawText(str('High:' + str(saveData.getItem('high score'))), 0, 17, 1)
  display.setFont("/lib/font3x5.bin", 3, 5, display.textSpaceWidth)
  display.drawText(str('Again?  A-Y B-N'), 0, 26, 1)
  display.setFont("/lib/font5x7.bin", 5, 7, display.textSpaceWidth)
  display.update()
  display.fill(0)
  while True:
    if buttons.buttonA.justPressed():
      Y_N = 1
      break
    if buttons.buttonB.justPressed():
      Y_N = 0
      break
  if Y_N == 0:
    break
  time.sleep(1)

#### !!!! BLOCKLY EXPORT !!!! ####