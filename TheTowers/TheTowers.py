# Author:       Lennen Madere
# Discord:      GlennMad
# File Name:    TheTowers.py
# Last Update:  06-14-2022
# Version:      1.0
"""
This game is a mini version of the Towers of Hanoi; at the start, the user has
the option of disk count for difficulty changes.  Any in progress gameplay should
be saved when the device is shut off and returned upon choosing the load option.
All highscores will be visible after the win screen and upon pressing the B-button
in the main menu.  If any bugs should be observed, please contact the Author on the
Thumby discord.  Thank you, and hope you enjoy the game!
"""

import thumby
import os

#SHARED FUNCTIONS
#Funtions by SHDWWZRD - NeoRetro Games
#=======================================================================================
def drawSprite( inspr, x:int, y:int, width:int, height:int, key=-1, frame = 0, masked = False):
    sprite = []
    if(globals().get('ImageFile') is not None and type(inspr)==ImageFile):
        if(inspr.masked):
            masked = True
            sprite.append(inspr.maskedBitmap)
        sprite.append(inspr.bitmap)
    elif(type(inspr[0]) == tuple):#animated sprite data
        if(masked):#masked
            sprite.append(bytearray(inspr[2*frame]))
            sprite.append(bytearray(inspr[2*frame+1]))
        else:#not masked
            sprite.append(bytearray(inspr[frame]))
    else:#not animated can not be masked
        sprite.append(bytearray(inspr))          
    if(masked):
        thumby.display.blit(sprite[0], x, y, width, height, 1,0,0)
        thumby.display.blit(sprite[1], x, y, width, height, 0,0,0)
    else:
        thumby.display.blit(sprite[0], x, y, width, height, key,0,0)
     
def getCamSmoothMove(distance:int):
    off = abs(distance)
    if (off >= 40):
        if(distance < 0):
            off = -20
        else:
            off = 20
    elif (off >= 4):
        off = int(distance / 2)
    elif (off > 0):
        if(distance < 0):
            off = -1
        else:
            off = 1
    else:
        off = 0
    return off
#=========================================================================================

def WinScreenShow():
    thumby.display.drawText("Win", 29,4, 0)
    thumby.display.drawText("in", 31,14, 0)
    Moves.show = True
    Moves.x, Moves.y = (36-(int(Moves.width/2))), 25
    Moves.drawMoves()
    if(thumby.actionJustPressed()):
        HighScores.LoadScores()
        HighScores.NewScore(Moves.moves)
        SaveGame.deleteSave()
        return 3
    return 10
    
def MainMenuShow(menu:int,state:int,choose:int):
    #Main Menu Section
    count = 0
    if (menu == 0):
        menu_arrow_coord = ((0,20),(0,29),(33,20))
        thumby.display.drawText("Main Menu", 10,4, 0)
        thumby.display.drawText("Play", 10,21, 0)
        thumby.display.drawText("Quit", 10,30, 0)
        if(SaveGame.isSaved()):
            thumby.display.drawText("Load", 43,21, 0)
        
        #Advance choice selection
        if(thumby.dpadJustPressed()):
            choose += 1
        if(choose>1):
            if(SaveGame.isSaved()):
                if(choose>2):
                    choose = 0
            else:
                choose = 0
        
        drawSprite(menu_arrow_masked, menu_arrow_coord[choose][0]+offset,menu_arrow_coord[choose][1], 8,8, masked=True)
        
        #Choose play
        if(choose == 0 and thumby.buttonA.justPressed()):
            #Move to diff selction
            menu = 1
            choose = 0
        #Choose load
        if(choose == 2 and thumby.buttonA.justPressed()):
            #Load Saved game
            menu = 0
            state = 2
        #Choose quit
        if(choose == 1 and thumby.buttonA.justPressed()):
            #Leave game
            menu = 0
            state = -1
        if(thumby.buttonB.justPressed()):
            menu = 0
            state = 3
            HighScores.LoadScores()
    #Choose Difficulty Section
    elif (menu == 1):
        diff_choice = (3,5,7)
        thumby.display.drawText("Choose", 2,4, 0)
        thumby.display.drawText("Difficulty", 21,12, 0)
        
        #Advance choice selection
        if(thumby.dpadJustPressed()):
            choose += 1
        if(choose>2):
            choose = 0
        
        thumby.display.drawText(str(diff_choice[choose]), 10,24, 0)
        thumby.display.drawText("Disks", 18,24, 0)
        drawSprite(menu_arrow_masked, 0+offset,23, 8,8, masked=True)
        
        if(thumby.buttonA.justPressed()):
            count = diff_choice[choose]
            menu = 0
            state = 0
        elif(thumby.buttonB.justPressed()):
            menu = 0
            choose = 0
    #If state returned: -1 -> Exit game; 0 -> New game; 2 -> Load game
    return menu, state, choose, count

