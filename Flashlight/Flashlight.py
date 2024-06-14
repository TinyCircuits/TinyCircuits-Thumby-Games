import thumby
import time

# A-Flashlight.py

black = bytearray([255, 233, 207, 9, 15, 9, 207, 233,
                   3, 3, 3, 0, 0, 0, 3, 3])

white = bytearray([0, 22, 48, 246, 240, 246, 48, 22,
                   0, 0, 0, 3, 3, 3, 0, 0])

version = bytearray([255, 233, 207, 9, 15, 9, 207, 233,
                     3, 3, 3, 0, 0, 0, 3, 3])
                     

# BITMAP: width: 8, height: 8
copyright = bytearray([255,129,189,165,165,165,129,255])

clicks = 1
fill = 1

while True:
    thumby.display.fill(fill)
    thumby.display.blit(version, 0, 31, 8, 8, -1, 0, 0)

    if thumby.buttonA.justPressed():
        if fill == 1:
            fill = 0
            version = bytearray([0, 22, 48, 246, 240, 246, 48, 22,
                                 0, 0, 0, 3, 3, 3, 0, 0])
        else:
            fill = 1
            version = bytearray([255, 233, 207, 9, 15, 9, 207, 233,
                                 3, 3, 3, 0, 0, 0, 3, 3])

    if thumby.buttonB.justPressed():
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