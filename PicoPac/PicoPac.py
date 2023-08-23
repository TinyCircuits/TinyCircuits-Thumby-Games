# Game by Christopher Carson
# https://github.com/ChristopherCarson
# Thanks to Xyvir for updating to new api syntax
# Battery level code by AyreGuitar

import thumby
import time
import machine
import math
import random
from machine import ADC

skip_opening = False

adc = ADC(26)

thumby.saveData.setName("PicoPac")

charging = 38000
level_1 = 33700 #~45min
level_2 = 34300 #~30min
level_3 = 35400 #~15min

# BITMAP: width: 11, height: 5
batt0 = bytearray([31,17,17,17,17,17,17,17,17,27,14])
batt1 = bytearray([31,31,31,31,17,17,17,17,17,27,14])
batt2 = bytearray([31,31,31,31,31,31,31,17,17,27,14])
batt3 = bytearray([31,31,31,31,31,31,31,31,31,31,14])
charg = bytearray([31,31,27,27,9,0,18,27,27,31,14])
emula = bytearray([31,21,17,0,31,2,31,0,31,16,31])

machine.freq(125000000)

def wait(ms):
    last_update = time.ticks_ms()
    while True:
        if time.ticks_ms() - last_update > ms:
            break

# BITMAP: width: 72, height: 40
map_image_1 = bytearray([0,0,0,254,254,254,254,254,254,254,254,254,254,254,254,254,254,254,254,254,254,254,254,254,254,254,254,254,254,254,254,254,254,254,254,254,254,254,254,254,0,0,0,254,254,254,254,254,254,254,254,254,254,254,254,254,254,254,254,254,254,254,254,254,254,254,254,254,254,254,0,0,
            0,0,0,255,255,255,255,255,255,255,0,0,0,255,255,255,255,255,255,255,248,248,248,248,248,248,248,248,248,248,0,0,0,255,255,255,255,255,255,255,248,248,248,255,255,255,255,255,255,255,0,0,0,248,248,248,248,248,248,248,248,248,248,255,255,255,255,255,255,255,248,248,
            224,224,224,255,255,255,255,255,255,255,224,224,224,255,255,255,255,255,255,255,3,3,3,255,255,255,255,255,255,255,224,224,224,255,255,255,255,255,255,255,3,3,3,255,255,255,255,255,255,255,224,224,224,255,255,255,255,255,255,255,3,3,3,255,255,255,255,255,255,255,3,3,
            15,15,15,255,255,255,255,255,255,255,143,143,143,143,143,143,143,143,143,143,128,128,128,143,143,143,143,143,143,143,143,143,143,255,255,255,255,255,255,255,128,128,128,143,143,143,143,143,143,143,143,143,143,255,255,255,255,255,255,255,128,128,128,255,255,255,255,255,255,255,0,0,
            0,0,0,63,63,63,63,63,63,63,63,63,63,63,63,63,63,63,63,63,63,63,63,63,63,63,63,63,63,63,63,63,63,63,63,63,63,63,63,63,63,63,63,63,63,63,63,63,63,63,63,63,63,63,63,63,63,63,63,63,63,63,63,63,63,63,63,63,63,63,0,0])

# BITMAP: width: 72, height: 40
map_image_2 = bytearray([0,0,0,254,254,254,254,254,254,254,254,254,254,254,254,254,254,254,254,254,254,254,254,254,254,254,254,254,254,254,0,0,0,254,254,254,254,254,254,254,254,254,254,254,254,254,254,254,254,254,254,254,254,254,254,254,254,254,254,254,254,254,254,254,254,254,254,254,254,254,0,0,
            0,0,0,255,255,255,255,255,255,255,0,0,0,248,248,248,248,248,248,248,248,248,248,255,255,255,255,255,255,255,0,0,0,255,255,255,255,255,255,255,248,248,248,248,248,248,248,248,248,248,0,0,0,248,248,248,248,248,248,248,248,248,248,255,255,255,255,255,255,255,0,0,
            0,0,0,255,255,255,255,255,255,255,224,224,224,255,255,255,255,255,255,255,3,3,3,255,255,255,255,255,255,255,224,224,224,255,255,255,255,255,255,255,3,3,3,255,255,255,255,255,255,255,224,224,224,255,255,255,255,255,255,255,3,3,3,255,255,255,255,255,255,255,0,0,
            192,192,192,255,255,255,255,255,255,255,143,143,143,143,143,143,143,143,143,143,128,128,128,143,143,143,143,143,143,143,143,143,143,255,255,255,255,255,255,255,0,0,0,255,255,255,255,255,255,255,143,143,143,143,143,143,143,143,143,143,128,128,128,255,255,255,255,255,255,255,128,128,
            63,63,63,63,63,63,63,63,63,63,63,63,63,63,63,63,63,63,63,63,63,63,63,63,63,63,63,63,63,63,63,63,63,63,63,63,63,63,63,63,0,0,0,63,63,63,63,63,63,63,63,63,63,63,63,63,63,63,63,63,63,63,63,63,63,63,63,63,63,63,63,63])

