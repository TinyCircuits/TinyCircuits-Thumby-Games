# Slot Machine

# Step into the glitzy world of classic casino fun 
# with the Slot Machine Arcade Game on your Thumby handheld console.
# This compact yet captivating game brings the thrill 
# of Las Vegas right to your fingertips, all on a tiny screen!

# Written by Iakov Korotenko
# Last edited summer 2024

'''
    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with this program.  If not, see <https://www.gnu.org/licenses/>.
'''

import time
import thumby
import random

# BITMAP: width: 72, height: 40
TITLE = bytearray([0,0,0,224,248,248,152,152,152,152,128,128,128,128,0,0,0,224,248,124,12,0,0,0,0,0,128,240,248,28,28,12,252,248,120,0,0,0,48,56,24,28,252,252,12,12,12,12,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,
            0,0,0,1,3,3,27,27,25,25,25,25,31,31,15,0,0,31,31,24,24,28,12,0,0,0,3,15,14,12,12,14,15,7,0,0,0,0,0,0,14,15,7,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,
            0,0,0,0,192,240,126,62,120,120,124,30,126,254,224,0,0,0,128,224,254,126,254,224,192,128,0,254,255,7,15,14,12,0,0,14,254,252,96,96,252,254,14,0,0,128,254,254,0,0,231,255,254,56,240,224,255,255,254,0,124,254,239,103,99,99,99,0,0,0,0,0,
            0,0,0,15,15,3,0,0,0,0,0,0,0,7,15,14,0,0,15,15,3,3,3,1,15,15,0,7,7,6,6,6,7,7,0,6,15,15,0,0,15,15,6,0,0,7,15,15,0,0,3,15,15,0,0,1,15,15,1,0,0,15,15,14,14,14,14,12,0,0,0,0,
            0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0])

# BITMAP: width: 16, height: 80
ICONS_01 = bytearray([255,255,227,235,235,235,235,235,107,171,219,123,131,255,255,255,
           255,255,255,255,255,131,189,134,251,253,254,255,255,255,255,255,
           255,199,23,247,119,151,231,119,183,231,151,119,247,23,199,255,
           255,255,254,252,249,243,243,241,242,243,243,249,252,254,255,255,
           255,255,255,255,7,251,253,253,253,253,251,7,255,255,255,255,
           255,243,237,236,238,239,207,175,175,175,207,238,236,237,243,255,
           255,255,255,255,255,127,135,235,219,187,127,127,127,255,255,255,
           255,241,238,238,238,241,255,255,249,246,239,239,239,246,249,255,
           255,255,143,7,115,115,1,115,1,115,115,115,255,255,255,255,
           255,255,255,207,206,206,128,206,128,206,206,192,224,241,255,255])
# BITMAP: width: 16, height: 80 
ICONS_02 = bytearray([255,255,227,235,235,235,235,235,107,171,219,123,131,255,255,255,
           255,255,255,255,255,131,189,134,251,253,254,255,255,255,255,255,
           255,199,23,247,119,151,231,119,183,231,151,119,247,23,199,255,
           255,255,254,252,249,243,243,241,242,243,243,249,252,254,255,255,
           255,255,255,255,7,251,253,253,253,253,251,7,255,255,255,255,
           255,243,237,236,238,239,207,175,175,175,207,238,236,237,243,255,
           255,255,255,255,255,127,135,235,219,187,127,127,127,255,255,255,
           255,241,238,238,238,241,255,255,249,246,239,239,239,246,249,255,
           255,255,143,7,115,115,1,115,1,115,115,115,255,255,255,255,
           255,255,255,207,206,206,128,206,128,206,206,192,224,241,255,255])

COMBINATIONS =[
    "Any 2 symbols",
    " 2 x bet",
    ""
    "Any 3 symbols",
    " 10 x bet"]

thumby.display.setFPS(30)
random.seed(time.ticks_ms())

scene = 0 #MENU
thumby.display.setFont("/lib/font3x5.bin", 3, 5, 1)

class MenuScene():
    def __init__(self):
        self.titleSprite = thumby.Sprite(72,40,TITLE,0,0)   


    def update(self):
        global scene
        thumby.display.drawSprite(self.titleSprite)
        thumby.display.drawText("A-Game B-Info", 5, 30, 1)
        if (thumby.buttonA.justPressed()):
            thumby.display.drawFilledRectangle(0,0,72,40,0)
            thumby.display.drawText("Let's get ready!", 5, 20, 1)
            thumby.display.update()
            time.sleep(2)
            scene = 1 #GAME
            
        thumby.display.update()    

