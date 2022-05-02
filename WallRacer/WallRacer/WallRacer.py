# WallRacer V1.1

import time
import thumby
import random
import os
           
VIRTUAL_WIDTH = 2 *  thumby.display.width
VIRTUAL_HEIGHT = 2 * thumby.display.height
BYTE_SIZE = VIRTUAL_WIDTH * VIRTUAL_HEIGHT // 8
BONUS_FACTOR = 20
BONUS_DISTANCE = 10
EXPLOSION_BITS = 72
EXPLOSION_STEPS = 15

BONUS_COUNT = 3

# 72x16 for 1 frames
TITLE = bytearray([0,8,248,248,8,0,128,96,248,0,0,0,200,56,8,0,128,128,128,64,192,192,192,0,0,132,126,0,0,132,126,0,0,0,136,248,120,8,8,24,240,0,0,128,128,128,64,192,192,192,0,0,0,128,128,64,64,64,0,0,128,128,64,192,0,0,128,128,0,128,128,0,0,0,0,127,56,6,1,0,3,127,48,14,1,0,0,62,65,64,96,56,31,127,64,64,0,127,64,0,0,127,64,0,64,64,127,67,2,6,30,113,64,64,62,65,64,96,56,31,127,64,64,0,63,64,64,64,32,32,0,62,105,68,66,33,32,0,112,15,1,0,0,0])

random.seed()

# Init global variables
virtual_screen = bytearray(BYTE_SIZE)   
highscore = [0,0,0,0,0,0,0,0,0,0]
speed = 1
bonus = [] 

player_x = 0
player_y = 0



# Save highscore to file 
def saveHighscore():
    global highscore
    
    f = open("/Games/WallRacer/highscore.dat", "w")
    saveString = ",".join([str(i) for i in highscore])
    f.write(saveString)
    f.close()
    
# Load highscore from file, create new if no file exists
def loadHighscore():
    global highscore
    try:
        f = open("/Games/WallRacer/highscore.dat")
        loadString = f.read()
        splitted = s.split(",")
        highscore = [int(numeric_string) for numeric_string in splitted]    
        f.close()
    except: 
        saveHighscore()
        
# Add a bonus at random position but keep distance to other and player
def addBonus():
    global player_x
    global player_y

    ok = 0
    
    while (ok == 0):
        ok = 1
        x = random.randint(10, VIRTUAL_WIDTH - 20)
        y = random.randint(10, VIRTUAL_HEIGHT - 20)
        
        #check distance to player
        if (x >= player_x - BONUS_DISTANCE) and (x <= player_x + BONUS_DISTANCE) and (y >= player_y - BONUS_DISTANCE) and (y <= player_y + BONUS_DISTANCE):
            ok = 0
        
        #check distance to other bonus    
        for point in bonus:
            if (x >= point[0] - BONUS_DISTANCE) and (x <= point[0] + BONUS_DISTANCE) and (y >= point[1] - BONUS_DISTANCE) and (y <= point[1] + BONUS_DISTANCE):
              ok = 0
        
    point = [x,y]
    bonus.append(point)
    
# Add inital bonus 
def initBonus():
    bonus.clear()
    for c in range(BONUS_COUNT):
        addBonus()