# BITMAP: width: 72, height: 40
map_image_3 = bytearray([0,0,0,254,254,254,254,254,254,254,254,254,254,254,254,254,254,254,254,254,0,0,0,254,254,254,254,254,254,254,254,254,254,254,254,254,254,254,254,254,0,0,0,254,254,254,254,254,254,254,254,254,254,254,254,254,254,254,254,254,254,254,254,254,254,254,254,254,254,254,0,0,
            248,248,248,255,255,255,255,255,255,255,0,0,0,255,255,255,255,255,255,255,248,248,248,255,255,255,255,255,255,255,0,0,0,255,255,255,255,255,255,255,248,248,248,255,255,255,255,255,255,255,248,248,248,248,248,248,248,248,248,248,248,248,248,255,255,255,255,255,255,255,0,0,
            3,3,3,255,255,255,255,255,255,255,224,224,224,227,227,227,227,227,227,227,227,227,227,227,227,227,227,227,227,227,224,224,224,255,255,255,255,255,255,255,3,3,3,227,227,227,227,227,227,227,227,227,227,227,227,227,227,227,227,227,3,3,3,255,255,255,255,255,255,255,224,224,
            0,0,0,255,255,255,255,255,255,255,143,143,143,143,143,143,143,143,143,143,143,143,143,255,255,255,255,255,255,255,15,15,15,255,255,255,255,255,255,255,128,128,128,255,255,255,255,255,255,255,15,15,15,255,255,255,255,255,255,255,128,128,128,255,255,255,255,255,255,255,15,15,
            0,0,0,63,63,63,63,63,63,63,63,63,63,63,63,63,63,63,63,63,63,63,63,63,63,63,63,63,63,63,0,0,0,63,63,63,63,63,63,63,63,63,63,63,63,63,63,63,63,63,0,0,0,63,63,63,63,63,63,63,63,63,63,63,63,63,63,63,63,63,0,0])

maze_images = (map_image_1, map_image_2, map_image_3)
# BITMAP: width: 7, height: 7
pac_image = bytearray([99,65,0,0,0,65,99])
# BITMAP: width: 7, height: 7
pac_image_R = bytearray([99,65,0,8,28,93,127])
# BITMAP: width: 7, height: 7
pac_image_D = bytearray([99,65,112,120,112,65,99])
# BITMAP: width: 7, height: 7
pac_image_L = bytearray([127,93,28,8,0,65,99])
# BITMAP: width: 7, height: 7
pac_image_U = bytearray([99,65,7,15,7,65,99])

# BITMAP: width: 7, height: 7
ghost_D = bytearray([1,64,8,0,72,1,3])
# BITMAP: width: 7, height: 7
ghost_R = bytearray([1,64,4,0,68,1,3])
# BITMAP: width: 7, height: 7
ghost_L = bytearray([3,1,68,0,4,64,1])
# BITMAP: width: 7, height: 7
ghost_U = bytearray([3,1,66,0,2,64,1])

# BITMAP: width: 7, height: 7
ghost_RD_mask = bytearray([126,63,127,127,63,126,124])
# BITMAP: width: 7, height: 7
ghost_LU_mask = bytearray([124,126,63,127,127,63,126])

# BITMAP: width: 15, height: 14
pac_large_1 = bytearray([224,248,252,254,254,255,255,255,255,255,254,254,252,248,224,
            1,7,15,31,31,63,63,63,63,63,31,31,15,7,1])
# BITMAP: width: 15, height: 14
pac_large_2 = bytearray([224,248,252,254,254,255,255,255,127,127,62,62,28,24,0,
            1,7,15,31,31,63,63,63,63,62,30,28,12,0,0])
