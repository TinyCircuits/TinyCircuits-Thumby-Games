# WallRacer V1.3

import time
import thumby
import random
import os
import framebuf


# Const Definitions           
GAME_NAME = "WallRacer"
VERSION = "V1.3"
VIRTUAL_WIDTH = 2 *  thumby.display.width
VIRTUAL_HEIGHT = 2 * thumby.display.height
BYTE_SIZE = VIRTUAL_WIDTH * VIRTUAL_HEIGHT // 8
BONUS_FACTOR = 20  # points for collecting a bonus dot multiplied by speed
BONUS_DISTANCE = 10 # minimum distance between dots
BONUS_COUNT = 3 # number of bonus dots displayed
EXPLOSION_BITS = 72 # number of pixels in the explosion
EXPLOSION_STEPS = 15 # number of steps the explosion runs


# Logging, uncomment to activate
#logfile = open("/Games/WallRacer/WallRacer.log", "w")
def log(msg):
    global logfile  
    #xmsg = str(time.ticks_ms())+": "+msg
    #logfile.write(xmsg+ "\n")
    #logfile.flush()
    #print(xmsg)

# Initialization
random.seed(time.ticks_ms())


# Virtual Screen and graphics

# 72x16 for 1 frames
TITLE = bytearray([0,8,248,248,8,0,128,96,248,0,0,0,200,56,8,0,128,128,128,64,192,192,192,0,0,132,126,0,0,132,126,0,0,0,136,248,120,8,8,24,240,0,0,128,128,128,64,192,192,192,0,0,0,128,128,64,64,64,0,0,128,128,64,192,0,0,128,128,0,128,128,0,0,0,0,127,56,6,1,0,3,127,48,14,1,0,0,62,65,64,96,56,31,127,64,64,0,127,64,0,0,127,64,0,64,64,127,67,2,6,30,113,64,64,62,65,64,96,56,31,127,64,64,0,63,64,64,64,32,32,0,62,105,68,66,33,32,0,112,15,1,0,0,0])
# 22x29 for 4 frames
NUMBERS = bytearray([0,0,224,248,252,254,254,255,63,31,31,31,31,63,255,254,254,252,248,224,0,0,0,254,255,255,255,255,255,0,0,0,0,0,0,0,0,255,255,255,255,255,254,0,0,15,255,255,255,255,255,224,128,0,0,0,0,128,224,255,255,255,255,255,15,0,0,0,0,3,7,15,15,31,31,31,31,31,31,31,31,15,15,7,3,0,0,0,0,0,0,240,248,248,252,126,255,255,255,255,255,255,0,0,0,0,0,0,0,0,0,0,0,3,1,1,0,0,255,255,255,255,255,255,0,0,0,0,0,0,0,0,0,0,0,128,128,128,128,128,255,255,255,255,255,255,128,128,128,128,128,0,0,0,0,0,0,31,31,31,31,31,31,31,31,31,31,31,31,31,31,31,31,0,0,0,0,128,224,248,252,254,254,255,63,31,31,31,31,63,254,254,254,252,248,224,0,0,0,3,3,3,3,7,7,0,0,0,128,192,224,248,255,255,255,127,31,7,0,0,0,128,192,224,240,248,248,252,190,191,159,143,143,135,131,129,128,128,128,128,0,0,0,31,31,31,31,31,31,31,31,31,31,31,31,31,31,31,31,31,31,31,0,0,0,0,0,32,56,126,126,127,63,15,15,15,15,31,255,255,255,254,252,240,0,0,0,0,0,0,0,0,0,0,248,248,248,248,248,252,255,255,223,207,135,131,0,0,0,0,48,240,248,248,248,224,192,128,128,128,128,193,227,255,255,255,255,255,126,0,0,0,0,0,1,3,7,7,15,15,31,31,31,31,15,7,7,7,3,1,0,0])

screen_buffer = bytearray(BYTE_SIZE)
virtual_screen = framebuf.FrameBuffer(screen_buffer, VIRTUAL_WIDTH, VIRTUAL_HEIGHT, framebuf.MONO_VLSB)

