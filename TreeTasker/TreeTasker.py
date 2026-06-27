#TreeTasker v0.1
#by Nemo.the.fishboy

import thumby
import os
import gc
gc.collect()
import json
import time
import ujson
from sys import path
path.append("/Games/TreeTasker")
from thumbyGrayscale import display, Sprite

from machine import ADC

adc = ADC(26)
batlev = 0
procent = 0

display.setFPS(30)

# BITMAP: width: 72, height: 40
bitmap0 = bytearray([255,255,255,255,255,255,31,71,23,167,243,171,243,167,23,71,31,255,255,255,255,255,255,255,0,252,254,254,254,254,254,14,246,250,250,10,186,250,246,14,254,254,254,254,254,254,252,0,255,255,255,255,255,255,255,127,191,127,255,127,191,223,111,183,219,231,255,255,255,255,255,255,
           31,223,223,223,223,223,223,220,221,220,217,218,217,220,221,220,223,223,223,223,223,223,223,223,192,199,207,207,207,207,207,206,205,203,203,203,203,203,205,206,207,207,207,207,207,207,199,192,223,223,223,223,223,223,223,222,221,219,218,219,221,222,223,223,223,223,223,31,31,31,31,31,
           0,159,159,159,159,159,159,159,159,159,159,159,159,159,159,159,159,159,159,159,159,159,159,159,159,159,159,159,159,159,159,159,159,159,159,159,159,159,159,159,159,159,159,159,159,159,159,159,159,159,159,159,159,159,159,159,159,159,159,159,159,159,159,159,159,159,159,0,0,0,0,0,
           0,63,63,63,63,63,63,63,63,63,63,63,63,63,63,63,63,63,63,63,63,63,63,63,63,63,63,63,63,63,63,63,63,63,63,63,63,63,63,63,63,63,63,63,63,63,63,63,63,63,63,63,63,63,63,63,63,63,63,63,63,63,63,63,63,63,63,0,0,0,0,0,
           0,127,127,127,127,127,127,127,127,127,127,127,127,127,127,127,127,127,127,127,127,127,127,127,127,127,127,127,127,127,127,127,127,127,127,127,127,127,127,127,127,127,127,127,127,127,127,127,127,127,127,127,127,127,127,127,127,127,127,127,127,127,127,127,127,127,127,0,0,0,0,0])
bitmap0SHD = bytearray([255,3,1,1,1,1,225,249,249,249,253,253,253,249,249,249,225,1,1,1,1,1,3,255,255,3,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,3,255,255,3,1,1,1,1,1,129,193,129,1,129,193,225,241,121,61,25,1,1,1,1,3,255,
           31,24,16,16,16,16,16,19,19,19,23,23,23,19,19,19,16,16,16,16,16,16,24,31,31,24,16,16,16,16,16,16,16,16,16,16,16,16,16,16,16,16,16,16,16,16,24,31,31,24,16,16,16,16,16,17,19,23,23,23,19,17,16,16,16,16,16,16,16,16,16,31,
           0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,
           0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,
           0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0])
backgroundimg = Sprite( 72, 40,(bitmap0,bitmap0SHD), 0, 0)

# BITMAP: width: 13, height: 13
bitmap14 = bytearray([176,93,224,95,91,229,254,229,91,95,233,86,185,
           17,7,16,31,27,20,15,20,27,31,0,10,10])
bitmap14SHD = bytearray([64,224,240,224,228,254,255,254,228,224,240,224,64,
           0,0,1,0,4,15,31,15,4,0,1,0,0])
moveicon = Sprite( 13, 13,(bitmap14,bitmap14SHD), 5, 0)

# BITMAP: width: 5, height: 5
bitmap4 = bytearray([19,7,19,25,28])
ticksymbol = thumby.Sprite(5, 5, bitmap4, 0,0)

# BITMAP: width: 5, height: 5
bitmap5 = bytearray([0,14,14,14,0])
emptyboxsymbol = thumby.Sprite(5, 5, bitmap5, 0,0)

# BITMAP: width: 5, height: 5
bitmap6 = bytearray([14,21,27,21,14])
crosssymbol = thumby.Sprite(5, 5, bitmap6, 0,0)

# BITMAP: width: 5, height: 5
bitmap7 = bytearray([29,30,10,26,29])
questionsymbol = thumby.Sprite(5, 5, bitmap7, 0,0)

symbols = [emptyboxsymbol,ticksymbol,crosssymbol,questionsymbol]

