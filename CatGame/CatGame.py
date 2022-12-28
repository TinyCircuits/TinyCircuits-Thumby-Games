
#version
__version__="1.0_init"

# Import items
import time
import thumby
import math
import random

thumby.saveData.setName("CatGame")

# bitmaps
# BITMAP: width: 8, height: 8
catbitmap = bytearray([0,96,126,124,124,126,96,0])
bowlfullbitmap = bytearray([0,112,88,92,92,88,112,0])
bowlemptybitmap = bytearray([0,112,80,80,80,80,112,0])
heartbitmap = bytearray([14,31,63,126,126,63,31,14])
mousebitmap = bytearray([127,62,124,248,208,0,0,0])
giftbitmap = bytearray([16,244,138,244,244,138,244,16])
micebitmap = bytearray([224,176,208,240,224,128,128,128])
yarnbitmap = bytearray([56,84,170,214,170,212,184,128])

#Create Sprites using Bitmap (width,height,bitmapData,x,y,key,mirrorX,mirrorY)
heartspr = thumby.Sprite(8,8,heartbitmap,key=0)
heartspr.x=32
heartspr.y=-8
catspr = thumby.Sprite(8,8,catbitmap,key=0)
catspr.x=32
catspr.y=-8
mousespr = thumby.Sprite(8,8,mousebitmap,key=0)
mousespr.x=0
mousespr.y=0
bowlemptyspr = thumby.Sprite(8,8,bowlemptybitmap,key=0)
bowlemptyspr.x=32
bowlemptyspr.y=-8
bowlfullspr = thumby.Sprite(8,8,bowlfullbitmap,key=0)
bowlfullspr.x=32
bowlfullspr.y=-8
giftspr = thumby.Sprite(8,8,giftbitmap,key=0)
giftspr.x=32
giftspr.y=-8
micespr = thumby.Sprite(8,8,micebitmap,key=0)
micespr.x=32
micespr.y=-8
yarnspr = thumby.Sprite(8,8,yarnbitmap,key=0)
yarnspr.x=32
yarnspr.y=-8

#Global Variables
score=0
cathungry=True
bowlfull=False
randomvar=0
gifts=0
day=0
happyness=0

#TITLE SCREEN
thumby.display.fill(0)
thumby.display.setFont("/lib/font8x8.bin",8,8,1)#8x8 font
thumby.display.drawText("Pet",14,0,1)
thumby.display.drawText("Cat",33,8,1)
thumby.display.setFont("/lib/font3x5.bin",3,5,1)#3x5 font
thumby.display.drawText("by Nemokitty9",0,35,1)
thumby.display.setFont("/lib/font5x7.bin",5,7,1)#5x7 font
thumby.display.update()
#Check is the player has pressed A or B
while(thumby.buttonA.pressed()==False and thumby.buttonB.pressed()==False):
    thumby.display.drawText("A:Play",18,17,1)
    thumby.display.drawText("B:Exit",18,25,1)
    thumby.display.update()
    if thumby.buttonB.pressed():
        thumby.reset()
    if thumby.buttonA.pressed():
        break

#HOW TO PLAY
thumby.display.fill(0)
thumby.display.setFont("/lib/font3x5.bin",3,5,1)#3x5 font
thumby.display.drawText("How to Play",0,0,1)
thumby.display.drawLine(0, 8, 72, 8, 1)
thumby.display.drawText("Take care", 0, 10, 1)
thumby.display.drawText("of your cat.", 0, 16, 1)
thumby.display.drawText("B to end day/wait",0,22,1)
thumby.display.drawText("A then B to Save",0,28,1)
thumby.display.drawSprite(mousespr)

thumby.display.update()
time.sleep(4) #Num of seconds to read the instructions

thumby.display.fill(0)
bowlfullspr.x=64
bowlfullspr.y=31
bowlemptyspr.x=64
bowlemptyspr.y=31

# Game begins.
thumby.display.setFont("/lib/font5x7.bin",5,7,1)
if (thumby.saveData.hasItem("pscore")):
    score = int(thumby.saveData.getItem("pscore"))
