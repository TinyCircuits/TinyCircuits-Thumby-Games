# snake by kari
# this is just a simple version of classic game snake i made for a video i shared over on my youtube channel
# if you want to learn more on how i made this and the game logic, check out my video here ---> https://youtu.be/iz1wbxlsdkQ

import thumby, random

titlescreen = bytearray([0,0,0,0,0,0,0,0,0,128,128,128,0,128,192,64,64,192,128,0,0,192,192,128,0,192,192,0,0,128,192,64,64,192,128,0,0,192,192,0,128,192,64,0,0,192,192,64,64,64,64,0,128,128,192,224,224,240,240,240,240,152,184,144,240,224,160,192,192,0,0,0,
    0,4,12,8,12,6,6,3,3,7,15,15,0,9,27,18,18,30,12,0,0,31,31,1,3,31,31,0,0,31,31,2,2,31,31,0,0,31,31,7,13,24,16,0,0,31,31,18,18,18,16,0,15,15,15,7,3,3,3,7,15,14,28,24,27,24,11,4,2,2,4,0,
    0,0,0,0,0,0,0,0,56,254,254,135,219,219,135,254,254,56,0,0,0,0,124,36,36,24,0,124,64,64,64,0,120,36,36,120,0,12,80,80,60,0,0,0,56,68,84,116,0,120,36,36,120,0,124,8,16,8,124,0,124,84,84,68,0,0,0,0,0,0,0,0,
    0,0,0,0,0,0,0,0,128,224,224,49,177,177,113,224,224,128,0,0,0,0,128,64,64,128,0,192,0,0,192,0,64,192,64,0,64,192,64,0,0,0,128,64,64,64,0,128,64,64,128,0,192,128,0,128,192,0,192,64,64,64,0,0,0,0,0,0,0,0,0,0,
    0,0,0,0,0,0,0,0,3,15,15,24,26,26,29,15,15,3,0,0,0,0,3,4,4,11,0,3,4,4,3,0,4,7,4,0,0,7,0,0,0,0,3,4,5,7,0,7,2,2,7,0,7,0,1,0,7,0,7,5,5,4,0,0,0,0,0,0,0,0,0,0])
titlescreenSpr = thumby.Sprite(72, 40, titlescreen, 0, 0)

gameoverscreen = bytearray([0,0,0,0,0,0,0,0,0,0,0,240,8,4,4,228,20,84,212,4,228,148,148,228,4,244,36,68,36,244,4,244,84,84,20,4,4,4,228,20,20,228,4,244,4,4,244,4,244,84,84,20,4,244,148,148,100,4,4,8,240,0,0,0,0,0,0,0,0,0,0,0,
    0,0,0,0,0,0,0,0,0,0,0,1,2,4,4,4,5,5,5,4,5,4,4,5,4,5,4,4,4,5,4,5,5,5,5,4,4,4,4,5,5,4,4,4,5,5,4,4,5,5,5,5,4,5,4,4,5,4,4,2,1,0,0,0,0,0,0,0,0,0,0,0,
    0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,128,128,192,192,192,192,128,128,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,
    0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,31,9,9,6,0,31,9,9,22,0,31,21,21,17,0,18,21,21,9,0,18,21,21,9,0,0,0,0,14,63,63,97,118,118,97,63,63,14,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,
    0,0,0,0,0,0,0,0,0,0,0,2,62,2,0,28,34,34,28,0,0,0,28,34,34,34,0,28,34,34,28,0,62,4,8,16,62,0,2,62,2,0,34,62,34,0,62,4,8,16,62,0,30,32,32,30,0,62,42,42,34,0,0,0,0,0,0,0,0,0,0,0])
gameoverscreenSpr = thumby.Sprite(72, 40, gameoverscreen, 0, 0)


def new_food():
    while(1):
        food_x = random.randint(0,(playing_area_width-1))
        food_y = random.randint(0,(playing_area_height-1))
        if playing_area[food_y][food_x] == 1 or food_x == snake_x and food_y == snake_y:
            pass
        else:
            break
    playing_area[food_y][food_x] = 2
    return(food_x, food_y)

while(1):

    # title
    thumby.display.fill(0) # clear screen
    thumby.display.drawSprite(titlescreenSpr)
    if(thumby.buttonA.justPressed()):

        # game loop
        while(1):
            
            # intialise game variables
            playing_area_width = 70
            playing_area_height = 32
            playing_area = [[0 for i in range(playing_area_width)] for j in range(playing_area_height)] # row, col
            speed = 5
            score = 0
            xdir = [-1, 0, 1, 0]
            ydir = [0, -1, 0, 1]
            key = 2
            snake_x = 35
            snake_y = 16
            snake_len = 10
            snake_dir = 2
            snake_body = [[snake_x, snake_y]] # array to hold snake body coordinates
            playing_area[snake_y][snake_x] = 1
            (food_x, food_y) = new_food()
            
            while(1):
                
                # draw screen
                thumby.display.setFPS(speed)
                thumby.display.fill(0) # clear screen
                thumby.display.drawRectangle(0, 6, 72, 34, 1) # draw border
                thumby.display.setFont("/lib/font3x5.bin", 3, 5, 1)
                thumby.display.drawText('score: ' + str(score), 0, 0, 1) # draw score
                for i in range(len(snake_body)): # draw snake
                    thumby.display.setPixel(snake_body[i][0] + 1, snake_body[i][1] + 7 , 1) # x, y, color
                thumby.display.setPixel(food_x + 1, food_y + 7, 1) # draw food
                thumby.display.update()
                
                # game logic
                snake_x += xdir[snake_dir]; snake_y += ydir[snake_dir] # move snake
                # wall and snake collision detection
                if snake_x > -1 and snake_x < playing_area_width and snake_y > -1 and snake_y < playing_area_height and playing_area[snake_y][snake_x] != 1:
                    # food collision detection
                    if playing_area[snake_y][snake_x] == 2: # eat food
                        #thumby.audio.playBlocking(2500, 250)
                        (food_x, food_y) = new_food() # generate new food
                        snake_len += 5 # increase snake length
                        speed += 1 # increase snake speed
                        score += 1 # increase score
                    
                    playing_area[snake_y][snake_x] = 1
                    snake_body.append([snake_x,snake_y]) # add to end
                    # check snake length
                    if len(snake_body) > snake_len:
                        playing_area[snake_body[0][1]][snake_body[0][0]] = 0
                        snake_body.pop(0) # remove first element
                else:
                    break # game over

                # detect key press
                if thumby.buttonU.justPressed(): # up
                    key = 1
                if thumby.buttonD.justPressed(): # down
                    key = 3
                if thumby.buttonL.justPressed(): # left
                    key = 0
                if thumby.buttonR.justPressed(): # right
                    key = 2
                if key % 2 != snake_dir % 2:
                    snake_dir = key # change direction of snake

            break

        # game over
        while(1):
            thumby.display.fill(0) # clear screen
            thumby.display.drawSprite(gameoverscreenSpr)
            thumby.display.setFont("/lib/font3x5.bin", 3, 5, 1)
            thumby.display.drawText('score: ' + str(score), 21, 14, 1) # draw score
            if(thumby.buttonA.justPressed()):
                break;
            thumby.display.update()
    
    if(thumby.buttonB.justPressed()): # quit game
        thumby.reset()

    thumby.display.update()