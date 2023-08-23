# learning micropython using microprocessor
# this program will select a random card from a virtual 52 card deck
# the user is able to select Red or Black using the B (red) or A (black) key
# the user is able to select a suit using the directional keys
#
# guess black or red using A-B buttons
# button A = Black
# button B = Red
#
# guess suits using direction pad
# up = Spade
# down = Heart
# right = Club 
# left = Diamond
#
# history of the last 5 cards will be displayed along the top
# there are reminds on screen of what the keys represent
#
# pressing both A + L keys together will reset the deck, history and score
# pressing the B + U keys together will cycle the number of decks used 1, 4 or 6
#
# this is the rewrite of the code. made the history section larger so they can been on the tiny screen
#
# // todo
#
# 
# 

import thumby
import random
import time
import machine

# need this to seed the random function
random.seed(time.ticks_us()) # Relies on minor inconsistencies to differ a little each time


# bitmap information

# BITMAP: width: 72, height: 40
title_spritemap = bytearray([255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,31,31,223,223,223,223,207,207,207,239,239,239,239,15,255,255,255,31,199,247,231,239,239,207,223,223,159,191,63,63,127,127,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,
           255,255,255,255,255,255,255,255,255,255,255,255,127,127,63,63,159,223,207,231,231,243,192,0,63,255,255,159,15,39,19,39,15,159,255,252,0,195,240,254,135,3,19,67,15,39,135,199,255,127,15,129,204,159,159,63,127,127,255,255,255,255,255,255,255,255,255,255,255,255,255,255,
           255,255,255,255,255,255,255,255,255,255,113,32,134,206,223,223,95,95,131,179,131,11,195,255,128,7,127,127,123,57,56,56,57,59,39,32,14,31,159,223,223,223,28,60,126,255,127,15,97,96,22,7,147,171,3,255,127,62,140,225,241,255,255,255,255,255,255,255,255,255,255,255,
           255,255,255,255,255,255,255,255,255,48,166,15,31,63,63,60,120,248,248,241,225,192,24,1,9,253,253,253,1,0,240,0,252,252,252,0,0,224,8,28,252,252,252,0,2,132,4,254,254,255,255,4,5,133,225,1,16,121,125,229,197,197,141,137,67,223,255,255,255,255,255,255,
           255,255,255,255,255,255,255,255,255,248,249,243,246,228,228,228,228,231,231,227,241,240,248,255,248,243,247,231,230,228,244,246,247,231,231,230,224,241,244,230,231,231,231,228,224,247,248,241,247,231,231,230,228,226,240,248,242,228,228,228,231,231,231,227,240,249,255,255,255,255,255,255])

suits_title_Spr = thumby.Sprite(72, 40, title_spritemap, 0, 0)
thumby.display.drawSprite(suits_title_Spr)
thumby.display.update()

show_title = True

def get_user_input():
    if(thumby.buttonL.justPressed()):
        return 'Diamond-L'
    if(thumby.buttonR.justPressed()):
        return 'Club-R'
    if(thumby.buttonU.justPressed()):
        return 'Spade-U'
    if(thumby.buttonD.justPressed()):
        return 'Heart-D'
    if(thumby.buttonA.justPressed()):
        return 'Black-A'
    if(thumby.buttonB.justPressed()):
        return 'Red-B'
    return ' '

while show_title:
    
    c = get_user_input()
    any_button_is_pressed = c != ' '
    
    if any_button_is_pressed:
        show_title = False
        break
    
# sprites to use for the history 0:blank 1:spade 2:heart 3:club 4:diamond
# 11x13 for 5 frames  
suit_spritemap = bytearray([255,1,1,1,1,1,1,1,1,1,255,31,16,16,16,16,16,16,16,16,16,31,159,15,7,3,1,0,1,3,7,15,159,31,31,30,22,19,16,19,22,30,31,31,124,254,255,255,254,252,254,255,255,254,124,0,0,1,3,7,15,7,3,1,0,0,255,15,15,25,48,0,48,25,15,15,255,31,28,28,22,19,16,19,22,28,28,31,96,240,248,252,254,255,254,252,248,240,96,0,0,1,3,7,15,7,3,1,0,0])

