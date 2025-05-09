import thumby
import time

# A-Flashlight.py

black = bytearray([255, 233, 207, 9, 15, 9, 207, 233,
                   3, 3, 3, 0, 0, 0, 3, 3])

white = bytearray([0, 22, 48, 246, 240, 246, 48, 22,
                   0, 0, 0, 3, 3, 3, 0, 0])

# BITMAP: width: 8, height: 10
off_flashlight = bytearray([0,16,48,240,240,240,48,16,
           0,0,0,3,3,3,0,0])

version = bytearray([255, 233, 207, 9, 15, 9, 207, 233,
                     3, 3, 3, 0, 0, 0, 3, 3])
                     

# BITMAP: width: 8, height: 8
copyright = bytearray([255,129,189,165,165,165,129,255])

clicks = 1
fill = 1
ctr = 2

thumby.display.fill(1)
thumby.display.brightness(127)

def checks():
    global ctr
    if ctr == 0:
        thumby.display.brightness(27)
    if ctr == 1:
        thumby.display.brightness(72)
    if ctr == 2:
        thumby.display.brightness(127)
    if ctr > 2:
        ctr = 0
    if ctr < 0:
        ctr = 2

while True:
    checks()
    thumby.display.fill(fill)
    #thumby.display.blit(version, 0, 31, 8, 8, -1, 0, 0)

    if thumby.buttonU.justPressed():
        ctr += 1
    if thumby.buttonD.justPressed():
        ctr -= 1
        

    if thumby.buttonB.justPressed() or thumby.buttonA.justPressed():
        if clicks == 1:
            thumby.display.fill(0)
            thumby.display.drawText("Exiting...", 5, 10, 1)
            thumby.display.drawText("   BBfiChe", 3, 25, 1)
            thumby.display.blit(copyright, 4, 25, 8, 8, -1, 0, 0)
            thumby.display.update()
            time.sleep(3)
            thumby.reset()
        else:
            clicks += 1

    thumby.display.update()
