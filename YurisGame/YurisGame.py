# Yuri's Game
#
# Released under MIT License
# Copyright Xu Pan (Douz) 2023
#
# Hold A/B button to pick up a bubble. Use directional buttons to 
# move the bubble and merge it with other bubbles. Your goal is 
# to form a single large bubble. This game is inspired by Yuri's
# childhood memory.
#

import time
import thumby
import math
import array
import random

# BITMAP: width: 72, height: 40
welcome_bitmap = bytearray([0,0,0,0,0,0,0,0,0,0,128,128,0,0,128,128,192,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,128,128,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,
            0,0,0,0,0,0,0,0,0,0,1,7,254,14,1,0,0,0,240,240,0,0,224,240,0,0,224,224,48,16,112,0,0,246,242,0,0,9,7,0,128,160,80,144,176,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,
            0,0,0,0,0,0,0,0,0,0,0,0,3,0,0,0,0,0,1,3,2,2,3,3,0,0,7,7,0,0,192,224,224,97,99,64,0,0,0,0,1,2,2,2,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,
            0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,31,127,65,128,144,136,88,56,0,0,224,212,148,172,184,96,0,254,252,4,4,248,12,252,248,0,0,32,120,232,168,184,144,0,0,0,0,0,0,0,0,0,0,
            0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0])
welcome = thumby.Sprite(72, 40, welcome_bitmap, 0, 0)
# BITMAP: width: 72, height: 40
ending_bitmap = bytearray([0,0,0,0,0,0,0,0,0,0,0,128,192,192,192,192,128,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,192,128,192,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,
            0,0,0,0,0,0,0,0,0,0,62,255,131,1,32,24,144,112,0,0,224,24,8,8,248,224,0,0,224,24,8,8,248,224,0,0,240,56,8,10,250,255,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,
            0,0,0,0,0,0,0,0,0,0,0,0,0,1,1,1,0,0,0,0,0,3,2,2,1,0,0,0,0,3,2,2,65,64,64,192,64,65,1,1,0,0,0,0,0,0,0,64,192,0,0,0,0,0,0,0,0,0,128,192,0,0,0,0,0,0,0,0,0,0,0,0,
            0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,96,128,0,0,224,63,5,5,0,224,24,8,8,248,224,0,0,245,143,8,8,8,240,0,0,0,0,0,191,0,0,0,0,0,0,0,0,0,0,0,0,0,
            0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,1,1,0,0,0,0,0,0,3,2,2,1,0,0,0,1,0,1,1,1,0,0,0,0,0,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0])
ending = thumby.Sprite(72, 40, ending_bitmap, 0, 0)

def distance(point1, point2):
    return(math.sqrt((point1[0]-point2[0])**2+(point1[1]-point2[1])**2))

def Bubble_bitmap(r):
    bit_map = []
    
    x = math.floor(r)
    y = 0
     
    bit_map.append([x,0])
    bit_map.append([-x,0])
    bit_map.append([0,x])
    bit_map.append([0,-x])
    
    P = 1 - r
 
    while x > y:  
        y += 1
        if P <= 0:
            P = P + 2 * y + 1
        else:        
            x -= 1
            P = P + 2 * y - 2 * x + 1

        if (x < y):
            break
            
        bit_map.append([x,y])
        bit_map.append([x,-y])
        bit_map.append([-x,y])
        bit_map.append([-x,-y])

        if x != y:
            bit_map.append([y,x])
            bit_map.append([y,-x])
            bit_map.append([-y,x])
            bit_map.append([-y,-x])

    return bit_map

def Collision_detect(bubble, Bubbles):
    for b in Bubbles:
        if b is not bubble:
            if distance([b.x, b.y],[bubble.x, bubble.y]) < (b.r+bubble.r):
                return b
    return None
    
def Merge(b1, b2):
    x = int((b1.r**2*b1.x + b2.r**2*b2.x) / (b1.r**2+b2.r**2))
    y = int((b1.r**2*b1.y + b2.r**2*b2.y) / (b1.r**2+b2.r**2))
    r = math.sqrt(b1.r**2+b2.r**2)
    thumby.audio.play(600, 100)
    return Bubble(r, x, y)

