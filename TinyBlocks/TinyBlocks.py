#attribution
#level based speed?
import thumby
import time
import uos
import random
import machine

machine.freq(125000000)

tetrisSplash=[
0x55, 0xaa, 0x55, 0xaa, 0x55, 0xaa, 0x55, 0xaa, 0x55, 0xaa, 0x55, 0xaa, 0x55, 0xaa, 0xf5, 0xfa, 0xfd, 0xfe, 0xff, 0xfe, 0xff, 0xfe, 0xff, 0xfe, 0xff, 0xfe, 0xff, 0xfe, 0xff, 0xfe, 0xf7, 0x86, 0xf7, 0xfe, 0x87, 0xfe, 0x87, 0xef, 0xde, 0x87, 0xfe, 0xe7, 0x9e, 0xe7, 0xfe, 0xff, 0xfe, 0xff, 0xfe, 0xff, 0xfe, 0xff, 0xfe, 0xff, 0xfe, 0xfd, 0xfa, 0xf5, 0xaa, 0x55, 0xaa, 0x55, 0xaa, 0x55, 0xaa, 0x55, 0xaa, 0x55, 0xaa, 0x55, 0xaa, 0x55, 
0x55, 0xaa, 0x55, 0xaa, 0x55, 0xaa, 0x55, 0xaa, 0x55, 0xaa, 0x55, 0xaa, 0xfd, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0xfb, 0xfb, 0xfb, 0x3, 0xfb, 0xfb, 0xfb, 0xff, 0x3, 0xfb, 0xfb, 0xfb, 0xfb, 0xf7, 0xf, 0xff, 0xfb, 0xfb, 0x3, 0xfb, 0xfb, 0xff, 0xf, 0xf7, 0xfb, 0xfb, 0xfb, 0xfb, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0xfd, 0xaa, 0x55, 0xaa, 0x55, 0xaa, 0x55, 0xaa, 0x55, 0xaa, 0x55, 0xaa, 0x55, 
0x55, 0xaa, 0x55, 0xaa, 0x55, 0xaa, 0x55, 0xaa, 0x55, 0xaa, 0x55, 0xaa, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0x0, 0xff, 0xff, 0xff, 0xff, 0x0, 0xf9, 0xe5, 0xdd, 0xbd, 0x7e, 0xff, 0xff, 0xff, 0xff, 0x0, 0xff, 0xff, 0xff, 0xff, 0xfe, 0xfd, 0xfd, 0xfd, 0xfb, 0x7, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0xaa, 0x55, 0xaa, 0x55, 0xaa, 0x55, 0xaa, 0x55, 0xaa, 0x55, 0xaa, 0x55, 
0x55, 0xaa, 0x55, 0xaa, 0x55, 0xaa, 0x55, 0xaa, 0x55, 0xaa, 0x55, 0xaa, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0xfc, 0xff, 0xff, 0xff, 0xff, 0xfc, 0xff, 0xff, 0xff, 0xff, 0xfe, 0xfd, 0xff, 0xfd, 0xfd, 0xfc, 0xfd, 0xfd, 0xff, 0xff, 0xfd, 0xfd, 0xfd, 0xfd, 0xfe, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0xaa, 0x55, 0xaa, 0x55, 0xaa, 0x55, 0xaa, 0x55, 0xaa, 0x55, 0xaa, 0x55, 
0x55, 0xaa, 0x55, 0xaa, 0x55, 0xaa, 0x55, 0xaa, 0x55, 0xaa, 0x55, 0xaa, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0xaa, 0x55, 0xaa, 0x55, 0xaa, 0x55, 0xaa, 0x55, 0xaa, 0x55, 0xaa, 0x55, 
]
for i in range(len(tetrisSplash)):
    tetrisSplash[i]=tetrisSplash[i]^0xff

B_COLS =14
B_ROWS =22
B_SIZE =(B_ROWS * B_COLS)

KEY_LEFT   =0
KEY_RIGHT  =1
KEY_ROT_R  =2
KEY_ROT_L  =3
KEY_DROP   =4
KEY_PAUSE  =5
KEY_QUIT   =6

keys = 'LR21DUS'

def getcharinputNew():
    if(thumby.buttonL.justPressed()):
        return 'L'
    if(thumby.buttonR.justPressed()):
        return 'R'
    if(thumby.buttonU.justPressed()):
        return 'U'
    if(thumby.buttonD.justPressed()):
        return 'D'
    if(thumby.buttonA.justPressed()):
        return '1'
    if(thumby.buttonB.justPressed()):
        return '2'
    return ' '

TL=     -B_COLS-1       #/* top left */
TC=     -B_COLS         #/* top center */
TR=     -B_COLS+1       #/* top right */
ML=     -1              #/* middle left */
MR=     1               #/* middle right */
BL=     B_COLS-1        #/* bottom left */
BC=     B_COLS          #/* bottom center */
BR=     B_COLS+1        #/* bottom right */

level = 1
points = 0
lines_cleared = 0
board = [] #[[[] for k in range(B_SIZE)]]
for i in range(B_SIZE):
  board.append(0)