number_sprite = thumby.Sprite(22, 29, NUMBERS, 25, 10, -1, 0, 0)


# Global Vars
highscore = [0,0,0,0,0,0,0,0,0,0]

speed = 1
bonus = [] # position of bonus dots
game_mode = 0 # 0 = full 1 = pure 2= multiplayer
player_x = 0
player_y = 0
player_direction = 0

# for multiplayer
won = 0 
first_player = 0
sending = True


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
        
# Add a bonus dot at random position but keep distance to other dots and player
def addBonus():
    global player_x
    global player_y

    ok = False
    
    while (not ok):
        ok = True
        x = random.randint(10, VIRTUAL_WIDTH - 10)
        y = random.randint(10, VIRTUAL_HEIGHT - 10)
        
        #check distance to player
        if (x >= player_x - BONUS_DISTANCE) and (x <= player_x + BONUS_DISTANCE) and (y >= player_y - BONUS_DISTANCE) and (y <= player_y + BONUS_DISTANCE):
            ok = False
        
        #check distance to other bonus    
        for point in bonus:
            if (x >= point[0] - BONUS_DISTANCE) and (x <= point[0] + BONUS_DISTANCE) and (y >= point[1] - BONUS_DISTANCE) and (y <= point[1] + BONUS_DISTANCE):
              ok = False
        
    point = [x,y]
    bonus.append(point)
    
# Add inital bonus 
def initBonus():
    bonus.clear()
    for c in range(BONUS_COUNT):
        addBonus()


# Draw one bonus dot at x,y location
def drawBonus(x, y, color):
    for nx in range(x-1, x+2):
        virtual_screen.vline(nx,y-1,3,color)
      
  
# Draw all bonus dots from the list        
def drawBonusList(color):
    for point in bonus:
          drawBonus(point[0], point[1], color)
      
# Check if a bonus is at location x,y if yes remove it from screen and return the index in the list      
def checkBonus(x,y):
    hit = -1
    for index in range(len(bonus)):
        point = bonus[index]
        if (x >= point[0]-1) and  (x <= point[0]+1) and  (y >= point[1]-1)  and  (y <= point[1]+1):
            drawBonus(point[0], point[1], 0)
            hit = index
    return hit          



def setStartPosition():
    global game_mode
    global player_x
    global player_y
    global player_direction
    
    if (game_mode == 2):
        if first_player:
            startpos = random.randint(0,1)
        else:            
            startpos = random.randint(2,3)
    else:
        startpos = random.randint(0,3) 

    if startpos == 0:
       player_x = 10
       player_y = 10
       player_direction = 0
    elif startpos == 1:
       player_x = 10
       player_y = VIRTUAL_HEIGHT - 10
       player_direction = 0
    elif startpos == 2:
       player_x =  VIRTUAL_WIDTH - 10
       player_y = 10
       player_direction = 2
    else:
       player_x =  VIRTUAL_WIDTH - 10
       player_y = VIRTUAL_HEIGHT - 10
       player_direction = 2