class Bubble:
    def __init__(self, r, center_x, center_y):
        self.r = r
        self.x = center_x
        self.y = center_y
        self.bitmap = Bubble_bitmap(r)
    
    def draw(self):
        for point in self.bitmap:
            thumby.display.setPixel(self.x+point[0], self.y+point[1], 1)
            
    def move(self, direction):
        if direction == 0: # UP
            if self.y > 0:
                self.y -= 1
        
        if direction == 1: # Down
            if self.y < 39:
                self.y += 1
        
        if direction == 2: # Left
            if self.x > 0:
                self.x -= 1
        
        if direction == 3: # Right
            if self.x < 71:
                self.x += 1
    
    def update_r(self, r):
        self.r = r
        self.bitmap = Bubble_bitmap(r)

class Cursor:
    def __init__(self, center_x, center_y):
        self.x = center_x
        self.y = center_y
        self.free = True
        self.free_bitmap = [[0,0],[1,1],[2,2],[3,3],[4,4],[5,5],[6,6],[7,7]]
        self.hold_bitmap = [[0,0],[-1,0],[1,0],[0,1],[0,-1],[1,1],[2,2],[3,3],[4,4],[5,5],[6,6],[7,7]]
    
    def draw(self):
        if self.free == True:
            for point in self.free_bitmap:
                thumby.display.setPixel(self.x+point[0], self.y+point[1], 1)
        else:
            for point in self.hold_bitmap:
                thumby.display.setPixel(self.x+point[0], self.y+point[1], 1)
    
    def move(self, direction):
        if direction == 0: # UP
            if self.y > 0:
                self.y -= 1
        
        if direction == 1: # Down
            if self.y < 39:
                self.y += 1
        
        if direction == 2: # Left
            if self.x > 0:
                self.x -= 1
        
        if direction == 3: # Right
            if self.x < 71:
                self.x += 1
            

