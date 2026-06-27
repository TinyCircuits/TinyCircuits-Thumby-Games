#Keyboard v0.2
#by Nemo.the.fishboy

import thumby
import time
import ujson

# BITMAP: width: 72, height: 40
bitmap0 = bytearray([255,255,255,255,3,171,3,63,143,35,139,227,255,255,63,143,35,139,35,171,35,139,35,143,255,255,63,191,63,255,255,255,63,191,63,255,225,237,13,97,109,13,97,109,13,97,109,13,97,109,13,97,109,13,97,109,13,97,109,13,97,109,13,97,109,13,97,109,13,97,127,255,
           255,255,255,255,96,170,96,254,120,162,40,99,255,255,248,226,232,226,234,226,234,226,234,227,255,255,224,234,96,107,99,107,0,170,0,255,255,255,255,192,219,219,192,219,219,192,219,219,192,219,219,192,219,219,192,219,219,192,219,219,192,219,219,192,219,219,192,219,202,192,192,255,
           127,63,31,96,127,125,126,126,127,125,118,91,108,53,67,127,127,255,255,255,255,255,1,85,1,175,143,175,12,93,28,125,252,254,6,87,7,215,7,87,7,255,127,31,81,21,81,5,81,7,255,255,7,87,7,175,135,215,199,255,255,127,31,95,15,175,143,175,1,85,1,255,
           0,128,64,224,160,80,240,160,92,254,246,160,80,240,224,192,248,0,1,255,255,255,240,245,112,186,176,181,177,116,241,252,255,255,240,245,240,245,240,245,240,255,60,241,244,241,245,240,245,240,255,255,240,53,240,255,255,255,255,255,255,252,241,116,241,245,240,250,240,245,240,255,
           0,1,3,3,2,5,7,10,5,63,127,98,5,7,3,1,3,0,0,255,255,255,241,238,223,161,186,186,161,223,238,241,255,255,251,251,224,251,251,255,243,231,192,231,243,255,255,251,251,251,251,255,255,192,253,253,195,255,227,213,213,219,255,192,255,1,237,237,243,255,255,255])
startscreen = thumby.Sprite(72, 40, bitmap0, 0,0)

keymap1 = [["1","2","3","4","5","6","7","8","9","0","-"],
          ["q","w","e","r","t","y","u","i","o","p","-1"],
          ["a","s","d","f","g","h","j","k","l","del","-1"],
          ["z","x","c","v"," ","b","n","m","=","\\n","-1"]]

keymap2 = [["!","@","#","$","%","^","&","*","(",")","_"],
          ["Q","W","E","R","T","Y","U","I","O","P","-1"],
          ["A","S","D","F","G","H","J","K","L","del","-1"],
          ["Z","X","C","V"," ","B","N","M","+","\\n","-1"]]

keymap3 = [["~","{","}","|",":",'"',"<",">","?"," "," "],
          ["`","[","]","\\",";","'",",",".","/"," ","-1"],
          ["_","+"," "," "," "," "," "," "," ","del","-1"],
          ["-","="," "," "," "," "," "," "," ","\\n","-1"]]

thumby.display.setFPS(30)

# BITMAP: width: 72, height: 40
keymap = bytearray([255,1,241,17,17,17,17,17,241,17,17,17,17,17,241,17,17,17,17,17,241,17,17,17,17,17,241,17,17,17,17,17,241,17,17,17,17,17,241,17,17,17,17,17,241,17,17,17,17,17,241,17,17,17,17,17,241,17,17,17,17,17,241,17,17,17,17,17,241,1,1,255,
           255,0,31,16,16,240,16,16,31,16,16,240,16,16,31,16,16,240,16,16,31,16,16,240,16,16,31,16,16,240,16,16,31,16,16,240,16,16,31,16,16,240,16,16,31,16,16,240,16,16,31,16,16,240,16,16,31,16,16,240,16,16,31,16,16,240,16,16,31,0,0,255,
           255,0,0,0,0,31,16,16,240,16,16,31,16,16,240,16,16,31,16,16,240,16,16,31,16,16,240,16,16,31,16,16,240,16,16,31,16,16,240,16,16,31,16,16,240,16,16,31,16,16,240,16,16,31,16,16,240,16,16,31,16,16,240,16,16,159,208,16,16,16,16,255,
           255,0,0,0,0,0,0,0,255,16,16,16,16,16,255,16,16,16,16,16,255,16,16,16,16,16,255,16,16,16,16,16,255,16,16,16,16,16,255,16,16,16,16,16,255,16,16,16,16,16,255,16,16,16,16,16,255,16,16,16,16,16,255,16,17,147,215,17,17,209,16,255,
           255,128,128,128,128,128,128,128,159,144,144,144,144,144,159,144,144,144,144,144,159,144,144,144,144,144,159,144,144,144,144,144,159,144,144,144,144,144,159,144,144,144,144,144,159,144,144,144,144,144,159,144,144,144,144,144,159,144,144,144,144,144,159,144,145,147,151,145,145,145,144,255])
