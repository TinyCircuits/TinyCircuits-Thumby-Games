#################################################################################
# Donut Clicker was based on the original clicker game, Cookie Clicker.         #
#                                                                               #
# (I did not copy Simple Cookie Clicker by Camerin Figueroa, I learned          #
# that it existed after I started this project.)                                #
#                                                                               #
# This is licensed under CC BY-SA 4.0 and is open-source with attribution.      #
# This free software is provided without any warranty or guarantees.            #
#################################################################################

import time
import thumby
import math
import machine

thumby.display.setFPS(10)

# BITMAP: width: 32, height: 32
donutIMG = bytearray([0,0,0,128,224,176,112,248,248,252,252,252,254,246,246,246,254,190,222,254,252,252,252,216,216,208,240,224,128,0,0,0,
         0,240,254,255,191,223,239,255,255,255,248,127,31,15,15,7,7,15,15,31,127,243,255,127,127,127,239,223,191,254,240,0,
        0,15,127,255,255,61,253,255,223,239,255,254,248,240,240,224,224,240,240,216,222,255,251,247,239,255,255,255,243,127,15,0,
        0,0,0,1,7,14,15,31,31,63,63,63,113,127,127,127,94,93,127,127,63,63,63,24,31,15,15,7,1,0,0,0])
# BITMAPS: width: 3, height: 5
arrowIMG = bytearray([17,10,4])
arrow2IMG = bytearray([4,10,17,0,17,10,4])

# Make the sprites
donutSprite = thumby.Sprite(32, 32, donutIMG, 0, 0, 0)
arrowRight = thumby.Sprite(3, 5, arrowIMG, 65, 35)
arrow2 = thumby.Sprite(7, 5, arrow2IMG, 61, 35)
arrowLeft = thumby.Sprite(3, 5, arrowIMG, 61, 35, -1, 1, 0)

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


# Creates the save file
thumby.saveData.setName("DonutClicker")

# Load all saved data
if(thumby.saveData.hasItem("donuts")):
    donuts = thumby.saveData.getItem("donuts")
if(thumby.saveData.hasItem("perClick")):
    perClick = thumby.saveData.getItem("perClick")
if(thumby.saveData.hasItem("perSec")):
    perSec = thumby.saveData.getItem("perSec")
if(thumby.saveData.hasItem("pcPrice")):
    pcPrice = thumby.saveData.getItem("pcPrice")
if(thumby.saveData.hasItem("psPrice")):
    psPrice = thumby.saveData.getItem("psPrice")
if(thumby.saveData.hasItem("buff")):
    buff = thumby.saveData.getItem("buff")

