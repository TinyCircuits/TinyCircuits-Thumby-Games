GAME_NAME="MineSweep"
GAME_DIR=f"/Games/{GAME_NAME}"

import gc
import io
import os
import random
import sys
import thumby
import time

sys.path.insert(sys.path.index("/lib"),GAME_DIR+"/lib");

gc.collect()
import thumbyGrayscale
import thumby2

gs=thumbyGrayscale.display
gs_b=thumby2.Buffer.screenSized(gs.buffer)
gs_sh=thumby2.Buffer.screenSized(gs.shading)
gs_bs=[gs_b,gs_sh]
gs_lg=gs_bs

MODES=[
    {"name":"Beginner","shortName":"BEGIN.","size":(9,9),"mines":10},
    {"name":"Intermed.","shortName":"INTER.","size":(16,16),"mines":40},
    {"name":"Advanced","shortName":"ADV.","size":(30,16),"mines":99},
]

def update():
    gs.show()
    thumby2.buttons.update()
    return thumby2.display.waitFrame()

SIDE=9

MINE_DIGIT_SPRS=[thumby2.Sprite(blit,4,6) for blit in [
# BITMAP: width: 4, height: 6
    bytes([0,8,4,0]),
# BITMAP: width: 4, height: 6
    bytes([0,34,63,32]),
# BITMAP: width: 4, height: 6
    bytes([34,49,41,38]),
# BITMAP: width: 4, height: 6
    bytes([18,33,37,26]),
# BITMAP: width: 4, height: 6
    bytes([12,10,63,8]),
# BITMAP: width: 4, height: 6
    bytes([39,37,37,25]),
# BITMAP: width: 4, height: 6
    bytes([30,37,37,25]),
# BITMAP: width: 4, height: 6
    bytes([1,49,13,3]),
# BITMAP: width: 4, height: 6
    bytes([26,37,37,26]),
]]

def drawMineDigit(digit,x,y):
    fb=MINE_DIGIT_SPRS[digit]
    if fb:
        for b in gs_lg:
            b.sprite(fb,x+3,y+2)

# BITMAP: width: 6, height: 6
MINE_SPR=thumby2.Sprite(bytes([18,45,30,30,45,18]),6,6)
EXPLODED_MINE_SSPR=(
# BITMAP: width: 12, height: 12
    thumby2.Sprite(
        bytes([144,180,74,148,107,148,146,107,148,42,212,144,0,2,5,2,13,4,2,13,2,5,2,0]),
        12,12),
# BITMAP: width: 12, height: 12
    thumby2.Sprite(
        bytes([0,240,248,12,6,102,102,6,12,248,240,0,0,0,1,3,6,6,6,6,3,1,0,0]),
        12,12))

def drawMine(x,y):
    gs_b.sprite(MINE_SPR,x+2,y+2)

def drawExplodedMine(x,y):
    gs_b.sprite(EXPLODED_MINE_SSPR[0],x-1,y-1)
    gs_sh.sprite(EXPLODED_MINE_SSPR[1],x-1,y-1)

# BITMAP: width: 6, height: 6
FLAG_SPR=thumby2.Sprite(bytes([5,39,55,63,48,32]),6,6)
# BITMAP: width: 6, height: 6
BAD_FLAG_SPR=thumby2.Sprite(bytes([0,37,50,61,48,32]),6,6)

def drawFlag(x,y):
    gs_b.sprite(FLAG_SPR,x+2,y+2)

def drawBadFlag(x,y):
    gs_b.sprite(BAD_FLAG_SPR,x+2,y+2)

F_NUM_MASK=0b00001111
F_MINE=0b00010000
F_OPEN=0b00100000
F_FLAG=0b01000000

def print57(text,row,column=0,color=gs.WHITE):
    gs_b.text57().print(text,row,column,color&1!=0)
    gs_sh.text57().print(text,row,column,color&2!=0)

def clear57(row,column=0,rows=1,columns=1000):
    for b in gs_bs:
        b.text57().clear(row,column,rows,columns)

def menuChoice(numOptions,startRow=0,selOption=0):
    while True:
        clear57(startRow,rows=numOptions,columns=1)
        print57(">",startRow+selOption)
        gs.show()
        btn=thumby2.buttons.wait([
            thumby2.buttons.UP,thumby2.buttons.DOWN,
            thumby2.buttons.A,thumby2.buttons.B,
        ])
        if btn==thumby2.buttons.UP:
            selOption-=1
        elif btn==thumby2.buttons.DOWN:
            selOption+=1
        elif btn==thumby2.buttons.A:
            thumby2.buttons.assumeUp()
            return selOption
        elif btn==thumby2.buttons.B:
            thumby2.buttons.assumeUp()
            return None
        selOption%=numOptions

