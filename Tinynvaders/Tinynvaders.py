#Tinynvaders
#coded by tibonev @ classicgames.com.br

import thumby
import math
import random

# player char: width: 4, height: 4 and variables to control the shot
player0 = bytearray([9,15,6,6])
player1 = bytearray([6,15,6,6])
playeranim = 0
playershot = bytearray([0,6,6,0])
playerx = 2
playery = 4
playerw = 4
playerh = 4
playersx = -20
playersy = 2
playercs = 0
shield = bytearray([9,6])
shieldicon = bytearray([2,7,2])
playershield = 0
playershieldstock = 0

#enemy char: width: 4 height: 4 and variables to control AI
enemy0 = bytearray([0,6,6,9])
enemy1 = bytearray([0,6,6,6])
enemyshot = bytearray([3,3,3,3]) #old version: enemyshot = bytearray([6,9])
enemyx = [64, 64, 64, 64]
enemyy = [4, 10, 16, 22]
enemydir = [-1,-1,-1,-1]
enemyanim = [0,1,0,1]
enemycs = [0,0,0,0]
enemysx = [-10, -10, -10, -10]
enemysy = [-10, -10, -10, -10]

#explosionsprite
ex0 = bytearray([0,0,0,24,24,0,0,0])
ex1 = bytearray([0,0,36,24,24,36,0,0])
ex2 = bytearray([129,0,36,0,0,36,0,129])
ex3 = bytearray([0,66,0,0,0,0,66,0])
ex4 = bytearray([129,0,0,0,0,0,0,129])
explosionanim = 0
exx = -10 
exy = -10

# screen limits
bordert = 4
borderb = 30
borderl = 2
borderr = 68

#title screen
titleScreen = bytearray([0,0,0,2,2,126,126,2,2,0,126,126,0,126,2,14,24,96,126,0,6,8,112,112,8,6,0,126,2,14,24,96,126,0,0,0,0,0,0,0,
           0,0,0,3,12,48,48,12,3,0,60,10,9,9,10,60,0,63,33,33,18,12,0,63,45,45,33,33,0,63,9,9,54,0,38,41,41,25,0,0,
           0,0,0,0,248,72,72,48,0,248,72,72,176,0,240,104,104,104,0,48,40,72,200,0,48,40,72,200,0,0,240,72,72,240,0,0,0,0,0,0,
           0,0,0,128,129,128,128,128,128,129,128,128,129,128,128,129,129,129,128,129,129,129,128,128,129,129,129,128,128,128,129,128,128,129,128,0,0,0,0,0,
           0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0])
           
#gameover screen
gameoverScreen = bytearray([0,0,0,120,120,128,128,120,120,0,0,240,8,8,8,240,0,0,248,0,0,0,0,248,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,
           0,0,0,128,128,135,7,0,0,0,128,131,4,4,4,131,128,128,3,4,132,132,132,3,0,0,0,128,128,0,0,128,128,0,0,128,128,0,0,0,
           0,0,0,127,64,64,33,30,0,0,127,127,0,0,63,76,76,76,0,0,127,64,64,33,30,0,0,111,111,0,0,111,111,0,0,111,111,0,0,0,
           0,0,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,0,0,
           0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0])

#other variables
gameFPS = 30 #to keep the game speed in check.
score = 0 #game score
gameState = 0 #gamestate (0 = title, 1 = playing, 2 = gameover)

#Start of Code#
def displayInit():
    global gameFPS
    thumby.display.setFPS(gameFPS)
    thumby.display.fill(0)
#EndDef

def varReset():
    global playeranim
    global playerx
    global playery
    global playerw
    global playerh
    global playersx
    global playersy
    global playercs
    global playershield
    global playershieldstock
    
    global enemyx
    global enemyy
    global enemydir
    global enemyanim
    global enemycs
    global enemysx
    global enemysy
    
    global explosionanim
    global exx
    global exy

    global score
    global gameState

    playeranim = 0
    playerx = 2
    playery = 4
    playerw = 4
    playerh = 4
    playersx = -20
    playersy = 2
    playercs = 0
    playershield = 0
    playershieldstock = 0

    score = 0
    gameState = 0
    
    enemyx = [64, 64, 64, 64]
    enemyy = [4, 10, 16, 22]
    enemydir = [-1,-1,-1,-1]
    enemyanim = [0,1,0,1]
    enemycs = [0,0,0,0]
    enemysx = [-10, -10, -10, -10]
    enemysy = [-10, -10, -10, -10]
    
    explosionanim = 0
    exx = -10 
    exy = -10
#EndDef

