from thumbySprite import Sprite
from thumbyGraphics import display
import io
import time
import thumbyButton as buttons
from thumbyAudio import audio
from thumbySaves import saveData
import random
Number = int

Score = None
title_hoist_limit = None
pipe_slide_limit = None
lowering_limit = None
pipe_1 = None
pipe_2 = None
Title_title = None
Bottom_pipes = None
pipe_3 = None
top_pipes = None
Pipe_Mask = None
Bird = None
Bird_Mask = None
bottom_pipe_mask = None
Title_background = None
ThumBirdText = None
Bird_y = None
Bird_acceleration = None
acceleration_regulator = None
bird_hight = None
bird_legth = None

pipe_1 = Sprite(1,1,bytearray([1]))

pipe_2 = Sprite(1,1,bytearray([1]))

pipe_3 = Sprite(1,1,bytearray([1]))

Pipe_Mask = Sprite(1,1,bytearray([1]))

Bird = Sprite(1,1,bytearray([1]))

Bird_Mask = Sprite(1,1,bytearray([1]))

bottom_pipe_mask = Sprite(1,1,bytearray([1]))

top_pipes = Sprite(1,1,bytearray([1]))

Bottom_pipes = Sprite(1,1,bytearray([1]))

Title_background = Sprite(1,1,bytearray([1]))

Title_title = Sprite(1,1,bytearray([1]))

ThumBirdText = Sprite(1,1,bytearray([1]))

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
def move_title_pipes_and_bird_down__move_background_out_the_bottom():
  global Score, title_hoist_limit, pipe_slide_limit, lowering_limit, pipe_1, pipe_2, Title_title, Bottom_pipes, pipe_3, top_pipes, Pipe_Mask, Bird, Bird_Mask, bottom_pipe_mask, Title_background, ThumBirdText, Bird_y, Bird_acceleration, acceleration_regulator, bird_hight, bird_legth
  lowering_limit = 0
  audio.playBlocking(2800, 100)
  time.sleep(0.1)
  audio.playBlocking(2800, 600)
  while True:
    if lowering_limit < 6:
      Title_title.y += 1
      Bottom_pipes.y += 1
    if lowering_limit < 21:
      Title_background.y += 1
    if lowering_limit < 9:
      Bird.y += 1
    if Title_background.width == Title_background.width and Title_background.height == Title_background.height:
        display.drawSpriteWithMask(Title_background, Title_background)
    if Bottom_pipes.width == bottom_pipe_mask.width and Bottom_pipes.height == bottom_pipe_mask.height:
        display.drawSpriteWithMask(Bottom_pipes, bottom_pipe_mask)
    if Title_title.width == Title_title.width and Title_title.height == Title_title.height:
        display.drawSpriteWithMask(Title_title, Title_title)
    if top_pipes.width == top_pipes.width and top_pipes.height == top_pipes.height:
        display.drawSpriteWithMask(top_pipes, top_pipes)
    if Bird.width == Bird_Mask.width and Bird.height == Bird_Mask.height:
        display.drawSpriteWithMask(Bird, Bird_Mask)
    display.drawLine(0, 0, 72, 0, 1)
    display.drawLine(0, 39, 72, 39, 1)
    lowering_limit = (lowering_limit if isinstance(lowering_limit, Number) else 0) + 1
    if lowering_limit == 21:
      break
    display.update()
    display.fill(0)

