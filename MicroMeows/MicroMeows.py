import time
import thumby
import math
import random
# MicroMeows

# BITMAP: width: 72, height: 40
catMap = bytearray([0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,128,192,192,224,224,96,96,224,192,128,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,128,128,128,128,128,128,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,
           0,0,0,0,0,0,0,0,0,4,4,12,28,254,255,255,31,3,1,0,2,6,0,255,255,255,254,248,0,0,0,0,0,0,0,0,0,0,0,192,240,252,254,254,63,15,7,3,9,25,3,255,255,254,252,224,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,
           0,0,0,0,0,0,0,0,0,0,0,0,0,0,3,7,15,12,28,24,28,28,30,31,15,15,7,1,0,0,0,0,0,0,0,0,0,0,0,3,15,31,63,63,120,112,96,112,112,120,60,63,31,31,15,7,3,3,2,2,0,0,0,0,0,0,0,0,0,0,0,0,
           0,0,0,96,32,32,48,16,16,16,8,8,8,8,12,4,4,4,4,4,132,4,0,0,0,14,31,31,143,207,255,127,255,254,126,62,254,252,252,248,240,0,0,0,0,64,64,128,128,128,128,128,128,128,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,
           0,32,48,32,48,16,16,24,8,12,12,4,4,2,2,2,194,97,49,25,12,134,130,128,128,64,64,64,79,119,193,142,143,131,128,0,0,1,1,13,24,16,48,32,96,66,194,132,132,136,136,24,16,16,49,33,33,33,97,67,67,194,130,130,2,2,0,0,0,0,0,0])

# BITMAP: width: 72, height: 40
intro = bytearray([255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,31,199,55,39,79,159,63,127,255,255,255,255,127,127,255,255,255,127,63,159,71,51,7,255,255,7,211,139,187,139,27,199,255,255,255,255,255,255,255,255,255,255,255,255,
           191,191,191,191,191,191,191,63,127,127,127,127,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,252,1,255,192,224,240,121,127,56,57,124,254,254,254,62,190,30,94,158,191,62,252,252,248,3,255,192,31,255,255,255,0,255,255,255,255,255,255,255,255,255,255,255,255,255,
           255,255,255,31,31,255,255,255,255,255,255,254,254,126,60,253,249,249,243,243,243,247,247,247,247,247,247,247,240,247,247,247,243,240,251,248,248,251,248,253,253,252,253,252,252,252,254,254,254,254,254,254,254,254,254,254,254,253,252,253,253,253,253,189,126,254,254,254,254,254,254,254,
           255,255,255,255,254,0,57,248,253,227,231,241,252,254,4,1,255,255,255,255,255,7,121,124,126,126,126,124,57,131,255,255,255,255,255,255,255,255,31,239,243,253,254,254,254,254,252,192,29,254,255,255,249,3,127,255,255,255,255,255,255,255,255,255,254,0,255,255,255,255,255,255,
           255,255,255,255,255,254,128,63,255,255,255,255,255,255,254,224,3,255,255,255,255,248,227,207,223,191,63,127,127,63,191,159,207,231,255,255,255,255,248,231,207,191,191,191,223,207,231,248,254,255,255,255,255,255,254,225,207,191,159,193,193,223,159,159,207,224,255,255,255,255,255,255])
           
# BITMAP: width: 16, height: 20
kitten = bytearray([0,224,240,248,124,120,240,224,224,240,120,124,248,240,224,0,
           126,223,215,215,196,236,247,39,39,247,204,212,215,155,251,126,
           0,0,1,1,3,3,3,3,3,3,3,3,1,1,0,0])  
           
# BITMAP: width: 16, height: 20
kitten2 = bytearray([224,240,248,124,124,240,224,192,224,224,240,240,240,240,240,0,
           239,207,95,252,221,63,191,255,191,183,113,121,127,31,15,0,
           2,6,7,7,7,7,7,6,5,3,5,8,9,1,1,0])

# BITMAP: width: 16, height: 20
kitten3 = bytearray([192,248,255,255,224,0,0,0,0,0,192,248,254,255,254,192,
           255,115,115,127,127,255,62,62,62,62,255,127,127,115,115,255,
           3,15,7,11,13,15,15,12,12,15,15,13,3,7,7,0])  

introSpr = thumby.Sprite(72, 40, intro, 0, 0)
catSpr  = thumby.Sprite(72, 40, catMap, 0, 0)

top     =[31,  0]
bottom  =[31, 20]
left    =[0 ,  6]
right   =[57,  6]

# Set the FPS (without this call, the default fps is 30)
thumby.display.setFPS(60)
thumby.display.setFont("/lib/font5x7.bin", 5, 7, 1)

def mapValue(x, in_min, in_max, out_min, out_max):
    return (x - in_min) * (out_max - out_min) / (in_max - in_min) + out_min

def playHit():
    for i in range(1000, 2000,100):
        thumby.audio.play(i, 20)
    # buzzer = Pin(28, Pin.OUT) 
    # buzzer.value(0)
    # buzzer.value(1)

def playNotHit():
    thumby.display.fill(1) # clear screen
    thumby.display.update() # clear screen
    thumby.display.fill(0) # clear screen
    thumby.display.drawSprite(catSpr)
    thumby.display.update() # clear screen
    thumby.audio.playBlocking(300, 200)
    thumby.audio.play(100, 200)

