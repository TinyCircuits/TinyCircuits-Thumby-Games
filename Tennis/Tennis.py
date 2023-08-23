import time
import thumby
import math
import random


thumby.display.setFPS(120)


def waitOnPressedAB():
    # Wait on already pressed A or B so subsequent screens are not skipped
    while thumby.buttonA.pressed() or thumby.buttonB.pressed():
        pass


waitOnPressedAB()


def handleLogoScreen():
    logo = thumby.Sprite(72, 40, "/Games/Tennis/TennisLogoFrames.bin")
    
    while True:
        # Alternate and display frames until a button is pressed
        logo.setFrame(int((time.ticks_ms() % 2000) / 1000))
        thumby.display.drawSprite(logo)
        thumby.display.update()
        
        if thumby.buttonA.justPressed() or thumby.buttonB.justPressed():
            break
        
    # Return next game screen ID
    return 1


def waitForPlayer(received):
    global server
    
    # If receive packet with current game screen, means other Thumby ready to go
    if received != None and received[0] == 2:
        server = True
        
        # Return next game screen ID
        return 3
    
    # Add dots to last line to indicate screen and game are active
    message = "player."
    for i in range(0, int((time.ticks_ms() % 750) / 250)):
        message += "."
    
    thumby.display.fill(0)
    thumby.display.drawFilledRectangle(3, 13, 60, 17, 0)
    thumby.display.drawText("Waiting for", 4, 4, 1)
    thumby.display.drawText(message, 4, 11, 1)
    thumby.display.drawText('A/B: Back', 4, 26, 1)
    
    thumby.display.update()
    
    # Navigate back if button is pressed while waiting
    if thumby.buttonA.justPressed() or thumby.buttonB.justPressed():
        return 1
    
    # Return current game screen ID
    thumby.link.send(bytearray([2]))
    return 2



# Sprites
court = thumby.Sprite(72, 40, "/Games/Tennis/TennisCourt.bin")

leftRacket = thumby.Sprite(2, 9, bytearray([255,255,1,1]))
rightRacket = thumby.Sprite(2, 9, bytearray([255,255,1,1]))
leftRacket.x = 0
leftRacket.y = int(thumby.display.height / 2 - leftRacket.height / 2)
rightRacket.x = thumby.display.width - rightRacket.width
rightRacket.y = int(thumby.display.height / 2 - rightRacket.height / 2)

ball = thumby.Sprite(2, 2, bytearray([3,3]))

# Score of player (the racket moved by this device) and the opponent    
leftRacketScore = 0
rightRacketScore = 0

server = False
singlePlayer = -1
courtSetup = False
playedBounceSound = 0
indicatePlayerTimeout = time.ticks_ms()
ballServeTimeout = time.ticks_ms()
lastBallRefresh = 0     # Only applies to singleplayer


def handleModeSelect():
    global server
    global singlePlayer
    
    waitOnPressedAB()
    
    thumby.display.fill(0)
    thumby.display.drawText("Mode Select", 2, 5, 1)
    thumby.display.drawText("B: 1 player", 2, 21, 1)
    thumby.display.drawText("A: 2 player", 2, 30, 1)
    thumby.display.update()
    
    while True:
        if thumby.buttonB.pressed():
            server = True
            singlePlayer = True
            return 3
        elif thumby.buttonA.pressed():
            singlePlayer = False
            return 2


def resetCourt(serveRight=True):
    global playedBounceSound
    global ballServeTimeout
    global indicatePlayerTimeout
    global courtSetup
    
    # Position the ball in the middle of the screen
    ball.x = thumby.display.width / 2 - 2
    ball.y = thumby.display.height / 2 - 1
    
    # Position the rackets and give ball velocity
    if server:
        # Get a random angle between 162 and 198 degrees
        angle = random.uniform(math.pi - math.pi/10, math.pi + math.pi/10)
        ball.velScale = 0.85                        # Add attribute
        ball.xVel = math.cos(angle)*ball.velScale   # Add attribute
        ball.yVel = math.sin(angle)*ball.velScale   # Add attribute
        
        if serveRight == True:
            ball.xVel = -ball.xVel
    
    # Reset these
    playedBounceSound = 0
    ballServeTimeout = time.ticks_ms()
    
    if courtSetup == False:
        indicatePlayerTimeout = time.ticks_ms()
    courtSetup = True


