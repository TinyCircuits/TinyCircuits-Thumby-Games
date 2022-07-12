GAME_NAME="MineSweep"
GAME_DIR=f"/Games/{GAME_NAME}"

import io
import os
import random
import thumby
import time

thumby2=__import__(GAME_DIR+"/lib/thumby2")

MODES=[
    {"name":"Beginner","size":(9,9),"mines":10},
    {"name":"Intermed.","size":(16,16),"mines":40},
    {"name":"Advanced","size":(30,16),"mines":99},
]

SIDE=9

DIGIT35_BLITS=[
    # BITMAP: width: 3, height: 5
    bytearray([31,17,31]),
    # BITMAP: width: 3, height: 5
    bytearray([0,31,0]),
    # BITMAP: width: 3, height: 5
    bytearray([29,21,23]),
    # BITMAP: width: 3, height: 5
    bytearray([17,21,31]),
    # BITMAP: width: 3, height: 5
    bytearray([7,4,31]),
    # BITMAP: width: 3, height: 5
    bytearray([23,21,29]),
    # BITMAP: width: 3, height: 5
    bytearray([31,21,29]),
    # BITMAP: width: 3, height: 5
    bytearray([1,1,31]),
    # BITMAP: width: 3, height: 5
    bytearray([31,21,31]),
    # BITMAP: width: 3, height: 5
    bytearray([23,21,31]),
]
# BITMAP: width: 3, height: 5
DIGIT35_QUESTION_BLIT=bytearray([1,21,7])

