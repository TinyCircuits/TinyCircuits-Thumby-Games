import thumby
import random
import math

# BITMAP: width: 10, height: 7
bitmap_ufo = bytearray([8,28,20,30,61,61,30,20,28,8])

# BITMAP: width: 50, height: 7
bitmap_explosion = bytearray([0,0,0,0,12,12,0,0,0,0,0,0,0,12,18,18,12,0,0,0,0,0,54,34,8,8,34,54,0,0,65,34,0,8,20,20,8,0,34,65,65,0,34,0,0,0,0,34,0,65])

# 72x40 for 1 frames
bitmap_title = bytearray([0,0,0,0,0,0,8,28,20,30,61,61,30,20,28,8,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,8,28,20,30,61,61,30,20,28,8,0,0,0,0,0,0,0,0,0,0,0,0,0,0,2,0,0,0,0,0,0,0,16,0,0,0,0,0,0,16,0,1,0,0,0,0,128,0,0,0,0,0,0,8,0,0,0,0,0,0,0,0,0,1,0,0,0,0,0,0,0,0,64,0,0,0,0,0,0,0,0,0,0,0,0,34,0,0,0,0,0,0,0,0,0,0,0,0,4,0,0,0,0,2,0,0,124,20,28,0,124,84,84,0,92,84,116,0,124,16,108,0,12,112,12,0,0,0,0,0,125,20,124,0,124,64,64,0,68,124,68,0,124,84,84,0,124,4,124,0,92,84,116,0,0,2,0,0,0,0,8,0,0,0,0,0,0,0,0,32,0,0,0,4,0,0,0,0,0,0,0,0,0,16,0,0,0,0,0,0,0,8,0,0,0,0,0,0,16,0,0,0,0,0,0,0,0,0,16,0,0,0,0,0,1,0,0,0,0,64,0,0,0,0,0,0,2,0,0,0,0,0,0,0,32,0,0,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255])

#music
tune1 = [659, 659, 659,   0, 659, 659, 659,   0, 659, 659, 659,   0, 523, 523, 587, 587, 587,   0, 587, 587, 587,   0, 523, 523, 587, 587, 587,   0, 659, 659, 659, 659,\
523, 523, 523, 523,   0,   0, 440, 440, 440, 440,   0,   0,   0,   0, 293, 329,   0,   0, 349, 329,   0,   0, 293, 329,   0,   0, 349, 329,   0,   0, 293,   0,\
659, 659, 659,   0, 659, 659, 659,   0, 659, 659, 659,   0, 587, 587, 659, 659, 659,   0, 659, 659, 659,   0, 587, 587, 659, 659, 659,   0, 739, 739, 739,   0,\
830, 830, 830,   0,   0,   0, 659, 659, 659,   0,   0,   0,   0,   0, 246, 261,   0,   0, 246, 261,   0,   0, 246, 261,   0,   0, 246, 739, 739,   0, 830, 830,\
880, 880, 880,   0, 880, 880, 880,   0, 880, 880, 880,   0, 880, 880, 880,   0, 784, 784, 784,   0, 784, 784, 784,   0, 784, 784, 784,   0, 784, 784, 784,   0,\
739, 739, 739,   0, 739, 739, 739,   0, 739, 739, 739,   0, 739, 739, 739,   0, 698, 698, 698,   0, 698, 698, 698,   0, 698, 698, 698,   0, 698, 698, 698,   0,\
659,   0,   0, 698, 659,   0,   0, 587, 659,   0,   0, 698, 659,   0,   0, 587, 659,   0,   0, 698, 659,   0,   0, 587, 659,   0,   0, 698, 659,   0,   0, 830,\
880, 880, 880, 880, 880, 880, 880, 880, 659, 659, 659, 659, 659, 659, 659, 659, 880, 880, 880, 880, 880, 880, 880, 880,   0,   0,   0,   0,   0,   0,   0,   0]

