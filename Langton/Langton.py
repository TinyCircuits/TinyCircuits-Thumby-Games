import thumby 
import random
from framebuf import FrameBuffer, MONO_HMSB, MONO_VLSB, MONO_HLSB
import time

# langton's ant for thumby
# based on game of life for thumby

simulate = False

buf = bytearray()
cells = []
blinks = 0
antd = 0

wb = 72//8 # 9 -> pixel width in bytes
hb = 360//wb # 40 -> pixel width in bytes

wc = 72//2 # 36 -> width in cells
hc = 40//2 # 20 -> height in cells
antx = wc//2
anty = hc//2


 # BITMAP: width: 72, height: 40
titlebmp = bytearray([188,190,128,128,128,128,128,192,0,248,252,6,2,34,32,254,254,0,254,254,0,2,2,2,254,252,0,248,252,134,130,162,34,226,226,0,4,6,6,254,246,6,6,2,0,252,254,130,130,130,128,254,252,0,254,254,0,2,2,2,254,252,0,6,152,156,150,146,146,130,242,242,
           241,249,13,5,69,65,253,253,0,253,253,0,4,4,4,253,249,0,9,13,12,252,236,12,13,5,0,48,73,157,21,97,160,33,40,36,180,152,48,1,117,52,52,4,116,52,85,5,117,117,85,5,68,116,21,5,68,116,20,4,5,5,100,52,117,5,149,213,149,21,85,84,
           3,3,96,48,104,72,83,67,208,131,139,16,112,248,248,211,99,64,160,32,64,3,131,128,128,0,152,48,90,75,40,8,11,13,0,144,67,16,8,0,66,18,196,232,240,228,212,184,64,96,160,224,192,160,224,64,224,240,240,241,226,231,200,220,35,113,141,196,54,19,218,76,
           0,0,0,128,65,29,194,201,62,78,233,169,237,108,201,67,1,48,242,115,219,252,4,254,204,13,114,156,199,192,229,144,0,132,66,64,128,32,8,3,0,0,6,159,15,31,14,3,192,23,14,2,39,142,57,70,11,10,86,149,45,11,91,17,147,28,0,1,2,7,8,28,
           0,48,248,117,126,57,220,9,96,240,3,235,121,209,224,128,0,192,96,209,243,186,248,193,128,114,103,19,79,53,3,1,20,16,56,56,16,15,0,0,16,8,2,128,0,64,24,2,0,0,0,0,20,32,0,0,53,64,128,0,2,4,16,0,32,2,8,32,0,64,0,0])
cover_screen = thumby.Sprite(72, 40, titlebmp, 0, 0, -1)


def BuildBuffer(): # converts game screen (cells) into a screen buffer
    global buf
    buf = bytearray() # will store our pixel data
    gi=0 # index into cells array
    for row in range(hb):
        if row%2 == 0:
            for col in range(wb):
                nb = 0b0
                for i in range(4):
                    nb |= (0b11*cells[gi]) << (i*2)
                    gi+=1
                buf.append(nb)
        else:
            buf.extend(buf[-wb:])


def InitCells(): # initializes the cells array
    global cells
    cells = []
    for row in range(hc):
        for col in range(wc):
            cells.append(0)

def handleInput(): # called every frame
    global cursor
    global simulate
    global cells

    if thumby.actionPressed(): # toggles the simulate flag
        Beep()
        if simulate:
            simulate = False
        else:
            simulate = True


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
        
def Simulate(): # simulates the ant
    global antx
    global anty
    global antd
    global cells
    global blinks
    
    gi = anty*wc + antx # get index into cells array
    
    if cells[gi] == 0: # change direction and color
        antd = (antd+1)%4
        cells[gi] = 1
    else:
        antd = (antd-1)%4
        cells[gi] = 0

    if antd == 0: # move ant
        anty -= 1
    elif antd == 1:
        antx += 1
    elif antd == 2:
        anty += 1
    elif antd == 3:
        antx -= 1
        
    if antx < 0: # wrap ant
        antx = wc-1
    elif antx >= wc:
        antx = 0
    if anty < 0:
        anty = hc-1
    elif anty >= hc:
        anty = 0
            
    # set frame buffer
    BuildBuffer()
    

fbuffer = FrameBuffer(thumby.display.display.buffer, 72, 40, MONO_VLSB) # create thumby buffer

old_ticks=0 # timer count on last frame
blink_interval=600 # ~ms per blink
next_blink = blink_interval # time until next blink in ms
blinks = 0 # used for animating sprite
thumby.display.setFPS(0) # who needs 60fps?!
InitCells()


while 1: # start screen loop
    thumby.display.fill(0)
    cover_screen.setFrame(blinks) # animate the controls screen
    thumby.display.drawSprite(cover_screen)
    thumby.display.update()
    handleInput()

    if simulate:
        break

while 1: # simulation screen loop
    Timing()
    
    thumby.display.fill(0)
    fbuffer.blit(FrameBuffer(buf, 72, 40, MONO_HMSB), 0, 0, 72,40) # drawing game board

    handleInput()
    
    if simulate:
        Simulate()
    
    thumby.display.update() # flush the screenbuffer