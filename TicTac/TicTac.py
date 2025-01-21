# TicTac
# by @angrykoala

import time
import thumby
import random

print("TicTac")
print("by @angrykoala")

single_player=False

# 1 is x
# 2 is o
# 0 is game finished
player_turn=1

# BITMAP: width: 9, height: 9
x_bitmap = bytearray([1,130,68,40,16,40,68,130,1,
           1,0,0,0,0,0,0,0,1])

# BITMAP: width: 9, height: 9
o_bitmap = bytearray([56,198,130,1,1,1,130,198,56,
           0,0,0,1,1,1,0,0,0])

# BITMAP: width: 3, height: 5
arrow_bitmap = bytearray([31,14,4])

thumby.display.setFPS(25)


table=[0,0,0,0,0,0,0,0,0] # From top left to bottom right

selected_square=4 # Center square (beggining from [0,0])
square_size=12

x_padding=18
y_padding=2

flash_speed=800


## Drawing functions

def draw_table():
    total_size=square_size*3
    for i in range(1,3):
        thumby.display.drawLine(x_padding+(square_size*i), y_padding, x_padding+(square_size*i), total_size+y_padding, 1)
        thumby.display.drawLine(x_padding, y_padding+(square_size*i), total_size+x_padding,y_padding+(square_size*i), 1)

def flash_square():
    position=get_position(selected_square)
    thumby.display.drawRectangle(position[0]+1, position[1]+1, square_size-1, square_size-1, 1)

def get_position(square): # Top left corner of the square
    pos_in_table = [(square%3)*square_size, int(square/3)*square_size]
    return [int(pos_in_table[0]+x_padding), pos_in_table[1]+y_padding]

def update_selected_square(value):
    global selected_square
    new_value=selected_square+value
    if new_value>=0 and new_value<=8:
        selected_square=new_value

def draw_players():
    for square, value in enumerate(table):
        position=get_position(square)
        if value==1:
            draw_player(x_bitmap, position)
        if value==2:
             draw_player(o_bitmap, position)

def draw_player(bitmap, position):
    player_sprite_size=9
    thumby.display.blit(bitmap, position[0]+2, position[1]+2, player_sprite_size, player_sprite_size, 0, 0, 0)

def user_input():
    global player_turn
    if thumby.buttonU.justPressed():
        update_selected_square(-3)
    if thumby.buttonD.justPressed():
        update_selected_square(3)
    if thumby.buttonL.justPressed():
        update_selected_square(-1)
    if thumby.buttonR.justPressed():
        update_selected_square(1)

    if thumby.buttonA.justPressed():
        if player_turn==1:
            if table[selected_square]==0:
                table[selected_square]=1
                player_turn=2
                thumby.audio.play(3000, 80)

        if player_turn==2 and single_player==False:
            if table[selected_square]==0:
                table[selected_square]=2
                player_turn=1
                thumby.audio.play(3000, 80)


# AI is completely stupid, any decent ai would lead to a boring, impossible to win game
def ai():
    options=[]
    for square, value in enumerate(table):
        if value==0:
            options.append(square)
    return random.choice(options)

## Game Result Checks

def check_endgame():
    player_1_row=get_3_in_a_row(1)
    if player_1_row!=None:
        draw_3_in_line(player_1_row)
        display_centered("1 Wins", 2, True)
        return 1
    player_2_row=get_3_in_a_row(2)
    if player_2_row!=None:
        draw_3_in_line(player_2_row)
        display_centered("2 Wins", 2, True)
        return 2
    elif is_tie():
        display_centered("Tie", 2, True)
        return 0
    return -1

def is_tie():
    for item in table:
        if item==0:
            return False
    return True

def get_3_in_a_row(player):
    for i in range(3):
        row_i=i*3
        row=[row_i, row_i+1, row_i+2]
        if is_row_completed(row, player): # rows
            return row
        column=[i, i+3, i+6]
        if is_row_completed(column, player): # column
            return column
    return check_diagonals_3_in_a_row(player)

def check_diagonals_3_in_a_row(player):
    diagonal1=[0, 4, 8]
    diagonal2=[2, 4, 6]
    if is_row_completed(diagonal1, player):
        return diagonal1
    if is_row_completed(diagonal2, player):
        return diagonal2
    return None

def is_row_completed(row, player):
    for item in row:
        if table[item]!=player:
            return False
    return True

def draw_3_in_line(row):
    half_square=int(square_size/2)
    source=get_position(row[0])
    target=get_position(row[2])
    thumby.display.drawLine(source[0]+half_square, source[1]+half_square, target[0]+half_square, target[1]+half_square, 1)


def display_centered(text, height, show_square=False):
    font_width=7
    size=len(text)*font_width
    if show_square:
        thumby.display.drawFilledRectangle(12,0,45, 10, 0)
        thumby.display.drawRectangle(11,0,46, 11, 1)
    thumby.display.drawText(text, int((thumby.display.width/2)-(size/2)), height, 1)


## Main Menu
show_main_menu=True
menu_option=1
def main_menu():
    global menu_option
    global show_main_menu
    global single_player
    global player_turn
    display_centered("TIC TAC", 2, False)
    display_centered("by @angrykoala", 12)


    arrow_positon=23
    if menu_option==2:
        arrow_positon=33

    thumby.display.blit(arrow_bitmap, 6,arrow_positon, 3,5, 0, 0, 0)

    thumby.display.drawText("1 Player", 12, 22, 1)
    thumby.display.drawText("2 Players", 12, 32, 1)

    if thumby.buttonU.justPressed():
        menu_option=1
    if thumby.buttonD.justPressed():
        menu_option=2

    if thumby.buttonA.justPressed():
        show_main_menu=False
        if menu_option==1:
            single_player=True
        elif menu_option==2:
            single_player=False

        random.seed(time.ticks_ms())
        player_turn=random.randint(1,2)
        print("Player "+str(player_turn)+" starts")


def main():
    global player_turn
    if player_turn==2 and single_player:
        action=ai()
        table[action]=2
        player_turn=1


    if player_turn!= 0:
        user_input()
        t0 = time.ticks_ms()
        if int(t0/flash_speed)%2==0:
            flash_square()
    draw_table()
    draw_players()

    endgame=check_endgame()
    if endgame!=-1:
        player_turn=0

    if player_turn==0:
        if thumby.buttonA.justPressed():
            return False
    return True


running=True
while(running):
    thumby.display.fill(0) # Fill canvas to black
    if show_main_menu:
        main_menu()
    else:
        running=main()
    thumby.display.update()
