
"""
    Created by: SunnyChowTheGuy
    
    Twitter: https://twitter.com/SunnyChowTheGuy
    YouTube: https://www.youtube.com/@SunnyChowTheDude
    
    Cover Art: @AyreGuitar
    project forked from "3D MAZE" developed by @3DSage
    
    
"""

import time
import thumby
import math
import random
customrender = __import__("/Games/Thoom/customrender")
gamesprite = __import__("/Games/Thoom/gamesprite")
_drawMeltScreen = customrender.drawMeltScreen
_drawBg = customrender.drawBg
_drawWall = customrender.drawWall
_drawWall2 = customrender.drawWall2
_drawMeltScreen = customrender.drawMeltScreen
_drawScaled = customrender.drawScaled
_drawPixel = customrender.drawPixel
_capture = customrender.capture
blitScaledWithMask = customrender.blitScaledWithMask
blitWithMask = customrender.blitWithMask
negativeEffect = customrender.negativeEffect
thumby.display.setFont("/lib/font3x5.bin", 3, 5, 1)

try:
    import emulator
    emulated = True
except ImportError:
    emulated = False
    
thumby.display.setFPS(30)


T_BG = gamesprite.BG
T_NormWall = gamesprite.NormWall
T_DoorWall = gamesprite.DoorWall
T_IconWall = gamesprite.IconWall
T_IconWall2 = gamesprite.IconWall2
T_IconWallD = gamesprite.IconWallD
T_IconWallB = gamesprite.IconWallB
T_DangerWall = gamesprite.DangerWall
T_HexoWall = gamesprite.HexoWall
T_BrickWall = gamesprite.BrickWall
T_SpecialWall = gamesprite.SpecialWall


T_Walls = [0,T_NormWall,T_DoorWall,T_IconWall,T_HexoWall,T_DangerWall,T_BrickWall,T_SpecialWall]
            
T_Title = gamesprite.Title
T_shotgun =  gamesprite.shotgun
T_shotgunM = gamesprite.shotgunM
T_shotgun_idle = gamesprite.shotgun_idle
T_shotgun_idleM = gamesprite.shotgun_idleM
T_shotgun_blast = gamesprite.shotgun_blast
T_shotgun_blastM =gamesprite.shotgun_blastM
T_shotgun_reload = gamesprite.shotgun_reload
T_shotgun_reloadM = gamesprite.shotgun_reloadM
           
T_imp32 = gamesprite.imp32
T_imp24 = gamesprite.imp24
T_imp18 = gamesprite.imp18
T_imp14 = gamesprite.imp14
T_imp10 = gamesprite.imp10
T_imp6 =gamesprite. imp6
T_imp32B = gamesprite.imp32B
T_imp24B = gamesprite.imp24B
T_imp18B = gamesprite.imp18B
T_imp14B = gamesprite.imp14B
T_imp10B = gamesprite.imp10B
T_imp32D = gamesprite.imp32D
T_imp24D = gamesprite.imp24D
T_imp18D = gamesprite.imp18D
T_imp14D = gamesprite.imp14D

T_demon32 = gamesprite.demon32
T_demon24 = gamesprite.demon24
T_demon18 = gamesprite.demon18
T_demon14 = gamesprite.demon14
T_demon10 = gamesprite.demon10
T_demon6 = gamesprite.demon6
T_demon32B = gamesprite.demon32B
T_demon24B = gamesprite.demon24B
T_demon18B = gamesprite.demon18B
T_demon14B = gamesprite.demon14B
T_demon10B = gamesprite.demon10B
T_demon32D = gamesprite.demon32D
T_demon24D = gamesprite.demon24D
T_demon18D = gamesprite.demon18D
T_demon14D = gamesprite.demon14D
            
T_key16 = gamesprite.key16
T_key12 = gamesprite.key12
T_key8 = gamesprite.key8
T_key = gamesprite.keyUI
T_press = gamesprite.pressUI


T_explosion = gamesprite.explosion
T_explosion2 = gamesprite.explosion2
T_fireball = gamesprite.fireball

T_guyLeft = gamesprite.guyLeft
T_guyRight = gamesprite.guyRight
T_guyHurt = gamesprite.guyHurt
T_guyDie = gamesprite.guyDie