# BITMAP: width: 5, height: 5
power_ball = bytearray([17,0,4,0,17])
            
player_offset = (3, 1)
last_update = time.ticks_ms()
last_opening_action = time.ticks_ms()
last_ghost_update = time.ticks_ms()

class pico_pac:
    state = 0
    x = 0 + player_offset[0]
    y = 0 + player_offset[1]
    direction = 'R'
    moving = False
    tileX = 0
    tileY = 0

class ghost_class:
    def __init__(self):
        self.scared = False
        self.x = 60 + player_offset[0]
        self.y = 39 + player_offset[1]
        self.direction = 'U'
        self.moving = True
        self.tileX = 0
        self.tileY = 0

# Initialize Global variables
opening_x = None
opening_state = None
player_lives = None
player_score = None
ghost_speed = None
pac = None
ghost_1 = None
ghost_2 = None
ghost_3 = None
ghosts = None
top_row_array = [0,1,1,1,1,1,1,1,1,1,1,1,0]
row_array = [1,1,1,1,1,1,1,1,1,1,1,1,1]
ball_array = None
balls_eaten = None
level = None
power_ball_1 = None
power_ball_2 = None
power_time = None
ghost_state = None
ghost_entering = None
ghost_multiplier = None
extra_life_score = None
maze_index = None

def reset_players():
    global pac, ghost_1, ghost_2, ghost_3, ghosts, ghost_entering, ghost_multiplier
    pac = pico_pac()
    ghost_1 = ghost_class()
    ghost_2 = ghost_class()
    ghost_3 = ghost_class()
    ghost_entering = False
    ghost_multiplier = 0
    if level > 3:
        ghosts = (ghost_1, ghost_2, ghost_3)
    else:
        ghosts = (ghost_1, ghost_2)
    multiplier = 0
    for ghost in ghosts:
        multiplier += 1
        ghost.y += multiplier * 10
    
def reset_balls():
    global ball_array, balls_eaten, power_ball_1, power_ball_2, power_time
    ball_array = [top_row_array.copy()]
    for i in range (0, 5):
        ball_array.append(row_array.copy())
    ball_array.append(top_row_array.copy())
    ball_array[6][12] = 1
    balls_eaten = 0
    power_ball_1 = True
    power_ball_2 = True
    power_time = 0

def init_state():
    global player_lives, player_score, ghost_speed, level, ghost_state, extra_life_score, maze_index
    player_lives = 3
    player_score = 0
    ghost_speed = 70 # The higher, the slower
    level = 1
    reset_players()
    reset_balls()
    ghost_state = 0
    extra_life_score = 5000
    maze_index = 0

init_state()

class maze:
    def __init__(self):
        # These are walls between player tiles.
        self.walls_right = []
        self.walls_down = []
        # These are the side portals in the walls [left-tileY, right-tileY]
        self.walls_portal = []
    
maze_1 = maze()
maze_1.walls_right.append([4])
maze_1.walls_right.append([1, 3, 5])
maze_1.walls_right.append([2, 4, 6])
maze_1.walls_right.append([])
maze_1.walls_down = [[]]
maze_1.walls_down.append([3])
maze_1.walls_down.append([1,3])
maze_1.walls_down.append([])
maze_1.walls_down.append([3])
maze_1.walls_down.append([1])
maze_1.walls_down.append([])
maze_1.walls_portal = [2, 1]
maze_2 = maze()
maze_2.walls_right.append([3])
maze_2.walls_right.append([1, 3, 5])
maze_2.walls_right.append([2, 4, 6])
maze_2.walls_right.append([4])
maze_2.walls_down.append([])
maze_2.walls_down.append([1, 3])
maze_2.walls_down.append([3])
maze_2.walls_down.append([])
maze_2.walls_down.append([1])
maze_2.walls_down.append([1, 3])
maze_2.walls_down.append([])
maze_2.walls_portal = [3, 3]
maze_3 = maze()
maze_3.walls_right.append([2, 4])
maze_3.walls_right.append([1, 3])
maze_3.walls_right.append([4, 6])
maze_3.walls_right.append([3, 5])
maze_3.walls_down.append([])
maze_3.walls_down.append([2, 3])
maze_3.walls_down.append([2])
maze_3.walls_down.append([])
maze_3.walls_down.append([2])
maze_3.walls_down.append([1, 2])
maze_3.walls_down.append([])
maze_3.walls_portal = [1, 2]
mazes = (maze_1, maze_2, maze_3)