class save_file:

    DIRS=["/Saves",f"/Saves/{GAME_NAME}"]
    PATH=f"/Saves/{GAME_NAME}/save"

    @staticmethod
    def load():
        try:
            with open(save_file.PATH,"b") as f:
                save=f.read()
        except OSError as e:
            if e.errno==errno.ENOENT:
                return None
            print(f"Error opening save file ({save_file.PATH}): {e}")
            return None
        try:
            return Game.deserialise(save)
        except Exception as e:
            print(f"Error deserialising save file ({save_file.PATH}): {e}")
            return None

    @staticmethod
    def destroy():
        try:
            os.remove(save_file.PATH)
            return True
        except OSError:
            return False

    @staticmethod
    def save(game):
        for dir in save_file.DIRS:
            try:
                os.mkdir(dir)
            except OSError:
                pass
        bytes=game.serialise()
        with open(save_file.PATH,"wb") as f:
            f.write(bytes)

class Game:

    NEIGHBOURS=[(1,0),(1,1),(0,1),(-1,1),(-1,0),(-1,-1),(0,-1),(1,-1)]

    SCROLLBAR_WIDTH=2
    SCROLL_BLOCK_WIDTH=1
    BOARD_FILL_RANGE_X=(2,71-SCROLLBAR_WIDTH-1)
    BOARD_FILL_RANGE_Y=(8,39-SCROLLBAR_WIDTH-1)
    PREFERRED_POS_RANGE_X=(2*SIDE+2,71-SCROLLBAR_WIDTH-(2*SIDE+2))
    PREFERRED_POS_Y=(39-SCROLLBAR_WIDTH-SIDE)//2

    def __init__(self,mode):
        self.mode=mode
        self.size=mode["size"]
        self.mines=mode["mines"]
        self.b=bytearray(self.size[0]*self.size[1])
        self.bInited=False
        self.numFlags=0
        self.safeLeft=self.size[0]*self.size[1]-self.mines
        self.pos=(0,0)
        self.boardOffset=(0,0)
        self.running=True
        self.win=None

    def __getitem__(self,pos):
        return self.b[pos[0]+pos[1]*self.size[0]]

    def __setitem__(self,pos,val):
        self.b[pos[0]+pos[1]*self.size[0]]=val

    def getNeighbours(self,pos):
        return [
            pos for pos in ((pos[0]+dx,pos[1]+dy) for dx,dy in Game.NEIGHBOURS)
            if self.posInRange(pos)
        ]

    def posInRange(self,pos):
        return 0<=pos[0]<self.size[0] and 0<=pos[1]<self.size[1]

    def draw(self,dPos=(0,0)):
        gs.fill(0)
        def calcOffset(offset,pos,size,
                boardFillRange,preferredPosRange,scrollbarLen):
            if self.running:
                posOnScreen=offset+pos
                if posOnScreen<preferredPosRange[0]:
                    offset=preferredPosRange[0]-pos
                elif posOnScreen+SIDE>preferredPosRange[1]:
                    offset=preferredPosRange[1]-pos-SIDE
            if offset>boardFillRange[0]:
                offset=boardFillRange[0]
            elif offset+size<boardFillRange[1]:
                offset=boardFillRange[1]-size
            scrollFrom=(boardFillRange[0]-offset)*scrollbarLen//size
            scrollTo=(boardFillRange[1]-offset)*scrollbarLen//size-1
            return (offset,(scrollFrom,scrollTo))
        x0,xScroll=calcOffset(
            self.boardOffset[0],self.pos[0]*SIDE+dPos[0],self.size[0]*SIDE,
            Game.BOARD_FILL_RANGE_X,Game.PREFERRED_POS_RANGE_X,
            72-Game.SCROLL_BLOCK_WIDTH)
        y0,yScroll=calcOffset(
            self.boardOffset[1],self.pos[1]*SIDE+dPos[1],self.size[1]*SIDE,
            Game.BOARD_FILL_RANGE_Y,(Game.PREFERRED_POS_Y,Game.PREFERRED_POS_Y+SIDE),
            40-Game.SCROLL_BLOCK_WIDTH)
        self.boardOffset=(x0,y0)
        xx,yy=self.size
        for x in range(xx+1):
            gs_sh.drawLineV(x*SIDE+x0,y0,y0+yy*SIDE,1)
        for y in range(yy+1):
            gs_sh.drawLineH(x0,y*SIDE+y0,x0+xx*SIDE,1)
        gs_b.drawRect(x0-1,y0-1,xx*SIDE+3,yy*SIDE+3,1)
        for y in range(yy):
            fy=y*SIDE+y0
            if -SIDE<fy<40:
                for x in range(xx):
                    fx=x*SIDE+x0
                    if -SIDE<fx<72:
                        field=self[(x,y)]
                        if field&F_OPEN!=0:
                            if field&F_MINE!=0:
                                drawExplodedMine(fx,fy)
                            else:
                                drawMineDigit(field&F_NUM_MASK,x*SIDE+x0,y*SIDE+y0)
                        else:
                            if field&F_FLAG!=0:
                                if not self.running and field&F_MINE==0:
                                    drawBadFlag(fx,fy)
                                else:
                                    drawFlag(fx,fy)
                            elif not self.running and field&F_MINE!=0:
                                drawMine(fx,fy)
        if self.running or not self.win:
            minesLeft=self.mines-self.numFlags
            minesLeftStr=str(minesLeft) if minesLeft>=0 else "?"
            minesLeftWid=4*len(minesLeftStr)-1
            for b in gs_bs:
                b.fillRect(0,0,minesLeftWid+3,8,0)
                b.drawLineH(0,6,minesLeftWid+1,1)
                b.drawLineV(minesLeftWid+1,0,6,1)
                b.text35().print(minesLeftStr,0,0)
        if self.running:
            for b in gs_lg:
                b.drawRect(
                    x0+self.pos[0]*SIDE+dPos[0]+1,y0+self.pos[1]*SIDE+dPos[1]+1,8,8,1)
        scrollWid=Game.SCROLLBAR_WIDTH
        scrollBlockWid=Game.SCROLL_BLOCK_WIDTH
        for b in gs_bs:
            b.fillRect(0,40-scrollWid,72-scrollWid,scrollWid,0)
            b.fillRect(72-scrollWid,0,scrollWid,40,0)
            b.drawLineH(xScroll[0],39,xScroll[1],1)
            b.drawLineV(71,yScroll[0],yScroll[1],1)
        if not self.running:
            if self.win:
                text="YOU WIN!"
                if (shn:=self.mode["shortName"]):
                    text+=f" ({shn})"
                textW=len(text)*4-1
                textX=(72-textW)//2
                for b in gs_bs:
                    b.drawLineH(0,7,70,0)
                gs_b.fillRect(0,0,70,7,1)
                gs_sh.fillRect(0,0,70,7,0)
                gs_b.text35().printXY(text,textX,1,0)
            else:
                text="GAME OVER"
                textW=len(text)*6-1
                textX=71-textW
                for b in gs_bs:
                    b.fillRect(textX-2,0,textW+5,10,0)
                gs_b.fillRect(textX-1,0,textW+4,9,1)
                gs_b.text57().printXY(text,textX,1,0)

    def panGameOverView(self,vec):
        self.boardOffset=(self.boardOffset[0]-vec[0],self.boardOffset[1]-vec[1])

    def open(self,pos):
        if self[pos]&F_OPEN==0:
            self[pos]|=F_OPEN
            self.__ensureInited()
            if self[pos]&F_MINE!=0:
                self.giveUp()
            else:
                self.safeLeft-=1
                if self[pos]&F_NUM_MASK==0:
                    self.__openCascade(pos)
                if self.safeLeft==0:
                    self.running=False
                    self.win=True
                    for x in range(self.size[0]):
                        for y in range(self.size[1]):
                            p=(x,y)
                            if self[p]&F_MINE!=0:
                                self[p]|=F_FLAG


    def __openCascade(self,pos):
        q=[pos]
        while len(q):
            p=q.pop()
            for n in self.getNeighbours(p):
                nf=self[n]
                if nf&F_OPEN==0 and nf&F_FLAG==0:
                    self[n]=nf|F_OPEN
                    self.safeLeft-=1
                    if nf&F_NUM_MASK==0:
                        q.append(n)

    def giveUp(self):
        self.__ensureInited(fieldOpened=False)
        self.running=False
        self.win=False

    def __ensureInited(self,fieldOpened=True):
        if not self.bInited:
            minesLeft=self.mines
            fieldsLeft=self.size[0]*self.size[1]-fieldOpened
            for x in range(self.size[0]):
                for y in range(self.size[1]):
                    p=(x,y)
                    if self[p]&F_OPEN==0:
                        if random.randrange(fieldsLeft)<minesLeft:
                            minesLeft-=1
                            self.__placeMine(p)
                        fieldsLeft-=1
            self.bInited=True

    def __placeMine(self,pos):
        self[pos]|=F_MINE
        for n in self.getNeighbours(pos):
            self[n]+=1

    def flag(self,pos):
        f=self[pos]
        if f&F_OPEN==0:
            f^=F_FLAG
            self[pos]=f
            if f&F_FLAG==0:
                self.numFlags-=1
            else:
                self.numFlags+=1

    B_SERIALISATION=[
        0,
        F_MINE,
        F_FLAG,
        F_MINE|F_FLAG,
        F_OPEN,
    ]
    BITS_PER_POS=2.3219281 # math.log(len(B_SERIALISATION))/math.log(2)

    @staticmethod
    def deserialise(bytes):
        inp=io.BytesIO(bytes)
        ver=inp.read(1)[0]
        if ver==1:
            sizeB=inp.read(2)
            size=(sizeB[0],sizeB[1])
            mines=inp.read(1)[0]
            matchModes=[m for m in MODES if m["size"]==size and m["mines"]==mines]
            shortName=matchModes[0]["shortName"] if matchModes else None
            g=Game({"size":size,"mines":mines,"shortName":shortName})
            g.bInited=inp.read(1)[0]
            g.pos=(inp.read(1)[0],inp.read(1)[0])
            boardVal=int.from_bytes(inp.read(),"big")
            for i in reversed(range(len(g.b))):
                boardVal,m=divmod(boardVal,len(Game.B_SERIALISATION))
                val=Game.B_SERIALISATION[m]
                g.b[i]|=val
                if val&F_OPEN!=0:
                    g.safeLeft-=1
                if val&F_FLAG!=0:
                    g.numFlags+=1
                if val&F_MINE!=0:
                    y,x=divmod(i,g.size[0])
                    g.__placeMine((x,y))
            return g
        else:
            return None

    def serialise(self):
        out=bytearray()
        out.append(1)
        out.append(self.size[0])
        out.append(self.size[1])
        out.append(self.mines)
        out.append(self.bInited)
        out.append(self.pos[0])
        out.append(self.pos[1])
        boardVal=0
        mask=F_MINE|F_FLAG|F_OPEN
        for b in self.b:
            boardVal*=len(Game.B_SERIALISATION)
            boardVal+=Game.B_SERIALISATION.index(b&mask)
        numBits=int(len(self.b)*Game.BITS_PER_POS+1)
        out.extend(boardVal.to_bytes((numBits+7)//8,"big"))
        return out

def drawLogo():
    text="MineSweep"
    x0=(72-len(text)*7)//2
    font=thumby2.Font.font("/lib/font5x7.bin",5,7,2)
    gs_b.text(font).printXY(text,x0+1,0,1)
    gs_sh.text(font).printXY(text,x0+1,0,1)
    gs_b.text(font).printXY(text,x0,0,1)
    gs_sh.text(font).printXY(text,x0,0,0)

def main(data):
    loadedGame=save_file.load()
    gs.fill(0)
    drawLogo()
    print57([m["name"] for m in MODES],1,1,color=gs.LIGHTGRAY)
    loadText="Load"
    print57(loadText,1+len(MODES),1,color=gs.LIGHTGRAY if loadedGame else gs.DARKGRAY)
    if "mainMenuSelOption" in data:
        selOption=data["mainMenuSelOption"]
    elif loadedGame is None:
        selOption=0
    else:
        selOption=len(MODES)
    selOption=menuChoice(len(MODES)+1,startRow=1,selOption=selOption)
    if selOption is None:
        clear57(1,rows=4)
        print57("Exit",2,color=gs.LIGHTGRAY)
        gs.show()
        time.sleep(1)
        return False
    data["mainMenuSelOption"]=selOption
    clear57(1,rows=4)
    if selOption==len(MODES):
        if loadedGame is None:
            print57(
                ["No saved","game.","Hold B in","game to save"],1,color=gs.LIGHTGRAY)
            print57("B",3,5)
            gs.show()
            thumby2.buttons.wait()
            return True
        g=loadedGame
        print57("Load game:",1)
        numFlagsStr=f"{g.numFlags}"
        print57(numFlagsStr,3,color=gs.LIGHTGRAY)
        drawFlag(6*len(numFlagsStr)-1,3*8-1)
        if g.numFlags<=g.mines:
            print57(
                f"({100*g.numFlags//g.mines}%)",3,len(numFlagsStr)+2,color=gs.LIGHTGRAY)
    else:
        g=Game(MODES[selOption])
        print57("New game:",1)
    paramsStr=f"{g.size[0]}x{g.size[1]}, {g.mines}"
    print57(paramsStr,2,color=gs.LIGHTGRAY)
    drawMine(6*len(paramsStr)-1,2*8-1)
    print57("B=back  A=OK",4,color=gs.LIGHTGRAY)
    print57("B       A",4)
    gs.show()
    if thumby2.buttons.wait()==thumby2.buttons.B:
        return True
    clear57(1,rows=4)
    print57([
        "Controls:",
        "A=step/chord",
        "B=set flag",
        "hold B=menu",
    ],1,color=gs.LIGHTGRAY)
    print57(["Controls:","A","B","hold B"],1)
    gs.show()
    if thumby2.buttons.wait()==thumby2.buttons.B:
        return True
    thumby2.buttons.assumeUp()
    if g==loadedGame:
        save_file.destroy()
        del data["mainMenuSelOption"]

    thumby.display.setFPS(40)
    while g.running:
        g.draw()
        update()
        spd=None
        for btn,vec in thumby2.buttons.DPAD_VECTORS:
            if btn.edge>0 or btn.downTimeMs()>=300:
                spd=vec
                break
        if spd:
            nPos=(g.pos[0]+spd[0],g.pos[1]+spd[1])
            if g.posInRange(nPos):
                dPos=(0,0)
                step=2
                for dd in range(step,SIDE,step):
                    dPos=(dPos[0]+step*spd[0],dPos[1]+step*spd[1])
                    g.draw(dPos=dPos)
                    update()
                g.pos=nPos
        if thumby2.buttons.A.edge>0:
            if g[g.pos]&F_OPEN!=0:
                num=g[g.pos]&F_NUM_MASK
                if num>0:
                    for n in g.getNeighbours(g.pos):
                        if g[n]&F_FLAG!=0:
                            num-=1
                            if num<0:
                                break
                    if num==0:
                        for n in g.getNeighbours(g.pos):
                            if g[n]&F_FLAG==0:
                                g.open(n)
            elif g[g.pos]&F_FLAG==0:
                g.open(g.pos)
            if not g.running:
                g.draw()
                gs.show()
                if g.win:
                    thumby2.audio.musicBlocking([
                        (11,6),(None,2),
                        (11,1),(None,1),
                        (11,1),(None,1),
                        (14,3),(None,1),
                        (11,3),(None,1),
                        (14,3),(None,1),
                        (19,12),
                    ],50)
                else:
                    tone=50
                    inv=True
                    for rep in range(30):
                        gs.invert(inv)
                        inv=not inv
                        thumby2.audio.musicBlocking([(tone,40)])
                        tone-=3
        elif thumby2.buttons.B.edge<0 and thumby2.buttons.B.longPressEdge==0:
            g.flag(g.pos)
        elif thumby2.buttons.B.longPressEdge>0:
            gs.fill(0)
            print57("Pause menu",0)
            print57([
                " Resume",
                " Give up",
                " Save & Menu",
                " Save & Exit",
            ],1,color=gs.LIGHTGRAY)
            gs.show()
            sel=menuChoice(4,startRow=1)
            thumby2.buttons.assumeUp()
            if sel==1:
                g.giveUp()
            elif sel==2:
                save_file.save(g)
                return True
            elif sel==3:
                save_file.save(g)
                gs.fill(0)
                drawLogo()
                print57(["Saved.","Exit"],2,color=gs.LIGHTGRAY)
                gs.show()
                time.sleep(1)
                return False
    thumby2.buttons.assumeUp()
    while True:
        g.draw()
        update()
        step=2
        for btn,vec in thumby2.buttons.DPAD_VECTORS:
            if btn.down:
                g.panGameOverView((vec[0]*step,vec[1]*step))
        if thumby2.buttons.A.down or thumby2.buttons.B.down:
            return True

def showTitleImg():
    with open(GAME_DIR+"/Title.bin","b") as f:
        data=f.read()
    gs_b.blit(data,0,0,72,40)
    gs_sh.blit(memoryview(data)[360:],0,0,72,40)
    del data
    for b in gs_lg:
        b.text35().printXY("Press A",40,0)
    gs.show()
    thumby2.buttons.wait()

with gs:
    showTitleImg()
    data={}
    while main(data):
        pass