def initGameBoard(disk_count:int):
    #Load game from save file
    # Initiate peg0 with the correct disk count
    for d in reversed(range((7-disk_count),7)):
        if(d==0): top=True
        else: top=False
        if(d==(disk_count-1)): bottom=True
        else: bottom=False
        disk_y = peg_ys[d]
        peg0.append(Disk(disk_x,disk_y,top,bottom,d))
        
    board = [peg0,peg1,peg2]
    return board

# May Needs #

# Disk class to be held in three individual stacks
#   Attributes within class to account for position
#   Height on stacks
#   Adjacent disks
#   Held state
"""
# BITMAP: width: 8, height: 8
bitmap3 = bytearray([0,0,60,60,24,24,0,0])
"""
TheTowers_Logo = (# width, height 72, 40
    0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0x83, 0x01, 0x11, 0x38, 0x38, 0x7c, 0x7c, 0x7c, 0x7c, 0x7c, 0x7c, 0x7c, 0x7c, 0x7c, 0x7c, 0x7c, 0x38, 0x38, 0x11, 0x01, 0x83, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 
    0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0xc1, 0xdd, 0xdd, 0x1d, 0xfd, 0xfd, 0xfd, 0x1d, 0xdc, 0xdc, 0x00, 0xfc, 0xfc, 0xc0, 0xde, 0xde, 0xde, 0xc0, 0xfc, 0xfc, 0x00, 0xfc, 0xfc, 0x0d, 0x6d, 0x6d, 0x6d, 0x6d, 0xed, 0xed, 0xe1, 0xff, 0xff, 0xff, 0xff, 
    0x7f, 0x7f, 0x7f, 0x7f, 0x7f, 0x7f, 0x7f, 0x7f, 0x7f, 0x7f, 0x7f, 0x7f, 0x7f, 0x7f, 0x7f, 0x7f, 0x7f, 0x7f, 0x7f, 0x7f, 0x7f, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0x00, 0x7f, 0x7f, 0x7f, 0x00, 0xff, 0xff, 0x00, 0x7f, 0x7f, 0x00, 0xfe, 0xfe, 0xfe, 0x00, 0x7f, 0x7f, 0x00, 0x7f, 0x7f, 0x61, 0x6d, 0x6d, 0x6d, 0x6c, 0x6f, 0x6f, 0x0f, 0xff, 0xc1, 0x80, 0x88, 
    0x1c, 0x1c, 0x3e, 0x3e, 0x3e, 0x3e, 0x3e, 0x3e, 0x3e, 0x3e, 0x3e, 0x3e, 0x3e, 0x3e, 0x3e, 0x3e, 0x3e, 0x3e, 0x3e, 0x1c, 0x1c, 0x88, 0x80, 0xc1, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0x3f, 0x1f, 0x1f, 0x8f, 0x8f, 0xcf, 0xff, 0xe0, 0xee, 0xee, 0x0e, 0xfe, 0xfe, 0xfe, 0x0e, 0xee, 0xee, 0x00, 0xf9, 0xfc, 0x0e, 0xf6, 0xf6, 0xf6, 0x0e, 0xfc, 0xf9, 0x00, 0xfe, 0x00, 0xff, 0xff, 0x7f, 0xff, 0xff, 0x00, 0xfe, 0x00, 0xfe, 0xfe, 0x86, 0xb6, 
    0xb6, 0xb6, 0x36, 0xf6, 0xf6, 0x00, 0xfe, 0xfe, 0xc2, 0xda, 0x66, 0x3c, 0x99, 0xc3, 0x19, 0x7c, 0xfe, 0xce, 0x86, 0xb6, 0xb6, 0xb6, 0xb6, 0x30, 0x79, 0xff, 0x7f, 0x3f, 0x3f, 0x1f, 0x18, 0x90, 0x91, 0x83, 0x83, 0x87, 0xff, 0xff, 0xff, 0xff, 0x80, 0xbf, 0xbf, 0xbf, 0x80, 0xff, 0xff, 0xe0, 0xcf, 0x9f, 0xb8, 0xb7, 0xb7, 0xb7, 0xb8, 0x9f, 0xcf, 0xe0, 0xcf, 0x98, 0xb3, 0x98, 0xce, 0x98, 0xb3, 0x98, 0xcf, 0x80, 0xbf, 0xbf, 0xb0, 0xb6, 
    0xb6, 0xb6, 0xb6, 0xb7, 0xb7, 0x80, 0xbf, 0xbf, 0x81, 0xf3, 0xe6, 0xcc, 0x99, 0xb3, 0x87, 0xb6, 0xb6, 0xb6, 0xb6, 0xb6, 0xb0, 0xb9, 0xbf, 0x9f, 0xc0, 0xff, 0xe0, 0xc0, 0xc6, 0x8f, 0x8f, 0x9f, 0x9f, 0x9f, 0x9f, 0x9f)