def getcharinputNew():
    if(thumby.buttonL.justPressed()):
        return 'L'
    if(thumby.buttonR.justPressed()):
        return 'R'
    if(thumby.buttonU.justPressed()):
        return 'U'
    if(thumby.buttonD.justPressed()):
        return 'D'
    if(thumby.buttonA.justPressed()):
        return '1'
    if(thumby.buttonB.justPressed()):
        return '2'
    return ' '

def display_battery():
    iconx = 61
    icony = 0
    iconw = 11
    iconh = 5
    black_background_offset = 4
    b=charging
    thumby.display.drawFilledRectangle(iconx-black_background_offset, 0, iconw+black_background_offset, iconh+black_background_offset, 0)
    in_emu=not hasattr(thumby.display.display,"cs")
    if (in_emu):
        thumby.display.blit(emula,iconx,icony,iconw,iconh,-1,0,0)
    else:
        v=adc.read_u16()
        b=min(b,v)
        if (v > charging):
            thumby.display.blit(charg,iconx,icony,iconw,iconh,-1,0,0)
            b=v
        else:
            if (b > level_3):
                thumby.display.blit(batt3,iconx,icony,iconw,iconh,-1,0,0)
            elif (b > level_2):
                thumby.display.blit(batt2,iconx,icony,iconw,iconh,-1,0,0)
            elif (b > level_1):
                thumby.display.blit(batt1,iconx,icony,iconw,iconh,-1,0,0)
            else:
                thumby.display.blit(batt0,iconx,icony,iconw,iconh,-1,0,0)

def check_ghost_turn(ghost):
    if ((ghost.x - player_offset[0]) % 10 == 0) and ((ghost.y - player_offset[1]) % 10 == 0) and ghost.y < 39:
        updated = False
        while updated == False:
            r = random.randint(0, 4)
            direction = 'U'
            if r == 1:
                direction = 'R'
            elif r == 2:
                direction = 'D'
            elif r == 3:
                direction = 'L'
            update_player_tile(ghost, direction, ghost.x, ghost.y)
            if check_valid_tile(ghost, direction) and not check_opposite_direction(ghost.direction, direction):
                ghost.direction = direction
                updated = True

def check_opposite_direction(d1, d2):
    if d1 == 'U' and d2 == 'D':
        return True
    elif d1 == 'D' and d2 == 'U':
        return True
    elif d1 == 'R' and d2 == 'L':
        return True
    elif d1 == 'L' and d2 == 'R':
        return True
    else:
        return False

def check_y_turn(direction):
    v = pac.x % 10
    if (v < 7):
        check_x =(math.floor(pac.x/10) * 10) + player_offset[0]
        update_player_tile(pac, direction, check_x, pac.y)
        if (check_valid_tile(pac, direction) == True):
            pac.x = check_x
            return True
    return False

def check_x_turn(direction):
    v = pac.y % 10
    if (v > 5):
        check_y =(math.ceil(pac.y/10) * 10) + player_offset[1]
        update_player_tile(pac, direction, pac.x, check_y)
        if (check_valid_tile(pac, direction) == True):
            pac.y = check_y
            return True
    if ( v < 5):
        check_y =(math.floor(pac.y/10) * 10) + player_offset[1]
        update_player_tile(pac, direction, pac.x, check_y)
        if (check_valid_tile(pac, direction) == True):
            pac.y = check_y
            return True
    return False
    
def check_valid_tile(player, direction):
    offset = 1
    if (direction == 'R'):
        if (player.tileX + offset == 7 and player.tileY == mazes[maze_index].walls_portal[1]):
            return True
        if (player.tileX + offset in mazes[maze_index].walls_right[player.tileY] or (player.tileX == 6 and player.tileY != mazes[maze_index].walls_portal[1])):
            return False
    elif (direction == 'L'):
        if (player.tileX + offset == -1 and player.tileY == mazes[maze_index].walls_portal[0]):
            return True
        if (player.tileX + offset in mazes[maze_index].walls_right[player.tileY] or (player.tileX == -1 and player.tileY != mazes[maze_index].walls_portal[0])):
            return False
    elif (direction == 'U'):
        if (player.tileY + offset in mazes[maze_index].walls_down[player.tileX] or player.tileY == -1):
            return False
    elif (direction == 'D'):
        if (player.tileY + offset in mazes[maze_index].walls_down[player.tileX] or player.tileY == 3):
            return False
    return True
        