def playerDraw():
    global player0
    global player1
    global playeranim
    global playershot
    global playerx
    global playery
    global playerw
    global playerh
    global playercs
    global playersx
    global playersy
    global bordert
    global borderb
    global borderl
    global borderr
    global playershield
    global shield
    global playershieldstock
    global shieldicon

    #ship
    if playeranim <= 5:
        playerSprite = thumby.Sprite(playerw, playerh, player0)
    #EndIf
    if playeranim > 5 and playeranim < 10:
        playerSprite = thumby.Sprite(playerw, playerh, player1)
    #EndIf
    playerSprite.x = playerx
    playerSprite.y = playery
    thumby.display.drawSprite(playerSprite)
    
    #shot
    if playercs == 1:
        playersx += 1 
        playerShotSprite = thumby.Sprite(4,4,playershot)
        playerShotSprite.x = playersx
        playerShotSprite.y = playersy
        if playersx > borderr:
            playercs = 0
            playersx = -5
        #EndIf
        thumby.display.drawSprite(playerShotSprite)
    #EndIf
    
    if playershield == 1:
        thumby.display.blit(shield, playerx + 6, playery, 2, 4, 0, 0, 0)        
    #EndIf
    
    if playershieldstock == 1:
        thumby.display.blit(shieldicon, 67, 0, 3, 3, 0, 0, 0)
    #EndIf
#EndDef

def playerControl():
    global playery
    global bordert
    global borderb
    global playercs
    global playersx
    global playersy
    global playeranim
    global playershield
    global playershieldstock
    
    if thumby.buttonU.pressed():
        if playery > bordert:
            playery -= 1
            playeranim += 1
        #EndIf
    #EndIf
    if thumby.buttonD.pressed():
        if playery < borderb:
            playery += 1
            playeranim += 1
        #EndIf
    #EndIf
    if thumby.buttonA.justPressed():
        if playercs == 0:
            thumby.audio.play(440, 100)
            playercs = 1
            playersx = 3
            playersy = playery
        #EndIf
    #EndIf
    if thumby.buttonB.justPressed():
        if playershieldstock == 1:
            playershieldstock = 0
            playershield = 1
            thumby.audio.play(250, 50)
        #EndIf
    #EndIf
    
    if playeranim == 10:
        playeranim = 0
    #EndIf
#EndDef

def enemyDraw():
    global enemy0
    global enemy1
    global enemydir
    global enemyanim
    global enemyx
    global enemyy
    global exx
    global exy
    global enemycs
    global enemysx
    global enemysy

    enemyindex = 0;
    
    while enemyindex < len(enemyy):
        if enemydir[enemyindex] == -1:
            enemyy[enemyindex] -= 1
        #EndIf
        if enemydir[enemyindex] == 1:
            enemyy[enemyindex] += 1
        #EndIf
    
        if enemyy[enemyindex] > borderb:
            enemydir[enemyindex] = enemydir[enemyindex] * -1
            enemyx[enemyindex] -= 4
        #EndIf
    
        if enemyy[enemyindex] < bordert:
            enemydir[enemyindex] = enemydir[enemyindex] * -1
            enemyx[enemyindex] -= 4
        #EndIf 

        if enemyx[enemyindex] < 0:
            enemyx[enemyindex] = 64
        #EndIf

        if enemyanim[enemyindex] <= 5:
            thumby.display.blit(enemy0, enemyx[enemyindex], enemyy[enemyindex], 4, 4, 0, 0, 0)    
        #EndIf
        if enemyanim[enemyindex] > 5 and enemyanim[enemyindex] < 10: 
            thumby.display.blit(enemy1, enemyx[enemyindex], enemyy[enemyindex], 4, 4, 0, 0, 0)    
        #EndIf
    
        enemyanim[enemyindex] += 1
        if enemyanim[enemyindex] == 10:
            enemyanim[enemyindex] = 0
        #EndIf
        
        #Shot Routines
        if enemycs[enemyindex] == 0:
            enemy_dice = 0
            enemy_dice = random.randint(0,150)
            if enemy_dice == 5:
                enemycs[enemyindex] = 1
                enemysx[enemyindex] = enemyx[enemyindex]
                enemysy[enemyindex] = enemyy[enemyindex]
            #EndIf
        #EndIf
        
        if enemycs[enemyindex] == 1:
            enemysx[enemyindex] -= 1
        #EndIf
        
        if enemysx[enemyindex] == -2:
            enemysx[enemyindex] = -100
            enemysy[enemyindex] = -100
            enemycs[enemyindex] = 0
        #EndIf
        
        thumby.display.blit(enemyshot, enemysx[enemyindex], enemysy[enemyindex], 4, 2, 0, 0, 0)
   
        enemyindex += 1
    #EndWhile