musicTitle =[
             4,4,16,4, 4,14,4,4, 12,4,4,11, 4,4,12,14,
             4,4,16,4, 4,14,4,4, 12,4,4,11, 0,0,0,0,
             4,4,16,4, 4,14,4,4, 12,4,4,11, 4,4,12,14,
             4,4,16,4, 4,14,4,4, 12,4,4,11, 0,0,0,0,
             13,13,25,13, 13,23,13,13, 21,13,13,19, 13,13,20,21,
             11,11,23,11, 11,21,11,11, 19,10,10,18, 0,0,0,0,
             4,4,16,4, 4,14,4,4, 12,4,4,11, 4,4,12,14,
             4,4,16,4, 4,14,4,4, 12,4,4,16, 18,19,18,0,
            ]


           
class Boss:
    def __init__(self):
        self.active = 0
        self.minX = -1
        self.maxX = -1
        self.depth = 0
        self.hp = 18
        self.frame = 0
        self.hitFrame = 0
        self.spawnCount = 0
    def update(self):
        global entites
        if(self.hp<=0):
            self.frame+=1
        elif(self.active):
            self.frame+=1
            if(self.frame==50):
                dirX, dirY = normalize(positionX-17.8,positionY-6.5)
                entites.append(FireBall(17.8,6.5, dirX, dirY))
                self.frame=0
                self.spawnCount +=1
                if(self.spawnCount >3):
                    if(len(entites)<5):
                        spawnY = 5.5
                        if(random.random()<0.5):
                            spawnY = 7.5
                        
                        if(random.random()<0.5):
                            en = Imp(17.8,spawnY)
                            en.active = 1
                            entites.append(en)
                        else:
                            en = Demon(17.8,spawnY)
                            en.active = 1
                            entites.append(en)
                        
                    self.spawnCount = 0
            
        if(self.hitFrame>0):
            self.hitFrame-=1
    def shoot(self):
        self.hp -= 1
        self.hitFrame = 10
        if(self.hp<=0):
            self.frame = 0
        
class Entity:
    def __init__(self,x,y):
        self.x = x
        self.y = y
        self.minX = -1
        self.maxX = -1
        self.depth = 0
        self.hp = 1
        self.frame = 0
    def update(self):
        global getKey
        if(self.hp ==0):
            self.frame+=1
            if(self.frame>60):
                return -1
        return 0
    def getAim(self):
        return 0
    def shoot(self):
        0
    def getSprite(self,scale):
        
        sp = 0
        spS = 1
        offset =0
        flip=0
        return sp,spS,offset,flip
    
class Demon(Entity):
    def __init__(self, x,y):
        Entity.__init__(self, x,y)
        self.active =0
        self.attacking =0
            
        
    def getAim(self):
        if(self.hp == 0):
            return 0
        return 1
    def update(self):
        global positionX, positionY
        if(self.hp<=0):
            0
        elif self.active:
            if(self.attacking):
                self.attacking+=1
                if( self.attacking==10 and len2d(positionX-self.x,positionY-self.y)<.8):
                    damage()
                if( self.attacking>=20):
                    self.attacking = 0
            elif len2d(positionX-self.x,positionY-self.y)<.8:
                self.attacking = 1
            else:
                if(self.frame ==0):
                    if( random.random()<0.5):
                        self.speedX,self.speedY = normalize(positionX-self.x,positionY-self.y)
                    else:
                        self.speedX,self.speedY = normalize( random.uniform(-1, 1), random.uniform(-1, 1))

                self.x,self.y,hitWall = move(self.x,self.y,self.speedX,self.speedY,0.06,0.25)
                self.frame+=1
                if(self.frame ==30):self.frame =0;
        elif len2d(positionX-self.x,positionY-self.y)<3:
            self.active=1
                
            
        return Entity.update(self)
    def shoot(self):
        self.hp = 0 
        self.frame=1
    def getSprite(self,scale):
        global frame
        
        sp = 0
        spS = 1
        offset =0
        
        #scale*=0.92 #custom scale
        if self.hp==1:
                if(scale>1.15):
                    sp = T_demon32
                    spS = scale
                elif(scale>1):
                    sp = T_demon32
                elif(scale>.7):
                    sp = T_demon24
                elif(scale>.54):
                    sp = T_demon18
                elif(scale>.4):
                    sp = T_demon14
                elif(scale>.3):
                    sp = T_demon10
                elif(scale>.1):
                    sp = T_demon6
        elif self.frame<6:
                if(scale>1.15):
                    sp = T_demon32B
                    spS = scale
                elif(scale>1):
                    sp = T_demon32B
                elif(scale>.7):
                    sp = T_demon24B
                elif(scale>.54):
                    sp = T_demon18B
                elif(scale>.4):
                    sp = T_demon14B
                elif(scale>.3):
                    sp = T_demon10B
        else:
                if(scale>1.15):
                    sp = T_demon32D
                    spS = scale
                elif(scale>1):
                    sp = T_demon32D
                elif(scale>.7):
                    sp = T_demon24D
                elif(scale>.54):
                    sp = T_demon18D
                elif(scale>.1):
                    sp = T_demon14D
            
            
        flip = (self.active and self.hp==1 and frame%10<5)
        return sp,spS,offset,flip
    
