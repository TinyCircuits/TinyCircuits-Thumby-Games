# https://github.com/TinyCircuits/tinycircuits.github.io
# https://github.com/TinyCircuits/TinyCircuits-Thumby-Games

import thumby
from gc import collect
from machine import reset
from random import choice
from random import random
from random import randrange
from time import time
from time import ticks_ms
from time import ticks_diff
from math import sin

class Const():
    menu=1
    settings=2
    help=3
    credits=4
    newgame=5
    newinfo=6
    newstory=7
    genlevel=8
    explore=9
    fight=10
    items=11
    spells=12
    stairs=13
    gameover=14
    gamewon=15
    quit=16
    
class Element():
    def __init__(self,v,c,l=None,dy=0):
        self.var=v
        self.callback=c
        self.callbacklong=l
        self.dy=dy
        self.state=None
        self.time=None
class Callback():
    def __init__(self,f,p=None):
        self.func=f
        self.params=p
    def execute(self):
        self.func(self.params) if self.params else self.func()

class States():
    def __init__(self):
        self.active=True
        self.current=0
        self.time=time()
        self.elements=[]
    def add(self,i,c,l=None):
        self.elements.append(Element(i,c,l))
    def update(self):
        for e in self.elements:
            i=e.var()
            if i and not e.state:
                e.state,e.time=True,ticks_ms()
            elif e.state and not i:
                self.reset()
                if e.callbacklong and ticks_diff(ticks_ms(),e.time)>config["timeinput"]:
                    e.callbacklong.execute()
                else:
                    e.callback.execute()
    def reset(self):
        for e in self.elements: e.state=False
    def clear(self):
        self.elements.clear()

class Handler():
    def __init__(self):
        self.active=False
        self.elements=[]
    def add(self,p):
        self.time=ticks_ms()
        self.active=True
        self.diff=0
        if type(p)==list: self.elements.insert(0,p)
        else: self.callback=p
    def update(self):
        self.diff=ticks_diff(ticks_ms(),self.time)
        if len(self.elements)>0:
            if self.diff>config["timepopup"]:
                self.elements.pop()
                self.time=ticks_ms()
                self.active=len(self.elements)!=0 or self.callback
        else:
            if self.callback and self.diff>config["timetransition"]*0.5:
                self.callback.execute()
                self.callback=None
            elif self.diff>config["timetransition"]:
                self.active=False
    def draw(self):
        l=len(self.elements)
        if l>0:
            e=self.elements[l-1]
            w,h=len(max(e,key=len)),len(e)
            x,y=4-w/2+sin(ticks_ms()/100)*0.25 if settings["shake"] else 0,2.5-h/2
            for k in range(l,0,-1):
                render_rect(x+k/charw,y+k/charh,w*charw,h*charh,Colors.white,Colors.black)
            for i,s in enumerate(e):
                render_text(s,x+0.2,y+i+0.1)
        else:
            w=int(lerpinout(0,2*screenw/3,self.diff/config["timetransition"]))
            render_rect(0,0,w,screenh,Colors.black)
            render_rect(10-w/charw,0,w,screenh,Colors.black)
            
class Text():
    choice=0 ## possibly move out of class
    def __init__(self,x,y,w,h,s=5,i=0):
        self.x=x
        self.y=y
        self.w=w
        self.h=h
        self.show=s
        self.index=i
        self.elements=[]
    def add(self,s,c,l=None):
        self.elements.append(Element(s,c,l,self.show))
    def update(self):
        for e in self.elements:
            e.dy-=0.1
            if e.dy<-len(e.var): self.execute()
    def execute(self,long=False):
        if settings["audio"]: beep()
        e=self.elements[self.index]
        e.callbacklong.execute() if long and e.callbacklong else e.callback.execute()
    def draw(self):
        for e in self.elements:
            ey=self.y+e.dy
            for i,s in enumerate(e.var):
                if ey+i<=self.y+self.show: render_text(s,self.x,ey+i,Colors.white)
    def reset(self,x=0,y=0,s=5,i=0,dy=0):
        self.x=x
        self.y=y
        self.show=s
        self.index=i
        self.dy=dy
    def clear(self,x=0,y=0,s=5):
        self.elements.clear()
        self.reset(x,y,s)
    def saveindex(self):
        Options.choice=self.index
    def restoreindex(self):
        if Options.choice: self.index=Options.choice
        Options.choice=None
    
