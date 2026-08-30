import time
import thumby

# BITMAP: width: 40, height: 20
logo1 = bytearray([0, 0, 192, 216, 24, 24, 24, 24, 24, 24, 56, 248, 248, 56, 248, 248, 248, 224, 128, 0, 0, 128, 192, 224, 112, 62, 30, 206, 230, 230, 102, 102, 6, 6, 4, 12, 252, 248, 112, 0, 0, 28, 31, 31, 24, 24, 24, 24, 24, 28, 30, 15, 7, 0, 0, 3, 15, 127, 63, 15, 7, 3, 1, 0, 0, 0, 0, 15, 15, 15, 12, 12, 12, 12, 14, 3, 3, 1, 0, 0, 246, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 246])
logo2 = bytearray([255, 255, 63, 39, 231, 231, 231, 231, 231, 231, 199, 7, 7, 199, 7, 7, 7, 31, 127, 255, 255, 127, 63, 31, 143, 193, 225, 49, 25, 25, 153, 153, 249, 249, 251, 243, 3, 7, 143, 255, 255, 227, 224, 224, 231, 231, 231, 231, 231, 227, 225, 240, 248, 255, 255, 252, 240, 128, 192, 240, 248, 252, 254, 255, 255, 255, 255, 240, 240, 240, 243, 243, 243, 243, 241, 252, 252, 254, 255, 255, 9, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 9])

# Initial mode states
current_logo = logo1
fill_color = 0
key_color = 0

# Track previous button state for single press detection
any_button_last_state = False

thumby.display.setFPS(60)
y = 20
x = 20
ydir = 'up'
xdir = 'right'

def is_any_button_pressed():
    return (
        thumby.buttonA.pressed() or
        thumby.buttonB.pressed() or
        thumby.buttonU.pressed() or
        thumby.buttonD.pressed() or
        thumby.buttonL.pressed() or
        thumby.buttonR.pressed()
    )

while True:
    # Check button states
    any_button_pressed = is_any_button_pressed()
    
    # Toggle parameters on initial press (rising edge detection)
    if any_button_pressed and not any_button_last_state:
        current_logo = logo2 if current_logo == logo1 else logo1
        fill_color = 1 if fill_color == 0 else 0
        key_color = 1 if key_color == 0 else 0
        
    any_button_last_state = any_button_pressed

    # Clear screen with active fill color
    thumby.display.fill(fill_color)
    
    print(xdir, ydir, x, y)
    
    # Boundary checks
    if y <= 0:
        ydir = 'down'
    if y >= 20:
        ydir = 'up'
    if x <= 0:
        xdir = 'right'
    if x >= 30:
        xdir = 'left'

    # Position updates
    if ydir == 'down':
        y += 1
    if ydir == 'up':
        y -= 1
    if xdir == 'left':
        x -= 1
    if xdir == 'right':
        x += 1

    time.sleep(0.1)
    
    # Render logo with active key color
    thumby.display.blit(current_logo, x, y, 40, 20, key_color, 0, 0)
    thumby.display.update()