tune2 = [0,   0,   0,   0, 329, 329, 329,   0,   0,   0,   0,   0, 329, 329, 329,   0,   0,   0,   0,   0, 293, 293, 293,   0,   0,   0,   0,   0, 293, 293, 293,   0,\
        0,   0,   0,   0, 220, 220, 220,   0,   0,   0,   0,   0, 220, 220, 220,   0,   0,   0,   0,   0, 220, 220, 220,   0,   0,   0,   0,   0, 220, 220, 220,   0,\
        0,   0,   0,   0, 329, 329, 329,   0,   0,   0,   0,   0, 329, 329, 329,   0,   0,   0,   0,   0, 329, 329, 329,   0,   0,   0,   0,   0, 329, 329, 329,   0,\
        0,   0,   0,   0, 415, 415, 415,   0,   0,   0,   0,   0, 415, 415, 415,   0,   0,   0,   0,   0, 415, 415, 415,   0,   0,   0,   0,   0, 415, 415, 415,   0,\
        0,   0,   0,   0, 440, 440, 440,   0,   0,   0,   0,   0, 440, 440, 440,   0,   0,   0,   0,   0, 392, 392, 392,   0,   0,   0,   0,   0, 392, 392, 392,   0,\
        0,   0,   0,   0, 369, 369, 369,   0,   0,   0,   0,   0, 369, 369, 369,   0,   0,   0,   0,   0, 349, 349, 349,   0,   0,   0,   0,   0, 349, 349, 349,   0,\
        0,   0,   0,   0, 329, 329, 329,   0,   0,   0,   0,   0, 329, 329, 329,   0,   0,   0,   0,   0, 329, 329, 329,   0,   0,   0,   0,   0, 329, 329, 329,   0,\
        0,   0,   0,   0, 440, 440, 440,   0,   0,   0,   0,   0, 440, 440, 440,   0,   0,   0,   0,   0, 440, 440, 440,   0,   0,   0,   0,   0,   0,   0,   0,   0]

idx = 0

class UFO:

    #7 possible positions
    pos = 0
    oldPos = 0
    oldxPos = 0
    clock = 0.0
    diff = 0
    exploded = False
    done_exploding = False
    curFrame = 0.0
    hits = 0

    respawn_delay = 60 #60 frames or 2 seconds at 30FPS
    respawn_counter = 0

    targeting_cow = False
    moving_to_cow = False
    targeted_cow = 0
    
    def __init__(self):
        #x=-70 to fly in from left
        self.sprite_ufo = thumby.Sprite(10, 7, bitmap_ufo, -70, 0, 0, 0, 0)
        
    def move(self, newPos):
        self.oldPos = self.sprite_ufo.x
        
        if newPos >= 0 and newPos <=6:
            self.pos = newPos
        self.clock = 0.0
        
        self.diff = self.sprite_ufo.x - newPos*10
            
    def update(self):
        
        if not self.exploded:
            self.clock += 0.025
            if self.clock > 1.0:
                self.clock = 1.0
                
            self.oldxPos = self.sprite_ufo.x
            
            self.smooth_pos = int(self.smoothPos(self.clock, self.diff))
            #print(self.diff, end = ", ")
            #print(self.smooth_pos)
                
            self.sprite_ufo.x = (self.oldPos - self.smooth_pos)+1
            
            if self.sprite_ufo.x != self.oldxPos:
                if abs(self.smooth_pos) > 7:
                    thumby.audio.play(250*abs(self.smooth_pos), 10) #moving sound
            
            if self.targeting_cow:
                if self.sprite_ufo.x == self.targeted_cow.cur_pos and self.moving_to_cow:
                    self.targeted_cow.target() #initiates abduction
                    self.moving_to_cow = False
                
            
            thumby.display.drawSprite(self.sprite_ufo)
        
        elif not self.done_exploding:
            self.sprite_ufo.setFrame(int(self.curFrame))
            thumby.display.drawSprite(self.sprite_ufo)
            self.curFrame += 0.5
            if self.curFrame > 4:
                self.curFrame = 0
                self.done_exploding = True
        else:
            self.respawn_counter += 1
            if self.respawn_counter >= self.respawn_delay:
                self.respawn()
                self.respawn_counter = 0
        
    def smoothPos(self, t, diff):
        #sigmoid position function
        if t != 1.0:
            return 1.0/(1+math.e**(-16*(t-0.5))) * float(diff)
        else:
            return float(diff)
        
    def getCol(self, ammo):
        if not self.exploded:
            if ammo.x > self.sprite_ufo.x and ammo.x < self.sprite_ufo.x + self.sprite_ufo.width:
                if ammo.y > self.sprite_ufo.y and ammo.y < self.sprite_ufo.height + self.sprite_ufo.y:
                    print("HIT")
                    self.exploded = True
                    if self.targeting_cow:
                        self.targeted_cow.release()
                    self.hits += 1
                    
                    #set up animation
                    x = self.sprite_ufo.x
                    y = self.sprite_ufo.y
                    self.sprite_ufo = thumby.Sprite(10, 7, bitmap_explosion, x, y, 0, 0, 0)
                    self.sprite_ufo.setFrame(0)
                    
                    thumby.audio.play(1046, 200)
                    return self.hits
                
    def respawn(self):
        self.oldPos = -70
        self.pos = 0
        self.clock = 0.0
        self.diff = 0
        self.exploded = False
        self.done_exploding = False
        self.curFrame = 0.0
        self.targeting_cow = False
        
        #x=-70 to fly in from left
        self.sprite_ufo = thumby.Sprite(10, 7, bitmap_ufo, -70, 0, 0, 0, 0)
        
    def targetCow(self, cow):
        self.targeting_cow = True
        self.moving_to_cow = True
        self.targeted_cow = cow
        
        self.oldPos = self.sprite_ufo.x
        
        self.clock = 0.0
        
        self.diff = self.sprite_ufo.x - self.targeted_cow.cur_pos + 1
        
    def takeOff(self):
        self.targeting_cow = False
        self.moving_to_cow = False
        
        self.oldPos = self.sprite_ufo.x
        
        self.clock = 0.0
        
        self.diff = self.sprite_ufo.x - 100 #fly off screen
        
