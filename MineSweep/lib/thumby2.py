import thumby
import time

__version__='1.3.0'

IN_EMULATOR=not hasattr(thumby.display.display,"cs")


class Sprite:

    def __init__(self,blit:ptr8,width:int,height:int):
        self.blit=blit
        self.width=width
        self.height=height


class Buffer:

    def __init__(self,buffer:ptr8,width:int,height:int):
        self.buffer=buffer
        self.width=width
        self.height=height
        self.textBuffer=None

    @staticmethod
    def screenSized(buffer:ptr8):
        return Buffer(buffer,72,40)

    @micropython.viper
    def fill(self,val:int):
        if val:
            val=0xFF
        b=ptr8(self.buffer)
        for i in range(int(len(b))):
            b[i]=val

    @micropython.viper
    def drawLineH(self,x1:int,y:int,x2:int,color:int):
        ww=int(self.width)
        hh=int(self.height)
        if 0<=y<hh:
            x1=int(min(max(x1,0),ww-1))
            x2=int(min(max(x2,0),ww-1))
            if x1>x2:
                x1,x2=x2,x1
            mask=int(1<<(y&0b111))
            pageAddr=int((y>>3)*ww)
            b=ptr8(self.buffer)
            if color:
                for offset in range(x1,x2+1):
                    b[pageAddr+offset]|=mask
            else:
                mask=int(mask^-1)
                for offset in range(x1,x2+1):
                    b[pageAddr+offset]&=mask

    @micropython.viper
    def drawLineV(self,x:int,y1:int,y2:int,color:int):
        ww=int(self.width)
        hh=int(self.height)
        if 0<=x<ww:
            y1=int(min(max(y1,0),hh-1))
            y2=int(min(max(y2,0),hh-1))
            if y1>y2:
                y1,y2=y2,y1
            firstPage=int(y1>>3)
            lastPage=int(y2>>3)
            maskStart=int(0x100-(1<<(y1&0b111)))
            maskEnd=int((1<<((y2&0b111)+1))-1)
            b=ptr8(self.buffer)
            if firstPage==lastPage:
                mask=int(maskStart&maskEnd)
                if color:
                    b[firstPage*ww+x]|=mask
                else:
                    b[firstPage*ww+x]&=mask^0xFF
            else:
                if color:
                    b[firstPage*ww+x]|=maskStart
                    b[lastPage*ww+x]|=maskEnd
                    for page in range(firstPage+1,lastPage):
                        b[page*ww+x]=0xFF
                else:
                    b[firstPage*ww+x]&=maskStart^0xFF
                    b[lastPage*ww+x]&=maskEnd^0xFF
                    for page in range(firstPage+1,lastPage):
                        b[page*ww+x]=0x00

    @micropython.viper
    def drawRect(self,x:int,y:int,width:int,height:int,color:int):
        self.drawLineH(x,y,x+width-1,color)
        self.drawLineH(x,y+height-1,x+width-1,color)
        self.drawLineV(x,y,y+height-1,color)
        self.drawLineV(x+width-1,y,y+height-1,color)

    @micropython.viper
    def fillRect(self,x:int,y:int,width:int,height:int,color:int):
        ww=int(self.width)
        hh=int(self.height)
        x2=int(min(x+width-1,ww-1))
        y2=int(min(y+height-1,hh-1))
        if x>=ww or x2<0 or y>=hh or y2<0:
            return
        x=int(max(x,0))
        y=int(max(y,0))
        firstPage=int(y>>3)
        lastPage=int(y2>>3)
        maskStart=int(0x100-(1<<(y&0b111)))
        maskEnd=int((1<<((y2&0b111)+1))-1)
        b=ptr8(self.buffer)
        if firstPage==lastPage:
            mask=int(maskStart&maskEnd)
            if color:
                for offset in range(x,x2+1):
                    b[firstPage*ww+offset]|=mask
            else:
                mask^=0xFF
                for offset in range(x,x2+1):
                    b[firstPage*ww+offset]&=mask
        else:
            if color:
                for offset in range(x,x2+1):
                    b[firstPage*ww+offset]|=maskStart
                    b[lastPage*ww+offset]|=maskEnd
                    for page in range(firstPage+1,lastPage):
                        b[page*ww+offset]=0xFF
            else:
                maskStart^=0xFF
                maskEnd^=0xFF
                for offset in range(x,x2+1):
                    b[firstPage*ww+offset]&=maskStart
                    b[lastPage*ww+offset]&=maskEnd
                    for page in range(firstPage+1,lastPage):
                        b[page*ww+offset]=0x00

    @micropython.viper
    def _blit(self,sprite:ptr8,x:int,y:int,width:int,height:int,
            key:int,mirrorX:int,mirrorY:int):
        ww=int(self.width)
        hh=int(self.height)
        if not 0-width<x<ww or not 0-height<y<hh:
            return
        xStart=int(x)
        yStart=int(y)
        b=ptr8(self.buffer)
        yFirst=int(max(0-yStart,0))
        blitHeight=int(min(height,hh-yStart))
        xFirst=int(max(0-xStart,0))
        blitWidth=int(min(width,ww-xStart))
        y=yFirst
        if key==0:
            while y<blitHeight:
                x=xFirst
                while x<blitWidth:
                    if sprite[((height-1-y if mirrorY==1 else y)>>3)*width+(width-1-x if mirrorX==1 else x)]&(
                            1<<((height-1-y if mirrorY==1 else y)&0x07)):
                        b[((yStart+y)>>3)*ww+xStart+x]|=1<<((yStart+y)&0x07)
                    x+=1
                y+=1
        elif key==1:
            while y<blitHeight:
                x=xFirst
                while x<blitWidth:
                    if sprite[((height-1-y if mirrorY==1 else y)>>3)*width+(width-1-x if mirrorX==1 else x)]&(
                            1<<((height-1-y if mirrorY==1 else y)&0x07))==0:
                        b[((yStart+y)>>3)*ww+xStart+x]&=0xFF^(1<<((yStart+y)&0x07))
                    x+=1
                y+=1
        else:
            while y<blitHeight:
                x=xFirst
                while x<blitWidth:
                    if sprite[((height-1-y if mirrorY==1 else y)>>3)*width+(width-1-x if mirrorX==1 else x)]&(
                            1<<((height-1-y if mirrorY==1 else y)&0x07)):
                        b[((yStart+y)>>3)*ww+xStart+x]|=1<<((yStart+y)&0x07)
                    else:
                        b[((yStart+y)>>3)*ww+xStart+x]&=0xFF^(1<<((yStart+y)&0x07))
                    x+=1
                y+=1

    def blit(self,blit:ptr8,x,y,width,height,key=-1,mirrorX=False,mirrorY=False):
        self._blit(blit,x,y,width,height,key,mirrorX,mirrorY)

    def sprite(self,sprite:Sprite,x,y,key=-1,mirrorX=False,mirrorY=False):
        self._blit(sprite.blit,x,y,sprite.width,sprite.height,key,mirrorX,mirrorY)

    def text(self,font=None):
        if self.textBuffer is None or font!=self.textBuffer.font:
            if font is None:
                raise RuntimeError("Font needed")
            self.textBuffer=TextBuffer(self,font)
        return self.textBuffer

    def text35(self):
        return self.text(Font.font35())

    def text57(self):
        return self.text(Font.font57())

    def text88(self):
        return self.text(Font.font88())