def update_player_tile(player, direction, x, y):
    player.tileX = math.floor(x/10)
    player.tileY = math.floor(y/10)
    if (direction == 'R'):
        player.tileX = math.floor((x-3)/10)
    elif (direction == 'L'):
        player.tileX = math.floor((x-4)/10)
    elif (direction == 'U'):
        player.tileY = math.floor((y-2)/10)
    elif (direction == 'D'):
        player.tileY = math.floor((y-1)/10)
        
def move(player):
    if (player.moving == True):
        if (player.direction == 'R'):
            player.x += 1
        elif (player.direction == 'L'):
            player.x -= 1
        elif (player.direction == 'U'):
            player.y -= 1
        elif (player.direction == 'D'):
            player.y += 1
        
def portal_transport(player):
    if player.x < -2:
        player.x = 68
        player.y = 10 * mazes[maze_index].walls_portal[1] + player_offset[1]
        player.direction = 'L'
    if player.x > 68:
        player.x = -2
        player.y = 10 * mazes[maze_index].walls_portal[0] + player_offset[1]
        player.direction = 'R'

def display_ghost(ghost):
    if power_time == 0 or (power_time > 40 and ghost_state % 2 == 0) or (power_time < 41 and ghost_state < 9):
        if (ghost.direction == 'R'):
            thumby.display.blitWithMask(ghost_R, ghost.x, ghost.y, 7, 7,-1,0,0, ghost_RD_mask)
        elif (ghost.direction == 'L'):
            thumby.display.blitWithMask(ghost_L, ghost.x, ghost.y, 7, 7,-1,0,0, ghost_LU_mask)
        elif (ghost.direction == 'U'):
            thumby.display.blitWithMask(ghost_U, ghost.x, ghost.y, 7, 7,-1,0,0, ghost_LU_mask)
        elif (ghost.direction == 'D'):
            thumby.display.blitWithMask(ghost_D, ghost.x, ghost.y, 7, 7,-1,0,0, ghost_RD_mask)

def display_pac():
    if (pac.state == 0 and pac.moving == True):
        thumby.display.blit(pac_image, pac.x, pac.y, 7, 7,-1,0,0)
    else:
        if (pac.direction == 'R'):
            thumby.display.blit(pac_image_R, pac.x, pac.y, 7, 7,1,0,0)
        elif (pac.direction == 'L'):
            thumby.display.blit(pac_image_L, pac.x, pac.y, 7, 7,1,0,0)
        elif (pac.direction == 'U'):
            thumby.display.blit(pac_image_U, pac.x, pac.y, 7, 7,1,0,0)
        elif (pac.direction == 'D'):
            thumby.display.blit(pac_image_D, pac.x, pac.y, 7, 7,1,0,0)

def check_collision(ghost):
    if abs(pac.x - ghost.x) < 5 and abs(pac.y - ghost.y) < 5:
        return True
    return False

def display_lives():
    x = 8
    for i in range(0, player_lives):
        if i < 2:
            thumby.display.blit(pac_large_2, x, 20, 15, 14,-1,0,0)
        else:
            if player_lives == 3:
                thumby.display.blit(pac_large_2, x, 20, 15, 14,-1,0,0)
            else:
                thumby.display.drawText(f"+{player_lives - 2}", x-3, 25, 1)
                break
        x = x + 20
        
def show_level():
    opening_scene()
    thumby.display.fill(0)
    display_score()
    thumby.display.drawText(f"Level:{level}", 10, 25, 1)
    thumby.display.update()
    wait(2000)
    show_score()
    
def show_score():
    global last_update
    last_update = time.ticks_ms()
    thumby.display.fill(0)
    if player_score == 0:
        thumby.display.drawText("Start", 23, 2, 1)
    else:
        display_score()
    display_lives()
    thumby.display.update()
    wait(2000)

def press_to_start():
    thumby.display.drawText("A: Play", 19, 12, 1)
    thumby.display.drawText("B: Exit", 19, 22, 1)
    thumby.display.drawText("v1.1", 50, 32, 1)
    thumby.display.update()
    character = ' '
    show_pac(-2)
    while True:
        if thumby.buttonB.pressed():
            thumby.reset()
        if thumby.buttonA.pressed():
            break

