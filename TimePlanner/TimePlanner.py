#####
###. TimePlanner v1.1
###. Developed by N0P3

import thumby
from sys import path
import time
import random
path.append("/Games/TimePlanner")
import events


#Spr = thumby.Sprite(16, 16, "/sprite0.bin", 10, 3) 

# Increase this to make the flutter animation change frames faster
thumby.display.setFPS(30) 

WHITE=1
BLACK=0

BOX_WIDTH=5
BOX_HEIGHT=5

# BITMAP: width: 8, height: 8
bitmap6 = bytearray([62,28,8,0,0,0,0,0])
# BITMAP: width: 8, height: 8
heart = bytearray([6,15,31,62,31,15,6,0])
# BITMAP: width: 8, height: 8
broken_heart = bytearray([6,9,17,34,17,9,6,0])

def draw_lives(x,y,n,total):
    for i in range(total):
        if n>0:
            thumby.display.blit(heart,x,y,7,6,0,0,0)
            n-=1
        else:
            thumby.display.blit(broken_heart,x,y,7,6,0,0,0)
        x+=8

    

def draw_empty_box(x,y):
    thumby.display.drawFilledRectangle(x, y, BOX_WIDTH, BOX_HEIGHT, BLACK)

def draw_box(x,y):
    thumby.display.drawRectangle(x, y, BOX_WIDTH, BOX_HEIGHT, WHITE)
    
def draw_filled_box(x,y):
    thumby.display.drawFilledRectangle(x, y, BOX_WIDTH, BOX_HEIGHT, WHITE)

def draw_chosen_box(x,y):
    draw_empty_box(x,y)
    draw_box(x,y)
    thumby.display.setPixel(x+int(BOX_WIDTH/2), y+int(BOX_HEIGHT/2), WHITE)
    
def draw_vertical_dashed_line(x,y,length,dash_len,color=WHITE):
    if color == 1:
        black=0
        white=1
    else:
        white=0
        black=1
        
    final_y=y+length
    #thumby.display.drawLine(x,y,x,final_y,black)
    
    end_y=y
    for i in range(int(length/dash_len)):
        end_y+=dash_len
        if end_y>final_y:
            end_y=final_y
        
        thumby.display.drawLine(x,y+(i*dash_len),x,end_y,white)
        
        white,black=black,white


class Timer:
    def __init__(self,action_interval):
        self.action_interval=action_interval
        self.last_action_time = time.ticks_ms()
        
    def reset(self):
        self.last_action_time = time.ticks_ms()

    def time_up(self):
        current_time = time.ticks_ms()
        return time.ticks_diff(current_time, self.last_action_time) >= self.action_interval

BOX = 0
FILLED = 1
CHOSEN = 2

class Event:
    def __init__(self,dataset):
        self.dataset=dataset
    
    def height(self):
        return len(self.dataset)
    
    def draw(self,x,y,mode):
        self.draw_with_scale(x,y,mode,BOX_WIDTH,BOX_HEIGHT)
            
    def draw_with_scale(self,x,y,mode,width,height):
        i=0
        for line in self.dataset:
            j=0
            for box in line:
                final_x=x+j*width
                final_y=y+i*(height)
                if box == 1:
                    if mode == BOX:
                       draw_box(final_x,final_y) 
                    elif mode == FILLED:
                        draw_filled_box(final_x,final_y)
                    elif mode == CHOSEN:
                        draw_chosen_box(final_x,final_y)
                    else:
                        print("Unknown Box Mode '",mode,"'")
                j+=1
                
            i+=1        
        
    def get_event_positions(self):
        positions={}
        y=0
        for line in self.dataset:
            x=0
            for item in line:
                if item == 1:
                    if y in positions:
                        positions[y].append(x)
                    else:
                        positions[y]=[x]
                x+=1
            y+=1
        return positions

