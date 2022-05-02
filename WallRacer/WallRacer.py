# WallRacer V1.0

import time
import thumby
import random
           
VIRTUAL_WIDTH = 2 *  thumby.display.width
VIRTUAL_HEIGHT = 2 * thumby.display.height

byte_size = VIRTUAL_WIDTH * VIRTUAL_HEIGHT // 8
virtual_screen = bytearray(byte_size)   

random.seed()

highscore = 1
speed = 1

# 72x20 for 1 frames
title = bytearray([0,16,240,240,16,0,0,192,240,0,0,0,144,112,16,0,0,0,0,128,128,128,128,0,0,8,252,0,0,8,252,0,0,0,16,240,240,16,16,48,224,0,0,0,0,0,128,128,128,128,0,0,0,0,0,128,128,128,0,0,0,0,128,128,0,0,0,0,0,0,0,0,0,0,1,255,112,12,3,0,7,254,96,28,3,0,0,124,131,129,193,112,63,255,129,128,0,255,128,0,0,255,128,0,128,128,255,135,4,12,60,226,129,128,124,131,129,193,112,63,255,129,128,0,126,129,129,128,64,64,0,124,211,137,132,67,64,0,225,31,2,1,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0])
           
# Draw a point on the virtual screen      
def draw(x, y):
    byteposition = x + ((y // 8) * VIRTUAL_WIDTH)
    bitmask = 1 << (y % 8);
    virtual_screen[byteposition] = virtual_screen[byteposition] | bitmask

# Check if a point is set in the virtual screen    
def check(x,y):
    byteposition = x + ((y // 8) * VIRTUAL_WIDTH)
    bitmask = 1 << (y % 8);
    
    return  (virtual_screen[byteposition] & bitmask) != 0
    
# Draw the outer frame of the game board
def draw_frame():
    for x in range(VIRTUAL_WIDTH):
      draw(x,0)
      draw(x,VIRTUAL_HEIGHT-1)
    for y in range(VIRTUAL_HEIGHT):
      draw(0,y)
      draw(VIRTUAL_WIDTH-1,y)

# Clear virtual screen      
def clear_screen():
    for p in range(byte_size):
        virtual_screen[p] = 0
      
# Game loop
def play_game():
    global speed
    
    thumby.display.setFPS(60)
    
    
    # Clear Virtual Screen
    clear_screen()
    # Add the Frame
    draw_frame()
    # Intalize Player
    player_x =random.randint(20, VIRTUAL_WIDTH - 40)
    player_y = random.randint(20, VIRTUAL_HEIGHT - 40)
    if (player_x > (VIRTUAL_WIDTH // 2)):
        player_direction = 2
    else:        
        player_direction = 0
    points = 0
    step = 0
  
    running = 1
  
    while (running):
        # Turn Left, any direction Button
        if thumby.buttonU.justPressed() or thumby.buttonD.justPressed()  or thumby.buttonL.justPressed() or thumby.buttonR.justPressed():
          player_direction = (player_direction - 1) % 4

        # Turn Right
        if thumby.buttonA.justPressed() or thumby.buttonB.justPressed():
            player_direction = (player_direction + 1) % 4
    
    
        step = step + speed;
        if (step >= 10):
            step = 0  
            if player_direction == 0:
                player_x = player_x + 1

            if player_direction == 1:
                player_y = player_y + 1

            if player_direction == 2:
                player_x = player_x - 1
        
            if player_direction == 3:
                player_y = player_y - 1
    
            #check for crash
            if check(int(player_x),int(player_y)):
               running = 0
    
            draw(int(player_x),int(player_y))
            points += 1

        thumby.display.fill(0)

        screen_x = int(thumby.display.width // 2 - player_x)
        screen_y = int(thumby.display.height // 2 - player_y)
    
        thumby.display.blit(virtual_screen, screen_x , screen_y  , VIRTUAL_WIDTH, VIRTUAL_HEIGHT, -1, 0, 0)
        thumby.display.update()

    return points

# Display points and highscore at end of game    
def display_points(points):
    global highscore
    
    thumby.display.setFPS(30)

    
    if (points > highscore):
        highscore = points
    
    thumby.display.fill(0)
      
    thumby.display.setFont("/lib/font8x8.bin", 8, 8, 1)
    thumby.display.drawText("Crash!", 8, 0, 1)
    
    thumby.display.setFont("/lib/font5x7.bin", 5, 7, 1)
    
    thumby.display.drawText("P:", 0, 16, 1)
    thumby.display.drawText(str(points), 18, 16, 1)
    
    thumby.display.drawText("H:", 0, 26, 1)
    thumby.display.drawText(str(highscore), 18, 26, 1)
    
    
    thumby.display.update()
    

    running = 1
    while (running):
        if thumby.buttonA.justPressed() or thumby.buttonB.justPressed():
            running = 0
      
# Dsiplay logo and speed selection
def display_menu():
    global speed
    running = 1
    step = 0
    
    thumby.display.fill(0)

    thumby.display.update()

    thumby.display.setFPS(30)
    
    thumby.display.setFont("/lib/font5x7.bin", 5, 7, 1)
    thumby.display.drawText("Speed:", 0, 22, 1)
    thumby.display.drawText(str(speed), 46, 22, 1)
    
    
    while (running):
        if thumby.buttonA.justPressed() or thumby.buttonB.justPressed():
            running = 0
        if (step < 72):
          step += 1    
          thumby.display.blit(title, 0 , 0 , step, 20, -1, 0, 0)

        if thumby.buttonU.justPressed():
            if (speed < 10):
                speed += 1
        if thumby.buttonD.justPressed():
            if (speed > 1):
                speed -= 1
        thumby.display.drawFilledRectangle(46, 22, 14, 7, 0)            
        thumby.display.drawText(str(speed), 46, 22, 1)
        thumby.display.update()
                


while(1):
  display_menu()
  points = play_game()    
  display_points(points)