class Imp(Entity):
    def __init__(self, x,y):
        Entity.__init__(self, x,y)
        self.active =0
        self.attacking =0
    
    def update(self):
        global positionX, positionY, entites
        if(self.hp<=0):
            0
        elif self.active:
            self.attacking +=1
            if(self.attacking>=56):
                if( self.attacking>=65):
                    dirX, dirY = normalize(positionX-self.x,positionY-self.y)
                    entites.append(FireBall(self.x,self.y, dirX, dirY))
                    self.attacking = 0
            else:
                if(self.frame ==0):
                    if( len2d(positionX-self.x,positionY-self.y)<1):
                        self.speedX,self.speedY = normalize(self.x-positionX,self.y-positionY)
                    else:
                        self.speedX,self.speedY = normalize( random.uniform(-1, 1), random.uniform(-1, 1))
                self.x,self.y,hitWall = move(self.x,self.y,self.speedX,self.speedY,0.05,0.25)
                self.frame+=1
                if(self.frame ==30):self.frame =0;
        elif len2d(positionX-self.x,positionY-self.y)<3:
            self.active=1
            
        return Entity.update(self)
    def getAim(self):
        if(self.hp == 0):
            return 0
        return 1
    def shoot(self):
        self.hp = 0 
        self.frame=1
    
    def getSprite(self,scale):
        global frame
        sp = 0
        spS = 1
        offset =0
        
        #scale*=0.92 #custom scale
        if self.hp==1:
                if(scale>1.15):
                    sp = T_imp32
                    spS = scale
                elif(scale>1):
                    sp = T_imp32
                elif(scale>.7):
                    sp = T_imp24
                elif(scale>.54):
                    sp = T_imp18
                elif(scale>.4):
                    sp = T_imp14
                elif(scale>.3):
                    sp = T_imp10
                elif(scale>.1):
                    sp = T_imp6
        elif self.frame<6:
                if(scale>1.15):
                    sp = T_imp32B
                    spS = scale
                elif(scale>1):
                    sp = T_imp32B
                elif(scale>.7):
                    sp = T_imp24B
                elif(scale>.54):
                    sp = T_imp18B
                elif(scale>.4):
                    sp = T_imp14B
                elif(scale>.3):
                    sp = T_imp10B
        else:
                if(scale>1.15):
                    sp = T_imp32D
                    spS = scale
                elif(scale>1):
                    sp = T_imp32D
                elif(scale>.7):
                    sp = T_imp24D
                elif(scale>.54):
                    sp = T_imp18D
                elif(scale>.1):
                    sp = T_imp14D
                    
        flip = (self.active and self.hp==1 and frame%10<5)
        return sp,spS,offset,flip
    
class Explosion(Entity):
    def __init__(self, x,y):
        Entity.__init__(self, x,y)
        self.oriX = x;
        self.oriY = y; 
    def update(self):
        if(self.frame ==0):
            thumby.audio.play(60,50)
        self.frame +=1;
        if( self.frame>12):
            self.x = self.oriX + random.uniform(-0.5, 0.5); 
            self.y = self.oriY + random.uniform(-0.5, 0.5); 
            self.frame = 0
    def getSprite(self,scale):
        sp = 0
        spS = 1
        offset =0
        flip = 0
        
        if( self.frame>8):
            0
        elif( self.frame>4):
            sp =T_explosion2
        else:
            sp =T_explosion
        spS = scale
        
        return sp,spS,offset,flip
    
class FireBall(Entity):
    def __init__(self, x,y,dirX,dirY):
        Entity.__init__(self, x,y)
        self.speedX,self.speedY = normalize(dirX,dirY)
    def update(self):
        self.x,self.y,hitWall = move(self.x,self.y,self.speedX,self.speedY,0.12,0.2)
        
        if len2d(self.x-positionX,self.y-positionY)<0.2:
            damage()
            return -1
            
        if(hitWall):
            return -1
        
    def getSprite(self,scale):
        sp = 0
        spS = 1
        offset =0
        flip = 0
        
        sp = T_fireball
        spS = scale
        
        return sp,spS,offset,flip
             
    
