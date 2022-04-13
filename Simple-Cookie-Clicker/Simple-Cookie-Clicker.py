import time
import thumby
import machine


"""
            ** Simple Cookie Clicker **

    
    Created by: Camerin Figueroa
    
    Github: RaspberryProgramming
    Website: https://www.camscode.com/
    
    Designed for the Thumby - https://thumby.us/
    Kickstarter Page: https://www.kickstarter.com/projects/kenburns/thumby-the-tiny-playable-keychain
    
    Emulate using their handy Web IDE: https://code.thumby.us/
    
    
"""


machine.freq(48000000)

# cookie bitmaps

cookie_bitmap = bytearray([0,0,0,128,224,240,248,124,252,254,254,254,254,254,254,254,255,255,127,63,126,254,254,252,248,240,224,224,192,128,0,0,
           96,254,255,255,255,255,255,252,252,255,255,63,31,31,31,255,255,255,254,252,254,255,255,255,255,31,191,255,255,255,254,0,
           0,127,255,255,255,195,199,239,255,255,255,255,254,254,255,255,255,255,255,255,255,199,135,135,207,255,255,255,255,255,127,6,
           0,0,1,3,7,15,15,31,63,127,127,127,127,248,248,252,127,127,127,127,127,127,127,63,31,31,7,3,1,0,0,0])
           
clicked_cookie_bitmap = bytearray([0,128,192,240,248,252,62,254,255,255,255,255,255,255,255,255,63,63,255,255,254,252,248,240,224,224,192,0,
           255,255,255,255,255,255,254,255,255,255,207,135,135,255,255,255,255,255,255,255,255,255,207,255,255,255,255,255,
           15,63,127,127,249,248,255,255,255,255,255,159,31,159,255,255,255,255,255,240,241,251,255,255,127,63,31,15,
           0,0,0,0,0,1,3,7,15,15,15,15,15,15,15,15,15,15,15,15,7,3,1,0,0,0,0,0])


# cookie Sprites

cookieSprite = thumby.Sprite(32, 32, cookie_bitmap, 22, 0, -1)

clickedCookieSprite = thumby.Sprite(28, 28, clicked_cookie_bitmap, 24, 2, -1)

# Cookie Count

cookieCount = 0

# Loop

while (True):
    
    thumby.display.fill(0) # Fill canvas to black

    # Display cookie being clicked
    if thumby.buttonA.pressed():
        thumby.display.drawSprite(clickedCookieSprite)
    
    # Draw Regular cookie
    else:
        thumby.display.drawSprite(cookieSprite)
    
    # First iteration after being pressed, increase cookie count
    if thumby.buttonA.justPressed():
        cookieCount += 1

    # Draw cookie count
    thumby.display.drawText("Cookies %d" % cookieCount, 2, 32, 1)

    # Update Display
    thumby.display.update()
    