def display_score():
    thumby.display.drawText(f"Score:{player_score}", 1, 2, 1)

def game_over():
    last_update = time.ticks_ms()
    highScore = 0
    thumby.display.fill(0)
    if (thumby.saveData.hasItem("highscore")):
        highScore = int(thumby.saveData.getItem("highscore"))
    if(player_score > highScore):
        thumby.saveData.setItem("highscore", player_score)
        highScore = player_score
    thumby.saveData.save()
    display_score()
    thumby.display.drawText(f"HiScr:{highScore}", 1, 15, 1)
    thumby.display.drawText("GAME OVER", 8, 28, 1)
    thumby.display.update()
    while(True):
        if thumby.buttonA.pressed() or thumby.buttonB.pressed():
            break
    thumby.display.fill(0)
    display_title()
    press_to_start()

def get_input():
    key = getcharinputNew()
    if key == '1':
        thumby.display.drawFilledRectangle(22, 13, 35, 13, 0)
        thumby.display.drawText("PAUSE", 25, 16, 1)
        display_battery()
        thumby.display.update()
        wait(200)
        while True:
            key = getcharinputNew()
            if key == '1':
                break
    if pac.x > 0 and pac.x < 66:
        if key == 'L':
            if (check_x_turn('L') == True):
                pac.moving = True
                pac.direction = 'L'
        if key == 'R':
            if (check_x_turn('R') == True):
                    pac.moving = True
                    pac.direction = 'R'
        if key == 'U':
            if (check_y_turn('U') == True):
                    pac.moving = True
                    pac.direction = 'U'
        if key == 'D':
            if (check_y_turn('D') == True):
                    pac.moving = True
                    pac.direction = 'D'

def eat_balls():
    global ball_array, player_score, balls_eaten
    x = 0
    y = -1
    array_x = -1
    array_y = -1
    for b in ball_array:
        array_y += 1
        y += 5
        for bb in b:
            array_x += 1
            x += 5
            if bb == 1:
                if abs(pac.x + 3 - x) < 3 and abs(pac.y + 2 - y) < 3:
                    ball_array[array_y][array_x] = 0
                    player_score += 10
                    balls_eaten += 1
                    thumby.audio.play(349, 50)
                else:
                    thumby.display.drawFilledRectangle(x, y, 2, 2, 0)
        x = 0
        array_x = -1
        
def eat_power_balls():
    global power_time, power_ball_1, power_ball_2
    p_time = 150
    if power_ball_1 == True:
        if abs(pac.x + 2 - 4) < 4 and abs(pac.y + 2 - 32) < 4:
            power_ball_1 = False
            power_time = p_time
            thumby.audio.play(349, 50)
    if power_ball_2 == True:
        if abs(pac.x + 2 - 63) < 4 and abs(pac.y + 2 - 2) < 4:
            power_ball_2 = False
            power_time = p_time
            thumby.audio.play(349, 50)

def display_ghost_bonus(bonus):
    thumby.display.drawFilledRectangle(27, 13, 22, 13, 0)
    thumby.display.drawText(f"{bonus}", 29, 16, 1)
    thumby.display.update()
    wait(1000)
    
def update_display():
    thumby.display.blit(maze_images[maze_index], 0, 0, 72, 40,-1,0,0)
    display_pac()

    eat_balls()
    eat_power_balls()

    for ghost in ghosts:
        display_ghost(ghost)

    if power_ball_1 == True:
        thumby.display.blit(power_ball, 4, 32, 5, 5,1,0,0)
    if power_ball_2 == True:
        thumby.display.blit(power_ball, 63, 2, 5, 5,1,0,0)
    if ghost_entering == True and power_time == 0:
        if pac.state == 0:
            thumby.display.drawFilledRectangle(60, 38, 10, 2, 1)

    thumby.display.update()
    
def display_title():
    thumby.display.setFont("/lib/font8x8.bin", 8, 8, 1)
    thumby.display.drawText("Pico Pac", 1, 1, 1)
    thumby.display.setFont("/lib/font5x7.bin", 5, 7, 1)

def opening_scene():
    thumby.display.fill(0)
    thumby.display.update()
    if level == 1:
        display_title()
    else:
        display_score()
    show_pac(85)

