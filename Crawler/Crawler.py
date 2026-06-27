import time
import thumby
import math
import random
from usys import stdin
from uselect import poll




background = bytearray([255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,
            255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,
            255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,
            255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,
            255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255])

#---------------------------Character Sprite Forward-------------------------------
mainBodyF = bytearray([6,82,6])
rightBodyF = bytearray([2,9])
leftBodyF = bytearray([4])

gunF = bytearray([0,2])

# Make a sprite object using bytearray (a path to binary file from 'IMPORT SPRITE' is also valid)
backgroundSprite = thumby.Sprite(72,40, background)
mainBodySpriteF = thumby.Sprite(3, 7, mainBodyF)
rightBodySpriteF = thumby.Sprite(2,5,rightBodyF)
leftBodySpriteF = thumby.Sprite(1,5,leftBodyF)
gunSpriteF = thumby.Sprite(2,2,gunF)

mainBodySpriteF.x = 34
mainBodySpriteF.y = 19

rightBodySpriteF.x = 37
rightBodySpriteF.y = 19

leftBodySpriteF.x = 33
leftBodySpriteF.y = 20

gunSpriteF.x = 39
gunSpriteF.y = 22
#---------------------------Character Sprite Backwards-----------------------------
mainBodyB = bytearray([6,82,6])
leftBodyB = bytearray([9,2])
gunB = bytearray([2,0])
rightBodyB = bytearray([4])

mainBodySpriteB = thumby.Sprite(3,7,mainBodyB)
leftBodySpriteB = thumby.Sprite(2,5,leftBodyB)
rightBodySpriteB = thumby.Sprite(1,5,rightBodyB)
gunSpriteB = thumby.Sprite(2,2,gunB)

mainBodySpriteB.x = mainBodySpriteF.x+1
mainBodySpriteB.y = mainBodySpriteF.y

leftBodySpriteB.x = mainBodySpriteB.x-2
leftBodySpriteB.y = mainBodySpriteB.y

rightBodySpriteB.x = mainBodySpriteB.x+3
rightBodySpriteB.y = mainBodySpriteB.y+1

gunSpriteB.x = mainBodySpriteB.x-4
gunSpriteB.y = mainBodySpriteB.y+3
#---------------------------Character Sprite Up------------------------------------
mainBodyU = bytearray([73,6,86,86,6,105,103])

mainBodySpriteU = thumby.Sprite(7,7,mainBodyU)

mainBodySpriteU.x = mainBodySpriteF.x-1
mainBodySpriteU.y = mainBodySpriteF.y
#---------------------------Character Sprite Down----------------------------------
mainBodyD = bytearray([73,2,86,86,2,105,79])

mainBodySpriteD = thumby.Sprite(7,7,mainBodyD)

mainBodySpriteD.x = mainBodySpriteU.x
mainBodySpriteD.y = mainBodySpriteU.y

#---------------------------Blocks-------------------------------------------------
hWall = bytearray([0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0])
topWallSprite = thumby.Sprite(70,3,hWall)
bottomWallSprite = thumby.Sprite(70,3,hWall)

vWallSmall = bytearray([0,0,0,0,0,0])
vWall = bytearray([0,0,0,0,0,0,0,0,0,0,0,0,0,0,0])
vWallSprite = thumby.Sprite(3, 38, vWall)
vWallSmallSprite2 = thumby.Sprite(2,20,vWall)
vWallSmallSprite1 = thumby.Sprite(3,10,vWallSmall)
vWallSmallSprite = thumby.Sprite(3, 10, vWallSmall)

topWallSprite.x = 1
topWallSprite.y = 1

bottomWallSprite.x = 1
bottomWallSprite.y = 36

vWallSprite.x = 67
vWallSprite.y = 1

vWallSmallSprite.x = 2
vWallSmallSprite.y = 1

vWallSmallSprite1.x = 2
vWallSmallSprite1.y =29

vWallSmallSprite2.x = 4
vWallSmallSprite2.y =10

#Type 2 Walls
hWallSmall = bytearray([0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0])
hWallDoor = bytearray([0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0])

hWallSmallSprite = thumby.Sprite(25, 3, hWallSmall)
hWallSmallSprite1 = thumby.Sprite(25, 3, hWallSmall)
hWallDoorSprite = thumby.Sprite(25, 2, hWallDoor)
vWallSprite1 = thumby.Sprite(3, 38, vWall)

exitWalls = [topWallSprite, bottomWallSprite, vWallSprite, vWallSmallSprite1, vWallSmallSprite]
exitWalls1 = [hWallSmallSprite1, hWallSmallSprite, topWallSprite, vWallSprite, vWallSprite1]
exitWalls2 = [hWallDoorSprite, vWallSmallSprite2]

newPlayerPos = [10, 6, 5, 35]

#---------------------------Bullets------------------------------------------------
# BITMAP: width: 2, height: 1
bulletX = bytearray([0,0])
bulletY = bytearray([0])

#---------------------------Null Sprite--------------------------------------------
null = bytearray([1])
nullSprite = thumby.Sprite(1,1,null)

#---------------------------Slime Sprites------------------------------------------
slimeSleep = bytearray([65,62,46,10,42,46,42,42,65])
slimeSleepSprite = thumby.Sprite(9,7,slimeSleep)
slimeSleepSprite.x = 32
slimeSleepSprite.y = 17

slimeWake = bytearray([65,62,46,12,42,46,42,44,65])
slimeWakeSprite = thumby.Sprite(9,7,slimeWake)
slimeWakeSprite.x = slimeSleepSprite.x
slimeWakeSprite.y = slimeSleepSprite.y

slimeBoss = bytearray([129,126,58,86,94,86,58,129])
slimeBossSprite = thumby.Sprite(8,8,slimeBoss)
slimeBossSprite.x = slimeSleepSprite.x
slimeBossSprite.y = slimeSleepSprite.y

slimeBoss1 = bytearray([65,62,28,42,46,42,28,65])
slimeBoss1Sprite = thumby.Sprite(8,7,slimeBoss1)
slimeBoss1Sprite.x = slimeSleepSprite.x
slimeBoss1Sprite.y = slimeSleepSprite.y+1

slimeBoss2 = bytearray([33,30,12,18,22,22,18,12,33])
slimeBoss2Sprite = thumby.Sprite(9,6,slimeBoss2)
slimeBoss2Sprite.x = slimeSleepSprite.x
slimeBoss2Sprite.y = slimeSleepSprite.y+2

slimeBoss3 = bytearray([9,6,6,4,2,6,2,4,9])
slimeBoss3Sprite = thumby.Sprite(9,4,slimeBoss3)
slimeBoss3Sprite.x = slimeSleepSprite.x
slimeBoss3Sprite.y = slimeSleepSprite.y+3

slimeDeath = bytearray([3,5,5,6,6,6,5,5,3])
slimeDeathSprite = thumby.Sprite(9,4,slimeDeath)
slimeBoss3Sprite.x = slimeDeathSprite.x
slimeBoss3Sprite.y = slimeDeathSprite.y+3

slimeStates = [slimeSleepSprite, slimeWakeSprite, slimeBossSprite, slimeBoss1Sprite, slimeBoss2Sprite, slimeBoss3Sprite, slimeDeathSprite]

#---------------------------Sentry Sprite------------------------------------------
sentrySleep1 = bytearray([16,108,170,108,108,170,108,16])
sentrySleep1Sprite = thumby.Sprite(8,8,sentrySleep1)
sentrySleep1Sprite.x = 32
sentrySleep1Sprite.y = 15

sentrySleep2 = bytearray([16,108,170,106,110,170,106,16])
sentrySleep2Sprite = thumby.Sprite(8,8,sentrySleep2)
sentrySleep2Sprite.x = sentrySleep1Sprite.x
sentrySleep2Sprite.y = sentrySleep1Sprite.y