# Draw a point on the virtual screen in selected color      
def draw(x, y, color):
    byteposition = x + ((y // 8) * VIRTUAL_WIDTH)
    bitmask = 1 << (y % 8);
    if (color == 1):
        virtual_screen[byteposition] = virtual_screen[byteposition] | bitmask
    else:
        virtual_screen[byteposition] = virtual_screen[byteposition] & ~bitmask
    
    

# Check if a point is set in the virtual screen    
def check(x,y):
    byteposition = x + ((y // 8) * VIRTUAL_WIDTH)
    bitmask = 1 << (y % 8);
    
    return  (virtual_screen[byteposition] & bitmask) != 0

# Draw a horizontakl line
# This can be optimzed
def draw_horizontal_line(x1,x2,y,color):
    for x in range(x1,x2+1):
        draw(x,y,color)
        
# Draw a vertical line
# This can be optimzed
def draw_vertical_line(x,y1,y2,color):
    for y in range(y1,y2+1):
        draw(x,y,color)
        
   
    
# Draw a frame
def draw_frame(x1,y1,x2,y2,color):
    draw_horizontal_line(x1,x2,y1,color)
    draw_horizontal_line(x1,x2,y2,color)
    draw_vertical_line(x1,y1,y2,color)
    draw_vertical_line(x2,y1,y2,color)
  

# Clear virtual screen      
def clear_screen():
    for p in range(BYTE_SIZE):
        virtual_screen[p] = 0
        

# Draw one bonus at x,y location
def draw_bonus(x, y, color):
    for nx in range(x-1, x+2):
        draw_vertical_line(nx, y-1, y+1, color)
      
  
# Draw all bonus from the list        
def draw_bonus_list(color):
    for point in bonus:
          draw_bonus(point[0], point[1], color)
      
# Check if a bonus is at location x,y if yes remove it from screen and return the index in the list      
def check_bonus(x,y):
    global player_x
    global player_y

    hit = -1
    for index in range(len(bonus)):
        point = bonus[index]
        if (x >= point[0]-1) and  (x <= point[0]+1) and  (y >= point[1]-1)  and  (y <= point[1]+1):
            draw_bonus(point[0], point[1], 0)
            hit = index
    return hit          
          

# Main game loop
def play_game():
    global speed
    global player_x
    global player_y

    #basic refresh speed    
    thumby.display.setFPS(60)
    
    
    # Clear virtual screen
    clear_screen()
    # Add the frame
    draw_frame(0,0,VIRTUAL_WIDTH-1, VIRTUAL_HEIGHT-1,1)
    
    # Intalize player position
    player_x =random.randint(20, VIRTUAL_WIDTH - 40)
    player_y = random.randint(20, VIRTUAL_HEIGHT - 40)
    
    # If player starts in the left halve from screen start running right
    # If plyer starts in the right halve of the screen start running left
    if (player_x > (VIRTUAL_WIDTH // 2)):
        player_direction = 2
    else:        
        player_direction = 0
    # points player has collected for this game
    points = 0
    # used for bonus flashing and speed
    counter = 0
    
    initBonus()
    
  
    running = 1
    while (running):
        # Turn left on any direction Button
        if thumby.buttonU.justPressed() or thumby.buttonD.justPressed()  or thumby.buttonL.justPressed() or thumby.buttonR.justPressed():
          player_direction = (player_direction - 1) % 4

        # Turn right on A or B
        if thumby.buttonA.justPressed() or thumby.buttonB.justPressed():
            player_direction = (player_direction + 1) % 4
    
    
        # throttle player 
        if (counter % (11-speed) == 0):
            # calculate new player position
            if player_direction == 0:
                player_x = player_x + 1

            if player_direction == 1:
                player_y = player_y + 1

            if player_direction == 2:
                player_x = player_x - 1
        
            if player_direction == 3:
                player_y = player_y - 1
    
            # check for bonus 
            hit = check_bonus(player_x, player_y)
            if (hit >= 0):
                # if hit remove the existing bonus and add a new one
                del bonus[hit]
                addBonus()
                bonus_points = speed * BONUS_FACTOR
                points += bonus_points
                thumby.display.fill(0)
                thumby.display.setFont("/lib/font8x8.bin", 8, 8, 1)
                thumby.display.drawText("Bonus!", 12, 10, 1)
                # center the bonus points
                if (bonus_points >= 1000):
                    length = 4 * 8
                elif (bonus_points >= 100):
                    length = 3 * 8
                elif (bonus_points >= 10):
                    length = 2 * 8
                else:
                    length = 8
                xpos =  (thumby.display.width // 2) - (length // 2) 
                thumby.display.drawText(str(speed * BONUS_FACTOR), xpos , 20, 1)
                
                thumby.display.update()
                time.sleep(1)
    
            #check for crash
            if check(player_x, player_y):
                explosion(36,20)
                running = 0
    
            draw(player_x, player_y, 1)
            points += 1
            
        counter += 1
        draw_bonus_list(counter % 2)

        thumby.display.fill(0)

        screen_x = int(thumby.display.width // 2 - player_x)
        screen_y = int(thumby.display.height // 2 - player_y)
    
        thumby.display.blit(virtual_screen, screen_x , screen_y  , VIRTUAL_WIDTH, VIRTUAL_HEIGHT, -1, 0, 0)
        thumby.display.update()

    return points

# Display points and highscore at end of game    
def display_points(points):
    global highscore
    global speed
    
    thumby.display.setFPS(30)

    
    if (points > highscore[speed-1]):
        highscore[speed-1] = points
        saveHighscore() 

    
    thumby.display.fill(0)
      
    thumby.display.setFont("/lib/font8x8.bin", 8, 8, 1)
    thumby.display.drawText("Crash!", 8, 0, 1)
    
    thumby.display.setFont("/lib/font5x7.bin", 5, 7, 1)
    
    thumby.display.drawText("P:", 0, 16, 1)
    thumby.display.drawText(str(points), 18, 16, 1)
    
    thumby.display.drawText("H:", 0, 26, 1)
    thumby.display.drawText(str(highscore[speed-1]), 18, 26, 1)
    
    
    thumby.display.update()
    

    running = 1
    while (running):
        if thumby.buttonA.justPressed() or thumby.buttonB.justPressed():
            running = 0
            
            
def explosion(x, y):
    step = 0

    bits = []
    for count in range(EXPLOSION_BITS):
        # x,y x speed, y speed
        bit = [x,y, (random.randint(0,40)-20) / 10, (random.randint(0,40) - 20) / 10]
        bits.append(bit)
    
    # animation is a bit fast on 60fps
    thumby.display.setFPS(30)

    
    while(step < EXPLOSION_STEPS):
        step += 1
        
        #remove from current position
        for bit in bits:
            thumby.display.setPixel(int(bit[0]), int(bit[1]), 0)
            
        # move bits to new position    
        for bit in bits:
            bit[0] = bit[0] + bit[2]
            if bit[0] < 0:
                bit[0] = 0
            if bit[0] >= thumby.display.width:
                bit[0] = thumby.display.width -1
                
            bit[1] = bit[1] + bit[3]
            if bit[1] < 0:
                bit[1] = 0
            if bit[1] >= thumby.display.height:
                bit[1] = thumby.display.height -1
            
        # draw at new position    
        for bit in bits:
            thumby.display.setPixel(int(bit[0]), int(bit[1]), 1)
            

        thumby.display.update()
    #remove from current position
    for bit in bits:
        thumby.display.setPixel(int(bit[0]), int(bit[1]), 0)
    thumby.display.update()
      

            
def test():
    
    explosion(36,20)
            
      
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
          thumby.display.blit(TITLE, 0 , 0 , step, 16, -1, 0, 0)

        if thumby.buttonU.justPressed():
            if (speed < 10):
                speed += 1
        if thumby.buttonD.justPressed():
            if (speed > 1):
                speed -= 1
                
        if thumby.buttonL.justPressed():
            test()
                
                
        thumby.display.drawFilledRectangle(46, 22, 14, 7, 0)            
        thumby.display.drawText(str(speed), 46, 22, 1)
        thumby.display.update()
                


loadHighscore() 


while(1):
  display_menu()
  points = play_game()    
  display_points(points)