if (thumby.saveData.hasItem("pcatx")):
    catspr.x= int(thumby.saveData.getItem("pcatx"))
if (thumby.saveData.hasItem("pcaty")):
    catspr.y= int(thumby.saveData.getItem("pcaty"))
if (thumby.saveData.hasItem("pgifts")):
    gifts = int(thumby.saveData.getItem("pgifts"))
if (thumby.saveData.hasItem("pday")):
    day = int(thumby.saveData.getItem("pday"))
if (thumby.saveData.hasItem("phappyness")):
    happyness = int(thumby.saveData.getItem("phappyness"))

while(1):
    
    thumby.display.fill(0)
    
    #Player Movement
    if thumby.buttonL.pressed():
        mousespr.x -= 0.25#Move left
    if thumby.buttonR.pressed():
        mousespr.x += 0.25#Move right
    #Don't go offscreen
    if mousespr.x<=0:#Left edge of screen
        mousespr.x=0
    elif (mousespr.x+7)>=72:#Right edge of screen 
        mousespr.x=64
    #Player Movement on Y cords
    if thumby.buttonU.pressed():
        mousespr.y -= 0.25#Move up
    if thumby.buttonD.pressed():
        mousespr.y += 0.25#Move down
    #Don't go offscreen on Y cords
    if mousespr.y<=0:#top edge of screen
        mousespr.y=0
    elif (mousespr.y+7)>=40:#bottom edge of screen 
        mousespr.y=32
    
    # Wait Command
    if thumby.buttonB.justPressed():
        day+=1
        thumby.display.drawText("%d" % score,0,0,1)
        thumby.display.drawText("Waited.",20,0,1)
        thumby.display.drawText("Gifts: ",0,10,1)
        thumby.display.drawText("%d" % gifts,35,10,1)
        thumby.display.drawText("Day: ",0,20,1)
        thumby.display.drawText("%d" % day,35,20,1)
        thumby.display.drawText("Happyness",0,30,1)
        thumby.display.drawText("%d" % happyness,55,30,1)
        catspr.y=random.randint(0,31)
        catspr.x=random.randint(0,64)
        thumby.display.update()
        time.sleep(2)
        randomvar=random.randint(0,8)
        if randomvar==0:
            cathungry=True
        #RNG of toy sprite
        randomvar=random.randint(0,1)
        if randomvar==0:
            randomvar=random.randint(0,1)
            if randomvar==0:
                micespr.x=random.randint(0,31)
                micespr.y=random.randint(0,64)
            elif randomvar==1:
                yarnspr.x=random.randint(0,31)
                yarnspr.y=random.randint(0,64)
        #RNG chance for gift to spawn (VERY RARE?!?!?)
        randomvar=random.randint(0,150)
        if randomvar==0:
            giftspr.x=random.randint(0,31)
            giftspr.y=random.randint(0,64)
        
    
        #Collision Detection (Cat)
    if thumby.buttonA.justPressed():
        
        if catspr.x<mousespr.x+8 and mousespr.x<catspr.x+8 and catspr.y<mousespr.y+8 and mousespr.y<catspr.y+8:
            collision=True
            score+=1
            if cathungry==False:
                
                catspr.y=random.randint(0,31)
                catspr.x=random.randint(0,64)
                thumby.audio.play(3000,60)
                time.sleep(1)
                randomvar=random.randint(0,10)
                if randomvar==0:
                    cathungry=True
                randomvar=random.randint(0,2)
                if randomvar==1:
                    happyness+=1
                
            elif cathungry==True:
                catspr.y=31
                catspr.x=52
                thumby.display.drawText("Cat Hungry!",8,0,1)
                time.sleep(2)
                if bowlfull==True:
                    bowlfull=False
                    cathungry=False
                    time.sleep(3)
                    randomvar=random.randint(0,20)
                    if randomvar==0:
                        cathungry=True
                        
        else:
            collision=False
    
    #Collision Detection (bowl)
    if thumby.buttonA.pressed():
        
        if bowlemptyspr.x<mousespr.x+8 and mousespr.x<bowlemptyspr.x+8 and bowlemptyspr.y<mousespr.y+8 and mousespr.y<bowlemptyspr.y+8:
            collision=True
            if bowlfull==False:
                score+=20
                bowlfull=True
            thumby.audio.play(1000,30)
            thumby.audio.play(2000,60)
            time.sleep(3)
        else:
            collision=False
    
    #Rendering of the food bowl when full/empty
    if bowlfull==True:
        thumby.display.drawSprite(bowlfullspr)
    elif bowlfull==False:
        thumby.display.drawSprite(bowlemptyspr)
    
    #Collision Detection (Gift)
    if thumby.buttonA.pressed():
        
        if giftspr.x<mousespr.x+8 and mousespr.x<giftspr.x+8 and giftspr.y<mousespr.y+8 and mousespr.y<giftspr.y+8:
            collision=True
            score+=250
            gifts+=1
            thumby.audio.playBlocking(2000,30)
            thumby.audio.playBlocking(4000,60)
            thumby.display.drawText("WOWZA!",0,10,1)
            thumby.display.drawText("A GIFT!!!",0,20,1)
            thumby.display.update()
            time.sleep(1)
            giftspr.x=32
            giftspr.y=-8
        else:
            collision=False
    
        #Collision Detection (toy)
    if thumby.buttonA.pressed():
        
        if micespr.x<mousespr.x+8 and mousespr.x<micespr.x+8 and micespr.y<mousespr.y+8 and mousespr.y<micespr.y+8:
            collision=True
            score+=5
            happyness+=2
            thumby.audio.playBlocking(2000,30)
            time.sleep(1)
            if micespr.x==32:
                catspr.x=yarnspr.x
                catspr.y=yarnspr.y
            elif yarnspr.x==32:
                catspr.x=micespr.x
                catspr.y=micespr.y
            micespr.x=32
            micespr.y=-8
            yarnspr.x=32
            yarnspr.y=-8
        else:
            collision=False
            
    if thumby.buttonA.pressed():
        
        if yarnspr.x<mousespr.x+8 and mousespr.x<yarnspr.x+8 and yarnspr.y<mousespr.y+8 and mousespr.y<yarnspr.y+8:
            collision=True
            score+=5
            happyness+=2
            thumby.audio.playBlocking(2000,30)
            time.sleep(1)
            if micespr.x==32:
                catspr.x=yarnspr.x
                catspr.y=yarnspr.y
            elif yarnspr.x==32:
                catspr.x=micespr.x
                catspr.y=micespr.y
            micespr.x=32
            micespr.y=-8
            yarnspr.x=32
            yarnspr.y=-8
        else:
            collision=False
    

    
    #Display Score
    thumby.display.drawText("%d" % score,0,0,1)
    
    #Save Command
    if thumby.buttonA.pressed() and thumby.buttonB.justPressed():
        thumby.saveData.setItem("pscore", int(score))
        thumby.saveData.setItem("pcatx", int(catspr.x))
        thumby.saveData.setItem("pcaty", int(catspr.y))
        thumby.saveData.setItem("pgifts", int(gifts))
        thumby.saveData.setItem("pday", int(day))
        thumby.saveData.setItem("phappyness", int(happyness))
        thumby.saveData.save()
        time.sleep(1)
        thumby.audio.play(3000,60)
        thumby.audio.play(2000,60)
        thumby.audio.play(1000,80)
        thumby.audio.play(2000,60)
        thumby.audio.play(3000,60)
        thumby.display.drawText("Saved.", 20,0,1)
        thumby.display.update()
        time.sleep(1)
    
    thumby.display.drawSprite(mousespr)
    thumby.display.drawSprite(catspr)
    thumby.display.drawSprite(micespr)
    thumby.display.drawSprite(yarnspr)
    thumby.display.drawSprite(giftspr)
    thumby.display.update()
    #oscore = int(thumby.saveData.getItem("pscore"))
    #if(oscore < score):
    #    
