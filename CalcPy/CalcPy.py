import thumby
from time import sleep

# Calculator icon
# BITMAP: width: 31, height: 38
bitmap0 = bytearray([254,255,255,7,7,7,199,71,71,71,71,71,71,71,71,71,71,71,71,71,71,71,71,71,199,7,7,7,255,255,254,
           255,255,255,0,0,0,231,228,228,228,228,4,4,228,228,228,228,228,4,4,228,228,228,228,231,0,0,0,255,255,255,
           255,255,255,0,0,0,243,243,243,243,243,0,0,243,243,243,243,243,0,0,243,243,243,243,243,0,0,0,255,255,255,
           255,255,255,0,0,0,249,249,249,249,249,0,0,249,249,249,249,249,0,0,249,249,249,249,249,0,0,0,255,255,255,
           31,63,63,56,56,56,56,56,56,56,56,56,56,56,56,56,56,56,56,56,56,56,56,56,56,56,56,56,63,63,31])
           
splash = thumby.Sprite(31, 38, bitmap0, 1, 1)

thumby.display.drawSprite(splash)
thumby.display.setFont('/lib/font8x8.bin', 8, 8, -1)
thumby.display.drawText('Ca', 32, 5, 1)
thumby.display.drawText('l', 45, 5, 1)
thumby.display.drawText('cPy', 51, 5, 1)
thumby.display.update()
sleep(1.3)
thumby.display.setFont('/lib/font5x7.bin', 5, 7, 1)
thumby.display.drawText('by', 46, 16, 1)
thumby.display.drawText('UnRed', 37, 24, 1)
thumby.display.drawText('Known', 37, 32, 1)
thumby.display.update()
thumby.display.fill(0)
thumby.display.setFont('/lib/font3x5.bin', 3, 5, 1)
sleep(1)

import math
import thumbyButton as button
from sys import path
path.append('/Games/CalcPy')
import CalcFun

prevExp = ''
layer = 0
cursor_pos = 1
prevCursor_pos = 0
char = ''
exp = ''
result = ''
exclude = ['del', 'clr', 'right', 'left', 'menu']
sqrts = []
donewline = 0
selx = 0
sely = 0
frameCounter = 0
borw = 0
rOffset = 0
doOffset = 0

# Numpad
# BITMAP: width: 22, height: 33
bitmap1 = bytearray([255,1,1,9,125,1,1,1,1,73,101,85,73,1,1,1,85,85,85,41,1,1,
           255,0,12,16,16,124,0,0,0,76,84,84,52,0,0,0,56,84,84,48,0,0,
           255,0,4,116,12,0,0,0,0,40,84,84,40,0,0,0,8,84,84,56,0,0,
           255,0,56,68,68,56,0,0,16,40,84,16,16,0,0,0,56,68,68,0,0,0,
           1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0])
numpad = thumby.Sprite(22, 33, bitmap1, 50, 7)

# Keypad
# BITMAP: width: 22, height: 33
bitmap2 = bytearray([255,17,17,125,17,17,1,1,1,17,41,69,1,1,1,1,1,69,41,17,1,1,
           255,16,16,16,16,16,0,0,0,0,56,68,0,0,0,0,0,68,56,0,0,0,
           255,0,40,16,40,0,0,0,16,8,4,8,16,0,0,0,0,24,24,0,0,0,
           255,16,16,84,16,16,0,0,0,16,32,60,4,0,0,68,32,16,8,68,0,0,
           1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0])
keypad = thumby.Sprite(22, 33, bitmap2, 50, 7)
           
# Square root
# BITMAP: width: 3, height: 5
bitmap3 = bytearray([4,15,1])
sqrt = thumby.Sprite(3, 5, bitmap3, 0, 0)

# Cursor, just a line
# BITMAP: width: 4, height: 1
bitmap4 = bytearray([1,1,1,1])
cursor = thumby.Sprite(4, 1, bitmap4, 0, 0)

# Cursor, just a line but black
# BITMAP: width: 4, height: 1
bitmap5 = bytearray([0,0,0,0])
cursorb = thumby.Sprite(4, 1, bitmap5, 0, 0)

