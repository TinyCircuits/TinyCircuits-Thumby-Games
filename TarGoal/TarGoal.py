#TarGoal v0.2
#by Nemo.the.fishboy

import thumby
import os
import json
import ujson
import time

try:
    try:
        targetslist = open("./Games/TarGoal/targetslist.json", "r+")
    except OSError:
        print("savefile does not exist, creating...")
        targetslist = open("./Games/TarGoal/targetslist.json", "w+")
        json.dump({"list":["First task","The second task is done!"],"check":[0,1],"icon":[0,2]}, targetslist) # Write default data to the save file
        targetslist.seek(0, 0)
    saveData=json.load(targetslist)
    ls=saveData["list"]
    ch=saveData["check"]
    ic=saveData["icon"]
    
    number_of_elements = len(ls)
    l = 0
    j = 0
    k = 0
    i = 0
    x = 3
    start = 0
    ictoch = 0
    eltoch = None
    eltochtext = ""
    chtoch = 0
    newtext = ""
    xpos = 3
    received = None
    text1 = ""
    thumby.display.setFPS(30)
    
    #-----------------------------
    
    # BITMAP: width: 72, height: 40
    bitmapthumbnail = bytearray([255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,127,127,159,159,231,103,185,217,217,217,217,185,103,231,159,159,127,127,255,255,255,
            255,255,255,255,127,191,127,255,127,191,63,127,253,253,221,237,237,109,109,127,255,231,219,189,189,153,165,189,153,165,189,189,189,189,189,189,189,189,189,189,189,129,129,195,195,231,231,255,255,129,129,126,126,195,189,126,195,189,126,102,102,126,189,195,126,189,195,126,126,129,129,255,
            127,63,31,96,127,125,126,126,127,125,118,91,108,53,67,127,126,255,255,255,159,159,159,159,159,159,159,159,31,31,159,159,159,159,159,159,255,255,255,255,255,255,127,191,223,111,111,111,175,175,47,110,222,57,249,231,230,157,155,155,155,155,157,230,231,249,249,254,126,127,127,255,
            0,128,64,224,160,80,240,160,92,254,246,160,80,240,224,192,248,0,1,255,255,255,255,255,255,255,255,255,0,0,255,255,243,243,51,51,51,51,15,15,255,255,0,255,3,2,207,207,243,19,83,82,222,30,63,207,39,55,207,63,254,109,183,180,183,13,254,255,0,255,0,182,
            0,1,3,3,2,5,7,10,5,63,127,98,5,7,3,1,3,0,0,255,255,255,255,255,255,255,255,255,192,192,255,255,240,240,207,201,201,207,240,240,207,207,254,253,192,192,250,250,218,218,250,250,219,216,255,252,219,217,252,255,255,156,235,234,235,156,251,255,224,239,224,237])
    startscreen = thumby.Sprite(72, 40, bitmapthumbnail, 0,0)
    
    #-----------------------------
    
    #image with arrows - image
    # BITMAP: width: 72, height: 40
    bitmap1 = bytearray([255,255,255,127,191,223,239,199,239,223,191,127,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,251,249,249,251,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,
           255,255,254,252,250,247,239,199,239,247,250,252,254,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,
           255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,
           255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,
           255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,223,159,159,223,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255])
    arrows = thumby.Sprite(72, 40, bitmap1)
    #-----------------------------
    
    # BITMAP: width: 15, height: 9
    bitmap2 = bytearray([249,1,253,132,252,132,253,1,249,255,241,254,158,238,241,
               1,1,0,0,0,0,0,1,1,1,1,1,0,1,1])
    trashbin = thumby.Sprite(15, 9, bitmap2, 50, 5)
    
    #-----------------------------
    
    # BITMAP: width: 15, height: 9
    bitmap3 = bytearray([255,191,31,15,31,17,17,17,17,17,241,224,241,251,255,
               1,1,1,0,1,1,1,1,1,1,1,1,1,1,1])
    switch = thumby.Sprite(15, 9, bitmap3, 50, 5)
    
    #-----------------------------
    
    # BITMAP: width: 20, height: 20
    bitmap4 = bytearray([3,253,2,250,250,250,250,250,250,250,250,250,250,250,250,250,250,2,253,3,
           0,255,0,255,255,255,255,255,255,255,255,255,255,255,255,255,255,0,255,0,
           12,11,4,5,5,5,5,5,5,5,5,5,5,5,5,5,5,4,11,12])
    iconbox = thumby.Sprite(20, 20, bitmap4, 25, 5)
    
    #-----------------------------
    
    # BITMAP: width: 14, height: 14
    bitmap5 = bytearray([255,255,199,195,241,249,249,121,57,17,131,199,255,255,
           63,63,63,63,63,63,36,36,62,63,63,63,63,63])
    questionmark = thumby.Sprite(14, 14, bitmap5, 28, 8)
    
    #-----------------------------
    
    # BITMAP: width: 14, height: 14
    bitmap13 = bytearray([255,255,255,255,255,1,125,125,1,255,255,255,255,255,
            63,63,63,63,63,51,45,45,51,63,63,63,63,63])
    exclamationmark = thumby.Sprite(14, 14, bitmap13, 28, 8)
    
    #-----------------------------
    
    # BITMAP: width: 14, height: 14
    bitmap6 = bytearray([255,7,251,125,205,205,253,253,205,205,125,251,7,255,
           63,56,55,46,44,41,43,43,41,44,46,55,56,63])
    smileyface = thumby.Sprite(14, 14, bitmap6, 28, 8)
    
    #-----------------------------
    
    # BITMAP: width: 14, height: 14
    bitmap11 = bytearray([255,7,251,253,205,205,253,253,205,205,253,251,7,255,
            63,56,55,45,45,45,45,45,45,45,45,55,56,63])
    nothingface = thumby.Sprite(14, 14, bitmap11, 28, 8)
    
    #-----------------------------
    
    # BITMAP: width: 14, height: 14
    bitmap12 = bytearray([255,7,251,253,205,77,125,125,77,205,253,251,7,255,
            63,48,47,41,44,46,47,47,46,44,41,47,48,63])
    sadface = thumby.Sprite(14, 14, bitmap12, 28, 8)
    
    #-----------------------------
    
    # BITMAP: width: 14, height: 14
    bitmap7 = bytearray([127,191,15,247,15,127,127,127,127,15,247,15,191,127,
           63,62,56,55,56,63,63,63,63,56,55,56,62,63])
    dumbbell = thumby.Sprite(14, 14, bitmap7, 28, 8)
    
    #-----------------------------
    
    # BITMAP: width: 14, height: 14
    bitmap8 = bytearray([255,255,255,207,211,221,110,134,66,161,211,235,243,255,
           63,15,23,43,53,58,61,62,63,63,63,63,63,63])
    toothbrush = thumby.Sprite(14, 14, bitmap8, 28, 8)
    
    #-----------------------------
    
    # BITMAP: width: 14, height: 14
    bitmap9 = bytearray([255,219,75,83,127,109,101,105,63,95,95,95,63,255,
           63,56,35,59,59,59,59,59,59,59,59,35,56,63])
    bedicon = thumby.Sprite(14, 14, bitmap9, 28, 8)
    #-----------------------------
    
    # BITMAP: width: 14, height: 14
    bitmap10 = bytearray([255,159,175,163,173,162,170,154,250,2,253,3,255,255,
           63,60,39,60,63,57,63,36,63,0,63,0,63,63])
    showericon = thumby.Sprite(14, 14, bitmap10, 28, 8)
    
    #-----------------------------
    
    
    #-----------------------------
    
    # BITMAP: width: 72, height: 20
    bitmap0 = bytearray([255,1,1,1,1,1,1,1,255,1,1,1,1,1,1,1,255,1,1,1,1,1,1,1,255,1,1,1,1,1,1,1,255,1,1,1,1,1,1,1,255,1,1,1,1,1,1,1,255,1,1,1,1,1,1,1,255,1,1,1,1,1,1,1,255,1,33,113,249,113,113,113,
           191,124,252,252,4,4,4,4,7,4,4,252,4,4,4,4,7,4,4,252,4,4,4,4,7,4,4,252,4,4,4,4,7,4,4,252,4,4,4,4,7,4,4,252,4,4,4,4,7,4,4,252,4,4,4,4,7,4,4,252,4,4,4,4,7,4,4,252,252,252,124,188,
           13,11,6,15,0,0,0,0,0,0,0,15,0,0,0,0,0,0,0,15,0,0,0,0,0,0,0,15,0,0,0,0,0,0,0,15,0,0,0,0,0,0,0,15,0,0,0,0,0,0,0,15,0,0,0,0,0,0,0,15,0,0,0,0,0,0,0,15,13,6,11,13])
    
    smallemptykeyboard = thumby.Sprite(72, 20, bitmap0, 0, 20)
    
    #-----------------------------
    
    # BITMAP: width: 6, height: 5
    bitmap00 = bytearray([27,17,0,17,17,17])
    blackarrow = thumby.Sprite(6, 5, bitmap00, 66, 23)
    
    #-----------------------------
    
    keymap1 = [["a","b","c","d","e","f","g","h","del"],
                ["i","j","k"," ","l","m","n","o","-1"]]
    keymap2 = [["A","B","C","D","E","F","G","H","del"],
                ["I","J","K"," ","L","M","N","O","-1"]]
    keymap3 = [["p","q","r","s","t","u","v","w","del"],
                ["x","y","z"," "," "," "," "," ","-1"]]
    keymap4 = [["P","Q","R","S","T","U","V","W","del"],
                ["X","Y","Z"," "," "," "," "," ","-1"]]
    keymap5 = [["1","2","3","4","5","6","7","8","del"],
                ["9","0","~"," ","-","=","[","]","-1"]]
    keymap6 = [["!","@","#","$","%","^","&","*","del"],
                ["(",")","`"," ","_","+","{","}","-1"]]
    keymap7 = [["|",":",'"'," ","<",">","?"," ","del"],
                ["\\",";","'"," ",",",".","/"," ","-1"]]
    
    whichkeymap = [keymap1,keymap2,keymap3,keymap4,keymap5,keymap6,keymap7]
    
    #-----------------------------
    
    icons_list_img = [ questionmark, exclamationmark, smileyface, nothingface, sadface, dumbbell, toothbrush, bedicon, showericon]
    
    selbox = [1,1]
    
    #-----------------------------
    
    thumby.display.setFPS(15)
    
    thumby.display.drawSprite(startscreen)
    thumby.display.update()
    time.sleep(3)
    
    def startapp():
        global i,x,w,number_of_elements,start,ls,ch
        while not (thumby.buttonA.pressed() and thumby.buttonL.pressed()):
            thumby.display.drawSprite(arrows)
            thumby.display.drawSprite(iconbox)
            thumby.display.drawSprite(icons_list_img[ic[i]])
            if (0 <= i <= number_of_elements-1):
                thumby.display.drawText(ls[i], x, 27, 0)
                thumby.display.drawText(str(i+1)+".", 3, 17, 0)
                if start != 25:
                    start += 1
                if (len(ls[i]) >= 12 and start == 25):
                    x -= 3
                if (x-40 < ((-1)*len(ls[i])*6 ) ):
                    x = 3
                    start = 0
            if ch[i]==1:
                thumby.display.drawFilledRectangle(6, 7, 3, 3, 0)
                thumby.display.drawLine(0, 30, 72, 30, 0)
            if thumby.buttonD.pressed() and thumby.buttonB.pressed() and eltoch==None:
                while thumby.buttonD.pressed() or thumby.buttonB.pressed():
                    pass
                thumby.display.drawSprite(trashbin)
                thumby.display.update()
                while True:
                    if thumby.buttonL.pressed():
                        while thumby.buttonL.pressed():
                            pass
                        del ls[i]
                        del ch[i]
                        del ic[i]
                        i=i-1
                        number_of_elements = len(ls)
                        break
                    if thumby.buttonR.pressed():
                        while thumby.buttonR.pressed():
                            pass
                        break
            if thumby.buttonD.pressed():
                i += 1
                x = 3
                start = 0
                while thumby.buttonD.pressed():
                    pass
            if thumby.buttonA.pressed() and thumby.buttonU.pressed():
                for h in range(len(ch)):
                    ch[h] = 0
                while thumby.buttonA.pressed() and thumby.buttonU.pressed():
                    pass
            if thumby.buttonB.pressed() and thumby.buttonL.pressed() and eltoch==None:
                while thumby.buttonB.pressed() or thumby.buttonL.pressed():
                    pass
                new()
            if thumby.buttonU.pressed() and thumby.buttonB.pressed() and eltoch==None:
                while thumby.buttonU.pressed() or thumby.buttonB.pressed():
                    pass
                if ch[i] == 0:
                    ch[i] = 1
                elif ch[i] == 1:
                    ch[i] = 0
            if thumby.buttonR.pressed() and thumby.buttonB.pressed():
                while thumby.buttonR.pressed() or thumby.buttonB.pressed():
                    pass 
                change()
            if eltoch != None:
                thumby.display.drawSprite(switch)
            if thumby.buttonU.pressed():
                i -= 1
                x = 3
                start = 0
                while thumby.buttonU.pressed():
                    pass
            if thumby.buttonL.pressed():
                ic[i] -= 1
                while thumby.buttonL.pressed():
                    pass
            if thumby.buttonR.pressed():
                ic[i] += 1
                while thumby.buttonR.pressed():
                    pass
            if i < 0:
                i = number_of_elements - 1
            if i > (number_of_elements - 1):
                i = 0
            if ic[i] < 0:
                ic[i] = len(icons_list_img) - 1
            if ic[i] >=  len(icons_list_img):
                ic[i] = 0
            thumby.display.update()
    
    def change():
        global eltoch,i,chtoch,ictoch
        if eltoch == None:
            eltoch = i
        else:
            eltochtext = ls[eltoch]
            chtoch = ch[eltoch]
            ictoch = ic[eltoch]
            ls[eltoch] = ls[i]
            ch[eltoch] = ch[i]
            ic[eltoch] = ic[i]
            ls[i] = eltochtext
            ch[i] = chtoch
            ic[i] = ictoch
            eltoch = None
    
    def checkoutofrange():
        global selbox
        if selbox[0] > 9:
            selbox[0] = 1
        if selbox[0] < 1:
            selbox[0] = 9
        if selbox[1] > 2:
            selbox[1] = 1
        if selbox[1] < 1:
            selbox[1] = 2
    
    def checknobox():
        global whichkeymap, selbox, l
        checkoutofrange()
        if whichkeymap[l][selbox[1]-1][selbox[0]-1]== "-1":
            return True
        else:
            return False
    
    def new():
        global newtext,ls,i,ch,xpos, received,number_of_elements,ic,l,selbox
        while True:
            thumby.display.fill(0)
            thumby.display.drawText("<New Target>", 0, 1, 1)
            thumby.display.drawFilledRectangle(0, 9, 72, 9, 1)
            thumby.display.drawText(str(newtext), xpos, 10, 0)
            thumby.display.drawSprite(smallemptykeyboard)
            if thumby.buttonA.justPressed():
                l += 1
            if l > 6:
                l = 0
            for j in range(len(keymap1)):
                for k in range(len(keymap1[j])):
                    if whichkeymap[l][j][k] != "-1" and whichkeymap[l][j][k] != "del":
                        thumby.display.drawText(str(whichkeymap[l][j][k]),2+(j-int(j/3))*3+k*8, 22+j*10,1)
            thumby.display.drawFilledRectangle(1+(selbox[1]-1)*3+(selbox[0]-1)*8, 21+(selbox[1]-1)*10, 7, 9, 1)
            if whichkeymap[l][selbox[1]-1][selbox[0]-1] == "del":
                thumby.display.drawSprite(blackarrow)
            else:
                thumby.display.drawText(str(whichkeymap[l][selbox[1]-1][selbox[0]-1]),2+(selbox[1]-1)*3+(selbox[0]-1)*8, 22+(selbox[1]-1)*10, 0)
            checkoutofrange()
            if thumby.buttonA.pressed() and thumby.buttonL.pressed():
                while thumby.buttonA.pressed() and thumby.buttonL.pressed():
                    pass
                break
            if thumby.buttonB.justPressed():
                if whichkeymap[l][selbox[1]-1][selbox[0]-1] == "del":
                    newtext = newtext[:-1]
                else:
                    newtext += whichkeymap[l][selbox[1]-1][selbox[0]-1]
            if thumby.buttonU.justPressed():
                selbox[1] -= 1
                while checknobox() == True:
                    selbox[1] -= 1
            if thumby.buttonL.justPressed():
                selbox[0] -= 1
                while checknobox() == True:
                    selbox[0] -= 1
            if thumby.buttonR.justPressed():
                selbox[0] += 1
                while checknobox() == True:
                    selbox[0] += 1
            if thumby.buttonD.justPressed():
                selbox[1] += 1
                while checknobox() == True:
                    selbox[1] += 1
            received = thumby.link.receive()
            if received != None:
                text1 = ujson.loads(received.decode())
                if text1 == "\\n":
                    newtext += "\n"
                elif text1 == "del":
                    newtext = newtext[:-1]
                else:
                    newtext += text1
            if len(newtext) > 8:
                xpos = 0-6*(len(newtext)-8)
            else:
                xpos = 3
            thumby.display.update()
        ls.insert(i+1, newtext)
        ch.insert(i+1, 0)
        ic.insert(i+1, 0)
        i = i+1
        xpos = 1
        number_of_elements = len(ls)
        newtext = ""
    
    startapp()
    
    # If we're done running, delete the old save and write the new data
    targetslist.close()
    os.remove("./Games/TarGoal/targetslist.json")
    targetslist = open("./Games/TarGoal/targetslist.json", "w")
    json.dump({"list":ls,"check":ch,"icon":ic}, targetslist)
    
    # Clean up
    targetslist.close()

except Exception as e:
    f = open("/crash.log", "w")
    f.write(str(e))
    f.close()