# indicator 0:blank 1:tick 2:cross 3:end
# 16x13 for 4 frames
indicate_spritemap = bytearray([255,1,253,5,245,21,85,85,85,85,21,245,5,253,1,255,31,16,23,20,21,21,21,21,21,21,21,21,20,23,16,31,255,1,129,129,1,1,1,1,1,129,193,97,49,25,1,255,31,16,16,17,19,22,20,22,19,17,16,16,16,16,16,31,255,1,1,5,13,25,177,225,225,177,25,13,5,1,1,255,31,16,16,20,22,19,17,16,16,17,19,22,20,16,16,31,255,1,241,81,81,17,1,193,65,193,1,193,65,241,1,255,31,16,17,17,17,17,16,17,16,17,16,17,17,17,16,31])

# score text and the border box for the score
# BITMAP: width: 22, height: 20
score_bitmap = bytearray([38,73,73,50,0,48,72,72,0,48,72,72,48,0,112,8,16,0,56,84,84,72,
           254,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,254,0,
           15,8,8,8,8,8,8,8,8,8,8,8,8,8,8,8,8,8,8,8,15,0])

# informaton icon so users can see what each suit is represented by the direction
# BITMAP: width: 25, height: 25
#suitsInfo_bitmap = bytearray([255,1,1,1,1,1,1,97,241,249,125,255,125,249,241,97,1,1,129,193,129,1,1,1,255,
#           255,24,60,126,255,126,60,24,0,16,17,125,17,16,0,56,124,57,19,255,19,57,124,56,255,
#           255,0,0,0,0,0,0,6,15,31,62,124,62,31,15,6,0,2,3,3,3,2,0,0,255,
#           1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1])

# increased the size so the icons does not touch the border
# BITMAP: width: 27, height: 26
suitsInfo_bitmap = bytearray([255,1,1,1,1,1,1,1,193,225,241,249,253,249,241,225,193,1,1,1,129,1,1,1,1,1,255,
           255,0,48,120,252,254,252,120,48,1,33,34,251,34,33,1,112,248,114,39,255,39,114,248,112,0,255,
           255,0,0,0,0,1,0,0,12,30,62,124,248,124,62,30,12,0,4,6,7,6,4,0,0,0,255,
           3,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,3])


# right arrow
# BITMAP: width: 8, height: 9
right_arrow_bitmap = bytearray([56,56,56,255,254,124,56,16,0,0,0,1,0,0,0,0])

# sprite creation

thumby.display.fill(0) # Fill canvas to black

# draw the suits information icon
suit_info_Spr = thumby.Sprite(27, 26, suitsInfo_bitmap)
suit_info_Spr.x = 0
suit_info_Spr.y = 14
thumby.display.drawSprite(suit_info_Spr)

# setup the sprite to use for displaying the history along the top
suit_set = thumby.Sprite(11, 13, suit_spritemap)

# 
right_arrow_spr = thumby.Sprite(8, 9, right_arrow_bitmap, 0, 2)
thumby.display.drawSprite(right_arrow_spr)

# putting R and B letters to represent the RED and BLACK selection for the B and A button
thumby.display.drawText('R', 56, 30, 1)
thumby.display.drawText('B', 65, 30, 1)

# draw the score frame
scoreSpr = thumby.Sprite(22, 20, score_bitmap, 30, 16)
thumby.display.drawSprite(scoreSpr)
thumby.display.drawText('906', 32, 27, 1)

#thumby.display.drawText('Welcome', 12, 2, 1)

thumby.display.update()

# runs through the history list matching the first 5 elements to the suits
# then update the history list on the screen
def update_history(history_list = ['o','o','o','o','o']):
    suit_set.setFrame(0)
    suit_set.y = 0
    
    for x in range(0, 5):

        if history_list[x][0] == 'o':
            suit_set.x = (x*13) + 9
            suit_set.setFrame(0)
            
        if history_list[x][0] == 'S':
            suit_set.x = (x*13) + 9
            suit_set.setFrame(1)                
    
        if history_list[x][0] == 'H':
            suit_set.x = (x*13) + 9
            suit_set.setFrame(2) 
            
        if history_list[x][0] == 'C':
            suit_set.x = (x*13) + 9
            suit_set.setFrame(3) 
    
        if history_list[x][0] == 'D':
            suit_set.x = (x*13) + 9
            suit_set.setFrame(4) 
    
        thumby.display.drawSprite(suit_set)
        thumby.display.update()


# display the icon if the user guess is correct or incorrect. will also set end of game
def do_indicator(indicate):
    indicate_Spr = thumby.Sprite(16, 13, indicate_spritemap)
    indicate_Spr.x = 55
    indicate_Spr.y = 15
    indicate_Spr.setFrame(0)

    if indicate == 'tick':
        indicate_Spr.setFrame(1)
    elif indicate == 'cross':
        indicate_Spr.setFrame(2)
    elif indicate == 'end':
        indicate_Spr.setFrame(3)        
    else:
        indicate_Spr.setFrame(0)
    
    thumby.display.drawSprite(indicate_Spr)
    thumby.display.update() 


