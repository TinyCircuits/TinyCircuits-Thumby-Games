import thumby
import random
import math
import time
from collections import namedtuple, deque


# use namedtuples to simulate enums
ShipDirection = namedtuple("ship_direction", ("none", "left", "right", "up", "down"))
MissileDirection = namedtuple("ship_direction", ("forward", "left", "right"))
FireDirection = namedtuple("ship_direction", ("forward", "side"))

# BITMAP: width: 72, height: 40
game_logo1 = bytearray([0,0,224,240,24,24,24,240,224,0,0,248,248,0,0,0,0,0,24,24,248,248,24,24,0,0,248,248,152,152,24,24,0,0,248,248,224,192,128,248,248,0,0,0,0,176,104,216,104,176,0,0,0,0,0,0,0,0,0,0,0,16,152,92,22,222,22,92,152,16,0,0,
            0,0,31,31,3,3,3,31,31,0,0,31,31,24,24,24,0,0,24,24,31,31,24,24,0,0,31,31,25,25,24,24,0,0,31,31,0,1,3,31,31,0,0,0,0,0,0,0,0,0,0,0,0,6,29,11,29,6,0,0,0,3,0,0,0,3,0,0,0,3,0,0,
            0,0,3,3,255,255,3,3,0,0,255,255,28,56,112,255,255,0,0,31,127,224,128,224,127,31,0,0,252,254,99,99,99,254,252,0,0,14,31,51,51,51,227,195,0,0,3,3,255,255,3,3,0,0,252,254,135,3,3,135,254,252,0,0,255,255,28,56,112,255,255,0,
            0,0,3,3,3,3,3,3,0,0,3,3,0,0,0,3,3,0,0,0,0,1,3,1,0,0,0,0,3,3,0,0,0,3,3,0,0,195,35,35,195,3,67,1,0,192,35,35,35,3,35,35,224,32,32,1,195,35,35,195,1,224,32,32,227,3,32,32,224,35,35,0,
            0,0,0,127,73,73,54,0,34,0,0,127,73,73,65,0,99,20,8,20,99,0,65,65,127,65,65,0,1,1,127,1,1,0,0,0,0,15,1,1,15,0,4,0,0,8,9,9,6,0,0,0,15,0,0,0,15,1,1,15,0,15,1,1,14,0,0,0,15,0,0,0])

# BITMAP: width: 72, height: 40
game_logo2 = bytearray([0,0,224,240,24,24,24,240,224,0,0,248,248,0,0,0,0,0,24,24,248,248,24,24,0,0,248,248,152,152,24,24,0,0,248,248,224,192,128,248,248,0,0,0,0,48,232,88,232,48,0,0,0,0,0,0,0,0,0,0,0,16,24,148,94,22,94,148,24,16,0,0,
            0,0,31,31,3,3,3,31,31,0,0,31,31,24,24,24,0,0,24,24,31,31,24,24,0,0,31,31,25,25,24,24,0,0,31,31,0,1,3,31,31,0,0,0,0,0,0,0,0,0,0,0,0,22,13,27,13,22,0,0,0,0,3,0,0,0,0,0,3,0,0,0,
            0,0,3,3,255,255,3,3,0,0,255,255,28,56,112,255,255,0,0,31,127,224,128,224,127,31,0,0,252,254,99,99,99,254,252,0,0,14,31,51,51,51,227,195,0,0,3,3,255,255,3,3,0,0,252,254,135,3,3,135,254,252,0,0,255,255,28,56,112,255,255,0,
            0,0,3,3,3,3,3,3,0,0,3,3,0,0,0,3,3,0,0,0,0,1,3,1,0,0,0,0,3,3,0,0,0,3,3,0,0,195,35,35,195,3,67,1,0,192,35,35,35,3,35,35,224,32,32,1,195,35,35,195,1,224,32,32,227,3,32,32,224,35,35,0,
            0,0,0,127,73,73,54,0,34,0,0,127,73,73,65,0,99,20,8,20,99,0,65,65,127,65,65,0,1,1,127,1,1,0,0,0,0,15,1,1,15,0,4,0,0,8,9,9,6,0,0,0,15,0,0,0,15,1,1,15,0,15,1,1,14,0,0,0,15,0,0,0])
            