def drawMinesLeft35(num,x,y):
    if num>=10:
        thumby.display.blit(DIGIT35_BLITS[num//10],x,y,3,5,-1,False,False)
        x+=4
    if num<0:
        blit=DIGIT35_QUESTION_BLIT
    else:
        blit=DIGIT35_BLITS[num%10]
    thumby.display.blit(blit,x,y,3,5,-1,False,False)

MINE_DIGIT_BLITS=[
    # BITMAP: width: 4, height: 6
    bytearray([0,8,4,0]),
    # BITMAP: width: 4, height: 6
    bytearray([0,34,63,32]),
    # BITMAP: width: 4, height: 6
    bytearray([34,49,41,38]),
    # BITMAP: width: 4, height: 6
    bytearray([18,33,37,26]),
    # BITMAP: width: 4, height: 6
    bytearray([12,10,63,8]),
    # BITMAP: width: 4, height: 6
    bytearray([39,37,37,25]),
    # BITMAP: width: 4, height: 6
    bytearray([30,37,37,25]),
    # BITMAP: width: 4, height: 6
    bytearray([1,49,13,3]),
    # BITMAP: width: 4, height: 6
    bytearray([26,37,37,26]),
]

def drawMineDigit(digit,x,y):
    blit=MINE_DIGIT_BLITS[digit]
    if blit:
        thumby.display.blit(blit,x+3,y+2,4,6,-1,False,False)

# BITMAP: width: 6, height: 6
MINE_BLIT=bytearray([18,45,30,30,45,18])
# BITMAP: width: 10, height: 10
EXPLODED_MINE_BLIT=bytearray([75,181,74,181,122,122,181,74,181,75,3,2,1,2,1,1,2,1,2,3])

def drawMine(x,y):
    thumby.display.blit(MINE_BLIT,x+2,y+2,6,6,-1,False,False)

def drawExplodedMine(x,y):
    thumby.display.blit(EXPLODED_MINE_BLIT,x,y,10,10,-1,False,False)

# BITMAP: width: 6, height: 6
FLAG_BLIT=bytearray([5,39,55,63,48,32])
# BITMAP: width: 6, height: 6
BAD_FLAG_BLIT=bytearray([0,37,50,61,48,32])

def drawFlag(x,y):
    thumby.display.blit(FLAG_BLIT,x+2,y+2,6,6,-1,False,False)

def drawBadFlag(x,y):
    thumby.display.blit(BAD_FLAG_BLIT,x+2,y+2,6,6,-1,False,False)

CURSOR_BLITS=[
    # BITMAP: width: 8, height: 8
    bytearray([153,129,0,0,129,129,0,102]),
    # BITMAP: width: 8, height: 8
    bytearray([204,1,1,128,128,1,1,204]),
]

CURSOR_CHANGE_INTERVAL_MS=150

def drawCursor(x,y):
    fr=(time.ticks_ms()//CURSOR_CHANGE_INTERVAL_MS)%4
    thumby.display.blit(CURSOR_BLITS[fr%2],
        x+1,y+1,8,8,0,fr==2,fr==3)

F_NUM_MASK=0b00001111
F_MINE=0b00010000
F_OPEN=0b00100000
F_FLAG=0b01000000

# BITMAP: width: 6, height: 8
DISABLE_TEXT57_BLIT=bytearray([219,109,182,219,109,182])

def disableText57(len,row,col):
    for ch in range(len):
        thumby.display.blit(DISABLE_TEXT57_BLIT,
            (col+ch)*6,row*8,6,8,1,False,False)

def menuChoice(numOptions,startRow=0,selOption=0):
    while True:
        thumby2.display.text.clear(startRow,rows=numOptions,columns=1)
        thumby2.display.text.print(">",startRow+selOption)
        thumby2.display.show()
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
        return Game.deserialise(save)

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
        with open(save_file.PATH,"wb") as f:
            f.write(game.serialise())

class Game:

    NEIGHBOURS=[(1,0),(1,1),(0,1),(-1,1),(-1,0),(-1,-1),(0,-1),(1,-1)]

    SCROLLBAR_WIDTH=2
    SCROLL_BLOCK_WIDTH=1
    BOARD_FILL_RANGE_X=(2,71-SCROLLBAR_WIDTH-1)
    BOARD_FILL_RANGE_Y=(8,39-SCROLLBAR_WIDTH-1)
    PREFERRED_POS_RANGE_X=(2*SIDE+2,71-SCROLLBAR_WIDTH-(2*SIDE+2))
    PREFERRED_POS_Y=(39-SCROLLBAR_WIDTH-SIDE)//2

    def __init__(self,mode):
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
        thumby.display.fill(0)
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
            scrollTo=(boardFillRange[1]-offset)*scrollbarLen//size
            return (offset,(scrollFrom,scrollTo-scrollFrom))
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
            thumby2.display.drawLineV(x*SIDE+x0,y0,yy*SIDE+y0,1)
        for y in range(yy+1):
            thumby2.display.drawLineH(x0,y*SIDE+y0,xx*SIDE+x0,1)
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
        minesLeft=self.mines-self.numFlags
        minesLeftWid=3
        if minesLeft>=10:
            minesLeftWid+=4
        thumby2.display.fillRect(0,0,minesLeftWid+3,8,0)
        thumby2.display.drawLineH(0,6,minesLeftWid+1,1)
        thumby2.display.drawLineV(minesLeftWid+1,0,6,1)
        drawMinesLeft35(minesLeft,0,0)
        if self.running:
            drawCursor(x0+self.pos[0]*SIDE+dPos[0],y0+self.pos[1]*SIDE+dPos[1])
        scrollWid=Game.SCROLLBAR_WIDTH
        scrollBlockWid=Game.SCROLL_BLOCK_WIDTH
        thumby2.display.fillRect(0,40-scrollWid,72-scrollWid,scrollWid,0)
        thumby2.display.fillRect(72-scrollWid,0,scrollWid,40,0)
        thumby2.display.fillRect(
            xScroll[0],40-scrollBlockWid,xScroll[1],scrollBlockWid,1)
        thumby2.display.fillRect(
            72-scrollBlockWid,yScroll[0],scrollBlockWid,yScroll[1],1)
        if not self.running:
            text="YOU WIN!" if self.win else "GAME OVER"
            textW=len(text)*6-1
            textX=71-textW
            thumby2.display.fillRect(textX-3,0,textW+6,10,0)
            thumby2.display.drawRect(textX-2,-1,textW+5,10,1)
            thumby.display.drawText(text,textX,0,1)

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
            g=Game({"size":size,"mines":mines})
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
    for i,c in enumerate(text):
        thumby.display.drawText(c,x0+7*i,0,1)
        thumby.display.drawText(c,x0+7*i+1,0,1)

def main(data):
    thumby2.display.text.font57i1()
    loadedGame=save_file.load()
    thumby.display.fill(0)
    drawLogo()
    thumby2.display.text.print([m["name"] for m in MODES],1,1)
    loadText="Load"
    thumby2.display.text.print(loadText,1+len(MODES),1)
    if loadedGame is None:
        disableText57(len(loadText),1+len(MODES),1)
    if "mainMenuSelOption" in data:
        selOption=data["mainMenuSelOption"]
    elif loadedGame is None:
        selOption=0
    else:
        selOption=len(MODES)
    selOption=menuChoice(len(MODES)+1,startRow=1,selOption=selOption)
    if selOption is None:
        thumby2.display.text.clear(1,rows=4)
        thumby2.display.text.print("Exit",2)
        thumby2.display.show()
        time.sleep(1)
        return False
    data["mainMenuSelOption"]=selOption
    thumby2.display.text.clear(1,rows=4)
    if selOption==len(MODES):
        if loadedGame is None:
            thumby2.display.text.print(
                ["No saved","game.","Hold B in","game to save"],1)
            thumby2.display.show()
            thumby2.buttons.wait()
            return True
        g=loadedGame
        thumby2.display.text.print("Load game:",1)
        numFlagsStr=f"{g.numFlags}"
        thumby2.display.text.print(numFlagsStr,3)
        drawFlag(6*len(numFlagsStr)-1,3*8-1)
        if g.numFlags<=g.mines:
            thumby2.display.text.print(
                f"({100*g.numFlags//g.mines}%)",3,len(numFlagsStr)+2)
    else:
        g=Game(MODES[selOption])
        thumby2.display.text.print("New game:",1)
    paramsStr=f"{g.size[0]}x{g.size[1]}, {g.mines}"
    thumby2.display.text.print(paramsStr,2)
    drawMine(6*len(paramsStr)-1,2*8-1)
    thumby2.display.text.print("B=back  A=OK",4)
    thumby2.display.show()
    if thumby2.buttons.wait()==thumby2.buttons.B:
        return True
    thumby2.display.text.clear(1,rows=4)
    thumby2.display.text.print([
        "Controls:",
        "A=step/chord",
        "B=set flag",
        "hold B=menu",
    ],1)
    thumby2.display.show()
    if thumby2.buttons.wait()==thumby2.buttons.B:
        return True
    thumby2.buttons.assumeUp()
    if g==loadedGame:
        save_file.destroy()
        del data["mainMenuSelOption"]

    thumby.display.setFPS(40)
    while g.running:
        g.draw()
        thumby2.update()
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
                    thumby2.display.update()
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
                thumby2.display.show()
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
                        thumby.display.display.invert(inv)
                        inv=not inv
                        thumby2.audio.musicBlocking([(tone,40)])
                        tone-=3
        elif thumby2.buttons.B.edge<0 and thumby2.buttons.B.longPressEdge==0:
            g.flag(g.pos)
        elif thumby2.buttons.B.longPressEdge>0:
            thumby.display.fill(0)
            thumby2.display.text.print([
                "Pause menu",
                " Resume",
                " Give up",
                " Save & Menu",
                " Save & Exit",
            ],0)
            thumby2.display.show()
            sel=menuChoice(4,startRow=1)
            thumby2.buttons.assumeUp()
            if sel==1:
                g.giveUp()
            elif sel==2:
                save_file.save(g)
                return True
            elif sel==3:
                save_file.save(g)
                thumby.display.fill(0)
                drawLogo()
                thumby2.display.text.print(["Saved.","Exit"],2)
                thumby2.display.show()
                time.sleep(1)
                return False
    thumby2.buttons.assumeUp()
    while True:
        g.draw()
        thumby2.update()
        step=2
        for btn,vec in thumby2.buttons.DPAD_VECTORS:
            if btn.down:
                g.panGameOverView((vec[0]*step,vec[1]*step))
        if thumby2.buttons.A.down or thumby2.buttons.B.down:
            return True

def showTitleImg():
    with open(GAME_DIR+"/Title.bin","b") as f:
        data=f.read()
    thumby.display.blit(data,0,0,72,40,-1,False,False)
    del data
    thumby2.display.show()
    thumby2.buttons.wait()

showTitleImg()
data={}
while main(data):
    pass
thumby.reset()
