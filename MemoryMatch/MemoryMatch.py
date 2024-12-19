import time
import thumby
import random

print("Memory Match")
print("by @TezFraser")

game_started = False


is_first_selection = True
last_selection = 0
show_main_menu = True
show_win = False


# BITMAP: width: 9, height: 9
questionMark = bytearray([0, 0, 4, 2, 178, 10, 4, 0, 0,
           0, 0, 0, 0, 0, 0, 0, 0, 0])

# BITMAP: width: 9, height: 9 CIRCLE
circle = bytearray([0, 56, 124, 254, 254, 254, 124, 56, 0,
           0, 0, 0, 0, 0, 0, 0, 0, 0])

# BITMAP: width: 9, height: 9 Square
squareShape = bytearray([0,254,254,254,254,254,254,254,0,
           0,0,0,0,0,0,0,0,0])
           
# BITMAP: width: 9, height: 9
quadSquare = bytearray([0,254,146,146,254,146,146,254,0,
           0,0,0,0,0,0,0,0,0])

# BITMAP: width: 9, height: 9 diamond
diamond = bytearray([0, 16, 56, 124, 254, 124, 56, 16, 0,
           0, 0, 0, 0, 0, 0, 0, 0, 0])

# BITMAP: width: 9, height: 9
cross = bytearray([0, 56, 56, 254, 254, 254, 56, 56, 0,
           0, 0, 0, 0, 0, 0, 0, 0, 0])

# BITMAP: width: 9, height: 9 Unused 
arrowUp = bytearray([0, 16, 24, 252, 254, 252, 24, 16, 0,
            0, 0, 0, 0, 0, 0, 0, 0, 0])

# BITMAP: width: 9, height: 9
heart = bytearray([0, 28, 62, 124, 248, 124, 62, 28, 0,
            0, 0, 0, 0, 0, 0, 0, 0, 0])

# BITMAP: width: 9, height: 9
arrowRight = bytearray([0, 56, 56, 56, 254, 124, 56, 16, 0,
            0, 0, 0, 0, 0, 0, 0, 0, 0])

# BITMAP: width: 3, height: 5 small select arrow
#arrow_bitmap = bytearray([31, 14, 4])

thumby.display.setFPS(25)

# Updated table for 4x3 grid (4 columns, 3 rows)
table = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]  # 4x3 grid

check_table = [1, 2, 3, 4, 5, 6, 1, 2, 3, 4, 5, 6] 

selected_square = 0  # Top left
square_size = 12

x_padding = 10
y_padding = 2

## Drawing functions

def draw_selection():
    position = get_position(selected_square)
    thumby.display.drawRectangle(position[0] + 1, position[1] + 1, square_size - 1, square_size - 1, 1)

def get_position(square):  # Top left corner of the square
    pos_in_table = [(square % 4) * square_size, int(square / 4) * square_size]  # Adjusted for 4 columns
    return [int(pos_in_table[0] + x_padding), pos_in_table[1] + y_padding]

def update_selected_square(value):
    global selected_square
    new_value = selected_square + value
    if new_value >= 0 and new_value < len(table):
        selected_square = new_value

def draw_players():
    for square, value in enumerate(table):
        position = get_position(square)
        if value == 1:
            draw_player(circle, position)
        elif value == 2:
            draw_player(quadSquare, position)
        elif value == 3:
            draw_player(diamond,position)
        elif value == 4:
            draw_player(cross,position)
        elif value == 5:
            draw_player(arrowRight,position)
        elif value == 6:
            draw_player(heart,position)
        else:
            draw_player(questionMark,position)

def draw_player(bitmap, position):
    player_sprite_size = 9
    thumby.display.blit(bitmap, position[0] + 2, position[1] + 2, player_sprite_size, player_sprite_size, 0, 0, 0)

def user_input():
    global is_first_selection
    global last_selection
    if thumby.buttonU.justPressed():
        update_selected_square(-4)  # Move up (4 columns)
    if thumby.buttonD.justPressed():
        update_selected_square(4)  # Move down (4 columns)
    if thumby.buttonL.justPressed():
        update_selected_square(-1)  # Move left
    if thumby.buttonR.justPressed():
        update_selected_square(1)  # Move right

    if thumby.buttonA.justPressed():
        if table[selected_square] == 0:
            thumby.audio.play(3000, 80)
            if is_first_selection:
                is_first_selection = False
                table[selected_square] = check_table[selected_square]
                #Uncomment if debugging
                #print(table[selected_square])
                last_selection = selected_square
            else:
                if table[last_selection] == check_table[selected_square]:
                    table[selected_square] = check_table[selected_square]
                    last_selection = -1
                    is_first_selection = True
                else:
                    table[selected_square] = check_table[selected_square]
                    full_display_update()
                    time.sleep(2)
                    table[selected_square] = 0
                    table[last_selection] = 0
                    is_first_selection = True
                    last_selection = -1

                    


## Game Result Checks

def check_endgame():
    isValid = True
    for i in range(len(table)):
        if(check_table[i] != table[i]):
            isValid = False
    return isValid

    
def decideOrder():
    random.seed(time.ticks_ms())
    global game_started
    global check_table
    #Random shuffle wasn't working so we rigged something together
    for j in range(10):
        newTable = []
        for i in range(12):
            if(len(check_table) > 0):
                newTable.append(check_table.pop(random.randint(0, 11-i)))
        check_table = newTable
    #Uncomment if debugging
    #print(check_table)
    game_started = True
    
def full_display_update():
    thumby.display.fill(0)
    draw_players()
    draw_selection()
    thumby.display.update()

def draw_mainmenu():
    global show_main_menu
    thumby.display.fill(0)
    thumby.display.setFont("/lib/font5x7.bin", 5, 7, 1)
    thumby.display.drawText("MEMORY", 18, 1, 1)
    thumby.display.drawText("MATCH!", 18, 10, 1)

    thumby.display.setFont("/lib/font3x5.bin", 3, 5, 1)
    thumby.display.drawText("PRESS A OR B", 10, 32, 1)
    thumby.display.drawText("By: @TezFraser", 10, 20, 1)
    anyButton = thumby.buttonA.justPressed() or thumby.buttonB.justPressed()

    if anyButton:
        show_main_menu=False
    
def draw_win():
    global show_win
    thumby.display.fill(0)
    thumby.display.setFont("/lib/font8x8.bin", 8, 8, 1)
    thumby.display.drawText("YOU", 20, 10, 1)
    thumby.display.drawText("WIN!", 18, 19, 1)
    thumby.display.update()
    time.sleep(3)
    show_win = False



# Main loop
while True:
    thumby.display.fill(0)
    if show_main_menu:
        draw_mainmenu()
        
    elif show_win:
        draw_win()
    else:
        if not game_started:
            decideOrder()
        full_display_update()
        user_input()
    
        game_result = check_endgame()
        if game_result:
            full_display_update()
            time.sleep(1)
            show_win = True
            draw_win()
            decideOrder()
            table = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]  # Reset grid
            is_first_selection = True  # Reset player turn
            last_selection = -1
            selected_square = 0
    
    thumby.display.update()
    time.sleep(0.1)
