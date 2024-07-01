import thumby
from math import sqrt
import time

# Define the logo, numbers, and general UI

# BITMAP: width: 22, height: 17
microsqrtcalc_logo = bytearray([255,35,189,243,61,163,63,237,225,45,191,33,237,191,161,53,169,191,225,109,225,255,
           255,13,108,111,252,29,172,171,31,252,14,125,127,255,15,108,111,255,221,127,128,255,
           1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1])        
# BITMAP: width: 7, height: 9
selected = bytearray([255,1,1,1,1,1,255,1,1,1,1,1,1,1])

# BITMAP: width: 60, height: 40
BBfiChe_logo = bytearray([0,254,254,6,250,250,250,6,250,250,250,6,254,250,250,2,250,250,254,2,250,250,250,254,2,234,234,18,254,2,250,250,250,250,250,2,254,254,254,254,2,254,254,194,190,190,194,254,254,2,254,2,186,186,186,186,186,70,254,0,
           0,255,255,252,255,255,135,180,183,183,183,52,255,253,5,244,245,245,247,4,253,253,5,183,180,183,71,252,255,244,245,245,5,245,245,244,255,255,255,255,0,255,255,255,185,128,191,255,255,0,255,8,107,107,107,107,107,108,255,0,
           0,255,255,255,255,255,13,237,237,237,237,252,31,111,108,109,29,253,253,12,251,255,252,255,255,15,236,239,239,239,239,255,252,255,255,255,255,255,255,255,0,255,255,255,7,116,4,255,255,0,255,232,235,235,11,235,235,235,255,0,
           0,255,95,95,223,223,80,215,87,215,87,223,80,95,223,223,80,95,223,208,87,87,87,215,95,80,87,215,87,87,87,223,95,223,95,223,95,95,95,255,0,223,239,239,15,249,9,239,15,0,255,31,111,111,104,111,111,31,255,0,
           0,127,64,91,100,127,124,67,124,127,68,127,64,91,100,127,64,91,100,127,64,125,127,127,95,64,95,127,64,95,95,127,64,123,64,127,64,91,91,127,64,123,121,122,122,127,120,123,120,64,127,112,127,127,127,127,127,112,127,0])
# BITMAP: width: 15, height: 9
sel_side = bytearray([255,1,1,1,1,1,1,1,1,1,1,1,1,1,255,
           1,1,1,1,1,1,1,1,1,1,1,1,1,1,1])

thumby.display.setFont("/lib/font3x5.bin", 3, 5, 1)
selx = 0
sely = 0
result = []
output = []
outpt_sv = 0
sel_area = 1
sels_x = 33
sels_y = 23
num = 0
dec_chk = False
exit = True
time_intro = 3
#Function to check which box is checked:
def appendnum(num):
    global selx, sely, result
    val = ''.join(map(str, result))
    result.clear()
    result.append(int(val+ str(num)))

def xyplacmntchk():
    global selx, sely, result, num, time_intro
    if selx == 0 and sely == 0:
        appendnum(1)
    elif selx == 8 and sely == 0:
        appendnum(2)
    elif selx == 16 and sely == 0:
        appendnum(3)
    elif selx == 24 and sely == 0:
        appendnum(4)
    elif selx == 32 and sely == 0:
        appendnum(5)
    elif selx == 40 and sely == 0:
        if result == []:
            pass
        else:
            result.pop()
        time.sleep(0.2)
    # BOTTOM ROW CHECK
    elif selx == 0 and sely == 8:
        appendnum(6)
    elif selx == 8 and sely == 8:
        appendnum(7)
    elif selx == 16 and sely == 8:
        appendnum(8)
    elif selx == 24 and sely == 8:
        appendnum(9)
    elif selx == 32 and sely == 8:
        appendnum(0)
    elif selx == 40 and sely == 8:
        time_intro = 2
        intro()
    else:
        pass
def intro():   
    global time_intro
    thumby.display.fill(0)  
    thumby.display.blit(BBfiChe_logo,6,0,60,40,0,0,0)
    thumby.display.update()
    time.sleep(time_intro)
    thumby.display.fill(0)
    thumby.display.drawText("Keybinds:",3,1,1)
    thumby.display.drawText("----------------",5,6,1)
    thumby.display.setFont("/lib/font5x7.bin", 5, 7, 1)
    thumby.display.drawText("To Exit:",2,13,1)
    thumby.display.drawText("Hold A+B",2,22,1)
    thumby.display.update()
    thumby.display.setFont("/lib/font3x5.bin", 3, 5, 1)
    time.sleep(time_intro)
    thumby.display.fill(0)
    thumby.display.drawText("Keybinds:",3,1,1)
    thumby.display.drawText("----------------",5,6,1)
    thumby.display.setFont("/lib/font5x7.bin", 5, 7, 1)
    thumby.display.drawText("Move around:",2,9,1)
    thumby.display.drawText("Left,Right,",1,17,1)
    thumby.display.drawText("Up,Down",1,25,1)
    thumby.display.drawText("Buttons",2,33,1)
    thumby.display.update()
    thumby.display.setFont("/lib/font3x5.bin", 3, 5, 1)
    time.sleep(time_intro)

intro()

#Main Code to run:
while True:
    thumby.display.blit(microsqrtcalc_logo,47 ,1 ,22 ,17 ,-1 ,0 ,0)
    thumby.display.drawText("1 2 3 4 5 <",2,2,1)
    thumby.display.drawText("6 7 8 9 0 i",2,10,1)
    thumby.display.drawText("Results:",8,18,1)
    thumby.display.drawText(f"Inpt:{result}",1,25,1)
    thumby.display.drawText(f"Out:{output}",1,31,1)
    thumby.display.blit(selected,selx,sely,7,9,0,0,0)
    sv_r = result
    # calculates the SQRT
    if result:
        output = sqrt(int(''.join(map(str, result))))
    #-----------------------------------------
    if thumby.buttonR.justPressed():
        selx += 8
    if thumby.buttonL.justPressed():
        selx -= 8
    if thumby.buttonD.justPressed():
        sely += 8
    if thumby.buttonU.justPressed():
        sely -= 8
    if thumby.buttonA.justPressed():
        xyplacmntchk()
    if thumby.buttonA.pressed() and thumby.buttonB.pressed():
        while True:
            thumby.display.fill(0)
            thumby.display.drawText("Are you sure you",3,1,1)
            thumby.display.drawText("Want to Exit?",6,7,1)
            thumby.display.drawText("----------------",5,11,1)
            thumby.display.drawText("Press up button",3,15,1)
            thumby.display.drawText("YES",15,25,1)
            thumby.display.drawText("NO",35,25,1)
            thumby.display.drawText("!",44,25,1)
            thumby.display.blit(sel_side,sels_x,sels_y,15,9,0,0,0)
            if thumby.buttonL.justPressed():
                sels_x -= 20
            if thumby.buttonR.justPressed():
                sels_x += 20
            if sels_x < 12:
                sels_x = 13
            if sels_x > 35:
                sels_x = 33
            if thumby.buttonU.justPressed():
                    if sels_x > 30:
                        break
                    if sels_x == 13:
                        thumby.reset()
            thumby.display.update()
           
        time.sleep(0.2)
    if sely == -8:
        sely += 8
    if selx == 48:
        selx -= 8
    if selx == -8:
        selx += 8
    if sely == 16:
        sely -= 8
    thumby.display.update()
    thumby.display.fill(0)