while(1):
    ticks = str(time.ticks_ms())
    
    # Draw your donut count (text) and prices if in shop
    if inShop == False:
        
        if int(ticks[-3]) == 5
            donuts += perSec
        
        donutSprite.x = 0
        donutSprite.y = int(round((thumby.display.height/2) - 16 + math.sin(int(ticks) / 300 * 2)))
        thumby.display.setFont("/lib/font5x7.bin", 5, 7, 1)
        thumby.display.drawText("%d" % donuts, 28, 0, 1)
        thumby.display.setFont("/lib/font3x5.bin", 3, 5, 1)
        thumby.display.drawText("Buff:", 35, 20, 1)
        thumby.display.drawText("%d" % buff + "%", 35, 26, 1)
    if inShop == True:
        thumby.display.setFont("/lib/font5x7.bin", 5, 7, 1)
        thumby.display.drawText("[B] Dnts/clk", 0, 1, 1)
        thumby.display.setFont("/lib/font3x5.bin", 3, 5, 1)
        thumby.display.drawText("%d" % perClick + ", Price: %d" % pcPrice, 0, 9, 1)
        thumby.display.setFont("/lib/font5x7.bin", 5, 7, 1)
        thumby.display.drawText("[A] Dnts/sec", 0, 17, 1)
        thumby.display.setFont("/lib/font3x5.bin", 3, 5, 1)
        thumby.display.drawText("%d" % perSec + ", Price: %d" % psPrice, 0, 25, 1)
    if inShop == "screen0":
        thumby.display.setFont("/lib/font5x7.bin", 5, 7, 1)
        thumby.display.drawText("Not enough", 0, 0, 1)
        thumby.display.drawText("donuts", 0, 9, 1)
        thumby.display.drawText("Any button", 0, 22, 1)
        thumby.display.drawText("to close", 0, 31, 1)
        if thumby.inputJustPressed():
            inShop = False
    if inShop == "prestige":
        thumby.display.setFont("/lib/font5x7.bin", 5, 7, 1)
        thumby.display.drawText("Prestige:", 0, 0, 1)
        thumby.display.drawText("reset all &", 0, 10, 1)
        thumby.display.drawText("get 10% buff", 0, 18, 1)
        thumby.display.drawText("Press B", 0, 32, 1)
        if thumby.buttonB.justPressed():
            if donuts >= 10000:
                inShop = "pStart"
            else:
                inShop = "pError"
    if inShop == "pError":
        thumby.display.setFont("/lib/font5x7.bin", 5, 7, 1)
        thumby.display.drawText("Minimum of", 0, 0, 1)
        thumby.display.drawText("10k donuts", 0, 9, 1)
        thumby.display.drawText("Any button", 0, 22, 1)
        thumby.display.drawText("to close", 0, 31, 1)
        if thumby.inputJustPressed():
            inShop = False
    if inShop == "pStart":
        thumby.display.setFont("/lib/font5x7.bin", 5, 7, 1)
        thumby.display.drawText("Sure?", 0, 0, 1)
        thumby.display.drawText("Press A&B to", 0, 12, 1)
        thumby.display.drawText("confirm", 0, 20, 1)
        if thumby.buttonB.pressed() and thumby.buttonA.pressed():
            buff += 10
            donuts = 0
            perClick = 1
            pcPrice = 50
            perSec = 0
            psPrice = 100
            inShop = False
    if inShop == "stats":
        thumby.display.setFont("/lib/font5x7.bin", 5, 7, 1)
        thumby.display.drawText("-- STATS --", 0, 0, 1)
        thumby.display.drawText("Clks %d" % clicks, 0, 8, 1)
        thumby.display.drawText("Buff %d" % buff + "%", 0, 16, 1)
        thumby.display.drawText("/clk %d" % perClick, 0, 24, 1)
        thumby.display.drawText("/sec %d" % perSec, 0, 32, 1)
    if inShop == "win":
        thumby.display.setFont("/lib/font5x7.bin", 5, 7, 1)
        thumby.display.drawText("You won!", 0, 0, 1)
        thumby.display.drawText("1Mil donuts", 0, 8, 1)
        thumby.display.drawText("A&B to reset", 0, 17, 1)
        thumby.display.drawText("+100% buff", 0, 25, 1)
        thumby.display.drawText("start w/5k", 0, 33, 1)
        if thumby.buttonB.pressed() and thumby.buttonA.pressed():
            buff += 100
            donuts = 4998
            perClick = 1
            pcPrice = 50
            perSec = 0
            psPrice = 100
            inShop = False
    
    # Display the sprites
    if inShop == False:
        thumby.display.drawSprite(donutSprite)
        thumby.display.drawSprite(arrowRight)
    if inShop == True or inShop == "prestige":
        thumby.display.drawSprite(arrow2)
    if inShop == "stats":
        thumby.display.drawSprite(arrowLeft)
        
        
    thumby.display.update()
    
    
    # Detect clicks
    if inShop == False and thumby.actionJustPressed():
        donuts += perClick + perClick*int(buff)/100
        clicks += 1
    if inShop == True and thumby.buttonB.justPressed():
        if donuts >= pcPrice:
            perClick += 1
            donuts -= pcPrice
            pcPrice += 70
        else:
            inShop = "screen0"
    if inShop == True and thumby.buttonA.justPressed():
        if donuts >= psPrice:
            perSec += 2
            donuts -= psPrice
            psPrice += 120
        else:
            inShop = "screen0"
            
    if thumby.buttonR.justPressed():
        if inShop == True:
            inShop = "prestige"
        elif inShop == "prestige":
            inShop = "stats"
        else:
            inShop = True
    if thumby.buttonL.justPressed():
        if inShop == "prestige":
            inShop = True
        elif inShop == "prestige":
            inShop = "stats"
        elif inShop == "stats":
            inShop = "prestige"
        else:
            inShop = False
        
        # Save data
        thumby.saveData.setItem("donuts", donuts)
        thumby.saveData.setItem("perClick", perClick)
        thumby.saveData.setItem("perSec", perSec)
        thumby.saveData.setItem("pcPrice", pcPrice)
        thumby.saveData.setItem("psPrice", psPrice)
        thumby.saveData.setItem("buff", buff)
        thumby.saveData.save()
    
    thumby.display.fill(0)