class Font:

    fontsDict=dict()

    def __init__(self,fontFile,charW,charH,spacingX,spacingY):
        with open(fontFile,"rb") as f:
            self.data=f.read()
        self.charW=charW
        self.charH=charH
        self.spacingX=spacingX
        self.spacingY=spacingY
        self.charDX=charW+spacingX
        self.charDY=charH+spacingY
        self.glyphCount=len(self.data)//charW

    def charData(self,char:str):
        chInd=int(ord(char)-0x20)
        if chInd<self.glyphCount:
            dInd=chInd*self.charW
            return self.data[dInd:dInd+self.charW]

    @staticmethod
    def font(fontFile,charW,charH,spacingX=0,spacingY=0):
        key=(fontFile,charW,charH,spacingX,spacingY)
        font=Font.fontsDict.get(key)
        if font is None:
            font=Font(*key)
            Font.fontsDict[key]=font
        return font

    @staticmethod
    def font35():
        return Font.font("/lib/font3x5.bin",3,5,1,1)

    @staticmethod
    def font57():
        return Font.font("/lib/font5x7.bin",5,7,1,1)

    @staticmethod
    def font88():
        return Font.font("/lib/font8x8.bin",8,8)


class TextBuffer:

    def __init__(self,screen,font):
        self.screen=screen
        self.font=font

    @micropython.viper
    def _printXY(self,text,x:int,y:int,color:int):
        if isinstance(text,str):
            text=[text]
        ww=int(self.screen.width)
        hh=int(self.screen.height)
        for row,line in enumerate(text):
            if 0-int(self.font.charH)<y<hh:
                xx=int(x)
                for ch in line:
                    chData=self.font.charData(ch)
                    if chData:
                        if not color:
                            chData=bytearray(chData)
                            for i in range(int(self.font.charW)):
                                chData[i]=int(chData[i])^0xFF
                        self.screen.blit(chData,xx,y,self.font.charW,self.font.charH,
                            key=1-color)
                    xx+=int(self.font.charDX)
            y+=int(self.font.charDY)

    def printXY(self,text,x,y,color=1):
        self._printXY(text,x,y,color)

    def print(self,text,row,column=0,color=1):
        self.printXY(text,column*self.font.charDX,row*self.font.charDY,color)

    def clear(self,row,column=0,rows=1,columns=1000,color=1):
        self.screen.fillRect(
            column*self.font.charDX,row*self.font.charDY,
            columns*self.font.charDX,rows*self.font.charDY,
            not color)