# BITMAP: width: 1, height: 1
small_star = bytearray([1])

# BITMAP: width: 7, height: 6
ship_none = bytearray([56,28,14,15,14,28,56])

# BITMAP: width: 7, height: 6
ship_left = bytearray([48,60,31,14,14,28,24])

# BITMAP: width: 7, height: 6
ship_right = bytearray([24,28,14,14,31,60,48])

# BITMAP: width: 7, height: 6
ship_forward = bytearray([28,30,15,7,15,30,28])

# BITMAP: width: 7, height: 6
ship_back = bytearray([56,28,12,6,12,28,56])

# BITMAP: width: 7, height: 7
ship_explosion1 = bytearray([73,42,28,127,28,42,73])

# BITMAP: width: 7, height: 7
ship_explosion2 = bytearray([54,85,99,0,99,85,54])

# BITMAP: width: 3, height: 3
missile_forward = bytearray([6,3,6])

# BITMAP: width: 3, height: 3
missile_left = bytearray([2,7,5])

# BITMAP: width: 3, height: 3
missile_right = bytearray([5,7,2])

# BITMAP: width: 5, height: 5
alien1a = bytearray([22,13,27,13,22])

# BITMAP: width: 5, height: 5
alien1b = bytearray([6,29,11,29,6])

# BITMAP: width: 5, height: 5
alien2 = bytearray([19,13,7,13,19])

# BITMAP: width: 5, height: 2
missiles3 = bytearray([3,0,3,0,3])

# BITMAP: width: 5, height: 2
missiles2 = bytearray([0,0,3,0,3])

# BITMAP: width: 5, height: 2
missiles1 = bytearray([0,0,0,0,3])

# BITMAP: width: 5, height: 2
missiles0 = bytearray([0,0,0,0,0])

# BITMAP: width: 8, height: 4
abduction_aliena = bytearray([8,12,10,15,11,14,12,8])

# BITMAP: width: 8, height: 4
abduction_alienb = bytearray([8,12,14,11,15,10,12,8])

# BITMAP: width: 8, height: 8
beam1 = bytearray([0,0,17,34,34,17,0,0])

# BITMAP: width: 8, height: 8
beam2 = bytearray([0,16,33,34,34,33,16,0])

# BITMAP: width: 8, height: 8
beam3 = bytearray([16,33,34,34,34,34,33,16])

# BITMAP: width: 8, height: 8
beam4 = bytearray([17,34,34,34,34,34,34,17])

# BITMAP: width: 8, height: 32
full_beam = bytearray(
    [
        0,0,17,34,34,17,0,0,
        0,16,33,34,34,33,16,0,
        16,33,34,34,34,34,33,16,
        17,34,34,34,34,34,34,17
    ]
)

# BITMAP: width: 8, height: 8
explosion1 = bytearray([0,0,36,24,24,36,0,0])

# BITMAP: width: 8, height: 8
explosion2 = bytearray([0,40,38,80,26,36,24,0])

# BITMAP: width: 8, height: 8
explosion3 = bytearray([84,169,38,209,26,36,154,101])

# BITMAP: width: 8, height: 8
explosion4 = bytearray([90,169,2,128,1,66,146,37])

# BITMAP: width: 8, height: 8
explosion5 = bytearray([70,129,0,128,1,0,129,69])

class Logo():
    
    def __init__(self):
        self.sprite = thumby.Sprite(72, 40, game_logo1+game_logo2, 0, 0, 0)
        self.frame_rate = 250
        self.timer = time.ticks_ms()
            
    def update(self, t0):
        if time.ticks_diff(self.timer, t0) <= 0:
            self.sprite.setFrame((self.sprite.getFrame() + 1) % 2)
            self.timer = time.ticks_add(t0, self.frame_rate)