"""
Typically DISK_COUNT will be set to 7 for full game play.
This value can be changed by the user through and IDE
for ease or testing.
"""
# A "const" for the count of disks
DISK_COUNT = 7

disksLarge_Outline = ( # Widths: 20, Heights: 4
# Frame 1/7
    (15,15,15,15,15,15,15,9,6,6,6,6,9,15,15,15,15,15,15,15),
# Frame 2/7
    (15,15,15,15,15,15,9,6,6,6,6,6,6,9,15,15,15,15,15,15),
# Frame 3/7
    (15,15,15,15,15,9,6,6,6,6,6,6,6,6,9,15,15,15,15,15),
# Frame 4/7
    (15,15,15,15,9,6,6,6,6,6,6,6,6,6,6,9,15,15,15,15),
# Frame 5/7
    (15,15,15,9,6,6,6,6,6,6,6,6,6,6,6,6,9,15,15,15),
# Frame 6/7
    (15,15,9,6,6,6,6,6,6,6,6,6,6,6,6,6,6,9,15,15),
# Frame 7/7
    (15,9,6,6,6,6,6,6,6,6,6,6,6,6,6,6,6,6,9,15))

"""
# BITMAP: width: 72, height: 30
widePegs = (0,0,0,0,0,0,0,0,0,0,0,0,252,252,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,252,252,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,252,252,0,0,0,0,0,0,0,0,0,0,0,0,
           0,0,0,0,0,0,0,0,0,0,0,0,255,255,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,255,255,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,255,255,0,0,0,0,0,0,0,0,0,0,0,0,
           0,0,0,0,0,0,0,0,0,0,0,0,255,255,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,255,255,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,255,255,0,0,0,0,0,0,0,0,0,0,0,0,
           48,48,48,48,48,48,48,48,48,48,48,48,63,63,48,48,48,48,48,48,48,48,48,48,48,48,48,48,48,48,48,48,48,48,48,63,63,48,48,48,48,48,48,48,48,48,48,48,48,48,48,48,48,48,48,48,48,48,63,63,48,48,48,48,48,48,48,48,48,48,48,48)
"""
menu_arrow_masked = (# Width: 8, Height: 8, Masked
    (255,195,189,189,219,219,231,255),
    (0,0,60,60,24,24,0,0))
arrow_masked = ( # Width: 8, Height: 8, Masked
    # Frame 1/1 Masked
    (255,225,205,157,157,205,225,255),
    (0,0,12,28,28,12,0,0))
