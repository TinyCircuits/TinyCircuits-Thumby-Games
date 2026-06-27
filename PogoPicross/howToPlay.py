#How to Play for Pogo Picross
import thumby

#making some shortcuts for myself re: setting the font
def fontSmall():
    thumby.display.setFont("/lib/font3x5.bin", 3, 5, 1)
def fontMed():
    thumby.display.setFont("/lib/font5x7.bin", 5, 7, 1)
def fontBig():
    thumby.display.setFont("/lib/font8x8.bin", 8, 8, 1)

def buttonAsound():
    thumby.audio.play(622, 100)

def buttonBsound():
    thumby.audio.play(523, 100)

def howToPlayGo():
    waiting = True
    #sprites
    # BITMAP: width: 5, height: 17
    squaresMap = bytearray([223,95,95,223,223,
               247,22,21,20,247,
               1,1,1,1,1])
    squaresSpr = thumby.Sprite(5, 17, squaresMap, 67, 9)
    
    # BITMAP: width: 5, height: 4
    checkMap = bytearray([4,8,4,2,1])
    checkSpr = thumby.Sprite(5, 4, checkMap, 67, 9)
    
    # BITMAP: width: 5, height: 5
    xMap2 = bytearray([17,10,4,10,17])
    xSpr2 = thumby.Sprite(5, 5, xMap2, 67, 9)
    
    # BITMAP: width: 17, height: 13
    tutorialMap1 = bytearray([255,17,17,17,255,17,17,17,255,17,17,17,255,0,34,238,136,
               1,1,29,1,1,5,29,17,1,1,29,1,1,0,0,0,0])
    tutorialSpr1 = thumby.Sprite(17, 13, tutorialMap1, 55, 9)
    
    # BITMAP: width: 17, height: 13
    tutorialMap2 = bytearray([255,159,95,63,255,255,255,255,255,249,245,243,255,0,34,238,136,
               1,1,29,1,1,5,29,17,1,1,29,1,1,0,0,0,0])
    tutorialSpr2 = thumby.Sprite(17, 13, tutorialMap2, 55, 9)
                
    while(waiting):
        thumby.display.fill(0)
        thumby.display.setFPS(60)
        thumby.display.drawSprite(tutorialSpr1)
        fontMed()
        thumby.display.drawText("HOW TO PLAY", 2, 0, 1)
        fontSmall()
        thumby.display.drawText("The numbers", 0, 9, 1)
        thumby.display.drawText("show how many", 0, 15, 1)
        thumby.display.drawText("squares are", 0, 21, 1)
        thumby.display.drawText("filled per row/col.", 0, 27, 1)
        thumby.display.drawText("1/5  A:Next B:Exit", 0, 35, 1)        
        thumby.display.update()
        if thumby.buttonB.justPressed():
            buttonBsound()
            waiting = False
            break
        if thumby.buttonA.justPressed():
            buttonAsound()
            waiting2 = True
            while(waiting2):
                thumby.display.fill(0)
                thumby.display.setFPS(60)
                thumby.display.drawSprite(tutorialSpr2)
                fontMed()
                thumby.display.drawText("HOW TO PLAY", 2, 0, 1)
                fontSmall()
                thumby.display.drawText("Put an X in", 0, 9, 1)
                thumby.display.drawText("squares that", 0, 15, 1)
                thumby.display.drawText("must not be", 0, 21, 1)
                thumby.display.drawText("filled.", 0, 27, 1)
                thumby.display.drawText("2/5  A:Next B:Prev", 0, 35, 1)
                thumby.display.update()
                if thumby.buttonB.justPressed():
                    buttonBsound()
                    waiting2 = False
                if thumby.buttonA.justPressed():
                    buttonAsound()
                    waiting3 = True
                    while(waiting3):
                        thumby.display.fill(0)
                        thumby.display.setFPS(60)
                        thumby.display.drawSprite(squaresSpr)
                        fontMed()
                        thumby.display.drawText("HOW TO PLAY", 2, 0, 1)
                        fontSmall()
                        thumby.display.drawText("Press A:", 0, 9, 1)
                        thumby.display.drawText("Switch square", 5, 15, 1)
                        thumby.display.drawText("between Filled,", 5, 21, 1)
                        thumby.display.drawText("X, and Empty.", 5, 27, 1)
                        thumby.display.drawText("3/5  A:Next B:Prev", 0, 35, 1)
                        thumby.display.update()
                        if thumby.buttonB.justPressed():
                            buttonBsound()
                            waiting3 = False
                        if thumby.buttonA.justPressed():
                            buttonAsound()
                            waiting4 = True
                            while(waiting4):
                                thumby.display.fill(0)
                                thumby.display.setFPS(60)
                                thumby.display.drawSprite(checkSpr)
                                fontMed()
                                thumby.display.drawText("HOW TO PLAY", 2, 0, 1)
                                fontSmall()
                                thumby.display.drawText("Press B:", 0, 9, 1)
                                thumby.display.drawText("Check Solution.", 5, 15, 1)
                                thumby.display.drawText("If Correct:", 0, 21, 1)
                                thumby.display.drawText("You win! :)", 5, 27, 1)
                                thumby.display.drawText("4/5  A:Next B:Prev", 0, 35, 1)
                                thumby.display.update()
                                if thumby.buttonB.justPressed():
                                    buttonBsound()
                                    waiting4 = False
                                if thumby.buttonA.justPressed():
                                    buttonAsound()
                                    waiting5 = True
                                    while(waiting5):
                                        thumby.display.fill(0)
                                        thumby.display.setFPS(60)
                                        thumby.display.drawSprite(xSpr2)
                                        fontMed()
                                        thumby.display.drawText("HOW TO PLAY", 2, 0, 1)
                                        fontSmall()
                                        thumby.display.drawText("If Incorrect:", 0, 9, 1)
                                        thumby.display.drawText("A number will", 5, 15, 1)
                                        thumby.display.drawText("show how many", 5, 21, 1)
                                        thumby.display.drawText("rows w/ errors.", 5, 27, 1)
                                        thumby.display.drawText("5/5  A:Exit B:Prev", 0, 35, 1)
                                        thumby.display.update()
                                        if thumby.buttonB.justPressed():
                                            buttonBsound()
                                            waiting5 = False
                                        if thumby.buttonA.justPressed():
                                            buttonBsound()
                                            waiting = False
                                            waiting2 = False
                                            waiting3 = False
                                            waiting4 = False
                                            waiting5 = False
                                            break