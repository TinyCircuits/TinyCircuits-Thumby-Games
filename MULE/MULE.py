# MULE.PY
# (c) Lauren32 2024
# Once upon a time, a guy made a game like this for personal computers. 
# Now, he is one of the 10 richest people in the world.
# Could this work for me? Only time will tell

import thumby
import time
import random
import gc

LANE1_Y = const(4) # Lane 2 X pos
LANE2_Y = const(19) # Lane 2 Y pos
LINE_Y = const(15) # Center line Y pos

# Draw a centered text box
def textbox(text,y,large=False):
    if large == True:
        font_w = 5
        font_h = 7
        thumby.display.setFont("/lib/font5x7.bin",font_w,font_h,1)
    else:
        font_w = 3
        font_h = 5
        thumby.display.setFont("/lib/font3x5.bin",font_w,font_h,1)
    w = len(text)*(font_w+1)+(font_w+1)
    x = round(36-(len(text)/2)*(font_w+1))-2
    thumby.display.drawFilledRectangle(x,y,w,font_h+4,0)
    thumby.display.drawRectangle(x,y,w,font_h+4,1)
    thumby.display.drawText(text,x+3,y+2,1)

class Car():
    WIDTH = 12
    def __init__(self):
        self.x = 5
        self.lane = 1 # lane 1 = high, 0 = low
        
    def reset(self):
        self.__init__()

class Mule():
    def __init__(self,x=72):
        self.x = x
        self.lane = random.randint(0,1) # lane 1 = high, 0 = low
        self.active = False

    def move(self):
        if self.active:
            self.x -= 1
            
    def reset(self):
        self.x = 72
        self.lane = random.randint(0,1)

