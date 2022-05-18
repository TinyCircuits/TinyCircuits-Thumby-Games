import thumby
from framebuf import FrameBuffer, MONO_HMSB, MONO_VLSB, MONO_HLSB
import random
import time

# Thomas Duffin, May 2022
# Conway's Game of Life, written in MicroPython for the Thumby console. 
# Free to modify and share, though credit is always appreciated!
# Github: tduffinntu@github.com

cursor = thumby.Sprite(2, 2, bytearray([3,3,0,0]), 72//2, 40//2, -1) # blinking square

# BITMAP: width: 72, height: 40
cover1 = bytearray([0,0,0,0,0,0,0,0,0,248,248,248,248,248,0,0,0,0,0,0,0,0,112,136,136,80,0,0,112,136,136,112,0,0,248,16,32,64,248,0,0,120,128,112,128,120,0,0,240,40,40,248,0,0,8,16,224,16,8,0,0,24,0,0,144,168,168,72,0,0,0,0,
           0,0,0,128,128,128,128,128,0,128,128,128,128,128,0,190,190,190,190,190,0,0,28,162,170,26,0,0,188,138,138,62,0,0,62,4,136,132,62,0,0,190,170,42,128,128,128,128,0,128,128,128,128,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,
           0,0,0,15,15,15,15,15,0,15,15,15,15,15,0,15,15,15,15,15,0,0,7,8,8,7,0,0,15,2,2,0,0,0,0,0,15,15,12,12,0,15,15,0,15,15,2,2,0,15,15,10,10,0,12,12,0,0,0,0,0,0,128,192,64,64,64,192,128,0,0,0,
           0,0,0,60,20,8,0,24,36,24,0,0,60,20,40,0,4,60,4,0,60,52,0,60,36,24,0,0,0,0,0,60,40,16,0,4,56,8,4,0,0,0,0,0,0,0,0,0,0,0,0,0,0,224,48,16,16,16,48,224,0,0,63,72,80,80,80,72,63,0,0,0,
           0,0,0,2,30,2,0,30,18,12,0,14,16,30,0,30,10,2,0,30,10,2,0,28,0,30,4,8,30,0,0,0,0,6,0,26,26,22,0,26,26,22,0,0,0,0,0,0,0,0,0,0,0,15,18,20,20,20,18,15,0,0,0,0,0,0,0,0,0,0,0,0])

# BITMAP: width: 72, height: 40
cover2 = bytearray([0,0,0,0,0,0,0,0,0,248,248,248,248,248,0,0,0,0,0,0,0,0,112,136,136,80,0,0,112,136,136,112,0,0,248,16,32,64,248,0,0,120,128,112,128,120,0,0,240,40,40,248,0,0,8,16,224,16,8,0,0,24,0,0,144,168,168,72,0,0,0,0,
           0,0,0,128,128,128,128,128,0,128,128,128,128,128,0,190,190,190,190,190,0,0,28,162,170,26,0,0,188,138,138,62,0,0,62,4,136,132,62,0,0,190,170,42,128,128,128,128,0,128,128,128,128,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,
           0,0,0,15,15,15,15,15,0,15,15,15,15,15,0,15,15,15,15,15,0,0,7,8,8,7,0,0,15,2,2,0,0,0,0,0,15,15,12,12,0,15,15,0,15,15,2,2,0,15,15,10,10,0,12,12,0,0,0,0,0,0,0,16,48,126,48,16,0,0,0,0,
           0,0,0,60,20,8,0,24,36,24,0,0,60,20,40,0,4,60,4,0,60,52,0,60,36,24,0,0,0,0,0,60,40,16,0,4,56,8,4,0,0,0,0,0,0,0,0,0,0,0,0,0,0,224,48,16,16,16,48,224,0,0,62,83,97,97,97,83,62,0,0,0,
           0,0,0,2,30,2,0,30,18,12,0,14,16,30,0,30,10,2,0,30,10,2,0,28,0,30,4,8,30,0,0,0,0,6,0,26,26,22,0,26,26,22,0,0,0,0,0,0,0,0,0,0,0,15,18,20,20,20,18,15,0,0,0,0,0,0,0,0,0,0,0,0])

# BITMAP: width: 72, height: 40
controls = bytearray([0,0,0,0,0,4,60,4,0,24,36,36,24,0,60,36,52,0,60,36,52,0,60,32,32,0,60,44,44,0,0,0,24,36,36,0,60,44,44,0,60,32,32,60,32,32,0,0,32,32,32,32,32,32,32,32,32,32,32,32,32,32,32,32,32,224,0,0,0,0,0,0,
           0,0,0,0,198,137,128,207,4,143,64,134,9,198,0,15,200,8,192,207,201,6,0,9,6,0,0,0,0,15,5,2,0,14,5,14,0,7,8,8,7,0,10,13,13,0,15,11,11,0,0,8,8,8,8,8,248,0,0,0,0,0,0,0,0,255,0,0,0,0,0,0,
           0,0,0,0,3,1,0,3,0,1,2,1,0,0,3,3,0,0,3,2,2,0,0,2,2,2,2,2,2,2,2,130,66,66,78,64,64,126,3,1,1,1,1,3,126,64,64,64,64,64,128,0,0,0,0,0,255,0,0,0,0,0,128,192,64,95,64,192,128,0,0,0,
           0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,31,40,40,40,40,72,240,0,0,0,0,0,0,240,72,40,40,40,40,31,0,0,224,48,16,23,16,48,224,0,0,63,72,80,80,80,72,63,0,0,0,
           0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,15,18,20,20,20,20,18,15,0,0,0,0,0,0,0,0,15,18,20,20,20,18,15,0,0,0,0,0,0,0,0,0,0,0,0])


cover_screen = thumby.Sprite(72, 40, cover1+cover2, 0, 0, -1) # combining bitmaps as animation frames

controls_screen = thumby.Sprite(72, 40, controls, 0, 0, -1)

simulate = False # are we simulating?

buf = bytearray() # our pixel data; like a texture!
cells = [] # the board we run our simulation on

wb = 72//8 # 9 -> pixel width in bytes
hb = 360//wb # 40 -> pixel width in bytes

wc = 72//2 # 36 -> width in cells
hc = 40//2 # 20 -> height in cells

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
            

def RandomizeGrid():
    global cells
    cells = [0]*(720)
    for i in range(len(cells)//6): # 720//6 =~ 120 'living' cells
        cells[random.randint(0,len(cells)-1)] = 1
    
    BuildBuffer()
    
    
def handleInput(): # called every frame
    global cursor
    global simulate
    global cells
    
    if thumby.buttonA.justPressed(): # toggle cell at cursor's position
        Beep()
        #print(f'x: {cursor.x}, y: {cursor.y}') # debugging cursor pos
        i = (cursor.x//2) + ((cursor.y//2) * 36)
        if cells[i] == 1:
            cells[i] = 0
        else:
            cells[i] = 1
        BuildBuffer()
        
    if thumby.buttonB.justPressed(): # toggles the simulate flag
        Beep()
        if simulate:
            simulate = False
        else:
            simulate = True
    
    if not simulate:
        if thumby.buttonL.justPressed(): # cursor control and screen wrapping
            Beep()
            cursor.x -= 2
            if cursor.x < 0:
                cursor.x = 2*wc-2
        if thumby.buttonR.justPressed():
            Beep()
            cursor.x += 2
            if cursor.x > 2*wc-2:
                cursor.x = 0
        if thumby.buttonU.justPressed():
            Beep()
            cursor.y -= 2
            if cursor.y < 0:
                cursor.y = 2*hc-2
        if thumby.buttonD.justPressed():
            Beep()
            cursor.y += 2
            if cursor.y > 2*hc-2:
                cursor.y = 0
    
            
def Simulate(): # inefficient, feel free to send suggestions!
    global cells
    
    old_cells = cells.copy() # previous state of board used to generate next board
    
    for row in range(hc): # remember rows go down, cols go across!
        for col in range(wc):
            c = col+(row*wc)
            neighbors = [c-wc, c-wc-1, c-wc+1, c-1, c+1, c+wc, c+wc-1, c+wc+1] # all 8 neighbors
            
            count = 0 # number of living neighbors
            for n in neighbors: # we wrap around top-left/bottom-right, and left/right for funsies
                if n >= len(cells):
                    count += old_cells[n%len(cells)]
                else:
                    count += old_cells[n]
            
            status = old_cells[c] # whether cell is alive or not
            
            if status == 1: # game of life rules
                if count < 2:
                    cells[c] = 0
                if count == 2 or count == 3:
                    cells[c] = 1
                if count > 3:
                    cells[c] = 0
            elif count == 3:
                cells[c] = 1
    
    BuildBuffer()
    
    
def Beep(): # audio feedback for inputs!
    thumby.audio.play(1000, 50)
    

### BOARD/STATE SETUP ###    
fbuffer = FrameBuffer(thumby.display.display.buffer, 72, 40, MONO_VLSB) # create thumby buffer

old_ticks=0 # timer count on last frame
blink_interval=600 # ~ms per blink
next_blink = blink_interval # time until next blink in ms
blinks = 0 # used for animating sprite

thumby.display.setFPS(30) # who needs 60fps?!
RandomizeGrid() # randomize grid before we start


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
        
        
### MAIN GAMEPLAY LOOPS ###
while 1: # splash screen
    Timing()
    if thumby.buttonA.justPressed(): # break from loop to go to next screen
        Beep()
        break
    
    thumby.display.fill(0)
    cover_screen.setFrame(blinks) # animate the controls screen
    thumby.display.drawSprite(cover_screen)
    thumby.display.update()

while 1: # controls screen
    if thumby.buttonA.justPressed():
        Beep()
        break
    
    thumby.display.fill(0)
    thumby.display.drawSprite(controls_screen)
    thumby.display.update()

while 1: # simulation screen
    Timing()
    
    thumby.display.fill(0)
    fbuffer.blit(FrameBuffer(buf, 72, 40, MONO_HMSB), 0, 0, 72,40) # drawing game board
    
    handleInput()
        
    if simulate: # hide cursor if simulating
        Simulate()
    else:
        cursor.setFrame(blinks)
        thumby.display.drawSprite(cursor)
    
    thumby.display.update() # flush the screenbuffer
