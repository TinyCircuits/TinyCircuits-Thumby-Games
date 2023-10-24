import thumby
import random
spr_cam = thumby.Sprite(72,40,"/Games/TinyFreddy/Cams.bin",0,0)

def static(frame):
    if(frame%4 == 0):
        # BITMAP: width: 72, height: 40
        bit_0 = bytearray([0,0,4,4,4,4,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,4,4,4,4,4,4,4,4,4,4,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,32,32,32,32,32,32,32,32,0,0,0,0,0,0,0,0,0,0,0,0,0,
                0,0,0,0,0,0,0,0,0,0,0,8,8,8,8,8,8,8,8,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,
                0,0,0,0,0,0,0,64,64,64,64,64,64,64,64,64,64,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,2,2,2,2,2,2,2,2,2,0,0,0,0,0,0,0,0,0,0,0,
                0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,
                0,0,0,0,0,0,0,0,64,64,64,64,64,64,64,64,64,64,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,16,16,16,16,16,16,16,16,16,16,16,16,16,16,16,16,16,0,0,0,0,0,0,0,0,0])
    
    if(frame%4 == 1):
        # BITMAP: width: 72, height: 40
        bit_0 = bytearray([0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,16,16,16,16,16,16,16,16,16,16,16,16,16,16,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,128,128,128,128,128,128,128,128,128,128,128,128,128,0,0,0,0,
                0,0,0,32,32,32,32,32,32,32,32,32,32,32,32,32,0,0,0,0,0,0,0,0,0,0,0,0,0,64,64,64,64,64,64,64,64,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,
                0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,128,128,128,128,128,128,128,128,128,128,128,128,128,128,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,
                0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,
                0,0,0,0,0,0,0,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,8,8,8,8,8,8,8,8,8,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0])
    
    if(frame%4 == 2):
        # BITMAP: width: 72, height: 40
        bit_0 = bytearray([0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,8,8,8,8,8,8,8,8,8,8,8,8,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,
                0,0,0,0,0,0,32,32,32,32,32,32,32,32,32,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,32,32,32,32,32,32,32,32,32,32,32,32,32,32,32,32,32,0,0,0,0,0,0,0,
                0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,8,8,8,8,8,8,8,8,8,8,8,8,8,8,8,8,8,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,
                0,0,0,0,0,4,4,4,4,4,4,4,4,4,4,4,4,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,32,32,32,32,32,32,32,32,32,32,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,
                0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,8,8,8,8,8,8,8,8,8,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,32,32,32,32,32,32,32,32,32,32,32,32,32,32,0])
    
    if(frame%4 == 3):
        # BITMAP: width: 72, height: 40
        bit_0 = bytearray([0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,64,64,64,64,64,64,64,64,64,64,64,64,64,64,64,0,0,
                0,1,1,1,1,1,1,1,1,1,1,1,1,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,4,4,4,4,4,4,4,4,4,4,4,4,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,
                0,0,0,0,0,0,0,0,0,0,0,4,4,4,4,4,4,4,4,4,4,4,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,
                0,0,128,128,128,128,128,128,128,128,128,128,128,128,128,128,128,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,16,16,16,16,16,16,16,16,16,16,16,16,16,16,16,16,0,0,0,0,0,0,
                0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,8,8,8,8,8,8,8,8,8,8,8,8,8,8,8,8,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0])
    
    thumby.display.blit(bit_0,0,0,72,40,0,0,0)

def getcamera(cam,camstate,freddyl,bonniel,chical,foxyl):
    
    spr_cam = thumby.Sprite(72,40,"/Games/TinyFreddy/Cams.bin",0,0)
    spr_cam.setFrame(0)
    
    if(cam == 0):
        text = "1a"
        if(bonniel == 0):
            if(chical == 0):
                spr_cam.setFrame(0)
            else:
                spr_cam.setFrame(1)
        elif(chical == 0):
            spr_cam.setFrame(2)
        elif(freddyl == 0):
            spr_cam.setFrame(3)
        else:
            spr_cam.setFrame(4)
    if(cam == 1):
        text = "1b"
        if(bonniel == 1):
            if(chical == 1):
                spr_cam.setFrame(8)
            else:
                spr_cam.setFrame(6)
        elif(chical == 1):
            spr_cam.setFrame(7)
        elif(freddyl == 1):
            spr_cam.setFrame(9)
        else:
            spr_cam.setFrame(10)
    if(cam == 2):
        text = "1c"
        if(foxyl == 0):
            spr_cam.setFrame(11)
        elif(foxyl == 1):
            spr_cam.setFrame(12)
        elif(foxyl == 2):
            spr_cam.setFrame(13)
        else:
            spr_cam.setFrame(14)
    if(cam == 3):
        text = "2a"
        if(foxyl == 3):
            spr_cam.setFrame(37+camstate)
            rand = random.randint(0,2)
            if(rand < 2):
                if(bonniel == 3):
                    spr_cam.setFrame(15)
                else:
                    spr_cam.setFrame(16)
            else:
                spr_cam.setFrame(17)
    if(cam == 4):
        text = "2b"
        if(bonniel == 5):
            rand = random.randint(0,6)
            if(rand < 3):
                spr_cam.setFrame(18)
            elif(rand < 6):
                spr_cam.setFrame(19)
            else:
                spr_cam.setFrame(20)
        else:
            spr_cam.setFrame(21)
    if(cam == 5):
        text = "3"
        if(bonniel == 4):
            spr_cam.setFrame(22)
        else:
            spr_cam.setFrame(23)
    if(cam == 6):
        text = "4a"
        if(chical == 4):
            spr_cam.setFrame(24)
        elif(freddyl == 4):
            spr_cam.setFrame(25)
        else:
            spr_cam.setFrame(26)
    if(cam == 7):
        text = "4b"
        if(chical == 5):
            rand = random.randint(0,6)
            if(rand < 3):
                spr_cam.setFrame(27)
            elif(rand < 6):
                spr_cam.setFrame(28)
            else:
                spr_cam.setFrame(29)
        elif(freddyl == 5):
            spr_cam.setFrame(30)
        else:
            spr_cam.setFrame(31)
    if(cam == 8):
        text = "5"
        if(bonniel == 2):
            spr_cam.setFrame(32)
        else:
            spr_cam.setFrame(33)
    if(cam == 10):
        if(chical == 2):
            spr_cam.setFrame(34)
        elif(freddyl == 2):
            spr_cam.setFrame(35)
        else:
            spr_cam.setFrame(36)
    if(cam == 9):
        thumby.display.drawText("CAMERA DISABLED",6,13,1)
        thumby.display.drawText("AUDIO ONLY",16,19,1)
    else:
        thumby.display.drawSprite(spr_cam)
    

