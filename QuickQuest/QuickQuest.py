import time
import thumby
import math
import machine
import random

thumby.display.setFPS(30)
random.seed(time.ticks_ms())

UII1 = bytearray([12,12,63,63,12,12])
UII2 = bytearray([30,35,53,53,35,30])
UII3 = bytearray([6,15,31,62,31,15,6])
UII4 = bytearray([4,46,107,42,58,16])
UII5 = bytearray([30,53,39,39,53,30])

UI1 = thumby.Sprite(6,6,UII1,0,34)
UI2 = thumby.Sprite(6,6,UII2,66,34)
UI3 = thumby.Sprite(7,6,UII3,35,9)
UI4 = thumby.Sprite(6,7,UII4,36,16)
UI5 = thumby.Sprite(6,6,UII5,36,25)

EImage1 = bytearray([0,0,0,0,0,0,0,0,0,4,134,134,142,206,206,204,108,24,68,194,128,128,0,0,0,0,0,0,0,0,0,0,192,192,192,192,192,192,192,192,252,7,1,0,2,21,47,127,191,127,255,127,255,255,255,126,252,192,192,192,192,192,192,192,31,15,15,15,15,15,7,7,7,7,6,4,8,8,16,16,16,16,48,56,56,60,62,63,63,63,63,63,63,63,63,63])
EImage2 = bytearray([0,0,0,1,1,3,3,2,52,56,28,204,196,164,244,176,0,0,64,224,224,126,4,8,0,0,0,0,0,0,0,0,16,16,16,16,16,16,0,56,124,126,78,204,217,153,169,109,236,228,244,112,24,88,108,44,14,7,14,7,0,16,16,16,0,0,0,0,0,0,0,0,0,59,51,54,54,53,53,52,55,59,0,1,1,1,0,0,0,0,0,0,0,0,0,0])
EImage3 = bytearray([240,96,240,240,240,240,240,224,192,128,0,0,192,224,96,16,0,0,0,0,0,0,0,0,0,0,0,64,224,64,0,0,61,249,192,61,125,251,227,7,63,127,127,34,255,255,28,60,60,60,124,124,124,124,124,124,60,60,60,60,28,28,12,4,0,0,0,0,0,0,0,0,0,0,0,0,1,3,3,4,0,0,0,0,0,8,28,8,0,0,0,0,0,0,0,0])
EImage4 = bytearray([0,0,0,0,0,0,128,188,92,64,160,160,208,208,208,232,232,232,232,200,200,136,136,16,16,144,160,160,192,0,0,0,4,4,4,8,8,9,126,126,99,227,227,255,255,7,7,7,7,255,255,255,255,255,129,129,129,64,64,127,8,8,8,8,0,0,0,0,0,32,0,32,8,16,4,32,10,0,34,0,8,1,1,1,1,1,0,0,0,0,0,0,0,0,0,0])
EImage5 = bytearray([255,255,255,255,127,127,127,127,127,127,99,65,227,255,255,255,255,255,255,255,255,255,31,15,63,255,227,129,227,255,255,255,128,144,208,192,192,208,194,192,194,192,128,130,128,128,0,0,33,1,33,3,3,3,3,6,7,7,7,7,15,47,47,15,63,63,63,63,63,63,63,63,63,63,63,63,63,63,63,63,62,62,62,60,60,61,57,56,56,58,50,48,48,48,32,32])
EImage6 = bytearray([0,0,0,0,0,192,32,35,39,230,254,254,252,204,204,136,152,152,16,240,240,32,96,96,64,192,192,0,0,0,0,0,0,0,0,0,0,255,0,0,0,205,255,131,123,1,6,6,14,13,9,3,255,255,106,0,0,0,0,0,0,0,0,0,0,0,0,0,0,15,16,16,16,21,23,23,23,22,22,20,20,20,20,22,23,22,15,0,0,0,0,0,0,0,0,0])
EImage7 = bytearray([255,200,255,255,0,156,248,120,240,240,240,240,120,248,28,192,240,240,0,255,244,255,254,135,255,0,240,240,252,223,143,3,255,255,111,255,0,3,7,14,30,23,23,222,238,247,59,156,31,15,0,255,255,255,255,246,255,0,31,31,127,255,255,254,63,63,4,63,0,0,0,32,48,56,30,15,7,0,62,63,14,0,0,63,2,63,63,15,63,0,0,0,32,48,57,63])
EImage8 = bytearray([0,0,0,0,192,208,216,248,220,220,252,252,252,252,252,252,220,220,220,252,220,252,252,124,140,244,124,120,160,0,0,0,192,192,192,0,181,181,245,245,245,245,245,197,181,165,181,197,245,245,245,245,245,245,181,4,250,250,253,125,190,0,192,192,63,63,63,32,45,45,45,47,45,45,47,45,47,47,47,47,47,47,47,45,47,45,45,32,55,55,59,59,61,60,63,63])
EImage9 = bytearray([255,255,63,159,127,55,23,227,241,209,81,81,113,115,227,87,55,255,255,255,255,255,255,63,31,7,7,31,63,255,255,3,223,47,232,197,23,126,254,254,247,247,202,142,143,199,199,238,110,14,145,127,255,241,245,245,244,244,244,180,117,245,245,244,63,63,60,51,47,28,56,49,35,35,39,39,39,39,38,50,57,28,15,48,62,61,59,55,47,31,17,0,0,0,17,31])
EImage10 = bytearray([0,0,0,0,0,0,0,0,224,240,248,56,188,124,252,60,252,60,184,120,240,224,0,0,0,0,0,0,0,0,0,0,0,0,0,128,0,0,0,255,255,255,255,188,126,253,255,252,255,252,254,255,255,255,255,0,0,0,0,0,0,0,0,0,0,8,12,8,15,8,8,15,15,15,15,7,6,1,3,1,7,15,7,3,3,0,7,8,12,14,8,8,8,0,0,0])
EImage11 = bytearray([254,130,0,0,0,0,0,161,225,243,254,125,254,200,216,240,224,64,2,14,252,248,240,224,128,0,0,0,0,0,0,0,231,247,250,186,28,60,252,254,255,255,255,254,252,248,248,52,108,236,222,191,191,191,63,127,255,254,240,0,0,2,28,240,0,1,0,33,56,62,63,63,63,63,31,15,31,63,63,63,60,56,33,4,13,12,29,24,25,27,25,28,12,14,7,3])
EImage12 = bytearray([15,7,15,31,191,255,255,63,143,135,131,131,131,129,129,129,129,129,1,1,3,3,7,31,255,255,191,31,15,7,15,31,0,2,0,0,3,3,3,3,63,125,252,160,171,175,191,252,252,253,127,126,188,14,92,224,131,3,3,0,0,0,2,0,0,0,0,0,0,0,0,0,32,24,4,2,1,5,13,13,12,14,6,7,3,0,0,0,0,1,2,12,16,0,0,0])