class ItemKey(Entity):
    def __init__(self, x,y):
        Entity.__init__(self, x,y)
        
    def update(self):
        global getKey
        if len2d(self.x-(positionX+directionX*0.3),self.y-(positionY+directionY*0.3))<0.3:
            getKey = 1
            thumby.audio.play(1000,50)
            return -1
    def getSprite(self,scale):
        
        sp = 0
        spS = 1
        offset =0
        flip=0
        
        if(scale>1.15):
                sp = T_key16
                spS = scale
        elif(scale>.7):
                sp = T_key16
        elif(scale>.5):
                sp = T_key12
        else:
                sp = T_key8
            
            
        return sp,spS,offset,flip


#the level map
T_Map =  [
           bytearray( [5, 5, 5, 5, 1, 6, 6, 6, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]),
           bytearray( [5, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1]),
           bytearray( [5, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 1, 6, 6, 6, 6, 1]),
           bytearray( [5, 0, 0, 0, 1, 1, 1, 1, 1, 1, 0, 0, 0, 1, 0, 0, 0, 0, 1]),
           bytearray( [5, 5, 5, 5, 1, 0, 0, 0, 0, 1, 1, 0, 1, 1, 0, 7, 0, 0, 1]),
           bytearray( [5, 0, 0, 5, 1, 0, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0, 0, 2]),
           bytearray( [5, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 3]),
           bytearray( [5, 0, 0, 5, 1, 0, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0, 0, 2]),
           bytearray( [5, 5, 5, 5, 1, 0, 0, 0, 0, 1, 0, 0, 0, 1, 0, 7, 0, 0, 1]),
           bytearray( [4, 4, 4, 4, 1, 1, 0, 1, 1, 1, 0, 0, 0, 1, 0, 0, 0, 0, 1]),
           bytearray( [4, 0, 0, 0, 0, 0, 0, 6, 4, 0, 0, 0, 0, 1, 6, 6, 6, 6, 1]),
           bytearray( [4, 0, 0, 0, 6, 0, 0, 6, 4, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1]),
           bytearray( [4, 0, 0, 0, 6, 0, 0, 6, 4, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1]),
           bytearray( [4, 4, 4, 4, 6, 6, 6, 6, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1])]
            
doors = [[4,6],[9,6],[13,6]]
entitesLv1 = [Demon(6,6.5),Demon(8,5),Demon(6.5,11.5),Demon(2.5,11),ItemKey(1.5,11.5)]
entitesLv2 = [Imp(10.5,6.5),Imp(10.5,9),Imp(10.5,1.5),Imp(2.5,1.5),Imp(2.5,3.5),ItemKey(1.5,2.5)]

# Defines starting position and direction
SW = 72
SH = 40
x = 0
y = 0
positionX = 2.5
positionY = 5.5
directionX = 1.0
directionY = 0.0
planeX = 0.0
planeY = 0.5
ROTATIONSPEED = 0.12
MOVESPEED = 0.08
PA = 0 #just for background
TGM = (math.cos(ROTATIONSPEED), math.sin(ROTATIONSPEED))# Trigeometric tuples + variables for index
ITGM = (math.cos(-ROTATIONSPEED), math.sin(-ROTATIONSPEED))
COS, SIN = (0,1)

gameState=0
walking = 0
aiming = 0
shooting = 0
getKey = 0
hp = 100
yOffset = 4

music = 0
frame = -60
depthMap= [0]*72
entites = []
boss = Boss()

gamePhase = 0
negativeVFX = 0

meltMap = bytearray([0]*72);
for i in range(72):
    meltMap[i] = int(12-12*math.cos(3.1415*2*i/72) +random.randrange(10))  

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
    positionX = 1.5; positionY = 6.5; 
    gamePhase = 0
    for door in doors:
       T_Map[door[1]][door[0]] = 2
    
        