def show_pac(ending_x):
    last_update = time.ticks_ms()
    global opening_x, opening_state, last_opening_action
    opening_state = 1
    opening_x = -50
    while True:
        if time.ticks_ms() - last_opening_action > 50:
            thumby.display.drawFilledRectangle(opening_x, 19, 15, 16, 0)
            opening_x = opening_x + 3
            if opening_state == 0:
                opening_state = 1
                thumby.display.blit(pac_large_1, opening_x, 20, 15, 14, 0, 0 ,0)
            else:
                opening_state = 0
                thumby.display.blit(pac_large_2, opening_x, 20, 15, 14, 0, 0, 0)
            thumby.display.update()
            last_opening_action = time.ticks_ms()
        if opening_x > ending_x:
            thumby.display.drawFilledRectangle(opening_x, 19, 15, 16, 0)
            thumby.display.blit(pac_large_2, opening_x, 20, 15, 14, 0, 0, 0)
            thumby.display.update()
            break

def opening_music():
    thumby.audio.play(392, 200)
    wait(200)
    thumby.audio.play(440, 200)
    wait(200)
    thumby.audio.play(494, 200)
    wait(200)
    thumby.audio.play(548, 500)
    wait(500)
    
def eat_ghosts_sound():
    thumby.audio.play(392, 50)
    wait(50)
    thumby.audio.play(440, 50)
    wait(50)
    thumby.audio.play(494, 50)
    wait(50)
    thumby.audio.play(440, 50)
    wait(50)
    thumby.audio.play(392, 50)
    wait(50)
    
if skip_opening == False:
    opening_scene()
    press_to_start()
    show_score()
    update_display()
    opening_music()

# main game loop
while True:
    # move ghosts
    ghost_entering = False
    current_ghost_speed = ghost_speed
    if power_time > 0:
        current_ghost_speed = 140
    if time.ticks_ms() - last_ghost_update > current_ghost_speed:
        for ghost in ghosts:
            # Keep eaten ghosts out until power time is over
            if power_time > 0 and ghost.y > 45:
                # use random number to keep ghosts from clumping together
                ghost.y = 45 + random.randint(5, 25)
            move(ghost)
            check_ghost_turn(ghost)
            portal_transport(ghost)
        last_ghost_update = time.ticks_ms()
    
    # move pac
    if time.ticks_ms() - last_update > 50:
        ghost_state += 1
        if ghost_state > 10:
            ghost_state = 0
        if pac.state == 1:
            pac.state = 0
        else:
            pac.state = 1
            
        if power_time > 0:
            power_time -= 1
        else:
            ghost_multiplier = 0
        
        get_input()
        move(pac)
        
        if (balls_eaten > 57 and maze_index == 0) or  (balls_eaten > 55 and maze_index > 0):
            wait(1000)
            level += 1
            maze_index += 1
            if maze_index > 2:
                maze_index = 0
            if ghost_speed > 30:
                ghost_speed -= 5
            show_level()
            reset_players()
            reset_balls()
            update_display()
            opening_music()

        portal_transport(pac)
        
        update_player_tile(pac, pac.direction, pac.x, pac.y)
        if (check_valid_tile(pac, pac.direction) == False):
            pac.moving = False
        
        for ghost in ghosts:
            if ghost.y > 35:
                ghost_entering = True
            if check_collision(ghost) == True:
                if power_time > 0:
                    eat_ghosts_sound()
                    ghost_multiplier += 1
                    display_ghost_bonus(100 * (2 ** ghost_multiplier))
                    player_score += 100 * (2 ** ghost_multiplier)
                    ghost.x = 60 + player_offset[0]
                    ghost.y = 50
                    ghost.direction = 'U'
                else:
                    thumby.audio.play(548, 200)
                    wait(200)
                    thumby.audio.play(494, 200)
                    wait(200)
                    thumby.audio.play(440, 200)
                    wait(200)
                    thumby.audio.play(392, 500)
                    wait(500)
                    reset_players()
                    player_lives = player_lives - 1
                    if player_lives == 0:
                        game_over()
                        init_state()
                        show_score()
                    else:
                        show_score()
                    break
        
        if player_score > extra_life_score:
            display_ghost_bonus('1UP')
            player_lives += 1
            extra_life_score += 5000
            
        last_update = time.ticks_ms()
        update_display()