cage1 = bytearray([0,254,254,254,254,254,254,254,254,254,254,0,0,7,7,7,7,7,7,7,7,7,7,0])
cage1Sprite = thumby.Sprite(12,12,cage1)
cage1Sprite.x = sentrySleep1Sprite.x-2
cage1Sprite.y = sentrySleep1Sprite.y-2

cage2 = bytearray([26,255,254,254,254,255,254,254,254,255,254,18,2,7,15,15,7,7,15,7,7,15,7,1])
cage2Sprite = thumby.Sprite(12,12,cage2)
cage2Sprite.x = cage1Sprite.x
cage2Sprite.y = cage1Sprite.y

sGun1 = bytearray([0,0])
sGun1Sprite = thumby.Sprite(2, 2,sGun1)
sGun1Sprite.x = cage1Sprite.x-1
sGun1Sprite.y = cage1Sprite.y-1

sGun2Sprite = thumby.Sprite(2, 2,sGun1)
sGun2Sprite.x = cage1Sprite.x-1
sGun2Sprite.y = cage1Sprite.y+5

sGun3Sprite = thumby.Sprite(2, 2,sGun1)
sGun3Sprite.x = cage1Sprite.x-1
sGun3Sprite.y = cage1Sprite.y+11

sGun4Sprite = thumby.Sprite(2, 2,sGun1)
sGun4Sprite.x = cage1Sprite.x+5
sGun4Sprite.y = cage1Sprite.y-1

sGun5Sprite = thumby.Sprite(2, 2,sGun1)
sGun5Sprite.x = cage1Sprite.x+11
sGun5Sprite.y = cage1Sprite.y-1

sGun6Sprite = thumby.Sprite(2, 2,sGun1)
sGun6Sprite.x = cage1Sprite.x+5
sGun6Sprite.y = cage1Sprite.y+11

sGun7Sprite = thumby.Sprite(2, 2,sGun1)
sGun7Sprite.x = cage1Sprite.x+11
sGun7Sprite.y = cage1Sprite.y+5

sGun8Sprite = thumby.Sprite(2, 2,sGun1)
sGun8Sprite.x = cage1Sprite.x+11
sGun8Sprite.y = cage1Sprite.y+11

sentrySprites = [cage2Sprite,cage1Sprite, sentrySleep2Sprite, sGun1Sprite, sGun2Sprite, sGun3Sprite, sGun4Sprite, sGun5Sprite, sGun6Sprite, sGun7Sprite, sGun8Sprite, sentrySleep1Sprite]
sentrySleepSprites = [cage2Sprite,cage1Sprite, sGun1Sprite, sGun2Sprite, sGun3Sprite, sGun4Sprite, sGun5Sprite, sGun6Sprite, sGun7Sprite, sGun8Sprite, sentrySleep2Sprite]
sentryWakeSprites = [cage2Sprite,cage1Sprite, sentrySleep1Sprite, sGun1Sprite, sGun2Sprite, sGun3Sprite, sGun4Sprite, sGun5Sprite, sGun6Sprite, sGun7Sprite, sGun8Sprite]

#---------------------------Cannon Sprite------------------------------------------
cannonSleep1 = bytearray([0,14,13,11,11,11,11,13,14,0])
cannonSleep1Sprite = thumby.Sprite(10, 5, cannonSleep1)
cannonSleep1Sprite.x = 32
cannonSleep1Sprite.y = 20

cannonSleep2 = bytearray([192,190,122,90,94,122,186,192])
cannonSleep2Sprite = thumby.Sprite(8, 8, cannonSleep2)
cannonSleep2Sprite.x = cannonSleep1Sprite.x+1
cannonSleep2Sprite.y = cannonSleep1Sprite.y-5

cannonWake1 = bytearray([192,190,114,86,94,118,178,192])
cannonWake1Sprite = thumby.Sprite(8, 8, cannonWake1)
cannonWake1Sprite.x = cannonSleep2Sprite.x
cannonWake1Sprite.y = cannonSleep2Sprite.y

cannonWake2 = bytearray([192,178,118,94,86,114,190,192])
cannonWake2Sprite = thumby.Sprite(8, 8, cannonWake2)
cannonWake2Sprite.x = cannonSleep2Sprite.x
cannonWake2Sprite.y = cannonSleep2Sprite.y

ball1 = bytearray([195,189,102,90,90,102,189,195])
ball1Sprite = thumby.Sprite(8, 8, ball1)
ball1Sprite.x = cannonSleep2Sprite.x
ball1Sprite.y = cannonSleep2Sprite.y

ball2 = bytearray([195,165,90,60,60,90,165,195])
ball2Sprite = thumby.Sprite(8, 8, ball2)
ball2Sprite.x = cannonSleep2Sprite.x
ball2Sprite.y = cannonSleep2Sprite.y

ballBoom1 = bytearray([195,189,126,126,126,126,189,195])
ballBoom1Sprite = thumby.Sprite(8, 8, ballBoom1)
ballBoom1Sprite.x = cannonSleep2Sprite.x
ballBoom1Sprite.y = cannonSleep2Sprite.y

ballBoom2 = bytearray([255,255,231,219,219,231,255,255])
ballBoom2Sprite = thumby.Sprite(8, 8, ballBoom2)
ballBoom2Sprite.x = cannonSleep2Sprite.x
ballBoom2Sprite.y = cannonSleep2Sprite.y

ballBoom3 = bytearray([102,165,219,60,60,219,165,102])
ballBoom3Sprite = thumby.Sprite(8, 8, ballBoom3)
ballBoom3Sprite.x = cannonSleep2Sprite.x
ballBoom3Sprite.y = cannonSleep2Sprite.y

ballBoom4 = bytearray([206,205,75,255,112,112,255,75,205,206,1,2,3,3,0,0,3,3,2,1])
ballBoom4Sprite = thumby.Sprite(10, 10, ballBoom4)
ballBoom4Sprite.x = cannonSleep2Sprite.x
ballBoom4Sprite.y = cannonSleep2Sprite.y

ballBoom5 = bytearray([206,205,255,255,252,252,255,255,205,206,1,2,3,3,0,0,3,3,2,1])
ballBoom5Sprite = thumby.Sprite(10, 10, ballBoom5)
ballBoom5Sprite.x = cannonSleep2Sprite.x
ballBoom5Sprite.y = cannonSleep2Sprite.y

ballBoom6 = bytearray([207,255,255,255,254,254,255,255,255,207,3,3,3,3,1,1,3,3,3,3])
ballBoom6Sprite = thumby.Sprite(10, 10, ballBoom6)
ballBoom6Sprite.x = cannonSleep2Sprite.x
ballBoom6Sprite.y = cannonSleep2Sprite.y

cannonSprites = [cannonSleep2Sprite, cannonWake1Sprite, cannonWake2Sprite, cannonSleep1Sprite,ball1Sprite, ball2Sprite, ballBoom1Sprite, ballBoom2Sprite, ballBoom3Sprite, ballBoom4Sprite]
ballSprites = [ball1Sprite, ball2Sprite, ballBoom1Sprite, ballBoom2Sprite, ballBoom3Sprite, ballBoom4Sprite, ballBoom5Sprite, ballBoom6Sprite]
ball = ballSprites[0]

#---------------------------Loot---------------------------------------------------
heartLoot = bytearray([57,54,46,29,46,54,57])
heartLootSprite = thumby.Sprite(7, 6, heartLoot)
heartLootSprite.x = 100
heartLootSprite.y = 100

heartLoot1 = bytearray([227,221,182,110,222,189,254,126,190,221,227,3,3,3,3,2,1,2,3,3,3,3])
heartLoot1Sprite = thumby.Sprite(11, 10, heartLoot1)
heartLoot1Sprite.x = 98
heartLoot1Sprite.y = 98