# BITMAP: width: 72, height: 40
bitmap1 = bytearray([255,255,255,255,255,255,191,187,59,125,243,251,59,191,145,213,241,255,191,191,63,159,127,255,31,95,27,243,231,207,59,123,59,157,243,251,127,241,245,241,255,255,255,255,255,255,255,255,255,255,255,255,255,241,237,237,157,61,245,117,109,101,245,125,249,99,47,223,111,183,219,227,
           255,243,231,143,153,139,131,134,140,9,0,12,135,131,129,137,137,140,222,207,231,247,255,251,231,143,173,161,175,47,224,46,175,167,161,141,78,111,109,117,125,253,254,254,249,127,120,122,120,127,255,255,15,239,15,255,127,184,51,247,247,246,118,119,100,237,236,238,46,161,63,127,
           127,127,127,127,127,127,126,120,121,0,0,0,103,115,127,1,1,231,231,249,249,231,231,255,255,7,7,153,153,24,153,0,231,255,255,4,5,153,25,25,153,0,231,255,48,175,171,173,217,117,140,255,0,255,30,182,107,221,62,255,129,126,219,169,171,174,113,255,0,255,6,251,
           0,128,64,224,160,80,240,160,92,254,246,160,80,240,224,192,248,1,3,255,127,127,127,191,63,126,126,249,9,232,233,232,9,255,255,254,254,248,249,248,248,248,249,255,254,254,126,126,158,159,255,255,254,158,158,127,127,254,254,127,127,159,158,254,254,254,255,255,254,254,254,255,
           0,1,3,3,2,5,7,10,5,63,127,98,5,7,3,1,3,0,0,255,255,231,247,231,239,231,231,239,254,198,214,198,254,255,255,255,255,255,231,231,159,159,231,231,249,249,254,254,255,255,255,255,255,159,159,230,230,249,249,230,230,159,159,255,255,255,255,255,255,255,255,255])
startscreen = thumby.Sprite(72, 40, bitmap1, 0,0)

# BITMAP: width: 9, height: 7
bitmap8 = bytearray([0,62,34,34,34,34,54,28,0])
lowbatteryimg = thumby.Sprite(9, 7, bitmap8, 63,0)

# BITMAP: width: 3, height: 5
bitmap2 = bytearray([0,17,27])
leftarrow = thumby.Sprite(3,5,bitmap2,0,4)

# BITMAP: width: 3, height: 5
bitmap3 = bytearray([27,17,0])
rightarrow = thumby.Sprite(3,5,bitmap3,0,4)

# BITMAP: width: 5, height: 3
bitmap9 = bytearray([3,1,0,1,3])
uparrow = thumby.Sprite(5,3,bitmap9,3,3)

# BITMAP: width: 5, height: 3
bitmap10 = bytearray([6,4,0,4,6])
downarrow = thumby.Sprite(5,3,bitmap10,3,8)


# Keymaps for small keyboard

keymap1 = [["a","b","c","d","e","f","g","h","del"],
            ["left","right","i"," ","j","k","l","\\n","-1"]]
keymap2 = [["A","B","C","D","E","F","G","H","del"],
            ["left","right","I"," ","J","K","L","\\n","-1"]]
keymap3 = [["m","n","o","p","q","r","s","t","del"],
            ["left","right","u"," ","v","w","x","\\n","-1"]]
keymap4 = [["M","N","O","P","Q","R","S","T","del"],
            ["left","right","U"," ","V","W","X","\\n","-1"]]
keymap5 = [["y","z","1","2","3","4","5","6","del"],
            ["left","right","7"," ","8","9","0","\\n","-1"]]
keymap6 = [["Y","Z","!","@","#","$","%","^","del"],
            ["left","right","&"," ","*","(",")","\\n","-1"]]
keymap7 = [["~","`","-","_","+","=","{","}","del"],
            ["left","right","|"," ","\\","[","]","\\n","-1"]]
keymap8 = [[":",";",'"',"'"," ","<",">","?","del"],
            ["left","right"," "," ",",",".","/","\\n","-1"]]

whichkeymap = [keymap1,keymap2,keymap3,keymap4,keymap5,keymap6,keymap7,keymap8]

# BITMAP: width: 7, height: 9
bitmap12 = bytearray([255,239,199,131,1,255,255,
           1,1,1,1,1,1,1])
leftblackarrow = thumby.Sprite(7, 9, bitmap12, 4, 31)

# BITMAP: width: 7, height: 9
bitmap13 = bytearray([255,255,1,131,199,239,255,
           1,1,1,1,1,1,1])
rightblackarrow = thumby.Sprite(7, 9, bitmap13, 12, 31)

# BITMAP: width: 6, height: 5
bitmap000 = bytearray([27,17,0,17,17,17])
blackarrow0 = thumby.Sprite(6, 5, bitmap000, 66, 23)

#Enter arrow

# BITMAP: width: 6, height: 5
bitmap010 = bytearray([27,17,0,27,27,24])
blackenterarrow0 = thumby.Sprite(6, 5, bitmap010, 61, 33)

# BITMAP: width: 72, height: 20
bitmap11 = bytearray([255,1,1,1,1,1,1,1,255,1,1,1,1,1,1,1,255,1,1,1,1,1,1,1,255,1,1,1,1,1,1,1,255,1,1,1,1,1,1,1,255,1,1,1,1,1,1,1,255,1,1,1,1,1,1,1,255,1,1,1,1,1,1,1,255,1,33,113,249,113,113,113,
           191,124,252,252,4,132,196,228,247,4,4,252,4,4,244,228,199,132,4,252,4,4,4,4,7,4,4,252,4,4,4,4,7,4,4,252,4,4,4,4,7,4,4,252,4,4,4,4,7,4,4,252,4,4,4,4,7,4,4,252,4,132,196,228,135,132,228,252,252,252,124,188,
           13,11,6,15,0,0,1,3,7,0,0,15,0,0,7,3,1,0,0,15,0,0,0,0,0,0,0,15,0,0,0,0,0,0,0,15,0,0,0,0,0,0,0,15,0,0,0,0,0,0,0,15,0,0,0,0,0,0,0,15,0,0,1,3,0,0,0,15,13,6,11,13])
