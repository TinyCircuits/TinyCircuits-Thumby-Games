#Space Evaders
#by SuperRiley64

#Don't let the UFOs abduct your prize-winning cows! Use the WWII tank your grandpa left you to evade the aliens!

import thumby
import random
import math
import time

# BITMAP: width: 10, height: 7
bitmap_ufo = bytearray([8,28,20,30,61,61,30,20,28,8])

# BITMAP: width: 50, height: 7
bitmap_explosion = bytearray([0,0,0,0,12,12,0,0,0,0,0,0,0,12,18,18,12,0,0,0,0,0,54,34,8,8,34,54,0,0,65,34,0,8,20,20,8,0,34,65,65,0,34,0,0,0,0,34,0,65])

#BITMAP: width: 10, height: 7
bitmap_cow_title = bytearray([12,11,126,27,124,28,124,28,124,2])

news_text = "BREAKING NEWS! Alien Spaceships have been detected over several farming towns. They are here to take livestock. Protect your cattle!"



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
    points = 0

    respawn_delay = 60 #60 frames or 2 seconds at 30FPS
    respawn_counter = 0

    targeting_cow = False
    moving_to_cow = False
    targeted_cow = 0
    
    def __init__(self, pos):
        self.pos = pos
        #x=-70 to fly in from left
        self.sprite_ufo = thumby.Sprite(10, 7, bitmap_ufo, random.choice([-50, 122]), 0, 0, 0, 0)
        
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
                    self.targeted_cow.target(self) #initiates abduction
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
            
            #draw # of hits
            thumby.display.drawFilledRectangle(self.sprite_ufo.x, self.sprite_ufo.y, 10, 7, 0)
            thumby.display.drawText(str(self.points), self.sprite_ufo.x, self.sprite_ufo.y, 1)
            
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
        
    def getCol(self, ammo, ufo_spots, points):
        if not self.exploded:
            if ammo.x > self.sprite_ufo.x and ammo.x < self.sprite_ufo.x + self.sprite_ufo.width:
                if ammo.y > self.sprite_ufo.y and ammo.y < self.sprite_ufo.height + self.sprite_ufo.y:
                    self.exploded = True
                    if self.targeting_cow:
                        self.targeted_cow.release()
                    self.hits += 1
                    ufo_spots[self.pos] = False
                    self.points = points + 1
                    
                    #set up animation
                    x = self.sprite_ufo.x
                    y = self.sprite_ufo.y
                    self.sprite_ufo = thumby.Sprite(10, 7, bitmap_explosion, x, y, 0, 0, 0)
                    self.sprite_ufo.setFrame(0)
                    
                    thumby.audio.play(1046, 200)
                    return 1
        return 0
                
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
        
        self.diff = self.sprite_ufo.x - self.targeted_cow.new_pos + 1
        
    def takeOff(self, ufo_spots):
        self.targeting_cow = False
        self.moving_to_cow = False
        
        self.oldPos = self.sprite_ufo.x
        ufo_spots[self.pos] = False
        
        self.clock = 0.0
        
        self.diff = self.sprite_ufo.x - 100 #fly off screen
        
