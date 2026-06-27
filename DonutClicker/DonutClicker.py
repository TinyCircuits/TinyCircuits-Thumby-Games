#################################################################################
# Donut Clicker was based on the original clicker game, Cookie Clicker.         #
#                                                                               #
# (I did not copy Simple Cookie Clicker by Camerin Figueroa, I learned          #
# that it existed after I started this project.)                                #
#                                                                               #
# This is licensed under CC BY-SA 4.0 and is open-source with attribution.      #
# This free software is provided without any warranty or guarantees.            #
#################################################################################

from time import ticks_ms
import thumby as t
from math import sin

t.display.setFPS(10)

def saveGame():
    t.saveData.setItem("donuts", donuts)
    t.saveData.setItem("perClick", perClick)
    t.saveData.setItem("perSec", perSec)
    t.saveData.setItem("pcPrice", pcPrice)
    t.saveData.setItem("psPrice", psPrice)
    t.saveData.setItem("buff", buff)
    t.saveData.save()
    t.saveData.setItem("donutsBackup", donuts)
    t.saveData.setItem("perClickBackup", perClick)
    t.saveData.setItem("perSecBackup", perSec)
    t.saveData.setItem("pcPriceBackup", pcPrice)
    t.saveData.setItem("psPriceBackup", psPrice)
    t.saveData.setItem("buffBackup", buff)
    t.saveData.save()
    
# Define images
#32x32
donutIMG = bytearray([0,0,0,128,224,176,112,248,248,252,252,252,254,246,246,246,254,190,222,254,252,252,252,216,216,208,240,224,128,0,0,0,
         0,240,254,255,191,223,239,255,255,255,248,127,31,15,15,7,7,15,15,31,127,243,255,127,127,127,239,223,191,254,240,0,
        0,15,127,255,255,61,253,255,223,239,255,254,248,240,240,224,224,240,240,216,222,255,251,247,239,255,255,255,243,127,15,0,
        0,0,0,1,7,14,15,31,31,63,63,63,113,127,127,127,94,93,127,127,63,63,63,24,31,15,15,7,1,0,0,0])
#3x5
arrowIMG = bytearray([17,10,4])
arrow2IMG = bytearray([4,10,17,0,17,10,4])
#8x8
floppyDiscIMG = bytearray([255,168,171,168,168,175,174,252])

# Make the sprites
donutSprite = t.Sprite(32, 32, donutIMG, 0, 0, 0)
arrowRight = t.Sprite(3, 5, arrowIMG, 65, 35)
arrow2 = t.Sprite(7, 5, arrow2IMG, 61, 35)
arrowLeft = t.Sprite(3, 5, arrowIMG, 61, 35, -1, 1, 0)
saveSprite = t.Sprite(8, 8, floppyDiscIMG, 0, 32)

# Initializes variables
donuts = 0
clicks = 0
perClick = 1
pcPrice = 50
perSec = 0
psPrice = 100
inShop = False
buff = 0
ticks = None
tillSave = 10

donutSprite.x = 0

# Initialize the save file
t.saveData.setName("DonutClicker")
# Load all saved data
if(t.saveData.hasItem("donuts")):
    donuts = t.saveData.getItem("donuts")
if(t.saveData.hasItem("perClick")):
    perClick = t.saveData.getItem("perClick")
if(t.saveData.hasItem("perSec")):
    perSec = t.saveData.getItem("perSec")
if(t.saveData.hasItem("pcPrice")):
    pcPrice = t.saveData.getItem("pcPrice")
if(t.saveData.hasItem("psPrice")):
    psPrice = t.saveData.getItem("psPrice")
if(t.saveData.hasItem("buff")):
    buff = t.saveData.getItem("buff")