smallemptykeyboard1 = thumby.Sprite(72, 20, bitmap11, 0, 20)


global childtool, nicechildren, movabletask

movabletask = False

selbox = [1,1]

l = 0
j = 0
k = 0
i = 0


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


try:
    # If a saved file exists, try to open and read from it
    realdate = open("realdate.json", "r+") # 'r+' will throw an exception if the file does not exist

except OSError:
    print("savefile does not exist, creating...")
    realdate = open("realdate.json", "w+")                                 # 'w+' will create the file if it does not exist
    json.dump({"Day":1,"Month":1}, realdate) # Write default data to the save file
    realdate.seek(0, 0)

saveData=json.load(realdate)
month_set=saveData["Month"]
day_set=saveData["Day"]


global whereamI, x
whereamI = 0
x = 4
start = 0

try:
    # If a saved file exists, try to open and read from it
    taskslists = open("/Games/TreeTasker/taskslists.json", "r+") # 'r+' will throw an exception if the file does not exist

except OSError:
    print("savefile does not exist, creating...")
    taskslists = open("/Games/TreeTasker/taskslists.json", "w+")                                 # 'w+' will create the file if it does not exist
    json.dump({"dailylist":[[0,"Task 1 taskslists",0, True, True],[0,"Task 2 taskslists",0, True, True],[1,"Task 2 1 taskslists", 1, True, True],[1,"Task 2 2 taskslists",2, True, True],[0,"Task 3 taskslists",0, True, True]],"todolist":[[0,"Task 1 taskslists",0, True, True],[0,"Task 2 taskslists",0, True, True],[1,"Task 2 1 taskslists", 1, True, True],[1,"Task 2 2 taskslists",2, True, True],[0,"Task 3 taskslists",0, True, True]]}, taskslists) # Write default data to the save file
    taskslists.seek(0, 0)

saveData1=json.load(taskslists)
DailyList=saveData1["dailylist"]
ToDoList=saveData1["todolist"]

display.drawSprite(startscreen)
display.update()
time.sleep(3)
quitfull = True

list_months = ["Jan.","Febr.","March","April","May","June","July","Aug.","Sept.","Oct.","Nov.","Dec."]
maxdays = [31,28,31,30,31,30,31,31,30,31,30,31]

modes = [["newtask","New Task"],["newsubtask","New Subtask"],["rename","Rename"],["foldorunfold","(Un)Fold"],["delete","Delete"],["move","Move"]]

tabsellect = 2
tabs = True
Irow = 0
IIrow = 0
positionTask = 0

lists = [DailyList,ToDoList]

def frpass():
    while thumby.buttonA.pressed() or thumby.buttonB.pressed() or thumby.buttonL.pressed() or thumby.buttonR.pressed() or thumby.buttonD.pressed() or thumby.buttonU.pressed():
        pass

def nrpass():
    while not thumby.buttonA.pressed() and not thumby.buttonB.pressed() and not thumby.buttonU.pressed() and not thumby.buttonD.pressed() and not thumby.buttonL.pressed() and not thumby.buttonR.pressed():
        pass