arrow_y = 2
offset = 0
offset_direction = 1

# BITMAP: width: 8, height: 8
bitmap27 = bytearray([255,255,231,195,195,231,255,255])

count_up = True
bad_move_count = 0
bad_move = False
x_masked = ( # Width 8, Height: 8, Masked
    # Frame 1/3, Masked
    (60,24,129,195,195,129,24,60),
    (0,0,0,0,0,0,0,0),
    # Frame 2/3, Masked
    (255,153,129,195,195,129,153,255),
    (0,0,0,0,0,0,0,0),
    # Frame 3/3, Masked
    (255,255,231,195,195,231,255,255),
    (0,0,0,0,0,0,0,0))

frameCounter = 0

# Accounts for the current peg under selection for both arrow and disk
curPeg = 0

peg_xs = [9,32,55]
peg_ys = [12,16,20,24,28,32,36]
peg_y_rev = [36,32,28,24,20,16,12]

class Save:
    def __init__(self,_file_name:str):
        self.file_name = _file_name
        self.read_data = []
        
    def saveGame(self,board,moves):
        
        savFile = open(self.file_name, 'w')
            
        for peg in board:
            d = 0
            while (d < len(peg)):
                savFile.write(str(peg[d].x))
                savFile.write(",")
                savFile.write(str(peg[d].y))
                savFile.write(",")
                savFile.write(str(peg[d].size))
                savFile.write(",")
                d += 1
        savFile.write(str(moves))
        #savFile.write(cursor.x)
        #savFile.write(cursor.y)
        savFile.close()
        return 0
        
    def loadGame(self,game_board,moves):
        
        self.read_data = open(self.file_name, 'r').read().split(",")
        if(len(self.read_data) == 10):
            disk_count = 3
        elif(len(self.read_data) == 16):
            disk_count = 5
        elif(len(self.read_data) == 22):
            disk_count = 7
        
        moves = int(self.read_data[len(self.read_data) - 1])
        
        #game_board = initGameBoard(disk_count)
        #print(game_board)
        
        peg_num = {3:0,26:1,49:2}
        disk_spot = {36:0,32:1,28:2,24:3,20:4,16:5,12:6}
        
        d = 0
        while((d/3) < disk_count):
            temp_x, temp_y, temp_size = int(self.read_data[d]), int(self.read_data[d+1]), int(self.read_data[d+2])
            
            if(peg_num[temp_x] == 0 and temp_y != 0): peg0.append(Disk(temp_x,temp_y,False,False,temp_size))
            elif(peg_num[temp_x] == 1 and temp_y != 0): peg1.append(Disk(temp_x,temp_y,False,False,temp_size))
            elif(peg_num[temp_x] == 2 and temp_y != 0): peg2.append(Disk(temp_x,temp_y,False,False,temp_size))
            
            if(peg_num[temp_x] == 0 and temp_y == 0): peg0.append(Disk(temp_x,peg_y_rev[len(peg0)],False,False,temp_size))
            elif(peg_num[temp_x] == 1 and temp_y == 0): peg1.append(Disk(temp_x,peg_y_rev[len(peg1)],False,False,temp_size))
            elif(peg_num[temp_x] == 2 and temp_y == 0): peg2.append(Disk(temp_x,peg_y_rev[len(peg2)],False,False,temp_size))
            
            d+=3
        game_board = [peg0,peg1,peg2]
        self.deleteSave()
        return game_board, moves, disk_count
    
    def deleteSave(self):
        try:
            os.remove(self.file_name)
        except OSError:
            return False
        return True
        
    def isSaved(self):
        try:
            st = os.stat(self.file_name)
        except OSError:
            return False
        return True

