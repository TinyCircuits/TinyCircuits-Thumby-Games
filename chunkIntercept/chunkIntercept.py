import time
import thumby
import random

thumby.display.setFPS(60)

FB_WIDTH = thumby.display.width #72
FB_HEIGHT = thumby.display.height #40

score = 0
scrollWidth = 20
scrollPosX = 0
numberOfBlocks = 1
maxBlocks = 8
gamePaused = False
gameOver = False
gamePending = True
lives = 3

def collision(objaX, objaY, objaW, objaH, objbX, objbY, objbW, objbH):
    return objaX < objbX + objbW and objaX + objaW > objbX and objaY < objbY + objbH and objaY + objaH > objbY

def textWdith(curString):
    return (len(curString) * 5)

class chunk:
  posX = 0
  posY = 0
  scale = 0
  vis = False

chunks = [chunk(), chunk(), chunk(), chunk(), chunk(), chunk(), chunk(), chunk()]

def resetBlock(block):
	block.scale = random.randint(3, 6)
	block.posX = random.randint(1, FB_WIDTH - block.scale)
	block.posY = random.randint(-120, -block.scale)

def gameReset():
    global lives
    global gameOver
    global score
    global numberOfBlocks
    global scrollPosX
    score = 0
    lives = 3
    for c in chunks:
        resetBlock(c)
        c.vis = False
    chunks[0].vis = True
    numberOfBlocks = 1
    scrollPosX = (int)(FB_WIDTH / 2 - scrollWidth / 2)

def gameLogic():
    global lives, gameOver, score, numberOfBlocks
    for i in range(numberOfBlocks):
        if chunks[i].posY > 0-chunks[i].scale:
            for b in chunks:
                if collision(chunks[i].posX, chunks[i].posY, chunks[i].scale, chunks[i].scale, b.posX, b.posY, b.scale, b.scale) and b != chunks[i] and chunks[i].vis and b.vis:
                    chunks[i].vis = False
                    resetBlock(chunks[i])
            if chunks[i].posY < FB_HEIGHT + chunks[i].scale + 1 and chunks[i].vis:
                if score <= 10:
                    chunks[i].posY = chunks[i].posY + 0.1
                elif score > 10 and score <= 100:
                    chunks[i].posY = chunks[i].posY + 0.15
                elif score > 100 and score <= 255:
                    chunks[i].posY = chunks[i].posY + 0.2
                elif score > 255 and score <= 500:
                    chunks[i].posY = chunks[i].posY + 0.25
                elif score > 500:
                    chunks[i].posY = chunks[i].posY + 0.3
            else:
                resetBlock(chunks[i])
                if chunks[i].vis:
                    lives -= 1
                    if lives <= 0:
                        gameOver = True
                    thumby.audio.play(1960, 1)
                else:
                    chunks[i].vis = True
            if collision(chunks[i].posX, (int)(chunks[i].posY), chunks[i].scale, chunks[i].scale, scrollPosX, FB_HEIGHT - 5, scrollWidth, 2) and chunks[i].vis:
                resetBlock(chunks[i])
                thumby.audio.play(5041, 1)
                score += 1
                if numberOfBlocks < maxBlocks:
                    if round(score/10) > 2:
                        numberOfBlocks = round(score/10)
                        print(round(score/10))
                    else:
                        if score > 2:
                            numberOfBlocks = 2
                        else:
                            numberOfBlocks = 1
        else:
            chunks[i].posY+=1

scrollTxtXPOS = 60
while(True): #Game Loop
    thumby.display.fill(1)
    if gamePending:
        thumby.display.setFont("/lib/font5x7.bin", 5, 7, 0)
        thumby.display.drawFilledRectangle(0, 0, FB_WIDTH, 16, 0)
        thumby.display.drawText("CHUNK", (int)((FB_WIDTH / 2) - (textWdith("CHUNK") / 2)), 1, 1)
        thumby.display.drawText("INTERCEPT", (int)((FB_WIDTH / 2) - (textWdith("INTERCEPT") / 2)), 8, 1)
        thumby.display.drawText("Press A", (int)((FB_WIDTH / 2) - (textWdith("Press A") / 2)), 8 + 8+1, 0)
        thumby.display.drawText("to play!", (int)((FB_WIDTH / 2) - (textWdith("to play!") / 2)), 8 + 8 + 8, 0)
        thumby.display.drawFilledRectangle(0, 16+8+8, FB_WIDTH, 8, 0)
        introScrollTXT = "Game created by: Soul - (Nicholas Hryckewycz)"
        if scrollTxtXPOS-1 >= 0-textWdith(introScrollTXT):
            scrollTxtXPOS-=1
        else:
            scrollTxtXPOS = FB_WIDTH
        thumby.display.drawText(introScrollTXT, scrollTxtXPOS, FB_HEIGHT-7, 1)
        if thumby.buttonA.justPressed():
            gameReset()
            gamePending = not gamePending
    elif gameOver:
        thumby.display.setFont("/lib/font5x7.bin", 5, 7, 0)
        thumby.display.drawFilledRectangle(0, 0, FB_WIDTH, FB_HEIGHT, 0)
        thumby.display.drawText("GAME OVER", (int)((FB_WIDTH / 2) - (textWdith("GAME OVER") / 2)), 1, 1)
        thumby.display.drawFilledRectangle(0, 1+7+1, FB_WIDTH, 17, 1)
        thumby.display.drawText("SCORE:", (int)((FB_WIDTH / 2) - (textWdith("SCORE:") / 2)), 1+8+1, 0)
        thumby.display.drawText("{}".format(score), (int)((FB_WIDTH / 2) - (textWdith("{}".format(score)) / 2)), 2+8+8, 0)
        thumby.display.drawText("PLAY AGAIN!", (int)((FB_WIDTH / 2) - (textWdith("PLAY AGAIN!") / 2)), FB_HEIGHT - 9, 1)
        if thumby.buttonA.justPressed():
            gameOver = not gameOver
            gameReset()
    elif not gameOver and not gamePending:#GAME CODE
        for c in chunks:
            if c.vis:
                if c.posY > 0-c.scale:
                    thumby.display.drawFilledRectangle(c.posX, (int)(c.posY), c.scale, c.scale, 0)
        gameLogic()
        for l in range(lives):
            thumby.display.drawRectangle(2 + (l * 5) + (l * 2), 2, 5, 5, 0)
        if thumby.buttonL.pressed():
            if scrollPosX - 1 >= 0:
                scrollPosX -= 1
        if thumby.buttonR.pressed():
            if scrollPosX + 1 <= FB_WIDTH-scrollWidth:
                scrollPosX += 1
        if thumby.buttonA.justPressed():
            scrollPosX = FB_WIDTH - scrollWidth
        if thumby.buttonB.justPressed():
            scrollPosX = 0
    
        thumby.display.drawFilledRectangle(scrollPosX, FB_HEIGHT - 5, scrollWidth, 2, 0)
    thumby.display.update()