def playBounceSound():
    global playedBounceSound
    thumby.audio.play(4000, 100)
    playedBounceSound = 1


def handleIndicatePlayer():
    if time.ticks_ms() - indicatePlayerTimeout < 2000:
        if server:
            thumby.display.drawText("^", 0, 32, 1)
        else:
            thumby.display.drawText("^", 67, 32, 1)


def handleRacketMove(racket):
    if thumby.buttonU.pressed() and racket.y - 0.75 >= 1:
        racket.y -= 0.75
    elif thumby.buttonD.pressed() and racket.y + 0.75 <= thumby.display.height - racket.height - 1:
        racket.y += 0.75


def handleAIRacketMove(racket):
    # The ai racket will only move when the ball is on its side by a random amount
    if not hasattr(racket, 'aiMoveXPos') or ball.x < 5:
        racket.aiMoveXPos = random.randint(40, 60)
    
    if ball.x > racket.aiMoveXPos:
        if racket.y + racket.y/2 > ball.y and racket.y - 0.75 >= 0.75:
            racket.y -= 0.75
        elif racket.y + racket.y/2 < ball.y and racket.y + 0.75 <= thumby.display.height - racket.height - 0.75:
            racket.y += 0.75


def handleSend():
    global playedBounceSound
    
    if singlePlayer != True:
        if server:
            # Pack the current game screen ID in the start
            data = bytearray([3, int(leftRacket.y), int(ball.x), int(ball.y), leftRacketScore, rightRacketScore, playedBounceSound])
            
            # Toggle sound state once it successfully sends once
            if thumby.link.send(data) != False and playedBounceSound == 1:
                playedBounceSound = 0
        else:
            # Pack the current game screen ID in the start
            thumby.link.send(bytearray([3, int(rightRacket.y)]))


def handleReceived(received):
    global leftRacketScore
    global rightRacketScore
    
    if received != None:
        # The first byte is the game screen ID, don't use that here
        if server:
            if len(received) == 2:
                rightRacket.y = received[1]
                return 1
        else:
            if len(received) == 7:
                leftRacket.y = received[1]
                ball.x = received[2]
                ball.y = received[3]
                leftRacketScore = received[4]
                rightRacketScore = received[5]
                if received[6] == 1:
                    playBounceSound()
                return 0


def isBallCollidedWithRacket(racket):
    return racket.x <= ball.x <= (racket.x + racket.width) and racket.y <= ball.y <= (racket.y + racket.height)


def racketBounceBall(racket):
    ballCenter = ball.y + ball.height/2
    racketCenter = racket.y + racket.height/2
    
    normal = -((racketCenter - ballCenter) / 5)
    
    ball.velScale += 0.025
    ball.xVel = math.cos(normal)*ball.velScale
    ball.yVel = math.sin(normal)*ball.velScale
    
    if ball.x > thumby.display.width//2:
        ball.xVel *= -1
    
    playBounceSound()


def handleBall():
    global leftRacketScore
    global rightRacketScore
    
    if time.ticks_ms() - ballServeTimeout >= 1500:
        ball.x += ball.xVel
        ball.y += ball.yVel
        
        # Collision with top or bottom
        if (ball.y <= 1) or (ball.y >= thumby.display.height - 2):
            ball.yVel = -ball.yVel
            playBounceSound()
        
        # Handle racket collision and score
        if isBallCollidedWithRacket(leftRacket):
            racketBounceBall(leftRacket)
        elif ball.x <= -ball.width:
            rightRacketScore += 1
            resetCourt(True)
        elif isBallCollidedWithRacket(rightRacket):
            racketBounceBall(rightRacket)
        elif ball.x >= thumby.display.width:
            leftRacketScore += 1
            resetCourt(False)


