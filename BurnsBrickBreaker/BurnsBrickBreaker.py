import time
import math

import thumby as tb
from thumby import display as dp

dp.setFPS(30)


def main():
    views = {
    'game':     GameView(),
    'lose':     LoseView(),
    'start':    StartView(),
    'win' :     WinView(),
    'instruct': InstructView()
    }
    current = 'start'
    once = True
    while(True):
        dp.fill(0)
        current = views[current].show()
        once = update_score(current,views, once)
        dp.update()


def update_score(current, views, once):
    if current == 'win':
        views[current].score += views['game'].score
        views['game'].reload()
        return once
    elif current == 'lose' and once:
        views['win'].score += views['game'].score
        views[current].score = views['win'].score
        views['win'].score = 0
        return False
    elif current == 'game':
        return True


class View:
    def __init__(self):
        pass
    
    def show(self):
        pass
    
    def draw_set(self, headline, first, second, third):
        dp.drawText(headline, 0, 0, 1)
        dp.drawLine(0, 8, 62, 8, 1)
        dp.drawText(first, 0, 12, 1)
        dp.drawText(second, 0, 21, 1)
        dp.drawText(third, 0, 30, 1)
            

class LoseView(View):
    def __init__(self):
        View.__init__(self)
        self.score = 0
        
    def show(self):
        headline = "Score: " + str(self.score)
        self.draw_set(headline, "Replay?", "Left: No", "A: Yes")
        if tb.buttonA.pressed() or tb.buttonR.pressed(): return 'game'
        elif tb.buttonL.pressed(): tb.reset()
        return 'lose'

class WinView(View):
    def __init__(self):
        View.__init__(self)
        self.score = 0

    def show(self):
        return 'game'
        
class InstructView(View):
    def show(self):
        # Game Instructions
        self.draw_set('Game Instr.', "Hit Ball &", "Break Bricks", '')
        dp.update()
        time.sleep(2)
        return 'game'

        
class StartView(View):
    
    def __init__(self):
        View.__init__(self)
        # BITMAP: width: 72, height: 30
        title_map = bytearray([0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,62,42,42,62,0,0,62,32,32,62,0,0,62,10,26,46,0,0,62,12,16,62,0,0,7,0,46,42,58,0,0,0,0,0,0,0,0,0,
           255,254,252,252,252,254,255,255,255,255,254,4,4,180,182,7,7,255,7,6,52,52,52,134,255,255,7,7,254,4,4,228,230,231,231,255,7,6,28,76,228,246,255,255,255,255,254,252,252,124,126,127,127,127,127,126,124,124,124,126,127,99,99,99,126,124,124,124,254,255,255,255,
           255,255,255,255,255,255,255,255,255,255,255,12,12,109,109,12,12,255,12,12,111,111,110,12,253,255,12,12,79,76,204,252,12,12,108,111,12,12,255,14,12,61,159,207,239,255,15,15,79,76,205,253,13,13,109,109,109,13,253,253,253,253,253,253,253,253,253,252,255,255,255,255,
           63,31,15,15,15,31,63,63,63,63,31,8,8,11,27,56,56,63,24,8,14,30,60,57,59,31,8,8,9,25,57,63,56,24,15,15,8,24,63,56,56,30,12,9,11,31,56,56,57,25,9,15,8,24,62,62,60,25,11,15,15,31,63,63,63,31,15,15,15,31,63,63])
        
        self.title = tb.Sprite(72,30, title_map, 0,0)
    
    def show(self):
        dp.drawSprite(self.title)
        dp.drawText("Load ...", 0 , 30, 1)
        dp.update()
        time.sleep(2)
        return 'instruct'


class GameView(View):
    def __init__(self):
        screen = Screen()
        self.pad  = PadWidget(screen)
        self.ball = BallWidget(self, self.pad, 30, 10)
        self.reload()

    def reload(self):
        self.bricks = self.get_bricks()
        self.ball.reset(self.bricks)
        self.pad.reset()
        self.lost = False
        self.score = 0

    @staticmethod
    def get_bricks():
        bricks = []
        for i in range(0, 10):
            bricks.append(Brick(1 + (i*7), 1))
            bricks.append(Brick(1 + (i*7), 5))
            bricks.append(Brick(1 + (i*7), 9))
        return bricks
        
    def game_over(self):
        self.lost = True
    
    def show(self):
        if self.lost: self.reload()
        
        self.ball.move()
        self.pad.move()
    
        for brick in self.bricks:
            if brick.lives > 0: brick.update()
            else:
                self.score += 1
                self.bricks.remove(brick)
        
        if self.lost: 
            time.sleep(1)
            return 'lose'
        elif len(self.bricks) == 0: return 'win'
        return 'game'


class Screen:
    def __init__(self):
        self.__w = dp.width
        self.__h = dp.height
        self.__b = 127
    
    @property
    def x(self):
        return 0
    
    @property    
    def y(self):
        return 0
        
    @property
    def width(self):
        return self.__w
        
        
    @property
    def height(self):
        return self.__h
    
    @property
    def right(self):
        return self.x + self.width
        
    @property
    def bottom(self):
        return self.y + self.height
    
        
    @property
    def brightness(self):
        return self.__b
    
    
    @brightness.setter
    def brightness(self, val):
        if 0 <= val < 128:
            self.__b = val
            dp.brightness(val)
        
            
    def contains(self, wd):
        return (wd.x > -1 and wd.right < self.__w and \
                wd.y > -1 and wd.bottom < self.__h)
                