shapes = [
  7,  TL,  TC,  MR,
  8,  TR,  TC,  ML,
  9,  ML,  MR,  BC,
  3,  TL,  TC,  ML,
  12,  ML,  BL,  MR,
  15,  ML,  BR,  MR,
  18,  ML,  MR,   2,           # sticks out
  0,  TC,  ML,  BL,
  1,  TC,  MR,  BR,
  10,  TC,  MR,  BC,
  11,  TC,  ML,  MR,
  2,  TC,  ML,  BC,
  13,  TC,  BC,  BR,
  14,  TR,  ML,  MR,
  4,  TL,  TC,  BC,
  16,  TR,  TC,  BC,
  17,  TL,  MR,  ML,
  5,  TC,  BC,  BL,
  6,  TC,  BC,  2 * B_COLS,   # sticks out 
]

shapePos = random.randint(1, 10000000) % 7 * 4
peek_shape = [shapes[shapePos],shapes[shapePos+1],shapes[shapePos+2],shapes[shapePos+3]]
shape = [0,0,0,0]

def drawCheckerboard():
  thumby.display.fill(0)
  for x in range(72/2):
    for y in range(5):
      thumby.display.drawSprite([0x55,0xAA], x*2, y*8, 2, 8,0,0,0)

def clearScreen():
  thumby.display.fillRect(34,2,36,12 ,0)
  thumby.display.fillRect(39-5,18,14,12,0)
  thumby.display.fillRect(52,18,18,12,0)
  
  thumby.display.rect(34-1,2-1,36+2,12+2,1)
  thumby.display.rect(39-1-5,18-1,14+2,12+2,1)
  thumby.display.rect(52-1,18-1,18+2,12+2,1)

def setBlock(xb, yb, val):
  thumby.display.fillRect(xb*2, yb*2, 2, 2, val)