class Calendar:
    def __init__(self,line_nums,line_length,preload=5):
       
        self.line_nums=line_nums
        self.deadline=1
        self.item_nums=14
        
        self.current_px=self.deadline+preload
        self.current_py=0
        self.current_index=0
        
         #init road
        self.road=[]
        for i in range(self.line_nums):
            line=[]
            current_preload=preload
            for j in range(line_length):
                if current_preload>0:
                    line.append(1)
                    current_preload-=1
                else:
                    line.append(0)
            self.road.append(line)
            
        
    
    
    def move_on(self):
        c.current_index+=1
        ok=True
        for line in self.road:
            if line[c.current_index]==0:
                ok=False
                break
        return ok
        
    
    def plan_event(self,event: Event):
        positions=event.get_event_positions()
        
        ok=True
        for y in positions:
            for x in positions[y]:
                final_x,final_y=self.current_index+self.current_px+x,self.current_py+y
                if self.road[final_y][final_x]!=0:
                    ok=False
                    
        if ok:
            for y in positions:
                for x in positions[y]:
                    final_x,final_y=self.current_index+self.current_px+x,self.current_py+y
                    print("(",x,",",y,") -> ","(",final_x,",",final_y,")")
                    self.road[final_y][final_x]=1
        
        return ok

    def draw(self,x,y,chosen_event: Event):
        
        calendar_x=x
        calendar_y=y+BOX_HEIGHT
        
        thumby.display.drawRectangle(
            calendar_x,
            calendar_y,
            calendar_x+self.item_nums*BOX_WIDTH,
            self.line_nums*BOX_HEIGHT,
            WHITE)
        
        dataset=[]
        for l in self.road:
            line=l[self.current_index:self.current_index+self.item_nums]
            dataset.append(line)
        e=Event(dataset)
        chosen_event.draw(x+self.current_px*BOX_WIDTH,calendar_y+self.current_py*BOX_HEIGHT,CHOSEN)
        e.draw(calendar_x,calendar_y,FILLED)
        draw_vertical_dashed_line(x+self.deadline*BOX_WIDTH,y,y+(self.line_nums+2)*BOX_HEIGHT,1)


        
        
        
def random_event(datasets):
    return Event(random.choice(events.Datasets))




preload=4
interval=3000
c=Calendar(3,50,preload)
t=Timer(interval)
e=random_event(events.Datasets)
next_event=random_event(events.Datasets)
score=0
lives=3
win=False
game_over=False
exit_timer=Timer(3000)
thumby.display.setFont("/lib/font3x5.bin",3,5,WHITE)
def game_update():
    global score
    global game_over
    global preload
    global interval
    global t
    global e
    global next_event
    global lives
    global win
    c.draw(1,2,e)
    e.draw_with_scale(4,31,CHOSEN,4,4)
    #thumby.display.blit(bitmap6,0,30,3,6,0,0,0)
    thumby.display.drawText("next:",30,33,WHITE)
    next_event.draw_with_scale(50,31,CHOSEN,4,4)
    thumby.display.drawText("Score:"+str(score),35,1,WHITE)
    draw_lives(47,23,lives,3)
    #thumby.display.fill(1)
    #thumby.display.drawSprite(Spr)
    #Spr.setFrame(Spr.currentFrame+1)
    
    #e=Event(events.CubeEvent)
    # e.draw(0,0,EMPTY)
    if t.time_up():
        if not c.move_on():
            print("Oops!")
            lives-=1
            if lives<=0:
                game_over=True
                exit_timer.reset()
        else:
            preload-=1
            if preload<=0:
                score+=1
                interval-=0
                t=Timer(interval)
            print("Score:",score)
        if c.current_index==35:
            game_over=True
            win=True
            exit_timer.reset()
        t.reset()
    
    if thumby.buttonR.justPressed():
        print("right")
        c.current_px+=1
        
    if thumby.buttonL.justPressed():
        print("left")
        c.current_px-=1
        if c.current_px<c.deadline:
            c.current_px=c.deadline
            
    if thumby.buttonU.justPressed():
        print("up")
        c.current_py-=1
        if c.current_py<0:
            c.current_py=0      
       
    if thumby.buttonD.justPressed():
        print("down")
        c.current_py+=1
              
            
    if thumby.buttonA.justPressed():
        print("A")
        if c.plan_event(e):
            e=next_event
            next_event=random_event(events.Datasets)
        else:
            print("Can't place event here")
    
    if c.current_py+e.height()>c.line_nums:
        c.current_py-=1

while(True):
    thumby.display.fill(0)
    if game_over:
        thumby.display.fill(0)
        thumby.display.setFont("/lib/font5x7.bin",5,7,WHITE)
        if win:
            thumby.display.drawText("YOU WIN",14,10,1)
            thumby.display.setFont("/lib/font3x5.bin",3,5,WHITE)
            thumby.display.drawText("Thanks for playing my game and reading my code.",1,22,1)
        else:
            thumby.display.drawText("Game Over",10,10,1)
            thumby.display.setFont("/lib/font3x5.bin",3,5,WHITE)
            thumby.display.drawText("Your Score:"+str(score),11,20,WHITE)
        
        if exit_timer.time_up():
            if thumby.buttonA.justPressed() or thumby.buttonB.justPressed():
                print("Exit")
                break
    else:
        game_update()
    # draw_box(thumby.display.width-20,thumby.display.height-6)
    # draw_filled_box(thumby.display.width-13,thumby.display.height-6)
    # draw_chosen_box(thumby.display.width-6,thumby.display.height-6)
    thumby.display.update()