def handleGameOver(received):
    global courtSetup
    global leftRacketScore
    global rightRacketScore
    global server
    global singlePlayer
    
    thumby.display.fill(0)
    
    if received != None and not server:
        leftRacketScore = received[1]
        rightRacketScore = received[2]
    
    if server:
        if leftRacketScore == 5:
            thumby.display.drawText("You Won!", 12, 3, 1)
        elif rightRacketScore == 5:
            thumby.display.drawText("You Lost!", 10, 3, 1)
    else:
        if rightRacketScore == 5:
            thumby.display.drawText("You Won!", 12, 3, 1)
        elif leftRacketScore == 5:
            thumby.display.drawText("You Lost!", 10, 3, 1)

    
    thumby.display.drawText("Play again?", 4, 20, 1)
    thumby.display.drawText("B:NO A:YES", 6, 30, 1)
    
    thumby.display.update()
    
    while True:
        # Send current game screen ID
        if singlePlayer != True:
            thumby.link.send(bytearray([4, leftRacketScore, rightRacketScore]))
        
            # Receive but do nothing to keep send and receive logic going
            thumby.link.receive()
        
        if thumby.buttonB.pressed():
            thumby.reset()
        elif thumby.buttonA.pressed():
            
            courtSetup = False
            leftRacketScore = 0
            rightRacketScore = 0
            server = False
            singlePlayer = -1
            leftRacket.y = int(thumby.display.height / 2 - leftRacket.height / 2)
            rightRacket.y = int(thumby.display.height / 2 - rightRacket.height / 2)
            
            # Return game screen ID we want to go to
            return 1


def main(received):
    if courtSetup == False:
        resetCourt()
    
    # Draw court background and scores
    thumby.display.drawSprite(court)
    thumby.display.drawText(str(leftRacketScore), 20, 2, 1)
    thumby.display.drawText(str(rightRacketScore), 45, 2, 1)
    
    handleIndicatePlayer()
    if server:
        handleRacketMove(leftRacket)
    else:
        handleRacketMove(rightRacket)
    
    handleSend()
    
    if handleReceived(received) == 1:
        handleBall()
    elif singlePlayer:
        global lastBallRefresh
        
        # Replicate speed of link API
        if time.ticks_ms() - lastBallRefresh >= 18:
            handleBall()
            lastBallRefresh = time.ticks_ms()
        
        handleAIRacketMove(rightRacket)
    
    if server and (rightRacketScore == 5 or leftRacketScore == 5):
        waitOnPressedAB()
        
        # Return to game screen ID
        return 4
    
    # Draw the ball and both rackets
    thumby.display.drawSprite(ball)
    thumby.display.drawSprite(leftRacket)
    thumby.display.drawSprite(rightRacket)
    
    thumby.display.update()
    
    # Return current game screen
    return 3


gameScreenID = 0


try:
    while True:
        received = None
        if singlePlayer != True and singlePlayer != -1:
            received = thumby.link.receive()
    
        if received != None and (received[0] == gameScreenID + 1 or received[0] < gameScreenID):
            gameScreenID = received[0]
    
        if gameScreenID == 0:
            gameScreenID = handleLogoScreen()
        elif gameScreenID == 1:
            gameScreenID = handleModeSelect()
        elif gameScreenID == 2:
            gameScreenID = waitForPlayer(received)
        elif gameScreenID == 3:
            gameScreenID = main(received)
        elif gameScreenID == 4:
            gameScreenID = handleGameOver(received)
            
except Exception as e:
    f = open("/crash.log", "w")
    f.write(str(e))
    f.close()