@micropython.native
def raycastWall(x:int, rayPositionX:float, rayPositionY:float):
        global frame,emulated,boss
        cameraX = 2.0 * x / SW - 1.0
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
        while  (hit<9):
            hit+=1
            if (sideDistanceX < sideDistanceY): sideDistanceX += deltaDistanceX; mapX += stepX; side = 0;
            else:                               sideDistanceY += deltaDistanceY; mapY += stepY; side = 1;
            if (T_Map[mapY][mapX] > 0): hit = 99
        if(hit!=99):
            return 99
        # Correction against fish eye effect
        if (side == 0): perpWallDistance = abs((mapX - rayPositionX + ( 1.0 - stepX ) / 2.0) / rayDirectionX)
        else:           perpWallDistance = abs((mapY - rayPositionY + ( 1.0 - stepY ) / 2.0) / rayDirectionY)
        # Calculating HEIGHT of the line to draw
        lineHEIGHT = abs(int(SH / (perpWallDistance+.0000001)))
        drawStart = -(lineHEIGHT >>1) + (SH >>1) -yOffset
        # if drawStat < 0 it would draw outside the screen
        tyo=0.0
        if (drawStart < 0): drawStart = 0; tyo=(lineHEIGHT-SH)/2.0;
        drawEnd = (lineHEIGHT >>1)+ (SH >>1)-yOffset
        if (drawEnd >= SH): drawEnd = SH
        # Wall shade
        if (side == 1):
            u = (100+rayPositionX +math.copysign(perpWallDistance/deltaDistanceX,rayDirectionX))%1
        else:
            u = (100+rayPositionY+math.copysign(perpWallDistance/deltaDistanceY, rayDirectionY))%1
        u*=24
        
        w = T_Map[mapY][mapX]
        if(w == 3):
            if(boss.minX>x):boss.minX = x;
            if(boss.maxX<x):boss.maxX = x;
            boss.depth = perpWallDistance
            
        w = T_Walls[w]
        
        _draw = _drawWall
        if emulated:
             _draw = _drawWall2
            
        if(lineHEIGHT>SH):
            _draw( w, x, int(drawStart), int(drawEnd-drawStart),int((lineHEIGHT-SH)/2*12/lineHEIGHT*256) , int(12/lineHEIGHT*256),int(u))
        else:
            _draw( w, x, int(drawStart), int(drawEnd-drawStart),0 , int(12/lineHEIGHT*256),int(u))
 
    #for depth map
        return perpWallDistance
        
        
@micropython.native
def dot(x1:float,y1:float,x2:float,y2:float):
    return x1*x2+y1*y2
    
@micropython.native
def len2d(x:float,y:float):
    return math.sqrt(x*x+y*y)

@micropython.native
def normalize(x:float,y:float):
    l = len2d(x,y)
    return x/l,y/l
            
            
@micropython.native
def prepareDrawEntity(e,renderList):
    entityX = e.x
    entityY =e.y
    entityX-=positionX
    entityY-=positionY
    entityRY = dot(entityX,entityY,directionX,directionY)
    entityRX = dot(entityX,entityY,-directionY,directionX)
    
    e.rx = entityRX
    e.ry = entityRY
    
    if(entityRY>0.2):
        renderList.append(e)
    
    
    
@micropython.native
def drawEntity(e):
    global frame
    
    entityD = e.ry
    entityD2 = e.rx
    e.minX = -1
    e.maxX = -1
    if(entityD>0.2):
        finalX = int(entityD2/entityD*SW+36)
        scale =  1/(entityD+.0000001)
        lineHEIGHT = abs(int(SH/2*scale))
        
        spArr,spS,offset,flip = e.getSprite(scale)
        
        if spArr == 0:
            return
        
        sp = spArr[0];
        spM = spArr[1]
        spW = sp.width
        spH = sp.height
        
        minX = int(finalX-spW*spS/2);
        maxX = int(minX+spW*spS);
        if minX<0 : minX = 0;
        if maxX>=SW : maxX = SW;
        for i in range(minX,maxX):
            if(depthMap[i]<entityD):
                minX+=1
            else:
                break
        n = maxX
        
        for i in range(maxX-minX):
            if(depthMap[n-i-1]<entityD):
                maxX-=1
            else:
                break
        if(maxX-minX <=0): return;
        
        e.minX = minX
        e.maxX = maxX
        if(spS==1):
            blitWithMask( sp.bitmap, int(finalX-spW/2), 20+lineHEIGHT-spH-yOffset-offset,spW, spH, flip,spM.bitmap,minX,maxX)
        else:
            blitScaledWithMask( sp.bitmap, int(finalX-spW*spS/2), 20+lineHEIGHT-int(spH*spS)-yOffset-offset,int(spW*spS), int(spH*spS), flip,spM.bitmap,minX,maxX,int(256/spS),spW)
           
     