class Explosion():
    
    def __init__(self):
        self.sprite = thumby.Sprite(8, 8, explosion1+explosion2+explosion3+explosion4+explosion5, 0, 0, 0)
        self.frame_rate = 100
        self.timer = time.ticks_ms()
        self.done = False
        
    def __lt__(self, other):
        return int(self.done) < int(other.done)
        
    def update(self, t0):
        if time.ticks_diff(self.timer, t0) <= 0:
            # Mark explosion as done
            if self.sprite.getFrame() == 4:
                self.done = True
                self.sprite.setFrame(0)
                return
            # Move sprite to next frame, reset timer
            if not self.done:
                self.sprite.setFrame(self.sprite.getFrame() + 1)
                self.timer = time.ticks_add(t0, self.frame_rate)

                
    def place(self, x, y):
        self.done = False
        self.timer = time.ticks_add(time.ticks_ms(), self.frame_rate)
        self.sprite.x = x
        self.sprite.y = y
        return self

class Star():
    
    def __init__(self, speed, x, y):
        self.sprite = thumby.Sprite(1, 1, small_star, x, y)
        self.frame_rate = speed * 100
        self.timer = time.ticks_ms()
        
    def __lt__(self, other):
        return self.sprite.y < other.sprite.y
    
    def move(self, t0):
        if time.ticks_diff(self.timer, t0) <= 0:
            self.timer = time.ticks_add(t0, self.frame_rate)
            self.sprite.y += 1
            
class Missile():
    
    missile_direction = MissileDirection(*range(3))
    fire_direction = FireDirection(*range(2))
    
    def __init__(self):
        self.sprite = thumby.Sprite(
            3, 3, missile_forward+missile_left+missile_right, 0, 0, 0
        )
        self.direction = Missile.missile_direction.forward
        self.alive = True
        self.move_timer = time.ticks_ms()
        self.frame_rate = 20
        
    def __lt__(self, other):
        return int(not self.alive) + int(self.out_of_bounds()) < int(not other.alive) + int(other.out_of_bounds())
        
    def orient(self, direction):
        self.direction = direction
        self.sprite.setFrame(self.direction)
        self.alive = True
        
    def move(self, t0):
        if time.ticks_diff(self.move_timer, t0) >= 0:
            return
        self.move_timer = time.ticks_add(t0, self.frame_rate)
        if self.direction == Missile.missile_direction.forward:
            self.sprite.y -= 1
        elif self.direction == Missile.missile_direction.left:
            self.sprite.x -= 1
        else:
            self.sprite.x += 1
            
    def out_of_bounds(self):
        return (
            self.sprite.y <= -self.sprite.height
            or self.sprite.x <= -self.sprite.width
            or self.sprite.x > thumby.display.width
        )

class MissileHUD():
    
    def __init__(self):
        self.sprite = thumby.Sprite(5, 2, missiles0+missiles1+missiles2+missiles3, thumby.display.width - 5, thumby.display.height - 2, 0)

    def update(self, num):
        self.sprite.setFrame(num)
            
