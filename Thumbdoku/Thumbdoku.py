import time
import thumby
import math

GAME_NAME = "Sudoku"
GAME_DIR = "/Games/" + GAME_NAME

import gc

free_min = gc.mem_free()

def gc_poke():
    global free_min
    free_now = gc.mem_free()
    print("free before poke:", free_now)
    if free_now < free_min:
        free_min = free_now
    gc.collect()
    print("free after poke:", gc.mem_free())

gc_poke()

from sys import path
path.append(GAME_DIR)

import thumbyGrayscale
graphics = thumbyGrayscale

graphics.display.setFPS(30)
graphics.display.fill(0)
graphics.display.drawText(" Loading... ", 0, 15, 1)
graphics.display.update()
gc_poke()

numbers = [bytearray([0,0,0]), bytearray([0,7,0]), bytearray([1,7,4]), bytearray([5,7,7]), bytearray([3,2,7]), bytearray([4,7,1]), bytearray([7,6,0]), bytearray([0,1,7]), bytearray([3,7,6]), bytearray([0,3,7])]
playing = False
diff = 0
cursor = 2


import random
from time import sleep

#A backtracking/recursive function to check all possible combinations of numbers until a solution is found
def fillGrid(locks, grid, depth):
    global counter
    numberList=[1,2,3,4,5,6,7,8,9]
    #Find next empty cell
    for g in range(0,depth):
        row = random.randint(0, 8)
        col = random.randint(0, 8)
        if grid[row][col]==0:
            value = random.randint(1, 9)
            #Check that this value has not already be used on this row
            if not(value in grid[row]):
              #Check that this value has not already be used on this column
              if not value in (grid[0][col],grid[1][col],grid[2][col],grid[3][col],grid[4][col],grid[5][col],grid[6][col],grid[7][col],grid[8][col]):
                #Identify which of the 9 squares we are working on
                square=[]
                if row<3:
                  if col<3:
                    square=[grid[i][0:3] for i in range(0,3)]
                  elif col<6:
                    square=[grid[i][3:6] for i in range(0,3)]
                  else:  
                    square=[grid[i][6:9] for i in range(0,3)]
                elif row<6:
                  if col<3:
                    square=[grid[i][0:3] for i in range(3,6)]
                  elif col<6:
                    square=[grid[i][3:6] for i in range(3,6)]
                  else:  
                    square=[grid[i][6:9] for i in range(3,6)]
                else:
                  if col<3:
                    square=[grid[i][0:3] for i in range(6,9)]
                  elif col<6:
                    square=[grid[i][3:6] for i in range(6,9)]
                  else:  
                    square=[grid[i][6:9] for i in range(6,9)]
                #Check that this value has not already be used on this 3x3 square
                if not value in (square[0] + square[1] + square[2]):
                  grid[row][col]=value
                  locks[row][col]=1
    return [grid, locks]

def genBoard(diff):
    board = []
    locks = []
    for i in range(9):
        board.append([0,0,0,0,0,0,0,0,0])
        locks.append([0,0,0,0,0,0,0,0,0])
    depth = (diff + 10) * 4
    return fillGrid(locks, board, depth)
    


ptrX = 0
ptrY = 0
boardX = 17
boardY = 1



while(True):
    if playing:
        if thumby.buttonU.justPressed():
            ptrY = int((ptrY - 1) % 9)
        if thumby.buttonD.justPressed():
            ptrY = int((ptrY + 1) % 9)
        if thumby.buttonL.justPressed():
            ptrX = int((ptrX - 1) % 9)
        if thumby.buttonR.justPressed():
            ptrX = int((ptrX + 1) % 9)
        
        if thumby.buttonA.justPressed():
            if locks[ptrY][ptrX] == 0:
                g = board[ptrY][ptrX]
                board[ptrY][ptrX] = int((g+1) % 10)
        if thumby.buttonB.justPressed():
            if locks[ptrY][ptrX] == 0:
                g = board[ptrY][ptrX]
                board[ptrY][ptrX] = int((g-1) % 10)
        
        
        graphics.display.fill(0)
        graphics.display.drawFilledRectangle(boardX, boardY, 37, 37, 2)
        graphics.display.drawRectangle(boardX, boardY, 37, 37, 3)
        graphics.display.drawLine(boardX, boardY+12, boardX+37, boardY+12, 3)
        graphics.display.drawLine(boardX, boardY+24, boardX+37, boardY+24, 3)
        graphics.display.drawLine(boardX+12, boardY, boardX+12, boardY+37, 3)
        graphics.display.drawLine(boardX+24, boardY, boardX+24, boardY+37, 3)
        for i in range(9):
            for j in range(9):
                graphics.display.blit(numbers[board[i][j]], boardX + 1 + j * 4, boardY + 1 + i * 4, 3, 3, -1, 0, 0)
        graphics.display.drawRectangle(ptrX * 4 + boardX - 1, ptrY * 4 + boardY - 1, 7, 7, 1)
        graphics.display.update()
    else:
        if thumby.buttonD.justPressed():
            cursor = int((cursor - 1) % 3)
        if thumby.buttonU.justPressed():
            cursor = int((cursor + 1) % 3)
        if thumby.buttonA.justPressed():
            diff = cursor
            gen = genBoard(diff)
            board = gen[0]
            locks = gen[1]
            playing = True
        
        graphics.display.fill(0)
        graphics.display.setFont("/lib/font5x7.bin", 5, 7, 1)
        graphics.display.drawText("SUDOKU", 18, 2, 1)
        graphics.display.setFont("/lib/font3x5.bin", 3, 5, 1)
        graphics.display.drawText("Difficulty:", 15, 12, 1)
        graphics.display.drawText("Easy", 27, 19, 1 if cursor == 2 else 3)
        graphics.display.drawText("Medium", 23, 25, 1 if cursor == 1 else 3)
        graphics.display.drawText("Hard", 27, 31, 1 if cursor == 0 else 3)
        graphics.display.update()