heartBeat = time.ticks_ms()
heartChange = False

heartSprites = [heartLoot1Sprite, heartLootSprite]
moveHeart = False

lootBackground = bytearray([127,127,127,127,127,127,127,127,127,127,127,127,127,127,127,127,127,127,127,127,127,127,127,127,127,127,127,127,127,127,127,127,127,127,127,127,127,127,127,127,127,127,127,127,0])
lootBackgroundSprite = thumby.Sprite(45, 8, lootBackground)

chest = bytearray([1,54,54,38,42,38,54,54,1])
chestSprite = thumby.Sprite(9,7, chest)

chestOpen =  bytearray([3,157,30,30,28,30,30,157,3,0,1,1,1,1,1,1,1,0])
chestOpenSprite = thumby.Sprite(9,10, chestOpen)

xSpeed = bytearray([2,8,31,21,27,21,31,8,6,31,0,26,24,31,0,10,31,0,10,31,0,14,17,31,8])
xSpeedSprite = thumby.Sprite(25,5,xSpeed)

xBullets = bytearray([2,12,31,21,27,21,31,0,10,4,31,0,15,0,31,0,15,31,0,15,31,0,10,31,30,0,30,31,8,2,31,8,31,31,31])
xBulletsSprite = thumby.Sprite(35, 5, xBullets)

xDamage = bytearray([2,12,31,21,27,21,31,0,14,17,31,1,26,1,31,0,29,27,29,0,31,1,26,1,31,17,14,10,19,31,0,10,31,8,31])
xDamageSprite = thumby.Sprite(35, 5, xDamage)

maxHealth = bytearray([0,29,27,29,0,31,1,26,1,31,4,27,4,31,27,27,31,0,27,0,31,0,10,31,1,26,1,31,0,15,31,30,0,30,31,0,27,0,31,8])
maxHealthSprite = thumby.Sprite(40,5,maxHealth)

lootSprites = [xSpeedSprite, xBulletsSprite, xDamageSprite, maxHealthSprite, lootBackgroundSprite]
lootTime = time.ticks_ms()
lootLoop = False
isChestOpen = False
giveLoot = False
lootInUse = [0,0,0]
currentLoot = 0

#---------------------------Health-------------------------------------------------
heartMeter = bytearray([28,50,109,91,109,115,127,127,127,62,28])
heartMeterSprite = thumby.Sprite(11, 7, heartMeter)
heartMeterSprite.x = 0
heartMeterSprite.y = 0

h3 = bytearray([10,0])
h3Sprite = thumby.Sprite(2, 5, h3)
h3Sprite.x = 7
h3Sprite.y = 1

h2 = bytearray([2,8])
h2Sprite = thumby.Sprite(2, 5, h2)
h2Sprite.x = 7
h2Sprite.y = 1

h1 = bytearray([31,0])
h1Sprite = thumby.Sprite(2, 5, h1)
h1Sprite.x = 7
h1Sprite.y = 1

healthList = [heartMeterSprite, h1Sprite, h2Sprite, h3Sprite]

health = 3
reset = False

#---------------------------Z's----------------------------------------------------
z1 = bytearray([0,0,0])
z1Sprite= thumby.Sprite(3, 1, z1)

z2 = bytearray([0])
z2Sprite = thumby.Sprite(1,1,z2)

#---------------------------Initiating Enemy Values--------------------------------
enemyList = []

newEPosX = 0
newEPosY = 0

enemyDir = 0

#---------------------------Variables----------------------------------------------
thumby.display.setFPS(60)


keyboard = poll()
keyboard.register(stdin)

bulletActive = False
bulletsList = []

playerColliderListF = [mainBodySpriteF, rightBodySpriteF, leftBodySpriteF, gunSpriteF]
playerColliderListB = [mainBodySpriteB, rightBodySpriteB, leftBodySpriteB, gunSpriteB]
playerColliderListU = [mainBodySpriteU]
playerColliderListD = [mainBodySpriteD]

playerColliderListAll = [mainBodySpriteF, rightBodySpriteF, leftBodySpriteF, mainBodySpriteB, rightBodySpriteB, leftBodySpriteB, mainBodySpriteU, mainBodySpriteD]

roomColliders = [topWallSprite, bottomWallSprite, vWallSprite,vWallSmallSprite2, vWallSmallSprite1, vWallSmallSprite, 
hWallDoorSprite, hWallSmallSprite1, hWallSmallSprite, vWallSprite1]

key = 'w'
characterDir = 0
playerSpeed = 1

key_pressed = False
canFire = True

layout = 1
levelType = 0
isDoorOpen = False
didCollide = False

t0 = time.ticks_ms()
t2 = time.ticks_ms()

isHurt = False
hurtCount = 0
hurtIFrames = 0
hurtTime = time.ticks_ms()

switchAnim = False
t3 = time.ticks_ms()

zsOn = False
zsList = []
zRates = [False, False, False]
zsDefaultRate = False
zsTimes0 = []

#Upgradable defaults
gunDamage = 1
fireRate = 500
bulletSpeed = 2
upgradeAttempts = 0

roomType = 0
initialRoom = False

randLoot = 0

colliderList = [topWallSprite, bottomWallSprite, vWallSprite,vWallSmallSprite2, vWallSmallSprite1, vWallSmallSprite, 
hWallDoorSprite, hWallSmallSprite1, hWallSmallSprite, vWallSprite1, chestOpenSprite, chestSprite]

deathScreen = bytearray([255,255,255,255,255,255,255,255,255,255,255,255,255,255,127,63,191,191,191,191,127,127,255,255,255,127,63,191,191,191,63,255,255,127,127,255,63,191,127,191,191,127,63,223,31,255,255,255,255,31,207,111,111,111,143,223,255,255,15,231,23,87,151,103,15,255,255,255,255,255,255,255,
           255,255,159,39,249,252,252,14,102,246,240,255,255,255,0,255,248,250,58,96,205,158,63,255,255,0,249,240,26,240,255,0,255,128,127,254,63,193,191,127,7,248,0,255,128,191,191,63,255,0,127,198,214,214,208,159,63,255,0,255,111,143,56,242,207,159,63,255,255,255,255,255,
           255,255,255,254,249,243,247,239,238,238,102,114,120,63,176,167,167,179,152,222,217,211,215,208,239,232,233,237,232,231,232,238,111,111,108,108,110,111,111,111,94,95,92,91,91,107,109,108,111,111,108,109,109,109,109,109,108,111,108,109,108,111,111,110,110,110,110,95,31,191,255,255,
           255,255,255,255,255,253,240,246,246,250,251,251,251,251,251,251,251,251,251,253,253,253,253,253,61,124,254,254,254,254,30,222,222,255,223,31,223,255,63,191,191,63,255,255,31,95,31,191,255,223,31,223,255,127,63,159,223,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,
           255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,247,247,242,248,252,255,243,246,244,241,255,255,240,255,255,240,254,254,240,255,255,240,254,248,251,255,255,248,255,255,254,254,253,253,249,255,255,255,255,255,255,255,255,255,255,255,255,255,255])
deathScreenSprite = thumby.Sprite(72, 40, deathScreen)
deathScreenSprite.x = 0
deathScreenSprite.y = 0
isInTitle = True
#title = 
#startButton = 
#background = 

#---------------------------Main Body----------------------------------------------
#
#
#---------------------------Title Screen-------------------------------------------
def Title_Screen():
    global isInTitle, deathScreenSprite
    deathScreenSprite.x = 0
    deathScreenSprite.y = 0
    thumby.display.drawSprite(deathScreenSprite)
    
    if thumby.buttonA.pressed():
        isInTitle = False

