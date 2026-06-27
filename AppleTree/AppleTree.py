#Catch the apples.
import time
import thumby
import math
import random
# Bitmaps: width:8, height:8
appleMap = bytearray([122,205,245,253,250,189,157,122])
basketMap = bytearray([126,213,173,213,173,213,237,126])

#Create Sprites using Bitmap (width,height,bitmapData,x,y,key,mirrorX,mirrorY)
appleSpr = thumby.Sprite(8,8,appleMap,key=0)
appleSpr.x=32
appleSpr.y=-8
basketSpr = thumby.Sprite(8,8,basketMap,key=0)
basketSpr.x=32
basketSpr.y=32

#Global Variables
score=0
collision=False

thumby.display.setFPS(60)#60 Frames per second

#TITLE SCREEN
thumby.display.fill(0)
thumby.display.setFont("/lib/font8x8.bin",8,8,1)#8x8 font
thumby.display.drawText("APPLE",14,0,1)
thumby.display.drawText("TREE",18,8,1)
thumby.display.setFont("/lib/font3x5.bin",3,5,1)#3x5 font
thumby.display.drawText("NIALLCHANDLERGAMES",0,35,1)
thumby.display.setFont("/lib/font5x7.bin",5,7,1)#5x7 font
thumby.display.update()
#Check is the player has pressed A or B
while(thumby.buttonA.pressed()==False and thumby.buttonB.pressed()==False):
    thumby.display.drawText("A:Play",18,17,1)
    thumby.display.drawText("B:Quit",18,25,1)
    thumby.display.update()
    if thumby.buttonB.pressed():
        thumby.reset()
    if thumby.buttonA.pressed():
        break

#HOW TO PLAY
thumby.display.fill(0)
thumby.display.setFont("/lib/font5x7.bin",5,7,1)#5x7 font
thumby.display.drawText("How to Play",4,0,1)
thumby.display.drawLine(0, 8, 72, 8, 1)
thumby.display.drawText("Catch the", 0, 10, 1)
thumby.display.drawText("apples with:", 0, 19, 1)
thumby.display.setFont("/lib/font8x8.bin",8,8,1)#8x8 font
thumby.display.drawText("< >",23,33,1)
thumby.display.drawSprite(basketSpr)

thumby.display.update()
time.sleep(4) #Num of seconds to read the instructions

#!THE ACTUAL GAME!
while(1):
    thumby.display.fill(0)
    
    #Collision Detection
    if appleSpr.x<basketSpr.x+8 and basketSpr.x<appleSpr.x+8 and appleSpr.y<basketSpr.y+8 and basketSpr.y<appleSpr.y+8:
        collision=True
        score+=1
        appleSpr.y=-8
        appleSpr.x=random.randint(0,64)
        thumby.audio.play(3000,60)
    else:
        collision=False

    #Player Movement
    if thumby.buttonL.pressed():
        basketSpr.x -= 0.5#Move left
    if thumby.buttonR.pressed():
        basketSpr.x += 0.5#Move right

    #Don't go offscreen
    if basketSpr.x<=0:#Left edge of screen
        basketSpr.x=0
    elif (basketSpr.x+7)>=72:#Right edge of screen 
        basketSpr.x=64

    #Show sprites on screen
    thumby.display.drawSprite(appleSpr)
    thumby.display.drawSprite(basketSpr)
    
    #Display Score
    thumby.display.drawText("%d" % score,0,0,1)

    
    #If apple falls off screen
    appleSpr.y+=0.2+(score/100)
    if appleSpr.y>=44:
        thumby.display.fill(1)
        thumby.display.drawText("GAMEOVER",0,16,0)
        thumby.display.update()
        time.sleep(2) # delay game for a few seconds so player can read closing message
        thumby.reset() # exit game to main menu

    thumby.display.update()