class Options(Text):
    def update(self,i):
        self.index=(self.index+i)%len(self.elements)
    def draw(self):
        l=len(self.elements)
        for i in range(l):
            index=i+self.index
            render_text(self.elements[index%l].var or "",self.x,self.y+i,get_color(Colors.rapidflash) if self.index==index else Colors.white)

class Actor():
    def __init__(self,c,m,t,b=False):
        self.id=c["id"]
        self.img=c["img"]
        self.name=c["name"]
        self.hp=c["hp"]
        self.hpmax=c["hp"]
        self.hplev=c["hp"]
        self.active=c["active"]
        self.passive=c["passive"]
        self.spells=str(c["spells"]).split("|") if c["spells"] else []
        self.items=str(c["items"]).split("|") if c["items"] else []
        self.level=c["level"]
        self.map=m
        self.tile=t
        self.boss=b
        self.shift=None
    def update(self):
        if self.shift:
            self.id=self.shift["id"]
            self.img=self.shift["img"]
            self.name=self.shift["name"]
            self.active=self.shift["active"]
            self.passive=self.shift["passive"]
            self.shift=None
        if self.passive=="regen":
            self.heal(1,True)
    def heal(self,v,supress=False):
        self.hp=min(self.hpmax,self.hp+v)
        if not supress and v>0: init_message(self.name+"\nhealed\n"+str(v)+"hp")
    def damage(self,v):
        if self.passive=="resist": v=max(1,v-1)
        if self.passive=="immune": v=1
        v=max(1,min(self.hp,round(v)))
        if self.hp>0: init_message(self.name+"\ndamaged\n-"+str(v)+"hp")
        self.hp-=v
        return v
    def attack(self,t,c,d):
        if t.hp>0:
            if self.active=="might": d+=1
            if self.passive=="strike": c*=1.5
            if t.passive=="dodge": c*=0.67
            if random()<c:
                t.damage(d)
            else:
                init_message(self.name+"\nmisses\n"+t.name)
    def special(self,t,c,v=None,i=None,supress=False):
        v=v if v else self.active
        m=choice(t) if type(t)==list and len(t)>0 else t
        if not supress: init_message(self.name+"\nuses\n"+v)
        if v=="flee":
            self.run(True)
            init_message(self.name+"\nflees")
        elif v=="cast":
            l=len(self.spells)
            if i and l>0:
                s=spells[int(i)]
            elif l>0:
                s=spells[int(choice(self.spells))]
            else:
                self.heal(self.level*2)
                return
            if not supress: init_message(self.name+"\ncasts\n"+s["name"])
            self.special(t,c,s["effect"],None,True)
        elif v=="pray":
            r=randrange(4)
            if r==0:
                self.special(t,c,"cast",None,True)
            elif r==1:
                self.special(t,c,"heal",None,True)
            elif r==2:
                self.special(t,c,"flee")
            else:
                init_message("prayer\nunheard")
        elif v=="heal":
            self.heal(self.level*2)
        elif v=="fury":
            for n in range(max(3,round(self.level/2))):
                m=choice(t) if type(t)==list else t
                self.attack(m,c*0.5,self.level/2)
        elif v=="burn":
            if type(t)==list:
                for m in t:
                    m.damage(self.level*2 if len(t)<2 else self.level)
            else:
                m.damage(self.level*2)
        elif v=="drain":
            self.heal(m.damage(self.level/2))
        elif v=="void":
            hp=0
            if type(t)==list:
                for m in t:
                    hp+=m.damage(self.level if len(t)<2 else self.level/2)
            else:
                hp+=m.damage(self.level)
            self.heal(hp)
        elif v=="shift":
            if self.shift:
                m=self.shift
            else:
                self.shift={"id":self.id,"img":self.img,"name":self.name,"active":self.active,"passive":self.passive}
                while True:
                    m=choice(monsters)
                    l=int(m["level"])
                    if l>self.level//2 and l<=self.level: break
            init_message(self.name+"\nshifts to\n"+m["name"])
            self.id=m["id"]
            self.img=int(m["img"])
            self.name=m["name"]
            self.active=m["active"] or None
            self.passive=m["passive"] or None
            init_fight() # fixes menu items
        elif v=="aura":
            m.damage(self.level*0.75)
        elif v=="slay":
            m.damage(9999)
        elif v=="potion":
            self.special(t,c,"heal")
        elif v=="map":
            self.map.set_visible(self.x,self.y,20)
            init_message("map\nrevealed")
        elif v=="tools":
            if self.tile.state&2>0:
                self.tile.state-=2
                init_message("trap\ndisarmed")
        else:
            init_message("missing\nspecial\n"+v)