# Describe this function...
def hoist_title():
  global Score, title_hoist_limit, pipe_slide_limit, lowering_limit, pipe_1, pipe_2, Title_title, Bottom_pipes, pipe_3, top_pipes, Pipe_Mask, Bird, Bird_Mask, bottom_pipe_mask, Title_background, ThumBirdText, Bird_y, Bird_acceleration, acceleration_regulator, bird_hight, bird_legth
  title_hoist_limit = 0
  while title_hoist_limit != 20:
    Title_title.y += -1
    title_hoist_limit = (title_hoist_limit if isinstance(title_hoist_limit, Number) else 0) + 1
    if Title_title.width == Title_title.width and Title_title.height == Title_title.height:
        display.drawSpriteWithMask(Title_title, Title_title)
    if Bird.width == Bird_Mask.width and Bird.height == Bird_Mask.height:
        display.drawSpriteWithMask(Bird, Bird_Mask)
    if top_pipes.width == top_pipes.width and top_pipes.height == top_pipes.height:
        display.drawSpriteWithMask(top_pipes, top_pipes)
    if Bottom_pipes.width == bottom_pipe_mask.width and Bottom_pipes.height == bottom_pipe_mask.height:
        display.drawSpriteWithMask(Bottom_pipes, bottom_pipe_mask)
    display.drawLine(0, 0, 72, 0, 1)
    display.drawLine(0, 39, 72, 39, 1)
    display.update()
    display.fill(0)

# Describe this function...
def slide_pipes_and_bird():
  global Score, title_hoist_limit, pipe_slide_limit, lowering_limit, pipe_1, pipe_2, Title_title, Bottom_pipes, pipe_3, top_pipes, Pipe_Mask, Bird, Bird_Mask, bottom_pipe_mask, Title_background, ThumBirdText, Bird_y, Bird_acceleration, acceleration_regulator, bird_hight, bird_legth
  pipe_slide_limit = 0
  while pipe_slide_limit != 28:
    Bottom_pipes.x += -3
    top_pipes.x += -3
    Bird.x += -1
    pipe_slide_limit = (pipe_slide_limit if isinstance(pipe_slide_limit, Number) else 0) + 1
    if top_pipes.width == top_pipes.width and top_pipes.height == top_pipes.height:
        display.drawSpriteWithMask(top_pipes, top_pipes)
    if Bottom_pipes.width == bottom_pipe_mask.width and Bottom_pipes.height == bottom_pipe_mask.height:
        display.drawSpriteWithMask(Bottom_pipes, bottom_pipe_mask)
    if Title_title.width == Title_title.width and Title_title.height == Title_title.height:
        display.drawSpriteWithMask(Title_title, Title_title)
    if Bird.width == Bird_Mask.width and Bird.height == Bird_Mask.height:
        display.drawSpriteWithMask(Bird, Bird_Mask)
    display.drawLine(0, 0, 72, 0, 1)
    display.drawLine(0, 39, 72, 39, 1)
    display.update()
    display.fill(0)

# Describe this function...
def check_high_score():
  global Score, title_hoist_limit, pipe_slide_limit, lowering_limit, pipe_1, pipe_2, Title_title, Bottom_pipes, pipe_3, top_pipes, Pipe_Mask, Bird, Bird_Mask, bottom_pipe_mask, Title_background, ThumBirdText, Bird_y, Bird_acceleration, acceleration_regulator, bird_hight, bird_legth
  if Score > saveData.getItem('high score'):
    saveData.setItem('high score', Score)
    saveData.save()


Score = 0
pipe_1 = Sprite(8,60,bytearray([0,255,0,0,230,0,255,0,
           0,255,0,0,253,0,255,0,
           12,15,12,12,12,12,15,12,
           0,0,0,0,0,0,0,0,
           0,0,0,0,0,0,0,0,
           3,255,3,3,243,3,255,3,
           0,255,0,0,123,0,255,0,
           0,15,0,0,6,0,15,0]), pipe_1.x,pipe_1.y,pipe_1.key,pipe_1.mirrorX,pipe_1.mirrorY)
pipe_2 = Sprite(8,60,bytearray([0,255,0,0,230,0,255,0,
           0,255,0,0,253,0,255,0,
           12,15,12,12,12,12,15,12,
           0,0,0,0,0,0,0,0,
           0,0,0,0,0,0,0,0,
           3,255,3,3,243,3,255,3,
           0,255,0,0,123,0,255,0,
           0,15,0,0,6,0,15,0]), pipe_2.x,pipe_2.y,pipe_2.key,pipe_2.mirrorX,pipe_2.mirrorY)