keyboardimg = thumby.Sprite(72, 40, keymap, 0,0)

# BITMAP: width: 16, height: 26
magnifyingglass = bytearray([252,254,7,3,3,3,243,11,11,11,11,243,3,7,254,252,
           255,255,0,12,14,7,3,1,1,1,5,14,4,0,255,255,
           255,255,128,0,0,0,0,0,0,0,0,0,0,128,255,255,
           0,1,3,3,3,3,3,3,3,3,3,3,3,3,1,0])
zoomwindow = thumby.Sprite(16, 26, magnifyingglass, 4,7)

# BITMAP: width: 72, height: 40
buttonsmap = bytearray([0,0,0,0,0,0,0,0,0,0,0,0,0,224,32,32,32,32,160,32,32,32,32,224,0,0,248,112,192,112,248,0,144,136,152,240,0,0,192,64,192,128,0,0,0,126,80,112,0,112,64,112,4,126,4,0,4,126,4,112,80,112,0,112,16,96,0,184,232,0,80,0,
           0,0,0,0,0,0,0,0,0,0,0,0,0,255,0,4,2,1,0,1,2,4,0,255,0,0,3,0,1,0,3,0,3,2,3,1,2,0,7,1,1,0,0,0,0,0,0,0,0,0,0,0,0,192,224,16,8,196,230,54,22,22,54,230,196,8,16,224,192,0,0,0,
           0,0,255,1,33,81,137,5,1,1,1,1,1,1,0,0,0,0,0,0,0,0,0,1,1,1,1,1,1,5,137,81,33,1,255,0,0,0,0,0,128,64,96,96,96,96,96,96,64,128,0,0,0,15,31,32,64,159,191,135,134,134,135,191,159,64,32,31,15,0,0,0,
           0,0,7,4,4,4,4,5,4,4,4,4,4,252,0,0,0,0,0,0,0,0,0,252,4,4,4,4,4,5,4,4,4,4,7,0,0,252,254,1,0,0,255,255,51,51,63,238,192,0,1,254,252,0,0,0,0,0,1,1,1,1,1,1,0,0,0,0,0,0,0,0,
           0,0,0,0,0,0,0,0,0,0,0,0,0,63,32,33,34,36,40,36,34,33,32,63,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,2,4,8,27,27,26,26,27,27,9,4,2,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0])
buttonsmapimg = thumby.Sprite(72, 40, buttonsmap, 0,0)

# BITMAP: width: 7, height: 9
selboxbars = bytearray([131,255,254,254,254,255,131,
           1,1,0,0,0,1,1])

whichkeymap = [keymap1,keymap2,keymap3]
i = 0
j = 0
k = 0
zoom = -1
selbox = [1,1]
showzoomedletter = False

def frpass():
    while thumby.buttonA.pressed() or thumby.buttonB.pressed() or thumby.buttonL.pressed() or thumby.buttonR.pressed() or thumby.buttonD.pressed() or thumby.buttonU.pressed():
        pass

def checkoutofrange():
    global selbox
    if selbox[0] > 11:
        selbox[0] = 1
    if selbox[0] < 1:
        selbox[0] = 11
    if selbox[1] > 4:
        selbox[1] = 1
    if selbox[1] < 1:
        selbox[1] = 4