def damage():
    global hp,negativeVFX,frame
    if(hp<=0):
        return
    hp-=10
    if(hp<=0):
        frame = 0
    negativeVFX = 1
    
@micropython.native
def sortEntites(e):
  return e.ry
  
@micropython.native
def script():
    global T_Map,entites,gamePhase,doors,getKey
    if(gamePhase == 0):
        door = doors[0]
        if(int(positionX)==door[0]-1 and int(positionY)==door[1]):
            T_Map[door[1]][door[0]] = 0
            entites = entitesLv1
            gamePhase = 1
            thumby.audio.play(60,50)
    elif(gamePhase == 1):
        door = doors[0]
        if(int(positionX)>door[0]):
            T_Map[door[1]][door[0]] = 2
            gamePhase = 2
    elif(gamePhase == 2):
        door = doors[1]
        if(int(positionX)==door[0]-1 and int(positionY)==door[1] and getKey == 1):
            T_Map[door[1]][door[0]] = 0
            getKey =0
            entites = entitesLv2
            gamePhase = 3
            thumby.audio.play(60,50)
    elif(gamePhase == 3):
        door = doors[1]
        if(int(positionX)>door[0]):
            T_Map[door[1]][door[0]] = 2
            gamePhase = 4
            
    elif(gamePhase == 4):
        door = doors[2]
        if(int(positionX)==door[0]-1 and int(positionY)==door[1] and getKey == 1):
            T_Map[door[1]][door[0]] = 0
            getKey =0
            entites = []
            gamePhase = 5
            boss.active =1
            thumby.audio.play(60,50)
        
    elif(gamePhase == 5):
        door = doors[2]
        if(int(positionX)>door[0]):
            T_Map[door[1]][door[0]] = 2
            gamePhase = 6
        
    elif(gamePhase == 6):
        if(boss.hp<=0):
              gamePhase = 4
              entites=[Explosion(17.2,6.5)];
        
@micropython.native
def process(): 
    global positionX,positionY,getKey
    global frame, depthMap, aiming,shooting, emulated
    global T_Walls, T_IconWall, T_IconWall2
    
    if(boss.hp<=0):
        T_Walls[3] = T_IconWallD
    elif(boss.hitFrame>0):
        T_Walls[3] = T_IconWallB
    elif(frame%10<5):
        T_Walls[3] = T_IconWall
    else:
        T_Walls[3] = T_IconWall2
    boss.minX = SW+1
    boss.maxX = -1
    boss.depth = -1
    _drawBg(T_BG,SW,PA)
    if(boss.active):
        boss.update()
    if emulated:
        for x in range(0, (SW>>1) ):
            d = raycastWall(x<<1,positionX,positionY)
            depthMap[x<<1] = d
            depthMap[(x<<1)+1] = d
    else:
        for x in range(0, (SW) ):
            d = raycastWall(x-1,positionX,positionY)
            depthMap[x] = d
    
    renderList= []
    for e in entites:
        res = e.update()
        if(res == -1):
            entites.remove(e)
        else:
            prepareDrawEntity(e,renderList)
        
    renderList.sort(reverse=True, key=sortEntites)
    seeAim = 0
    for e in renderList:
        drawEntity(e)
        if(e.getAim() and abs(e.rx)<.24 and e.ry>0 and e.ry<3): 
            seeAim=e; 
            
    if(seeAim == 0 ):
        if(boss.hp>0 and boss.minX < (SW>>1) and boss.maxX>(SW>>1) and boss.depth<3.5):
            seeAim=boss;
    if(seeAim != 0 and walking<4):
        aiming += 1;
        if(aiming==5):
            thumby.audio.play(200,50)
            seeAim.shoot()
            shooting = 1
    else:
        aiming =0
    if(hp<=0):
        0
    elif(shooting>0):
        if(shooting<3):
            thumby.display.blitWithMask( T_shotgun_blast, 18, 24,15, 17, -1, 0,0,T_shotgun_blastM)
            thumby.display.blitWithMask( T_shotgun_blast, 36, 24,15, 17, -1, 1,0,T_shotgun_blastM)
            thumby.display.blitWithMask( T_shotgun, 29, 36,15, 7, -1, 0,0,T_shotgunM)
        elif(shooting<5):
            thumby.display.blitWithMask( T_shotgun_blast, 18, 24,15, 17, -1, 0,0,T_shotgun_blastM)
            thumby.display.blitWithMask( T_shotgun_blast, 36, 24,15, 17, -1, 1,0,T_shotgun_blastM)
            thumby.display.blitWithMask( T_shotgun, 29, 37,15, 7, -1, 0,0,T_shotgunM)
        elif(shooting<8):
            thumby.display.blitWithMask( T_shotgun, 29-(shooting-5)*3, 37-(shooting-5)*2,15, 7, -1, 0,0,T_shotgunM)
            
        else:
            #thumby.display.blitWithMask( T_shotgun, 29, 37-(shooting>>2),15, 7, -1, 0,0,T_shotgunM)
            sinNum = math.sin((shooting-8)/8*3.14)
            thumby.display.blitWithMask( T_shotgun_idle, 20-min(3,(shooting-8)), 25,47, 15, -1, 0,0,T_shotgun_idleM)
            thumby.display.blitWithMask( T_shotgun_reload, 2+((shooting-8)*3), 32-int(10*sinNum),25, 17, -1, 0,0,T_shotgun_reloadM)
            
    elif(walking==5):
        thumby.display.blitWithMask( T_shotgun_idle, 6, 29+int(3*math.sin(frame)),47, 15, -1, 0,0,T_shotgun_idleM)
    elif(walking>2):
        thumby.display.blitWithMask( T_shotgun_idle, 6+(5-walking)*3, 29+(5-walking),47, 15, -1, 0,0,T_shotgun_idleM)
    else:
        thumby.display.blitWithMask( T_shotgun, 29-walking, 33,15, 7, -1, 0,0,T_shotgunM)
    
    if(shooting>0):
        shooting+=1
        aiming = 0
        if(shooting>18):shooting =0;
    if(getKey ==1):
        thumby.display.blitWithMask( T_key[0], 0, 0,11, 9, -1, 0,0,T_key[1])
    thumby.display.drawFilledRectangle( 55, 0, 19, 7,0)
    hpStr = str(hp)+"%"
    while len(hpStr)<4:
        hpStr = " "+hpStr
    thumby.display.drawText(hpStr, 56, 1, 1)
    frame += 1
    
    