def get_high_score():
    # Default high score
    high_score = 0
 
    # Try to read the high score from a file
    try:
        high_score_file = open("/Games/MicroMeows/scores.txt", "r")
        high_score = int(high_score_file.read())
        high_score_file.close()
        print("The high score is", high_score)
    except ValueError:
        # There's a file there, but we don't understand the number.
        print("I'm confused. Starting with no high score.")
    except:
        # Error reading file, no high score
        print("There is no high score yet.")
        save_high_score(0)
 
    return high_score

def save_high_score(new_high_score):
    try:
        # Write the file to disk
        high_score_file = open("/Games/MicroMeows/scores.txt", "w")
        high_score_file.write(str(new_high_score))
        print("Saved the high score.")
        high_score_file.close()
    except:
        # Hm, can't write it.
        print("Unable to save the high score.")

#start
thumby.display.drawSprite(introSpr)
thumby.display.update()
while (not (thumby.buttonA.justPressed() or thumby.buttonB.justPressed())):
    thumby.display.update()

highScore = get_high_score()
thumby.display.fill(0) # clear screen
thumby.display.setFont("/lib/font8x8.bin", 8, 8, 1)
thumby.display.drawText("HIGH", 12, 22, 1)
thumby.display.drawText(str(highScore), 12, 31, 1)
while (not (thumby.buttonA.justPressed() or thumby.buttonB.justPressed())):
    thumby.display.update()


endGameTime=2*60*1000
startTime = time.ticks_ms()
totalScore = 0
while(time.ticks_ms() < startTime + endGameTime):
    # spawn a new kitten!:
    t0 = time.ticks_ms()
    thumby.display.fill(0) # clear screen

    spr = random.randint(1,3)
    if spr==1:
        kittenSprite = thumby.Sprite(16, 20, kitten)
    if spr==2:
        kittenSprite = thumby.Sprite(16, 20, kitten2)
    if spr==3:
        kittenSprite = thumby.Sprite(16, 20, kitten3)

    side = random.randint(1,4)
    if side==1:
        kittenSprite.x = top[0]
        kittenSprite.y = top[1]
    if side==2:
        kittenSprite.x = right[0]
        kittenSprite.y = right[1]
    if side==3:
        kittenSprite.x = bottom[0]
        kittenSprite.y = bottom[1]
    if side==4:
        kittenSprite.x = left[0]
        kittenSprite.y = left[1]


    thumby.display.drawSprite(kittenSprite)

    gameTime = time.ticks_ms() - startTime + 1
    
    low = mapValue(gameTime, 0, endGameTime,2000,10)
    high = mapValue(gameTime, 0, endGameTime,5000,100)
    pause = random.randint(int(low),int(high))
    hit = False
    done = False
    while (not done):
        score = int(mapValue(time.ticks_ms() - t0,pause,0,0,100))

        thumby.display.drawFilledRectangle(thumby.display.width-20, 0, 20, 7, 0) # clear score
        scoreBarHeight = int(((pause - (time.ticks_ms() - t0)) / pause) * 7)
        thumby.display.drawFilledRectangle(thumby.display.width-20, 7- scoreBarHeight, 1, scoreBarHeight, 1) # scorebar
        thumby.display.drawText(str(score),thumby.display.width-18 , 0, 1)

        thumby.display.drawFilledRectangle(0, 0, 30, 7, 0) # clear totalScore
        thumby.display.drawText(str(totalScore), 0, 0, 1)

        thumby.display.update()
        if (side==1):
            if (thumby.buttonU.justPressed()):
                hit = True
                done= True
            if (thumby.buttonR.justPressed()):
                hit = False
                done= True
            if (thumby.buttonD.justPressed()):
                hit = False
                done= True
            if (thumby.buttonL.justPressed()):
                hit = False
                done= True
        if (side==2):
            if (thumby.buttonU.justPressed()):
                hit = False
                done= True
            if (thumby.buttonR.justPressed()):
                hit = True
                done= True
            if (thumby.buttonD.justPressed()):
                hit = False
                done= True
            if (thumby.buttonL.justPressed()):
                hit = False
                done= True
        if (side==3):
            if (thumby.buttonU.justPressed()):
                hit = False
                done= True
            if (thumby.buttonR.justPressed()):
                hit = False
                done= True
            if (thumby.buttonD.justPressed()):
                hit = True
                done= True
            if (thumby.buttonL.justPressed()):
                hit = False
                done= True
        if (side==4):
            if (thumby.buttonU.justPressed()):
                hit = False
                done= True
            if (thumby.buttonR.justPressed()):
                hit = False
                done= True
            if (thumby.buttonD.justPressed()):
                hit = False
                done= True
            if (thumby.buttonL.justPressed()):
                hit = True
                done= True
        if (time.ticks_ms() >= t0 + pause):
            done=True
    if (hit):    
        totalScore += score
        playHit()
    else:
        playNotHit()
highScore=get_high_score()
if (totalScore>highScore):
    save_high_score(totalScore)
thumby.display.fill(0) # clear screen
thumby.display.setFont("/lib/font8x8.bin", 8, 8, 1)

thumby.display.drawText("SCORE", 12, 5, 1)
thumby.display.drawText(str(totalScore), 12, 14, 1)
thumby.display.drawText("HIGH", 12, 22, 1)
thumby.display.drawText(str(highScore), 12, 31, 1)
while (not (thumby.buttonA.justPressed() or thumby.buttonB.justPressed())):
    thumby.display.update()

