
# fix brightness not persistent

from machine import freq
freq(250_000_000)
from machine import mem32, soft_reset, ADC
from time import sleep, ticks_ms
from os import listdir, stat
from gc import collect as gc_collect
import thumby
freq(48_000_000)

adc = ADC(26)
v = adc.read_u16()
v //= 100

QuickLoad = 0
syssettingsSelpos = 0
briteSlider = 0

settingsSelpos = -1
SettingsScroll = 0
scroll = 0


try:
    cfg = open('thumby.cfg', 'r').read().split(',')
    modcfg = open('mods.cfg', 'r').read().split(',')
except:
    cfg = open('thumby.cfg', 'w')
    cfg.write('audioenabled,1,lastgame,/Games/TinyBlocks/TinyBlocks.py,brightness,1')
    cfg.close()
    modcfg = open('mods.cfg', 'w')
    modcfg.write('Fastboot,0,BrightSlider,0,brightness,64')
    modcfg.close()

def getCfg(source, key):
    cfg = open('thumby.cfg', 'r').read().split(',')
    modcfg = open('mods.cfg', 'r').read().split(',')
    if source == 'thumby':
        for i in range(len(cfg)):
            if cfg[i] == key:
                return cfg[i+1]
    elif source == 'mods':
        for i in range(len(modcfg)):
            if modcfg[i] == key:
                return modcfg[i+1]
    return False
    
def saveCfg(dest, key, setting):
    if dest == 'thumby':
        cfg = open('thumby.cfg', 'r').read().split(',')
        for i in range(len(cfg)):
            if cfg[i] == key:
                cfg[i+1] = setting
        cfgfile = open("thumby.cfg", "w")
        cfgfile.write(','.join(cfg))
        cfgfile.close()
    if dest == 'mods':
        modcfg = open('mods.cfg', 'r').read().split(',')
        for i in range(len(modcfg)):
            if modcfg[i] == key:
                modcfg[i+1] = setting
        modcfgfile = open("mods.cfg", "w")
        modcfgfile.write(','.join(modcfg))
        modcfgfile.close()
    
def BattPercent(voltage):
    if voltage < 313:
        return 1
    elif voltage > 380:
        return 'CHRG'
    else:
        return (voltage - 313) / 0.67

audioSetting = int(getCfg('thumby', 'audioenabled'))
brightnessSetting=int(getCfg('thumby', 'brightness'))
QuickLoad=int(getCfg('mods', 'Fastboot'))
briteSlider=int(getCfg('mods', 'BrightSlider'))
audioSettings=['Audio: Off', 'Audio:  On']
brightnessSettings=['Brite: Low', 'Brite: Mid', 'Brite:  Hi']
quickloadSettings=['QLoad: Off', 'QLoad:  On']
briteSliderSettings=['BrBar: Off', 'BrBar: On']
brightnessVals=[1,28,127]
batteryPercent=['Batt: ' + str(int(BattPercent(v))) + '%']
settings=[audioSettings[audioSetting], brightnessSettings[brightnessSetting], batteryPercent[0]]
syssettings = [quickloadSettings[QuickLoad], briteSliderSettings[briteSlider]]


startTime=ticks_ms()
TCSplash=thumby.Sprite(72, 24, 'lib/TClogo.bin',0,0,-1)
thumbySplash=thumby.Sprite(72, 24, 'lib/thumbyLogo.bin',0,0,-1)
x = 5
y = 36
if QuickLoad == 0:
    yScrollPos = 0
    yScrollTarget = 0
else:
    yScrollPos = -40
    yScrollTarget = -40
noButtonPress = 1
brightnessValue = brightnessVals[brightnessSetting] if not briteSlider else int(getCfg('mods', 'brightness'))
settingsBMonly = bytearray([81,81,85,69,69,127,65,65,85,85,93,127,125,65,65,125,127,125,65,65,125,127,93,65,65,93,127,65,65,115,103,65,65,127,65,65,93,85,69,69,127,81,81,85,69,69])
gamesBMonly = bytearray([65,65,93,85,69,69,127,67,65,117,65,67,127,65,65,115,103,115,65,65,127,65,65,85,85,93,127,81,81,85,69,69])
syssettingsBMonly = bytearray([81,81,85,69,69,127,121,113,71,71,113,121,127,81,81,85,69,69,127,127,127,127,81,81,85,69,69,127,65,65,85,85,93,127,125,65,65,125,127,125,65,65,125,127,93,65,65,93,127,65,65,115,103,65,65,127,65,65,93,85,69,69,127,81,81,85,69,69])
settingsHeader = thumby.Sprite(46, 7, settingsBMonly)
gamesHeader = thumby.Sprite(32, 7, gamesBMonly)
syssettingsHeader = thumby.Sprite(68, 7, syssettingsBMonly, 2, 0)