TitleI = bytearray([192,64,192,0,0,0,0,0,192,0,0,0,0,0,192,0,0,0,220,95,220,0,0,0,0,0,0,0,0,0,0,0,0,0,192,0,255,0,255,0,254,0,254,0,254,0,254,2,134,0,255,120,134,0,255,0,255,0,254,0,254,0,254,18,158,0,140,18,230,0,255,2,1,7,5,0,5,5,5,4,5,4,5,5,5,4,37,20,21,20,241,87,245,16,21,21,37,4,5,5,5,4,5,5,4,4,5,5,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,8,15,13,15,8,0,0,0,0,0,0,0,0,0,0,0,0,0,0])

EventSprites = thumby.Sprite(32,22,EImage1+EImage2+EImage3+EImage4+EImage5+EImage6+EImage7+EImage8+EImage9+EImage10+EImage11+EImage12,0,9)
TitleSprite = thumby.Sprite(36,28,TitleI,18,0)

Day = 0
Health = 3
Wealth = 3
Happiness = 3
BHealth = 3.0
BWealth = 3.0
BHappiness = 3.0
BarSpeed = 0.03
MaxStat = 4
GameMode = 0
GTimer = 0
MadeChoice = 0
TopText = ""
TopTextGoal = ""
TotalEffect = 0

