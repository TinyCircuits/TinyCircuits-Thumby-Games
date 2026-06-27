import thumby
import random
def static(frame,mode):
    spr_static = thumby.Sprite(72,40,"/Games/TinyFreddy/CamFlip.bin",0,0,0)
    if(mode == 0):
        spr_static.setFrame((frame%4)+14)
        thumby.display.drawSprite(spr_static)
    else:
        if(frame%2):
            xtra = 1.1*(((frame%50)/10)-2)
            thumby.display.drawLine(13,round((frame%50)+xtra),35,(frame%50),1)
            thumby.display.drawLine(35,(frame%50),57,round((frame%50)+xtra),1)
            thumby.display.drawLine(0,round((frame%50)+xtra*3),13,round((frame%50)+xtra),1)
            thumby.display.drawLine(57,round((frame%50)+xtra),71,round((frame%50)+xtra*3),1)
        s = 20
        while(s>0):
            rl = random.randint(1,16)
            rx = random.randint(0,72-rl)
            ry = random.randint(0,39)
            while(rl > 0):
                thumby.display.setPixel(rx+rl,ry,1)
                rl -= 1
            s -= 1
def getcamera(cam,camstate,freddyl,bonniel,chical,foxyl):
    spr_cam = thumby.Sprite(72,40,"/Games/TinyFreddy/Cams.bin",0,0)
    spr_cam.setFrame(0)
    if(cam == 0):
        text = "1a"
        if(bonniel == 0):
            if(chical == 0):
                if((camstate % 50) == 6):
                    spr_cam.setFrame(68)
                else:
                    spr_cam.setFrame(0)
            else:
                spr_cam.setFrame(1)
        elif(chical == 0):
            spr_cam.setFrame(2)
        elif(freddyl == 0):
            if((camstate % 10) == 9):
                    spr_cam.setFrame(69)
            else:
                spr_cam.setFrame(3)
        else:
            spr_cam.setFrame(4)
    if(cam == 1):
        text = "1b"
        if(bonniel == 1):
            if(chical == 1):
                spr_cam.setFrame(8)
            else:
                if((camstate % 5) == 4):
                    spr_cam.setFrame(70)
                else:
                    spr_cam.setFrame(6)
        elif(chical == 1):
            if((camstate % 5) == 4):
                spr_cam.setFrame(71)
            else:
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
            if((camstate % 10) == 8):
                spr_cam.setFrame(72)
            else:
                spr_cam.setFrame(14)
    if(cam == 3):
        text = "2a"
        if(foxyl == 3):
            spr_cam.setFrame(37+camstate)
            rand = random.randint(0,2)
        else:
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
            if((camstate % 100) == 20):
                spr_cam.setFrame(73)
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
            if((camstate % 2) == 0):
                spr_cam.setFrame(74)
            else:
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
            if((camstate % 5) == 2):
                spr_cam.setFrame(76)
            else:
                spr_cam.setFrame(32)
        else:
            if((camstate % 100) == 2):
                spr_cam.setFrame(75)
            else:
                spr_cam.setFrame(33)
    if(cam == 10):
        if(chical == 2):
            if((camstate % 2) == 0):
                spr_cam.setFrame(77)
            else:
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
        temp = [47,10,8,3,"1a"]
        if(cam == 1):
            temp = [41,14,20,12,"1b"]
        elif(cam == 2):
            temp = [38,22,2,3,"1c"]
        elif(cam == 3):
            temp = [42,29,3,5,"2a"]
        elif(cam == 4):
            temp = [42,36,3,3,"2b"]
        elif(cam == 5):
            temp = [37,30,2,4,"3"]
        elif(cam == 6):
            temp = [54,29,3,5,"4a"]
        elif(cam == 7):
            temp = [54,36,3,3,"4b"]
        elif(cam == 8):
            temp = [36,14,2,5,"5"]
        elif(cam == 9):
            temp = [60,29,6,5,"6"]
        elif(cam == 10):
            temp = [64,17,2,9,"7"]
        thumby.display.drawFilledRectangle(temp[0],temp[1],temp[2],temp[3],1)
        thumby.display.drawFilledRectangle(0,34,12+(len(temp[4])*4),6,0)
        thumby.display.drawText("CAM"+temp[4],0,35,1)