#EndDef

def collision_shot_enemy():
    global enemyx
    global enemyy
    global playersx
    global playersy
    global playercs
    global explosionanim
    global exx
    global exy
    global playershieldstock
    global score
    
    enemyindex = 0
    
    while enemyindex < len(enemyy):
        if playersx >= enemyx[enemyindex] and playersx <= enemyx[enemyindex] + 8 and playery >= enemyy[enemyindex] and playery <= enemyy[enemyindex] + 8:
            explosionanim = 1
            exx = enemyx[enemyindex]
            exy = enemyy[enemyindex]
            playercs = 0
            playersx = -5
            enemyx[enemyindex] = 90
            enemyy[enemyindex] = 4
            score += 1
            thumby.audio.play(330,120)
        #EndIf
        enemyindex += 1
    #EndWhile
    
    if score == 5:
        playershieldstock = 1
    #EndIf

#EndDef

def collision_shot_player():
    global playerx
    global playery
    global playershield
    global enemysx
    global enemysy
    global exx
    global exy
    global explosionanim
    global gameState
    global enemyx
    global enemyy
    
    enemyindex = 0
    
    while enemyindex < len(enemysx):
        #Collision Player with EnemyShot#
        if enemysx[enemyindex] == 5 and enemysy[enemyindex] >= playery and enemysy[enemyindex] <= playery + 4:
            if playershield == 0: 
                exx = playerx
                exy = playery
                explosionanim = 1
                thumby.audio.play(120,300)
                gameState = 2
            #EndIf
            
            if playershield == 1:
                thumby.audio.play(200, 100)
                playershield = 0
            #EndIf
        #EndIf
        
        #Collision Player with EnemyShip$
        if enemyx[enemyindex] > 0 and enemyx[enemyindex] < 7 and enemyy[enemyindex] >= playery and enemyy[enemyindex] <= playery + 4:
            if playershield == 0: 
                exx = playerx
                exy = playery
                explosionanim = 1
                thumby.audio.play(120,300)
                gameState = 2
            #EndIf
            
            if playershield == 1:
                thumby.audio.play(200, 100)
                playershield = 0
            #EndIf
        #EndIf
        enemyindex += 1
    #EndWhile
#EndDef

def explosion_animation():
    global ex0
    global ex1
    global ex2
    global ex3
    global ex4
    global explosionanim
    global exx
    global exy
    
    exSprite = thumby.Sprite(8,8,ex0)
    
    if explosionanim > 0 and explosionanim < 3:
        exSprite = thumby.Sprite(8,8,ex0)
    if explosionanim >= 3 and explosionanim < 6:
        exSprite = thumby.Sprite(8,8,ex1)
    if explosionanim >= 6 and explosionanim < 9:
        exSprite = thumby.Sprite(8,8,ex2)
    if explosionanim >= 9 and explosionanim < 11:
        exSprite = thumby.Sprite(8,8,ex3)
    if explosionanim >= 11 and explosionanim < 13:
        exSprite = thumby.Sprite(8,8,ex4)
    
    if explosionanim > 0:
        explosionanim +=1
    
    if explosionanim >= 13:
        explosionanim = 0
    
    exSprite.x = exx
    exSprite.y = exy
    if explosionanim > 0:
        thumby.display.drawSprite(exSprite)
#EndDef

def doTitleScreen():
    global titleScreen
    global gameState
    #titleControl = 0
    
    thumby.display.blit(titleScreen, 15, 5, 40, 40, 0, 0, 0)
    thumby.display.update()
    
    if thumby.buttonA.justPressed():
        gameState = 1
    #EndIf
#EndDef

def doGameOver():
    global gameState
    global gameoverScreen
    
    thumby.display.blit(gameoverScreen, 15,5,40,40,0,0,0)
    thumby.display.update()
    
    if thumby.buttonA.justPressed():
        displayInit()
        varReset()
        gameState = 0
    #EndIf
#EndDef

# code start #
displayInit()
varReset()
while True:
    if gameState == 0:
        doTitleScreen()
    #EndIf
    
    if gameState == 1:
        thumby.display.fill(0)
        playerDraw()    
        enemyDraw()
        playerControl()
        collision_shot_enemy()
        collision_shot_player()
        explosion_animation()
        thumby.display.update()
    #EndIf
    
    if gameState == 2:
        explosion_animation()
        thumby.display.update()
        if explosionanim == 0:
            displayInit()
            doGameOver()
        #EndIf
    #EndIf
#EndWhile