class Monster(Actor):
    def __init__(self,c,m,t,b=False):
        super().__init__(c,m,t,b)
        del self.hplev
        del self.items
    def __len__(self):
        return len(self.tile.monsters)
    def move(self):
        ttile=self.map.get_random_neighbour(self.tile.x,self.tile.y)
        ttile.monsters.append(self)
        self.tile.monsters.remove(self)
        self.tile=ttile
    def run(self,auto=False):
        self.move()
    def strike(self,t):
        super().attack(t,config["toblock"],randrange(self.level))

class Player(Actor):
    def __init__(self,c,m=None,t=None,b=False):
        super().__init__(c,m,t,b)
        self.depth,self.xp,self.x,self.y,self.xlast,self.ylast=1,0,0,0,0,0
    def __len__(self):
        return -1
    def move(self,d):
        ## get coords
        dx,dy=d["x"],d["y"]
        cx,cy=self.x+dx,self.y+dy
        tx,ty=cx+dx,cy+dy
        ## if within bounds
        if self.map.is_wall(cx,cy,False):
            ## if current tile trapped and not backtracking
            if self.tile.state&2>0 and (tx!=self.xlast or ty!=self.ylast):
                if random()<config["toavoid"]:
                    init_message("avoided\ntrap")
                else:
                    init_message("caught\nby trap")
                    self.damage(self.depth)
            ## update location and state
            self.xlast,self.ylast=self.x,self.y
            self.x,self.y=tx,ty
            self.tile=self.map.get_tile(self.x,self.y)
            self.map.set_visible(self.x,self.y,1)
            self.update()
            self.map.update(self,True)
            update_state()
            ## messages
            if len(self.tile.monsters)>0:
                s="fighting"
                for m in self.tile.monsters: s+="\n"+m.name
                init_message(s)
    def run(self,autoescape=False):
        if not autoescape and self.active!="flee":
            self.damage(len(self.tile.monsters))
            if random()>config["toescape"]:
                init_message("did not\nescape")
                self.map.update(self)
                return
        ## get random nearby moveable tile
        ttile=self.map.get_random_neighbour(self.x,self.y)
        self.move({"x":(ttile.x-self.x)//2,"y":(ttile.y-self.y)//2})
    def strike(self):
        super().attack(choice(self.tile.monsters),config["tohit"],self.level)
        self.map.update(self)
    def action(self):
        if self.active==None:
            pass
        elif self.active=="cast":
            set_state(Const.spells)
        else:
            super().special(self.tile.monsters,config["tohit"])
            self.map.update(self)
    def cast(self,v):
        self.hp-=1 ## damage player for casting a spell
        super().special(self.tile.monsters,config["tohit"],"cast",v,True)
        self.map.update(self)
        update_state()
    def use(self,v):
        #init_message(self.name+"\nuses item")
        if type(v)==int:
            s,i=spells[v],str(v)
            if len(self.tile.monsters)>0:
                super().special(self.tile.monsters,config["tohit"],s["effect"],None,True)
                self.items.remove(i)
            elif self.passive=="learn":
                if v in self.spells:
                    init_message("already\nknown")
                else:
                    init_message("learned\n"+s["name"])
                    self.spells.append(v)
                    self.items.remove(i)
            else:
                init_message("combat\nuse only")
        else:
            super().special(self.tile.monsters,config["tohit"],v)
            self.items.remove(v)
        ## update map and return to previous state
        self.map.update(self)
        update_state()
    def stairs(self):
        self.depth+=-1 if self.boss else 1
        if self.depth>0:
            set_transition(Const.genlevel)
        else:
            update_state()
        
class Tile():
    def __init__(self,x,y):
        self.x=x
        self.y=y
        self.wall=True
        self.seen=False
        self.state=0 #1=stairs,2=trap,4=treasure
        self.monsters=[]
    
class Level():
    def __init__(self):
        self.w=0
        self.h=0
        self.map=None
    def update(self,p,moved=False):
        ## update monsters
        if not moved and len(p.tile.monsters)>0:
            ## player regeneration
            if p.passive=="regen" and random()<config["toregen"]: p.heal(1,True)
            ## loop through monsters
            for m in reversed(p.tile.monsters):
                ## regenerating monsters are hard to kill!
                if m.passive=="regen" and random()<config["toregen"]:
                    if m.hp<1: init_message(m.name+"\ncomes back\nto life!")
                    m.heal(1,True)
                ## monster is dead
                if m.hp<1:
                    ## remove is destroying order of
                    init_message(m.name+"\ndied!")
                    p.boss=p.boss or m.boss 
                    p.xp+=m.level
                    while p.xp>=pow(p.level,2):
                        p.xp-=pow(p.level,2)
                        p.hp+=p.hplev
                        p.hpmax+=p.hplev
                        p.level+=1
                        init_message("level\nup!")
                    if m.boss: init_message("boss\nkilled\nnow\nescape!")
                    p.tile.monsters.remove(m)
                ## activate specical move
                elif m.active and random()<config["toactive"]:
                    m.special(p,config["toblock"])
                ## else standard attack
                else:
                    m.strike(p)
        ## move monsters
        else:
            movelist=[]
            for x in range(self.w):
                for y in range(self.h):
                    tile=self.map[x][y]
                    for m in tile.monsters:
                        m.update()
                        if not self.is_same_tile(tile,p) and random()<config["tomove"]:
                            movelist.append(m)
            for m in movelist: m.move()
    def clear(self):
        if self.map:
            for x in range(len(self.map)):
                for y in range(len(self.map[x])):
                    self.map[x][y].monsters.clear()
            self.map.clear()
    def is_wall(self,x,y,wall):
        if not self.is_inbounds(x,y): return False
        return self.map[x][y].wall==wall
    def is_seen(self,x,y):
        if not self.is_inbounds(x,y): return False
        return self.map[x][y].seen
    def is_inbounds(self,x,y):
        return not(x<0 or y<0 or x>=self.w or y>=self.h)
    def is_same_tile(self,t,o):
        return t.x==o.x and t.y==o.y
    def get_tile(self,x,y):
        return self.map[x][y]
    def get_dir(self,i,l=1):
        d,j=[0,1,0,-1],i+1
        return d[i%4]*l,d[j%4]*l
    def get_neighbours(self,x,y,wall,l=2):
        r=[]
        for i in range(4):
            dx,dy=self.get_dir(i,l)
            tx,ty=x+dx,y+dy
            if self.is_wall(tx,ty,wall):
                r.append(self.map[tx][ty])
        return r
    def get_corridor_neighbour(self,origin,target):
        ox,oy=origin.x,origin.y
        return self.map[ox+(target.x-ox)//2][oy+(target.y-oy)//2]
    def get_random_tile(self,full=False):
        if full: return self.map[randrange(self.w)][randrange(self.h)]
        return self.map[randrange(self.w)//2*2][randrange(self.h)//2*2]
    def get_random_neighbour(self,x,y):
        r=[]
        for i in range(4):
            dx,dy=self.get_dir(i)
            tx,ty=x+dx,y+dy
            if self.is_wall(tx,ty,False):
                r.append(self.map[x+dx*2][y+dy*2])
        return choice(r)
    def set_visible(self,x,y,size):
        for tx in range(x-size,x+size+1):
            for ty in range(y-size,y+size+1):
                if self.is_inbounds(tx,ty):
                    self.map[tx][ty].seen=True
   
# ===============================================
# picodisplay pack display functions
# move to include?
# ===============================================
class Colors():
    black=0
    white=1
    flash=-1
    rapidflash=-2

def load_data():
    global screenw,screenh,screenbuffer,charw,charh,fontsize,sprites
    global spells,classes,monsters,bosses,treasures,settings,config,lang,text_credits,text_story,text_help,text_bool,text_back,text_skip,text_info
    ## load display
    screenw,screenh=thumby.display.width,thumby.display.height
    render_cls(0)
    render_update()
    ## load graphics
    charw,charh,fontsize=8,8,1
    with open("/Games/TinyRogue/trtgraphics.txt") as f: sprites=[list(map(int,(line.strip().split(",")))) for line in f]
    ## load data
    with open("/Games/TinyRogue/trdata.txt") as f: data=[line.strip() for line in f]
    spells,classes,monsters=parse_data(data[0]),parse_data(data[1]),parse_data(data[2])
    bosses,treasures=parse_data(data[3]),data[4].split(",")
    settings,config,lang=parse_data(data[5],bool)[0],parse_data(data[6],float)[0],parse_data(data[7])[0]
    text_credits,text_story,text_help=(data[8]).split("\\n"),(data[9]).split("\\n"),(data[10]).split("\\n")
    text_bool,text_back={True:"on",False:"off"},lang['z']+"/"+lang['x']+" BACK"
    text_skip,text_info=lang['z']+"/"+lang['x']+" SKIPS",lang['z']+"=? "+lang['x']+"=GO"

def render_cls(v=0):
    thumby.display.fill(int(v))
def render_update():
    thumby.display.update()
def render_text(s,x,y,c=1):
    for i,n in enumerate(s.split("\n")): thumby.display.drawText(n.upper(),round(x*charw),round(y*charh)+i*charh,c)
def render_rect(x,y,w,h,border=1,inner=0,edge=2):
    x,y=round(x*charw),round(y*charh)
    if inner!=0:
        thumby.display.drawFilledRectangle(x,y,w,h,inner)
        thumby.display.drawRectangle(x,y,w,h,border)
    else:
        thumby.display.drawFilledRectangle(x,y,w,h,inner)
        thumby.display.drawRectangle(x,y,w,h,border)
def render_sprite(spr,x,y,w=8,h=8,k=0):
    thumby.display.blit(bytearray(spr),round(x*charw),round(y*charh),w,h,k,0,0)
def beep():
    thumby.audio.play(440,100)
    
def init_input_move():
    state.clear()
    state.add(get_key_up,Callback(player.move,{"x":0,"y":-1}))
    state.add(get_key_down,Callback(player.move,{"x":0,"y":1}))
    state.add(get_key_left,Callback(player.move,{"x":-1,"y":0}))
    state.add(get_key_right,Callback(player.move,{"x":1,"y":0}))
    state.add(get_key_x,Callback(set_state,Const.items))
    state.add(get_key_z,Callback(set_state,Const.items))
def init_input_menu():
    state.clear()
    state.add(get_key_up,Callback(options.update,-1))
    state.add(get_key_menu_down,Callback(options.update,1))
    state.add(get_key_x,Callback(options.execute),Callback(options.execute,True))
    state.add(get_key_z,Callback(options.execute),Callback(options.execute,True))
    
def get_color(c):
    if c==Colors.rapidflash: return Colors.white if ticks_diff(0,ticks_ms())%500<250 else Colors.black
    if c==Colors.flash: return Colors.white if time()%2<1 else Colors.black
    return Colors.white
def get_key_menu_down():
    return thumby.buttonD.pressed()
def get_key_up():
    return thumby.buttonU.pressed()
def get_key_down():
    return thumby.buttonD.pressed()
def get_key_left():
    return thumby.buttonL.pressed()
def get_key_right():
    return thumby.buttonR.pressed()
def get_key_x():
    return thumby.buttonA.pressed()
def get_key_z():
    return thumby.buttonB.pressed()

# ===============================================
# core functionality
# ===============================================
def init():
    global arr_init,arr_update,arr_draw,state,level,handler,options,text,player
    ## load information
    load_data()
    ## setup arrays
    arr_init=[None,init_menu,init_settings,init_help,init_credits,init_newgame,init_newinfo,init_newstory,init_genlevel,init_explore,init_fight,init_items,init_spells,init_stairs,init_gameover,init_gamewon,init_quit]
    arr_update=[update_title,None,None,None,None,None,None,None,None,update_explore,update_fight,None,None,None,update_menuwait,update_menuwait,None]
    arr_draw=[draw_title,draw_menu,None,None,None,None,draw_newinfo,None,None,draw_explore,draw_map,None,None,draw_map,None,None,None]
    ## setup classes
    state,level,handler,player=States(),Level(),Handler(),Player(classes[0])
    options,text=Options(0,0,screenw,screenh),Text(0,0,screenw,screenh)
def update():
    if handler.active:
        handler.update()
    else:
        state.update()
        text.update()
        if arr_update[state.current]: arr_update[state.current]()
def draw():
    render_cls()
    options.draw()
    text.draw()
    if arr_draw[state.current]: arr_draw[state.current]()
    if handler.active: handler.draw()
    render_update()
def shutdown():
    state.clear()
    state.active=False
    
def toggle_setting(v):
    settings[v]=not settings[v]
    options.saveindex()
    set_state(Const.settings)
def set_state(v):
    state.current=v
    arr_init[v]()
def set_transition(v):
    if settings["fades"]: handler.add(Callback(set_state,v))
    else: set_state(v) 
def lerp(a,b,t):
    return a*(1-t)+b*t
def lerpinout(a,b,t):
    if t<.5: return lerp(a,b,t*2)
    return lerp(a,b,1-t)

def parse_data(data,t=None):
    ## seperate keys from values
    ret,raw=[],data.split(":")
    ids,content=raw[0].split(","),raw[1].split(";")
    ## seperate keys from values
    for i,n in enumerate(content):
        d,e=n.split(","),{}
        for j,m in enumerate(ids):
            e[m]=int(d[j]) if d[j].isdigit() else d[j] or None
        ret.append(e)
    ## convert ints to booleans
    if t==bool:
        for n in ret:
            for m in ids:
                if n[m]==0 or 1:
                    n[m]=n[m]==1
    ## convert to floats
    elif t==float:
        for n in ret:
            for m in ids:
                n[m]=float(n[m])
    ## return parsed data
    return ret
 
def init_menu():
    level.clear()
    text.clear(0,0,3)
    options.clear(0,2)
    options.add("new game",Callback(set_transition,Const.newgame))
    options.add("settings",Callback(set_transition,Const.settings))
    options.add("help",Callback(set_transition,Const.help))
    options.add("credits",Callback(set_transition,Const.credits))
    options.add("quit",Callback(set_state,Const.quit))
    init_input_menu()
def init_settings():
    options.clear()
    options.add("back",Callback(set_transition,Const.menu))
    for k in settings.keys(): options.add(k+":"+text_bool[settings[k]],Callback(toggle_setting,k))
    options.restoreindex()
def init_help():
    options.clear(0,4)
    options.add("back",Callback(set_transition,Const.menu))
    text.add(text_help,Callback(set_transition,Const.menu))
def init_credits():
    options.clear(0,4)
    options.add("back",Callback(set_transition,Const.menu))
    text.add(text_credits,Callback(set_transition,Const.menu))
def init_newgame():
    options.clear()
    options.add("back",Callback(set_transition,Const.menu))
    for n in classes:
        options.add(n["name"],Callback(set_transition,Const.newstory),Callback(set_transition,Const.newinfo))
    options.restoreindex()
def init_newinfo():
    options.saveindex()
    options.clear(0,4)
    options.add("back",Callback(set_transition,Const.newgame))
def init_newstory():
    global player
    player=Player(classes[options.index-1])
    if settings["story"]:
        options.clear(0,4)
        options.add("skip",Callback(set_transition,Const.genlevel))
        text.add(text_story,Callback(set_transition,Const.genlevel))
    else:
        set_state(Const.genlevel)
def init_genlevel():
    ## prep for level gen
    text.clear()
    options.clear()
    level.clear()
    collect()
    ## setup level
    depth=min(config["capdepth"],player.depth)
    level.w=level.h=min(depth//2*2+3,19)
    level.map=[[Tile(x,y) for y in range(level.h)] for x in range(level.w)]
    ## setup player
    player.x,player.y=randrange(level.w)//2*2,randrange(level.h)//2*2
    player.map,player.tile=level,level.map[player.x][player.y]
    player.tile.wall=False
    ## random maze gen
    level.set_visible(player.x,player.y,1)
    opentiles=level.get_neighbours(player.x,player.y,True)
    while len(opentiles)>0:
        tile=choice(opentiles)
        tile.wall=False
        potentials=level.get_neighbours(tile.x,tile.y,True)
        while len(potentials)>0:
            ttile=potentials.pop()
            if not ttile in opentiles:
                opentiles.append(ttile)
        potentials=level.get_neighbours(tile.x,tile.y,False)
        if len(potentials)>0:
            ttile=choice(potentials)
            ctile=level.get_corridor_neighbour(tile,ttile)
            ttile.wall=False
            ctile.wall=False
        opentiles.remove(tile)
    ## generate stairs
    while True:
        ttile=level.get_random_tile()
        if not level.is_same_tile(ttile,player): break
    ttile.state+=1
    ## generate gaps
    for i in range(int(depth*config["gengaps"])):
        while True:
            ttile=level.get_random_tile(True)
            if ttile.x%2==1 and ttile.y%2==0 or ttile.x%2==0 and ttile.y%2==1: break
        ttile.wall=False
    ## generate traps
    for i in range(int(depth*config["gentraps"])):
        while True:
            ttile=level.get_random_tile()
            if not level.is_same_tile(ttile,player): break
        ttile.state+=2
    ## generate treasure
    for i in range(int(depth*config["gentreasures"])):
        while True:
            ttile=level.get_random_tile()
            if not level.is_same_tile(ttile,player): break
        ttile.state+=4
    ## generate monsters
    for i in range(int(depth*config["genmonsters"])):
        while True:
            ttile=level.get_random_tile()
            if not level.is_same_tile(ttile,player) and len(ttile.monsters)<4: break
        ## gen monster
        while True:
            m=choice(monsters)
            l=int(m["level"])
            if l>depth//2 and l<=depth: break
        ttile.monsters.append(Monster(m,level,ttile))
    ## generate boss
    if not player.boss and depth>=config["genboss"]:    
        while True:
            ttile=level.get_random_tile()
            if not level.is_same_tile(ttile,player): break
        ## gen monster
        while True:
            m=choice(bosses)
            l=int(m["level"])
            if l>depth//2 and l<=depth: break
        ttile.monsters.append(Monster(m,level,ttile,True))
    ## update state
    set_state(Const.gamewon if player.depth==0 else Const.explore)
def init_explore():
    options.clear()
    init_input_move()
def init_fight():
    options.clear(5,1,4)
    options.add("hit",Callback(player.strike))
    options.add("item",Callback(set_state,Const.items))
    options.add(player.active,Callback(player.action))
    options.add("run",Callback(player.run))
    init_input_menu()
def init_items():
    options.clear(0,0,min(5,len(player.items)+1))
    options.add("back",Callback(update_state))
    for n in player.items:
        if n.isdigit(): v,s=int(n),"*"+spells[int(n)]["name"]
        else: v,s=n,n
        options.add(s,Callback(player.use,v))
    init_input_menu()
def init_spells():
    options.clear(0,0,min(5,len(player.spells)+1))
    options.add("back",Callback(set_state,Const.fight))
    for n in player.spells:
        options.add(spells[int(n)]["name"],Callback(player.cast,n))
    init_input_menu()
def init_stairs():
    options.clear(5,1,2)
    options.add("stay",Callback(set_state,Const.explore))
    options.add("take",Callback(player.stairs))
    init_input_menu()
def init_gameover():
    state.clear()
    options.clear()
    init_message("you\ndied!")
def init_gamewon():
    state.clear()
    options.clear()
    init_message("you\nescaped!\nyou won!")
def init_quit():
    shutdown()

def init_message(s):
    handler.add(s.split("\n"))

def update_title():
    if time()>state.time+2:
        del sprites[len(sprites)-1]
        set_state(Const.menu)
def update_explore():
    if player.hp<1 or len(player.tile.monsters)>0: update_state()
def update_fight():
    if player.hp<1 or len(player.tile.monsters)<1: update_state()
def update_menuwait():
    if time()>state.time+2: set_transition(Const.menu)
def update_state():
    if player.hp<1:
        set_transition(Const.gameover)
    elif player.depth<1:
        set_transition(Const.gamewon)
    elif len(player.tile.monsters)>0:
        set_state(Const.fight)
    elif player.tile.state&2>0 and player.passive=="disarm":
        init_message("trap\ndisarmed")
        player.tile.state-=2
        update_state()
    elif player.tile.state&4>0:
        init_message("found\nitem")
        player.items.append(choice(treasures))
        player.tile.state-=4
        update_state()
    elif player.tile.state&1>0:
        set_state(Const.stairs)
    elif state.current!=Const.explore:
        set_state(Const.explore)

def draw_title():
    render_sprite(sprites[14],0.5,0.5,64,32)
def draw_menu():
    render_sprite(sprites[13],0.5,0,64,16)
def draw_newinfo():
    c=classes[Options.choice-1]
    render_text(c["name"]+"\n"+str(c["hp"])+" hp/lv\n"+(c["active"] or "none")+"\n"+c["passive"] or "none",0,0)
def draw_explore():
    draw_map()
    info="f"+str(player.depth) if time()%4<2 else "l"+str(player.level)
    px,py,cw,ch,size=player.x,player.y,fontsize/charw,fontsize/charh,level.w+2
    render_text("?"+str(px//2)+","+str(py//2),5,1)
    render_rect(6.125,2.125,size,size,1,1)
    for i in range(len(info)): render_text(info[i],5,2+i)
    for x in range(level.w):
        for y in range(level.h):
            tile=level.map[x][y]
            if tile.seen and not tile.wall:
                render_rect(6.25+x*cw,2.25+y*ch,1,1,get_color(Colors.flash) if tile.state&1>0 else Colors.black)    
    render_rect(6.25+px*cw,2.25+py*ch,1,1,get_color(Colors.rapidflash))
def draw_map():
    ## variables
    tile,images=level.map[player.x][player.y],settings["image"]
    ## health
    if images:
        render_rect(6,0,charw*3*player.hp//player.hpmax,charh,1,1)
        render_sprite(sprites[0],5,0)
        render_sprite(sprites[player.img],2,2)
    else:
        render_text("h:"+str(player.hp),5,0)
        render_text(player.id,2,2)
    ## room
    for i in range(25):
        x,y=i%5,i//5
        if x%4==0 or y%4==0:
            dx,dy=(x-2)//2,(y-2)//2
            if x!=2 and y!=2 or not level.is_wall(player.x+dx,player.y+dy,False):
                if images: render_sprite(sprites[1],x,y)
                else: render_text("#",x,y)
            elif not level.is_seen(player.x+dx*2,player.y+dy*2):
                if images: render_sprite(sprites[12],x,y)
                else: render_text("o",x,y)
    ## contents
    if tile.state&1>0: render_sprite(sprites[2],1,1) if images else render_text("/",1,1) 
    if tile.state&2>0: render_sprite(sprites[3],1,3) if images else render_text("^",1,3)
    if tile.state&4>0: render_sprite(sprites[4],3,1) if images else render_text("!",3,1)
    ## monsters
    for i,n in enumerate(tile.monsters):
        x,y=level.get_dir(i)
        if images: render_sprite(sprites[n.img],x+2,y+2)
        else: render_text(n.id,x+2,y+2)

# core initialisation
init()

# core loop
while state.active:
    update()
    draw()
    collect()

## clear screen
render_cls(0.0)
render_update()

## restart machine
reset()