def camMap(cam,camMode):
    #Camera Map
    if(camMode == 1):
        # BITMAP: width: 37, height: 31
        bit_0 = bytearray([240,16,16,240,160,240,16,16,16,16,16,31,17,17,17,17,17,17,17,17,31,16,16,16,16,16,240,0,128,128,128,128,0,128,128,128,128,
           7,4,244,23,16,255,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,255,5,255,0,0,255,69,239,40,40,239,
           0,240,17,17,241,67,250,14,10,14,250,2,34,66,250,66,34,2,250,14,10,14,250,2,254,10,15,8,11,10,10,251,1,3,2,2,3,
           0,3,2,2,3,1,127,64,64,64,127,20,62,34,34,34,62,20,127,64,64,64,127,0,3,2,2,2,2,2,2,3,0,0,0,0,0])
        
        thumby.display.blit(bit_0,35,9,37,31,0,0,0)
        
        # BITMAP: width: 37, height: 31
        bit_0 = bytearray([255,31,31,255,191,255,31,31,31,31,31,31,17,17,17,17,17,17,17,17,31,31,31,31,31,31,255,255,255,255,255,255,255,255,255,255,255,
           255,252,252,31,31,255,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,255,253,255,0,0,255,125,255,56,56,255,
           255,255,31,31,255,127,254,14,10,14,254,254,254,254,254,254,254,254,254,14,10,14,254,254,254,10,15,15,15,14,14,255,255,255,254,254,255,
           127,127,126,126,127,127,127,64,64,64,127,119,127,99,99,99,127,119,127,64,64,64,127,127,127,126,126,126,126,126,126,127,127,127,127,127,127])
        
        thumby.display.blit(bit_0,35,9,37,31,1,0,0)
        
        text = ""
        
        if(cam == 0):
            thumby.display.drawRectangle(46,9,10,5,0)
            thumby.display.drawFilledRectangle(47,10,8,3,1)
            text = "1a"
        
        elif(cam == 1):
            thumby.display.drawRectangle(40,13,22,14,0)
            thumby.display.drawFilledRectangle(41,14,20,12,1)
            text = "1b"
        
        elif(cam == 2):
            thumby.display.drawRectangle(37,21,4,5,0)
            thumby.display.drawFilledRectangle(38,22,2,3,1)
            text = "1c"
        
        elif(cam == 3):
            thumby.display.drawRectangle(41,28,5,7,0)
            thumby.display.drawFilledRectangle(42,29,3,5,1)
            text = "2a"
        
        elif(cam == 4):
            thumby.display.drawRectangle(41,35,5,5,0)
            thumby.display.drawFilledRectangle(42,36,3,3,1)
            text = "2b"
        
        elif(cam == 5):
            thumby.display.drawRectangle(36,29,4,6,0)
            thumby.display.drawFilledRectangle(37,30,2,4,1)
            text = "3"
        
        elif(cam == 6):
            thumby.display.drawRectangle(53,28,5,7,0)
            thumby.display.drawFilledRectangle(54,29,3,5,1)
            text = "4a"
        
        elif(cam == 7):
            thumby.display.drawRectangle(53,35,5,5,0)
            thumby.display.drawFilledRectangle(54,36,3,3,1)
            text = "4b"
        
        elif(cam == 8):
            thumby.display.drawRectangle(35,13,4,7,0)
            thumby.display.drawFilledRectangle(36,14,2,5,1)
            text = "5"
        
        elif(cam == 9):
            thumby.display.drawRectangle(59,28,8,7,0)
            thumby.display.drawFilledRectangle(60,29,6,5,1)
            text = "6"
        
        elif(cam == 10):
            thumby.display.drawRectangle(63,16,4,11,0)
            thumby.display.drawFilledRectangle(64,17,2,9,1)
            text = "7"
        
        thumby.display.drawFilledRectangle(0,34,12+(len(text)*4),6,0)
        thumby.display.drawText("CAM"+text,0,35,1)