Script=[
["Singing bard",1,"Cheer","Boo","Jaunty tune!","He's crying.",0,0,1,0,0,-1],
["An apple?",0,"Buy","Leave","Poisoned!","Best not.",-1,-1,0,0,0,0],
["An apple?",0,"Buy","Leave","Delicious!","Best not.",1,-1,1,0,0,0],
["Fast river",4,"Wade","Boat","Drowning!","Pricey!",-1,0,-1,0,-1,0],
["Old tavern",5,"Drink","Work","Party time!","Money made.",0,-1,1,0,1,-1,],
["Quiet shack",3,"Rest","Loot","Nice nap.","A rare coin!",1,0,0,0,1,0],
["A robbery!",2,"Fight","Pay","Hard battle.","Oh well.",-1,0,0,0,-1,0],
["Wood spirit",6,"Fight","Bow","Soul rend!","Respectful.",-2,0,0,0,0,0],
["Dire wolf!",6,"Fight","Pet","Hard battle.","Good pup.",-1,0,0,0,0,1],
["Dwarf beer?",5,"Drink","Nope","So strong!","Sad dwarf",-1,0,1,0,0,-1],
["Fast river",4,"Wade","Boat","Easy peasy.","Pricey!",0,0,0,0,-1,0],
["Wailing bard",1,"Listen","Boo","Awful tune!","Silence.",0,0,-1,0,0,0],
["Fishing spot",4,"Okay","Nope","No nibbles.","Moving on.",0,0,-1,0,0,0],
["Fishing spot",4,"Okay","Nope","A goldfish!","Moving on.",0,1,0,0,0,0],
["Fishing spot",4,"Okay","Nope","A clownfish!","Moving on.",0,0,1,0,0,0],
["Spooky shack",3,"Rest","Loot","Foul dreams.","Only dust.",0,0,-1,0,0,0],
["A hideout",3,"Rest","Loot","Nice nap.","Booby trap!",1,0,0,-1,0,0],
["Marauder!",2,"Fight","Beg","Hard battle.","Embarrassing",-1,0,0,0,0,-1],
["Treasure?",7,"Loot","Nope","Gah! Mimic!","Regret...",-1,0,0,0,0,-1],
["Treasure?",7,"Loot","Nope","A rare coin!","Regret...",0,1,0,0,0,-1],
["Treasure?",7,"Loot","Nope","Jackpot!","Regret...",0,2,0,0,0,-1],
["Potion?",8,"Buy","Nope","Recovered!","Not today.",2,-1,0,0,0,0],
["Joke book?",8,"Buy","Nope","Delightful!","Not today.",0,-1,2,0,0,0],
["A lit bomb?",8,"Buy","NO!","BOOM!","Dangerous!",-1,-1,0,0,0,0],
["Berserker!",2,"Fight","Beg","Hard battle.","Embarrassing",-1,0,0,0,0,-1],
["You died...",9,"","Try again?","","Once more...",0,0,0,0,0,0],
["Toll road!",2,"Pay","Detour","Rip-off!","Long walk.",0,-1,0,0,0,-1],
["",99,"","New game","","",0,0,0,0,0,0],
["Keep up your",99,"","Adventure!","","",0,0,0,0,0,0],
["A dragon!",10,"Talk","Fight","Small talk!","You clash!",0,0,-1,-1,0,0],
["Not done yet",10,"Talk","Fight","Bargaining!","You strike!",0,0,-1,-1,0,0],
["Once more!",10,"Talk","Fight","Negotiation!","Fatal blow!",0,0,-1,-1,0,0],
["Thank ye.",11,"OK","Reward","Best be off.","Coin for ye.",0,0,0,0,1,0],
["Slay dragon?",11,"OK","Nope","Godspeed.","But ye must!",0,0,0,0,0,0],
]

EventDeck = [0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,26] 
EventsRemaining = len(EventDeck)
CEvent = 27

