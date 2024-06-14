"""
This work is licensed under the Creative Commons Attribution-ShareAlike 3.0 Unported License. 
To view a copy of this license, visit http://creativecommons.org/licenses/by-sa/3.0/ or send a letter to Creative Commons, PO Box 1866, Mountain View, CA 94042, USA.
"""
import random
import thumby
import math
import time
thumby.display.setFPS(60)

SpaceshipLoop=1

#Bitmaps
# BITMAP: width: 10, height: 10
RockMap = bytearray([112,204,34,25,70,33,18,2,156,96,
           0,1,2,2,1,2,1,1,0,0])
# BITMAP: width: 10, height: 10
PaperMap = bytearray([0,63,245,213,85,85,85,127,224,0,
           0,0,0,3,3,3,3,3,3,3])
# BITMAP: width: 10, height: 10
ScissorsMap = bytearray([195,38,172,216,112,112,216,172,38,195,
           1,3,1,0,0,0,0,1,3,1])
# BITMAP: width: 10, height: 15
SpaceshipMap = bytearray([0,0,252,2,25,25,2,252,0,0,
           12,14,121,40,72,40,72,121,14,12])

#Initiating Bitmaps
RockSprite = thumby.Sprite(10, 10, RockMap)
PaperSprite = thumby.Sprite(10, 10, PaperMap)
ScissorsSprite = thumby.Sprite(10, 10, ScissorsMap)
SpaceshipSprite = thumby.Sprite(10, 15, SpaceshipMap)

RPS_MOVES = [
    "Rock",
    "Paper",
    "Scissors"
]

def showresult(ai, user, winner):
    thumby.display.fill(0)
    thumby.display.drawText("AI:",23,2,1)
    thumby.display.drawText("You:",17,12,1)
    winnerlinex = 7 if winner=="AI" else 3
    thumby.display.drawText("Winner: {}".format(winner),winnerlinex,23,1)
    thumby.display.drawText("You:"+str(userscore)+" Ai:"+str(aiscore),6,32,1)
    Sprite_Results(userchoice, aichoice)
    thumby.display.update()
    time.sleep(3)

def rpstostr(rps):
    if(rps<0 or rps>2):
        raise ValueError("Invalid move integer value.")
    return RPS_MOVES[rps]

def get_result_str(winner):
    if winner==0:
        return "Tie"
    elif winner==1:
        return "AI"
    else:
        return "You"

def who_won(p1, p2):
    diff = p2-p1
    if diff==1 or diff==-2:
        return 2
    elif diff==2 or diff==-1:
        return 1
    elif diff==0:
        return 0

def Sprite_Results(userchoice, aichoice):
    choices=[RockSprite, PaperSprite, ScissorsSprite]
    aisprite = choices[aichoice]
    usersprite = choices[userchoice]
    aisprite.x=40
    aisprite.y=1
    thumby.display.drawSprite(aisprite)
    usersprite.x=40
    usersprite.y=12
    thumby.display.drawSprite(usersprite)
   
"""
Hidden Game
"""
def CollisionGame(SpaceshipLoop):
    SpaceshipSprite.x = 10
    SpaceshipSprite.y = 20
    while SpaceshipLoop==1:
        thumby.display.fill(0)
        #Inputs
        if thumby.buttonU.pressed():
            SpaceshipSprite.y-=0.5
        if thumby.buttonD.pressed():
            SpaceshipSprite.y+=0.5
        if thumby.buttonR.pressed():
            SpaceshipSprite.x+=0.5
        if thumby.buttonL.pressed():
            SpaceshipSprite.x-=0.5
        #Wall Collision detection
        #Left Wall
        if SpaceshipSprite.x<0:
            SpaceshipSprite.x=0.5
        #Top Wall
        if SpaceshipSprite.y<0:
            SpaceshipSprite.y=0.5
        #Right Wall
        if SpaceshipSprite.x>62:
            SpaceshipSprite.x=62
        #Bottom Wall
        if SpaceshipSprite.y>28:
            SpaceshipSprite.y=28
        #Drawing On Screen
        thumby.display.drawSprite(SpaceshipSprite)
        thumby.display.update()
    
thumby.display.fill(0)
thumby.display.drawText("Rock",23,2,1)
thumby.display.drawText("Paper",21,11,1)
thumby.display.drawText("Scissors",12,20,1)
thumby.display.drawText("Oliver2402",7,29,1)
thumby.display.update()
time.sleep(3)

while True:
    userscore=0
    aiscore=0
    while aiscore<9 and userscore<9:
        aichoice = random.randint(0,2)
        buttonPushed=False
        thumby.display.fill(0)
        #Text Displaying
        thumby.display.drawText("left=",8,5,1)
        thumby.display.drawText("up=",20,16,1)
        thumby.display.drawText("right=",2,28,1)
        #Setting Positioning for Sprites (Changed in another function)
        RockSprite.x = 40
        RockSprite.y = 4
        PaperSprite.x = 40
        PaperSprite.y = 16
        ScissorsSprite.x = 40
        ScissorsSprite.y = 28
        #Sprite Displaying
        thumby.display.drawSprite(RockSprite)
        thumby.display.drawSprite(PaperSprite)
        thumby.display.drawSprite(ScissorsSprite)
        thumby.display.update()
        userchoice = None
        while userchoice is None:
            if thumby.buttonL.justPressed():
                userchoice=0
            if thumby.buttonU.justPressed():
                userchoice=1
            if thumby.buttonR.justPressed():
                userchoice=2
            if thumby.buttonD.justPressed():
                CollisionGame(SpaceshipLoop)
        winner = who_won(aichoice, userchoice)
        result_str = get_result_str(winner)
        if winner==1:
            aiscore = aiscore+1
        elif winner==2:
            userscore=userscore+1
        showresult(rpstostr(aichoice), rpstostr(userchoice), result_str)
    if userscore==9:
        thumby.display.fill(0)
        thumby.display.drawText("You won!",11,0,1)
        thumby.display.drawText("Got 9 points",0,9,1)
        thumby.display.drawText("AI "+str(aiscore)+" points",3,18,1)
        thumby.display.update()
        time.sleep(4)
    else:
        thumby.display.fill(0)
        thumby.display.drawText("You lost!",11,0,1)
        thumby.display.drawText("Got "+str(userscore)+" points",0,9,1)
        thumby.display.drawText("AI 9 points",3,18,1)
        thumby.display.update()
        time.sleep(4)
    if userscore==9 or aiscore==9:
        while (1):
            thumby.display.fill(0)
            thumby.display.drawText('Game Over!',6,0,1)
            thumby.display.drawText('A:Play Again',0,14,1)
            thumby.display.drawText('B:Quit',0,28,1)
            thumby.display.update()
            if thumby.buttonA.pressed():
                time.sleep(.5)
                break
            if thumby.buttonB.pressed():
                thumby.reset()