#---------------------------Controls Level Layout----------------------------------
def Level_Layout():
    
    #Spawns enemies
    Room_Spawns()
    
    #Global variables used
    global layout, levelType, isDoorOpen
    
    #Layout for if the player entered a right door.
    if layout == 1:
        mainBodySpriteF.x = 15
        
        rightBodySpriteF.x = 18
        
        leftBodySpriteF.x = 14
        
        gunSpriteF.x = 20
    
    #Layout if the player entered a left door.
    if layout == 2:
        mainBodySpriteF.x = 59
        
        rightBodySpriteF.x = 62
        leftBodySpriteF.x = 58
        gunSpriteF.x = 64
        
    #Layout if the player entered a lower door.
    if layout == 3:
        mainBodySpriteF.y = 5
        rightBodySpriteF.y = 5
        leftBodySpriteF.y = 6
        gunSpriteF.y = 8
    
    #Layout if the player entered an upper door.
    if layout == 4:
        mainBodySpriteF.y = 25
        rightBodySpriteF.y = 25
        leftBodySpriteF.y = 26
        gunSpriteF.y = 28
    
    #Layout randomizer
    layout = random.randint(1,4)
    
    #Right door room.
    if layout == 1:
        levelType = 0
        topWallSprite.x = 1
        topWallSprite.y = 1
        
        bottomWallSprite.x = 1
        bottomWallSprite.y = 36
        
        vWallSprite.x = 2
        vWallSprite.y = 1
        
        vWallSmallSprite.x = 67
        vWallSmallSprite.y = 1
        
        vWallSmallSprite1.x = 67
        vWallSmallSprite1.y =29
        
        vWallSmallSprite2.x = 66
        vWallSmallSprite2.y =10
        
    #Left door room.
    elif layout == 2:
        levelType = 0
        topWallSprite.x = 1
        topWallSprite.y = 1
        
        bottomWallSprite.x = 1
        bottomWallSprite.y = 36
        
        vWallSprite.x = 67
        vWallSprite.y = 1
        
        vWallSmallSprite.x = 2
        vWallSmallSprite.y = 1
        
        vWallSmallSprite1.x = 2
        vWallSmallSprite1.y =29
        
        vWallSmallSprite2.x = 4
        vWallSmallSprite2.y =10
    
    #Lower door room.
    elif layout == 3:
        levelType = 1
        topWallSprite.x = 1
        topWallSprite.y = 1
    
        hWallSmallSprite.x = 1
        hWallSmallSprite.y = 36
        
        hWallSmallSprite1.x = 46
        hWallSmallSprite1.y = 36
        
        hWallDoorSprite.x = 24
        hWallDoorSprite.y = 35
        
        vWallSprite.x = 67
        vWallSprite.y = 1
        
        vWallSprite1.x = 2
        vWallSprite1.y = 1
    
    #Upper door room.
    elif layout  == 4:
        levelType = 1
        topWallSprite.x = 1
        topWallSprite.y = 36
    
        hWallSmallSprite.x = 1
        hWallSmallSprite.y = 1
        
        hWallSmallSprite1.x = 46
        hWallSmallSprite1.y = 1
        
        hWallDoorSprite.x = 24
        hWallDoorSprite.y = 3
        
        vWallSprite.x = 67
        vWallSprite.y = 1
        
        vWallSprite1.x = 2
        vWallSprite1.y = 1
    
    #Moves the rest of the player's body.
    Teleport()
        