class Ship():
    
    ship_direction = ShipDirection(*range(5))
    
    def __init__(self, max_missiles):
        self.sprite = thumby.Sprite(7, 6, ship_none+ship_left+ship_right+ship_forward+ship_back, thumby.display.width/2, thumby.display.height/2, 0)
        self.explosion_sprite = thumby.Sprite(7, 6, ship_explosion1+ship_explosion1+ship_explosion2+ship_explosion2, 0, 0)
        self.alive = True
        self.explosion_frames = 10
        self.xvelocity = 0
        self.yvelocity = 0
        self.missile_queue = deque((), max_missiles)
        for _ in range(max_missiles):
            self.missile_queue.append(Missile())
        self.move_timer = time.ticks_ms()
        self.frame_rate = 25
        
        
    def move(self, l, r, u, d, t0):
        if time.ticks_diff(self.move_timer, t0) >= 0:
            return
        self.move_timer = time.ticks_add(t0, self.frame_rate)
        self.sprite.setFrame(
            Ship.ship_direction.left if l
            else Ship.ship_direction.right if r
            else Ship.ship_direction.up if u 
            else Ship.ship_direction.down if d
            else Ship.ship_direction.none
        )
        self.xvelocity = -1 if l else 1 if r else 0
        self.yvelocity = -1 if u else 1 if d else 0
        self.sprite.x += self.xvelocity
        self.sprite.y += self.yvelocity
        
        if self.sprite.x < 0:
            self.sprite.x = 0
        if self.sprite.y < 0:
            self.sprite.y = 0
        if self.sprite.x > thumby.display.width - self.sprite.width:
            self.sprite.x = thumby.display.width - self.sprite.width
        if self.sprite.y > thumby.display.height - self.sprite.height:
            self.sprite.y = thumby.display.height - self.sprite.height
            
    def fire(self, direction):
        if direction == Missile.fire_direction.forward and len(self.missile_queue) > 0:
            new_missile = self.missile_queue.popleft()
            new_missile.orient(Missile.missile_direction.forward)
            new_missile.sprite.x = self.sprite.x + 2
            new_missile.sprite.y = self.sprite.y - 3
            return (new_missile,)
        elif direction == Missile.fire_direction.side and len(self.missile_queue) > 1:
            new_left_missile = self.missile_queue.popleft()
            new_left_missile.orient(Missile.missile_direction.left)
            new_left_missile.sprite.x = self.sprite.x - new_left_missile.sprite.width
            new_left_missile.sprite.y = self.sprite.y + 2
            new_right_missile = self.missile_queue.popleft()
            new_right_missile.orient(Missile.missile_direction.right)
            new_right_missile.sprite.x = self.sprite.x + self.sprite.width - 1
            new_right_missile.sprite.y = self.sprite.y + 2
            return (new_left_missile, new_right_missile,)
        return tuple()
        
class BasicAlien():
    
    def __init__(self):
        self.sprite = thumby.Sprite(5, 5, alien1a+alien1b, 0, 0)
        self.amplitude = random.randint(3, 7)
        self.centerx = 0
        self.centery = 0
        self.move_timer = time.ticks_ms()
        self.speed = 0
        self.alive = True
        self.move_function = lambda x, y: (x + 1, y + 0)
        
    def __lt__(self, other):
        return int(not self.alive) + int(self.out_of_bounds()) < int(not self.alive) + int(other.out_of_bounds())
        
    def score(self):
        return 20 - int(self.speed/10)
        
    def initialize(self, x, y, s, mf):
        self.sprite.x = self.centerx = x
        self.sprite.y = self.centery = y
        self.speed = s
        self.move_function = mf
        
    def move(self, t0):
        if time.ticks_diff(self.move_timer, t0) >= 0:
            return
        self.move_timer = time.ticks_add(t0, self.speed)
        self.sprite.setFrame((self.sprite.getFrame() + 1) % 2)
        self.sprite.x, self.sprite.y = self.move_function(self.sprite.x, self.sprite.y)

    # Check for collision with another sprite
    def collides_with(self, other):
        return (
            other.x - self.sprite.width <= self.sprite.x <= other.x + other.width
            and other.y - self.sprite.height <= self.sprite.y <= other.y + other.height
        )
        
    def out_of_bounds(self):
        return (
            self.sprite.y > self.sprite.height + thumby.display.height
            or self.sprite.x > thumby.display.width
            or self.sprite.x < -self.sprite.width
        )
        
        
    # self.sprite.x = self.centerx + self.amplitude*math.sin(self.sprite.y*0.05*2*math.pi)
         