MusicBass = [293,0,293,293,293,0,293,293,293,0,293,293,293,0,293,293,293,0,293,293,293,0,293,293,293,0,293,293,293,0,293,293,293,0,293,293,293,0,293,293,293,0,293,293,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
MusicMelody = [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,587,587,0,0,0,880,880,0,783,783,783,783,0,0,440,523,587,587,0,0,0,880,880,0,987,987,987,987,440,440,587,783,880,880,880,880,880,880,880,880,880,880,880,880,880,880,880,880]

MusicTimer = 0
MusicTimer2 = 0

while(True):
    #Draw UI
    thumby.display.fill(0)
    thumby.display.drawFilledRectangle(45, 10, int(26*BHealth/MaxStat), 3, 1)
    thumby.display.drawFilledRectangle(45, 18, int(26*BWealth/MaxStat), 3, 1)
    thumby.display.drawFilledRectangle(45, 26, int(26*BHappiness/MaxStat), 3, 1)
    thumby.display.setFont("/lib/font5x7.bin", 5, 7, 1)
    thumby.display.drawText(TopText, 0, 0, 1)
    thumby.display.drawText(Script[CEvent][2], 8, 33, 1)
    thumby.display.drawText(Script[CEvent][3], 64-6*len(Script[CEvent][3]), 33, 1)
    if Script[CEvent][1] != 99:
        thumby.display.drawSprite(EventSprites)
    if len(Script[CEvent][2])>0:
        thumby.display.drawSprite(UI1)
    thumby.display.drawSprite(UI2)
    thumby.display.drawSprite(UI3)
    thumby.display.drawSprite(UI4)
    thumby.display.drawSprite(UI5)
    
    #Bar animations
    if BHealth<Health:
        thumby.display.drawFilledRectangle(35, 9, 7, 7, 0)
        thumby.display.drawLine(36, 12, 40, 12, 1)
        thumby.display.drawLine(38, 10, 38, 14, 1)
        BHealth+=BarSpeed
        if BHealth>Health:
            BHealth = Health
    if BHealth>Health:
        thumby.display.drawFilledRectangle(35, 9, 7, 7, 0)
        thumby.display.drawLine(36, 12, 40, 12, 1)
        BHealth-=BarSpeed
        if BHealth<Health:
            BHealth = Health
    if BHappiness<Happiness:
        thumby.display.drawFilledRectangle(36, 25, 7, 7, 0)
        thumby.display.drawLine(36, 28, 40, 28, 1)
        thumby.display.drawLine(38, 26, 38, 30, 1)
        BHappiness+=BarSpeed
        if BHappiness>Happiness:
            BHappiness = Happiness
    if BWealth>Wealth:
        thumby.display.drawFilledRectangle(36, 16, 7, 7, 0)
        thumby.display.drawLine(36, 19, 40, 19, 1)
        BWealth-=BarSpeed
        if BWealth<Wealth:
            BWealth = Wealth
    if BWealth<Wealth:
        thumby.display.drawFilledRectangle(36, 16, 7, 7, 0)
        thumby.display.drawLine(36, 19, 40, 19, 1)
        thumby.display.drawLine(38, 17, 38, 21, 1)
        BWealth+=BarSpeed
        if BWealth>Wealth:
            BWealth = Wealth
    if BHappiness>Happiness:
        thumby.display.drawFilledRectangle(36, 25, 7, 7, 0)
        thumby.display.drawLine(36, 28, 40, 28, 1)
        BHappiness-=BarSpeed
        if BHappiness<Happiness:
            BHappiness = Happiness
    #Death event
    if CEvent == 25:
        thumby.display.drawFilledRectangle(30, 8, 42, 24, 0)
        if GameMode==1 or GameMode==2:
            thumby.display.drawText(str(Day)+" days", 30, 24, 1)
            thumby.display.drawText("from", 40, 8, 1)
            if Day>27:
                thumby.display.drawText("dragon", 32, 16, 1)
            else:
                if Health<1:
                    thumby.display.drawText("injury", 32, 16, 1)
                elif Wealth<1:
                    thumby.display.drawText("poverty", 30, 16, 1)
                elif Happiness<1:
                    thumby.display.drawText("sadness", 30, 16, 1)
                else:
                    thumby.display.drawText("old age", 30, 16, 1)
         
    #Fade in
    if GameMode == 0:
        thumby.display.drawFilledRectangle(0, 33, 72, 10, 0)
        thumby.display.drawFilledRectangle(0, 9, 32, 22-GTimer, 0)
        thumby.display.drawFilledRectangle(0, 9+GTimer, 32, 30, 0)
        GTimer+=1
        
        if GTimer>30:
            TopTextGoal = Script[CEvent][0]
            TopText = ""
            GTimer = 0
            GameMode = 1
            
    #Gameplay
    elif GameMode == 1:
        if GTimer < 10:
            GTimer+=1
        else:
            if thumby.actionPressed():
                GameMode = 2
                MadeChoice = 1
                GTimer = 0
            elif thumby.dpadPressed():
                if len(Script[CEvent][2])>0:
                    GameMode = 2
                    MadeChoice = 0
                    GTimer = 0
    #Flashing
    elif GameMode == 2:
        GTimer+=1
        if GTimer == 1:
            thumby.audio.play(261, 10)
        if GTimer == 3:
            thumby.audio.play(329, 10)
        if GTimer == 5:
            thumby.audio.play(392, 10)
        if GTimer == 7:
            thumby.audio.play(493, 10)
        if MadeChoice == 0:
             thumby.display.drawFilledRectangle(64-6*len(Script[CEvent][3]), 33, 60, 10, 0)
             if GTimer%2 == 0:
                 thumby.display.drawFilledRectangle(0, 33, 72, 10, 0)
        if MadeChoice == 1:
             if len(Script[CEvent][2])>0:
                thumby.display.drawFilledRectangle(0, 33, 8+6*len(Script[CEvent][2]), 10, 0)
             if GTimer%2 == 0:
                 thumby.display.drawFilledRectangle(0, 33, 72, 10, 0)
        if GTimer>30:
            TopTextGoal = Script[CEvent][4+MadeChoice]
            TopText = ""
            GTimer = 0
            Health += Script[CEvent][6+3*MadeChoice]
            Wealth += Script[CEvent][7+3*MadeChoice]
            Happiness += Script[CEvent][8+3*MadeChoice]
            TotalEffect = Script[CEvent][6+3*MadeChoice]+Script[CEvent][7+3*MadeChoice]+Script[CEvent][8+3*MadeChoice]
            if TotalEffect == 0:
                if Script[CEvent][6+3*MadeChoice] <0 or Script[CEvent][7+3*MadeChoice] <0 or Script[CEvent][8+3*MadeChoice] <0:
                    TotalEffect = -1
            if Health>MaxStat:
                Health = MaxStat
            if Wealth>MaxStat:
                Wealth = MaxStat
            if Happiness > MaxStat:
                Happiness = MaxStat
            GameMode = 3
            if CEvent == 27 or CEvent == 28:
                GameMode = 4
                GTimer=24
    #Consequences
    elif GameMode == 3:
        GTimer+=1
        if GTimer == 15:
            if TotalEffect<0:
                thumby.audio.play(493, 20)
            if TotalEffect>0:
                thumby.audio.play(415, 20)
        if GTimer == 20:
            if TotalEffect<0:
                thumby.audio.play(466, 20)
            if TotalEffect>0:
                thumby.audio.play(440, 20)
        if GTimer == 25:
            if TotalEffect<0:
                thumby.audio.play(440, 20)
            if TotalEffect>0:
                thumby.audio.play(466, 20)
        if GTimer == 30:
            if TotalEffect<0:
                thumby.audio.play(415, 20)
            if TotalEffect>0:
                thumby.audio.play(493, 20)
        if MadeChoice == 0:
             thumby.display.drawFilledRectangle(64-6*len(Script[CEvent][3]), 33, 60, 10, 0)
        if MadeChoice == 1:
            if len(Script[CEvent][2])>0:
                thumby.display.drawFilledRectangle(0, 33, 8+6*len(Script[CEvent][2]), 10, 0)
        if GTimer>60:
            GTimer = 0
            TopText = ""
            TopTextGoal = ""
            GameMode = 4
    #Refresh
    elif GameMode == 4:
        GTimer+=1
        thumby.display.drawFilledRectangle(0, 33, 72, 10, 0)
        thumby.display.drawFilledRectangle(0, 9, 32, GTimer, 0)
        thumby.display.drawFilledRectangle(0, 32-GTimer, 32, GTimer, 0)
        if GTimer > 24:
            GTimer = 0
            if CEvent == 25:
                #restart game
                
                Day = 0
                Health = 3
                Wealth = 3
                Happiness = 3
                BHealth = 3.0
                BWealth = 3.0
                BHappiness = 3.0
                EventDeck = [0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,26] 
                EventsRemaining = len(EventDeck)
                CEvent = 33
                EventSprites.setFrame(Script[CEvent][1])
                GameMode = 0
            elif CEvent == 27:
                #Title screen over
                GTimer = -40
                CEvent = 28
                GameMode = 5
                TopTextGoal = ""
                TopText = ""
            elif CEvent == 28:
                #Tutorial over
                CEvent = 33
                GameMode = 0
                TopTextGoal = ""
                TopText = ""
                EventSprites.setFrame(Script[CEvent][1])
            else:
                Day+=1
                if Health < 1 or Wealth < 1 or Happiness < 1:
                    CEvent = 25
                    MusicTimer2 = 48
                    EventSprites.setFrame(Script[CEvent][1])
                elif EventsRemaining == 0:
                    #If dragon1
                    if CEvent == 29:
                        CEvent = 30
                    #If dragon2
                    elif CEvent == 30:
                        CEvent = 31
                    #If dragon3
                    elif CEvent == 31:
                        CEvent = 32
                    #If thank ye
                    elif CEvent == 32:
                        GameMode = 6
                        TopTextGoal = "  The end!"
                        TopText = ""
                    #Start of dragons
                    else:
                        CEvent = 29
                    EventSprites.setFrame(Script[CEvent][1])
                else:
                    EventsRemaining-=1
                    CEvent = EventDeck[random.randint(0,EventsRemaining)]
                    EventSprites.setFrame(Script[CEvent][1])
                    EventDeck.remove(CEvent)
                if GameMode != 6:
                    GameMode = 0
    #Tutorial
    if GameMode == 5:
        GTimer+=1
        if GTimer == 0:
            TopTextGoal = "Keep up your"
            TopText = ""
        if GTimer == 40:
            TopTextGoal = "Health,"
            TopText = ""
        if GTimer == 80:
            TopTextGoal = "Wealth,"
            TopText = ""
        if GTimer == 120:
            TopTextGoal = "Happiness."
            TopText = ""
        if GTimer == 160:
            TopTextGoal = "Got it?"
            TopText = ""
        if GTimer < 40:
            thumby.display.drawFilledRectangle(34, 8, 38, 24, 0)
        elif GTimer < 80:
            thumby.display.drawFilledRectangle(34, 15, 38, 17, 0)
        elif GTimer < 120:
            thumby.display.drawFilledRectangle(34, 24, 38, 8, 0)
        if GTimer < 160:
            thumby.display.drawFilledRectangle(0, 33, 72, 10, 0)
        else:
            if thumby.actionPressed():
                GameMode = 2
                GTimer = 0
    #The end
    if GameMode == 6:
        GTimer+=1
        
        thumby.display.drawFilledRectangle(0, 9, 72, 50, 0)
        if GTimer > 120:
            GTimer = 0
            Day = 0
            Health = 3
            Wealth = 3
            Happiness = 3
            BHealth = 3.0
            BWealth = 3.0
            BHappiness = 3.0
            EventDeck = [0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,26] 
            EventsRemaining = len(EventDeck)
            CEvent = 27
            GameMode = 0
    #Game over music
    if CEvent == 25:
        if GameMode<2:
            if MusicTimer<57:
                if MusicBass[MusicTimer] > 0:
                    thumby.audio.play(int(MusicBass[MusicTimer]*0.5), 50)
                if MusicMelody[MusicTimer] > 0:
                    thumby.audio.play(int(MusicMelody[MusicTimer]*0.5), 200)
                MusicTimer2+=1
                if MusicTimer2%6 == 0:
                    MusicTimer = int(MusicTimer2/6)
                else:
                    MusicTimer = 1
        else:
            MusicTimer=0
            MusicTimer2 = 0
    #Title screen
    if CEvent == 27:
        thumby.display.drawFilledRectangle(0, 0, 72, 31, 0)
        thumby.display.drawSprite(TitleSprite)
        
        if GameMode<2:
            if MusicTimer<57:
                if MusicBass[MusicTimer] > 0:
                    thumby.audio.play(293, 10)
                if MusicMelody[MusicTimer] > 0:
                    thumby.audio.play(MusicMelody[MusicTimer], 100)
                MusicTimer2+=1
                if MusicTimer2%3 == 0:
                    MusicTimer = int(MusicTimer2/3)
                else:
                    MusicTimer = 1
            
        else:
            MusicTimer=0
            MusicTimer2 = 0
    if len(TopTextGoal) > len(TopText):
        thumby.audio.play(196, 5)
        TopText = TopTextGoal[:len(TopText)+1]
            

    thumby.display.update()