class ThumbyDisplayBuffer(Buffer):

    def __init__(self):
        super().__init__(thumby.display.display.buffer,72,40)

    def cloneBuffer(self):
        return self.buffer[:]

    def setBuffer(self,buffer):
        thumby.display.display.buffer=buffer
        self.buffer=buffer

    @micropython.native
    def show(self):
        d=thumby.display.display
        if IN_EMULATOR:
            d.show()
        else:
            d.cs(1)
            d.dc(1)
            d.cs(0)
            d.spi.write(d.buffer)
            d.cs(1)

    def waitFrame(self):
        timeLeftMs=None
        if thumby.display.frameRate>0:
            frEndTime=thumby.display.lastUpdateEnd+1000//thumby.display.frameRate
            timeLeftMs=frEndTime-time.ticks_ms()
            if timeLeftMs>1:
                time.sleep_ms(timeLeftMs-1)
            while time.ticks_ms()<frEndTime:
                pass
        thumby.display.lastUpdateEnd=time.ticks_ms()
        return timeLeftMs

    def update(self):
        self.show()
        return self.waitFrame()

display=ThumbyDisplayBuffer()


class buttons:

    class Button:

        LONG_PRESS_MS=400

        def __init__(self,pin):
            self.pin=pin
            self.reset()
            self.update()

        def reset(self):
            self.downSinceMs=0
            self.down=False
            self.edge=0
            self.longPress=False
            self.longPressEdge=0
            self.assumingUp=False

        def downTimeMs(self):
            if self.downSinceMs==0:
                return 0
            return time.ticks_ms()-self.downSinceMs

        def update(self):
            now=time.ticks_ms()
            downNow=self.pin.value()==0
            if self.assumingUp:
                if not downNow:
                    self.assumingUp=False
                return
            longPressNow=downNow and self.downSinceMs!=0 and \
                now-self.downSinceMs>=buttons.Button.LONG_PRESS_MS
            self.edge=downNow-self.down
            self.down=downNow
            self.longPressEdge=longPressNow-self.longPress
            self.longPress=longPressNow
            if self.edge>0:
                self.downSinceMs=now
            elif not self.down:
                self.downSinceMs=0

        def assumeUp(self):
            self.reset()
            self.assumingUp=True

    UP=Button(thumby.buttonU.pin)
    DOWN=Button(thumby.buttonD.pin)
    RIGHT=Button(thumby.buttonR.pin)
    LEFT=Button(thumby.buttonL.pin)
    A=Button(thumby.buttonA.pin)
    B=Button(thumby.buttonB.pin)

    UD=[UP,DOWN]
    RL=[RIGHT,LEFT]
    DPAD=UD+RL
    AB=[A,B]
    ALL=DPAD+AB

    UD_VALS=[(UP,1),(DOWN,-1)]
    RL_VALS=[(RIGHT,1),(LEFT,-1)]

    DPAD_VECTORS=[
        (UP,(0,-1)),
        (DOWN,(0,1)),
        (RIGHT,(1,0)),
        (LEFT,(-1,0)),
    ]

    @staticmethod
    def update():
        for button in buttons.ALL:
            button.update()

    @staticmethod
    def assumeUp():
        for button in buttons.ALL:
            button.assumeUp()

    @staticmethod
    def wait(activeButtons=None):
        if activeButtons is None:
            activeButtons=buttons.ALL
        if len(activeButtons)==0:
            return None
        for b in activeButtons:
            b.assumeUp()
        while True:
            buttons.update()
            for b in activeButtons:
                if b.down:
                    return b
            time.sleep_ms(10)


class audio:

    BASE_FREQ=440
    HALFTONE=2**(1/12)

    @staticmethod
    def freq(halftones,baseFreq=BASE_FREQ):
        return int(baseFreq*audio.HALFTONE**halftones)

    @staticmethod
    def musicBlocking(noteTuples,baseIntervalMs=1,baseFreq=BASE_FREQ):
        for halftones,duration in noteTuples:
            if halftones is None:
                time.sleep_ms(int(duration*baseIntervalMs))
            else:
                thumby.audio.playBlocking(
                    audio.freq(halftones,baseFreq),
                    int(duration*baseIntervalMs))


def update():
    display.show()
    buttons.update()
    return display.waitFrame()

def requireMinThumbyVersion(reqVersion):
    actVersion=thumby.__version__
    try:
        act,req=(list(map(int,v.split("."))) for v in [actVersion,reqVersion])
    except ValueError:
        println(f"Cannot parse version. Required: {reqVersion}, "+
            f"actual: {actVersion}. Accepted.")
        return
    act,req=(list(v.split(".")) for v in [actVersion,reqVersion])
    if act<req:
        thumby.display.fill(0)
        display.text.font57i1()
        display.text.print(
            ["Cannot run!","Update libs","in IDE!","",f"{actVersion}<{reqVersion}"],0)
        display.show()
        buttons.wait()
        thumby.reset()