class Widget(tb.Sprite):
    
    def __init__(self, width, height, bitmapData, x=0, y=0, key=-1, mirrorX=0, mirrorY=0):
        tb.Sprite.__init__(self, width, height, bitmapData, x, y, key, mirrorX, mirrorY)

    @property
    def right(self):
        return self.x + self.width
        
    @right.setter
    def right(self, val):
        self.x = val - self.width
        
    @property
    def bottom(self):
        return self.y + self.height
        
    @bottom.setter
    def bottom(self, val):
        self.y = val - self.height
        
    @property
    def center_x(self):
        return int(self.x + self.width/2)
        
    @center_x.setter
    def center_x(self, val):
        self.x = int(val - self.width/2)
        
    @property
    def center_y(self):
        return int(self.y + self.height/2)
        
    @center_y.setter
    def center_y(self, val):
        self.y = int(val - self.height/2)
        

    
    def move(self, x=0, y=0):
        self.x += x
        self.y += y
        
        self.update()
    
    def collides(self, wd):
        return (wd.x < self.right and wd.right > self.x and \
                wd.y < self.bottom and wd.bottom > self.y)
                
    def update(self):
        dp.drawSprite(self)
        
        
class BallWidget(Widget):
    def __init__(self, view, pad, x=0, y=0):
        # BITMAP: width: 4, height: 4
        ballMap = bytearray([6,15,15,6])
        Widget.__init__(self, 4, 4, ballMap, x, y, key=0)
        self.view = view
        self.screen = pad.screen
        self.pad = pad
        self.bricks = []
        self.speed = 1
        self.dir_x = 1
        self.dir_y = 2
    
    def reset(self, bricks):
        self.bricks = bricks
        self.speed = 1
        self.dir_x = 0
        self.dir_y = -3
        self.x = 36
        self.y = 30
        
    def __bounce(self):
      
        if self.collides(self.pad):
            return self.__bounce_pad()
        
        for brick in self.bricks:
            if self.collides(brick):
                wall = self.__bounce_wall(brick)
                brick.damage()
                if wall != 0: return wall
            
        return self.__bounce_wall(self.screen)
       
    def __bounce_pad(self): 
        sum = int(math.fabs(self.dir_x) + math.fabs(self.dir_y)) # save entire speed
        new_x = int((self.center_x - self.pad.center_x)/(self.pad.width*0.5)*sum) # relate x speed to relation between ball and pad mid
        sign_x, sign_y = math.copysign(1, new_x), math.copysign(1, self.dir_y) # save signs
        if new_x*sign_x == sum: new_x -= sign_x # x cannot have the entire speed. Otherwise it will bounce horizontally forever.
        self.dir_x  = new_x
        self.dir_y  = (sum - math.fabs(new_x)) * -1 * sign_y # assign remaining speed and invert y
        return 5 
     
     
    def __bounce_wall(self, obj):
        wall = self.hit_wall(obj)
        if 0 < wall < 3: self.dir_x *= -1
        elif wall > 2: self.dir_y *= -1
        return wall
    
    def move(self):
        x, y = self.x, self.y
        self.x += self.dir_x*self.speed
        self.y += self.dir_y*self.speed
        bounce = self.__bounce()
        if  bounce > 0:
            self.x, self.y = x + self.dir_x*self.speed, y + self.dir_y*self.speed
        if bounce == 6:
            self.view.game_over()
        self.update()
        
    def hit_wall(self, obj ):
        # None, Left, Rigth, Top, Bottom
        if self.x < obj.x: wall = 1
        elif self.right > obj.right: wall = 2
        elif self.y < obj.y: wall = 3
        elif self.bottom > obj.bottom: wall = 4
        else:
            wall = 0
        if obj is self.screen and wall == 4: wall = 6
        return wall
        
class PadWidget(Widget):
    def __init__(self, screen):
        # BITMAP: width: 25, height: 3
        padMap = bytearray([2,3,5,5,5,5,5,5,5,5,5,5,5,5,5,5,5,5,5,5,5,5,7,3,2])
        Widget.__init__(self, 25, 3, padMap, screen.width/2 - 5, screen.height - 4, key=0)
        self.screen = screen
        self.speed = 5
        self.is_rebounced = False
        
    def reset(self):
        self.is_rebounced = False
        self.center_x = self.screen.width/2
        
    def move(self):
        x = 0
        if not tb.buttonA.pressed(): self.is_rebounced = True
        if tb.buttonL.pressed():    x = self.speed *-1
        elif (tb.buttonR.pressed() or tb.buttonA.pressed()) and self.is_rebounced:  x = self.speed
        self.x = max(min(self.x + x, self.screen.width-self.width), self.screen.x)
        
        
        self.update()
            

class Brick(Widget):
    def __init__(self, x, y, lives=3):
        # BITMAP: width: 6, height: 3
        fullMap         =   [7,7,7,7,7,7]
        batteredMap     =  [3,6,6,3,3,6]
        destroyedMap    =  [1,4,4,3,1,6]
        metalMap        =  [7,5,5,5,5,7]
        frames = []
        for lst in (fullMap, batteredMap, destroyedMap, metalMap):
            frames.extend(lst)
        
        Widget.__init__(self, 6, 3, bytearray(frames), x, y, key=0)
        self.lives = lives
        self.setFrame(0)
        
    def damage(self, isFire=False):
        self.lives -=1
        self.setFrame(3-self.lives)
            
main()
    
    