thumby.display.setFPS(50)

if QuickLoad == 0:
    thumbySplash.y = -37
    while thumbySplash.y < 5:
        thumbySplash.y += 2
        TCSplash.y=thumbySplash.y+37
        thumby.display.fill(0)
        thumby.display.drawSprite(thumbySplash)
        thumby.display.drawSprite(TCSplash)
        thumby.display.update()
    thumbyLogoHeight=thumbySplash.y

frameCounter = 0
xScrollPos = 0
xScrollTarget = 0
selpos = -1
files = listdir('/Games')

for k in range(len(files)):
    if(stat("/Games/"+files[k])[0] != 16384):
        files[k] = ""
try:
    while(True):
        files.remove("")
except ValueError:
    pass
shortFiles= list(files)


for k in range(len(shortFiles)):
    if(len(shortFiles[k])>10):
        shortFiles[k]=shortFiles[k][0:8]+'..'

gc_collect()

def writeCenteredText(text, x, y ,color):
    textLen = min(len(text),10)
    thumby.display.drawText(text, x - ( textLen * 6) // 2 + 1, y,color)

rightArrowBA = bytearray([0b11111,0b01110,0b00100])
leftArrowBA = bytearray([0b00100,0b01110,0b11111])
rightArrowBAinv = bytearray([0b11111^0xff,0b01110^0xff,0b00100^0xff])
leftArrowBAinv = bytearray([0b00100^0xff,0b01110^0xff,0b11111^0xff])

def drawBracketsAround(text, x, y ,color):
    textLen = min(len(text),10)
    xc=x -(textLen * 6) // 2 -2
    if(color):
        thumby.display.blit(rightArrowBA, xc-1, y+1, 3, 5,-1,0,0)
    xc=x +(textLen * 6) // 2 +2
    if(color):
        thumby.display.blit(leftArrowBA, xc-1, y+1, 3, 5,-1,0,0)

lastPosition = 0
xOffset = 0

def printList(nameList, position, x, y, longNames=None):
    offset1=0
    offset2=0
    pxWidth=0
    global lastPosition
    global xOffset
    if(longNames):
        if position is not lastPosition:
            lastPosition=position
            xOffset=0
        if(position==0 and len(longNames[0])>10):
            xOffset+=1
            pxWidth= len(longNames[0])*6
            offset1=xOffset%pxWidth
        if(position>=1 and len(longNames[position])>10):
            xOffset+=1
            pxWidth= len(longNames[position])*6 +20
            offset2=xOffset%pxWidth
    actualPosition = position
    position = max(position,1)
    if(position > 1 and len(nameList) > 0 and 0+scroll>1):
        writeCenteredText(nameList[position-2], x, y+0,1)
    if(position > 0 and len(nameList) > 0):
        if(longNames and actualPosition==0 and len(longNames[0])>10):
            writeCenteredText(longNames[position-1], x-offset1, y+8,1)
            writeCenteredText(longNames[position-1], x-offset1+pxWidth, y+8,1)
            thumby.display.drawFilledRectangle(0,y+8,8,8,0)
            thumby.display.drawFilledRectangle(72-8,y+8,8,8,0)
        else:
            writeCenteredText(nameList[position-1], x, y+8,1)
    if(position>=0):
        if(longNames and actualPosition>=1 and len(longNames[position])>10):
            writeCenteredText(longNames[position], x-offset2, y+16, 1)
            writeCenteredText(longNames[position], x-offset2+pxWidth, y+16, 1)
            thumby.display.drawFilledRectangle(0,y+16,6,8,0)
            thumby.display.drawFilledRectangle(72-6,y+16,6,8,0)
        else:
            writeCenteredText(nameList[position], x, y+16, 1)
    if(position < len(nameList)-1):
        writeCenteredText(nameList[position+1], x, y+24,1)
    if(position < len(nameList)-2):
        writeCenteredText(nameList[position+2], x, y+32,1)
    if(position < len(nameList)-3):
        writeCenteredText(nameList[position+3], x, y+40,1)

def launchGame():
    if(selpos>=0):
        gamePath="/Games/"+files[selpos]+"/"+files[selpos]+".py"
        saveCfg('thumby', "lastgame", gamePath)
    mem32[0x4005800C]=1
    soft_reset()

def briteSetting():
    drawBracketsAround('Brite: Mid', 36, 16, 1)
    frameCounter = 0
    global brightnessValue
    while(1):
        if thumby.buttonL.pressed():
            frameCounter += 1
            if frameCounter > 20:
                brightnessValue -= 2
            else:
                brightnessValue -= 1
        elif thumby.buttonR.pressed():
            frameCounter += 1
            if frameCounter > 20:
                brightnessValue += 2
            else:
                brightnessValue += 1
        else:
            frameCounter = 0
        
        if thumby.inputJustPressed():
            if thumby.buttonA.pressed() or thumby.buttonB.pressed():
                saveCfg('mods', 'brightness', str(min(127, brightnessValue)))
                break
        
        if brightnessValue > 127:
            brightnessValue = 127
        if brightnessValue < 0:
            brightnessValue = 0
        
        thumby.display.brightness(int(brightnessValue))
        
        thumby.display.drawFilledRectangle(47, 17, 18, 5, 0)
        thumby.display.drawFilledRectangle(47, 17, brightnessValue//7, 5, 1)
        thumby.display.update()

def systemSettings():
    syssettingsSelpos = 0
    frameCounter = 0
    justEntered = 1
    scroll = 0
    global QuickLoad, syssettings, briteSlider, thumbyLogoHeight, yScrollPos, yScrollTarget, startTime, TCSplash, thumbySplash, x, y, noButtonPress
    while(1):
        scrollDisplayed=scroll
        if(syssettingsSelpos<1 or (syssettingsSelpos==1 and scroll>0)):
            scrollDisplayed=0
        selectOffset= 16
        if(syssettingsSelpos<2):
            selectOffset = syssettingsSelpos*8+8
        if thumby.inputJustPressed():
            if thumby.buttonA.pressed():
                if syssettingsSelpos == 0:
                    QuickLoad = (QuickLoad+1) % 2
                    saveCfg('mods', 'Fastboot', str(QuickLoad))
                elif syssettingsSelpos == 1:
                    briteSlider = (briteSlider+1) % 2
                    saveCfg('mods', 'BrightSlider', str(briteSlider))
            if thumby.buttonB.pressed():
                break
            if thumby.buttonU.pressed():
                syssettingsSelpos -= 1
            if thumby.buttonD.pressed():
                syssettingsSelpos += 1
        
        if syssettingsSelpos > len(syssettings) -1:
            syssettingsSelpos = 0
        elif syssettingsSelpos < 0:
            syssettingsSelpos = len(syssettings) -1
        
        syssettings = [quickloadSettings[QuickLoad], briteSliderSettings[briteSlider]]
        
        thumby.display.fill(0)
        printList(syssettings, syssettingsSelpos, 36, 0+scrollDisplayed)
        thumby.display.drawFilledRectangle(0, 0, 72, 7, 1)
        if(ticks_ms() % 1000 < 500 and syssettingsSelpos>=0):
            drawBracketsAround(syssettings[syssettingsSelpos], 36, selectOffset, 1)
        thumby.display.drawSprite(syssettingsHeader)
        thumby.display.update()
        
        #gamesorter

thumby.display.brightness(brightnessValue)
while(1):
    if QuickLoad == 0:
        thumbySplash.setFrame(thumbySplash.currentFrame+1)
        if(yScrollTarget!=yScrollPos):
            if(yScrollTarget>yScrollPos):
                yScrollPos += 1
                if(abs(yScrollTarget-yScrollPos)>4):
                    yScrollPos += 1
                if(abs(yScrollTarget-yScrollPos)>12):
                    yScrollPos += 2
            elif(yScrollTarget<yScrollPos):
                yScrollPos -= 1
                if(abs(yScrollTarget-yScrollPos)>4):
                    yScrollPos -= 1
                if(abs(yScrollTarget-yScrollPos)>12):
                    yScrollPos -= 2
    if(xScrollTarget!=xScrollPos):
        if(xScrollTarget>xScrollPos):
            xScrollPos += 1
            if(abs(xScrollTarget-xScrollPos)>4):
                xScrollPos += 1
            if(abs(xScrollTarget-xScrollPos)>12):
                xScrollPos += 2
        elif(xScrollTarget<xScrollPos):
            xScrollPos -= 1
            if(abs(xScrollTarget-xScrollPos)>4):
                xScrollPos -= 1
            if(abs(xScrollTarget-xScrollPos)>12):
                xScrollPos -= 2
    thumby.display.fill(0)
    if QuickLoad == 0:
        thumbySplash.x=xScrollPos-xScrollPos
        thumbySplash.y=yScrollPos+thumbyLogoHeight
        thumby.display.drawSprite(thumbySplash)
        
        color= ((ticks_ms()-startTime)//500)&1 if yScrollTarget==0 else 1
        writeCenteredText("Start", xScrollPos-xScrollPos + thumby.display.width//2, yScrollPos+32-2,1)
        drawBracketsAround("Start", xScrollPos-xScrollPos + thumby.display.width//2, yScrollPos+32-2,1-color)
    
        if(noButtonPress):
            thumby.display.drawLine(yScrollPos+x-2,y-2,yScrollPos+x,y,0)
            thumby.display.drawLine(yScrollPos+x,y,yScrollPos+x+2,y-2,0)
            if(yScrollPos == 0):
                frame=frameCounter%6
                if(frame<3):
                    y+=1
                else:
                    y-=1
                thumby.display.drawLine(x-2,y-2,x,y,1)
                thumby.display.drawLine(x,y,x+2,y-2,1)

    if(72>xScrollPos>-72):
        thumby.display.drawFilledRectangle(xScrollPos, max(0,yScrollPos+40), 72, 7,1)
        scrollDisplayed=scroll
        if(selpos<1 or (selpos==1 and scroll>0)):
            scrollDisplayed=0
        printList(shortFiles, selpos, xScrollPos + thumby.display.width//2, yScrollPos+40+scrollDisplayed, files)
            
        selectOffset= 16
        if(selpos<2):
            selectOffset = selpos*8+8
            
        gamesHeader.x= xScrollPos + 72//2 - 32//2 +1
        gamesHeader.y= max(0,yScrollPos+40)
        thumby.display.drawSprite(gamesHeader)
        
        if(ticks_ms() % 1000 < 500 and selpos<0 and yScrollTarget == -40 and xScrollTarget == 0):
            thumby.display.blit(rightArrowBAinv, xScrollPos + 65, yScrollPos+40 +1, 3, 5,1,0,0)
        if(ticks_ms() % 1000 < 500 and selpos>=0):
            drawBracketsAround(files[selpos], xScrollPos + thumby.display.width//2, yScrollPos+40+selectOffset+scrollDisplayed, 1)

    if(0>xScrollPos>-144):
        thumby.display.drawFilledRectangle(xScrollPos+72, max(0,yScrollPos+40), 72, 7,1)
        scrollDisplayed=scroll
        if(settingsSelpos<1 or (settingsSelpos==1 and scroll>0)):
            scrollDisplayed=0
        selectOffset= 16
        if(settingsSelpos<2):
            selectOffset = settingsSelpos*8+8
        printList(settings, settingsSelpos, 72+xScrollPos + thumby.display.width//2, yScrollPos+40+scrollDisplayed)
        if briteSlider == 1:
            thumby.display.drawRectangle(72+xScrollPos+46, yScrollPos+56+scrollDisplayed if settingsSelpos < 2 else yScrollPos+56-(8*(settingsSelpos-1))+scrollDisplayed, 20, 7, 1)
            thumby.display.drawFilledRectangle(72+xScrollPos+47, yScrollPos+57+scrollDisplayed if settingsSelpos < 2 else yScrollPos+57-(8*(settingsSelpos-1))+scrollDisplayed, 18, 5, 0)
            thumby.display.drawFilledRectangle(72+xScrollPos+47, yScrollPos+57+scrollDisplayed if settingsSelpos < 2 else yScrollPos+57-(8*(settingsSelpos-1))+scrollDisplayed, brightnessValue//7, 5, 1)
            
        
        
        if(ticks_ms() % 1000 < 500 and settingsSelpos>=0):
            drawBracketsAround(settings[settingsSelpos], 72+xScrollPos + thumby.display.width//2, yScrollPos+40+selectOffset+scrollDisplayed, 1)
        settingsHeader.x=72+xScrollPos + 72//2 - 46//2 +1
        settingsHeader.y=max(0,yScrollPos+40)
        thumby.display.drawSprite(settingsHeader)
        
        
        if(ticks_ms() % 1000 < 500 and settingsSelpos<0 and yScrollTarget == -40 and xScrollTarget == -72):
            thumby.display.blit(leftArrowBAinv, 72+xScrollPos + 6, yScrollPos+40 +1, 3, 5,1,0,0)
    
    if(scroll < 0):
        scroll += 1
        if(scroll < -4):
            scroll += 1
    if(scroll > 0):
        scroll -= 1
        if(scroll > 4):
            scroll -= 1
    
    thumby.display.update()
    frameCounter+=1
    
    if(thumby.inputJustPressed()):
        if(noButtonPress):
            noButtonPress = False
        if(thumby.buttonD.pressed()):
            if QuickLoad == 0:
                if(yScrollTarget == 0 and yScrollPos == yScrollTarget):
                    yScrollTarget = -40
                elif(yScrollTarget <= -40 and yScrollPos == yScrollTarget):
                    if(xScrollTarget == 0 and selpos < len(files)-1):
                        selpos += 1
                        scroll = 8
                    elif xScrollTarget == 0 and selpos == len(files) -1:
                        selpos = -1
                    if(xScrollTarget == -72 and settingsSelpos < len(settings)-1):
                        settingsSelpos += 1
                        scroll = 8
            else:
                if(xScrollTarget == 0 and selpos < len(files)-1):
                    selpos += 1
                    scroll = 8
                elif xScrollTarget == 0 and selpos == len(files) -1:
                    selpos = -1
                if(xScrollTarget == -72 and settingsSelpos < len(settings)-1):
                    settingsSelpos += 1
                    scroll = 8
        if(thumby.buttonU.pressed()):
            if QuickLoad == 0:
                if(yScrollPos == yScrollTarget):
                    if(xScrollTarget == 0):
                        if(selpos > 0):
                            selpos -= 1
                            scroll = -8
                        else:
                            if(selpos>-1):
                                selpos=-1
                            else:
                                yScrollTarget=0
                    if(xScrollTarget == -72):
                        if(settingsSelpos > 0):
                            settingsSelpos -= 1
                            scroll = -8
                        else:
                            if(settingsSelpos>-1):
                                settingsSelpos=-1
                            else:
                                yScrollTarget=0
                                xScrollTarget=0
                    if yScrollPos == 0:
                        selpos = len(files) -1
                        yScrollTarget = -40
            else:
                if(xScrollTarget == 0):
                    if(selpos > 0):
                        selpos -= 1
                        scroll = -8
                    else:
                        if(selpos>-1):
                            selpos=-1
                        elif selpos == -1:
                            selpos = len(files) -1
                if(xScrollTarget == -72):
                    if(settingsSelpos > 0):
                        settingsSelpos -= 1
                        scroll = -8
                    else:
                        if(settingsSelpos>-1):
                            settingsSelpos=-1
                
        if(thumby.buttonR.pressed()):
            if(yScrollPos == -40 and yScrollPos == yScrollTarget):
                if(xScrollTarget == 0 and xScrollPos == xScrollTarget and selpos==-1 and settingsSelpos==-1):
                    xScrollTarget = -72
        if(thumby.buttonL.pressed()):
            if(yScrollPos == -40 and yScrollPos == yScrollTarget):
                if(xScrollTarget == -72 and xScrollPos == xScrollTarget and selpos==-1 and settingsSelpos==-1):
                    xScrollTarget = 0
        if(thumby.buttonA.pressed() or thumby.buttonB.pressed()):
            if QuickLoad == 0:
                if(yScrollTarget == 0 and xScrollTarget == 0):
                    launchGame()
            else:
                if xScrollTarget == 0 and selpos == -1:
                    launchGame()
            if(yScrollTarget <= -40):
                if(xScrollTarget == 0 and selpos>=0):
                    launchGame()
                if(xScrollTarget == -72):
                    if settingsSelpos == -1:
                        systemSettings()
                    if(settingsSelpos==0):
                        audioSetting= (audioSetting+1) % 2
                        thumby.audio.setEnabled(audioSetting)
                        saveCfg('thumby', "audioenabled", str(audioSetting))
                        thumby.audio.play(500,20)
                    if(settingsSelpos==1):
                        if briteSlider == 0:
                            brightnessSetting= (brightnessSetting+1) % 3
                            thumby.display.brightness(brightnessVals[brightnessSetting])
                            saveCfg('thumby', "brightness", str(brightnessSetting))
                        else:
                            briteSetting()
                    settings=[audioSettings[audioSetting], brightnessSettings[brightnessSetting], batteryPercent[0]]

thumby.reset()