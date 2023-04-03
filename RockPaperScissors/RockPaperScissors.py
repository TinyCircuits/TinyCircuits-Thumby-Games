"""
This work is licensed under the Creative Commons Attribution-ShareAlike 3.0 Unported License. 
To view a copy of this license, visit http://creativecommons.org/licenses/by-sa/3.0/ or send a letter to Creative Commons, PO Box 1866, Mountain View, CA 94042, USA.
"""
import random
import thumby
import math
import time

RPS_MOVES = [
    "Rock",
    "Paper",
    "Scissors"
]

def showscore(userscore,aiscore):
    thumby.display.fill(0)
    thumby.display.drawText("Your score="+str(userscore),0,0,1)
    thumby.display.drawText("AI score="+str(aiscore),5,20,1)
    thumby.display.update()
    time.sleep(2)

def showresult(ai, user, winner):
    thumby.display.fill(0)
    thumby.display.drawText("AI: {}".format(ai),0,0,1)
    thumby.display.drawText("You: {}".format(user),0,9,1)
    thumby.display.drawText("Winner: {}".format(winner),0,18,1)
    thumby.display.drawText("You:"+str(userscore)+" Ai:"+str(aiscore),5,27,1)
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

thumby.display.fill(0)
thumby.display.drawText("Rock",23,0,1)
thumby.display.drawText("Paper",21,9,1)
thumby.display.drawText("Scissors",12,18,1)
thumby.display.drawText("Oliver2402",7,27,1)
thumby.display.update()
time.sleep(3)

while True:
    userscore=0
    aiscore=0
    while aiscore<9 and userscore<9:
        aichoice = random.randint(0,2)
        buttonPushed=False
        thumby.display.fill(0)
        thumby.display.drawText("left=rock",8,0,1)
        thumby.display.drawText("up=paper",12,9,1)
        thumby.display.drawText("right=scisor",0,18,1)
        thumby.display.update()
        userchoice = None
        while userchoice is None:
            if thumby.buttonL.justPressed():
                userchoice=0
            if thumby.buttonU.justPressed():
                userchoice=1
            if thumby.buttonR.justPressed():
                userchoice=2
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