class Cow:
    # BITMAP: width: 10, height: 7
    bitmap_cow = bytearray([12,11,126,27,124,28,124,28,124,2])
    # BITMAP: width: 10, height: 7
    bitmap_cow_invert = bytearray([115,116,1,100,3,99,3,99,3,125])
    cur_pos = 1
    new_pos = 1
    screen_pos = [1, 11, 51, 61]
    
    move_delay = 300
    move_counter = 0 #cow moves every 10 seconds
    
    #abduction variables
    targeted = False
    gone = False
    
    frame = 0
    
    def __init__(self):
        self.sprite_cow = thumby.Sprite(10,7, self.bitmap_cow, 1, 33, -1, 0, 0)
        
    def update(self):
        self.frame += 1
        if not self.gone:
            if self.targeted:
                #draw tractor beam
                thumby.display.drawFilledRectangle(self.cur_pos, 7, 10, 33, 1)
                
                if self.frame % 5 == 0:
                    self.sprite_cow.y -= 1 #rise every 5 frames
                
                if self.sprite_cow.y < 8:
                    self.gone = True
                    
            else:
                if self.sprite_cow.y < 33:
                    self.sprite_cow.y += 1
                self.move_counter += 1
                if self.move_counter >= self.move_delay:
                    self.move_counter = 0
                    self.move()
                    
                if self.cur_pos < self.new_pos:
                    self.cur_pos += 1
                if self.cur_pos > self.new_pos:
                    self.cur_pos -= 1
                    
                self.sprite_cow.x = self.cur_pos   
                
            thumby.display.drawSprite(self.sprite_cow)
    
    def move(self):
        if not self.targeted:
            self.new_pos = (random.randrange(0, 7)*10)+1
        
            #flip cow sprite accordingly
            if self.new_pos > self.cur_pos: #face right
                self.sprite_cow = thumby.Sprite(10,7, self.bitmap_cow, self.cur_pos, 33, -1, 1, 0)
            elif self.new_pos < self.cur_pos: #face left
                self.sprite_cow = thumby.Sprite(10,7, self.bitmap_cow, self.cur_pos, 33, -1, 0, 0)
        
        
        
    def target(self):
        self.targeted = True
        self.sprite_cow = thumby.Sprite(10,7, self.bitmap_cow_invert, self.cur_pos, 33, -1, 0, 0)
    
    def release(self):
        self.targeted = False
        self.sprite_cow = thumby.Sprite(10,7, self.bitmap_cow, self.cur_pos, 33, -1, 0, 0)
    