#---------------------------Draws Main Sprites-------------------------------------
def DrawSprites(direction):
    zsTime1 = time.ticks_ms()
    hurtTime1 = time.ticks_ms()
    eHurtTime1 = time.ticks_ms()
    cannonLook1 = time.ticks_ms()
    heartBeat1 = time.ticks_ms()
    lootTime1 = time.ticks_ms()
    
    #Global variables used
    global isDoorOpen,sentryHealth, isInTitle, ball, health, lootInUse, randLoot, currentLoot, gunDamage, giveLoot, fireRate, playerSpeed, roomType, chestSprite, chestOpenSprite, isChestOpen, heartChange, lootLoop,lootTime, heartLootSprite, heartLoot1Sprite, heartBeat, exitWalls2, cannonDir, eHurtTime, eHurtOcilate, cannonLook, isEHurt, eHurtCount, healthList, switchAnim, t3, enemyData, zsTimes0, zsList, zRates, zsDefaultRate, isHurt, hurtCount, hurtIFrames, hurtTime
    
    
    thumby.display.drawSprite(backgroundSprite)
    
    if isInTitle == False:
        if heartBeat1 - heartBeat > 500:
            if heartChange == False:
                heartChange = True
            elif heartChange == True:
                heartChange = False
            heartBeat = heartBeat1
        
        if heartChange == False:
            thumby.display.drawSprite(heartLoot1Sprite)
        elif heartChange == True:
            thumby.display.drawSprite(heartLootSprite)
        
        for i in enemyData:
            if enemyData[2][0] == True:
                thumby.display.drawSprite(ball)
            if i[0] == True and i[3][i[2]].y <= mainBodySpriteF.y and eHurtOcilate == False and i[2] != 6:
                if enemyData[0][0] == True:
                    thumby.display.drawSprite(i[3][i[2]])
                if enemyData[1][0] == True and sentryHealth > 10:
                    if enemyData[1][2] == 0:
                        for j in sentrySleepSprites:
                            thumby.display.drawSprite(j)
                    else:
                        for j in sentryWakeSprites:
                            thumby.display.drawSprite(j)
                if enemyData[1][0] == True and sentryHealth <= 10:
                    for j in sentryWakeSprites:
                        if j != cage1Sprite:
                            thumby.display.drawSprite(j)
                
                if enemyData[2][0] == True:
                        
                    if enemyData[2][2] == 0:
                        thumby.display.drawSprite(cannonSprites[3])
                        thumby.display.drawSprite(cannonSprites[0])
                    else:
                        if cannonLook1 - cannonLook > 600:
                            cannonLook = cannonLook1
                            if cannonDir == False:
                                cannonDir = True
                            else:
                                cannonDir = False
                            
                        if cannonDir == True:
                            thumby.display.drawSprite(cannonSprites[3])
                            thumby.display.drawSprite(cannonSprites[1])
                        else:
                            thumby.display.drawSprite(cannonSprites[3])
                            thumby.display.drawSprite(cannonSprites[2])
                            
                    
            if i[0] == True and i[2] == 6 and slimeDeathSprite.y <= mainBodySpriteF.y+2:
                thumby.display.drawSprite(slimeDeathSprite)
                if moveHeart == False:
                    heartLootSprite.x = slimeDeathSprite.x+1
                    heartLootSprite.y = slimeDeathSprite.y-9
                    
                    heartLoot1Sprite.x = heartLootSprite.x-2
                    heartLoot1Sprite.y = heartLootSprite.y-2
                
        if isHurt == False or (hurtIFrames == 2):
            #Draws the player
            if characterDir == 0:
                thumby.display.drawSprite(mainBodySpriteF)
                thumby.display.drawSprite(rightBodySpriteF)
                thumby.display.drawSprite(leftBodySpriteF)
                thumby.display.drawSprite(gunSpriteF)
            if characterDir == 1:
                thumby.display.drawSprite(mainBodySpriteB)
                thumby.display.drawSprite(rightBodySpriteB)
                thumby.display.drawSprite(leftBodySpriteB)
                thumby.display.drawSprite(gunSpriteB)
            if characterDir == 3:
                thumby.display.drawSprite(mainBodySpriteU)
            if characterDir == 2:
                thumby.display.drawSprite(mainBodySpriteD)
            
            if hurtTime1 - hurtTime > 100 and hurtIFrames == 2:
                hurtIFrames = 1
                hurtTime = hurtTime1
                hurtCount += 1
        else:
            if hurtTime1 - hurtTime > 100:
                hurtIFrames = 2
                hurtTime = hurtTime1
    
        if hurtCount > 3:
            isHurt = False
            hurtCount = 0
            hurtIFrames = 0
        #Draw Enemies
        for i in enemyData:
            if i[0] == True and i[3][i[2]].y > mainBodySpriteF.y and eHurtOcilate == False and i[2] != 6:
                if enemyData[0][0] == True:
                    thumby.display.drawSprite(i[3][i[2]])
                if enemyData[1][0] == True and sentryHealth > 10:
                    if enemyData[1][2] == 0:
                        for j in sentrySleepSprites:
                            thumby.display.drawSprite(j)
                    else:
                        for j in sentryWakeSprites:
                            thumby.display.drawSprite(j)
                            
                if enemyData[1][0] == True and sentryHealth <= 10:
                    for j in sentryWakeSprites:
                        if j != cage1Sprite:
                            thumby.display.drawSprite(j)
                
                if enemyData[2][0] == True:
                    if enemyData[2][2] == 0:
                        thumby.display.drawSprite(cannonSprites[3])
                        thumby.display.drawSprite(cannonSprites[0])
                    else:
                        if cannonLook1 - cannonLook > 600:
                            cannonLook = cannonLook1
                            if cannonDir == False:
                                cannonDir = True
                            else:
                                cannonDir = False
                            
                        if cannonDir == True:
                            thumby.display.drawSprite(cannonSprites[3])
                            thumby.display.drawSprite(cannonSprites[1])
                        else:
                            thumby.display.drawSprite(cannonSprites[3])
                            thumby.display.drawSprite(cannonSprites[2])
                
            if i[0] == True and i[2] == 6 and slimeDeathSprite.y > mainBodySpriteF.y+2:
                thumby.display.drawSprite(slimeDeathSprite)
                
                if moveHeart == False:
                    heartLootSprite.x = slimeDeathSprite.x+1
                    heartLootSprite.y = slimeDeathSprite.y-9
                    
                    heartLoot1Sprite.x = heartLootSprite.x-2
                    heartLoot1Sprite.y = heartLootSprite.y-2
        #Draws bullets.
        for i in bulletsList:
            if i[0] != nullSprite:
                thumby.display.drawSprite(i[0])
    
        #Draws room doors
        if levelType == 0:
            for i in exitWalls:
                thumby.display.drawSprite(i)
            exitWalls2[0].x = 100
        else:
            for i in exitWalls1:
                thumby.display.drawSprite(i)
            exitWalls2[1].x = 100
            
        if isDoorOpen == False:
            if levelType == 1:
                thumby.display.drawSprite(exitWalls2[0])
            else:
                thumby.display.drawSprite(exitWalls2[1])
    
        if zsOn == True:
            if zsDefaultRate == False:
                zsDefaultRate = True
                zsTimes0 = [time.ticks_ms(), time.ticks_ms(), time.ticks_ms()]
            if zsTime1 - zsTimes0[0] > 1000 and zRates[0] == False:
    
                thumby.display.drawSprite(zsList[0])
                thumby.display.drawSprite(zsList[1])
                thumby.display.drawSprite(zsList[2])
                thumby.display.drawSprite(zsList[3])
                thumby.display.drawSprite(zsList[4])
                
            if zsTime1 - zsTimes0[1] > 2000 and zRates[1] == False:
                zRates[0] = True
                thumby.display.drawSprite(zsList[5])
                thumby.display.drawSprite(zsList[6])
                thumby.display.drawSprite(zsList[7])
                thumby.display.drawSprite(zsList[8])
                thumby.display.drawSprite(zsList[9])
                    
            if zsTime1 - zsTimes0[2] > 3000 and zRates[2] == False:
                zRates[1] = True
                thumby.display.drawSprite(zsList[10])
                thumby.display.drawSprite(zsList[11])
                thumby.display.drawSprite(zsList[12])
                thumby.display.drawSprite(zsList[13])
                thumby.display.drawSprite(zsList[14])
            if  zsTime1 - zsTimes0[2] > 4000 and zRates[2] == False:
                zsTimes0[0] = zsTime1
                zsTimes0[1] = zsTime1
                zsTimes0[2] = zsTime1
    
                zRates[2] = False
                zRates[1] = False
                zRates[0] = False
    
        if eHurtTime1 - eHurtTime > 100 and eHurtCount < 4 and isEHurt == True:
            eHurtCount += 1
            eHurtTime = eHurtTime1
            eHurtOcilate = not eHurtOcilate
    
        if eHurtCount > 3:
            eHurtCount = 0
            eHurtOcilate = False
            isEHurt = False
                
        #Draws the UI
        thumby.display.drawSprite(healthList[0])
        if health > 0:
            thumby.display.drawSprite(healthList[health])
        
        if lootTime1 - lootTime > 500:
            lootTime = lootTime1
            if lootLoop == False:
                lootLoop = True
            else:
                lootLoop = False
        randLoot = random.randint(1, 5)
        if roomType == 1 and isChestOpen == False:
            thumby.display.drawSprite(chestSprite)
        if isChestOpen == True:
            thumby.display.drawSprite(chestOpenSprite)
            chestOpenSprite.x = chestSprite.x
            chestOpenSprite.y = chestSprite.y-3
            if giveLoot == False:
                giveLoot = True
                if randLoot == 1:
                    print("Speed")
                    if lootInUse[0] == 0:
                        lootInUse[0] = 1
                        playerSpeed *= 1.5
                        currentLoot = 1
                if randLoot == 2:
                    print("Damage")
                    if lootInUse[1] == 0:
                        lootInUse[1] = 1
                        gunDamage *= 2
                        currentLoot = 3
                if randLoot == 3:
                    print("Bullet")
                    if lootInUse[2] == 0:
                        lootInUse[2] = 1
                        fireRate /= 2
                        currentLoot = 2
                if randLoot == 4:
                    print("Health")
                    health = 3
                    currentLoot = 4
                    
            for i in lootSprites:
                if i != lootBackgroundSprite:
                    i.x = 12
                    i.y = 0
                else:
                    i.x = 11
                    i.y = -1
            
            thumby.display.drawSprite(lootBackgroundSprite)
            if currentLoot == 1:
                thumby.display.drawSprite(lootSprites[0])
            elif currentLoot == 2:
                thumby.display.drawSprite(lootSprites[1])
            elif currentLoot == 3:
                thumby.display.drawSprite(lootSprites[2])
            else:
                thumby.display.drawSprite(lootSprites[3])

    else:
        Title_Screen()
    #Updates screen.
    thumby.display.update()

#---------------------------Enemy Spawns-------------------------------------------

def Room_Spawns():
    global enemyData, initialize, currentLoot, giveLoot, lootSprites, isChestOpen, slimeHealth, moveHeart, lootSprites, chestOpenSprite, chestSprite, isChestOpen, roomType, initialRoom, giveLoot
    
    roomType = random.randint(1,3)
    moveHeart = False
    for i in lootSprites:
            i.x = 100
    chestSprite.x = 100
    chestOpenSprite.x = 100
    giveLoot = False
    isChestOpen = False
    currentLoot = 0
    for i in heartSprites:
        i.x += 100
        i.y += 100
    if initialRoom == True:
        if roomType == 1:
            isChestOpen = False
            print("Loot room")
            for i in enemyData:
                i[0] = False
            
            chestSprite.x = 32
            chestSprite.y = 18
            
        else:
            print("enemy room")
            for i in enemyData:
                i[0] = False
            
            initialize = True
            slimeHealth = 10
            enemyType = random.randint(0, len(enemyData) - 1)  # Choose a random enemy type
            enemyData[enemyType][0] = True
    else:
        initialRoom = True