def updateScreen():
  #print("update")
  
  clearScreen()
  
  global level
  #preview[B_COLS * 10];
  preview = []
  for i in range(B_COLS * 10):
    preview.append(0)
  # thumby.display piece preview
  #memset (preview, 0, sizeof(preview));
  preview[2 * B_COLS + 1] = 7
  preview[2 * B_COLS + 1 + peek_shape[1]] = 7
  preview[2 * B_COLS + 1 + peek_shape[2]] = 7
  preview[2 * B_COLS + 1 + peek_shape[3]] = 7

  for y in range(4):
    for x in range(4):
      setBlock(x + 22-3, y + 10, preview[y * B_COLS + x])

  # thumby.display board.
  for y in range(1, B_ROWS-1):
    for x in range(B_COLS):
      setBlock(x + 2, y-1, board[y * B_COLS + x])

  # Update points and level*/
  #while (lines_cleared >= 10):
    #lines_cleared -= 10
    #level+=1
  
  thumby.display.drawText('%04d' % (points//10), 36, 5)
  thumby.display.drawText('%02d' % lines_cleared, 36+18-1, 21)
  # level
  thumby.display.update()

def fits_in(shape, pos):
  try:
    if (board[pos] or board[pos + shape[1]] or board[pos + shape[2]]  or board[pos + shape[3]]):
      return 0
  except:
    print("fits_in exception")
    return 0
  return 1

def place(shape, pos, b):
  try:
    board[pos] = b
    board[pos + shape[1]] = b
    board[pos + shape[2]] = b
    board[pos + shape[3]] = b
  except:
    print("place exception")

def next_shape():
  print("next")
  global peek_shape
  next = peek_shape
  shapePos = random.randint(1, 10000000) % 7 * 4
  peek_shape = [shapes[shapePos],shapes[shapePos+1],shapes[shapePos+2],shapes[shapePos+3]]
  if (next==0):
    return next_shape()
  return next;

def show_high_score():
    
  for y in range(40):
    thumby.display.fillRect(8,40-y,20,1,1)
    time.sleep_ms(15)
    thumby.display.update()
    thumby.audio.play(100+(40-y)*20, 50)
  
  for i in range(41):
    thumby.display.fillRect(8,0,20,i,0)
    thumby.display.drawText("G", 9, -2+5+0)
    thumby.display.drawText("A", 9, -2+5+8)
    thumby.display.drawText("M", 9, -2+5+16)
    thumby.display.drawText("E", 9, -2+5+24)
    thumby.display.drawText("O", 19, 2+5+0)
    thumby.display.drawText("V", 19, 2+5+8)
    thumby.display.drawText("E", 19, 2+5+16)
    thumby.display.drawText("R", 19, 2+5+24)
    time.sleep_ms(10)
    thumby.display.update()
  
  lastUpdate=time.ticks_ms()
  while(getcharinputNew()==' '):
    color = 1
    if (((time.ticks_ms()-lastUpdate)//500) & 1):
      color = 0
    thumby.display.drawText("G", 9, -2+5+0, color)
    thumby.display.drawText("A", 9, -2+5+8, color)
    thumby.display.drawText("M", 9, -2+5+16, color)
    thumby.display.drawText("E", 9, -2+5+24, color)
    thumby.display.drawText("O", 19, 2+5+0, color)
    thumby.display.drawText("V", 19, 2+5+8, color)
    thumby.display.drawText("E", 19, 2+5+16, color)
    thumby.display.drawText("R", 19, 2+5+24, color)
    if(i<=42):
      thumby.display.fillRect(8,i,20,42-i,0)
      i+=1
    time.sleep_ms(10)
    thumby.display.update()

fastDropDelay=50
dropDelay=500
leftRightUpdateDelay=100

while(True):
  print("start")
  level = 1;
  points = 0;
  lines_cleared = 0
  c = ' '
  pos = 17+3
  backup = []
  movingLeftOrRight = 0
  
  thumby.display.fill(0)
  thumby.display.drawSprite(tetrisSplash, 0,0, 72, 40,0,0,0)
  #thumby.display.update()
  #while(1):
  #    a=1
  #thumby.display.fillRect(10,24,72-20,16,0)
  isdisplayed=0;
  thumby.display.update()
  
  while(getcharinputNew()==' '):
    if((time.ticks_ms()//1000)&1):
      if isdisplayed == 0 :
        thumby.display.drawText("START", 16, 30,1)
        thumby.display.update()
        isdisplayed = 1
    else:
      if isdisplayed == 1 :
        #thumby.display.fillRect(10,24,72-20,16,0)
        thumby.display.drawText("START", 16, 30,0)
        thumby.display.update()
        isdisplayed = 0


  # Initialize board
  for i in range(B_SIZE-1):
    if (i < B_COLS*1 or (i % B_COLS) <= 1 or (i % B_COLS) >= (B_COLS-2)):
      board[(B_SIZE-1)-i] = 7
    else:
      board[(B_SIZE-1)-i] = 0

  drawCheckerboard()
  clearScreen()

  shape = next_shape()
  print("startloop")
  lastUpdate=time.ticks_ms()
  lastDrop=time.ticks_ms()
  while (1):
    c=getcharinputNew()
    if(c==' '):
        if(time.ticks_ms()-lastUpdate > 50):
            if(thumby.buttonD.pressed()):
                lastUpdate=time.ticks_ms()
                c = 'D'
                points+=1
        if(time.ticks_ms()-lastDrop > 500):
            lastDrop=time.ticks_ms()
            #lastUpdate=time.ticks_ms()
            c = 'D'
        if(c != 'D' and time.ticks_ms()-lastUpdate > (100)):
            lastUpdate=time.ticks_ms()
            if(thumby.buttonL.pressed()):
                c = 'L'
            elif(thumby.buttonR.pressed()):
                c = 'R'
    else:
        lastUpdate=time.ticks_ms()
    
    #continue
    if (c == keys[KEY_DROP]):
      #print(B_COLS,pos, pos//B_COLS)
      if (fits_in (shape, pos + B_COLS)):
        pos += B_COLS
        c=' '
        thumby.audio.play(300, 10, 5000)
      else:
        place (shape, pos, 7)
        #points+=1;
        j=0
        currentLines=lines_cleared
        while(j < (B_COLS*(B_ROWS-1))):
          while (board[j]):
            if (j % B_COLS == 11):
              lines_cleared+=1
              while (j % B_COLS>1):
                board[j] = 0
                j-=1
              updateScreen()
              thumby.audio.play(1000, 50)
              while(j):
                board[j + B_COLS] = board[j]
                j-=1
              updateScreen()
              thumby.audio.play(100, 100)
            j+=1
          j = B_COLS * (j // B_COLS + 1)
        if(lines_cleared-currentLines==1):
          points+=(((lines_cleared//5)+1)*40)
        if(lines_cleared-currentLines==2):
          points+=(((lines_cleared//5)+1)*100)
        if(lines_cleared-currentLines==3):
          points+=(((lines_cleared//5)+1)*300)
        if(lines_cleared-currentLines==4):
          points+=(((lines_cleared//5)+1)*1200)
        if(lines_cleared-currentLines==0):
          thumby.audio.play(100, 50)
        shape = next_shape()
        pos=17+3
        if (fits_in (shape, pos)==0):
          c = keys[KEY_QUIT]
    if (c == keys[KEY_LEFT]):
      pos-=1
      if (fits_in (shape, pos)==0):
        pos+=1
    if (c == keys[KEY_ROT_L]):
      backup = shape
      shape = shapes[4*shape[0]:4*shape[0]+4]
      # Check if it fits, if not restore shape from backup 
      if (fits_in (shape, pos)==0):
        shape = backup
    if (c == keys[KEY_ROT_R]):
      backup = shape
      shape = shapes[4*shape[0]:4*shape[0]+4]
      shape = shapes[4*shape[0]:4*shape[0]+4]
      shape = shapes[4*shape[0]:4*shape[0]+4]
      # Check if it fits, if not restore shape from backup
      if (fits_in (shape, pos)==0):
        shape = backup
    if (c == keys[KEY_RIGHT]):
      pos+=1
      if (fits_in (shape, pos)==0):
        pos-=1
    if (c == keys[KEY_DROP]):
      a=1
    if (c == keys[KEY_QUIT]):
      show_high_score ()
      break;

    place (shape, pos, 7);
    updateScreen ();
    place (shape, pos, 0);
    
  a=0