try:
    def surequit():
        frpass()
        global quitfull
        display.fill(0)
        display.setFont("/lib/font5x7.bin", 5, 7, 1)
        display.drawText("Are you sure", 1 , 2, 1)
        display.drawText("you want to", 1 , 10, 1)
        display.drawText("exit?", 1 , 18, 1)
        display.drawText("B-Yes, A-No", 2 , 30, 1)
        display.update()
        while True:
            if thumby.buttonA.pressed():
                frpass()
                return 0
            if thumby.buttonB.pressed():
                quitfull = False
                frpass()
                return 0
    
    def firsttabaction():
        global Irow, tabs
        if Irow == 1:
            leftarrow.x = 2
            leftarrow.y = 16
            display.drawSprite(leftarrow)
            display.setFont("/lib/font3x5.bin", 3, 5, 1)
            display.drawText("EDIT? B-ok",15,24,0)
            if thumby.buttonB.pressed():
                editdate()
                updatedate()
        if Irow == 2:
            leftarrow.x = 2
            leftarrow.y = 31
            display.drawSprite(leftarrow)
            if thumby.buttonB.pressed():
                frpass()
                newday()
                updatedate()
        if Irow > 2:
            Irow = 2
        if Irow != 0:
            if thumby.buttonU.pressed():
                Irow -= 1
                frpass()
            if thumby.buttonD.pressed():
                Irow += 1
                frpass()
        elif Irow == 0:
            tabs = True
    
    def secondorthirdtabaction(dayortask):
        global IIrow, tabs, whereamI, positionTask, x, start, exactlist, whichlist, movabletask
        whichlist = dayortask
        lists[whichlist][0][0] = 0
        color = 0
        display.setFont("/lib/font3x5.bin", 3, 5, 1)
        exactlist = []
        for c in range(len(lists[whichlist])):
            if lists[whichlist][c][4] == True:
                exactlist.append(lists[whichlist][c])
                exactlist.append(c)
                
        helper = 0
        for i in range(3):
            try:
                while lists[whichlist][whereamI+i+helper][4] == False:
                    helper += 1
                if lists[whichlist][whereamI+i+helper][2] == 0:
                    color = 0
                elif lists[whichlist][whereamI+i+helper][2] == 1:
                    color = 3
                elif lists[whichlist][whereamI+i+helper][2] == 2:
                    color = 2
                else:
                    color = 2
                display.drawText(lists[whichlist][whereamI+i+helper][1], 6+int(lists[whichlist][whereamI+i+helper][0])*4, 15+9*i, color)
                symbols[lists[whichlist][whereamI+i+helper][2]].x = 61
                symbols[lists[whichlist][whereamI+i+helper][2]].y = 15+9*i
                display.drawRectangle(60, 14+9*i, 7, 7, 1)
                display.drawSprite(symbols[lists[whichlist][whereamI+i+helper][2]])
                childtool = 0
                nicechildren = 0
                while lists[whichlist][whereamI+i+helper+childtool+1][0] > lists[whichlist][whereamI+i+helper][0] and whereamI+i+helper+childtool+2 < len(lists[whichlist]):
                    if lists[whichlist][whereamI+i+helper+childtool+1][2] == 1:
                        nicechildren += 1
                    childtool += 1
                try:
                    if lists[whichlist][whereamI+i+helper+childtool+1][0] > lists[whichlist][whereamI+i+helper][0]:
                        if lists[whichlist][whereamI+i+helper+childtool+1][2] == 1:
                            nicechildren += 1
                        childtool += 1
                except:
                    pass
                if childtool >= 1 and lists[whichlist][whereamI+i+helper][3] == False:
                    display.drawFilledRectangle(57-len(str(nicechildren))*4-len(str(childtool))*4, 15+i*9, 4*(len(str(nicechildren))+len(str(childtool)))+3, 5, 3)
                    display.drawText(str(nicechildren)+"/"+str(childtool), 57-len(str(nicechildren))*4-len(str(childtool))*4 , 15+i*9 , 2)
            except:
                pass
        leftarrow.x = 2
        leftarrow.y = 15+(IIrow-1)*9
        if tabs == False:
            if lists[whichlist][exactlist[positionTask*2+1]][2] == 0:
                color = 0
            elif lists[whichlist][exactlist[positionTask*2+1]][2] == 1:
                color = 3
            elif lists[whichlist][exactlist[positionTask*2+1]][2] == 2:
                color = 2
            else:
                color = 2
            if start != 50:
                start += 1
            if (len(lists[whichlist][exactlist[positionTask*2+1]][1]) >= 12 and start == 50):
                x -= 2
            if (x-20 < ((-1)*len(lists[whichlist][exactlist[positionTask*2+1]][1])*4 ) ):
                x = 6+4*lists[whichlist][exactlist[positionTask*2+1]][0]
                start = 0
            symbols[lists[whichlist][exactlist[positionTask*2+1]][2]].x = 61
            symbols[lists[whichlist][exactlist[positionTask*2+1]][2]].y = 15+9*(IIrow-1)
            display.drawFilledRectangle(5+4*lists[whichlist][exactlist[positionTask*2+1]][0], 14+(IIrow-1)*9, 55, 7, 1)
            display.drawRectangle(60, 14+(IIrow-1)*9, 7, 7, 1)
            display.drawText(lists[whichlist][exactlist[positionTask*2+1]][1], x, 15+(IIrow-1)*9, color)
            childtool = 0
            nicechildren = 0
            try:
                while lists[whichlist][exactlist[positionTask*2+1]+childtool+1][0] > lists[whichlist][exactlist[positionTask*2+1]][0] and exactlist[positionTask*2+1]+childtool+2 < len(lists[whichlist]):
                    if lists[whichlist][exactlist[positionTask*2+1]+childtool+1][2] == 1:
                        nicechildren += 1
                    childtool += 1
                try:
                    if lists[whichlist][exactlist[positionTask*2+1]+childtool+1][0] > lists[whichlist][exactlist[positionTask*2+1]][0]:
                        if lists[whichlist][exactlist[positionTask*2+1]+childtool+1][2] == 1:
                            nicechildren += 1
                        childtool += 1
                except:
                    pass
            except:
                pass
            if childtool >= 1 and lists[whichlist][exactlist[positionTask*2+1]][3] == False:
                display.drawFilledRectangle(57-len(str(nicechildren))*4-len(str(childtool)*4), 15+(IIrow-1)*9, 4*(len(str(nicechildren))+len(str(childtool)))+3, 5, 3)
                display.drawText(str(nicechildren)+"/"+str(childtool), 57-len(str(nicechildren))*4-len(str(childtool)*4) , 15+(IIrow-1)*9 , 2)
            display.drawSprite(symbols[lists[whichlist][exactlist[positionTask*2+1]][2]])
        if tabs == False:
            display.drawSprite(leftarrow)
        if IIrow > 3:
            IIrow = 3
            
        if IIrow != 0:
            if thumby.buttonU.pressed():
                if movabletask == True and positionTask > 0:
                    thirdhand = lists[whichlist][exactlist[positionTask*2+1]]
                    forthhand = lists[whichlist][exactlist[positionTask*2+1]][3]
                    fifthhand = lists[whichlist][exactlist[(positionTask*2-2)+1]][3]
                    lists[whichlist][exactlist[positionTask*2+1]] = lists[whichlist][exactlist[(positionTask*2-2)+1]]
                    lists[whichlist][exactlist[(positionTask*2-2)+1]] = thirdhand
                    lists[whichlist][exactlist[positionTask*2+1]][3] = forthhand
                    lists[whichlist][exactlist[(positionTask*2-2)+1]][3] = fifthhand
                    
                if IIrow != 1:
                    IIrow -= 1
                    positionTask -= 1
                elif IIrow == 1 and whereamI+3 == 3 and movabletask == False:
                    IIrow -= 1
                elif IIrow == 1 and whereamI+3 != 3:
                    whereamI = exactlist[(positionTask-1)*2+1]
                    positionTask -= 1
                x = 6+4*lists[whichlist][exactlist[positionTask*2+1]][0]
                start = 0
            if thumby.buttonD.pressed():
                if movabletask == True and positionTask+1 < len(exactlist)/2:
                    thirdhand = lists[whichlist][exactlist[positionTask*2+1]]
                    forthhand = lists[whichlist][exactlist[positionTask*2+1]][3]
                    fifthhand = lists[whichlist][exactlist[(positionTask*2+2)+1]][3]
                    lists[whichlist][exactlist[positionTask*2+1]] = lists[whichlist][exactlist[(positionTask*2+2)+1]]
                    lists[whichlist][exactlist[(positionTask*2+2)+1]] = thirdhand
                    lists[whichlist][exactlist[positionTask*2+1]][3] = forthhand
                    lists[whichlist][exactlist[(positionTask*2+2)+1]][3] = fifthhand
                if IIrow == 3:
                    if positionTask+1 < len(exactlist)/2 :
                        whereamI = exactlist[(positionTask-1)*2+1]
                        positionTask += 1
                elif IIrow < 3 and IIrow < len(exactlist)/2 and positionTask < len(exactlist)/2-1:
                        IIrow += 1
                        positionTask += 1
                x = 6+4*lists[whichlist][exactlist[positionTask*2+1]][0]
                start = 0
            if thumby.buttonL.pressed() and movabletask == True:
                if lists[whichlist][exactlist[2*positionTask+1]][0] > 0:
                    lists[whichlist][exactlist[2*positionTask+1]][0] -= 1
                x = 6+4*lists[whichlist][exactlist[positionTask*2+1]][0]
            if thumby.buttonR.pressed() and movabletask == True:
                if lists[whichlist][exactlist[2*positionTask+1]][0] < 2:
                    lists[whichlist][exactlist[2*positionTask+1]][0] += 1
                x = 6+4*lists[whichlist][exactlist[positionTask*2+1]][0]
            if thumby.buttonB.pressed():
                lists[whichlist][exactlist[2*positionTask+1]][2] += 1
                if lists[whichlist][exactlist[2*positionTask+1]][2] > 3:
                    lists[whichlist][exactlist[2*positionTask+1]][2] = 0
                updatelists()
            if thumby.buttonA.pressed() and tabs == False:
                frpass()
                mode = selectfunction()
                if mode == False:
                    pass
                else:
                    function_to_call = globals()[mode]
                    function_to_call()
            frpass()
        elif IIrow == 0:
            tabs = True
        display.drawFilledRectangle(67, 13, 5, 30, 0)
        if len(exactlist)/2 > 3:
            display.drawFilledRectangle(69, 14+int(positionTask/3)*int(24/int((len(exactlist)/2-1)/3+1)), 2, int(24/int((len(exactlist)/2-1)/3+1))+1, 1)
        if movabletask == True:
            display.drawSprite(moveicon)
            
    def selectfunction():
        modenumber = 0
        while True:
            display.drawFilledRectangle(2,1,68,11,3)
            display.drawText(modes[modenumber][1]+"?",10,5,0)
            if modenumber > 0:
                display.drawSprite(uparrow)
            if modenumber < len(modes)-1:
                display.drawSprite(downarrow)
            display.update()
            if movabletask == True and modenumber != 5:
                modenumber = 5
            elif thumby.buttonU.pressed():
                modenumber -= 1
                if modenumber == 1 and lists[whichlist][exactlist[2*positionTask+1]][0] >= 2:
                    modenumber -= 1
            elif thumby.buttonD.pressed():
                modenumber += 1
                if modenumber == 1 and lists[whichlist][exactlist[2*positionTask+1]][0] >= 2:
                    modenumber += 1
            elif thumby.buttonA.pressed():
                return False
            elif thumby.buttonB.pressed():
                return modes[modenumber][0]
            if modenumber > len(modes)-1:
                modenumber -= 1
            if modenumber < 0:
                modenumber = 0
            frpass()
    
    def newtask():
        a = enterText("New Task:", "")
        if a == False:
            pass
        else:
            corpos = 1
            try:
                while lists[whichlist][exactlist[positionTask*2+1]+corpos][0] > lists[whichlist][exactlist[positionTask*2+1]][0]:
                    corpos += 1
            except:
                pass
            lists[whichlist].insert(exactlist[positionTask*2+1]+corpos, [lists[whichlist][exactlist[positionTask*2+1]][0],a,0,True,True])
        updatelists()
    
    def newsubtask():
        a = enterText("New Subtask:", "")
        if a == False:
            pass
        else:
            corpos = 1
            lists[whichlist].insert(exactlist[positionTask*2+1]+corpos, [lists[whichlist][exactlist[positionTask*2+1]][0]+1,a,0,True,lists[whichlist][exactlist[positionTask*2+1]][3]])
        updatelists()
    
    def rename():
        a = enterText("Rename:", str(lists[whichlist][exactlist[positionTask*2+1]][1]))
        if a == False:
            pass
        else:
            lists[whichlist][exactlist[positionTask*2+1]][1] = a
        updatelists()
    
        
    def foldorunfold():
        notthere = False
        childtool = 0
        leveltask = 0
        try:
            if lists[whichlist][exactlist[positionTask*2+1]][0] < lists[whichlist][exactlist[positionTask*2+1]+1][0]:
                if lists[whichlist][exactlist[positionTask*2+1]][3] == True:
                    lists[whichlist][exactlist[positionTask*2+1]][3] = False
                    while lists[whichlist][exactlist[positionTask*2+1]+childtool+1][0] > lists[whichlist][exactlist[positionTask*2+1]][0] and exactlist[positionTask*2+1]+childtool+2 < len(lists[whichlist]):
                        # if lists[whichlist][exactlist[positionTask*2+1]+childtool+1][3] == False:
                        #     notthere = True
                        lists[whichlist][exactlist[positionTask*2+1]+childtool+1][4] = False
                        childtool += 1
                    try:
                        if lists[whichlist][exactlist[positionTask*2+1]+childtool+1][0] > lists[whichlist][exactlist[positionTask*2+1]][0] and exactlist[positionTask*2+1]+childtool+2 <= len(lists[whichlist]):
                            lists[whichlist][exactlist[positionTask*2+1]+childtool+1][4] = False
                        childtool += 1
                    except:
                        pass
                elif lists[whichlist][exactlist[positionTask*2+1]][3] == False:
                    lists[whichlist][exactlist[positionTask*2+1]][3] = True
                    while lists[whichlist][exactlist[positionTask*2+1]+childtool+1][0] > lists[whichlist][exactlist[positionTask*2+1]][0] and exactlist[positionTask*2+1]+childtool+2 < len(lists[whichlist]):
                        if lists[whichlist][exactlist[positionTask*2+1]+childtool+1][3] == False:
                            leveltask = lists[whichlist][exactlist[positionTask*2+1]+childtool+1][0]
                            lists[whichlist][exactlist[positionTask*2+1]+childtool+1][4] = True
                            notthere = True
                        elif lists[whichlist][exactlist[positionTask*2+1]+childtool+1][3] == True and leveltask == lists[whichlist][exactlist[positionTask*2+1]+childtool+1][0]:
                            notthere = False
                        if notthere == False:
                            lists[whichlist][exactlist[positionTask*2+1]+childtool+1][4] = True
                        childtool += 1
                    try:
                        if notthere == False and lists[whichlist][exactlist[positionTask*2+1]+childtool+1][0] > lists[whichlist][exactlist[positionTask*2+1]][0] and exactlist[positionTask*2+1]+childtool+2 <= len(lists[whichlist]):
                            lists[whichlist][exactlist[positionTask*2+1]+childtool+1][4] = True
                        childtool += 1
                    except:
                        pass
        except:
            pass
        updatelists()
    
    
    def delete():
        global positionTask, whereamI, IIrow
        if len(lists[whichlist]) > 1:
            if lists[whichlist][exactlist[positionTask*2+1]][3] == False:
                foldorunfold()
            del lists[whichlist][exactlist[positionTask*2+1]]
            if IIrow == 1 and exactlist[positionTask*2-1] == 0:
                pass
            elif IIrow == 3 and positionTask+1 == len(exactlist)/2 and len(exactlist)/2 > 3:
                if len(exactlist)/2 > 3:
                    whereamI -= exactlist[(positionTask-1)*2+1]
                positionTask -= 1
            elif len(exactlist)/2 <= 3:
                positionTask -= 1
                IIrow -= 1
        updatelists()
        
    
    def move():
        global movabletask
        if movabletask == True:
            movabletask = False
        elif movabletask == False:
            movabletask = True
    
    def newday():
        global day_set, maxdays, month_set
        day_set += 1
        if day_set > maxdays[month_set-1]:
            day_set = 1
            month_set += 1
        if month_set > 12:
            month_set = 1
        for i in range(len(DailyList)):
            DailyList[i][2] = 0
        updatedate()
        updatelists()
    
    editfinish=False
    monorday=1
    oldday_set = 1
    oldmonth_set = 1
    oldchanges = True
    
    def editdate():
        frpass()
        global editfinish, monorday, day_set, month_set, maxdays, oldday_set, oldmonth_set, oldchanges
        editfinish = False
        oldchanges = False
        oldday_set=day_set
        oldmonth_set=month_set
        while editfinish == False:
            display.fill(1)
            display.setFont("/lib/font5x7.bin", 5, 7, 1)
            display.drawText("EDIT MODE",10,5,0)
            display.drawText(list_months[month_set-1],7,15,0)
            display.drawText(str(day_set),56,15,0)
            if monorday == 1:
                leftarrow.x = 2
                leftarrow.y = 16
                display.drawSprite(leftarrow)
                if thumby.buttonD.pressed():
                    month_set += 1
                    frpass()
                if thumby.buttonU.pressed():
                    month_set -= 1
                    frpass()
            if monorday == 2:
                leftarrow.x = 51
                leftarrow.y = 16
                display.drawSprite(leftarrow)
                if thumby.buttonD.pressed():
                    day_set += 1
                    frpass()
                if thumby.buttonU.pressed():
                    day_set -= 1
                    frpass()
            if month_set < 1:
                month_set = 12
            if day_set < 1:
                day_set = maxdays[month_set-1]
            if month_set > 12:
                month_set = 1
            if day_set < 1:
                day_set = maxdays[month_set-1]
            if day_set > maxdays[month_set-1]:
                day_set = 1
            if thumby.buttonL.pressed():
                monorday = 1
            if thumby.buttonR.pressed():
                monorday = 2
            if thumby.buttonA.pressed():
                canceledit()
            if thumby.buttonB.pressed():
                doedit()
            if oldchanges == True:
                day_set = oldday_set
                month_set = oldmonth_set
            display.update()
    
    
    
    def doedit():
        frpass()
        global editfinish
        display.fill(0)
        display.setFont("/lib/font5x7.bin", 5, 7, 1)
        display.drawText("Do you want", 1 , 2, 1)
        display.drawText("save the", 1 , 10, 1)
        display.drawText("edit?", 1 , 18, 1)
        display.drawText("B-Yes, A-No", 2 , 30, 1)
        display.update()
        while True:
            if thumby.buttonA.pressed():
                frpass()
                return 0
            if thumby.buttonB.pressed():
                editfinish = True
                frpass()
                return 0
    
    def canceledit():
        frpass()
        global editfinish, oldchanges
        display.fill(0)
        display.setFont("/lib/font5x7.bin", 5, 7, 1)
        display.drawText("Do you want", 1 , 2, 1)
        display.drawText("to cancel", 1 , 10, 1)
        display.drawText("the edit?", 1 , 18, 1)
        display.drawText("B-Yes, A-No", 2 , 30, 1)
        display.update()
        while True:
            if thumby.buttonA.pressed():
                frpass()
                return 0
            if thumby.buttonB.pressed():
                editfinish = True
                oldchanges = True
                frpass()
                return 0
    
    tick = 0
    blink = 1
    
    
    def enterText(title,texttask):
        nrpass()
        display.disableGrayscale()
        global newtext,received,l,selbox,typedText
        newtext = texttask
        linely = 0
        index_to_add = len(texttask)-1
        if index_to_add == -1:
            index_to_add = 0
        selbox[0] = 1
        selbox[1] = 1
        while True:
            frpass()
            display.fill(0)
            if len(title) > 12:
                    display.setFont("/lib/font3x5.bin", 3, 5, 1)
            display.drawText(str(title), 1, 1, 1)
            display.setFont("/lib/font5x7.bin", 5, 7, 1)
            display.drawFilledRectangle(0, 9, 72, 9, 1)
            display.drawText(str(newtext), 31-index_to_add*6, 10, 0)
            display.drawSprite(smallemptykeyboard1)
            if linely < 30:
                display.drawLine(36, 9, 36, 18, 0)
            linely += 1
            if linely > 60:
                linely = 0
            if thumby.buttonA.justPressed():
                l += 1
            if l > len(whichkeymap)-1:
                l = 0
            for j in range(len(keymap1)):
                for k in range(len(keymap1[j])):
                    if whichkeymap[l][j][k] != "-1" and whichkeymap[l][j][k] != "del" and whichkeymap[l][j][k] != "\\n" and whichkeymap[l][j][k] != "left" and whichkeymap[l][j][k] != "right":
                        display.drawText(str(whichkeymap[l][j][k]),2+(j-int(j/3))*3+k*8, 22+j*10, 1)
            display.drawFilledRectangle(1+(selbox[1]-1)*3+(selbox[0]-1)*8, 21+(selbox[1]-1)*10, 7, 9, 1)
            if whichkeymap[l][selbox[1]-1][selbox[0]-1] == "del":
                display.drawSprite(blackarrow0)
            elif whichkeymap[l][selbox[1]-1][selbox[0]-1] == "\\n":
                display.drawSprite(blackenterarrow0)
            elif whichkeymap[l][selbox[1]-1][selbox[0]-1] == "left":
                display.drawSprite(leftblackarrow)
            elif whichkeymap[l][selbox[1]-1][selbox[0]-1] == "right":
                display.drawSprite(rightblackarrow)
            else:
                display.drawText(str(whichkeymap[l][selbox[1]-1][selbox[0]-1]),2+(selbox[1]-1)*3+(selbox[0]-1)*8, 22+(selbox[1]-1)*10, 0)
            checkoutofrange()
            if (thumby.buttonA.pressed() and thumby.buttonL.pressed())or(whichkeymap[l][selbox[1]-1][selbox[0]-1] == "del" and thumby.buttonB.pressed() and len(newtext) == 0):
                display.enableGrayscale()
                return False
            if thumby.buttonB.pressed() and whichkeymap[l][selbox[1]-1][selbox[0]-1] == "\\n":
                display.enableGrayscale()
                return newtext
            if thumby.buttonB.justPressed():
                if whichkeymap[l][selbox[1]-1][selbox[0]-1] == "del":
                    newtext = newtext[:index_to_add] + newtext[index_to_add+1:]
                    if index_to_add > 0:
                        index_to_add -= 1
                elif whichkeymap[l][selbox[1]-1][selbox[0]-1] == "left":
                    if index_to_add > 0:
                        index_to_add -= 1
                elif whichkeymap[l][selbox[1]-1][selbox[0]-1] == "right":
                    if index_to_add < len(newtext)-1:
                        index_to_add += 1
                else:
                    try:
                        newtext = newtext[:index_to_add] + newtext[index_to_add] + whichkeymap[l][selbox[1]-1][selbox[0]-1] + newtext[index_to_add+1:]
                        index_to_add += 1
                    except:
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
                    display.enableGrayscale()
                    return newtext
                elif text1 == "del":
                    newtext = newtext[:-1]
                else:
                    newtext += text1
            display.update()
    
    
    def batteryallert():
        global tick, blink, batlev, procent
        tick += 1
        if tick > 30:
            tick = 0
            blink = blink*(-1)
            procent = int((batlev-32000)/60)
        if blink == 1:
                display.setFont("/lib/font3x5.bin", 3, 5, 1)
                display.drawSprite(lowbatteryimg)
                display.drawFilledRectangle(50, 0, 13, 7, 0)
                display.drawText(str(procent), 51, 1, 1)
                display.drawText("%", 60, 1, 1)
    
    def updatedate():
        global realdate
        os.remove("realdate.json")
        realdate = open("realdate.json", "w")
        json.dump({"Day":day_set,"Month":month_set}, realdate)
        realdate.close()
    
    def updatelists():
        global taskslists
        os.remove("/Games/TreeTasker/taskslists.json")
        taskslists = open("/Games/TreeTasker/taskslists.json", "w")
        json.dump({"dailylist":DailyList,"todolist":ToDoList}, taskslists)
        taskslists.close()
        
    while quitfull:
        batlev = adc.read_u16()
        display.drawSprite(backgroundimg)
        rightarrow.x = 19 + (tabsellect-1)*24
        leftarrow.x = 2 + (tabsellect-1)*24
        display.drawSprite(rightarrow)
        if tabs == True:
            leftarrow.y = 4
            display.drawSprite(leftarrow)
        if thumby.buttonA.pressed() and tabs == True:
            surequit()
        if tabsellect > 1 and tabs == True and thumby.buttonL.pressed():
            tabsellect -= 1
            frpass()
        elif tabsellect < 3 and tabs == True and thumby.buttonR.pressed():
            tabsellect += 1
            frpass()
        if tabsellect == 1 and tabs == True and thumby.buttonD.pressed():
            tabs = False
            Irow = 1
            frpass()
            positionTask = 0
        if tabsellect == 2 and tabs == True and thumby.buttonD.pressed():
            tabs = False
            IIrow = 1
            frpass()
            positionTask = 0
        if tabsellect == 3 and tabs == True and thumby.buttonD.pressed():
            tabs = False
            IIrow = 1
            frpass()
            positionTask = 0
        if tabsellect == 1:
            display.drawFilledRectangle(1, 14, 70, 25, 1)
            display.setFont("/lib/font5x7.bin", 5, 7, 1)
            display.drawText(list_months[month_set-1],7,15,0)
            display.drawText(str(day_set),56,15,0)
            display.drawText("[New day?]",7,30,0)
            firsttabaction()
        if tabsellect == 2:
            secondorthirdtabaction(0)
        if tabsellect == 3:
            secondorthirdtabaction(1)
        if batlev < 33700:
            batteryallert()
        display.update()
    
    updatedate()
    updatelists()
    
    # Clean up
    realdate.close()
    taskslists.close()

except Exception as e:
    f = open("/crash.log", "w")
    f.write(str(e))
    f.close()