class HighScores:
    
    def __init__(self,_file_name:str):
        self.file_name = _file_name
        self.three_scores = [300,333,321,345]
        self.five_scores = [500,555,543,567]
        self.seven_scores = [700,777,765,789]
        self.scoreTable = {3:self.three_scores,5:self.five_scores,7:self.seven_scores}
        self.selection = -1
        self.disk_to_selc = {3:0,5:1,7:2}
        self.selc_to_disk = {0:3,1:5,2:7}
        self.read_data = []
        
    #Display each set of scores independently, change with button press
    def DisplayScores(self):
        
        #disk_to_selc = {3:0,5:1,7:2}
        if(self.selection == -1):
            if(DISK_COUNT == 0):
                self.selection = 0
            else:
                self.selection = self.disk_to_selc[DISK_COUNT]
        scoreTitles = {0:"Three",1:"Five",2:"Seven"}
        if(self.selection > 2):
            self.selection = 0
        score_x, score_y = 47, 5
        thumby.display.drawText(scoreTitles[self.selection],2,5,0)
        thumby.display.drawText("Disks",2,15,0)
        thumby.display.drawText("Score:",2,25,0)
        for num in range(1,5):
            thumby.display.drawText(str(num) + ".",36,score_y,0)
            score_y += 8
        score_y = 5
        for score in self.scoreTable[self.selc_to_disk[self.selection]]:
            thumby.display.drawText(str(score),score_x,score_y,0)
            score_y += 8
        if(thumby.dpadJustPressed()): self.selection += 1
        if(thumby.actionJustPressed()): 
            HighScores.SaveScores(Moves.moves)
            if(prevWin):
                thumby.reset()
            else:
                return 2
        drawSprite(menu_arrow_masked, 62+offset,18, 8,8, masked=True)
        return 3
    
    def NewScore(self,moves:int):
        self.scoreTable[DISK_COUNT].append(moves)
        self.scoreTable[DISK_COUNT].sort()
        if(len(self.scoreTable[DISK_COUNT])>4):
            temp_score = self.scoreTable[DISK_COUNT].pop()
        print(self.scoreTable[3])
        return 0
    
    #Save all scores to the file    
    def SaveScores(self,moves:int):
        savFile = open(self.file_name, 'w')
        
        for i in range(0,4):
            savFile.write(str(self.scoreTable[3][i]))
            savFile.write(",")
        for i in range(0,4):
            savFile.write(str(self.scoreTable[5][i]))
            savFile.write(",")
        for i in range(0,4):
            savFile.write(str(self.scoreTable[7][i]))
            savFile.write(",")
        
        savFile.close()
        return 0
    
    #Load all scores from the file
    def LoadScores(self):
        if(self.isSaved()):
            self.read_data = open(self.file_name, 'r').read().split(",")
            for i in range(0,4):
                self.three_scores[i] = int(self.read_data.pop(0))
            for i in range(0,4):
                self.five_scores[i] = int(self.read_data.pop(0))
            for i in range(0,4):
                self.seven_scores[i] = int(self.read_data.pop(0))
            self.scoreTable.update({3:self.three_scores,5:self.five_scores,7:self.seven_scores})
            print(self.three_scores)
            print(self.scoreTable[3])
        return 0
        
    def isSaved(self):
        try:
            st = os.stat(self.file_name)
        except OSError:
            return False
        return True

class MovesCounter:
    def __init__(self,_init_x:int,_init_y:int,_moves:int,_show:bool):
        self.x = _init_x
        self.y = _init_y
        self.target_x = self.x
        self.target_y = self.y
        self.moves = _moves
        self.show = _show
        self.add_move = False
        self.width = 9
    
    # Update the x and y based on the show or no show bool
    def tickMoves(self):
        if(self.x != self.target_x or self.y != self.target_y):
            self.x += getCamSmoothMove(self.target_x - self.x)
            self.y += getCamSmoothMove(self.target_y - self.y)
        if(self.add_move):
            self.moves+=1
            self.add_move = False
        if(self.moves>=10 and self.moves<100):
            self.width = 15
        elif(self.moves>=100):
            self.width = 19
        return 0
    
    def drawMoves(self):
        thumby.display.drawRectangle(self.x,self.y,self.width,11,0)
        thumby.display.drawText(str(self.moves), self.x+2,self.y+2,0)
        return 0
        
    def saveMoves(self):
        return 0