def checknobox():
    global whichkeymap, selbox, i
    checkoutofrange()
    if whichkeymap[i][selbox[1]-1][selbox[0]-1]== "-1":
        return True
    else:
        return False

noquit = True

def manual():
    frpass()
    thumby.display.drawSprite(buttonsmapimg)
    thumby.display.update()
    while not thumby.buttonA.pressed() and not thumby.buttonB.pressed() and not thumby.buttonL.pressed() and not thumby.buttonR.pressed() and not thumby.buttonD.pressed() and not thumby.buttonU.pressed():
        pass
    frpass()
    thumby.display.fill(0)
    thumby.display.setFont("/lib/font5x7.bin", 5, 7, 1)
    thumby.display.drawText("Help/Instr.", 3, 1, 1)
    thumby.display.drawText("^,v,<,>-nav.", 3, 11, 1)
    thumby.display.drawText("B-send char.", 3, 21, 1)
    thumby.display.drawText("A-ch. keyb.", 3, 31, 1)
    thumby.display.update()
    while not thumby.buttonA.pressed() and not thumby.buttonB.pressed() and not thumby.buttonL.pressed() and not thumby.buttonR.pressed() and not thumby.buttonD.pressed() and not thumby.buttonU.pressed():
        pass
    frpass()
    thumby.display.fill(0)
    thumby.display.drawText("Help/Instr.", 3, 1, 1)
    thumby.display.drawText("A+^ - Zoom", 3, 11, 1)
    thumby.display.drawText("A+< - Quit", 3, 21, 1)
    thumby.display.drawText("A+v - Help", 3, 31, 1)
    thumby.display.update()
    while not thumby.buttonA.pressed() and not thumby.buttonB.pressed() and not thumby.buttonL.pressed() and not thumby.buttonR.pressed() and not thumby.buttonD.pressed() and not thumby.buttonU.pressed():
        pass

def zoomch():
    global selbox,zoomwindow
    if selbox[0] < 6:
        zoomwindow.x = 52
    if selbox[0] > 5:
        zoomwindow.x = 4

thumby.display.drawSprite(startscreen)
thumby.display.update()
time.sleep(3)

while noquit:
    thumby.display.fill(0)
    thumby.display.drawSprite(keyboardimg)
    if thumby.buttonA.justPressed():
        i += 1
    if i > 2:
        i = 0
    thumby.display.setFont("/lib/font3x5.bin", 3, 5, 1)
    for j in range(len(keymap1)):
        for k in range(len(keymap1[j])):
            if whichkeymap[i][j][k] != "-1" and whichkeymap[i][j][k] != "\\n" and whichkeymap[i][j][k] != "del":
                thumby.display.drawText(str(whichkeymap[i][j][k]),4+(j-int(j/3))*3+k*6,6+j*8,1)
    checkoutofrange()
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
    if thumby.buttonB.justPressed():
        thumby.link.send(ujson.dumps('').encode())
        thumby.link.send(ujson.dumps(whichkeymap[i][selbox[1]-1][selbox[0]-1]).encode())
    thumby.display.blit(selboxbars, 2+((selbox[1]-1)-int((selbox[1]-1)/3))*3+(selbox[0]-1)*6, 4+(selbox[1]-1)*8, 7, 9, 1, 0, 0)
    if thumby.buttonA.pressed() and thumby.buttonL.pressed():
        noquit = False
    if thumby.buttonA.pressed() and thumby.buttonU.pressed():
        zoom = zoom*(-1)
        while thumby.buttonA.pressed() and thumby.buttonU.pressed():
            pass
    if zoom == 1:
        zoomch()
        thumby.display.drawSprite(zoomwindow)
        thumby.display.setFont("/lib/font8x8.bin", 8, 8, 1)
        thumby.display.drawText(str(whichkeymap[i][selbox[1]-1][selbox[0]-1]),zoomwindow.x+4,zoomwindow.y+14,1)
    if thumby.buttonA.pressed() and thumby.buttonD.pressed():
        manual()
        frpass()
    thumby.display.update()
thumby.display.setFont("/lib/font5x7.bin", 5, 7, 1)