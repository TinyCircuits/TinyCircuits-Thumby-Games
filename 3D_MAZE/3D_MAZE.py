import time
import thumby
import math

thumby.display.setFPS(30)

#the level map
T_Map =  [
            [1, 2, 1, 1, 5, 1, 1, 1, 4, 1, 1, 1],
            [1, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0, 1],
            [1, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 1],
            [1, 0, 0, 1, 1, 1, 0, 0, 0, 0, 0, 1],
            [1, 1, 0, 0, 0, 0, 0, 1, 0, 0, 1, 1],
            [1, 0, 0, 0, 1, 0, 1, 1, 1, 0, 0, 1],
            [1, 1, 0, 0, 0, 0, 0, 1, 0, 0, 0, 1],
            [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
            [1, 1, 0, 1, 0, 0, 0, 1, 0, 1, 0, 1],
            [1, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 1],
            [1, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 1],
            [1, 1, 1, 1, 3, 1, 1, 1, 1, 1, 1, 1]]


# BITMAP: width: 72, height: 20
T_City = (
1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,0,1,1,1,1,1,
1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,
1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,
1,1,1,1,1,1,0,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,0,0,0,1,
1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,
1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,0,0,0,1,1,1,1,1,1,1,0,1,1,
1,1,1,1,1,1,1,1,0,1,0,1,1,1,1,0,1,1,1,1,1,1,1,1,1,1,1,1,1,1,
1,1,1,1,1,1,1,1,1,1,1,0,0,0,1,1,1,1,1,1,1,1,1,1,1,1,1,1,0,0,
0,0,0,1,1,1,1,1,0,0,0,1,1,1,1,1,1,1,0,0,0,0,0,1,1,1,1,0,1,1,
1,1,1,1,1,0,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,0,0,0,0,0,1,1,1,
1,1,1,1,1,1,1,1,1,1,0,1,0,1,0,1,1,1,1,1,0,1,0,1,1,1,1,1,1,1,
0,1,0,1,0,1,1,1,1,0,1,1,1,1,1,1,1,0,1,1,1,1,1,1,1,1,1,1,1,1,
1,1,1,1,0,1,0,1,0,1,1,1,1,0,0,0,1,1,1,1,1,1,0,0,0,0,0,1,1,1,
1,1,0,0,0,0,0,1,1,1,1,1,0,0,0,0,0,1,1,1,0,0,0,1,1,1,1,1,0,0,
0,1,1,1,1,1,1,1,0,1,1,1,1,1,1,1,0,0,0,0,0,1,1,1,1,0,1,0,0,1,
1,1,1,1,0,1,0,1,0,1,1,1,1,1,0,1,0,1,0,1,1,1,1,1,0,1,0,1,0,1,
1,1,0,1,0,1,1,1,1,0,0,1,0,1,1,1,1,1,1,0,0,0,1,1,1,1,1,0,0,1,
0,1,0,1,1,1,0,0,0,0,0,0,1,1,1,1,0,0,0,0,0,1,1,1,1,0,0,0,0,0,
0,1,1,1,1,1,0,0,0,0,0,1,1,1,0,0,0,1,1,1,0,0,0,0,0,1,1,1,1,0,
0,0,0,0,0,0,1,1,1,0,0,0,0,0,0,1,1,1,0,1,0,1,0,0,0,1,1,1,0,1,
0,1,0,1,1,1,1,0,0,1,0,1,0,0,1,1,1,1,0,1,0,1,0,1,1,1,0,1,0,1,
1,1,0,1,0,1,0,1,1,1,0,0,1,0,1,0,1,0,1,1,1,0,0,1,0,1,0,1,1,1,
0,0,0,0,0,0,0,1,1,1,0,0,0,0,0,1,1,1,0,0,0,0,0,0,0,0,1,1,1,1,
0,0,0,0,0,1,1,0,0,0,0,0,1,1,0,0,0,0,0,1,1,1,0,0,0,0,0,0,0,0,
1,1,1,0,0,0,0,0,0,1,1,1,0,1,0,1,0,1,0,1,1,1,0,1,0,1,0,1,1,1,
0,1,0,1,0,1,0,0,0,1,1,1,0,1,0,1,0,1,1,0,1,0,1,0,1,1,0,1,0,1,
0,1,1,1,0,0,1,0,1,0,1,0,1,1,1,0,0,1,0,1,0,1,1,1,0,0,0,0,0,0,
0,1,1,1,0,0,0,0,0,1,1,1,0,0,0,0,0,0,0,0,0,1,1,1,0,0,0,0,0,1,
1,0,0,0,0,0,1,1,0,0,0,0,0,1,1,1,0,0,0,0,0,0,0,0,1,1,1,0,0,0,
0,0,0,1,1,1,0,1,0,1,0,1,0,1,1,1,0,1,0,1,0,1,1,1,0,1,0,1,0,1,
0,1,0,1,1,1,0,1,0,1,0,1,1,0,1,0,1,0,1,1,0,1,0,1,0,1,1,1,0,0,
1,0,1,0,1,0,1,1,1,0,0,1,0,1,0,1,1,1,0,0,0,0,0,0,0,1,1,1,0,0,
0,0,0,1,1,1,0,0,0,0,0,0,0,0,0,1,1,1,0,0,0,0,0,1,1,0,0,0,0,0,
1,1,0,0,0,0,0,1,1,1,0,0,0,0,0,0,0,0,1,1,1,0,0,0,0,0,0,1,1,1,
0,1,0,1,0,1,0,1,1,1,0,1,0,1,0,1,1,1,0,1,0,1,0,1,0,1,0,1,1,1,
0,1,0,1,0,1,1,0,1,0,1,0,1,1,0,1,0,1,0,1,1,1,0,0,1,0,1,0,1,0,
1,1,1,0,0,1,0,1,0,1,1,1,0,0,0,0,0,0,0,1,1,1,0,0,0,0,0,1,1,1,
0,0,0,0,0,0,0,0,0,1,1,1,0,0,0,0,0,1,1,0,0,0,0,0,1,1,0,0,0,0,
0,1,1,1,0,0,0,0,0,0,0,0,1,1,1,0,0,0,0,0,0,1,1,1,0,1,0,1,0,1,
0,1,1,1,0,1,0,1,0,1,1,1,0,1,0,1,0,1,0,1,0,1,1,1,0,1,0,1,0,1,
1,0,1,0,1,0,1,1,0,1,0,1,0,1,1,1,0,0,1,0,1,0,1,0,1,1,1,0,0,1,
0,1,0,1,1,1,0,0,0,0,0,0,0,1,1,1,0,0,0,0,0,1,1,1,0,0,0,0,0,0,
0,0,0,1,1,1,0,0,0,0,0,1,1,0,0,0,0,0,1,1,0,0,0,0,0,1,1,1,0,0,
0,0,0,0,0,0,1,1,1,0,0,0,0,0,0,1,1,1,0,1,0,1,0,1,0,1,1,1,0,1,
0,1,0,1,1,1,0,1,0,1,0,1,0,1,0,1,1,1,0,1,0,1,0,1,1,0,1,0,1,0,
1,1,0,1,0,1,0,1,1,1,0,0,1,0,1,0,1,0,1,1,1,0,0,0,0,0,0,1,1,1,
0,0,0,0,0,0,0,1,1,1,0,0,0,0,0,1,1,1,0,0,0,0,0,0,0,0,0,1,1,1,
0,0,0,0,0,1,1,0,0,0,0,0,1,1,0,0,0,0,0,1,1,1,0,0,0,0,0,0,0,0,
)

#wall texture
T_Brick = (0,0,1,0,0,1,0,0)

# BITMAP: width: 70, height: 40
T_Title = [5,5,5,5,5,5,5,5,5,5,5,5,5,5,5,5,253,9,19,39,79,159,63,127,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,127,63,159,79,239,47,47,47,47,47,47,47,47,47,47,47,47,47,
           0,0,0,128,128,128,128,128,128,128,128,0,0,0,0,0,255,0,0,0,0,0,129,254,2,2,66,194,2,194,66,130,2,2,194,66,130,66,194,2,194,66,194,2,66,66,194,2,194,66,2,2,254,1,0,0,255,0,0,0,0,0,0,0,0,0,0,0,0,0,
           18,18,18,16,7,28,48,63,30,7,16,18,18,18,18,18,255,18,18,9,9,9,4,255,0,0,5,7,0,7,4,3,0,0,7,0,0,0,7,0,7,1,7,0,6,5,4,0,7,5,0,0,255,18,34,36,255,36,36,33,15,57,97,127,61,15,33,36,36,36,
           128,128,128,128,128,128,128,128,128,128,128,128,128,128,128,128,255,64,32,16,8,4,2,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,2,4,8,31,16,16,16,16,16,16,16,16,16,16,16,16,16,
           0,124,84,40,0,12,112,12,0,40,0,68,84,124,0,124,68,56,0,92,84,116,0,124,20,124,0,124,84,116,0,124,84,68,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]

# BITMAP: width: 24, height: 24
T_win1 = (208,208,208,208,208,208,208,208,208,16,240,0,240,16,208,208,208,208,208,208,208,208,208,208,
           255,255,255,255,255,255,135,183,183,0,255,0,255,0,183,183,135,255,255,255,255,255,255,255,
           11,11,11,11,11,11,11,11,11,8,15,0,15,8,11,11,11,11,11,11,11,11,11,11)

T_win2 = (64,160,160,144,208,232,8,252,224,0,224,32,224,0,224,0,252,8,232,208,144,160,160,64,
           255,255,255,255,143,175,0,255,0,0,243,18,243,0,243,0,255,0,175,143,255,255,255,255,
           2,5,5,9,11,23,16,63,0,0,1,1,1,0,1,0,63,16,23,11,9,5,5,2)

T_win3 = (64,176,14,255,0,0,224,0,224,0,224,32,224,0,224,0,224,0,0,0,255,14,176,64,
           255,255,0,255,240,0,128,3,240,0,243,18,243,0,243,18,243,0,112,0,255,0,255,255,
           2,13,112,255,0,1,0,1,0,0,1,1,1,0,1,0,1,0,1,0,255,112,13,2)

T_win4 = (255,0,0,0,0,0,224,0,224,0,224,32,224,0,224,0,224,0,0,0,0,0,0,255,
           255,0,0,0,240,0,128,3,240,0,243,18,243,0,243,18,243,0,112,0,0,0,0,255,
           255,0,0,0,0,1,0,1,0,0,1,1,1,0,1,0,1,0,1,0,0,0,0,255)

# BITMAP: width: 8, height: 8
T_Fire_1 = (0,64,224,208,132,224,176,0)
T_Fire_2 = (0,144,224,240,200,224,160,0)
T_Fire_3 = (0,84,248,225,180,240,160,0)
T_Fire_4 = (40,208,132,176,248,212,128,0)


# Defines starting position and direction
SW = 70
SH = 40
x = 0
y = 0
positionX = 2.5
positionY = 5.5
directionX = 1.0
directionY = 0.0
planeX = 0.0
planeY = 0.5
ROTATIONSPEED = 0.3
MOVESPEED = 0.4
PA = 0 #player angle
TGM = (math.cos(ROTATIONSPEED), math.sin(ROTATIONSPEED))# Trigeometric tuples + variables for index
ITGM = (math.cos(-ROTATIONSPEED), math.sin(-ROTATIONSPEED))
COS, SIN = (0,1)
timer=0.0
gameState=0
level=2
exitX=1
exitY=1
expert=0 #expert mode


def init():
    global positionX 
    global positionY 
    global directionX 
    global directionY 
    global planeX  
    global planeY 
    global PA  
    global TGM 
    global ITGM 
    global COS 
    global SIN
    global exitX
    global exitY
    directionX = 1.0
    directionY = 0.0
    planeX = 0.0
    planeY = 0.5
    PA = 0 #player angle
    if(level==2): positionX = 2.5; positionY = 5.5; exitX=1; exitY=1; #start pos, win pos
    if(level==3): positionX = 6.5; positionY = 9.5; exitX=4; exitY=10; #start pos, win pos    
    if(level==4): positionX = 4.5; positionY = 2.5; exitX=8; exitY=1; #start pos, win pos   
    
def rays(): 
    for x in range(0, SW):
        cameraX = 2.0 * x / SW - 1.0
        rayPositionX = positionX
        rayPositionY = positionY
        rayDirectionX = directionX + planeX * cameraX
        rayDirectionY = directionY + planeY * cameraX + .000000000000001 # avoiding ZDE 
        # In what square is the ray?
        mapX = int(rayPositionX)
        mapY = int(rayPositionY)
        # Delta distance calculation
        deltaDistanceX = math.sqrt(1.0 + (rayDirectionY * rayDirectionY) / (rayDirectionX * rayDirectionX))
        deltaDistanceY = math.sqrt(1.0 + (rayDirectionX * rayDirectionX) / (rayDirectionY * rayDirectionY))
        # We need sideDistanceX and Y for distance calculation. Checks quadrant
        if (rayDirectionX < 0): stepX = -1; sideDistanceX = (rayPositionX - mapX) * deltaDistanceX
        else:                   stepX =  1; sideDistanceX = (mapX + 1.0 - rayPositionX) * deltaDistanceX
        if (rayDirectionY < 0): stepY = -1; sideDistanceY = (rayPositionY - mapY) * deltaDistanceY
        else:                   stepY =  1; sideDistanceY = (mapY + 1.0 - rayPositionY) * deltaDistanceY
        # Finding distance to a wall
        hit = 0
        while  (hit == 0):
            if (sideDistanceX < sideDistanceY): sideDistanceX += deltaDistanceX; mapX += stepX; side = 0;
            else:                               sideDistanceY += deltaDistanceY; mapY += stepY; side = 1;
            if (T_Map[mapY][mapX] > 0): hit = 1
        # Correction against fish eye effect
        if (side == 0): perpWallDistance = abs((mapX - rayPositionX + ( 1.0 - stepX ) / 2.0) / rayDirectionX)
        else:           perpWallDistance = abs((mapY - rayPositionY + ( 1.0 - stepY ) / 2.0) / rayDirectionY)
        # Calculating HEIGHT of the line to draw
        lineHEIGHT = abs(int(SH / (perpWallDistance+.0000001)))
        drawStart = -lineHEIGHT / 2.0 + SH / 2.0
        # if drawStat < 0 it would draw outside the screen
        tyo=0.0
        if (drawStart < 0): drawStart = 0; tyo=(lineHEIGHT-SH)/2.0;
        drawEnd = lineHEIGHT / 2.0 + SH / 2.0
        if (drawEnd >= SH): drawEnd = SH - 1
        # Wall shade
        tys=8.0 / lineHEIGHT
        ty =tyo*tys
        for y in range(int(drawStart), int(drawEnd)):
            color=T_Brick[int(ty)]
            ty+=tys        
            if (side == 1): color=abs(color-1) #inverted texture
            if(T_Map[mapY][mapX]==level): color=0 #exit wall
            if(expert==1): color=0 #all walls black
            if( color==1): thumby.display.setPixel(x, y, color)#draw wall
        # draw sky
        xo = PA - x
        if (xo < 0): xo += 72; xo = xo % 72
        for y in range(0, int(drawStart)-2):
            color=T_City[y*72+xo]
            if( color==1): thumby.display.setPixel(x, y, color)#sky
            thumby.display.setPixel(x, 40-y,1)#floor
  

while(1):
    thumby.display.fill(0) # Fill canvas to black
    if(gameState==0): #draw title 
        #thumby.display.blit(T_Title, 0, 0, 70, 40)
        thumby.display.blit( bytearray(T_Title), 0, 0, 70, 40,0,0,0)
        if(int(timer)==0): thumby.display.blit(bytearray(T_Fire_1), 59, 7, 8, 8, 0,0,0); thumby.display.blit(bytearray(T_Fire_3), 3, 6, 8, 8, 0,0,0)
        if(int(timer)==1): thumby.display.blit(bytearray(T_Fire_2), 59, 7, 8, 8, 0,0,0); thumby.display.blit(bytearray(T_Fire_4), 3, 6, 8, 8, 0,0,0)
        if(int(timer)==2): thumby.display.blit(bytearray(T_Fire_3), 59, 7, 8, 8, 0,0,0); thumby.display.blit(bytearray(T_Fire_1), 3, 6, 8, 8, 0,0,0)
        if(int(timer)==3): thumby.display.blit(bytearray(T_Fire_4), 59, 7, 8, 8, 0,0,0); thumby.display.blit(bytearray(T_Fire_2), 3, 6, 8, 8, 0,0,0) 
        timer+=0.05 
        if(timer>4): timer=0; 
        if(thumby.buttonB.pressed() or thumby.buttonA.pressed()): init(); gameState=1; thumby.display.fill(0)
        
    if(gameState==1): #main game 
        if(thumby.buttonU.pressed()): 
            if not T_Map[int(positionY)][int(positionX + directionX * MOVESPEED*2)]:
                positionX += directionX * MOVESPEED
            if not T_Map[int(positionY + directionY * MOVESPEED*2)][int(positionX)]:
                 positionY += directionY * MOVESPEED
    
        if(thumby.buttonD.pressed()): 
            if not T_Map[int(positionX - directionX * MOVESPEED*2)][int(positionY)]:
                positionX -= directionX * MOVESPEED
            if not T_Map[int(positionX)][int(positionY - directionY * MOVESPEED*2)]:
                positionY -= directionY * MOVESPEED
    
        if(thumby.buttonL.pressed()):        
            oldDirectionX = directionX
            directionX = directionX * ITGM[COS] - directionY * ITGM[SIN]
            directionY = oldDirectionX * ITGM[SIN] + directionY * ITGM[COS]
            oldPlaneX = planeX
            planeX = planeX * ITGM[COS] - planeY * ITGM[SIN]
            planeY = oldPlaneX * ITGM[SIN] + planeY * ITGM[COS]
            PA += 20
            if(PA > 71): PA -= 72
        if(thumby.buttonR.pressed()):       
            oldDirectionX = directionX
            directionX = directionX * TGM[COS] - directionY * TGM[SIN]
            directionY = oldDirectionX * TGM[SIN] + directionY * TGM[COS]
            oldPlaneX = planeX
            planeX = planeX * TGM[COS] - planeY * TGM[SIN]
            planeY = oldPlaneX * TGM[SIN] + planeY * TGM[COS]
            PA -= 20 
            if(PA < 0): PA += 72
        rays()
        if(int(positionX)==exitX and int(positionY)==exitY): #won level
            timer=0; gameState=2; level+=1; 
            if(level>4): gameState=3 
         
    if(gameState==2): #win level
        thumby.display.drawText("YES!!", 20,  8, 1)
        thumby.display.drawText("Next", 22, 19, 1)
        thumby.display.drawText("Level",19, 29, 1)
        timer+=0.1
        if(timer>50): init(); timer=0; gameState=1;  

    if(gameState==3): #win game
        thumby.display.drawText("Congrats!", 7,  2, 1)
        if(int(timer)==0): thumby.display.blit(bytearray(T_win1), 23, 13, 24, 24, 0,0,0)
        if(int(timer)==1): thumby.display.blit(bytearray(T_win2), 23, 13, 24, 24, 0,0,0)
        if(int(timer)==2): thumby.display.blit(bytearray(T_win3), 23, 13, 24, 24, 0,0,0)
        if(int(timer)==3): thumby.display.blit(bytearray(T_win4), 23, 13, 24, 24, 0,0,0)
        if(int(timer)==4): thumby.display.blit(bytearray(T_win4), 23, 13, 24, 24, 0,0,0)
        if(int(timer)==5): thumby.display.blit(bytearray(T_win3), 23, 13, 24, 24, 0,0,0)
        if(int(timer)==6): thumby.display.blit(bytearray(T_win2), 23, 13, 24, 24, 0,0,0)
        if(int(timer)==7): thumby.display.blit(bytearray(T_win1), 23, 13, 24, 24, 0,0,0)
        timer+=0.015 
        if(timer>7): timer=0;  
        if(thumby.buttonB.pressed() or thumby.buttonA.pressed()): timer=0; gameState=4
        
    if(gameState==4): #expert mode
        thumby.display.drawText("Hard Mode", 7, 20, 1)
        timer+=0.1 
        if(timer>50): expert=1; gameState=0; level=2; timer=0;  
    
    thumby.display.update()