#---------------------------Player Resets------------------------------------------
def Reset():
    global health, enemyList, reset, isInTitle
    health = 3
    enemyList = []
    reset = False
    isInTitle = True
    mainBodySpriteF.x = 34
    mainBodySpriteF.y = 19
    
    rightBodySpriteF.x = 37
    rightBodySpriteF.y = 19
    
    leftBodySpriteF.x = 33
    leftBodySpriteF.y = 20
    
    gunSpriteF.x = 39
    gunSpriteF.y = 22
    
    Teleport()
    
    print("Loot room")
    for i in enemyData:
        i[0] = False

#---------------------------Player Sprite Teleportation----------------------------
#Changes the child sprites for the player to match the player's position.
def Teleport():
    mainBodySpriteB.x = mainBodySpriteF.x+1
    mainBodySpriteB.y = mainBodySpriteF.y
    
    leftBodySpriteB.x = mainBodySpriteB.x-2
    leftBodySpriteB.y = mainBodySpriteB.y
    
    rightBodySpriteB.x = mainBodySpriteB.x+3
    rightBodySpriteB.y = mainBodySpriteB.y+1
    
    gunSpriteB.x = mainBodySpriteB.x-4
    gunSpriteB.y = mainBodySpriteB.y+3
    
    mainBodySpriteU.x = mainBodySpriteF.x-1
    mainBodySpriteU.y = mainBodySpriteF.y
    mainBodySpriteD.x = mainBodySpriteU.x
    mainBodySpriteD.y = mainBodySpriteU.y

#---------------------------Boss AI------------------------------------------------

def Cannon_Boss():
    global cannonSprites, ballSprites, cannonHealth, ballBoomTime, ballPhase, ball, cannonBallTime, ballSpeed, mainBodySpriteF, zsList, initialize, wiggleTimes, canWiggle, wiggleDir, isSleep, zsOn, awake, wakeyCounter, enemyData, wakeyTime, shootTime, bounce, shootCounter
    
    if initialize == True:
        zsList = []
        initialize = False
        cannonHealth = 20
        isSleep = True
        zsOn = False
        awake = False
        wakeyCounter = 0
        enemyData[2][2] = 0
        shootCounter = 0
        bounce = False
        canWiggle = False
        wiggleDir = False
        wiggleTimes = 0
        ball.x = 100
        ball.y = 100
        cannonBallLifeTime = time.ticks_ms()
    
    wakeyTime1 = time.ticks_ms()
    shootTime1 = time.ticks_ms()
    wiggleTime1 = time.ticks_ms()
    ballBoomTime1 = time.ticks_ms()
    
    
    isAwake = False
    

    if enemyData[2][2] == 0 and zsOn == False and isSleep == True:
        zsOn = True
        Zs(cannonSleep1Sprite.x+3, cannonSleep1Sprite.y)
        Zs(cannonSleep1Sprite.x+6, cannonSleep1Sprite.y-3)
        Zs(cannonSleep1Sprite.x+10, cannonSleep1Sprite.y-4)
    
    if (enemyData[2][2] == 1 or enemyData[2][2] == 0) and wakeyTime1 - wakeyTime > 500 and isSleep == False and awake == False:
        if enemyData[2][2] == 0:
            enemyData[2][2] = 1
            wakeyCounter+=1
            if wakeyCounter >= 3:
                awake = True
        else:
            enemyData[2][2] = 0
        wakeyTime = wakeyTime1
        
    if awake == True and enemyData[2][2] != 6:
        if shootTime1 - shootTime > 500:
            if bounce == False:
                cannonSprites[1].y += 1
                cannonSprites[2].y += 1
                bounce = True
            else:
                shootCounter+=1
                cannonSprites[1].y -= 1
                cannonSprites[2].y -= 1
                bounce = False
            
            shootTime = shootTime1
        
        
        if shootCounter > 3:

            if ballBoomTime1 - ballBoomTime > 100:
                x1 = ball.x
                y1 = ball.y
                ball = ballSprites[ballPhase]
                ballPhase += 1
                ball.x = x1
                ball.y = y1
                
                ballBoomTime = ballBoomTime1
            
            if ballPhase >= 8:
                ballPhase = 0
            
                ball.x = cannonSprites[0].x
                ball.y = cannonSprites[0].y-7
            
                ballPhase = 0
                shootCounter = 0
                canWiggle = True
        
        if canWiggle == True and wiggleTime1 - wiggleTime > 100:
            if wiggleTimes < 10:
                if wiggleDir == False:
                    wiggleDir = True
                    wiggleTimes += 1
                    for i in cannonSprites:
                        i.x -= 1
                else:
                    wiggleDir = False
                    wiggleTimes += 1
                    for i in cannonSprites:
                        i.x += 1
                            
            else:
                wiggleTimes = 0
                canWiggle = False
        
        cannonBallTime1 = time.ticks_ms()
    
        if cannonBallTime1 - cannonBallTime > 500:
            cannonBallTime = cannonBallTime1
            
            x1 = ball.x
            y1 = ball.y
            
            if ballPhase == 0:
                ballPhase = 1
                ball = ballSprites[ballPhase]
                ball.x = x1
                ball.y = y1
            elif ballPhase == 1:
                ballPhase = 0
                ball = ballSprites[ballPhase]
                ball.x = x1
                ball.y = y1
                    
        if ballPhase == 0 or ballPhase == 1:
            if ball.x > mainBodySpriteF.x:
                ball.x -= ballSpeed
            else:
                ball.x += ballSpeed
                
            if ball.y > mainBodySpriteF.y:
                ball.y -= ballSpeed
            else:
                ball.y += ballSpeed
            
        

def Sentry_Boss():
    global sentrySprites, sentryHealth, isSleep, possibleDir, zsList, zsOn, enemyData,direction, wakeyTime, wakeyCounter, awake, initialize, isAwake, mainBodySpriteF, sentrySpeed, chargeTime
    
    if initialize == True:
        zsList = []
        initialize = False
        sentryHealth = 20
        isSleep = True
        zsOn = False
        awake = False
        wakeyCounter = 0
        enemyData[1][2] = 0
        sentrySleep1Sprite.x = 32
        sentrySleep1Sprite.y = 15
    
        sentrySleep2Sprite.x = sentrySleep1Sprite.x
        sentrySleep2Sprite.y = sentrySleep1Sprite.y
        
        cage1Sprite.x = sentrySleep1Sprite.x-2
        cage1Sprite.y = sentrySleep1Sprite.y-2
        
        cage2Sprite.x = cage1Sprite.x
        cage2Sprite.y = cage1Sprite.y
        
        sGun1Sprite.x = cage1Sprite.x-1
        sGun1Sprite.y = cage1Sprite.y-1
        
        sGun2Sprite.x = cage1Sprite.x-1
        sGun2Sprite.y = cage1Sprite.y+5
        
        sGun3Sprite.x = cage1Sprite.x-1
        sGun3Sprite.y = cage1Sprite.y+11
        
        sGun4Sprite.x = cage1Sprite.x+5
        sGun4Sprite.y = cage1Sprite.y-1
        
        sGun5Sprite.x = cage1Sprite.x+11
        sGun5Sprite.y = cage1Sprite.y-1
        
        sGun6Sprite.x = cage1Sprite.x+5
        sGun6Sprite.y = cage1Sprite.y+11
        
        sGun7Sprite.x = cage1Sprite.x+11
        sGun7Sprite.y = cage1Sprite.y+5
        
        sGun8Sprite.x = cage1Sprite.x+11
        sGun8Sprite.y = cage1Sprite.y+11
        
    chargeTime1 = time.ticks_ms()
    wakeyTime1 = time.ticks_ms()
    
    isAwake = False

    if enemyData[1][2] == 0 and zsOn == False and isSleep == True:
        zsOn = True
        Zs(cage1Sprite.x+3, cage1Sprite.y)
        Zs(cage1Sprite.x+6, cage1Sprite.y-3)
        Zs(cage1Sprite.x+10, cage1Sprite.y-4)
    
    if (enemyData[1][2] == 1 or enemyData[1][2] == 0) and wakeyTime1 - wakeyTime > 500 and isSleep == False and awake == False:
        if enemyData[1][2] == 0:
            enemyData[1][2] = 1
            wakeyCounter+=1
            if wakeyCounter >= 3:
                awake = True
        else:
            enemyData[1][2] = 0
        wakeyTime = wakeyTime1
        
    if awake == True and enemyData[1][2] != 6:
        enemyData[1][2] = 1
        
        if chargeTime1 - chargeTime > 2000:
            chargeTime = chargeTime1
            
            possibleDir = []

            if mainBodySpriteF.x > sentrySprites[0].x:
                possibleDir.append(0)
            else:
                possibleDir.append(1)

            if mainBodySpriteF.y > sentrySprites[0].y:
                possibleDir.append(2)
            else:
                possibleDir.append(3)
                
            randDir = random.randint(0,1)
            if randDir == 0:
                direction = possibleDir[0]
            else:
                direction = possibleDir[1]
        
        for i in sentrySprites:
            if direction == 0 and sentrySleep1Sprite.x < mainBodySpriteF.x:
                i.x += sentrySpeed
            if direction == 1 and sentrySleep1Sprite.x > mainBodySpriteF.x:
                i.x -= sentrySpeed
            if direction == 2 and sentrySleep1Sprite.y < mainBodySpriteF.y:
                i.y += sentrySpeed
            if direction == 3 and sentrySleep1Sprite.y > mainBodySpriteF.y:
                i.y -= sentrySpeed