# Main game loop
def playGame():
    global game_mode
    global speed
    global player_x
    global player_y
    global player_direction
    global sending
    global won
    global first_player

    log("Game")

    
    # Clear virtual screen
    virtual_screen.fill(0)
    # Add the frame
    virtual_screen.rect(0,0,VIRTUAL_WIDTH,VIRTUAL_HEIGHT-1,1)
    
    # Initialize player position in one of the corners
    setStartPosition()
    
    # points player has collected for this game
    points = 0
    # used for bonus flashing and speed
    counter = 0
    
    #Bonus dots only for mode 0
    if (game_mode == 0):
      initBonus()
      
    # default empty message for multiplayer
    send_data = bytearray([0])
    
    # refresh speed  
    throttle = 11 - speed

    
    running = 1
    while (running):
        # Turn left on any direction Button
        if thumby.buttonU.justPressed() or thumby.buttonD.justPressed()  or thumby.buttonL.justPressed() or thumby.buttonR.justPressed():
          player_direction = (player_direction - 1) % 4

        # Turn right on A or B
        if thumby.buttonA.justPressed() or thumby.buttonB.justPressed():
            player_direction = (player_direction + 1) % 4



    
        # throttle player 
        if (counter % throttle == 0):
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
            if (game_mode == 0):
                hit = checkBonus(player_x, player_y)
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
            if virtual_screen.pixel(player_x, player_y):
                explosion(36,20)
                running = 0
                won = 0
                if (game_mode == 2):
                    #create explosion message
                    send_data = bytearray([5, player_x, player_y])
            else:
                if (game_mode == 2):
                    #create player position message
                    send_data = bytearray([4, player_x, player_y])
                
            
            #Draw the player    
            virtual_screen.pixel(player_x, player_y, 1)    
            points += 1
            
        if (game_mode == 0):
            drawBonusList(counter % 2)


        # send and receive multiplayer messages
        if (game_mode == 2):
            received = thumby.link.receive() 
            if received != None:
                # Player position message
                if received[0] == 4:
                    virtual_screen.pixel(received[1], received[2], 1)
                # Player crash message    
                elif received[0] == 5:
                    explosion(received[1] - player_x + 36, received[2] - player_y + 20)
                    won = 1
                    points *= 2
                    running = 0
                sending = True # got a message, now I am allowed to send
        
            if sending:
                if thumby.link.send(send_data):
                    sending = False # just sent a messages, stop sending until i got a messages
                    send_data = bytearray([0]) # message is sent, clear it
                

        # update screem
        thumby.display.fill(0)
        screen_x = int(thumby.display.width // 2 - player_x)
        screen_y = int(thumby.display.height // 2 - player_y)
        thumby.display.blit(screen_buffer, screen_x , screen_y  , VIRTUAL_WIDTH, VIRTUAL_HEIGHT, -1, 0, 0)
        thumby.display.update()

        counter += 1
    return points

# Display points and highscore at end of game    
def displayPoints(points):
    global highscore
    global speed
    global game_mode
    global won

    log("Points")

    
    thumby.display.setFPS(30)

    
    thumby.display.fill(0)
    thumby.display.setFont("/lib/font8x8.bin", 8, 8, 1)
    if (game_mode ==2):
        if won:
            thumby.display.drawText("Winner!", 8, 0, 1)
        else:
            thumby.display.drawText("Lost!", 8, 0, 1)
    else:    
        thumby.display.drawText("Crash!", 8, 0, 1)
    
    thumby.display.setFont("/lib/font5x7.bin", 5, 7, 1)
    
    thumby.display.drawText("P:", 0, 16, 1)
    thumby.display.drawText(str(points), 18, 16, 1)

    # Highscore only for single player
    if (game_mode < 2):
        if (points > highscore[speed-1]):
            highscore[speed-1] = points
            saveHighscore() 
        thumby.display.drawText("H:", 0, 26, 1)
        thumby.display.drawText(str(highscore[speed-1]), 18, 26, 1)
    thumby.display.update()
    

    # wait for button press
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
      
            
      
# Dsiplay logo and speed selection
def displayMenu():
    global speed
    global game_mode
    global VERSION

    log("Menu")

    thumby.display.setFPS(30)

    
    running = 1
    step = 0
    
    thumby.display.fill(0)
    thumby.display.update()

    
    thumby.display.setFont("/lib/font5x7.bin", 5, 7, 1)
    thumby.display.drawText("Speed:", 0, 17, 1)
    thumby.display.drawText("Mode:", 0, 25, 1)
    thumby.display.drawText(VERSION, 0, 33, 1)
    
    
    while (running):
        # Button A or B to start
        if thumby.buttonA.justPressed() or thumby.buttonB.justPressed():
            running = 0
    
        # Logo animation    
        if (step < 72):
          step += 1    
          thumby.display.blit(TITLE, 0 , 0 , step, 16, -1, 0, 0)
    

       
        # Speed selection
        if thumby.buttonU.justPressed():
            if (speed < 10):
                speed += 1
        if thumby.buttonD.justPressed():
            if (speed > 1):
                speed -= 1
            changed = 1

                
        # Mode selection    
        if thumby.buttonR.justPressed():
            if (game_mode < 2):
                game_mode += 1
        if thumby.buttonL.justPressed():
            if (game_mode > 0):
                game_mode -= 1
            changed = 1

                
        
        # Update display
        thumby.display.drawFilledRectangle(46, 17, 14, 7, 0)            
        thumby.display.drawText(str(speed), 46, 17, 1)
        
        # Display mode
        thumby.display.drawFilledRectangle(46, 25, 26, 7, 0)            
        if (game_mode == 0):
            thumby.display.drawText("1P *", 46, 25, 1)
        elif (game_mode == 1):
            thumby.display.drawText("1P", 46, 25, 1)
        else:    
            thumby.display.drawText("2P", 46, 25, 1)
        thumby.display.update()
          
                

# messages
# 0 nothing to do
# 1,<speed> connect
# 2,<countdown> start countdown
# 4,x,y player position
# 5,x,y crash
                

def batostr(ba):
   return ", ".join(str(b) for b in ba)
    

def waitForPlayer():
    global sending
    global speed
    global first_player

    log("WaitForPlayer")

    # connection state
    # 0 connecting, just spam connect messages until one reaches a thumby
    # 1 first player
    # 2 second player
    # 3 connected, exit loop
    connected = 0;    
    first_player = 0
    
    
    thumby.display.fill(0)
    thumby.display.setFont("/lib/font5x7.bin", 5, 7, 1)
    thumby.display.drawText("Connecting", 0, 0, 1)
    thumby.display.update()

    count = 0
    log("Start SyncLoop "+ str(connected))
    while (connected < 3):
        received = thumby.link.receive()
        if received != None:

            # connect message            
            if received[0] == 1:
                # use the smaller speed 
                if speed > received[1]:
                    speed = received[1]
                connected = 1   # got a connect message, so I am now first player
                first_player = 1 # remember that I am first player for player positioning later
                start_time = time.ticks_ms() # remember "now" for countdown 
            # countdown message
            if received[0] == 2:
                # display the number
                number_sprite.setFrame(received[1])
                thumby.display.drawSprite(number_sprite)
                thumby.display.update()
                
                if received[1] == 0:
                    connected = 3  # if countdown = 0 exit waitForPlayer    
                else:
                    connected = 2  # connected as second player
            sending = True # got a message, now I am allowed to send

        if sending:
            if (connected == 0):
                data = bytearray([1,speed])  # not connected yet, just send connect messages with my speed setting
            elif (connected == 1):
                # I am first player, so I send the countdown messages
                diff_seconds = time.ticks_diff(time.ticks_ms(), start_time) // 1000
                count = 3 - diff_seconds
                
                if count <= 0:
                    count = 0
                    connected = 3  # if countdown = 0 exit waitForPlayer    
                data = bytearray([2,count])    
                
                # display the countdown
                number_sprite.setFrame(count)
                thumby.display.drawSprite(number_sprite)
                thumby.display.update()
            else:
                data = bytearray([0]) # second player has connected=2 , nothing to send
                
            if thumby.link.send(data):
                # as soon as one message is received switch to ping pong mode
                if (connected > 0):
                    sending = True

        # check for cancel
        if thumby.buttonU.justPressed():
            connected = 9        
    log("End SyncLoop "+ str(connected))
    
    return connected


loadHighscore() 


log("Start")
while(1):
    
    
  displayMenu()
  if (game_mode == 2):
      try:
          connected = waitForPlayer()  
          if (connected == 3):
              points = playGame()
              displayPoints(points)
              
          
      except Exception as e:
          log(str(e))
            
  else:      
    points = playGame()    
    displayPoints(points)