class Tank:
    # BITMAP: width: 20, height: 7
    bitmap_tank = bytearray([120,4,4,4,120,124,126,126,126,127,127,126,126,126,124,120,4,4,4,120])
    
    #7 possible positions
    pos = 3
    screen_pos = 35
    
    pressed = False
    gun_dirs = [29, 31, 33, 35, 37, 39, 41]
    
    def __init__(self):
        self.sprite_tank = thumby.Sprite(20, 7, self.bitmap_tank, 26, 33, 0, 0, 0)

    def update(self):
        #draw tank body
        thumby.display.drawSprite(self.sprite_tank)
        
        #draw gun
        thumby.display.drawLine(35, 36, self.screen_pos, 29, 1)
        thumby.display.drawLine(36, 36, self.screen_pos+1, 29, 1)
        
    def input(self):
        
        
        if thumby.buttonR.pressed() and not self.pressed:
            self.pos += 1
            if self.pos > 6:
                self.pos = 6
            self.pressed = True
            print(self.pos)
            self.screen_pos = self.gun_dirs[self.pos]
        elif thumby.buttonL.pressed() and not self.pressed:
            self.pos -= 1
            if self.pos < 0:
                self.pos = 0
            self.pressed = True
            print(self.pos)
            self.screen_pos = self.gun_dirs[self.pos]
        elif not thumby.buttonL.pressed() and not thumby.buttonR.pressed():
            self.pressed = False
    
class Ammo:
    slope = 0.0
    init_x = 0.0
    init_y = 0.0
    x = 0.0
    y = 0.0
    change_x = 0.0
    change_y = 0.0
    visible = False
    speed = 1.0
    pressed = False
    
    def __init__(self, x, y, speed):
        self.init_x = x
        self.init_y = y
        self.speed= speed
        pass
    
    def update(self):
        self.x += self.change_x * self.speed
        self.y += self.change_y * self.speed
        
        thumby.display.setPixel(int(self.x), int(self.y), 1)
        
    def input(self, tank):
        if thumby.buttonA.pressed() and not self.pressed:
            self.pressed = True
            self.shoot(tank)
        elif not thumby.buttonA.pressed():
            self.pressed = False
    
    def shoot(self, tank):
        self.x = self.init_x
        self.y = self.init_y
        self.change_x = tank.gun_dirs[tank.pos] - 35
        self.change_y = -7
            
        


myUFO = UFO()
myCow = Cow()
myTank = Tank()
myAmmo = Ammo(33, 36, 0.25)
frame = 0
title_screen = True

game_level = 1

thumby.display.setFPS(16) #Music FPS

#draw title screen
thumby.display.blit(bitmap_title, 0, 0, 72, 40, 0, 0, 0)

while 1:
    while title_screen:
        if idx < len(tune1):
            if tune1[idx] != 0 and tune2[idx] == 0:
                thumby.audio.play(tune1[idx], 58)
        
            elif tune1[idx] == 0 and tune2[idx] != 0:
                thumby.audio.play(tune2[idx], 58)
            
            elif tune1[idx] != 0 and tune2[idx] != 0:
                #cheap multi voice
                thumby.audio.playBlocking(tune1[idx], 10)
                thumby.audio.playBlocking(tune2[idx], 10)
                thumby.audio.playBlocking(tune1[idx], 10)
                thumby.audio.playBlocking(tune2[idx], 10)
                thumby.audio.playBlocking(tune1[idx], 10)
                thumby.audio.playBlocking(tune2[idx], 8)
        idx += 1
        if thumby.buttonA.pressed():
            thumby.display.setFPS(30) #Gameplay FPS
            title_screen = False
        else:
            thumby.display.update()
    
    #more movements as level increases
    if frame % (120 - game_level*5) == 0 and not myUFO.targeting_cow:
        
        #attempt an abduction once in a while
        #becomes more frequent with level
        if random.randrange(0, 20 - game_level) == 0 and not myCow.gone:
            myUFO.targetCow(myCow)
        else:
            ufo_pos = random.randrange(0, 7)
        
        myUFO.move(ufo_pos)
        
    myTank.input()
    myAmmo.input(myTank)

    
    if myUFO.getCol(myAmmo) % 5 == 0 and game_level < 20:
        game_level += 1
        print("Level " + str(game_level))
        
    thumby.display.fill(0)
    
    thumby.display.drawText(str(myUFO.hits), 60, 33, 1)
    
    myUFO.update()
    myCow.update()
    myTank.update()
    myAmmo.update()
    thumby.display.update()
    frame += 1