while 1:
    ticks = str(ticks_ms())
    
    # Draw your donut count, and prices if in shop
    if inShop == False:
        if int(ticks[-3]) == 5:
            donuts += perSec
            tillSave -= 1
        
        if tillSave < 2:
            t.display.drawSprite(saveSprite)
            
        if tillSave < 1:
            saveGame()
            tillSave = 10
        
        donutSprite.y = int(round((t.display.height/2) - 16 + sin(int(ticks) / 300 * 2)))
        t.display.setFont("/lib/font5x7.bin", 5, 7, 1)
        t.display.drawText("%d" % donuts, 28, 0, 1)
        t.display.setFont("/lib/font3x5.bin", 3, 5, 1)
        t.display.drawText("Buff:", 35, 20, 1)
        t.display.drawText("%d" % buff + "%", 35, 26, 1)
    if inShop == True:
        t.display.setFont("/lib/font5x7.bin", 5, 7, 1)
        t.display.drawText("[B] Dnts/clk", 0, 1, 1)
        t.display.setFont("/lib/font3x5.bin", 3, 5, 1)
        t.display.drawText("%d" % perClick + ", Price: %d" % pcPrice, 0, 9, 1)
        t.display.setFont("/lib/font5x7.bin", 5, 7, 1)
        t.display.drawText("[A] Dnts/sec", 0, 17, 1)
        t.display.setFont("/lib/font3x5.bin", 3, 5, 1)
        t.display.drawText("%d" % perSec + ", Price: %d" % psPrice, 0, 25, 1)
    if inShop == "screen0":
        t.display.setFont("/lib/font5x7.bin", 5, 7, 1)
        t.display.drawText("Not enough", 0, 0, 1)
        t.display.drawText("donuts", 0, 9, 1)
        t.display.drawText("Any button", 0, 22, 1)
        t.display.drawText("to close", 0, 31, 1)
        if t.inputJustPressed():
            inShop = False
    if inShop == "prestige":
        t.display.setFont("/lib/font5x7.bin", 5, 7, 1)
        t.display.drawText("Prestige:", 0, 0, 1)
        t.display.drawText("reset all &", 0, 10, 1)
        t.display.drawText("get 10% buff", 0, 18, 1)
        t.display.drawText("Press B", 0, 32, 1)
        if t.buttonB.justPressed():
            inShop = "pStart" if donuts >= 10000 else "pError"
    if inShop == "pError":
        t.display.setFont("/lib/font5x7.bin", 5, 7, 1)
        t.display.drawText("Minimum of", 0, 0, 1)
        t.display.drawText("10k donuts", 0, 9, 1)
        t.display.drawText("Any button", 0, 22, 1)
        t.display.drawText("to close", 0, 31, 1)
        if t.inputJustPressed():
            inShop = False
    if inShop == "pStart":
        t.display.setFont("/lib/font5x7.bin", 5, 7, 1)
        t.display.drawText("Sure?", 0, 0, 1)
        t.display.drawText("Press A&B to", 0, 12, 1)
        t.display.drawText("confirm", 0, 20, 1)
        if t.buttonB.pressed() and t.buttonA.pressed():
            buff += 10
            donuts = 0
            perClick = 1
            pcPrice = 50
            perSec = 0
            psPrice = 100
            inShop = False
    if inShop == "stats":
        t.display.setFont("/lib/font5x7.bin", 5, 7, 1)
        t.display.drawText("-- STATS --", 0, 0, 1)
        t.display.drawText("Clks %d" % clicks, 0, 8, 1)
        t.display.drawText("Buff %d" % buff + "%", 0, 16, 1)
        t.display.drawText("/clk %d" % perClick, 0, 24, 1)
        t.display.drawText("/sec %d" % perSec, 0, 32, 1)
    if inShop == "win":
        t.display.setFont("/lib/font5x7.bin", 5, 7, 1)
        t.display.drawText("You won!", 0, 0, 1)
        t.display.drawText("1Mil donuts", 0, 8, 1)
        t.display.drawText("A&B to reset", 0, 17, 1)
        t.display.drawText("+100% buff", 0, 25, 1)
        t.display.drawText("start w/5k", 0, 33, 1)
        if t.buttonB.pressed() and t.buttonA.pressed():
            buff += 100
            donuts = 4998
            perClick = 1
            pcPrice = 50
            perSec = 0
            psPrice = 100
            inShop = False
    
    # Display the sprites
    if inShop == False:
        t.display.drawSprite(donutSprite)
        t.display.drawSprite(arrowRight)
    if inShop == True or inShop == "prestige":
        t.display.drawSprite(arrow2)
    if inShop == "stats":
        t.display.drawSprite(arrowLeft)
        
    t.display.update() # Draw everything on screen
    
    # Detect clicks
    if inShop == False and t.actionJustPressed():
        donuts += perClick + perClick*int(buff)/100
        clicks += 1
    if inShop == True and t.buttonB.justPressed():
        if donuts >= pcPrice:
            perClick += 1
            donuts -= pcPrice
            pcPrice += 70
        else:
            inShop = "screen0"
    if inShop == True and t.buttonA.justPressed():
        if donuts >= psPrice:
            perSec += 2
            donuts -= psPrice
            psPrice += 120
        else:
            inShop = "screen0"
            
    if t.buttonR.justPressed():
        if inShop == True:
            inShop = "prestige"
        elif inShop == "prestige":
            inShop = "stats"
        else:
            inShop = True
    if t.buttonL.justPressed():
        if inShop == "prestige":
            inShop = True
        elif inShop == "prestige":
            inShop = "stats"
        elif inShop == "stats":
            inShop = "prestige"
        else:
            inShop = False
        
    t.display.fill(0)