class Disk:
    def __init__(self,_init_x:int,_init_y:int,_top:bool,_bottom:bool,_size:int):
        self.x = _init_x
        self.y = _init_y
        self.top = _top
        self.bottom = _bottom
        self.size = _size
        self.target_x = self.x
        self.target_y = self.y
    
    # Update all calculations for a Disk object
    def tickDisk(self):
        if(self.x != self.target_x or self.y != self.target_y):
            self.x += getCamSmoothMove(self.target_x - self.x)
            self.y += getCamSmoothMove(self.target_y - self.y)
        return 0
    
    # Draw all disk objects to the screen
    def drawDisk(self):
        drawSprite(disksLarge_Outline,self.x,self.y,20,4,-1,self.size,False)
        return 0
        
    def setTargets(self,target_x:int,target_y:int):
        self.target_x = target_x
        self.target_y = target_y
        return 0
        
    def saveDisk(self):
        if(self.target_y == self.y and self.y != 0): return True
        return False

class Cursor:
    def __init__(self,_init_x:int,_init_y:int,_init_off:int):
        self.x = _init_x
        self.y = _init_y
        self.offset = _init_off
        self.held = 0
        self.target_x = self.x
        self.target_y = self.y
    
    def tickCursor(self):
        if(self.x != self.target_x or self.y != self.target_y):
            self.x += getCamSmoothMove(self.target_x - self.x)
            self.y += getCamSmoothMove(self.target_y - self.y)
        return 0
    
    def drawCursor(self):
        drawSprite(arrow_masked, self.x,self.y+self.offset, 8,8, -1,0, True)
        return 0
    
    def setTargets(self,target_x:int,target_y:int):
        self.target_x = target_x
        self.target_y = target_y
        return 0

disk_x = 3
disk_y = 34
top = False
bottom = False
doSave = False
prevWin = False

# Initiate the board with empty pegs
peg0 = []
peg1 = []
peg2 = []
hold = 0
board = []

# Initiate the move counter
Moves = MovesCounter(73,0, 0, False)

SaveGame = Save("/Games/TheTowers/TheTowers.sav")

HighScores = HighScores("/Games/TheTowers/TheTowersHS.sav")

GameState = 0

# Set the FPS (without this call, the default fps is 30)
thumby.display.setFPS(25)

thumby.display.setFont('lib/font5x7.bin', 5, 7, 0)

