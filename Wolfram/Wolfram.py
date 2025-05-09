import thumby 
import random
from framebuf import FrameBuffer, MONO_HMSB, MONO_VLSB, MONO_HLSB
import time

# simulate 1D cellular automata by Stephen Wolfram
# http://mathworld.wolfram.com/ElementaryCellularAutomaton.html

simulate = False
at_start_screen = True
buf = bytearray()
cells = []
blinks = 0
rule = 30
fbuffer = FrameBuffer(thumby.display.display.buffer, 72, 40, MONO_VLSB) # create thumby buffer
old_ticks=0 # timer count on last frame
blink_interval=600 # ~ms per blink
next_blink = blink_interval # time until next blink in ms

wb = 72//8 # 9 -> pixel width in bytes
hb = 360//wb # 40 -> pixel width in bytes

wc = 72//2 # 36 -> width in cells
hc = 40//2 # 20 -> height in cells

cursor = bytearray([1, 1, 1, 1])
cursor_sprite = thumby.Sprite(2, 2, cursor) # create a cursor sprite
cursor_sprite.x = 0
cursor_sprite.y = 0

# BITMAP: width: 72, height: 40
titlebmp = bytearray([0,0,0,32,176,184,108,216,240,0,56,240,224,200,226,232,226,200,224,240,56,0,240,216,108,184,176,32,0,0,0,8,4,252,0,192,4,248,0,224,16,16,224,4,248,0,128,0,224,144,48,0,224,16,48,0,144,208,224,0,16,224,16,96,16,224,4,32,80,80,128,0,
           1,6,12,24,48,179,175,158,64,227,197,143,30,124,239,207,239,124,30,143,69,227,192,158,47,179,48,24,12,6,225,16,16,16,57,0,193,160,224,8,241,1,0,8,240,1,1,0,239,0,224,8,241,0,0,0,33,161,192,1,0,193,32,96,0,7,0,2,1,1,0,0,
           0,0,0,0,0,0,1,3,7,14,29,59,119,238,220,186,118,238,93,59,23,14,5,3,1,0,0,128,64,32,241,2,194,2,193,16,225,66,66,0,129,66,67,128,65,130,67,128,65,130,3,64,65,130,3,16,227,67,65,2,64,67,128,0,0,0,0,0,0,0,0,0,
           0,0,0,0,0,0,0,0,0,128,64,32,80,136,21,3,21,136,80,32,64,128,0,0,4,2,1,0,2,2,31,0,3,4,7,0,3,4,6,0,3,4,4,3,0,7,0,1,0,31,0,6,7,3,4,0,3,4,6,0,6,7,3,4,0,0,0,0,0,0,0,0,
           40,136,72,32,80,136,20,2,21,136,81,32,65,128,1,0,1,128,65,32,81,136,21,2,20,136,80,32,72,136,40,104,232,200,168,64,220,204,172,64,220,204,148,64,220,220,148,64,208,220,132,64,208,220,132,96,232,200,168,64,216,204,156,64,232,200,168,104,232,200,168,104])
cover_screen = thumby.Sprite(72, 40, titlebmp, 0, 0, -1)


# contains all rows
def BuildBuffer():
    global buf
    buf = bytearray(wb*hb)
    for i in range(0, wb*hb):
        buf[i] = 0

# contains all cells
def BuildCells():
    global cells
    cells = []
    for i in range(0, wc*hc + 2):
        cells.append(0)

# set cell to 1
def SetCell(x, y):
    global cells
    cells[y*wc+x] = 1

# set cell to 0
def ClearCell(x, y):
    global cells
    cells[y*wc+x] = 0

# set all cells to 0
def WipeCells():
    global cells
    for i in range(0, wc*hc):
        cells[i] = 0

# get cell state
def GetCell(x, y):
    global cells
    return cells[y*wc+x]

def CheckRule(x, y, i):
    global rule
    if (rule & (1 << i)) > 0:
        SetCell(x, y)
    else:
        ClearCell(x, y)

