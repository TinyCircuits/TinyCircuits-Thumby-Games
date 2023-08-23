import thumby
import random

thumby.display.setFPS(60)
# BITMAP: width: 7, height: 6
bitmap0 = bytearray([28,42,41,51,37,38,24])
# BITMAP: width: 8, height: 40
bitmap1 = bytearray([0,255,255,255,255,255,255,0,
           0,255,255,255,255,255,255,0,
           0,255,255,255,255,255,255,0,
           0,255,255,255,255,255,255,0,
           248,255,255,255,255,143,143,248])
# BITMAP: width: 8, height: 40
bitmap2 = bytearray([31,255,255,255,255,241,241,31,
           0,255,255,255,255,255,255,0,
           0,255,255,255,255,255,255,0,
           0,255,255,255,255,255,255,0,
           0,255,255,255,255,255,255,0])
# BITMAP: width: 60, height: 30
bitmap3 = bytearray([0,0,12,12,12,12,12,252,252,12,12,12,236,236,0,0,0,0,0,224,224,0,0,252,252,0,0,0,0,0,0,0,0,0,0,192,224,112,56,28,12,12,12,28,56,112,224,192,0,0,248,248,24,24,24,24,248,248,0,0,
           0,0,0,0,0,0,0,255,255,0,0,0,255,255,128,128,128,128,128,255,255,0,0,255,255,0,0,0,0,0,0,0,0,0,0,255,255,48,48,48,48,48,48,48,48,48,255,255,0,0,255,255,6,6,6,6,7,7,0,0,
           0,0,0,0,0,0,0,255,255,0,0,0,255,255,1,1,1,1,1,255,255,0,0,255,255,128,128,128,128,128,128,128,128,0,0,255,255,0,0,0,0,0,0,0,0,0,255,255,0,0,255,255,0,0,0,0,0,0,0,0,
           0,0,0,0,0,0,0,1,1,0,0,0,1,1,0,0,0,0,0,1,1,0,0,1,1,1,1,1,1,1,1,1,1,0,0,1,1,0,0,0,0,0,0,0,0,0,1,1,0,0,1,1,0,0,0,0,0,0,0,0])

bird = thumby.Sprite(7,6,bitmap0)
bird.x = 3
gamestate = "menu"
bird.y = 10
menuScreen = thumby.Sprite(60,30,bitmap3)
menuScreen.x = 7
menuScreen.y = 2
yVel = 0
pipe1X = 72
pipe1Y = random.randint(-37,-20)
pipe1UP = thumby.Sprite(8,40,bitmap1)
pipe1UP.x = pipe1X
pipe1UP.y = pipe1Y
pipe1DN = thumby.Sprite(8,40,bitmap2)
pipe1DN.x = pipe1X
pipe1DN.y = pipe1Y + 60
pipe1PT = False
pipe2X = 109
pipe2Y = random.randint(-37,-20)
pipe2UP = thumby.Sprite(8,40,bitmap1)
pipe2UP.x = pipe2X
pipe2UP.y = pipe2Y
pipe2DN = thumby.Sprite(8,40,bitmap2)
pipe2DN.x = pipe2X
pipe2DN.y = pipe2Y + 60
pipe2PT = False
score = 0
init = False
while True:
    if thumby.buttonL.pressed():
        thumby.reset()
    if gamestate == "play":
        # funcs first
        if bird.y+6<40:
            yVel+=0.07
        else:
            yVel=0
            bird.y=34
            init = False
            gamestate = "menu"
        if thumby.inputJustPressed():
            yVel=-0.9
        bird.y+=yVel
        pipe1X-=0.5
        pipe2X-=0.5
        if pipe1X<-8:
            pipe1X=72
            pipe1Y = random.randint(-34,-25)
            pipe1UP.y = pipe1Y
            pipe1DN.y = pipe1Y + 60
            pipe1PT = False
        if pipe1X<6 and not pipe1PT:
            score+=1
            pipe1PT = True
        if pipe2X<-8:
            pipe2X=72
            pipe2Y = random.randint(-34,-25)
            pipe2UP.y = pipe2Y
            pipe2DN.y = pipe2Y + 60
            pipe2PT = False
        if pipe2X<6 and not pipe2PT:
            score+=1
            pipe2PT = True
        
        # draw last
    if gamestate == "menu":
        if thumby.buttonA.justPressed():
            yVel=-1.6
            gamestate="play"
        else:
            _ = random.randint(-34,25)
            if init == False:
                score = 0
                pipe1X = 80
                pipe1Y = random.randint(-37,-20)
                pipe2X = 116
                pipe2Y = random.randint(-37,-20)
                bird.y=10
                pipe1PT = False
                pipe2PT = False
                init = True
    pipe2UP.x = pipe2X
    pipe2DN.x = pipe2X
    pipe1UP.x = pipe1X
    pipe1DN.x = pipe1X
    thumby.display.fill(0)
    if gamestate == "play":
        thumby.display.drawSprite(bird)
    thumby.display.drawSprite(pipe1UP)
    thumby.display.drawSprite(pipe1DN)
    thumby.display.drawSprite(pipe2UP)
    thumby.display.drawSprite(pipe2DN)
    thumby.display.drawLine(0,39,71,39,1)
    if gamestate == "menu":
        thumby.display.drawSprite(menuScreen)
        thumby.display.setFont("/lib/font3x5.bin",3,5,1)
        thumby.display.drawText("PRESS ANY BUTTON",5,30,1)
        thumby.display.setFont("/lib/font5x7.bin", 5, 7, 1)
    if gamestate == "play":
        thumby.display.drawText(str(score),60,10,1)
    # thumby.display.fill(0)
    # thumby.display.setFont("/lib/font8x8.bin",8,8,1)
    # thumby.display.drawText("GAME",2,10,1)
    # thumby.display.drawText("OVER",2,20,1)
    thumby.display.update()
    if thumby.display.getPixel(int(bird.x - 1), int(bird.y - 1)) == 1 and gamestate == "play":
        gamestate = "menu"
        init = False
    elif thumby.display.getPixel(int(bird.x + 7), int(bird.y - 1)) == 1 and gamestate == "play":
        gamestate = "menu"
        init = False
    elif thumby.display.getPixel(int(bird.x + 7), int(bird.y + 6)) == 1 and gamestate == "play":
        gamestate = "menu"
        init = False
    elif thumby.display.getPixel(int(bird.x - 1), int(bird.y + 6)) == 1 and gamestate == "play":
        gamestate = "menu"
        init = False
