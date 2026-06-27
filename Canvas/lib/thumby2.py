import thumby
import time

__version__='1.2.1'

IN_EMULATOR=not hasattr(thumby.display.display,"cs")

@micropython.viper
def clamp(v:int,min:int,max:int)->int:
    if v<min:
        return min
    elif v>max:
        return max
    else:
        return v

def __checkClampRange(v1:int,v2:int,min:int,max:int)->(bool,int,int):
    if v1>max:
        return (False,0,0)
    if v1<min:
        if v2<min:
            return (False,0,0)
        v1=min
    if v2>max:
        v2=max
    return (True,v1,v2)

class display:

    class text:

        @staticmethod
        def font35i1():
            thumby.display.setFont("/lib/font3x5.bin",3,6,1)

        @staticmethod
        def font57i1():
            thumby.display.setFont("/lib/font5x7.bin",5,8,1)

        @staticmethod
        def font88():
            thumby.display.setFont("/lib/font8x8.bin",8,8,0)

        @staticmethod
        def print(text,row,column=0,color=1):
            if isinstance(text,str):
                text=[text]
            x0=column*(thumby.display.textWidth+thumby.display.textSpaceWidth)
            yPerRow=thumby.display.textHeight
            y0=row*yPerRow
            for row,line in enumerate(text):
                thumby.display.drawText(line,x0,y0+row*yPerRow,color)

        @staticmethod
        def clear(row,column=0,rows=1,columns=1000,color=1):
            xPerChar=thumby.display.textWidth+thumby.display.textSpaceWidth
            display.fillRect(
                column*xPerChar,row*thumby.display.textHeight,
                columns*xPerChar-1,rows*thumby.display.textHeight,not color)

    @staticmethod
    @micropython.viper
    def drawLineH(x1:int,y:int,x2:int,color:int):
        if 0<=y<40:
            x1=int(clamp(x1,0,71))
            x2=int(clamp(x2,0,71))
            if x1>x2:
                x1,x2=x2,x1
            mask=int(1<<(y&0b111))
            pageAddr=int((y>>3)*72)
            buf=ptr8(thumby.display.display.buffer)
            if color:
                for offset in range(x1,x2+1):
                    buf[pageAddr+offset]|=mask
            else:
                mask=int(mask^-1)
                for offset in range(x1,x2+1):
                    buf[pageAddr+offset]&=mask

    @staticmethod
    @micropython.viper
    def drawLineV(x:int,y1:int,y2:int,color:int):
        if 0<=x<72:
            y1=int(clamp(y1,0,39))
            y2=int(clamp(y2,0,39))
            if y1>y2:
                y1,y2=y2,y1
            firstPage=int(y1>>3)
            lastPage=int(y2>>3)
            maskStart=int(0x100-(1<<(y1&0b111)))
            maskEnd=int((1<<((y2&0b111)+1))-1)
            buf=ptr8(thumby.display.display.buffer)
            if firstPage==lastPage:
                mask=int(maskStart&maskEnd)
                if color:
                    buf[firstPage*72+x]|=mask
                else:
                    buf[firstPage*72+x]&=mask^0xFF
            else:
                if color:
                    buf[firstPage*72+x]|=maskStart
                    buf[lastPage*72+x]|=maskEnd
                    for page in range(firstPage+1,lastPage):
                        buf[page*72+x]=0xFF
                else:
                    buf[firstPage*72+x]&=maskStart^0xFF
                    buf[lastPage*72+x]&=maskEnd^0xFF
                    for page in range(firstPage+1,lastPage):
                        buf[page*72+x]=0x00

    @staticmethod
    @micropython.viper
    def drawRect(x:int,y:int,width:int,height:int,color:int):
        display.drawLineH(x,y,x+width-1,color)
        display.drawLineH(x,y+height-1,x+width-1,color)
        display.drawLineV(x,y,y+height-1,color)
        display.drawLineV(x+width-1,y,y+height-1,color)

    @staticmethod
    @micropython.viper
    def fillRect(x:int,y:int,width:int,height:int,color:int):
        x1x2=__checkClampRange(x,x+width-1,0,71)
        if not x1x2[0]:
            return
        y1y2=__checkClampRange(y,y+height-1,0,39)
        if not y1y2[0]:
            return
        x1=int(x1x2[1])
        x2=int(x1x2[2])
        y1=int(y1y2[1])
        y2=int(y1y2[2])
        firstPage=int(y1>>3)
        lastPage=int(y2>>3)
        maskStart=int(0x100-(1<<(y1&0b111)))
        maskEnd=int((1<<((y2&0b111)+1))-1)
        buf=ptr8(thumby.display.display.buffer)
        if firstPage==lastPage:
            mask=int(maskStart&maskEnd)
            if color:
                for offset in range(x1,x2+1):
                    buf[firstPage*72+offset]|=mask
            else:
                mask^=0xFF
                for offset in range(x1,x2+1):
                    buf[firstPage*72+offset]&=mask
        else:
            if color:
                for offset in range(x1,x2+1):
                    buf[firstPage*72+offset]|=maskStart
                    buf[lastPage*72+offset]|=maskEnd
                    for page in range(firstPage+1,lastPage):
                        buf[page*72+offset]=0xFF
            else:
                maskStart^=0xFF
                maskEnd^=0xFF
                for offset in range(x1,x2+1):
                    buf[firstPage*72+offset]&=maskStart
                    buf[lastPage*72+offset]&=maskEnd
                    for page in range(firstPage+1,lastPage):
                        buf[page*72+offset]=0x00

    @staticmethod
    def cloneBuffer():
        return thumby.display.display.buffer[:]

    @staticmethod
    def setBuffer(buffer):
        thumby.display.display.buffer=buffer

    @staticmethod
    @micropython.native
    def show():
        d=thumby.display.display
        if IN_EMULATOR:
            d.show()
        else:
            d.cs(1)
            d.dc(1)
            d.cs(0)
            d.spi.write(d.buffer)
            d.cs(1)

    @staticmethod
    def waitFrame():
        timeLeftMs=None
        if thumby.display.frameRate>0:
            frEndTime=thumby.display.lastUpdateEnd+\
                1000//thumby.display.frameRate
            timeLeftMs=frEndTime-time.ticks_ms()
            if timeLeftMs>1:
                time.sleep_ms(timeLeftMs-1)
            while time.ticks_ms()<frEndTime:
                pass
        thumby.display.lastUpdateEnd=time.ticks_ms()
        return timeLeftMs

    @staticmethod
    def update():
        display.show()
        return display.waitFrame()

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