class Cow:
    
    #Cow Frames
    #0 - Still
    #1 - Walk 1
    #2 - Walk 2
    #3-7 - Spin
    
    
    # 10x7 for 7 frames
    bitmap_cow = bytearray([12,11,126,27,124,28,124,28,124,2,12,11,126,27,60,28,124,28,60,2,12,11,62,27,124,28,60,28,124,4,0,12,11,123,124,28,124,126,0,0,0,0,0,123,30,30,123,0,0,0,0,0,126,124,28,124,123,11,12,0,2,124,28,124,28,124,27,126,11,12])
    
    # 10x7 for 7 frames
    bitmap_cow_invert = bytearray([115,116,1,100,3,99,3,99,3,125,115,116,1,100,67,99,3,99,67,125,115,116,65,100,3,99,67,99,3,123,127,115,116,4,3,99,3,1,127,127,127,127,127,4,97,97,4,127,127,127,127,127,1,3,99,3,4,116,115,127,125,3,99,3,99,3,100,1,116,115])

    # BITMAP: width: 7, height: 7
    bitmap_heart = bytearray([0,12,30,60,30,12,0])

    spin_seq = [0, 3, 4, 5, 6, 5, 4, 3]
    spin_idx = 0

    cur_pos = 1
    new_pos = 1
    pos = 0 #0 to 3
    screen_pos = [1, 11, 51, 61]
    y_pos = 33
    
    move_delay = 300
    move_counter = 0 #cow moves every 10 seconds
    
    #abduction variables
    targeted = False
    gone = False
    
    frame = 0
    walk_frame = False
    show_heart = False
    heart_frame = 0
    
    def __init__(self):
        self.sprite_cow = thumby.Sprite(10, 7, self.bitmap_cow, 1, self.y_pos, -1, 0, 0)
        self.sprite_heart = thumby.Sprite(7, 7, self.bitmap_heart, 1, self.y_pos - 8, -1, 0, 0)
        self.sprite_cow.setFrame(0)
        
    def update(self, ufo_spots, game_level):
        self.sprite_heart.x = self.sprite_cow.x + 2
        self.sprite_heart.y = self.sprite_cow.y - 8
        
        if self.show_heart:
            thumby.display.drawSprite(self.sprite_heart)
        
        self.frame += 1
        if not self.gone:
            if self.targeted:
                self.show_heart = False
                #draw tractor beam
                thumby.display.drawFilledRectangle(self.cur_pos, 7, 10, 33, 1)
                
                if self.frame % (11-game_level//2) == 0:
                    self.y_pos -= 1 
                    self.sprite_cow.setFrame(self.spin_seq[self.spin_idx])
                    
                    self.spin_idx += 1
                    if self.spin_idx >= len(self.spin_seq):
                        self.spin_idx = 0
                    
                    self.sprite_cow.y = self.y_pos
                
                if self.sprite_cow.y < 8:
                    self.gone = True
                    
            else:
                self.sprite_cow.setFrame(0)
                if self.y_pos == 32:
                    self.show_heart = True
                if self.y_pos < 33:
                    self.y_pos += 1
                    self.sprite_cow.y = self.y_pos
                else:
                    if self.walk_frame:
                        self.sprite_cow.setFrame(1)
                    else:
                        self.sprite_cow.setFrame(2)
                    
                    if self.cur_pos < self.new_pos:
                        self.cur_pos += 1
                        if self.cur_pos % 2 == 0:
                            self.walk_frame = not self.walk_frame
                    elif self.cur_pos > self.new_pos:
                        self.cur_pos -= 1
                        if self.cur_pos % 2 == 0:
                            self.walk_frame = not self.walk_frame
                    else:
                        self.sprite_cow.setFrame(0)
                    
                    self.sprite_cow.x = self.cur_pos
                    
                        
            thumby.display.drawSprite(self.sprite_cow)
        elif self.targeted:
            dialog("Oh no!", 2)
            self.ufo.takeOff(ufo_spots)
            self.targeted = False
    
    def move(self, pos):
        self.show_heart = False
        self.pos = pos
        if not self.targeted:
            #self.new_pos = (random.randrange(0, 7)*10)+1
            
            #4 possible (and visible!) cow positions
            self.new_pos = self.screen_pos[pos]
        
            #flip cow sprite accordingly
            if self.new_pos > self.cur_pos: #face right
                self.sprite_cow = thumby.Sprite(10,7, self.bitmap_cow, self.cur_pos, self.y_pos, -1, 1, 0)
            elif self.new_pos < self.cur_pos: #face left
                self.sprite_cow = thumby.Sprite(10,7, self.bitmap_cow, self.cur_pos, self.y_pos, -1, 0, 0)
        
    def target(self, ufo):
        self.targeted = True
        self.ufo = ufo
        self.sprite_cow = thumby.Sprite(10,7, self.bitmap_cow_invert, self.cur_pos, self.y_pos, -1, 0, 0)
    
    def release(self):
        self.targeted = False
        self.sprite_cow = thumby.Sprite(10,7, self.bitmap_cow, self.cur_pos, self.y_pos, -1, 0, 0)
    
class Tank:
    # BITMAP: width: 20, height: 7
    bitmap_tank = bytearray([120,4,84,4,120,124,126,126,126,127,127,126,126,126,124,120,4,84,4,120])    
    
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
        
    def take_input(self):
        
        
        if thumby.buttonR.pressed() and not self.pressed:
            self.pos += 1
            if self.pos > 6:
                self.pos = 6
            self.pressed = True
            self.screen_pos = self.gun_dirs[self.pos]
        elif thumby.buttonL.pressed() and not self.pressed:
            self.pos -= 1
            if self.pos < 0:
                self.pos = 0
            self.pressed = True
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
    speed = 3.0
    pressed = False
    last_shot = 0
    
    def __init__(self, x, y, speed):
        self.init_x = x
        self.init_y = y
        self.speed= speed
        pass
    
    def update(self):
        self.x += self.change_x * self.speed
        self.y += self.change_y * self.speed
        
        thumby.display.setPixel(int(self.x), int(self.y), 1)
        
    def take_input(self, tank, frame):
        if thumby.buttonA.pressed() and frame - self.last_shot >= 15 and not self.pressed:
            self.pressed = True
            self.shoot(tank)
            self.last_shot = frame
        elif not thumby.buttonA.pressed():
            self.pressed = False
    
    def shoot(self, tank):
        self.x = self.init_x
        self.y = self.init_y
        self.change_x = tank.gun_dirs[tank.pos] - 35
        self.change_y = -7
            
def dialog(text, secs):
    
    width = 6*len(text)
    
    #box
    thumby.display.drawFilledRectangle(36-width//2, 12, width, 9, 0)
    thumby.display.drawRectangle(34-width//2, 11, width+3, 11, 1)
    
    thumby.display.drawText(text, 36-width//2, 13, 1)
    thumby.display.update()
    time.sleep(secs)

def game():   
    # 72x40 for 1 frames
    bitmap_title = bytearray([0,0,0,0,32,0,0,2,0,152,36,200,0,252,36,24,0,248,36,248,0,248,4,136,0,252,36,4,0,0,0,0,0,0,0,0,0,0,0,0,252,36,4,0,124,128,124,0,248,36,248,0,252,4,248,0,252,36,4,0,252,36,216,0,0,16,0,1,0,0,64,0,0,0,0,0,16,0,0,0,0,0,1,0,0,1,0,0,16,1,0,1,0,0,1,0,0,1,1,1,8,0,0,0,0,0,0,0,0,2,64,0,1,1,1,0,0,1,0,0,1,0,1,0,1,17,0,0,1,1,1,8,1,0,1,0,0,0,0,0,2,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,128,128,128,128,128,128,128,128,128,128,128,128,128,128,128,128,128,128,128,128,128,128,128,128,128,128,128,128,128,128,128,128,128,128,128,128,128,128,128,128,128,128,128,128,128,128,128,128,128,128,128,128,128,128,128,128,128,128,128,128,128,128,128,128,128,128,128,128,128,128,128,128,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255])
    # 72x30 for 1 frames
    bitmap_field = bytearray([0,0,0,0,0,0,64,0,0,0,0,0,0,4,0,0,0,0,0,0,0,0,0,0,0,16,0,0,0,0,0,0,0,0,0,0,0,128,0,0,0,0,0,0,0,32,0,0,0,0,0,0,0,0,0,0,16,0,0,0,0,0,0,0,0,0,0,0,16,0,0,0,0,0,0,128,0,0,0,0,0,0,0,0,0,64,0,0,0,0,0,0,0,0,0,0,4,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,64,0,0,0,0,0,0,0,64,0,0,0,0,0,0,0,0,0,1,0,0,0,128,0,16,0,0,0,0,128,128,192,64,64,64,64,64,96,32,32,32,32,32,32,32,32,32,32,32,32,32,32,32,32,160,192,192,192,192,192,192,192,192,192,192,192,192,192,192,128,128,128,128,0,0,0,0,0,128,128,0,0,0,0,0,0,0,0,0,32,0,0,0,0,0,0,0,0,0,0,0,24,24,24,24,16,16,16,16,24,16,16,16,16,16,16,16,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,0,1,1,1,1,3,3,3,3,3,3,7,7,7,7,7,7,6,6,6,6,4,12,12,12,12,28,28,28,28,28,28,28,28,28,28])
    
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
    
    myTank = Tank()
    myAmmo = Ammo(36, 35, 0.25)
    frame = 0
    title_screen = True
    game_over = False
    
    game_level = 1
    points = 0
    last_points = 0
    
    #keeps track of where each UFO is
    ufo_spots = [False, False, False, False, False, False, False]
    cow_spots = [False, False, False, False]
    UFOS = [UFO(0)]
    Cows = [Cow(), Cow()]
    
    #title screen animation vars
    ufo_bounce = True
    cow_shake = False
    text_x = 72
    
    thumby.display.setFPS(16) #Music FPS
    

    
    while 1:
        while title_screen:    
            thumby.display.fill(0)
            thumby.display.blit(bitmap_title, 0, 0, 72, 40, 0, 0, 0)
            
            if text_x > -6*len(news_text):
                thumby.display.drawText(news_text, text_x, 32, 0)
                text_x -= 3
            else:
                thumby.display.drawText("Press A", 15, 32, 0)
                
            cow_shake = not cow_shake
            if frame % 4 == 0:
                ufo_bounce = not ufo_bounce
            if ufo_bounce:
                thumby.display.blit(bitmap_ufo, 29, 2, 10, 7, 0, 0, 0)
            else:
                thumby.display.blit(bitmap_ufo, 29, 3, 10, 7, 0, 0, 0)
                
            if cow_shake:
                thumby.display.blit(bitmap_cow_title, 10, 20, 10, 7, 0, 1, 0)
                thumby.display.blit(bitmap_cow_title, 52, 20, 10, 7, 0, 0, 0)
            else:
                thumby.display.blit(bitmap_cow_title, 11, 20, 10, 7, 0, 1, 0)
                thumby.display.blit(bitmap_cow_title, 51, 20, 10, 7, 0, 0, 0)
                
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
                frame = 0
                thumby.display.setFPS(30) #Gameplay FPS
                title_screen = False
            else:
                thumby.display.update()
                frame += 1
        
        while not game_over:
            #UFO movement
            if frame % (120 - game_level*5) == 0:
                #attempt an abduction once in a while
                #becomes more frequent with level
                if game_level == 20 or random.randrange(0, 4 - game_level//5) == 0:
                    targeting_cow = random.choice(Cows)
                    if not targeting_cow.gone:
                        moving_ufo = random.choice(UFOS)
                        if not moving_ufo.targeting_cow:
                            moving_ufo.targetCow(targeting_cow)
                            ufo_spots[moving_ufo.pos] = False
                else:
                    moving_ufo = random.choice(UFOS)
                    if not moving_ufo.targeting_cow and not moving_ufo.exploded:
                     #mark current ufo spot as free
                        ufo_spots[moving_ufo.pos] = False
                    
                        new_pos = random.randrange(0,7)
                        while ufo_spots[new_pos]:
                            new_pos = random.randrange(0,7)
                    
                        #mark new ufo spot as taken
                        ufo_spots[new_pos] = True
                        moving_ufo.move(new_pos)
                
            #cow movement - random every 5 seconds
            if frame % 150 == 0:
                moving_cow = random.choice(Cows)
                
                cow_spots[moving_cow.pos] = False
                
                if moving_cow.targeted == False:
                    new_pos = random.randrange(0,4)
                    while cow_spots[new_pos]:
                        new_pos = random.randrange(0,4)
                    
                    cow_spots[new_pos] = True
                    moving_cow.move(new_pos)
                
            myTank.take_input()
            myAmmo.take_input(myTank, frame)
                
            thumby.display.fill(0)
            
            thumby.display.blit(bitmap_field, 0, 0, 72, 30, 0, 0, 0)
        
            #Screen update section
            myAmmo.update()
            
            for ufo in UFOS:
                points += ufo.getCol(myAmmo, ufo_spots, points)   
                ufo.update()
                
            for cow in Cows:
                cow.update(ufo_spots, game_level)
                
            myTank.update()
            
    
        
    
            thumby.display.update()
            frame += 1
            
            #game over condition
            if Cows[0].gone and Cows[1].gone and not Cows[0].targeted and not Cows[1].targeted:
                game_over = True
                
            #leveling
            if points % 5 == 0 and game_level < 20 and points != last_points: #every 5 hits
                game_level += 1
                last_points = points
                dialog("Level " + str(game_level), 2)
                
            #spawn more UFOs
            if game_level == 3 and len(UFOS) < 2:
                new_pos = random.randrange(0,7)
                while ufo_spots[new_pos]:
                    new_pos = random.randrange(0,7)
                UFOS.append(UFO(new_pos))
            if game_level == 7 and len(UFOS) < 3:
                new_pos = random.randrange(0,7)
                while ufo_spots[new_pos]:
                    new_pos = random.randrange(0,7)
                UFOS.append(UFO(new_pos))
            if game_level == 11 and len(UFOS) < 4:
                new_pos = random.randrange(0,7)
                while ufo_spots[new_pos]:
                    new_pos = random.randrange(0,7)
                UFOS.append(UFO(new_pos))
            
        #game over screen
        while game_over:
            thumby.display.fill(0)
            
            try:
                f = open("/Games/SpaceEvader/hs.txt")
                hs = int(f.read())
                f.close()
            except: #make default melody file
                f = open("/Games/SpaceEvader/hs.txt", "w")
                f.write(str(points))
                f.close()
                hs = points
                
            if points > hs:
                f = open("/Games/SpaceEvader/hs.txt", "w")
                f.write(str(points))
                f.close()
                hs = points
                
            score_str = "Score: " + str(points)
            
            
            hiscore_str = "Hi: " + str(hs)
            
            thumby.display.drawText("Game Over!", 6, 0, 1)
            thumby.display.drawText(score_str, 36-(len(score_str)*6)//2, 8, 1)
            thumby.display.drawText(hiscore_str, 36-(len(hiscore_str)*6)//2, 16, 1)
            
            thumby.display.drawFilledRectangle(0, 25, 71, 39, 1)
            thumby.display.drawText("A: Again", 12, 25, 0)
            thumby.display.drawText("B: Quit", 15, 33, 0)
            
            if thumby.buttonA.pressed():
                game()
            elif thumby.buttonB.pressed():
                thumby.reset()
            
            thumby.display.update()

thumby.display.fill(0)
dialog("SuperRiley64", 0.25)
thumby.audio.playBlocking(523, 100)
thumby.audio.playBlocking(1046, 400)
dialog("SuperRiley64", 0.75)
game()