while(1):
    
    frameCounter += 1
    
    if doOffset == 1:
        if frameCounter % 10 == 0:
            rOffset += 1
        
    if doOffset == 3:
        if rOffset > -4:
            if frameCounter % 10 == 0:
                rOffset -= 1
        else:
            doOffset = 4
    
    if doOffset == 2:
        if frameCounter % 100 == 0:
            doOffset = 3
    
    if doOffset == 4:
        if frameCounter % 100 == 0:
            doOffset = 0
    
    if len(str(result)) > 12:
        if rOffset < (len(str(result))*4) - 44:
            if doOffset == 0:
                doOffset = 1
        else:
            rOffset -= 1
            doOffset = 2
    else:
        doOffset = 0
    
    if doOffset == 3 and rOffset == -4:
        doOffset == 0
    
    if frameCounter % 60 == 0:
        borw = (borw+1) % 2
    
    if 'a' in exp:
        sqrts = [i for i, c in enumerate(exp) if c == 'a']
        
    for s in sqrts:
        try:
            if exp[s] != 'a':
                sqrts.pop(sqrts.index(s))
        except:
            sqrts.pop(sqrts.index(s))
    
    if len(exp) > 60: exp = exp[:-1]
    cursor.x = 1 if cursor_pos == 0 else (cursor_pos%12)*4 if cursor_pos < 60 else 80
    cursor.y = ((cursor_pos // 12)*6)+6
    cursorb.x = cursor.x
    cursorb.y = cursor.y
    thumby.display.fill(0)
    thumby.display.drawLine(50, 0, 50, 6, 1)
    thumby.display.drawLine(50, 7, 72, 7, 1)
    thumby.display.drawLine(0, 32, 49, 32, 1)
    CalcFun.printex(exp)
    result = str(result)
    if result == '<function>':
        thumby.display.drawText('USE (', 1, 34, 1)
    else:
        thumby.display.drawText(result, 1-rOffset, 34, 1)
    
    if layer == 0:
        thumby.display.drawSprite(numpad)
    elif layer == 1:
        thumby.display.drawSprite(keypad)
    thumby.display.drawLine(selx*7+50, sely*8+15, selx*7+56, sely*8+15, 1)
    thumby.display.drawLine(selx*7+50, sely*8+15, selx*7+50, sely*8+8, 1)
    thumby.display.drawLine(selx*7+50, sely*8+7, selx*7+56, sely*8+7, 1)
    thumby.display.drawLine(selx*7+57, sely*8+15, selx*7+57, sely*8+7, 1)
    thumby.display.drawText(CalcFun.desc(selx, sely, layer), 52, 1, 1)
    thumby.display.drawSprite(cursor if borw == 0 else cursorb)
    try:
        result = CalcFun.solve(exp)
    except:
        if len(exp) == 0:
            result = '='
        else:
            result = 'ERROR'
    if 'a' in exp:
       for s in sqrts:
            sqrt.x = s%12 * 4
            sqrt.y = (s//12)*6
            thumby.display.drawFilledRectangle(sqrt.x, sqrt.y, 4, 5, 0)
            thumby.display.drawSprite(sqrt)
    thumby.display.update()
    
    if cursor_pos < 0:
        cursor_pos = len(exp)
    elif cursor_pos > len(exp):
        cursor_pos = 0
    if button.buttonB.justPressed():
        layer = 1 if layer == 0 else 0
        
    if button.buttonL.justPressed():
        selx = (selx-1)%3
    elif button.buttonR.justPressed():
        selx = (selx+1)%3
        
    if button.buttonU.justPressed():
        sely = (sely-1)%4
    elif button.buttonD.justPressed():
        sely = (sely+1)%4
        
    if button.buttonA.justPressed():
        borw = 0
        frameCounter = -60
        char = CalcFun.char(selx, sely, layer)
        if char in exclude:
            if char == 'del':
                if cursor_pos != 0:
                    exp = exp[:cursor_pos-1] + exp[cursor_pos:]
                if len(exp) > 0 and cursor_pos != 0: cursor_pos -= 1
            elif char == 'clr':
                if prevExp == '':
                    prevExp = exp
                    prevCursor_pos = cursor_pos
                    exp = ''
                    cursor_pos = 0
                elif prevExp != '':
                    if exp == '':
                        exp = prevExp
                        cursor_pos = prevCursor_pos
                        prevExp = ''
                        prevCursor_pos = 0
                    else:
                        prevExp = exp
                        prevCursor_pos = cursor_pos
                        exp = ''
                        cursor_pos = 0
            elif char == 'left': cursor_pos -= 1
            elif char == 'right': cursor_pos += 1
        else:
            exp = exp[:cursor_pos] + CalcFun.char(selx, sely, layer) + exp[cursor_pos:]
            cursor_pos += 1
        
    
