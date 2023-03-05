from sys import path as syspath
syspath.insert(0, '/Games/RocketCup')

import time
import math
import thumbyGrayscale as thumby
#import thumby
import thumbyAudio
import random
from thumbySaves import saveData
from machine import Pin, UART

thumby.display.setFPS(30)

try:
    import emulator
    emulated = True
except ImportError:
    emulated = False

def lerp(v1,v2,f):
    return v1 + (v2-v1) * f
    
def saveDataOptItem(key, default):
    if (saveData.hasItem(key)):
        return saveData.getItem(key)
    else:
        return default

try:
    
    sprBallTex = thumby.Sprite(12, 12, [bytearray([231,231,255,60,60,255,231,231,255,60,60,255,
               9,9,15,15,15,15,9,9,15,15,15,15]),bytearray([60,60,219,231,231,219,60,60,219,231,231,219,
               15,15,6,9,9,6,15,15,6,9,9,6])])
    sprBallVoid = thumby.Sprite(18, 18, bytearray([0,0,0,0,0,0,128,192,192,192,192,128,0,0,0,0,0,0,
               0,0,0,0,0,0,7,15,15,15,15,7,0,0,0,0,0,0,
               0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]), key=1)
    sprBallOutline = thumby.Sprite(8, 8, [bytearray([60,66,129,129,129,129,66,60]),bytearray([0,64,128,128,128,128,64,60])], key=0)
    
    # BITMAP: width: 16, height: 8
    bmpWipe = bytearray([119,238,119,238,187,221,187,221,221,187,221,187,238,119,238,119])
    
    saveData.setName("RocketCup")
    sdSound = saveDataOptItem("sound",1)
    sdGrayscale = saveDataOptItem("grayscale",1)
    sdAi = saveDataOptItem("ai",0)
    sdTurnAssist = saveDataOptItem("turn-assist",0)
    
    if (not sdGrayscale):
        thumby.display.disableGrayscale()
        
    thumbyAudio.audio.setEnabled(sdSound)
    
    
    ###############
    ## MENU LOOP ##
    ###############
    
    
    # BITMAP: width: 45, height: 40
    bmpMenuCar = bytearray([0,88,16,96,224,96,96,96,48,48,48,48,16,24,24,24,24,24,24,29,10,4,8,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,
               0,0,0,240,240,240,224,240,184,240,240,248,232,194,140,152,194,68,105,249,251,248,252,252,248,248,240,224,192,128,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,
               0,160,128,192,187,247,215,31,47,15,15,11,127,95,255,255,252,248,240,224,193,131,143,255,231,135,135,3,3,3,3,2,140,216,224,192,128,192,192,192,128,128,0,0,0,
               0,2,7,7,3,5,2,0,0,0,0,0,0,1,15,15,31,31,31,31,47,63,255,255,191,127,63,63,255,255,127,255,255,255,255,255,255,255,255,239,15,7,3,3,0,
               0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,31,62,63,0,7,2,0,0,0,0,1,3,12,11,11,0,9,0,4,4,18,1,0,1,0,0])
    bmpsMenuCar = bytearray([16,120,112,224,224,224,96,112,240,240,112,112,56,56,56,56,120,248,31,31,30,28,24,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,
               0,0,112,248,184,48,16,112,233,223,140,28,62,62,126,126,190,191,191,175,15,14,22,12,24,8,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,
               0,252,254,254,255,250,248,248,248,249,115,127,126,252,248,33,198,12,216,1,66,198,184,0,116,4,132,132,128,128,130,134,136,248,0,64,192,64,64,192,0,128,128,0,0,
               0,3,15,31,63,63,63,31,15,1,0,0,0,3,15,31,27,30,157,235,251,242,227,226,230,224,232,193,209,224,192,52,192,128,144,64,128,11,222,255,254,252,255,127,0,
               0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,15,63,127,255,255,255,255,127,7,3,3,31,63,63,63,63,63,63,63,63,31,31,15,15,7,0,0])
    
    # BITMAP: width: 42, height: 8
    bmpMenuLogoRocket = bytearray([0,0,126,126,22,126,108,0,60,126,102,126,60,0,60,126,102,102,0,126,126,24,126,102,0,126,126,86,86,0,6,126,126,6,60,66,1,1,1,1,0,0])
    bmpsMenuLogoRocket = bytearray([60,126,129,193,233,129,219,255,195,129,153,193,227,255,195,129,153,221,255,129,193,231,129,221,255,129,129,169,253,255,249,129,193,253,255,195,129,129,129,129,66,60])
    
    # BITMAP: width: 33, height: 12
    bmpMenuLogoCup = bytearray([0,0,224,24,4,2,2,2,2,2,0,0,0,0,254,2,0,0,252,2,1,0,0,0,0,248,7,1,65,33,28,0,0,
               0,0,3,4,8,0,4,4,4,4,2,1,0,0,15,0,0,2,3,0,0,0,0,8,7,0,0,0,0,0,0,0,0])
    bmpsMenuLogoCup = bytearray([28,50,226,249,253,95,71,67,99,62,28,124,134,130,254,254,64,32,252,254,255,1,124,134,3,249,255,31,65,99,126,126,60,
               0,0,3,7,15,14,12,12,12,4,2,1,0,0,15,15,12,6,7,15,15,4,0,8,15,15,15,8,0,0,0,0,0])
    
    # BITMAP: width: 33, height: 8
    bmpMenuLogoCupShineA = bytearray([0,0,224,248,252,30,6,2,2,2,0,0,0,0,254,254,0,0,252,254,255,0,0,0,0,248,255,31,65,99,126,126,60])
    bmpsMenuLogoCupShineA = bytearray([28,50,2,225,249,93,69,65,97,60,28,124,134,130,0,252,64,32,0,252,254,1,124,134,3,1,248,30,0,66,98,126,60])
    bmpMenuLogoCupShineB = bytearray([0,0,3,7,15,14,12,12,12,4,2,1,0,0,15,15,12,6,7,15,15,4,0,8,15,15,15,8,0,0,0,0,0])
    bmpsMenuLogoCupShineB = bytearray([0,0,0,3,7,14,8,8,8,0,0,0,0,0,0,15,12,4,4,15,15,4,0,0,8,15,15,8,0,0,0,0,0])
    # BITMAP: width: 8, height: 8
    bmpMenuLogoCupShineMaskA = bytearray([7,56,199,63,255,248,192,0])
    bmpMenuLogoCupShineMaskB = bytearray([240,240,241,254,241,255,255,254])
    bmpMenuLogoCupShineSliceA = bytearray(8)
    bmpsMenuLogoCupShineSliceA = bytearray(8)
    bmpMenuLogoCupShineSliceB = bytearray(8)
    bmpsMenuLogoCupShineSliceB = bytearray(8)
    
    sfxNav = [600,100]
    
    animFrame = 0
    animDuration = 45
    while (animFrame < animDuration + 5):
        animFrame += 1
        
        # Car Driving
        animLerp = ((-math.cos(math.pi * animFrame / animDuration) + 1) * 0.75) % 1
        animX = lerp(-70,70,animLerp)
        animY = lerp(-45,45,animLerp)
        thumby.display.fill(0)
        
        # Car Brake Jerk
        if (animFrame == animDuration + 5):
            animX = 0
            animY = 0
        elif (animFrame > animDuration):
            animX = 1
            animY = 1
        else:
            #Ball Rotation
            ballLerp = (-math.cos(math.pi * animFrame / animDuration) + 1)
            
        sprBallTex.x = 66 - 9 + ((int(ballLerp * 10+1)) % 6)
        sprBallTex.y = 6 - 9 + ((int(ballLerp * 5)) % 6)
        thumby.display.drawSprite(sprBallTex)
        sprBallVoid.x = 66 - 9
        sprBallVoid.y = 6 - 9
        thumby.display.drawSprite(sprBallVoid)
        
        thumby.display.blit([bmpMenuCar, bmpsMenuCar],round(animX),round(animY),45,40,-1,0,0)
        thumby.display.blit([bmpMenuLogoRocket,bmpsMenuLogoRocket],72 - 44,2,42,8,0,0,0)
        thumby.display.blit([bmpMenuLogoCup,bmpsMenuLogoCup],72 - 33,11,33,12,0,0,0)
        
        thumby.display.update()
    
    showOptions = False
    optionSelect = 0
    options = [["Play CPU"], 
            ["Link Cable"],
            ["Training"],
            ["Sound OFF","Sound ON"], 
            ["Display BW","Display GS"], 
            ["AI EASY","AI MEDIUM","AI HARD"],
            ["Turn ONCE","Turn SLOW","Turn FAST"],
            ["Credits"]]
    optionText = [0,0,0,sdSound,sdGrayscale,sdAi,sdTurnAssist,0]
    gameMode = -1
    
    thumby.display.setFont("/lib/font3x5.bin", 3, 5, 2)
    while (True):
        if (not showOptions and 
                (thumby.buttonL.justPressed() 
                or thumby.buttonR.justPressed()
                or thumby.buttonA.justPressed())):
            showOptions = True
        else:
            if (thumby.buttonR.justPressed()):
                optionSelect = (optionSelect + 1) % len(options)
                thumbyAudio.audio.play(sfxNav[0],sfxNav[1])
            elif (thumby.buttonL.justPressed()):
                optionSelect = (optionSelect + len(options) - 1) % len(options)
                thumbyAudio.audio.play(sfxNav[0],sfxNav[1])
            elif (thumby.buttonA.justPressed()):
                if (optionSelect == 0): # Play CPU
                    gameMode = 0
                    break
                
                elif (optionSelect == 1): # Link Cable
                    gameMode = 1
                    break
                
                elif (optionSelect == 2): # Training
                    gameMode = 2
                    break
                
                elif (optionSelect == 3): # Sound
                    sdSound = optionText[optionSelect] = (sdSound + 1) % 2
                    saveData.setItem("sound",sdSound)
                    saveData.save()
                    thumbyAudio.audio.setEnabled(sdSound)
                    thumbyAudio.audio.play(sfxNav[0],sfxNav[1])
    
                elif (optionSelect == 4): # Display
                    sdGrayscale = optionText[optionSelect] = (sdGrayscale + 1) % 2
                    saveData.setItem("grayscale",sdGrayscale)
                    saveData.save()
                    if (sdGrayscale):
                        thumby.display.enableGrayscale()
                    else:
                        thumby.display.disableGrayscale()
                    
                elif (optionSelect == 5): # AI
                    sdAi = optionText[optionSelect] = (sdAi + 1) % 3
                    saveData.setItem("ai",sdAi)
                    saveData.save()
                
                elif (optionSelect == 6): # Turn Assist
                    sdTurnAssist = optionText[optionSelect] = (sdTurnAssist + 1) % 3
                    saveData.setItem("turn-assist",sdTurnAssist)
                    saveData.save()
                    
                elif (optionSelect == 7): # Credits
                    gameMode = 3
                    break
        
        animFrame += 1
        ballLerp += abs((math.pi*math.sin((math.pi*animFrame)/100))/100)
        sprBallTex.x = 66 - 9 + ((int(ballLerp * 10+1)) % 6)
        sprBallTex.y = 6 - 9 + ((int(ballLerp * 5)) % 6)
        thumby.display.drawSprite(sprBallTex)
        sprBallVoid.x = 66 - 9
        sprBallVoid.y = 6 - 9
        thumby.display.drawSprite(sprBallVoid)
        
        thumby.display.blit([bmpMenuLogoRocket,bmpsMenuLogoRocket],72 - 44,2,42,8,0,0,0)
        thumby.display.blit([bmpMenuLogoCup,bmpsMenuLogoCup],72 - 33,11,33,12,0,0,0)
        
        shineFrame = min((animFrame * 3) % (30 * 15),(animFrame * 3 + 40) % (30 * 15))
        if (shineFrame < (33 + 7)):
            shineX = shineFrame - 7
            shineY = 11
            for i in range(8):
                j = shineX + i
                if (j < 0 or j >= 33):
                    bmpMenuLogoCupShineSliceA[i] = 0
                    bmpsMenuLogoCupShineSliceA[i] = 0
                    bmpMenuLogoCupShineSliceB[i] = 0
                    bmpsMenuLogoCupShineSliceB[i] = 0
                else:
                    bmpMenuLogoCupShineSliceA[i] = bmpMenuLogoCupShineA[j]
                    bmpsMenuLogoCupShineSliceA[i] = bmpsMenuLogoCupShineA[j]
                    bmpMenuLogoCupShineSliceB[i] = bmpMenuLogoCupShineB[j]
                    bmpsMenuLogoCupShineSliceB[i] = bmpsMenuLogoCupShineB[j]
            thumby.display.blitWithMask([bmpMenuLogoCupShineSliceA,bmpsMenuLogoCupShineSliceA], 
                    72 - 33 + shineX, shineY, 8, 8, 0, 0, 0, bmpMenuLogoCupShineMaskA)
            thumby.display.blitWithMask([bmpMenuLogoCupShineSliceB,bmpsMenuLogoCupShineSliceB], 
                    72 - 33 + shineX, shineY+8, 8, 8, 0, 0, 0, bmpMenuLogoCupShineMaskB)
                    
        thumby.display.blit([bmpMenuCar, bmpsMenuCar],0,0,45,40,0,0,0)
    
        if (showOptions):
            thumby.display.drawFilledRectangle(0, 40 - 11, 72, 9, 2)
            text = options[optionSelect][optionText[optionSelect]]
            thumby.display.drawText(text, 36 - int(5*len(text)/2), 40 - 9, 1)
        
        thumby.display.update()
    
    #Screen Wipe
    for i in range(72//4 + 4 + 5):
        for j in range(5):
            thumby.display.blit(bmpWipe,i*4-j*4-12,32-j*8,16,8,1,0,0)
        thumby.display.update()
    
    #[CPU,Linked,Training,Credits]
    oppExist = [True,True,False,False][gameMode]
    ballExist = [True,True,True,False][gameMode]
    scoreExist = [True,True,True,False][gameMode]
    goalExist = [True,True,True,False][gameMode]
    
    gmCPU = (gameMode == 0)
    gmLinked = (gameMode == 1)
    gmTraining = (gameMode == 2)
    gmCredits = (gameMode == 3)
    
    
    ####################
    ## LINK HANDSHAKE ##
    ####################
    
    
    class Link:
        mode = 0 # 0 = write first, 1 = read first
        syncFrames = 0
        
        def __init__(self):
            self.uart = UART(0, baudrate=115200, rx=Pin(1, Pin.IN), tx=Pin(0, Pin.OUT), timeout=1000, txbuf=1, rxbuf=1)
            Pin(2, Pin.OUT).value(1)
            while (self.uart.any() > 0):
                self.uart.read(1)
                
        def tryHandshake(self):
            self.uart.write(bytearray([0x80]))
            self.uart.read(1) #echo
            time.sleep(0.1) #enough time for a response
            while (self.uart.any() > 0):
                response = self.uart.read(1)[0]
                if (response == 0x81): #HandshakeAck
                    self.mode = 1
                    return True
            return False
            
        def tryHandshakeAck(self):
            while (self.uart.any() > 0):
                response = self.uart.read(1)[0]
                if (response == 0x80): #Handshake
                    self.uart.write(bytearray([0x81]))
                    self.uart.read(1) #echo
                    self.mode = 0
                    return True
            return False
            
        def sync(self,data):
            self.syncFrames += 1
            self.waitCount = 0
            if (self.mode == 0): #write first
                self.uart.write(bytearray([data]))
                self.uart.read(1) #echo
                
                while (self.uart.any() == 0):
                    self.waitCount += 1
                
                return self.uart.read(1)[0]
                
            else: #read first
                while (self.uart.any() == 0):
                    self.waitCount += 1
                ret = self.uart.read(1)
                
                self.uart.write(bytearray([data]))
                self.uart.read(1) #echo
                
                return ret[0]
                
        def clear(self):
            while (link.uart.any() > 0):
                link.uart.read(1)
    
    class EmuLink:
        syncFrames = 0
        
        def tryHandshake(self):
            self.mode = 0
            return random.random() < 0.3
            
        def tryHandshakeAck(self):
            self.mode = 1
            return random.random() < 0.01
            
        def sync(self,data):
            self.syncFrames += 1
            return data
            
        def clear(self):
            pass
    
    if (gmLinked):
        if (emulated):
            link = EmuLink()
        else:
            link = Link()
        
        thumby.display.setFont("/lib/font3x5.bin", 3, 5, 2)
        thumby.display.drawText("CONNECTING", 36 - 23, 10, 1)
        HandshakeWait = 0
        while (True):
            if (HandshakeWait >= 30):
                HandshakeWait = 0
                if (link.tryHandshake()):
                    break
            else:
                if (link.tryHandshakeAck()):
                    break
            
            HandshakeWait += 1
            
            lineX = 36 + HandshakeWait
            thumby.display.drawLine(lineX-1, 20, lineX-1, 30, 0)
            thumby.display.drawLine(72-lineX+1, 20, 72-lineX+1, 30, 0)
            thumby.display.drawLine(lineX, 20, lineX, 30, 1)
            thumby.display.drawLine(72-lineX, 20, 72-lineX, 30, 1)
            thumby.display.update()
    
        thumby.display.drawText("MODE "+str(link.mode), 36 - 15, 35, 1)
        thumby.display.update()
        link.clear()
        time.sleep(1)
    
    
    ###############
    ## GAME LOOP ##
    ###############
    
    
    # BITMAP: width: 16, height: 16
    bmpCountdown3 = [bytearray([0,0,0,252,252,76,76,79,76,12,12,252,4,0,0,0,
               0,0,0,31,31,18,18,18,18,16,16,31,0,0,0,0]),
               bytearray([0,0,0,0,248,72,72,72,75,8,8,248,248,0,0,0,
               0,0,0,32,63,50,50,50,50,48,48,63,63,0,0,0])]
    bmpCountdown2 = [bytearray([0,0,0,252,252,220,204,79,12,12,156,252,4,0,0,0,
               0,0,0,31,31,17,16,16,18,19,19,31,0,0,0,0]),
               bytearray([0,0,0,0,248,216,200,72,11,8,152,248,248,0,0,0,
               0,0,0,32,63,49,48,48,50,51,51,63,63,0,0,0])]
    bmpCountdown1 = [bytearray([0,0,0,252,252,220,204,15,12,252,252,252,4,0,0,0,
               0,0,0,31,31,19,19,16,16,19,19,31,0,0,0,0]),
               bytearray([0,0,0,0,248,216,200,8,11,248,248,248,248,0,0,0,
               0,0,0,32,63,51,51,48,48,51,51,63,63,0,0,0])]
    bmpCountdownRotate1 = [bytearray([0,0,0,0,0,252,252,15,12,252,4,0,0,0,0,0,
               0,0,0,0,0,31,31,16,16,31,0,0,0,0,0,0]),
               bytearray([0,0,0,0,0,0,248,8,11,248,248,0,0,0,0,0,
               0,0,0,0,0,32,63,48,48,63,63,0,0,0,0,0])]
    bmpCountdownRotate2 = [bytearray([0,0,0,0,0,0,0,255,0,0,0,0,0,0,0,0,
               0,0,0,0,0,0,0,31,0,0,0,0,0,0,0,0]),
               bytearray([0,0,0,0,0,0,0,0,255,0,0,0,0,0,0,0,
               0,0,0,0,0,0,0,32,63,0,0,0,0,0,0,0])]
    bmpCountdownNumber = [bmpCountdown3,bmpCountdown2,bmpCountdown1]
    bmpCountdownAnim = [bmpCountdownRotate2,bmpCountdownRotate1,bmpCountdownNumber[0],bmpCountdownNumber[0],bmpCountdownRotate1]
    bmpCountdownArrow = [bytearray([24,40,79,129,129,79,40,24]),bytearray([0,16,48,126,126,48,16,0])]
    
    # BITMAP: width: 8, height: 8
    bmpCarUp = bytearray([0,0,100,90,90,100,0,0])
    bmpsCarUp = bytearray([0,0,100,38,38,100,0,0])
    bmpCarDiag = bytearray([0,16,40,76,58,18,12,0])
    bmpsCarDiag = bytearray([0,24,24,118,102,30,28,0])
    bmpCarRight = bytearray([0,60,36,24,24,36,24,0])
    bmpsCarRight = bytearray([0,36,60,0,0,60,24,0])
    
    bmpCarPlayer = bmpCarUp + bmpCarDiag + bmpCarRight
    bmpsCarPlayer = bmpsCarUp + bmpsCarDiag + bmpsCarRight
    bmpCarOpponent = bmpCarUp + bmpCarDiag + bmpCarRight
    bmpsCarOpponent = bmpsCarUp + bmpsCarDiag + bmpsCarRight
    
    bmpTrail0 = bytearray([0,0,0,0,0,0])
    bmpsTrail0 = bytearray([0,0,0,0,0,0])
    bmpTrail1 = bytearray([0,0,0,0,0,0])
    bmpsTrail1 = bytearray([0,0,12,12,0,0])
    bmpTrail2 = bytearray([0,0,12,12,0,0])
    bmpsTrail2 = bytearray([0,12,30,30,12,0])
    bmpTrail3 = bytearray([12,30,51,51,30,12])
    bmpsTrail3 = bytearray([12,18,33,33,18,12])
    bmpTrail4 = bytearray([0,0,0,0,0,0])
    bmpsTrail4 = bytearray([0,0,0,0,0,0])
    bmpTrails = bmpTrail0 + bmpTrail1 + bmpTrail2 + bmpTrail3 + bmpTrail4
    bmpsTrails = bmpsTrail0 + bmpsTrail1 + bmpsTrail2 + bmpsTrail3 + bmpsTrail4
    trailFrameCount = 5
    trailInterval = 2
    trailDuration = 16
    trailSpriteCount = (trailDuration + (trailInterval-1)) // trailInterval
    
    sprGoal = thumby.Sprite(4, 16, [bytearray([253,0,0,0,191,0,0,0]),bytearray([6,0,2,72,96,0,64,18])], key=0)

    bmpDigits = [bytearray([0,14,0]),
                bytearray([31,31,0]),
                bytearray([2,10,8]),
                bytearray([10,10,0]),
                bytearray([24,27,0]),
                bytearray([8,10,2]),
                bytearray([0,10,2]),
                bytearray([30,30,0]),
                bytearray([0,10,0]),
                bytearray([8,10,0])]
    sprDigit = thumby.Sprite(3,5, bmpDigits[0], key=1)

    bmpScoreTab = [bytearray([15,63,255,127,127,127,127,127,127,127,127,127,31,7,0]),
                bytearray([0,7,31,255,255,255,255,255,255,255,255,255,255,63,15])]
    
    mapRotX = [1,1,0,-1,-1,-1,0,1]
    mapRotY = [0,1,1,1,0,-1,-1,-1]
    
    speed1 = 0.75
    speed1MoveFrames = 30
    speed1StopFrames = 10
    speed1RevFrames = 5
    speed2 = 1.5
    
    class Car:
        x = 0.0
        y = 0.0
        
        rotate = 0
        gas = 0
        allowBoost = False
        
        speedShift = 0.0
        speed = 0
        
        trailCounter = 0
        trailNext = 0
        trailDecay = []
        
        sprTrails = []
        
        def __init__(self, bmpCars, bmpsCars):
            self.sprCar = thumby.Sprite(8, 8, [bmpCars, bmpsCars], key=0)
            for i in range(trailSpriteCount):
                self.sprTrails.append(thumby.Sprite(6, 6, [bmpTrails, bmpsTrails], key=0))
            for i in range(trailSpriteCount):
                self.trailDecay.append(0)
        
        def physicsUpdate(self):
            
            if (self.gas > 0):
                if (self.speedShift >= 0.0):
                    self.speedShift += 1.0 / speed1MoveFrames
                else:
                    self.speedShift += 1.0 / speed1RevFrames
                if (self.speedShift > 1.0):
                    self.speedShift = 1.0
            elif (self.gas < 0):
                if (self.speedShift >= 0.0):
                    self.speedShift -= 1.0 / speed1RevFrames
                else:
                    self.speedShift -= 1.0 / speed1RevFrames
                if (self.speedShift < -1.0):
                    self.speedShift = -1.0
            else:
                if (self.speedShift > 0.0):
                    self.speedShift -= 1.0 / speed1StopFrames
                    if (self.speedShift < 0.0):
                        self.speedShift = 0.0
                elif (self.speedShift < 0.0):
                    self.speedShift += 1.0 / speed1RevFrames
                    if (self.speedShift > 0.0):
                        self.speedShift = 0.0
    
            if (self.allowBoost and self.speedShift >= 1.0):
                self.speed = speed2
            elif (self.speedShift > 0.0):
                self.speed = speed1
            elif (self.speedShift < 0.0):
                self.speed = -speed1
            else:
                self.speed = 0
                
            self.trailCounter += 1
            
            self.x += self.speed * math.cos(self.rotate*math.pi/4.0)
            self.y += self.speed * math.sin(self.rotate*math.pi/4.0)
                
            if (self.x < 3):
                self.x = 3
            if (self.x > 69):
                self.x = 69
            if (self.y < 3):
                self.y = 3
            if (self.y > 37):
                self.y = 37
                    
        def draw(self):
            if (self.allowBoost and self.speedShift >= 1.0 and ((self.trailCounter % trailInterval) == 0)):
                self.sprTrails[self.trailNext].x = round(self.x) - 3
                self.sprTrails[self.trailNext].y = round(self.y) - 3
                self.trailDecay[self.trailNext] = trailDuration
                self.trailNext = (self.trailNext + 1) % trailSpriteCount
                
            for i in range(trailSpriteCount):
                if (self.trailDecay[i] > 0):
                    self.trailDecay[i] -= 1
                self.sprTrails[i].setFrame((trailFrameCount * self.trailDecay[i]) // trailDuration)
                thumby.display.drawSprite(self.sprTrails[i])
            
            if ((self.rotate % 2) == 1):
                self.sprCar.setFrame(1)
            elif ((self.rotate % 4) < 2):
                self.sprCar.setFrame(2)
            else:
                self.sprCar.setFrame(0)
                
            self.sprCar.mirrorX = 1 if (((self.rotate+5)%8)<3) else 0 #3,4,5
            self.sprCar.mirrorY = 1 if (((self.rotate+7)%8)<3) else 0 #1,2,3
            self.sprCar.x = round(self.x) - 4
            self.sprCar.y = round(self.y) - 4
            thumby.display.drawSprite(self.sprCar)
    
    ballDrag = 0.9
    
    class Ball:
        x = 0.0
        y = 0.0
        velX = 0.0
        velY = 0.0
        
    player = Car(bmpCarPlayer, bmpsCarPlayer)
    if (gmLinked):
        opponent = Car(bmpCarPlayer, bmpsCarPlayer)
    else:
        opponent = Car(bmpCarOpponent, bmpsCarOpponent)
    ball = Ball()
    
    if (gmLinked and link.mode == 1):
        car1 = opponent
        car2 = player
    else:
        car1 = player
        car2 = opponent
    
    scoreLeft = 0
    scoreRight = 0
    
    aiRotateInterval = [30,20,10][sdAi] if gmCPU else 0
    aiCanBoost = [False,True,True][sdAi] if gmCPU else True
    aiCanReverse = [False,False,True][sdAi] if gmCPU else True
    aiNextRotate = 0
    
    player.allowBoost = True
    opponent.allowBoost = aiCanBoost
    
    countdownFrames = 0
    countdownEnd = 20 * 3 + 10
    
    goal = False
    goalFrame = 0
    goalEnd = 40
    
    #[idle,slow,fast,boost]
    sfxCarHzVariation = 0.25
    sfxCarHzRange = [5.0,10.0,15.0,20.0]
    sfxCarFreqRange = [150,150,200,250]
    sfxCarDuration = 40
    sfxCarNextPlay = 0.0
    
    #[frequency,duration]
    sfxCountdownBeep = [600,200]
    sfxCarBump = [200,50]
    sfxBallKick = [300,100]
    sfxGoalBeep = [800,500]
    
    scoreTabWait = 0
    scoreTabLerp = 1.0
    
    turnAssistRateSlow = 10
    turnAssistRateFast = 5
    turnAssistFrame = 0
    turnAssistL = False
    turnAssistR = False
    
    if (gmCredits):
        creditNames = [
            "Demod",
            "acedent",
            "Adrian 2 Cool",
            "AyreGuitar",
            "hemlockmay",
            "JasonTC",
            "Laver:na",
            "Mason W",
            "Oliver2402",
            "speedyink",
            "SunnyChow",
            "TacoTormentor",
            "Timendus",
            "transistortester",
            ";;; TurtleMoon ;;;",
            "Unimatrix0",
            "Vali",
            "Windows Vista",
            "Xyvir",
            "THANK YOU FOR PLAYING ;"]
        for i in range(1,len(creditNames)-2):
            j = random.randrange(i+1,len(creditNames)-1)
            creditNames[i], creditNames[j] = creditNames[j], creditNames[i]
            
        # BITMAP: width: 50, height: 64 (5x7(8) letters - 0 to z)
        bmpCreditLetters = bytearray([62,81,73,69,62,0,66,127,64,0,66,97,81,73,70,33,65,69,75,49,24,20,18,127,16,47,73,73,73,49,60,74,73,73,48,3,113,9,5,3,54,73,73,73,54,6,73,73,41,30,
           56,84,86,85,24,12,18,36,18,12,0,0,12,12,0,0,2,0,4,0,2,32,0,8,0,0,4,0,18,0,0,48,52,0,0,124,18,17,18,124,127,73,73,73,54,62,65,65,65,34,
           127,65,65,34,28,127,73,73,73,65,127,9,9,9,1,62,65,73,73,122,127,8,8,8,127,0,65,127,65,0,32,64,65,63,1,127,8,20,34,65,127,64,64,64,64,127,2,12,2,127,
           127,4,8,16,127,62,65,65,65,62,127,9,9,9,6,62,65,81,33,94,127,9,25,41,70,70,73,73,73,49,1,1,127,1,1,63,64,64,64,63,31,32,64,32,31,63,64,56,64,63,
           99,20,8,20,99,7,8,112,8,7,97,81,73,69,67,0,0,12,8,126,127,8,12,0,0,0,8,20,54,21,21,54,20,8,0,30,18,12,18,12,12,18,12,18,30,32,84,84,84,120,
           127,72,68,68,56,56,68,68,68,40,56,68,68,72,127,56,84,84,84,24,8,126,9,1,2,8,84,84,84,60,127,8,4,4,120,0,68,125,64,0,32,64,68,61,0,0,127,16,40,68,
           0,65,127,64,0,124,4,24,4,120,124,8,4,4,120,56,68,68,68,56,124,20,20,20,8,8,20,20,24,124,124,8,4,4,8,72,84,84,84,32,4,63,68,64,32,60,64,64,32,124,
           28,32,64,32,28,60,64,32,64,60,68,40,16,40,68,12,80,80,80,60,68,100,84,76,68,0,0,1,0,0,0,0,64,8,0,1,0,0,0,4,0,24,28,28,0,64,0,0,1,0])

        # BITMAP: width: 30, height: 32 (3x4 letters - 0 to z)
        bmpCreditLettersTiny = bytearray([239,249,143,113,239,112,253,153,251,249,157,255,247,148,255,251,153,245,255,157,253,241,81,255,255,189,111,251,155,159,
           255,25,246,255,155,249,255,85,113,127,217,125,255,82,191,185,159,217,28,248,31,255,130,253,127,136,120,255,195,255,
           253,162,237,227,174,163,237,175,251,239,233,143,239,89,15,143,233,239,255,41,239,15,217,15,143,217,15,244,74,174,
           96,143,96,238,198,238,174,66,174,46,202,46,46,229,130,242,149,254,240,158,242,248,158,242,255,154,240,254,152,254])

        creditDebrisLetters = [12,13,14,15,16,75,76,77,78,79]
        creditSpecialLetters = [43,45,47]
        
        sprCreditDebris = []
        sprCreditLetters = []
        creditDebrisChance = 20
        creditSpecialChance = 5000
        
        creditsLettersX = 100
        creditsLettersY = 20
        creditsCarMinX = 26.0
        creditsCarMaxX = 46.0
        
        bmpCreditDebris = bytearray(5)
        creditPosition = 0
        creditNextDebrisCheck = 0
        creditRevealedCount = 0
        creditFrame = 0
    
    def resetField():
        global countdownFrames
        
        if (gmLinked):
            random.seed(link.syncFrames)
            
        if (gmTraining):
            ball.x = 40.0 + 16*random.random()
            ball.y = 8.0 + 32*random.random()
            ball.velX = 0.0
            ball.velY = 0.0
            car1.x = 32.0 - 16*random.random()
            car1.y = 8.0 + 32*random.random()
            car1.rotate = 0
            car1.speedShift = 0.0
            countdownFrames = countdownEnd
        
        elif (gmCredits):
            car1.x = 36.0
            car1.y = 20.0
            car1.rotate = 0
            car1.speedShift = 0.0
            countdownFrames = 0
            
        else: # CPU or Linked
            ball.x = 36.0
            ball.y = 20.0
            ball.velX = 0.0
            ball.velY = 0.0
            car1.x = 10.0
            car1.y = 20.0 + (random.random()-0.5)
            car1.rotate = 0
            car1.speedShift = 0.0
            car2.x = 61.0
            car2.y = 20.0 + (random.random()-0.5)
            car2.rotate = 4
            car2.speedShift = 0.0
            countdownFrames = 0
    
    resetField()
    
    thumby.display.setFont("/lib/font5x7.bin", 5, 7, 1)
            
    while(1):
        
        ### INPUTS
        
        if (sdTurnAssist > 0):
            if (sdTurnAssist == 1):
                turnAssistRate = turnAssistRateSlow
            elif (sdTurnAssist == 2):
                turnAssistRate = turnAssistRateFast
            
            if (thumby.buttonL.pressed()):
                turnAssistL = (turnAssistFrame % turnAssistRate) == 0
                turnAssistR = False
                turnAssistFrame += 1
            elif (thumby.buttonR.pressed()):
                turnAssistR = (turnAssistFrame % turnAssistRate) == 0
                turnAssistL = False
                turnAssistFrame += 1
            else:
                turnAssistR = False
                turnAssistL = False
                turnAssistFrame = 0
        
        inputPacket = 0
        if (thumby.buttonL.justPressed() or turnAssistL):
            inputPacket = inputPacket | 0x1
            player.rotate = (player.rotate + 7) % 8
        if (thumby.buttonR.justPressed() or turnAssistR):
            inputPacket = inputPacket | 0x2
            player.rotate = (player.rotate + 1) % 8
        if (thumby.buttonA.pressed()):
            inputPacket = inputPacket | 0x4
            player.gas = 1
        elif (thumby.buttonB.pressed()):
            inputPacket = inputPacket | 0x8
            player.gas = -1
        else:
            player.gas = 0
        
        if (gmLinked):
            linkedInput = link.sync(inputPacket)
            
            if (linkedInput&0x1): #buttonL just pressed
                opponent.rotate = (opponent.rotate + 7) % 8
            if (linkedInput&0x2): #buttonR just pressed
                opponent.rotate = (opponent.rotate + 1) % 8
            if (linkedInput&0x4): #buttonA
                opponent.gas = 1
            elif (linkedInput&0x8): #buttonB
                opponent.gas = -1
            else:
                opponent.gas = 0
    
        ### OPPONENT AI
        
        if (gmCPU):
            # Find target
            if (ball.x < 36):
                ballGoalDir = math.atan2(20-ball.y,-4-ball.x)
                aiTargetX = ball.x - 5 * math.cos(ballGoalDir)
                aiTargetY = ball.y - 5 * math.sin(ballGoalDir)
            else:
                if (opponent.x < ball.x):
                    if (opponent.y < 20):
                        aiTargetX = ball.x + 4
                        aiTargetY = ball.y + 8
                    else:
                        aiTargetX = ball.x + 4
                        aiTargetY = ball.y - 8
                else:
                    ballGoalDir = math.atan2(20-ball.y,75-ball.x)
                    aiTargetX = ball.x + 5 * math.cos(ballGoalDir)
                    aiTargetY = ball.y + 5 * math.sin(ballGoalDir)
                
            aiTargetDir = math.atan2(aiTargetY-opponent.y,aiTargetX-opponent.x)
            aiTargetRotate = round((4 * aiTargetDir) / math.pi)
            
            aiRotateDelta = (aiTargetRotate - opponent.rotate)
            if (aiRotateDelta > 4):
                aiRotateDelta -= 8
            if (aiRotateDelta < -4):
                aiRotateDelta += 8
            
            # Rotate towards target
            if (aiNextRotate > 0):
                aiNextRotate -= 1
            else:
                aiNextRotate = aiRotateInterval
                if (aiRotateDelta > 0):
                    opponent.rotate = (opponent.rotate + 1) % 8
                if (aiRotateDelta < 0):
                    opponent.rotate = (opponent.rotate + 7) % 8
            
            # Move if we are mostly aligned with target
            if (abs(aiRotateDelta) < 2):
                opponent.gas = 1
            elif (aiCanReverse and abs(aiRotateDelta) > 2):
                opponent.gas = -1
            else:
                opponent.gas = 0
                
        if (countdownFrames < countdownEnd):
            player.gas = 0
            opponent.gas = 0
        
        ### PHYSICS
        
        if (oppExist):
            # Car Collision
            carCarDist = math.sqrt((car2.y-car1.y)**2+(car2.x-car1.x)**2)
            if (carCarDist<7):
                carCarDir = math.atan2(car2.y-car1.y,car2.x-car1.x)
                carCarDx = (7-carCarDist) * math.cos(carCarDir)
                carCarDy = (7-carCarDist) * math.sin(carCarDir)
                car1.x -= carCarDx
                car1.y -= carCarDy
                car2.x += carCarDx
                car2.y += carCarDy
                if (not goal):
                    thumbyAudio.audio.play(sfxCarBump[0],sfxCarBump[1])
    
        car1.physicsUpdate()
        if (oppExist):
            car2.physicsUpdate()
        
        if (ballExist):
            ballKick = False
            ballPlayerDist = math.sqrt((ball.y-car1.y)**2+(ball.x-car1.x)**2)
            if (ballPlayerDist < 6):
                ballKick = True
                ballKickX = car1.x
                ballKickY = car1.y
                ballKickSpeed = car1.speed * 1.5
                ballPlayerDir = math.atan2(car1.y-ball.y,car1.x-ball.x)
                car1.x += min(1,(6-ballPlayerDist)) * math.cos(ballPlayerDir)
                car1.y += min(1,(6-ballPlayerDist)) * math.sin(ballPlayerDir)
        
            if (oppExist):
                ballOpponentDist = math.sqrt((ball.y-car2.y)**2+(ball.x-car2.x)**2)
                if (ballOpponentDist < 6):
                    if (ballKick):
                        ballKickX = (ballKickX + car2.x)/2
                        ballKickY = (ballKickY + car2.y)/2
                        ballKickSpeed = max(ballKickSpeed, car2.speed * 1.5)
                    else:
                        ballKick = True
                        ballKickX = car2.x
                        ballKickY = car2.y
                        ballKickSpeed = car2.speed * 1.5
                    ballOpponentDir = math.atan2(car2.y-ball.y,car2.x-ball.x)
                    car2.x += min(1,(6-ballOpponentDist)) * math.cos(ballOpponentDir)
                    car2.y += min(1,(6-ballOpponentDist)) * math.sin(ballOpponentDir)
        
            if (ballKick):
                kickDir = math.atan2(ball.y-ballKickY,ball.x-ballKickX)
                ball.velX = ballKickSpeed * math.cos(kickDir)
                ball.velY = ballKickSpeed * math.sin(kickDir)
                if (not goal):
                    thumbyAudio.audio.play(sfxBallKick[0],sfxBallKick[1])
        
            if (ball.y < 12 or ball.y > 28):
                if (ball.x < 4):
                    ball.x = 4
                    ball.velX = abs(ball.velX)
                if (ball.x > 68):
                    ball.x = 68
                    ball.velX = -abs(ball.velX)
                if (ball.y < 4):
                    ball.y = 4
                    ball.velY = abs(ball.velY)
                if (ball.y > 36):
                    ball.y = 36
                    ball.velY = -abs(ball.velY)
            else:
                if (math.sqrt((ball.y-12)**2+(ball.x)**2) < 4):
                    ball.velX = abs(ball.velX)
                    ball.velY = abs(ball.velY)
                if (math.sqrt((ball.y-28)**2+(ball.y)**2) < 4):
                    ball.velX = abs(ball.velX)
                    ball.velY = -abs(ball.velY)
                if (math.sqrt((ball.y-12)**2+(ball.x-71)**2) < 4):
                    ball.velX = -abs(ball.velX)
                    ball.velY = abs(ball.velY)
                if (math.sqrt((ball.y-28)**2+(ball.x-71)**2) < 4):
                    ball.velX = -abs(ball.velX)
                    ball.velY = -abs(ball.velY)
                if (ball.x <= -1):
                    ball.x = -1
                    ball.velX = 0
                if (ball.x >= 72):
                    ball.x = 72
                    ball.velX = 0
    
            ball.x += ball.velX
            ball.y += ball.velY
            
            ball.velX *= ballDrag
            ball.velY *= ballDrag
        
        ### CREDITS
        
        if (gmCredits):
            creditFrame += 1
            
            creditsShift = 0
            if (player.x < creditsCarMinX and creditPosition > 0):
                creditsShift = round(creditsCarMinX - player.x)
            if (player.x > creditsCarMaxX and creditPosition < len(creditNames)*200 + 100):
                creditsShift = round(creditsCarMaxX - player.x)
            
            creditPosition -= creditsShift
            
            player.x += creditsShift
            for spr in sprCreditDebris:
                spr.x += creditsShift
            for spr in sprCreditLetters:
                spr.x += creditsShift
            for spr in player.sprTrails:
                spr.x += creditsShift
            
            for spr in sprCreditLetters:
                if (not spr.revealed and max(abs(player.x-(spr.x+1)),abs(player.y-(spr.y+1))) < 7):
                    spr.revealed = True
                    spr.x -= 1
                    spr.y -= 1
                    spr.width = 5
                    spr.height = 7
                    spr.bitmap = spr.revealBitmap
                    creditRevealedCount += 1
                    if (creditRevealedCount == len(sprCreditLetters)):
                        for spr2 in sprCreditLetters:
                            spr2.origY = spr2.y
                            
                if (creditRevealedCount == len(sprCreditLetters)):
                    spr.y = round(spr.origY + 2*math.sin((creditPosition + creditFrame + spr.x)/10.0))
            
            if (len(sprCreditDebris) > 0):
                creditNextDebrisCheck = (creditNextDebrisCheck + 1) % len(sprCreditDebris)
                spr = sprCreditDebris[creditNextDebrisCheck]
                if (spr.x + spr.width < -1 or spr.x > 73):
                    sprCreditDebris.remove(spr)
                    
            if (creditsShift > 0): #Car moving left
                for i in range(creditsShift):
                    spawnX = -5 + i
                    if (random.randrange(creditDebrisChance) == 0):
                        pick = random.choice(creditDebrisLetters)
                        bmp = bmpCreditLetters[pick*5:pick*5+5]
                        if (sdGrayscale):
                            bmp = [bmpCreditDebris,bmp]
                        sprCreditDebris.append(thumby.Sprite(5,7,bmp,
                            x=spawnX,
                            y=random.randrange(33),
                            key=0,
                            mirrorX=random.getrandbits(1),
                            mirrorY=random.getrandbits(1)))
                    
                    spawnX = -10 + i
                    if (random.randrange(creditSpecialChance) == 0):
                        pick = random.choice(creditDebrisLetters)
                        bmp = bmpCreditLetters[pick*5:pick*5+10]
                        if (sdGrayscale):
                            bmp = [bmp,bmp]
                        sprCreditDebris.append(thumby.Sprite(10,7,bmp,
                            x=spawnX,
                            y=random.randrange(33),
                            key=0))
                    
            if (creditsShift < 0): #Car moving right
                for i in range(-creditsShift):
                    if ((creditPosition-i) % 200 == 100):
                        creditNameIndex = (creditPosition-i) // 200
                        if (creditNameIndex >= 0 and creditNameIndex < len(creditNames)):
                            sprCreditLetters.clear()
                            creditRevealedCount = 0
                            creditName = creditNames[creditNameIndex]
                            offset = 0
                            nameY = 5 + random.randrange(33-10)
                            if (creditNameIndex == 0 or creditNameIndex == len(creditNames)-1):
                                nameY = 20 - 3
                            for letter in creditName:
                                if (letter.isspace()):
                                    offset += 6
                                    continue
                                pick = ord(letter) - 48
                                
                                col = pick % 10
                                row = pick // 20
                                bank = (pick % 20) // 10
                                bmpOffset = (row * 10 + col) * 3
                                bmpTiny = bmpCreditLettersTiny[bmpOffset:bmpOffset+3]
                                for j in range(len(bmpTiny)):
                                    if (bank == 1):
                                        bmpTiny[j] = bmpTiny[j] >> 4
                                
                                bmp = bmpCreditLetters[pick*5:pick*5+5]
                                spr = thumby.Sprite(3,4,bmpTiny,
                                    x=72+offset+1,y=nameY+1,
                                    key=0)
                                spr.revealBitmap = bmp
                                spr.revealed = False
                                sprCreditLetters.append(spr)
                                offset += 6
                    
                    spawnX = 72 - i
                    if (random.randrange(creditDebrisChance) == 0):
                        pick = random.choice(creditDebrisLetters)
                        bmp = bmpCreditLetters[pick*5:pick*5+5]
                        if (sdGrayscale):
                            bmp = [bmpCreditDebris,bmp]
                        sprCreditDebris.append(thumby.Sprite(5,7,bmp,
                            x=spawnX,
                            y=random.randrange(33),
                            key=0,
                            mirrorX=random.getrandbits(1),
                            mirrorY=random.getrandbits(1)))
                    
                    if (random.randrange(creditSpecialChance) == 0):
                        pick = random.choice(creditSpecialLetters)
                        bmp = bmpCreditLetters[pick*5:pick*5+10]
                        if (sdGrayscale):
                            bmp = [bmp,bmp]
                        sprCreditDebris.append(thumby.Sprite(10,7,bmp,
                            x=spawnX,
                            y=random.randrange(33),
                            key=0))
            
        ### SCORING
        
        if (ballExist and not goal):
            if (ball.x <= -1 or ball.x >= 72):
                if (ball.x < 36):
                    scoreRight += 1
                    goalDirection = 1
                    if (gmCPU):
                        goalText = "CPU Scored!"
                    else:
                        goalText = "P2 Scored!"
                else:
                    scoreLeft += 1
                    goalDirection = -1
                    goalText = "P1 Scored!"
                
                if (gmTraining):
                    resetField()
                else:
                    goal = True
                    goalFrame = 0
                
                thumbyAudio.audio.play(sfxGoalBeep[0],sfxGoalBeep[1])
            
        ### SOUND
        
        if (sdSound):
            if (player.speedShift == 0.0): #Idle
                sfxCarHz = sfxCarHzRange[0]
                sfxCarFreq = sfxCarFreqRange[0]
            elif (player.speedShift == 1.0): #Boost
                sfxCarHz = sfxCarHzRange[3]
                sfxCarFreq = sfxCarFreqRange[3]
            else:
                sfxCarLerp = player.speedShift
                sfxCarHz = round(lerp(sfxCarHzRange[1],sfxCarHzRange[2],sfxCarLerp))
                sfxCarFreq = round(lerp(sfxCarFreqRange[1],sfxCarFreqRange[2],sfxCarLerp))
            if (thumbyAudio.audio.pwm.duty_u16() == 0): #Not playing anything
                if (sfxCarNextPlay <= 0.0):
                    variation = random.uniform(1.0-sfxCarHzVariation,1.0+sfxCarHzVariation)
                    thumbyAudio.audio.play(round(variation * sfxCarFreq), sfxCarDuration)
                    sfxCarNextPlay += variation / sfxCarHz
                sfxCarNextPlay -= 0.0333 # 1/30
        
        ### DISPLAY
        
        thumby.display.fill(0)
        
        if (ballExist):
            ballRoundX = round(ball.x)
            ballRoundY = round(ball.y)
            sprBallTex.x = ballRoundX - 9 + (ballRoundX % 6)
            sprBallTex.y = ballRoundY - 9 + (ballRoundY % 6)
            thumby.display.drawSprite(sprBallTex)
            sprBallVoid.x = ballRoundX - 9
            sprBallVoid.y = ballRoundY - 9
            thumby.display.drawSprite(sprBallVoid)
            sprBallOutline.x = ballRoundX - 4
            sprBallOutline.y = ballRoundY - 4
            thumby.display.drawSprite(sprBallOutline)
        
        #thumby.display.blit(bmpTrails[1], round(aiTargetX)-2,round(aiTargetY)-2,4,4,0,0,0);
        
        if (gmCredits):
            for spr in sprCreditDebris:
                thumby.display.drawSprite(spr)
            for spr in sprCreditLetters:
                thumby.display.drawSprite(spr)
        
        if (oppExist):
            car2.draw()
        car1.draw()
        
        if (goalExist):
            sprGoal.x = 0
            sprGoal.y = 12
            sprGoal.mirrorX = 0
            thumby.display.drawSprite(sprGoal)
            sprGoal.x = 68
            sprGoal.y = 12
            sprGoal.mirrorX = 1
            thumby.display.drawSprite(sprGoal)
        
        if (scoreExist):
            if (oppExist):
                minCarBallY = min(car1.y,car2.y,ball.y)
            else:
                minCarBallY = min(car1.y,ball.y)
            
            if (minCarBallY < 10):
                scoreTabWait = 30
                scoreTabLerp = max(0,scoreTabLerp-0.1)
            else:
                if (scoreTabWait > 0):
                    scoreTabWait -= 1
                else:
                    scoreTabLerp = min(1,scoreTabLerp+0.1)
                
            if (sdGrayscale):
                scoreTabY = round(lerp(-7,0,scoreTabLerp))
            else:
                scoreTabY = round(lerp(-8,0,scoreTabLerp))
            thumby.display.blit(bmpScoreTab,14,scoreTabY,15,8,0,0,0)
            thumby.display.blit(bmpScoreTab,43,scoreTabY,15,8,0,0,0)
            
            sprDigit.y = scoreTabY + 1
            sprDigit.x = 18
            sprDigit.bitmap = bmpDigits[(scoreLeft//10) % 10]
            thumby.display.drawSprite(sprDigit)
            sprDigit.x = 22
            sprDigit.bitmap = bmpDigits[scoreLeft % 10]
            thumby.display.drawSprite(sprDigit)
            sprDigit.x = 47
            sprDigit.bitmap = bmpDigits[(scoreRight//10) % 10]
            thumby.display.drawSprite(sprDigit)
            sprDigit.x = 51
            sprDigit.bitmap = bmpDigits[scoreRight % 10]
            thumby.display.drawSprite(sprDigit)
        
        if (goal):
            x = round(20*math.tan(goalDirection*((goalFrame+1)/(goalEnd+2) - 0.5)*math.pi))
            thumby.display.drawFilledRectangle(round(x*1.5),20-5,72,10,2)
            thumby.display.drawText(goalText,x+37-3*len(goalText),20-3,0)
            thumby.display.drawText(goalText,x+36-3*len(goalText),20-4,1)
            
            if (goalFrame == goalEnd//2):
                resetField()
            
            if (goalFrame < goalEnd):
                goalFrame += 1
            else:
                goal = False
        
        if (countdownFrames < countdownEnd - 10):
            bmpCountdownAnim[2] = bmpCountdownNumber[countdownFrames//20]
            bmpCountdownAnim[3] = bmpCountdownAnim[2]
            if (countdownFrames < 10):
                countdownY = -16 + 2*countdownFrames
            elif (countdownFrames >= 75):
                countdownY = 0 - (2*countdownFrames-75)
            else:
                countdownY = 0
            if ((countdownFrames % 20)==9):
                thumbyAudio.audio.play(sfxCountdownBeep[0],sfxCountdownBeep[1])
            thumby.display.blit(bmpCountdownAnim[(countdownFrames//4)%5], 28, countdownY, 16, 16, 0, 0, 0)
            
            if (oppExist and (countdownFrames % 10) < 5):
                thumby.display.blit(bmpCountdownArrow, round(player.x) - 4, round(player.y) - 12, 8, 8, 0, 0, 0)
            
        if (countdownFrames < countdownEnd):
            countdownFrames += 1
        
        thumby.display.update()

except Exception as e:
    f = open("/crash.log", "w")
    f.write(str(e))
    f.close()
    raise e