class Game:
    # BITMAP: width: 12, height: 8
    bmp_car = bytearray([0,24,189,255,189,60,60,189,231,189,24,0])

    # BITMAP: width: 12, height: 8
    bmp_mule = bytearray([32,16,248,24,248,56,56,249,30,255,12,0])
    # BITMAP: width: 6, height: 4
    bmp_mule_ul = bytearray([0,0,8,8,8,8])
    bmp_mule_ul_mask = bytearray([15,15,7,7,7,7])
    bmp_mule_ur = bytearray([8,9,14,15,12,0])
    bmp_mule_ur_mask = bytearray([7,6,1,0,3,15])
    bmp_mule_ll = bytearray([2,1,15,1,15,3])
    bmp_mule_ll_mask = bytearray([13,14,0,14,0,12])
    bmp_mule_lr = bytearray([3,3,15,1,15,0])
    bmp_mule_lr_mask = bytearray([12,12,0,14,0,15])

    def __init__(self):
        self.score = 0
        self.hiscore = 0
        self.mules = [Mule()]
        self.mules[0].active = True
        self.car = Car()
        self.g_line_x = 5
        
    def reset(self):
        self.score = 0
        self.car.reset()
        self.mules = [Mule()] # Delete and recreate mules
        self.mules[0].active = True

    def game_over(self):
        thumby.display.fill(0)
        textbox("Game Over",5,True)
        thumby.display.drawText(f"Score: {self.score}",5,22,1)
        thumby.display.drawText(f"High: {self.hiscore}",5,31,1)
        thumby.display.update()
        self.score = 0
        while not thumby.inputJustPressed():
            pass
    
    # Detect a collision from the front.
    # Returns -1 if no collision or mule number
    def collision_detect_front(self):
        for i in range(len(self.mules)):
            if self.mules[i].lane == 1:
                y = LANE1_Y + 4
            else:
                y = LANE2_Y + 4
            
            if thumby.display.getPixel(self.mules[i].x,y):
                return i
        
        return -1
    
    # Detect a collision when switching lanes.
    # Returns -1 if no collision or mule number
    def collision_detect_side(self):
        for i in range(len(self.mules)):
            if self.mules[i].lane == 1:
                y = LANE2_Y + 4
            else:
                y = LANE1_Y + 4
            
            if thumby.display.getPixel(self.mules[i].x,y) or thumby.display.getPixel(self.mules[i].x+10,y):
                return i
        
        return -1

    def mule_explode(self, mule_num):
        if self.mules[mule_num].lane == 1:
                y1 = LANE1_Y
        else:
                y1 = LANE2_Y
        y2 = y1 + 4
        x1 = self.mules[mule_num].x
        x2 = self.mules[mule_num].x + 6
        
        for i in range(9):
            if i>0:
                thumby.display.blit(Game.bmp_mule_ul,x1-i,y1-i,6,4,0,0,0)
                thumby.display.blit(Game.bmp_mule_ur,x2+i,y1-i,6,4,0,0,0)
                thumby.display.blit(Game.bmp_mule_ll,x1-i,y2+i,6,4,0,0,0)
                thumby.display.blit(Game.bmp_mule_lr,x2+i,y2+i,6,4,0,0,0)
                thumby.display.update()
            
            thumby.audio.playBlocking(random.randint(500,1000),200)

            thumby.display.blit(Game.bmp_mule_ul_mask,x1-i,y1-i,6,4,1,0,0)
            thumby.display.blit(Game.bmp_mule_ur_mask,x2+i,y1-i,6,4,1,0,0)
            thumby.display.blit(Game.bmp_mule_ll_mask,x1-i,y2+i,6,4,1,0,0)
            thumby.display.blit(Game.bmp_mule_lr_mask,x2+i,y2+i,6,4,1,0,0)

            thumby.display.drawLine(0,LANE1_Y-2,72,LANE1_Y-2,1)
            thumby.display.drawLine(0,LANE2_Y+9,72,LANE2_Y+9,1)
            self.draw_score()            
            thumby.display.update()
        textbox("BANG!",13)
        thumby.display.update()
        
    def draw_road(self):
        thumby.display.drawLine(0,LANE1_Y-2,72,LANE1_Y-2,1)
        thumby.display.drawLine(0,LANE2_Y+9,72,LANE2_Y+9,1)

        for x in range(self.g_line_x,70,10):
            thumby.display.drawLine(x,LINE_Y,x+4,LINE_Y,1)
        self.g_line_x -= 1
        if self.g_line_x < -5:
            self.g_line_x = 5
    
    def draw_actors(self):
        if self.car.lane == 1:
            car_y = LANE1_Y
        else:
            car_y = LANE2_Y
        thumby.display.blit(Game.bmp_car,self.car.x,car_y,12,8,0,0,0)
        
        for mule in self.mules:
            if mule.lane == 1:
                mule_y = LANE1_Y
            else:
                mule_y = LANE2_Y
            
            thumby.display.blit(Game.bmp_mule,mule.x,mule_y,12,8,0,0,0)
    
    # This micropython doesn't have abc, but this is intended to be overriden
    def draw_score(self):
        pass
        
    def draw(self):
        thumby.display.fill(0)
        self.draw_road()
        self.draw_actors()
        self.draw_score()

# Classic game mode
class GameA(Game):
    def __init__(self):
        super().__init__()
        self.mule_score = 0

    def draw_score(self):
        thumby.display.drawText(f"Driver:{self.score}  Mule:{self.mule_score}",3,32,1)

    # Main game loop
    def start(self):
        thumby.display.setFont("/lib/font3x5.bin",3,5,1)
        while True:
            self.draw()
            thumby.display.update()
            if thumby.buttonL.justPressed():
                break
            elif thumby.actionJustPressed():
                collision = self.collision_detect_side()
                self.car.lane = int(not self.car.lane)
                self.draw()
                thumby.display.update()
                thumby.audio.play(1000,200)
            else:
                self.mules[0].move()
                if self.mules[0].x == 5:
                    self.car.x += 3
                    self.mules[0].reset()
                    self.mules[0].lane = random.randint(0,1)
                    continue
                elif self.car.x > 40:
                    self.score += 1
                    self.car.x = 5
                    textbox("Mule loses!",13)
                    thumby.display.update()
                    time.sleep(1)
                    continue
                else:
                    collision = self.collision_detect_front()
            
            if collision != -1:
                self.mule_explode(0)
                self.mule_score += 1
                self.mules[0].reset()
                self.car.reset()
                time.sleep(1)
        
        try:
            s = round(self.score/self.mule_score) # score is a ratio
        except ZeroDivisionError:
            s = self.score
        self.score = s
        self.mule_score = 0
        self.game_over()
        self.reset()
        return