def SetPixel(x, y):
    global buf
    buf[y*wb+x//8] |= 1 << (x%8)

def ClearPixel(x, y):
    global buf
    buf[y*wb+x//8] &= ~(1 << (x%8))

def InitFirstRow():
    SetCell(wc//2, 0)

def Beep(): # audio feedback for inputs!
    thumby.audio.play(1000, 50)

def Timing(): # does some common timing and animation handling
    global old_ticks
    global blink_interval
    global next_blink
    global blinks
    
    new_ticks = time.ticks_ms() # calculating delta ticks
    dt = new_ticks - old_ticks
    old_ticks = new_ticks
    
    next_blink -= dt # handle blinking the cursor sprite
    if next_blink <= 0:
        next_blink = blink_interval
        blinks += 1

def FlashCurrentRule(): # flashes the current rule on the screen
    global rule

    thumby.display.fill(0)
    thumby.display.drawText(str(rule), 0, 0, 1)
    thumby.display.update() # flush the screenbuffer
    

def Simulate():
    # simulate 1D cellular automata by Stephen Wolfram
    # http://mathworld.wolfram.com/ElementaryCellularAutomaton.html
    global cells
    global buf
    global simulate
    global blinks

    if simulate:
        # build next generation
        for y in range(1, hc):
            for x in range(1, wc-1):
                l = GetCell(x-1, y-1)
                c = GetCell(x, y-1)
                r = GetCell(x+1, y-1)
                i = l*4 + c*2 + r
                CheckRule(x, y, i)

        # draw next generation
        for y in range(0, hc):
            for x in range(0, wc):
                if GetCell(x, y) == 1:
                    SetPixel(x*2, y*2)
                    SetPixel(x*2+1, y*2)
                    SetPixel(x*2, y*2+1)
                    SetPixel(x*2+1, y*2+1)
                else:
                    ClearPixel(x*2, y*2)
                    ClearPixel(x*2+1, y*2)
                    ClearPixel(x*2, y*2+1)
                    ClearPixel(x*2+1, y*2+1)

        # shift cells up
        for y in range(1, hc):
            for x in range(0, wc):
                cells[y*wc+x] = GetCell(x, y-1)

        # draw first row
        for x in range(0, wc):
            if GetCell(x, 0) == 1:
                SetPixel(x*2, 0)
                SetPixel(x*2+1, 0)
            else:
                ClearPixel(x*2, 0)
                ClearPixel(x*2+1, 0)


        simulate = False
    
    thumby.display.fill(0)
    fbuffer.blit(FrameBuffer(buf, 72, 40, MONO_HMSB), 0, 0, 72,40) # drawing game board
    thumby.display.update() # flush the screenbuffer
    Draw()

def Draw():
    global buf
    global blinks
    global cursor_sprite

    # draw the buffer
    thumby.display.drawSprite(cursor_sprite)
    thumby.display.update()
    Timing()

def HandleInput():
    global simulate
    global rule
    global at_start_screen
    if thumby.buttonA.justPressed():
        Beep()
        if at_start_screen:
            at_start_screen = not at_start_screen
        elif not at_start_screen:
            SetCell(cursor_sprite.x//2, cursor_sprite.y//2)
            simulate = True
    if thumby.buttonB.justPressed():
        Beep()
        if at_start_screen:
            at_start_screen = not at_start_screen
        elif not at_start_screen:
            WipeCells()
            simulate = True
    if thumby.buttonU.justPressed():
        Beep()
        rule += 1
        if rule > 255:
            rule = 0
        FlashCurrentRule()
        BuildBuffer()
        BuildCells()
        InitFirstRow()
        simulate = True
    if thumby.buttonD.justPressed():
        Beep()
        rule -= 1
        if rule < 0:
            rule = 255
        FlashCurrentRule()
        BuildBuffer()
        BuildCells()
        InitFirstRow()
        simulate = True
    if thumby.buttonL.justPressed():
        Beep()
        if cursor_sprite.x > 0:
            cursor_sprite.x -= 2
    if thumby.buttonR.justPressed():
        Beep()
        if cursor_sprite.x < 71:
            cursor_sprite.x += 2
        
BuildBuffer()
BuildCells()
InitFirstRow()


while 1:
    thumby.display.fill(0)
    cover_screen.setFrame(blinks)
    thumby.display.drawSprite(cover_screen)
    thumby.display.update()
    HandleInput()

    if not at_start_screen:
        break

    thumby.display.update()


simulate = True
at_start_screen = False

while 1:
    Simulate()
    HandleInput()