def deck_shuffle(stack = 1):

    deck = ['SA', 'S2', 'S3', 'S4', 'S5', 'S6', 'S7', 'S8', 'S9', 'S10', 'SJ', 'SQ', 'SK',
        'HA', 'H2', 'H3', 'H4', 'H5', 'H6', 'H7', 'H8', 'H9', 'H10', 'HJ', 'HQ', 'HK',
        'CA', 'C2', 'C3', 'C4', 'C5', 'C6', 'C7', 'C8', 'C9', 'C10', 'CJ', 'CQ', 'CK',
        'DA', 'D2', 'D3', 'D4', 'D5', 'D6', 'D7', 'D8', 'D9', 'D10', 'DJ', 'DQ', 'DK'
        ]  

    return deck*stack


def do_reset(stack):
    thumby.display.drawFilledRectangle(32, 27, 18, 8, 0)
    history_list = ['o','o','o','o','o']
    score = 0
    deck = deck_shuffle(stack)
    do_indicator('blank')
    
    return history_list, score, deck

def compare_card(user_select, deck):
    point = 0
    
    if len(deck) == 1:
        card = deck.pop(0)

    else:
        position = random.randint(0, (len(deck) - 1))
        card = deck.pop(position)

    if user_select[0:3] == 'Bla':
        if card[0] == 'C' or card[0] == 'S':
            print('BLAck correct')
            point = 1
            
    if user_select[0:3] == 'Red':
        if card[0] == 'H' or card[0] == 'D':
            print('RED correct')
            point = 1
            
    if user_select[0:3] == 'Spa':
        if card[0] == 'S':
            print('SPAde correct')
            point = 4
            
    if user_select[0:3] == 'Hea':
        if card[0] == 'H':
            print('HEArt correct')
            point = 4
            
    if user_select[0:3] == 'Clu':
        if card[0] == 'C':
            print('CLUb correct')
            point = 4
            
    if user_select[0:3] == 'Dia':
        if card[0] == 'D':
            print('DIAmond correct')
            point = 4

    return card, point, deck

# initial settings, for when the script is first executed
# initial setup, create all necessary global variables

do_indicator('blank')
deck = deck_shuffle()
history_list = ['o','o','o','o','o']
update_history(history_list)
point = 0
score = 0
card = ''
stack = 1
thumby.display.drawLine(36, 38, 38, 38, 1)

# loop to wait for user to make a selection
while True:

    c = get_user_input()
    any_button_is_pressed = c != ' '

    if any_button_is_pressed:

        if len(deck) < 1:
            print('deck is empty')
            do_indicator('end')

        else:
            card, point, deck = compare_card(c, deck)
            
            history_list.insert(0, card)
            update_history(history_list)
            
            if point > 0:
                do_indicator('tick')
            else:
                do_indicator('cross')
            
            score = score + point
            
            print("score:", score, "Cards Left:", len(deck))
            
            thumby.display.drawFilledRectangle(32, 27, 18, 8, 0)
            thumby.display.drawText("%03d" % (score), 32, 27, 1)
            thumby.display.update()    

# will reset the game                
        if thumby.buttonL.pressed() and thumby.buttonA.pressed():
            print('Reset')
            history_list, score, deck = do_reset(stack)
            update_history()

# toggle between the number of decks to use, 1, 4, 6. will update the indicator line below the score
        if thumby.buttonU.pressed() and thumby.buttonB.pressed():
            thumby.display.drawLine(36, 38, 46, 38, 0)
        
            if stack == 1:
                stack = 4
                thumby.display.drawLine(36, 38, 38, 38, 1)
                thumby.display.drawLine(40, 38, 42, 38, 1)
                
            elif stack == 4:
                stack = 6
                thumby.display.drawLine(36, 38, 38, 38, 1)
                thumby.display.drawLine(40, 38, 42, 38, 1)
                thumby.display.drawLine(44, 38, 46, 38, 1)
                
            elif stack == 6:        
                stack = 1
                thumby.display.drawLine(36, 38, 38, 38, 1)
                
            history_list, score, deck, = do_reset(stack)
            update_history()
            thumby.display.update()
            
            print("Card in the Deck:", len(deck))
                

   