# New game mode
class GameB(Game):
    def __init__(self):
        super().__init__()
        self.delay = 0.020 # game speed for difficulty
        
    def draw_score(self):
        thumby.display.drawText(f"Score: {self.score}",5,34,1)
    
    # Return true if there are no mules on the road
    def road_empty(self):
        empty = True
        for mule in self.mules:
            if mule.x > 0 and mule.x < 70:
                empty = False
        return empty

    # Line mules back up at regular intervals        
    def reset_mules(self):
        x = 72
        for i in range(len(self.mules)):
            self.mules[i].lane = random.randint(0,1)
            self.mules[i].active = True
            self.mules[i].x = x
            x += 36

    # Main game loop
    def start(self):
        thumby.display.setFont("/lib/font3x5.bin", 3, 5, 1)
        add_mules = True
        while True:
            thumby.display.update()
            if thumby.actionJustPressed():
                collide = self.collision_detect_side()
                self.car.lane = int(not self.car.lane)
                self.draw()
                thumby.display.update()
                thumby.audio.play(1000,200)
            elif thumby.buttonL.pressed():
                break
            else:
                for mule in self.mules:
                    mule.move()
                    if mule.x == -11:
                        print(f"mule count: {len(self.mules)}")
                        self.score += 1
                        # Update difficulty on certain levels
                        if (self.score % 10 == 0) and self.delay > 0.001:
                            self.delay -= 0.005
                        if self.car.x < 30 and (self.score % 3 == 0):
                            self.car.x += 1
                        if self.score % 5 == 0:
                            if len(self.mules) < 4:
                                self.mules.append(Mule())
                        # At 4 mules, stop adding more and start looping
                        if add_mules == False:
                            mule.x = self.mules[-1].x + 36
                            mule.lane = random.randint(0,1)
                            self.mules.append(self.mules[0])
                            self.mules = self.mules[1:]
                        elif self.road_empty():
                            self.reset_mules()
                            if len(self.mules) == 4:
                                add_mules = False
                collide = self.collision_detect_front()
            
            if collide != -1:
                self.mule_explode(collide)
                time.sleep(1)
                break

            self.draw()
            time.sleep(self.delay)
            
        if self.score > self.hiscore:
            self.hiscore = self.score
        self.game_over()
        self.reset()
        return
            
# Display title screen
def title_screen(index):
    thumby.display.setFont("/lib/font5x7.bin",5,7,1)
    thumby.display.fill(0)
    thumby.display.drawText("MULE.PY",18,2,1)
    thumby.display.drawText("Game  A",18,13,1)
    thumby.display.drawText("Game  B",18,22,1)
    thumby.display.drawText("Quit",18,31,1)
    bullet_y = 0
    if index == 0:
        bullet_y = 13
    elif index == 1:
        bullet_y = 22
    else:
        bullet_y = 31
    thumby.display.drawText("*",3,bullet_y,1)
    thumby.display.update()     
    
# Dsiplay about screen
def about_screen():
    thumby.display.setFont("/lib/font5x7.bin",5,7,1)
    thumby.display.fill(0)
    thumby.display.drawText("MULE.PY 1.0",2,2,1)
    thumby.display.drawText("Lauren32",2,13,1)
    thumby.display.drawText("2024",2,22,1)
    thumby.display.drawText("CC BY-SA3.0",2,31,1)
    thumby.display.update()

game_a = GameA()
game_b = GameB()
menu_index = 0
thumby.display.setFPS(60)
gc.enable() # enable garbage collection

while True:
    title_screen(menu_index)
    if thumby.buttonU.justPressed() and menu_index > 0:
        menu_index -= 1
    elif thumby.buttonD.justPressed() and menu_index < 2:
        menu_index += 1
    elif thumby.buttonL.justPressed():
        about_screen()
        while not thumby.inputJustPressed():
            pass
    elif thumby.actionJustPressed():
        if menu_index == 0:
            game_a.start()
        elif menu_index == 1:
            game_b.start()
        elif menu_index == 2:
            thumby.reset()
            
            