def Slime_Boss():
    global slimeBoss3Sprite, initialize, slimeBoss2Sprite, slimeHealth, zsList,slimeBoss1Sprite, awake, slimeSpeed, cycleReset, jumpTime, changeDirTime, targetPos, wakeyCounter, isSleep, slimeBossSprite, slimeSleepSprite, slimeWakeSprite, enemyData, zsOn, wakeyTime, slimeStates
    
    if initialize == True:
        zsList = []
        initialize = False
        slimeHealth = 10
        enemyData[0][2] = 0
        isSleep = True
        zsOn = False
        awake = False
        wakeyCounter = 0
        cycleReset = False
        for i in slimeStates:
            i.x = slimeStates[0].x
            i.y = slimeStates[0].y
    wakeyTime1 = time.ticks_ms()
    jumpTime1 = time.ticks_ms()
    changeDirTime1 = time.ticks_ms()
    
    isAwake = False

    if enemyData[0][2] == 0 and zsOn == False and isSleep == True:
        zsOn = True
        Zs(slimeSleepSprite.x, slimeSleepSprite.y)
        Zs(slimeSleepSprite.x+3, slimeSleepSprite.y-3)
        Zs(slimeSleepSprite.x+7, slimeSleepSprite.y-4)
        
    if (enemyData[0][2] == 1 or enemyData[0][2] == 0) and wakeyTime1 - wakeyTime > 500 and isSleep == False:
        if enemyData[0][2] == 0:
            enemyData[0][2] = 1
            wakeyCounter+=1
            if wakeyCounter >= 3:
                enemyData[0][2] = 5
        else:
            enemyData[0][2] = 0
        wakeyTime = wakeyTime1
    
    if enemyData[0][2] > 1 and jumpTime1 - jumpTime > 100 and cycleReset == False and enemyData[0][2] != 6:
        jumpTime = jumpTime1
        isAwake = True
        
        if enemyData[0][2] > 2:
            enemyData[0][2] -= 1
            
            slimeStates[2].y -= 3
            slimeStates[3].y -= 3
            slimeStates[4].y -= 3
            slimeStates[5].y -= 3
            slimeStates[6].y -= 2
        else:
            cycleReset = True
    if cycleReset == True and jumpTime1 - jumpTime > 100  and enemyData[0][2] != 6:
        jumpTime = jumpTime1
        isAwake = True
        awake = True
        
        if enemyData[0][2] < 5:
            enemyData[0][2] += 1

            
            slimeStates[2].y += 3
            slimeStates[3].y += 3
            slimeStates[4].y += 3
            slimeStates[5].y += 3
            slimeStates[6].y += 2
        else:
            cycleReset = False
    
    if isAwake and enemyData[0][2] != 6:
        if changeDirTime1 - changeDirTime > 1000:
            changeDirTime = changeDirTime1
            targetPos = [random.randint(10,60), random.randint(10,30)]
        
        if targetPos[0]- slimeStates[2].x > 0:
            slimeSpeed = abs(slimeSpeed)
        else:
            slimeSpeed = abs(slimeSpeed)
            slimeSpeed *= -1
            
        slimeStates[2].x += slimeSpeed
        slimeStates[3].x += slimeSpeed
        slimeStates[4].x += slimeSpeed
        slimeStates[5].x += slimeSpeed
        slimeStates[6].x += slimeSpeed
        
        if targetPos[1]- slimeStates[2].y > 0:
            slimeSpeed = abs(slimeSpeed)
        else:
            slimeSpeed = abs(slimeSpeed)
            slimeSpeed *= -1
            
        slimeStates[2].y += slimeSpeed
        slimeStates[3].y += slimeSpeed
        slimeStates[4].y += slimeSpeed
        slimeStates[5].y += slimeSpeed
        slimeStates[6].y += slimeSpeed

        
initialize = True    
awake = False
wakeyCounter = 0
isSleep = True
cycleReset = False
targetPos = [0,0]
slimeSpeed = 2
slimeHealth = 10
isEHurt =False
eHurtCount = 0
eHurtOcilate = False

#Sentry Variables
sentryHealth = 20
chargeTime = time.ticks_ms()
sentrySpeed = 3
direction = 0
possibleDir = []

cannonLook = time.ticks_ms()
shootTime = time.ticks_ms()
wiggleTime = time.ticks_ms()
cannonBallTime = time.ticks_ms()
ballBoomTime = time.ticks_ms()
cannonHealth = 20
ballPhase = 0
cannonDir = False
bounce = False
shootCounter = 0
canWiggle = False
wiggleDir = False
wiggleTimes = 0
ballSpeed = .2

wakeyTime = time.ticks_ms()
jumpTime = time.ticks_ms()
changeDirTime = time.ticks_ms()
eHurtTime = time.ticks_ms()

activateSlime = False
activateSentry = False
activateCannon = False
enemyData = [[activateSlime, Slime_Boss, 0, slimeStates], [activateSentry, Sentry_Boss, 0, sentrySprites], [activateCannon, Cannon_Boss, 0, cannonSprites]]

#Initializes Enemies.
Room_Spawns()

def Zs(x, y):
    global z1Sprite, z2Sprite

    z1S = thumby.Sprite(3, 1, z1)
    z1S.x = x+8
    z1S.y = y-1
        
    z1S1 = thumby.Sprite(3, 1, z1)
    z1S1.x = z1S.x
    z1S1.y = z1S.y-4
        
    z2S = thumby.Sprite(1, 1, z2)
    z2S.y = z1S.y-1
    z2S.x = z1S.x
        
    z2S1 = thumby.Sprite(1, 1, z2)
    z2S1.y = z1S.y-2
    z2S1.x = z1S.x+1

    z2S2 = thumby.Sprite(1, 1, z2)
    z2S2.y = z1S.y-3
    z2S2.x = z1S.x+2
        
    zsList.append(z1S)
    zsList.append(z1S1)
    zsList.append(z2S)
    zsList.append(z2S1)
    zsList.append(z2S2)

        
