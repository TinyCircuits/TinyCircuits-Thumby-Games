GAME_NAME="Canvas"
GAME_DIR="/Games/"+GAME_NAME

import framebuf
import gc
import os
import re
import sys
import thumby
import time

thumby2=__import__(GAME_DIR+"/lib/thumby2")

thumby2.requireMinThumbyVersion("1.6")

@micropython.native
def scrollCalc(
        areaLen,contentLen,contentScroll,posInContent,posLen,
        preferredPosInAreaMargin0,preferredPosInAreaMargin1,
        minMarginAroundPos0,minMarginAroundPos1,
        smallContentAlignDir,
        scrollBarLen):
    if contentLen<=areaLen:
        scroll=-((areaLen-contentLen)*(smallContentAlignDir+1)//2)
        scrollBar=None
    else:
        scroll=min(max(contentScroll,
            posInContent+posLen+preferredPosInAreaMargin1-areaLen),
            posInContent-preferredPosInAreaMargin0)
        scroll=min(max(scroll,0),contentLen-areaLen)
        scrollBar=(
            (scrollBarLen-1)*scroll//contentLen,
            (scrollBarLen-1)*(scroll+areaLen)//contentLen,
        )
    scrollPosMargin=min(max(scroll,
        posInContent+posLen+minMarginAroundPos1-areaLen),
        posInContent-minMarginAroundPos0)
    if scrollPosMargin!=scroll and not scrollBar:
        scrollBar=(0,scrollBarLen-1)
    return (scrollPosMargin,scrollBar)

def menuChoice(options,row,rows,selOption=0):
    thumby2.buttons.assumeUp()
    selOption=min(max(selOption,0),len(options)-1)
    scroll=0
    while True:
        thumby2.display.text.clear(row,rows=rows)
        scroll,scrollBarRange=scrollCalc(
            rows,len(options),scroll,selOption,1,
            1,1,0,0,-1,rows*8)
        thumby2.display.text.print(">",row+selOption-scroll)
        for line in range(rows):
            rowInd=line+scroll
            if rowInd<len(options):
                text=options[rowInd]
                if isinstance(text,dict):
                    text=text["text"]
                    if callable(text):
                        text=text()
                thumby2.display.text.print(text,row+line,column=1)
        if scrollBarRange:
            thumby2.display.drawRect(
                70,8*row,2,8*len(options),0)
            thumby2.display.drawLineV(
                71,8*row+scrollBarRange[0],8*row+scrollBarRange[1],1)
        thumby2.display.show()
        time.sleep_ms(50)
        thumby2.buttons.update()
        if "onSelect" in options[selOption]:
            onSelect=options[selOption]["onSelect"]
            if thumby2.buttons.A.edge>0 or thumby2.buttons.RIGHT.edge>0:
                onSelect(1)
            elif thumby2.buttons.LEFT.edge>0:
                onSelect(-1)
        elif thumby2.buttons.A.edge>0:
            thumby2.buttons.assumeUp()
            return selOption
        if thumby2.buttons.B.edge>0:
            thumby2.buttons.assumeUp()
            return None
        for btn,dir in thumby2.buttons.UD_VALS:
            if btn.edge>0 or btn.longPress:
                newSelOption=selOption-dir
                if not 0<=newSelOption<len(options):
                    if btn.edge>0:
                        newSelOption%=len(options)
                    else:
                        newSelOption=selOption
                selOption=newSelOption
                break

def confirm(text,yesText="OK",noText="Cancel"):
    thumby.display.fill(0)
    if isinstance(text,str):
        text=[text]
    thumby2.display.text.print(text,0)
    return menuChoice([noText,yesText],len(text),2)==1

def simpleConfirm(text):
    thumby2.buttons.assumeUp()
    thumby.display.fill(0)
    scroll=0
    lHei=max(1,len(text)-4)
    while True:
        thumby.display.fill(0)
        scroll,scrollBar=scrollCalc(
            5,len(text),0,scroll,5,
            0,0,0,0,-1,40)
        thumby2.display.text.print(text,-scroll)
        if scrollBar:
            thumby2.display.drawRect(70,0,2,40,0)
            thumby2.display.drawLineV(71,scrollBar[0],scrollBar[1],1)
        thumby2.display.show()
        time.sleep_ms(50)
        thumby2.buttons.update()
        if thumby2.buttons.A.edge>0 or thumby2.buttons.B.edge>0:
            res=thumby2.buttons.A.edge>0
            thumby2.buttons.assumeUp()
            return res
        for btn,dir in thumby2.buttons.UD_VALS:
            if btn.edge>0 or btn.longPress:
                scroll=min(max(scroll-dir,0),lHei-1)
                break

# BITMAP: width: 5, height: 3
UP_ARROW_BLIT=bytearray([4,2,1,2,4])

def enterSize(size,text="Canvas size:"):
    thumby2.buttons.assumeUp()
    thumby.display.fill(0)
    thumby2.display.text.print(text,0)
    xy=list(size)
    column=0
    while True:
        thumby2.display.text.clear(1,rows=3)
        xStr,yStr=map(str,xy)
        thumby2.display.text.print(f"<{xStr}x{yStr}>",2)
        arrowsX=3*len(xStr)+3 if column==0 else 3*len(yStr)+6*len(xStr)+9
        thumby.display.blit(UP_ARROW_BLIT,arrowsX,10,5,3,-1,False,False)
        thumby.display.blit(UP_ARROW_BLIT,arrowsX,26,5,3,-1,False,True)
        thumby2.display.show()
        time.sleep_ms(10)
        thumby2.buttons.update()
        if thumby2.buttons.A.edge>0:
            thumby2.buttons.assumeUp()
            return tuple(xy)
        if thumby2.buttons.B.edge>0:
            thumby2.buttons.assumeUp()
            return None
        for btn,v in thumby2.buttons.UD_VALS:
            if btn.edge>0 or btn.longPress:
                val=xy[column]
                incr=max(min((btn.downTimeMs()//500)**2,val//10),1)
                xy[column]=min(max(val+v*incr,1),9999)
        for btn in thumby2.buttons.RL:
            if btn.edge>0:
                column^=1

ALPHABET="".join([chr(c) for c in range(ord("A"),ord("Z")+1)])
NAME_CHARS=" "+ALPHABET+ALPHABET.lower()+"0123456789,+-"

def enterName(name,text):
    thumby2.buttons.assumeUp()
    thumby.display.fill(0)
    thumby2.display.text.print(text,0)
    thumby2.display.text.print("A=save",4,6)
    nn=[0]*10
    for i in range(len(name)):
        nn[i]=max(0,NAME_CHARS.find(name[i]))
    column=min(max(len(name)-1,0),len(nn)-1)
    if nn.count(0)==len(nn):
        nn[column]=1
    while True:
        thumby2.display.text.clear(1,rows=3)
        str="".join(NAME_CHARS[i] for i in nn)
        thumby2.display.text.print("<"+str+">",2)
        thumby.display.blit(UP_ARROW_BLIT,6+column*6,10,5,3,-1,False,False)
        thumby.display.blit(UP_ARROW_BLIT,6+column*6,26,5,3,-1,False,True)
        thumby2.display.show()
        time.sleep_ms(15)
        thumby2.buttons.update()
        if thumby2.buttons.A.edge>0:
            thumby2.buttons.assumeUp()
            newNn=[0]*len(nn)
            i=0
            for j in range(len(nn)):
                if nn[j]!=0:
                    newNn[i]=nn[j]
                    i+=1
            if newNn==nn:
                str=str.strip()
                if len(str)==0:
                    return
                return str
            column=max(0,column-nn[:column+1].count(0))
            nn=newNn
        if thumby2.buttons.B.edge>0:
            thumby2.buttons.assumeUp()
            return None
        for btn,v in thumby2.buttons.UD_VALS:
            if btn.edge>0 or btn.longPress:
                nn[column]=(nn[column]+v)%len(NAME_CHARS)
        for btn,v in thumby2.buttons.RL_VALS:
            if btn.edge>0 or btn.longPress:
                column=(column+v)%len(nn)

class save_files:

    DIR="/Saves/"+GAME_NAME
    DIRS=["/Saves",DIR]

    DEMOS_DIR=GAME_DIR+"/demos"

    PANIC_NAME="_PANIC"
    CLIP_PREFIX="Clip-"

    FILE_NAME_WITH_SIZE_RE=re.compile("^(.+)_(\d+)+x(\d+)\.bin$")

    TYPE_NORMAL=" "
    TYPE_CLIP="#"
    TYPE_DEMO="+"
    TYPE_PANIC="!"

    TYPES_PRIORITY=TYPE_NORMAL+TYPE_CLIP+TYPE_DEMO+TYPE_PANIC

    @staticmethod
    def list(typesPriority=""):
        save_files._ensureDirs()
        res=[]
        for dir,type in [
            (save_files.DIR,save_files.TYPE_NORMAL),
            (save_files.DEMOS_DIR,save_files.TYPE_DEMO),
        ]:
            for f in os.listdir(dir):
                path=f"{dir}/{f}"
                if save_files.isFile(path):
                    mat=save_files.FILE_NAME_WITH_SIZE_RE.match(f)
                    if mat:
                        name=mat.group(1)
                        fType=type
                        if type==save_files.TYPE_NORMAL:
                            if name==save_files.PANIC_NAME:
                                fType=save_files.TYPE_PANIC
                            elif name.startswith(save_files.CLIP_PREFIX):
                                fType=save_files.TYPE_CLIP
                        res.append({
                            "path":path,
                            "name":name,
                            "listName":"%-10s%s"%(name,fType),
                            "size":tuple(int(mat.group(g)) for g in [2,3]),
                            "type":fType,
                        })
        typesPriority+=save_files.TYPES_PRIORITY
        return sorted(res,key=lambda s:
            (typesPriority.find(s["type"]),s["name"],s["size"]))

    @staticmethod
    def _listEquivSavesPaths(name):
        save_files._ensureDirs()
        res=[]
        for f in os.listdir(save_files.DIR):
            path=f"{save_files.DIR}/{f}"
            if save_files.isFile(path):
                mat=save_files.FILE_NAME_WITH_SIZE_RE.match(f)
                if mat and mat.group(1)==name:
                    res.append(path)
        return res

    @staticmethod
    def loadBytes(descriptor):
        gc.collect()
        buf=bytearray(bufLen(descriptor["size"]))
        with open(descriptor["path"],"b") as f:
            f.readinto(buf)
        return buf

    @staticmethod
    def delete(name):
        paths=save_files._listEquivSavesPaths(name)
        if len(paths):
            for f in paths:
                os.remove(f)
            return True
        return False

    @staticmethod
    def exists(name):
        return len(save_files._listEquivSavesPaths(name))

    @staticmethod
    def save(name,size,buffer):
        save_files._ensureDirs()
        save_files.delete(name)
        path=f"{save_files.DIR}/{name}_{size[0]}x{size[1]}.bin"
        with open(path,"wb") as f:
            f.write(buffer)

    @staticmethod
    def panicSave(canvas):
        save_files.save(save_files.PANIC_NAME,canvas.size,canvas.getBuffer())

    @staticmethod
    def _ensureDirs():
        for dir in save_files.DIRS:
            try:
                os.mkdir(dir)
            except OSError as e:
                if e.errno!=errno.EEXIST:
                    raise e

    @staticmethod
    def isFile(path):
        try:
            return os.stat(path)[0]&(1<<15)!=0
        except OSError as e:
            if e.errno==errno.ENOENT:
                return False
            raise e

    @staticmethod
    def saveException(exc):
        save_files._ensureDirs()
        with open(f"{save_files.DIR}/{save_files.PANIC_NAME}.txt","w") as f:
            sys.print_exception(exc,f)

class CircularUndo:

    def __init__(self,size):
        self.size=size
        self.history=[None]*size
        self.clear()

    def clear(self):
        self.bottom=0
        self.top=0
        self.index=0

    def do(self,item):
        self.history[self.index]=item
        self.index=(self.index+1)%self.size
        self.top=self.index
        if self.top==self.bottom:
            self.bottom=(self.bottom+1)%self.size

    def undo(self):
        if self.index!=self.bottom:
            self.index=(self.index-1)%self.size
            return self.history[self.index]

    def redo(self):
        if self.index!=self.top:
            res=self.history[self.index]
            self.index=(self.index+1)%self.size
            return res

def bufLen(size):
    return size[0]*((size[1]+7)//8)

class FBuf:

    def __init__(self,size,buf=None):
        if not buf:
            buf=bytearray(bufLen(size))
        self.raw=buf
        self.fb=framebuf.FrameBuffer(buf,size[0],size[1],framebuf.MONO_VLSB)

class CanvasSettings:

    def __init__(self):
        self.showStatus=False
        self.showFrame=True

    def toggleShowStatus(self):
        self.showStatus^=True

    def toggleShowFrame(self):
        self.showFrame^=True

settings=CanvasSettings()

class Canvas:

    CURSOR_CYCLE=8

    ZOOM_LEVELS=[1,2,3,5,7,11]

    RECT_SEL_MODE_CORNER=1
    RECT_SEL_MODE_SIZE=2

    def __init__(self,size,buf=None,name=None):
        self.name=name
        self.size=size
        self.width=size[0]
        self.height=size[1]
        self.buf=FBuf(size,buf)
        self._centerPos()
        self.scrollX=0
        self.scrollY=0
        self.zoom=0
        self.pixelSize=Canvas.ZOOM_LEVELS[self.zoom]
        self.zoomBuf=FBuf((72,40))
        self.zoomBufValid=False
        self.cursorPhase=0
        self.undoManager=CircularUndo(500)
        self.modified=False
        self.statusStr=None
        self.rectSelMode=None

    def getBuffer(self):
        return self.buf.raw

    def moveBy(self,vec,allowWrap:bool=False):
        return self.moveTo((self.posX+vec[0],self.posY+vec[1]),allowWrap)

    @micropython.native
    def moveTo(self,pos,allowWrap:bool=False):
        if self.rectSelMode and self.rectSelMode[0]==Canvas.RECT_SEL_MODE_SIZE:
            rectSelSize=self.rectSelMode[1]
        else:
            rectSelSize=None
        if rectSelSize:
            allowWrap=False
        negX=rectSelSize[0]-1 if rectSelSize else 0
        negY=rectSelSize[1]-1 if rectSelSize else 0
        def np(p:int,neg:int,len:int)->int:
            if not -neg<=p<len:
                if allowWrap:
                    p%=len
                else:
                    p=int(min(max(p,-neg),len-1))
            return p
        posX=np(pos[0],negX,self.width)
        posY=np(pos[1],negY,self.height)
        if posX!=self.posX or posY!=self.posY:
            self.posX=posX
            self.posY=posY
            self.cursorPhase=0
            self.statusStr=None
            return True
        return False

    def toggle(self):
        self._markModified()
        self.undoManager.do((self.posX,self.posY))
        self._togglePixel(self.posX,self.posY)

    def undo(self):
        pos=self.undoManager.undo()
        if pos:
            self._togglePixel(pos[0],pos[1])
            self.moveTo(pos)
            return True
        return False

    def redo(self):
        pos=self.undoManager.redo()
        if pos:
            self._togglePixel(pos[0],pos[1])
            self.moveTo(pos)
            return True
        return False

    @micropython.native
    def _togglePixel(self,x,y):
        col=not self.buf.fb.pixel(x,y)
        self.buf.fb.pixel(x,y,col)
        if self.zoomBufValid:
            self.zoomBuf.fb.fill_rect(
                x*self.pixelSize-self.scrollX,y*self.pixelSize-self.scrollY,
                self.pixelSize,self.pixelSize,col)

    @micropython.native
    def invertRect(self,rect):
        rx,ry,rw,rh=rect
        fb=self.buf.fb
        for x in range(rx,rx+rw):
            for y in range(ry,ry+rh):
                fb.pixel(x,y,not fb.pixel(x,y))
        self._markBigChange()

    def fillRect(self,rect,color):
        rx,ry,rw,rh=rect
        self.buf.fb.fill_rect(rx,ry,rw,rh,color)
        self._markBigChange()

    @micropython.native
    def flipHRect(self,rect):
        rx,ry,rw,rh=rect
        fb=self.buf.fb
        for px in range(rw//2):
            x=rx+px
            x2=rx+rw-1-px
            for y in range(ry,ry+rh):
                self._swap(fb,x,y,x2,y)
        self._markBigChange()

    @micropython.native
    def flipVRect(self,rect):
        rx,ry,rw,rh=rect
        fb=self.buf.fb
        for py in range(rh//2):
            y=ry+py
            y2=ry+rh-1-py
            for x in range(rx,rx+rw):
                self._swap(fb,x,y,x,y2)
        self._markBigChange()

    @micropython.native
    def flipHVRect(self,rect):
        rx,ry,rw,rh=rect
        fb=self.buf.fb
        for px in range(rw//2):
            x=rx+px
            x2=rx+rw-1-px
            for py in range(rh):
                self._swap(fb,x,ry+py,x2,ry+rh-1-py)
        if rw%2==1:
            xc=rx+rw//2
            for py in range(rh//2):
                self._swap(fb,xc,ry+py,xc,ry+rh-1-py)
        self._markBigChange()

    @micropython.native
    def _swap(self,fb,x1,y1,x2,y2):
        p1=fb.pixel(x1,y1)
        fb.pixel(x1,y1,fb.pixel(x2,y2))
        fb.pixel(x2,y2,p1)

    def crop(self,rect):
        if self._reframe((rect[2],rect[3]),-rect[0],-rect[1]):
            self._centerPos()
            return True
        return False

    def _centerPos(self):
        self.posX=(self.width-1)//2
        self.posY=(self.height-1)//2

    def _reframe(self,newSize,px,py):
        oldBuf=self.buf
        gc.collect()
        try:
            self.buf=FBuf(newSize)
        except MemoryError:
            self.buf=oldBuf
            simpleConfirm(["MemoryError","","Try smaller","canvas."])
            return False
        self.size=newSize
        self.width=newSize[0]
        self.height=newSize[1]
        self.buf.fb.blit(oldBuf.fb,px,py)
        del oldBuf
        gc.collect()
        self.posX+=px
        self.posY+=py
        self.scrollX+=px
        self.scrollY+=py
        self._markBigChange()
        return True

    def rotate(self,rotRight):
        newSize=(self.height,self.width)
        oldBuf=self.buf
        gc.collect()
        try:
            self.buf=FBuf(newSize)
        except MemoryError:
            self.buf=oldBuf
            simpleConfirm(["MemoryError","","Cannot","rotate."])
            return False
        self.size=newSize
        self.width=newSize[0]
        self.height=newSize[1]
        self._copyRot(oldBuf.fb,rotRight)
        del oldBuf
        gc.collect()
        self._centerPos()
        self.scrollX=0
        self.scrollY=0
        self._markBigChange()
        return True

    @micropython.native
    def _copyRot(self,prevFb,rotRight):
        if rotRight:
            sx,sy=0,self.width-1
            dx,dy=1,-1
        else:
            sx,sy=self.height-1,0
            dx,dy=-1,1
        fb=self.buf.fb
        srcY=sy
        for x in range(self.width):
            for y in range(self.height):
                if prevFb.pixel(sx+y*dx,srcY):
                    fb.pixel(x,y,1)
            srcY+=dy

    def copy(self,rect):
        rx,ry,rw,rh=rect
        gc.collect()
        try:
            buf=FBuf((rw,rh))
        except MemoryError:
            simpleConfirm(["MemoryError","","Try smaller","rect."])
            return
        buf.fb.blit(self.buf.fb,-rx,-ry)
        return buf

    def paste(self,src,x,y,key=-1):
        self.buf.fb.blit(src.fb,x,y,key)
        self._markBigChange()

    def changeZoom(self,dir,allowWrap=False):
        zoom=self.zoom+dir
        if allowWrap:
            zoom%=len(Canvas.ZOOM_LEVELS)
        self.setZoom(zoom)

    @micropython.native
    def setZoom(self,zoom:int):
        zoom=min(max(zoom,0),len(Canvas.ZOOM_LEVELS)-1)
        if zoom!=self.zoom:
            onScreenX=self.posX*self.pixelSize+self.pixelSize//2-self.scrollX
            onScreenY=self.posY*self.pixelSize+self.pixelSize//2-self.scrollY
            self.zoom=zoom
            self.pixelSize=Canvas.ZOOM_LEVELS[zoom]
            self.scrollX=self.posX*self.pixelSize+self.pixelSize//2-onScreenX
            self.scrollY=self.posY*self.pixelSize+self.pixelSize//2-onScreenY
            self.zoomBufValid=False
            self.cursorPhase=0

    def _markBigChange(self):
        self._markModified()
        self.rectSelMode=None
        self.zoomBufValid=False
        self.undoManager.clear()
        self.posX=min(max(self.posX,0),self.width-1)
        self.posY=min(max(self.posY,0),self.height-1)

    def _markModified(self):
        if not self.modified:
            self.modified=True
            self.statusStr=None

    def markSaved(self,name):
        self.name=name
        self.modified=False
        self.statusStr=None

    @micropython.native
    def draw(self):
        pixelSize=self.pixelSize
        canvasLenX,canvasLenY=72,40
        showStatus=settings.showStatus or self.rectSelMode
        if showStatus:
            canvasLenY-=6
        areaLenX,areaLenY=canvasLenX,canvasLenY
        scrollBarLenX,scrollBarLenY=areaLenX,areaLenY
        curMarg=2 if self.rectSelMode else 0
        def scrollCalcX():
            marg=(areaLenX-32)//2
            return scrollCalc(
                areaLenX,self.width*pixelSize,self.scrollX,
                max(self.posX,0)*pixelSize,pixelSize,
                marg,marg,curMarg,curMarg,
                0,scrollBarLenX)
        def scrollCalcY():
            marg=(areaLenY-pixelSize)//2
            return scrollCalc(
                areaLenY,self.height*pixelSize,self.scrollY,
                max(self.posY,0)*pixelSize,pixelSize,
                marg,marg,curMarg,curMarg,
                0,scrollBarLenY)
        scrollY,scrollBarY=scrollCalcY()
        if scrollBarY:
            areaLenX-=2
            scrollBarLenX-=1
        scrollX,scrollBarX=scrollCalcX()
        if scrollBarX:
            areaLenY-=2
            scrollBarLenY-=1
            scrollY,newScrollBarY=scrollCalcY()
            if newScrollBarY and not scrollBarY:
                areaLenX-=2
                scrollBarLenX-=1
                scrollX,scrollBarX=scrollCalcX()
            scrollBarY=newScrollBarY
        scrollDx=scrollX-self.scrollX
        scrollDy=scrollY-self.scrollY
        self.scrollX=scrollX
        self.scrollY=scrollY
        thumby.display.fill(0)
        if self.zoom==0:
            thumby.display.blit(
                self.buf.raw,-scrollX,-scrollY,
                self.width,self.height,
                -1,False,False)
        else:
            if self.zoomBufValid:
                if scrollDx!=0 or scrollDy!=0:
                    if abs(scrollDx)>=72 or abs(scrollDy)>=40:
                        self.zoomBufValid=False
                    else:
                        self.zoomBuf.fb.scroll(-scrollDx,-scrollDy)
                        if scrollDy!=0:
                            if scrollDy<0:
                                iy0,iy1=0,-scrollDy
                            else:
                                iy0,iy1=40-scrollDy,40
                            self.zoomBuf.fb.fill_rect(0,iy0,72,iy1-iy0,0)
                            self._redrawZoomBufY(iy0,iy1)
                        if scrollDx!=0:
                            if scrollDx<0:
                                ix0,ix1=0,-scrollDx
                            else:
                                ix0,ix1=72-scrollDx,72
                            self.zoomBuf.fb.fill_rect(ix0,0,ix1-ix0,40,0)
                            self._redrawZoomBufX(ix0,ix1)
            if not self.zoomBufValid:
                self.zoomBuf.fb.fill(0)
                self._redrawZoomBufY(0,40)
                self.zoomBufValid=True
            thumby.display.blit(self.zoomBuf.raw,0,0,72,40,-1,False,False)
        if settings.showFrame:
            thumby2.display.drawRect(
                -self.scrollX-2,-self.scrollY-2,
                self.width*pixelSize+4,self.height*pixelSize+4,1)
        if self.rectSelMode:
            rx,ry,rw,rh=self._rectSelRect()
            scrX=rx*pixelSize-self.scrollX
            scrY=ry*pixelSize-self.scrollY
            color=self.cursorPhase<4
            thumby2.display.drawLineH(scrX-1,scrY-2,scrX+rw*pixelSize,color)
            thumby2.display.drawLineH(scrX-1,scrY+rh*pixelSize+1,scrX+rw*pixelSize,color)
            thumby2.display.drawLineV(scrX-2,scrY-1,scrY+rh*pixelSize,color)
            thumby2.display.drawLineV(scrX+rw*pixelSize+1,scrY-1,scrY+rh*pixelSize,color)
            thumby2.display.drawRect(scrX-1,scrY-1,rw*pixelSize+2,rh*pixelSize+2,not color)
        scrX=self.posX*pixelSize-self.scrollX
        scrY=self.posY*pixelSize-self.scrollY
        color=not self.buf.fb.pixel(self.posX,self.posY)
        if not self.rectSelMode or self.rectSelMode[0]!=Canvas.RECT_SEL_MODE_SIZE:
            if self.pixelSize<=2:
                if self.cursorPhase==0:
                    thumby2.display.fillRect(scrX,scrY,pixelSize,pixelSize,color)
            else:
                thumby.display.setPixel(scrX+pixelSize//2,scrY+pixelSize//2,color)
        if areaLenX<72:
            thumby2.display.fillRect(areaLenX,0,72-areaLenX,40,0)
        if areaLenY<40:
            thumby2.display.fillRect(0,areaLenY,areaLenX,40-areaLenY,0)
        if scrollBarX:
            thumby2.display.drawLineH(scrollBarX[0],canvasLenY-1,scrollBarX[1],1)
        if scrollBarY:
            thumby2.display.drawLineV(canvasLenX-1,scrollBarY[0],scrollBarY[1],1)
        if showStatus:
            thumby.display.drawText(self._getStatusStr(),0,35,1)
        self.cursorPhase=(self.cursorPhase+1)%Canvas.CURSOR_CYCLE

    @micropython.native
    def _redrawZoomBufY(self,y0:int,y1:int):
        pixelSize=self.pixelSize
        sy=-self.scrollY
        for y in range(self.height):
            if y0-pixelSize<sy<y1:
                for x in range(self.width):
                    if self.buf.fb.pixel(x,y):
                        sx=x*pixelSize-self.scrollX
                        self.zoomBuf.fb.fill_rect(
                            sx,sy,pixelSize,pixelSize,1)
            sy+=pixelSize

    @micropython.native
    def _redrawZoomBufX(self,x0:int,x1:int):
        pixelSize=self.pixelSize
        sx=-self.scrollX
        for x in range(self.width):
            if x0-pixelSize<sx<x1:
                for y in range(self.height):
                    if self.buf.fb.pixel(x,y):
                        sy=y*pixelSize-self.scrollY
                        self.zoomBuf.fb.fill_rect(
                            sx,sy,pixelSize,pixelSize,1)
            sx+=pixelSize

    def _getStatusStr(self):
        if not self.statusStr:
            if self.rectSelMode:
                _,_,w,h=self._rectSelRect()
                n=f"{w}x{h}"
            else:
                n=self.name or ""
                if self.modified:
                    n="*"+n
            n="%-18s"%n
            p=f"{self.posX},{self.posY}"
            self.statusStr=n[:17-len(p)]+" "+p
        return self.statusStr

    def rectSelStartCorner(self):
        self.rectSelMode=(Canvas.RECT_SEL_MODE_CORNER,(self.posX,self.posY))
        self.statusStr=None

    def rectSelStartSize(self,size):
        self.rectSelMode=(Canvas.RECT_SEL_MODE_SIZE,size)
        self.statusStr=None

    def rectSelEnd(self):
        rect=self._rectSelRect()
        self.rectSelMode=None
        self.statusStr=None
        return rect

    def _rectSelRect(self):
        m=self.rectSelMode[0]
        if m==Canvas.RECT_SEL_MODE_CORNER:
            cx,cy=self.rectSelMode[1]
            xs=sorted([cx,self.posX])
            ys=sorted([cy,self.posY])
            return (xs[0],ys[0],xs[1]-xs[0]+1,ys[1]-ys[0]+1)
        if m==Canvas.RECT_SEL_MODE_SIZE:
            sx,sy=self.rectSelMode[1]
            return (self.posX,self.posY,sx,sy)

    def fullRect(self):
        return (0,0,self.width,self.height)

def drawTitle():
    text="Canvas"
    x0=(72-len(text)*7)//2
    for i,c in enumerate(text):
        thumby.display.drawText(c,x0+7*i,0,1)
        thumby.display.drawText(c,x0+7*i+1,0,1)

def tryLoadBytes(descriptor):
    name=descriptor["name"]
    w,h=descriptor["size"]
    thumby.display.fill(0)
    thumby2.display.text.print([name,"%12s"%f"{w}x{h}"],0)
    isDemo=descriptor["type"]==save_files.TYPE_DEMO
    opts=["Cancel","Load"]
    if isDemo:
        thumby2.display.text.print("(demo)",2)
        freeRow=3
    else:
        opts.insert(0,"Delete")
        freeRow=2
    selInd=menuChoice(opts,freeRow,5-freeRow,selOption=len(opts)-1)
    if selInd is None:
        return
    sel=opts[selInd]
    if sel=="Delete":
        save_files.delete(name)
        simpleConfirm(["Deleted:",name])
    elif sel=="Load":
        return save_files.loadBytes(descriptor)

def loadCanvas():
    thumby2.buttons.assumeUp()
    selOption=0
    while True:
        saves=save_files.list(save_files.TYPE_PANIC)
        thumby.display.fill(0)
        thumby2.display.text.print("Load canvas:",0)
        selOption=menuChoice([s["listName"] for s in saves],1,4,selOption)
        if selOption is None:
            return
        sd=saves[selOption]
        bs=tryLoadBytes(sd)
        if bs:
            return Canvas(sd["size"],bs,sd["name"])

def saveCanvas(c):
    name=enterName(c.name or "","Save:")
    if name:
        if _save(c,name,c.name):
            return True
    return False

FINAL_DIGITS_RE=re.compile("^(.*?)(\d+)$")

def saveCanvasAs(c):
    if c.name:
        mat=FINAL_DIGITS_RE.match(c.name)
        if mat:
            pName="%s%0*d"%(mat.group(1),len(mat.group(2)),int(mat.group(2))+1)
        else:
            pName=c.name+"1"
    else:
        pName=""
    name=enterName(pName,"Save as:")
    if name:
        if _save(c,name):
            return True
    return False

def _save(c,name,canOverwriteName=None):
    rSizeStr="%12s"%f"{c.width}x{c.height}"
    if name!=canOverwriteName and save_files.exists(name):
        if not confirm(["Exists:",name,rSizeStr],"Overwrite"):
            return False
    save_files.save(name,c.size,c.getBuffer())
    c.markSaved(name)
    simpleConfirm(["Saved as:",name,rSizeStr])
    return True

SHORT_HELP="""\
Draw with A

Hold B for
menu
""".splitlines()

HELP="""\
Canvas by
     TPReal

Controls:

Dir=
 move pen
A=
 draw point
A+Dir=
 draw line,
 also slant
B+Up/Dn=
 zoom +/-
B+L/R=
 undo/redo
hold B=
 draw menu

Draw menu:

Canvas op.:
 Perform
 operation
 on the who-
 le canvas.
 NO UNDO!

Rect op.:
 Perform
 operation
 on a se-
 lected
 rectangle
 area.
 NO UNDO!

Crop:
 Crop the
 canvas to
 selected
 area.
 NO UNDO!

Reframe:
 Change si-
 ze and/or
 pan.
 NO UNDO!

Copy:
 Save rect
 area to
 clipboard
 file.

Paste:
 Paste from
 a file.

Status:
 Turn on /
 off status
 bar.

Frame:
 Turn on /
 off frame
 around
 canvas.

Saves dir:
/Saves/
     Canvas
""".splitlines()

def selectRect(c):
    thumby2.buttons.assumeUp()
    thumby2.display.text.font35i1()
    while True:
        c.draw()
        thumby2.update()
        dpadAnyDown=False
        if thumby2.buttons.A.edge>0 or thumby2.buttons.B.edge>0:
            rect=c.rectSelEnd()
            res=rect if thumby2.buttons.A.edge>0 else None
            thumby2.buttons.assumeUp()
            thumby2.display.text.font57i1()
            return res
        for btn,vec in thumby2.buttons.DPAD_VECTORS:
            if (btn.edge<0 and btn.longPressEdge==0) or \
                btn.downTimeMs()>=CANVAS_DPAD_LONG_PRESS_MS:
                    c.moveBy(vec,btn.edge<0)

RECT_OPS=["Flip H","Flip V","Rotate 180","Invert","Clear !","Fill !"]
CANVAS_OPS=["Rotate R","Rotate L"]+RECT_OPS

def doRectOp(c,rect,op):
    if op==0:
        c.flipHRect(rect)
    elif op==1:
        c.flipVRect(rect)
    elif op==2:
        c.flipHVRect(rect)
    elif op==3:
        c.invertRect(rect)
    else:
        c.fillRect(rect,op-4)

def doCanvasOp(c,op):
    if op<=1:
        return c.rotate(op==0)
    else:
        doRectOp(c,c.fullRect(),op-2)
        return True

DRAW_MENU_OPTIONS=[
    {
        "text":lambda:f"Zoom  <x{c.pixelSize}>",
        "onSelect":lambda d:c.changeZoom(d,True),
    },
    "Canvas op.",
    "Rect op.",
    "Crop",
    "Reframe",
    "Copy",
    "Paste",
    {
        "text":lambda:f"Status [{"x" if settings.showStatus else " "}]",
        "onSelect":lambda _:settings.toggleShowStatus(),
    },
    {
        "text":lambda:f"Frame  [{"x" if settings.showFrame else " "}]",
        "onSelect":lambda _:settings.toggleShowFrame(),
    },
    "Canv. info",
    "Mem info",
    "Help",
    "Save",
    "Save as",
    "Close",
    "Exit",
    # "!FailNow!",
]

def showDrawMenu(c):
    thumby2.buttons.assumeUp()
    gc.collect()
    selOption=0
    while True:
        selOption=menuChoice(DRAW_MENU_OPTIONS,0,5,selOption)
        if not selOption:
            return
        sel=DRAW_MENU_OPTIONS[selOption]
        if sel=="Canvas op.":
            thumby.display.fill(0)
            thumby2.display.text.print("Canvas op:",0)
            op=menuChoice(CANVAS_OPS,1,4)
            if op is not None:
                if doCanvasOp(c,op):
                    return
        elif sel=="Rect op.":
            thumby.display.fill(0)
            thumby2.display.text.print("Rect op:",0)
            op=menuChoice(RECT_OPS,1,4)
            if op is not None:
                c.rectSelStartCorner()
                rect=selectRect(c)
                if rect:
                    doRectOp(c,rect,op)
                    return
        elif sel=="Crop":
            c.rectSelStartCorner()
            rect=selectRect(c)
            if rect:
                if c.crop(rect):
                    return
        elif sel=="Reframe":
            newSize=enterSize(c.size,"Frame size:")
            if newSize:
                px,py=c.posX,c.posY
                c.posX-=(newSize[0]-1)//2
                c.posY-=(newSize[1]-1)//2
                c.rectSelStartSize(newSize)
                rect=selectRect(c)
                if rect:
                    if c.crop(rect):
                        return
                else:
                    c.posX=px
                    c.posY=py
        elif sel=="Copy":
            c.rectSelStartCorner()
            rect=selectRect(c)
            if not rect:
                continue
            buf=c.copy(rect)
            if not buf:
                continue
            name=enterName(save_files.CLIP_PREFIX+"1","Save clip:")
            if not name:
                continue
            save_files.save(name,(rect[2],rect[3]),buf.raw)
            del buf
            gc.collect()
            return
        elif sel=="Paste":
            saves=save_files.list(save_files.TYPE_CLIP)
            thumby.display.fill(0)
            thumby2.display.text.print("Paste:",0)
            sel=menuChoice([s["listName"] for s in saves],1,4)
            if sel is None:
                continue
            sd=saves[sel]
            try:
                bs=tryLoadBytes(sd)
                buf=FBuf(sd["size"],bs) if bs else None
            except MemoryError:
                simpleConfirm(
                    ["MemoryError","","Cannot","insert","this file."])
                continue
            if not buf:
                continue
            c.rectSelStartSize(sd["size"])
            rect=selectRect(c)
            if not rect:
                continue
            thumby.display.fill(0)
            thumby2.display.text.print(["Paste","pixels:"],0)
            sel=menuChoice(["All","White","Black"],2,3)
            if sel is None:
                continue
            c.paste(buf,rect[0],rect[1],key=sel-1)
            del buf
            gc.collect()
            return
        elif sel=="Canv. info":
            simpleConfirm(["Canvas:",
                c.name or "(no name)","%12s"%f"{c.width}x{c.height}"])
        elif sel=="Mem info":
            gc.collect()
            alloc=gc.mem_alloc()
            free=gc.mem_free()
            total=alloc+free
            usedFrac=alloc/total
            simpleConfirm(["RAM usage:","%10d B"%alloc,"of %7d B"%total,
                f"= {round(100*usedFrac)}%"])
        elif sel=="Help":
            simpleConfirm(HELP)
        elif sel=="Save":
            if saveCanvas(c):
                return
        elif sel=="Save as":
            if saveCanvasAs(c):
                return
        elif sel=="Close":
            if not c.modified or confirm(
                    ["Close with-","out saving?",""],"Close"):
                return "close"
        elif sel=="Exit":
            if not c.modified or confirm(
                    ["Exit with-","out saving?",""],"Exit"):
                thumby.reset()
        elif sel=="!FailNow!":
            failingNow

CANVAS_DPAD_LONG_PRESS_MS=200

def useCanvas(c):
    thumby2.display.text.font35i1()
    thumby.display.setFPS(15)
    dpadAnyLongPress=False
    pureBLongPress=False
    while True:
        c.draw()
        thumby2.update()
        dpadAnyDown=False
        if thumby2.buttons.B.down:
            if thumby2.buttons.B.edge>0:
                pureBLongPress=True
            for btn in thumby2.buttons.ALL:
                if btn!=thumby2.buttons.B and btn.down:
                    pureBLongPress=False
                    break
            if pureBLongPress and thumby2.buttons.B.longPressEdge>0:
                thumby2.display.text.font57i1()
                sel=showDrawMenu(c)
                if sel=="close":
                    return
                thumby2.display.text.font35i1()
            else:
                for btn,zoomDir in thumby2.buttons.UD_VALS:
                    if btn.edge>0:
                        btn.assumeUp()
                        c.changeZoom(zoomDir)
                if thumby2.buttons.LEFT.edge>0 or thumby2.buttons.LEFT.longPress:
                    c.undo()
                elif thumby2.buttons.RIGHT.edge>0 or thumby2.buttons.RIGHT.longPress:
                    c.redo()
            dpadAnyLongPress=False
        else:
            for btn in thumby2.buttons.DPAD:
                if btn.down:
                    dpadAnyDown=True
                    if btn.downTimeMs()>=CANVAS_DPAD_LONG_PRESS_MS:
                        dpadAnyLongPress=True
            if not dpadAnyDown:
                dpadAnyLongPress=False
            moved=False
            for btn,vec in thumby2.buttons.DPAD_VECTORS:
                if (btn.edge<0 and btn.longPressEdge==0) or \
                    (btn.down and dpadAnyLongPress):
                    if c.moveBy(vec,btn.edge<0):
                        moved=True
            if thumby2.buttons.A.edge>0 or \
                    (moved and thumby2.buttons.A.down and thumby2.buttons.A.edge==0):
                c.toggle()

def showTitleImg():
    with open(GAME_DIR+"/demos/Title_72x40.bin","b") as f:
        data=f.read()
    thumby.display.blit(data,0,0,72,40,-1,False,False)
    del data
    thumby2.display.show()
    thumby2.buttons.wait()

showTitleImg()
helpShown=False
selOption=0
newCanvasSize=(72,40)
thumby2.display.text.font57i1()
while True:
    thumby.display.fill(0)
    c=None
    drawTitle()
    selOption=menuChoice(["New","Load","Help","Exit"],1,4,selOption)
    if selOption is None or selOption==3:
        thumby2.display.text.clear(1,rows=4)
        thumby2.display.text.print("Exit",2)
        thumby2.display.show()
        time.sleep(1)
        thumby.reset()
    elif selOption==0:
        size=enterSize(newCanvasSize)
        if size:
            newCanvasSize=size
            gc.collect()
            try:
                c=Canvas(size)
            except MemoryError:
                c=None
                simpleConfirm(["MemoryError","","Try smaller","canvas."])
    elif selOption==1:
        c=loadCanvas()
    elif selOption==2:
        simpleConfirm(HELP)
    if c:
        if not helpShown:
            simpleConfirm(SHORT_HELP)
            helpShown=True
        try:
            useCanvas(c)
        except Exception as e:
            try:
                save_files.panicSave(c)
                print("Panic save created.")
                save_files.saveException(e)
                thumby.display.fill(0)
                thumby2.display.text.print("   Panic!",3)
                time.sleep_ms(500)
            except Exception as e2:
                print(e2)
            raise e
        del c