pipe_3 = Sprite(8,60,bytearray([0,255,0,0,230,0,255,0,
           0,255,0,0,253,0,255,0,
           12,15,12,12,12,12,15,12,
           0,0,0,0,0,0,0,0,
           0,0,0,0,0,0,0,0,
           3,255,3,3,243,3,255,3,
           0,255,0,0,123,0,255,0,
           0,15,0,0,6,0,15,0]), pipe_3.x,pipe_3.y,pipe_3.key,pipe_3.mirrorX,pipe_3.mirrorY)
Pipe_Mask = Sprite(8,60,bytearray([0,255,255,255,255,255,255,0,
           0,255,255,255,255,255,255,0,
           12,15,15,15,15,15,15,12,
           0,0,0,0,0,0,0,0,
           0,0,0,0,0,0,0,0,
           3,255,255,255,255,255,255,3,
           0,255,255,255,255,255,255,0,
           0,15,15,15,15,15,15,0]), Pipe_Mask.x,Pipe_Mask.y,Pipe_Mask.key,Pipe_Mask.mirrorX,Pipe_Mask.mirrorY)
Bird = Sprite(21//3,7,bytearray([12,18,17,21,18,12,12,6,9,17,21,62,48,0,28,34,38,18,15,3,0]), Bird.x,Bird.y,Bird.key,Bird.mirrorX,Bird.mirrorY)
Bird_Mask = Sprite(21//3,7,bytearray([12,30,31,31,30,12,12,6,15,31,31,62,48,0,28,62,62,30,15,3,0]), Bird_Mask.x,Bird_Mask.y,Bird_Mask.key,Bird_Mask.mirrorX,Bird_Mask.mirrorY)
bottom_pipe_mask = Sprite(75,45,bytearray([0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,
            0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,
            0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,128,128,128,128,128,128,128,128,128,128,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,
            0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,7,255,255,255,255,255,255,255,255,7,0,0,0,0,0,0,0,0,0,0,0,0,0,192,192,192,192,192,192,192,192,192,192,0,0,0,0,0,0,0,0,0,120,248,248,248,248,248,248,248,248,120,0,0,0,0,0,0,0,0,
            0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,255,255,255,255,255,255,255,255,0,0,0,0,0,0,0,0,0,0,0,0,0,0,3,255,255,255,255,255,255,255,255,3,0,0,0,0,0,0,0,0,0,0,255,255,255,255,255,255,255,255,0,0,0,0,0,0,0,0,0,
            0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,3,3,3,3,3,3,3,3,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,3,3,3,3,3,3,3,3,0,0,0,0,0,0,0,0,0,0,0,3,3,3,3,3,3,3,3,0,0,0,0,0,0,0,0,0]), bottom_pipe_mask.x,bottom_pipe_mask.y,bottom_pipe_mask.key,bottom_pipe_mask.mirrorX,bottom_pipe_mask.mirrorY)
top_pipes = Sprite(75,45,bytearray([0,0,0,252,0,0,204,0,252,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,252,0,0,220,0,252,0,
           0,0,0,255,0,0,125,0,255,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,96,127,96,96,103,96,127,96,
           0,0,6,7,6,6,6,6,7,6,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,
           0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,
           0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,
           0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]), top_pipes.x,top_pipes.y,top_pipes.key,top_pipes.mirrorX,top_pipes.mirrorY)
Bottom_pipes = Sprite(75,45,bytearray([0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,
           0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,
           0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,
           0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,3,255,3,3,243,3,255,3,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,128,128,128,128,128,128,128,128,0,0,0,0,0,0,0,0,0,0,0,48,240,48,48,48,48,240,48,0,0,0,0,0,0,0,0,0,
           0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,255,0,0,157,0,255,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,255,1,1,249,1,255,1,0,0,0,0,0,0,0,0,0,0,0,0,255,0,0,223,0,255,0,0,0,0,0,0,0,0,0,0,
           0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,3,0,0,3,0,3,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,3,0,0,2,0,3,0,0,0,0,0,0,0,0,0,0,0,0,0,3,0,0,1,0,3,0,0,0,0,0,0,0,0,0,0]), Bottom_pipes.x,Bottom_pipes.y,Bottom_pipes.key,Bottom_pipes.mirrorX,Bottom_pipes.mirrorY)
Title_background = Sprite(75,45,bytearray([0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,
           0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,
           0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,128,128,128,128,128,128,128,0,0,128,192,192,224,224,224,224,224,224,192,192,128,0,0,0,0,128,128,128,128,128,128,0,0,0,0,0,0,0,128,128,128,192,192,192,192,0,0,
           0,172,238,174,239,15,255,255,31,223,94,6,244,80,112,0,0,0,0,0,0,0,0,0,8,238,175,111,0,190,42,190,42,190,0,123,251,3,63,63,63,63,63,63,63,63,7,55,87,240,86,6,254,170,0,255,255,135,7,7,7,6,4,6,7,0,134,254,2,120,43,123,43,0,0,
           0,230,87,106,83,232,211,235,80,99,91,232,212,234,85,106,0,0,0,0,0,0,0,0,208,233,84,106,85,234,213,234,85,106,85,234,212,234,84,0,0,0,0,0,0,0,0,232,212,234,85,104,87,234,212,234,84,106,0,0,0,0,0,0,0,0,211,233,84,106,85,234,213,0,0,
           0,2,0,2,1,3,1,2,0,2,1,3,1,2,0,2,0,0,0,0,0,0,0,0,1,2,0,2,1,3,1,2,0,2,1,3,1,2,0,0,0,0,0,0,0,0,0,3,1,2,0,2,1,3,1,2,0,2,0,0,0,0,0,0,0,0,1,2,0,2,1,3,1,0,0]), Title_background.x,Title_background.y,Title_background.key,Title_background.mirrorX,Title_background.mirrorY)
Title_title = Sprite(55,16,bytearray([0,0,60,36,228,4,4,228,36,252,4,4,156,16,16,240,16,16,240,16,16,240,16,16,144,16,16,144,16,16,252,4,4,36,4,4,60,252,36,36,252,16,16,144,144,240,16,16,156,4,4,252,0,0,0,
            0,0,0,0,15,8,8,15,0,15,8,8,15,8,8,15,8,8,9,8,8,15,8,8,15,8,8,15,8,8,15,8,8,9,9,8,8,15,8,8,15,8,8,15,0,15,8,8,9,8,8,15,0,0,0]), Title_title.x,Title_title.y,Title_title.key,Title_title.mirrorX,Title_title.mirrorY)
ThumBirdText = Sprite(96,48,bytearray([0,0,0,0,0,0,0,127,81,127,0,0,15,9,15,9,15,0,127,65,107,65,127,0,127,81,65,69,127,0,127,69,119,81,127,0,127,65,81,71,124,0,0,15,9,15,0,0,62,99,65,93,119,0,119,93,65,99,62,0,127,85,99,85,127,0,28,54,34,54,28,0,0,240,144,240,0,0,28,20,20,20,28,0,0,112,80,112,0,0,120,76,119,25,15,0,
           127,65,73,65,127,0,119,93,65,95,112,0,127,69,85,81,127,0,119,93,85,65,127,0,31,17,119,65,127,0,127,81,85,69,127,0,127,65,85,69,127,0,7,5,125,65,127,0,127,65,85,65,127,0,31,17,117,65,127,0,0,124,84,124,0,0,0,252,148,252,0,0,28,54,107,93,119,0,62,42,42,42,62,0,119,93,107,54,28,0,7,125,85,113,31,0,
           127,65,93,81,127,0,127,65,117,65,127,0,127,65,81,71,124,0,127,65,93,85,119,0,127,65,73,99,62,0,127,65,85,93,119,0,127,65,117,29,7,0,127,65,93,69,127,0,127,65,119,65,127,0,119,93,65,93,119,0,120,72,95,65,127,0,127,65,99,73,127,0,127,65,95,80,112,0,127,65,115,65,127,0,127,65,99,65,127,0,127,65,93,65,127,0,
           127,65,117,17,31,0,127,65,77,65,127,0,127,65,113,71,124,0,127,81,85,69,127,0,7,125,65,125,7,0,127,65,95,65,127,0,63,97,79,97,63,0,127,65,103,65,127,0,127,73,99,73,127,0,31,113,71,113,31,0,127,77,65,89,127,0,0,127,65,93,119,0,15,25,119,76,120,0,119,93,65,127,0,14,11,13,11,14,0,0,224,160,160,160,224,0,
           0,15,9,15,0,0,126,74,74,66,126,0,127,65,87,68,124,0,124,68,84,84,124,0,124,68,87,65,127,0,126,66,82,82,126,0,28,119,65,117,31,0,252,164,164,132,252,0,127,65,119,68,124,0,0,127,69,127,0,0,224,160,191,133,255,0,127,65,111,84,124,0,0,127,65,127,0,0,124,68,100,68,124,0,124,68,116,68,124,0,124,68,84,68,124,0,
           252,132,228,36,60,0,60,36,228,132,252,0,124,68,116,20,28,0,112,92,68,116,28,0,28,118,66,86,124,0,124,68,92,68,124,0,60,100,92,100,60,0,124,68,76,68,124,0,124,84,108,84,124,0,252,164,172,132,252,0,28,116,68,92,112,0,28,119,65,93,119,0,0,255,129,255,0,0,119,93,65,119,28,0,7,13,9,11,14,0,0,0,0,0,0,0]), ThumBirdText.x,ThumBirdText.y,ThumBirdText.key,ThumBirdText.mirrorX,ThumBirdText.mirrorY)
__setFontFromBytes__(6, 8, ThumBirdText.bitmap)
display.textSpaceWidth = 0
display.setFPS(20)
top_pipes.x = -3
top_pipes.y = -2
Bottom_pipes.x = -3
Bottom_pipes.y = -2
Title_title.x = 10
Title_title.y = 0
Title_background.x = -3
Title_background.y = -2
Bird.x = 33
Bird.y = 13
if top_pipes.width == top_pipes.width and top_pipes.height == top_pipes.height:
    display.drawSpriteWithMask(top_pipes, top_pipes)
if Bottom_pipes.width == bottom_pipe_mask.width and Bottom_pipes.height == bottom_pipe_mask.height:
    display.drawSpriteWithMask(Bottom_pipes, bottom_pipe_mask)
if Title_title.width == Title_title.width and Title_title.height == Title_title.height:
    display.drawSpriteWithMask(Title_title, Title_title)
if Title_background.width == Title_background.width and Title_background.height == Title_background.height:
    display.drawSpriteWithMask(Title_background, Title_background)
if Bird.width == Bird_Mask.width and Bird.height == Bird_Mask.height:
    display.drawSpriteWithMask(Bird, Bird_Mask)
display.drawLine(0, 0, 72, 0, 1)
display.drawLine(0, 39, 72, 39, 1)
display.update()
display.fill(0)
time.sleep(3)
move_title_pipes_and_bird_down__move_background_out_the_bottom()
while True:
  if buttons.inputJustPressed():
    audio.playBlocking(1800, 150)
    audio.playBlocking(2500, 150)
    break
hoist_title()
time.sleep(1)
slide_pipes_and_bird()
time.sleep(2)
display.setFPS(10)
if not saveData.hasItem('high score'):
  saveData.setItem('high score', 0)
  saveData.save()
pipe_1.y = random.randint(-19, -1)
pipe_2.y = random.randint(-19, -1)
pipe_3.y = random.randint(-19, -1)
pipe_1.x = 70
pipe_2.x = 110
pipe_3.x = 150
Bird_y = Bird.y
Bird_acceleration = 0
while True:
  Bird_y = (Bird_y if isinstance(Bird_y, Number) else 0) + Bird_acceleration
  if acceleration_regulator == 4:
    Bird_acceleration = (Bird_acceleration if isinstance(Bird_acceleration, Number) else 0) + 1
    acceleration_regulator = 0
  acceleration_regulator = (acceleration_regulator if isinstance(acceleration_regulator, Number) else 0) + 1
  if Bird_acceleration > 0:
    Bird.setFrame(1)
    Bird_Mask.setFrame(1)
    bird_hight = 6
    bird_legth = 6
  elif Bird_acceleration < 0:
    Bird.setFrame(2)
    Bird_Mask.setFrame(2)
    bird_hight = 6
    bird_legth = 6
  else:
    Bird.setFrame(3)
    Bird_Mask.setFrame(3)
    bird_legth = 7
    bird_hight = 5
  pipe_1.x += -1
  pipe_2.x += -1
  pipe_3.x += -1
  Bird.y = Bird_y
  if pipe_1.width == Pipe_Mask.width and pipe_1.height == Pipe_Mask.height:
      display.drawSpriteWithMask(pipe_1, Pipe_Mask)
  if pipe_2.width == Pipe_Mask.width and pipe_2.height == Pipe_Mask.height:
      display.drawSpriteWithMask(pipe_2, Pipe_Mask)
  if pipe_3.width == Pipe_Mask.width and pipe_3.height == Pipe_Mask.height:
      display.drawSpriteWithMask(pipe_3, Pipe_Mask)
  display.drawLine(0, 0, 72, 0, 1)
  display.drawLine(0, 39, 72, 39, 1)
  if buttons.inputJustPressed():
    Bird_acceleration = -2
    Bird.y = Bird.y - 2
  if bool(display.getPixel(Bird.x - 1, Bird.y - 1)):
    audio.play(200, 1000)
    break
  elif bool(display.getPixel(Bird.x + bird_legth, Bird.y - 1)):
    audio.play(200, 1000)
    break
  elif bool(display.getPixel(Bird.x + bird_legth, Bird.y + bird_hight)):
    audio.play(200, 1000)
    break
  elif bool(display.getPixel(Bird.x - 1, Bird.y + bird_hight)):
    audio.play(200, 1000)
    break
  elif bool(display.getPixel(Bird.x + bird_legth, Bird.y + 2)):
    audio.play(200, 1000)
    break
  elif bool(display.getPixel(Bird.x + bird_legth, Bird.y + 3)):
    audio.play(200, 1000)
    break
  if Bird.y > 35:
    audio.play(200, 1000)
    break
  if pipe_1.x == -5:
    Score = (Score if isinstance(Score, Number) else 0) + 1
    audio.play(2000, 200)
    check_high_score()
  if pipe_2.x == -5:
    Score = (Score if isinstance(Score, Number) else 0) + 1
    audio.play(2000, 200)
    check_high_score()
  if pipe_3.x == -5:
    Score = (Score if isinstance(Score, Number) else 0) + 1
    audio.play(2000, 200)
    check_high_score()
  if pipe_1.x < -8:
    pipe_1.x = pipe_3.x + 40
    pipe_1.y = random.randint(-19, -1)
  if pipe_2.x < -8:
    pipe_2.x = pipe_1.x + 40
    pipe_2.y = random.randint(-19, -1)
  if pipe_3.x < -8:
    pipe_3.x = pipe_2.x + 40
    pipe_3.y = random.randint(-19, -1)
  if Bird.width == Bird_Mask.width and Bird.height == Bird_Mask.height:
      display.drawSpriteWithMask(Bird, Bird_Mask)
  display.update()
  display.fill(0)
display.fill(0)
display.drawText(str('Game Over!'), 6, 0, 1)
display.drawText(str('score:' + str(Score)), 0, 8, 1)
display.drawText(str('High:' + str(saveData.getItem('high score'))), 0, 16, 1)
display.update()
display.fill(0)
time.sleep(1.5)
while True:
  if buttons.inputJustPressed():
    break