class GameScene():
    
    def __init__(self):
        self.CODE_0 = {-6:"7",-5:"7",-4:"L",-3:"R",-2:"C",-1:"D",0:"7",1:"L",2:"R",3:"C", 4:"D", 5:"7", 6:"L"}
        self.CODE_1 = {-6:"7",-5:"7",-4:"L",-3:"R",-2:"C",-1:"D",0:"7",1:"L",2:"R",3:"C", 4:"D", 5:"7", 6:"L"}
        self.CODE_2 = {-6:"7",-5:"7",-4:"L",-3:"R",-2:"C",-1:"D",0:"7",1:"L",2:"R",3:"C", 4:"D", 5:"7", 6:"L"}
        self.iconsSprite01 = thumby.Sprite(16,80, ICONS_01,0,0)
        self.iconsSprite02 = thumby.Sprite(16,80, ICONS_02, 0, -80)
        self.iconsSprite11 = thumby.Sprite(16,80, ICONS_01,17,0)
        self.iconsSprite12 = thumby.Sprite(16,80, ICONS_02, 17, -80)
        self.iconsSprite21 = thumby.Sprite(16,80, ICONS_01, 34, 0)
        self.iconsSprite22 = thumby.Sprite(16,80, ICONS_02, 34, -80)
        
        self.ySpeed0 = 0
        self.ySpeed1 = 0
        self.ySpeed2 = 0
        self.friction = 0.07
        self.combinationOffset = 40
        
        self.cash = 100
        self.bet = 10
        self.spin = 0
        self.running = False
        self.winDialog = False
        self.loseDialog = False
        self.legendDialog = False
        self.over = False
        self.lastCombination=""
        
    def update(self):    
        global scene
        self.checkButtons()
        if (self.running and self.isWillStop()): #game just finished
            self.running = False
            self.lastCombination = self.getCombination()
            self.price = self.calculatePrice()
            self.cash += self.price
            if (self.cash <=0):
                self.over = True
            elif (self.price>0):
                self.winDialog = True
            else:
                self.loseDialog = True
            
        if (self.legendDialog):
            self.drawLegend()
        elif (self.winDialog):
            self.drawWin()
        elif (self.loseDialog):
            self.drawLose()
        elif (self.over):
            self.drawOver()    
        else: 
            self.calculateGame()
            self.drawGame()
            
    def checkButtons(self):   
        if (thumby.buttonA.justPressed()):
            if (self.winDialog or self.loseDialog):
                self.winDialog = False
                self.loseDialog = False
            elif (self.over):
                thumby.reset()
            elif (not self.running):
                self.ySpeed0 = 5.8 + random.random()*3
                self.ySpeed1 = 7.1 + random.random()*5
                self.ySpeed2 = 9.2 + random.random()*7
                self.running = True
                self.spin += 1
        
        self.legendDialog = thumby.buttonB.pressed()
        if (thumby.buttonU.justPressed() and self.isWillStop() ):
            betDif = self.cash // 10
            if(self.bet+betDif<=self.cash):
                self.bet+=betDif;
            else:
                self.bet = self.cash
                
        if (thumby.buttonD.justPressed() and self.isWillStop() ):
            if(self.bet>=10):
                self.bet-=5
            else:     
                self.bet = self.cash
    
    def getCombination(self):
        pos0=(20-self.iconsSprite01.y)//16
        pos1=(20-self.iconsSprite11.y)//16
        pos2=(20-self.iconsSprite21.y)//16
        return self.CODE_0[pos0]+self.CODE_1[pos1]+self.CODE_2[pos2]
        
    def calculatePrice(self):
        if ((self.lastCombination[0]==self.lastCombination[1] 
            and not self.lastCombination[0]==self.lastCombination[2])
            or
            (self.lastCombination[0]==self.lastCombination[2] 
            and not self.lastCombination[0]==self.lastCombination[1])
            or
            (self.lastCombination[1]==self.lastCombination[2] 
            and not self.lastCombination[1]==self.lastCombination[0])):
                return 2 * self.bet   #ANY 2
        elif(self.lastCombination[0]==self.lastCombination[1] 
            and self.lastCombination[0]==self.lastCombination[2]):
                return 10 * self.bet  #ANY 3
        else:        
            return -self.bet
        
    def isWillStop(self):
        return (self.ySpeed0 == 0 and self.ySpeed1 == 0 and self.ySpeed2 ==0)
        
    def calculateGame(self):            
        if (self.iconsSprite01.y > 80):
            self.iconsSprite01.y = -80
            self.iconsSprite02.y = 0
            
        if (self.iconsSprite02.y > 80):
            self.iconsSprite02.y = -80
            self.iconsSprite01.y = 0
            
        if (self.iconsSprite11.y > 80):
            self.iconsSprite11.y = -80
            self.iconsSprite12.y = 0
            
        if (self.iconsSprite12.y > 80):
            self.iconsSprite12.y = -80 
            self.iconsSprite11.y = 0
            
        if (self.iconsSprite21.y > 80):
            self.iconsSprite21.y = -80
            self.iconsSprite22.y = 0
            
        if (self.iconsSprite22.y > 80):
            self.iconsSprite22.y = -80  
            self.iconsSprite21.y = 0
            
            
        print (str(self.iconsSprite01.y)+":"+str(self.iconsSprite01.y % 20))
            
        if (abs(self.iconsSprite01.y % 16) < 2 and self.ySpeed0 < 2):
            self.ySpeed0 = 0
            
        if (abs(self.iconsSprite11.y % 16) < 2 and self.ySpeed1 < 2):
            self.ySpeed1 = 0
            
        if (abs(self.iconsSprite21.y % 16) < 2 and self.ySpeed2 < 2):
            self.ySpeed2 = 0    
            
        self.iconsSprite01.y += self.ySpeed0
        self.iconsSprite02.y += self.ySpeed0
        
        self.iconsSprite11.y += self.ySpeed1
        self.iconsSprite12.y += self.ySpeed1
        
        self.iconsSprite21.y += self.ySpeed2
        self.iconsSprite22.y += self.ySpeed2
        
        if(self.ySpeed0 > 0):
            self.ySpeed0 -= self.friction
        else:
            self.ySpeed0= 0
        
        if(self.ySpeed1 > 0):
            self.ySpeed1 -= self.friction
        else:
            self.ySpeed1= 0
            
        if(self.ySpeed2 > 0):
            self.ySpeed2 -= self.friction
        else:
            self.ySpeed2= 0    
            
            
            
    def drawWin(self):        
        thumby.display.drawFilledRectangle(0,0,72,40,1)
        thumby.display.drawText("YOU WIN", 23, 5, 0)
        thumby.display.drawText("Cash: "+str(self.cash)+"$", 20, 15, 0)
        thumby.display.drawText("Bet: "+str(self.bet)+"$", 20, 25, 0)
        # thumby.display.drawText(self.lastCombination, 50, 25, 0)
        thumby.display.drawText("Press A", 20, 32, 0)
        thumby.display.update()
        
        
    def drawLose(self):        
        thumby.display.drawFilledRectangle(0,0,72,40,1)
        thumby.display.drawText("YOU LOSE", 23, 5, 0)
        thumby.display.drawText("Cash: "+str(self.cash)+"$", 20, 15, 0)
        thumby.display.drawText("Bet: "+str(self.bet)+"$", 20, 25, 0)
        thumby.display.drawText("Press A", 20, 32, 0)
        thumby.display.update()
        
        
    def drawGame(self):        
        thumby.display.drawFilledRectangle(0,0,72,40,1)
        thumby.display.drawSprite(self.iconsSprite01)
        thumby.display.drawSprite(self.iconsSprite02)
        thumby.display.drawSprite(self.iconsSprite11)
        thumby.display.drawSprite(self.iconsSprite12)
        thumby.display.drawSprite(self.iconsSprite21)
        thumby.display.drawSprite(self.iconsSprite22)
        thumby.display.drawText("Cash", 50, 0, 0)
        thumby.display.drawText(str(self.cash)+"$", 55, 10, 0)
        thumby.display.drawText("Bet", 50, 20, 0)
        thumby.display.drawText(str(self.bet)+"$", 55, 30, 0)
        thumby.display.update()    
    
    def drawLegend(self):    
        thumby.display.drawFilledRectangle(0,0,72,40,0)
        thumby.display.drawFilledRectangle(1,1,70,38,1)
        for i in range(len(COMBINATIONS)):
            thumby.display.drawText(COMBINATIONS[i], 5, self.combinationOffset+i*10, 0)
        if (self.combinationOffset < -50):
            self.combinationOffset = 40
        else:    
            self.combinationOffset -= 1    
        thumby.display.update()   
        
    def drawOver(self):    
        thumby.display.drawFilledRectangle(1,1,70,38,0)
        thumby.display.drawText("Game Over", 15, 10, 1)
        thumby.display.drawText("You took "+str(self.spin)+ " spins", 5, 30, 1)
        thumby.display.update()   
    
menuScene = MenuScene()
gameScene = GameScene()

while True:
    if (scene==0):
        menuScene.update()
    elif(scene==1): 
        gameScene.update()
            
    