@micropython.native
def move(ox,oy,mx,my,speed,r):
    hitWall = 0
    if not T_Map[int(oy)][int(ox + mx * (speed+r))]:
        ox+= mx* speed
    else:
        hitWall = 1
    if not T_Map[int(oy + my * (speed+r))][int(ox)]:
        oy+= my* speed
    else:
        hitWall = 1
    return ox,oy,hitWall
      
@micropython.native
def selfmove(mx,my):
    global positionX,positionY,walking
    positionX,positionY,hitWall= move(positionX,positionY,mx,my,MOVESPEED,0.3)
    walking = 5

while(1): # Fill canvas to black
    if(gameState==0): #draw title 
        #thumby.display.blit(T_Title, 0, 0, 70, 40)
        thumby.display.fill(0)
        if frame<0:
         
            thumby.display.drawText("Made by", 0,10, 1)
            thumby.display.drawText("@SunnyChowTheGuy", 0, 18, 1)
            
            frame+=1
        elif frame==0:
            thumby.display.blit( T_Title, 0, 0, 72, 40,0,0,0)
            if(thumby.buttonB.pressed() or thumby.buttonA.pressed()):
               frame=1
        elif frame>50:
            #init()
            frame = 0
            gameState=1
        else:
            thumby.display.fill(0)
            _drawMeltScreen(T_Title,meltMap,frame*2-32)
            frame+=1
        
        
        
        if music%5 == 0:
            i = math.floor(music/5)%len(musicTitle)
            if i < len(musicTitle) and musicTitle[i]!= 0:
                timeCount = 1
                for j in range(i+1,len(musicTitle)):
                    if(musicTitle[j]!= 0):
                        break;
                    timeCount+=1
                thumby.audio.play(int(256*math.pow(2,musicTitle[i]/12)),100*timeCount)
        music +=1
    if(gameState==1): #control
        thumby.display.fill(0)
        thumby.display.drawText("^v : move", 1, 2, 1)
        thumby.display.drawText("<> : rotate", 1, 8, 1)
        thumby.display.drawText("<> + B : Strafe", 1, 14, 1)
        thumby.display.drawText("stop : auto shoot", 1, 20, 1)
        if frame%20<10:
            thumby.display.blit( T_press,69, 38, 3, 2, -1,0,0)
        
        frame+=1
        if(thumby.buttonB.pressed() or thumby.buttonA.pressed()):
            gameState = 2
            frame=0
            
    elif(gameState==2): #opening
        thumby.display.fill(1)
        if frame <15:
            thumby.display.blit( T_guyLeft, 24, 5, 24, 29,-1,0,0)
        elif frame <30:
            thumby.display.blit( T_guyRight, 24, 5, 24, 29,-1,0,0)
        elif frame <45:
            thumby.display.blit( T_guyLeft, 24, 5, 24, 29,-1,0,0)
        elif frame <60:
            thumby.display.blit( T_guyRight, 24, 5, 24, 29,-1,0,0)
        elif frame <120:
            thumby.display.drawText("IT'S THOOMIN TIME!", 1, 18, 0)
        elif frame ==120:
            init()
            frame = 0
            gameState=3
            random.seed ( time.ticks_ms())
            continue
            
            
        frame+=1
        
    elif(gameState==3): #main game 
        if(hp>0):
            if(walking>0):walking -=1;
            if(thumby.buttonU.pressed()): 
                selfmove(directionX,directionY)
        
            if(thumby.buttonD.pressed()): 
                selfmove(-directionX,-directionY)
        
            if(thumby.buttonA.pressed()): 
                if(thumby.buttonL.pressed()):
                    selfmove(directionY,-directionX)
                if(thumby.buttonR.pressed()): 
                    selfmove(-directionY,directionX)
                
            else:
                if(thumby.buttonL.pressed()):        
                    oldDirectionX = directionX
                    directionX = directionX * ITGM[COS] - directionY * ITGM[SIN]
                    directionY = oldDirectionX * ITGM[SIN] + directionY * ITGM[COS]
                    oldPlaneX = planeX
                    planeX = planeX * ITGM[COS] - planeY * ITGM[SIN]
                    planeY = oldPlaneX * ITGM[SIN] + planeY * ITGM[COS]
                    PA -= 4
                    if(PA > 71): PA -= 72
                if(thumby.buttonR.pressed()):       
                    oldDirectionX = directionX
                    directionX = directionX * TGM[COS] - directionY * TGM[SIN]
                    directionY = oldDirectionX * TGM[SIN] + directionY * TGM[COS]
                    oldPlaneX = planeX
                    planeX = planeX * TGM[COS] - planeY * TGM[SIN]
                    planeY = oldPlaneX * TGM[SIN] + planeY * TGM[COS]
                    PA += 4
                    if(PA < 0): PA += 72
            if(boss.hp<=0 and boss.frame>90):
                cap = _capture()
                gameState=4
                frame=0
        else:
            
            frame+=1
            if(yOffset<7):
                yOffset+=1
            if frame>=60:
                gameState=6
                frame=0
                
        script()
        process()
            
    elif(gameState==4):# win
        thumby.display.fill(0)
        _drawMeltScreen(cap,meltMap,frame*2-32)
        frame+=1
        if frame>50:
            frame=0
            gameState = 5
        
    elif(gameState==5):# win2
         thumby.display.drawText("CONGRAT!", 1, 10, 1)
         thumby.display.drawText("YOU KILLED", 1, 18, 1)
         thumby.display.drawText("THE EMOJI OF SIN!", 1, 24, 1)
         frame+=1
         if(frame>30):
            if frame%20<10:
                thumby.display.blit( T_press,69, 38, 3, 2, -1,0,0)
            if(thumby.buttonB.pressed() or thumby.buttonA.pressed()):
                thumby.reset()
    elif(gameState==6):# gameover
        if frame <30:
            thumby.display.fill(1)
            thumby.display.blit( T_guyHurt, 24, 5, 24, 29,-1,0,0)
        elif frame <60:
            thumby.display.fill(1)
            thumby.display.blit( T_guyDie, 24, 5, 24, 29,-1,0,0)
        else:
            thumby.display.fill(0)
            thumby.display.drawText("GAME OVER", 18, 17, 1)
            if(frame>90):
                if frame%20<10:
                    thumby.display.blit( T_press,69, 38, 3, 2, -1,0,0)
                if(thumby.buttonB.pressed() or thumby.buttonA.pressed()):
                    thumby.reset()
                    
        frame+=1
                
    if(negativeVFX):
        negativeEffect()
        negativeVFX += 1
        if(negativeVFX>2):negativeVFX=0;
        
    thumby.display.update()