# Outer loop
while(1):
    
    # Welcome screen
    t1 = time.ticks_ms()   # Get time (ms)
    Bubbles = []
    while(1):
        thumby.display.drawSprite(welcome)
        
        t = time.ticks_ms()   # Get time (ms)
        # new Bubble
        if (t-t1)>300 and len(Bubbles)<4:
            rand_r = 1
            rand_x = random.randint(2, 70)
            rand_y = random.randint(2, 38)
            Bubbles.append(Bubble(rand_r, rand_x, rand_y))
            # print(Bubbles)
            t1= time.ticks_ms()   # Get time (ms)
        
        # Change size of Bubbles
        for bubble in Bubbles:
            bubble.update_r(bubble.r+0.5)
        
        # Delete large Bubbles
        for bubble in Bubbles:
            if bubble.r > 30:
                Bubbles.remove(bubble)
                
        # Display
        for bubble in Bubbles:
            bubble.draw()
            
        thumby.display.update()
        
        if thumby.actionJustPressed():
            break
    
    # Setup
    thumby.display.fill(0) # Fill canvas to black
    n = random.randint(10, 22)
    
    # Initialize bubbles
    Bubbles = []
    for i in range(n):
        rand_r = random.randrange(1, 4)
        # test if overlap
        overlap = True
        while(overlap):
            overlap = False
            rand_x = random.randint(2, 70)
            rand_y = random.randint(2, 38)
            for bubble in Bubbles:
                if distance([rand_x, rand_y],[bubble.x, bubble.y]) < (rand_r+bubble.r):
                    overlap = True
                    break
        Bubbles.append(Bubble(rand_r, rand_x, rand_y))
    
    # Display
    for bubble in Bubbles:
        bubble.draw()
        
    # Initialize Cursor
    cursor = Cursor(36,20)
    cursor.draw()
    
    thumby.display.update()
    
    t0 = time.ticks_ms()   # Get time (ms)
    # Main loop, game mode
    while(1):
        
        thumby.display.fill(0) # Fill canvas to black
        
        for bubble in Bubbles:
            bubble.draw()
            
        cursor.draw()
        
        # Find selected bubble
        bubble_selected = None
        if thumby.actionPressed():
            cursor.free = False
            # find if hold a bubble
            for bubble in Bubbles:
                if distance([cursor.x, cursor.y],[bubble.x, bubble.y]) < bubble.r:
                    bubble_selected = bubble
                    break
        else:
            cursor.free = True
            
        # Split
        # here to set split frequency and smallist r that can be splitted
        if bubble_selected is not None and bubble_selected.r >= 5 and random.random() < 0.0012:
            r = bubble_selected.r
            x = bubble_selected.x
            y = bubble_selected.y
            new_r = math.sqrt(r**2/2)
            random_angle = random.uniform(0,math.pi)
            Bubbles.remove(bubble_selected)
            new_bubble_1 = Bubble(new_r, round(x+new_r*math.cos(random_angle)), math.ceil(y+new_r*math.sin(random_angle)))
            new_bubble_2 = Bubble(new_r, round(x-new_r*math.cos(random_angle)), math.floor(y-new_r*math.sin(random_angle)))
            if Collision_detect(new_bubble_1, Bubbles) is None and Collision_detect(new_bubble_2, Bubbles) is None:
                Bubbles.append(new_bubble_1)
                Bubbles.append(new_bubble_2)
            else:
                Bubbles.append(bubble_selected)
            continue
        
        # Move
        if thumby.buttonU.justPressed():
            cursor.move(0)
            if bubble_selected is not None:
                bubble_selected.move(0)
        if thumby.buttonD.justPressed():
            cursor.move(1)
            if bubble_selected is not None:
                bubble_selected.move(1)
        if thumby.buttonL.justPressed():
            cursor.move(2)
            if bubble_selected is not None:
                bubble_selected.move(2)
        if thumby.buttonR.justPressed():
            cursor.move(3)
            if bubble_selected is not None:
                bubble_selected.move(3)
                
        # Merge
        while bubble_selected is not None:
            bubble_encountered = Collision_detect(bubble_selected, Bubbles)
            if bubble_encountered is not None:
                new_bubble = Merge(bubble_selected, bubble_encountered)
                Bubbles.append(new_bubble)
                Bubbles.remove(bubble_selected)
                Bubbles.remove(bubble_encountered)
                bubble_selected = new_bubble
                thumby.audio.play(600, 100)
            else:
                break
        
        # Jitter all bubbles
        
        t = time.ticks_ms()   # Get time (ms)
        # here to set jitter frequency
        if (t-t0)>3000:
            t0 = time.ticks_ms()   # Get time (ms)
            for bubble in Bubbles:
                # jitter range
                dx = random.randint(-1,1)
                dy = random.randint(-1,1)
                bubble.x += dx
                if bubble.x < 2 or bubble.x >70:
                    bubble.x -= dx
                    continue
                bubble.y += dy
                if bubble.y < 2 or bubble.y >38:
                    bubble.x -= dx
                    bubble.y -= dy
                    continue
                Bubbles.remove(bubble)
                if Collision_detect(bubble, Bubbles) is None:
                    Bubbles.append(bubble)
                else:
                    bubble.x -= dx
                    bubble.y -= dy
                    Bubbles.append(bubble)
        
        # Finished!
        if len(Bubbles) == 1:
            break
        
        thumby.display.update()
    
    # Ending screen.
    t0 = time.ticks_ms()   # Get time (ms)
    t1 = t0
    Bubbles = []
    while(1):
        thumby.display.drawSprite(ending)
        
        t = time.ticks_ms()   # Get time (ms)
        
        # new Bubble
        if (t-t1)>300 and len(Bubbles)<4:
            rand_r = 1
            rand_x = random.randint(2, 70)
            rand_y = random.randint(2, 38)
            Bubbles.append(Bubble(rand_r, rand_x, rand_y))
            # print(Bubbles)
            t1= time.ticks_ms()   # Get time (ms)
        
        # Change size of Bubbles
        for bubble in Bubbles:
            bubble.update_r(bubble.r+0.5)
        
        # Delete large Bubbles
        for bubble in Bubbles:
            if bubble.r > 30:
                Bubbles.remove(bubble)
        
        # Display
        for bubble in Bubbles:
            bubble.draw()
        thumby.display.update()
        
        # Press to restart
        if (t-t0)>1000 and thumby.actionJustPressed():
            break