while(True):
    thumby.display.fill(1) # Fill canvas to black
    
    # Counter for frames which resets back to zero
    frameCounter+=0.25
    if(frameCounter%2==0):
        offset+=offset_direction
        if(offset==2): offset_direction=-1
        elif(offset==0): offset_direction=1
    
    if (GameState == 0):
        #Draw title
        drawSprite(TheTowers_Logo,0,0,72,40)
        frameCounter += 1
        if (frameCounter >= 125 or thumby.inputJustPressed()):
            frameCounter = 0
            GameState = 2
            menu, state, choose = 0, 1, 0
    elif (GameState == 2):
        #Draw Menu
        menu, state, choose, DISK_COUNT = MainMenuShow(menu, state, choose)
        if(state == 0):
            board = initGameBoard(DISK_COUNT)
            GameState = -1
        elif(state == 2):
            board, Moves.moves, DISK_COUNT = SaveGame.loadGame(board,Moves.moves)
            GameState = -1
        elif(state == 3):
            GameState = 3
        elif(state == -1):
            #exit game
            thumby.reset()
            #GameState = 3
    elif (GameState == 3):
        GameState = HighScores.DisplayScores()
        menu, state, choose = 0, 1, 0
        
    elif (GameState == 10):
        #Win game
        GameState = WinScreenShow()
        prevWin = True
    else:
        # If one of the two right-most pegs have a full stack, win state:
        if(len(peg1) == (DISK_COUNT) or len(peg2) == (DISK_COUNT)):
            GameState = 10
            continue
        
        # Gameplay Layout #
        # Update frame for all moving parts (sprites)
        # Follow current peg selection with arrow
        # Move top disk of stack when selected into arrow
        # Move disk with the current peg selection
        # Drop disk on top of stack for new peg
        # Check the size of new top disk with previous top disk
        # If new top disk is larger, return to previous stack
        # Once all disks have been moved from a stack, begin check for win
        
        # Draw the peg board
        #drawSprite(widePegs, 0,10, 72,30, False,False, -1, 0, False)
        for x in range(12,59,23):
            thumby.display.drawRectangle(x,12, 2,28, 0)
        #thumby.display.drawRectangle(12,12, 2,28, 0)
        #thumby.display.drawRectangle(35,12, 2,28, 0)
        #thumby.display.drawRectangle(58,12, 2,28, 0)
        
        # Initiate each disk on it's current peg
        for peg in board:
            i=0
            while(i<len(peg)):
                peg[i].tickDisk()
                peg[i].drawDisk()
                i+=1
        
        # If hold contains a disk object, draw disk realative to arrow
        if(hold != 0):
            hold.setTargets(peg_xs[curPeg]-6,arrow_y-2)
            hold.tickDisk()
            hold.drawDisk()
        
        if(not bad_move):
            drawSprite(arrow_masked, peg_xs[curPeg],2+offset, 8,8, -1,0, True)
        # If there was a bad move, display the x
        if(bad_move):
            if(count_up):
                if(bad_move_count>=2.99):
                    count_up = False
                    bad_move_count = 2
                    continue
                drawSprite(x_masked, peg_xs[curPeg],4, 8,8, -1,int(bad_move_count), True)
                bad_move_count+=0.2
                thumby.display.update()
                continue
            else:
                if(bad_move_count<=0.1):
                    count_up = True
                    bad_move = False
                    bad_move_count = 0
                    continue
                drawSprite(x_masked, peg_xs[curPeg],4, 8,8, -1,int(bad_move_count), True)
                bad_move_count = bad_move_count - 0.2
                thumby.display.update()
                continue
        
        # Checks which dpad button has been pressed, if Left, move arrow left,
        # otherwise, arrow is moved right
        if(thumby.buttonL.justPressed() == True):
            curPeg = curPeg - 1
            Moves.show = False
        elif(thumby.dpadJustPressed() == True):
            curPeg+=1
            Moves.show = False
        if(curPeg>=3):
            curPeg = 0
        elif(curPeg<=-1):
            curPeg = 2
            
        # If hold is empty and pickup is pressed, move top disk to hold position
        if(hold == 0 and thumby.buttonB.justPressed() == True):
            if(len(board[curPeg])>0):
                hold = board[curPeg].pop()
                hold.setTargets(peg_xs[curPeg]-6,arrow_y-2)
                hold.tickDisk()
                hold.drawDisk()
            Moves.show = False
            SaveGame.saveGame(board,Moves.moves)
        # If hold is not empty and action button is pressed, place disk ontop of stack
        elif(hold != 0 and thumby.buttonB.justPressed() == True):
            # If the peg is not empty...
            if(len(board[curPeg])>0):
                # If the top most disk is smaller than the held disk
                if(hold.size > board[curPeg][len(board[curPeg])-1].size):
                    # Animate the X for incorrect movement
                    bad_move = True
                    continue
            # For allowed moves, disk object moves to the curent peg list.
            hold.setTargets(peg_xs[curPeg]-6,peg_y_rev[len(board[curPeg])])
            board[curPeg].append(hold)
            hold = 0
            # Add a move if the held disk was placed properly
            Moves.add_move = True
            Moves.show = False
            Moves.tickMoves()
            SaveGame.saveGame(board,Moves.moves)
        # If the A button was pressed, display the move counter
        if(thumby.buttonA.justPressed()==True):
            Moves.show = True
            Moves.target_x, Moves.target_y = (72-Moves.width), 0
            Moves.tickMoves()
            Moves.drawMoves()
        else:
            if(Moves.show == False):
                Moves.target_x, Moves.target_y = 73, 0
            Moves.tickMoves()
            Moves.drawMoves()
        
    # End game state else    
    thumby.display.update()
    














# Space for editor