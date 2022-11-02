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
start_screen = bytearray([255,255,255,255,255,31,255,255,255,255,255,127,159,127,255,255,255,31,159,127,255,255,31,255,255,127,191,223,223,223,191,255,255,63,223,223,191,255,223,223,31,223,223,255,255,127,191,223,223,223,191,127,255,255,31,159,127,255,255,31,255,255,143,255,255,63,223,223,191,255,255,255,
           255,255,255,255,255,224,239,239,239,231,249,250,251,250,249,231,255,224,255,254,249,231,224,255,255,248,247,239,237,237,241,255,255,247,238,237,243,255,255,255,224,255,255,255,255,248,247,239,239,239,247,248,255,255,224,255,254,249,231,224,255,255,255,255,255,247,238,237,243,255,255,255,
           255,255,255,255,255,255,255,127,255,255,255,255,127,127,255,255,255,127,255,127,127,127,127,127,255,255,255,255,255,255,39,151,119,207,223,63,255,255,255,255,255,255,255,255,255,255,255,255,255,131,235,227,255,131,235,211,255,131,171,255,179,171,155,255,179,171,155,255,255,255,255,255,
           255,255,255,255,159,231,233,238,233,231,159,255,128,254,249,231,159,128,255,255,255,128,255,255,255,255,255,255,255,255,252,253,251,51,207,62,254,30,252,62,126,126,125,131,255,255,255,255,207,175,111,255,239,239,15,239,15,79,63,255,255,15,175,79,239,239,15,239,239,255,255,255,
           255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,254,253,254,254,253,254,254,253,252,255,255,255,255,255,255,255,254,254,254,255,255,255,254,254,255,255,254,255,255,254,255,255,255,255,254,255,255,255,255,255])
cover_screen = thumby.Sprite(72, 40, start_screen, 0, 0, -1) # combining bitmaps as animation frames


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

    if thumby.buttonB.justPressed(): # toggles the simulate flag
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