#---------------------------Main Game Loop-----------------------------------------
while(1):
    if health < 1 and reset == False:
        reset = True
        Reset()
        
    isDoorOpen = True
    for i in enemyData:
        if i[0] == True and i[2] != 6:
            isDoorOpen = False
        
    t1 = time.ticks_ms()
    tHealth = time.ticks_ms()
    
    #Clears null bullets.
    for i in range(len(bulletsList)-1):
        if bulletsList[i][0] == nullSprite:
            del bulletsList[i]
                
    #----------------------------------------------
    '''
    Change to make it so that when the player interacts with an object there are only limited keys that can go through
    lik when hitting top of box you can only move up, left, right
    '''
        
    playerPosDir = []
    
        
    if thumby.buttonR.pressed():
            
        if "R" not in playerPosDir:
            characterDir = 0
            for x in playerColliderListAll:
                x.x += playerSpeed
            gunSpriteB.x += playerSpeed
            gunSpriteF.x += playerSpeed
                
    if thumby.buttonL.pressed():
        if "L" not in playerPosDir:
            characterDir = 1
            for x in playerColliderListAll:
                x.x -= playerSpeed
            gunSpriteB.x -= playerSpeed
            gunSpriteF.x -= playerSpeed
                
    if thumby.buttonD.pressed():
        if "D" not in playerPosDir:
            characterDir = 2
            for x in playerColliderListAll:
                x.y += playerSpeed
            gunSpriteB.y += playerSpeed
            gunSpriteF.y += playerSpeed
                
    if thumby.buttonU.pressed():
        if "U" not in playerPosDir:
            characterDir = 3
            for x in playerColliderListAll:
                x.y -= playerSpeed
            gunSpriteB.y -= playerSpeed
            gunSpriteF.y -= playerSpeed     
                    
    for i in colliderList:
        for j in playerColliderListAll:
            if i.x < j.x + j.width and i.x + i.width > j.x and i.y < j.y + j.height and i.y + i.height > j.y:
                if thumby.buttonL.pressed() and "L" not in playerPosDir:
                    playerPosDir.append("L")
                    characterDir = 0
                    for x in playerColliderListAll:
                        x.x += playerSpeed
                    gunSpriteB.x += playerSpeed
                    gunSpriteF.x += playerSpeed
                            
                if thumby.buttonR.pressed() and "R" not in playerPosDir:
                    playerPosDir.append("R")
                    characterDir = 1
                    for x in playerColliderListAll:
                        x.x -= playerSpeed
                    gunSpriteB.x -= playerSpeed
                    gunSpriteF.x -= playerSpeed
                            
                if thumby.buttonU.pressed() and "U" not in playerPosDir:
                    playerPosDir.append("U")
                    characterDir = 2
                    for x in playerColliderListAll:
                        x.y += playerSpeed
                    gunSpriteB.y += playerSpeed
                    gunSpriteF.y += playerSpeed
                            
                if thumby.buttonD.pressed() and "D" not in playerPosDir:
                    playerPosDir.append("D")
                    characterDir = 3
                    for x in playerColliderListAll:
                        x.y -= playerSpeed
                    gunSpriteB.y -= playerSpeed
                    gunSpriteF.y -= playerSpeed
                if (i == vWallSmallSprite2 or i == hWallDoorSprite) and isDoorOpen:
                    isDoorOpen = False
                    Level_Layout()
           
    #Bullet creation.
    if thumby.buttonA.pressed() and t1-t0 > fireRate:
        t0 = t1
        bulletActive = True
        if characterDir == 0:
            bulletXSprite = thumby.Sprite(2,1,bulletX)
            bulletXSprite.x = gunSpriteF.x
            bulletXSprite.y = gunSpriteF.y
                    
            bulletsList.append([bulletXSprite, 0])
                                        
        elif characterDir == 1:
            bulletXSprite = thumby.Sprite(2,1,bulletX)
            bulletXSprite.x = gunSpriteB.x
            bulletXSprite.y = gunSpriteB.y
                
            bulletsList.append([bulletXSprite, 1])
                    
        elif characterDir == 2:
            bulletYSprite = thumby.Sprite(1,2,bulletY)
            bulletYSprite.x = mainBodySpriteD.x+6
            bulletYSprite.y = mainBodySpriteD.y+5
                        
            bulletsList.append([bulletYSprite, 2])
                                    
        elif characterDir == 3:
            bulletYSprite = thumby.Sprite(1,2,bulletY)
            bulletYSprite.x = mainBodySpriteU.x+6
            bulletYSprite.y = mainBodySpriteU.y+4
                
            bulletsList.append([bulletYSprite, 3])
                
    #Controls bullet movement.      
    if bulletActive == True and canFire == True:
                
        for i in bulletsList:
            if i[0] != nullSprite:
                if i[1] == 0:
                    i[0].x += bulletSpeed
                if i[1] == 1:
                    i[0].x -= bulletSpeed
                if i[1] == 2:
                    i[0].y += bulletSpeed
                if i[1] == 3:
                    i[0].y -= bulletSpeed
                        
    #Enemy AI calling.
    for i in enemyData:
        if i[0] == True:
            i[1]()
        
    #Collision detection loops.   
    for i in colliderList:
            
        for j in bulletsList:
            if i.x < j[0].x + j[0].width and i.x + i.width > j[0].x and i.y < j[0].y + j[0].height and i.y + i.height > j[0].y:
                bulletsList.remove(j)
                if i == chestSprite:
                    isChestOpen = True
                    
    for i in heartSprites:
        for j in playerColliderListAll:
            if i.x < j.x + j.width and i.x + i.width > j.x and i.y < j.y + j.height and i.y + i.height > j.y and tHealth-t2 >= 2000: 
                moveHeart = True
                heartSprites[0].x = 100
                heartSprites[1].x = 100
                if health < 3:
                    health+=1
                    
                  
    #Enemy Death
    for i in enemyData:  # Iterate through a copy of enemyList
        for j in bulletsList:
            if i[3][i[2]].x < j[0].x + j[0].width and i[3][i[2]].x + i[3][i[2]].width > j[0].x and i[3][i[2]].y < j[0].y + j[0].height and i[3][i[2]].y + i[3][i[2]].height > j[0].y and i[0] == True:
                if i[0] == True:
                    if i[2] == 0:
                        zsOn = False
                        isSleep = False
                    if awake == True:
                        if enemyData[0][0] == True:
                            slimeHealth -= gunDamage
                            if slimeHealth <= 0:
                                i[2] = 6
                        if enemyData[1][0] == True:
                            sentryHealth -= gunDamage
                            if sentryHealth <= 0:
                                i[2] = 6
                                slimeDeathSprite.x = cage1Sprite.x+3
                                slimeDeathSprite.y = cage1Sprite.y+7
                                    
                        if enemyData[2][0] == True:
                            cannonHealth -= gunDamage
                            if cannonHealth <= 0:
                                i[2] = 6
                                slimeDeathSprite.x = cannonSprites[0].x
                                slimeDeathSprite.y = cannonSprites[0].y+5
                                ball.x = 100
                                ball.y = 100
                                
                        isEHurt = True
                        eHurtCount = 0
                        eHurtOcilate = True
                            
                    bulletsList.remove(j)
            
        for j in playerColliderListAll:
            if i[3][i[2]].x < j.x + j.width and i[3][i[2]].x + i[3][i[2]].width > j.x and i[3][i[2]].y < j.y + j.height and i[3][i[2]].y + i[3][i[2]].height > j.y and tHealth-t2 >= 2000: 
                if i[0] == True and i[2] != 0 and i[2] != 6:
                    health -= 1
                    isHurt = True
                    hurtIFrames = 2
                    t2 = tHealth
            if ball.x < j.x + j.width and ball.x + ball.width > j.x and ball.y < j.y + j.height and ball.y + ball.height > j.y and tHealth-t2 >= 2000 and i == enemyData[2]: 
                if i[0] == True and i[2] != 0 and i[2] != 6:
                    health -= 1
                    isHurt = True
                    hurtIFrames = 2
                    t2 = tHealth        
    
    DrawSprites(key)
