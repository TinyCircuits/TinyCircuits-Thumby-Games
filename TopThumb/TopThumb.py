#Top Thumb, created by Wandyez 2022
#Title Sprite Artwork by AyreGuitar
#The objective of this game is to create a 'Afterburner' style game. This game consists of 3 main components:
#Component 1: The Horizon - The Horizon is a line drawn on the edges of the screen, and repeated to create
#and alternated to create a movement 'animation', the horizon is shifted with D pad input to create
#the impression of going left and right, up and down
#Component 2: The Jet - The Jet represents the player, the jet moves slightly on the center of the screen
#to create the impression of movement. The Jet switches sprites as well. The jet also has a 'real' coordinate
#plane to help dodge obstacles so that no collision actually occurs
#Component 3: The enemies
#the enemies exist on the 'real' coordinate plane, and are spawned in accordingly
#this is done using an object renderer that renders all objects in a list
#objects are added to the object renderer through the level list
#the enemies sprite changes in size as they get closer
#
#NOTE: This runs much much slower on the emulator.

#Import stuff you need
import thumby
import random
import time

#This is the Font, the file path is specified. 
thumby.display.setFont("/lib/font5x7.bin", 5, 7, 1)
currentScore = 0
ScoreModifier = 0.05 #since everything is based on framerate, so too should be score. 
thumby.saveData.setName("HighScore")
highScoreLocal = 0
#Define constants:
thumby.display.setFPS(60) #Keep the FPS set to 100 so any counters tied to FPS are equivallent roughly to 10 miliseconds.


Initizalization = True
while(Initizalization == True):
    #if I stuff everything into an initialization I can go back to it (big brain move)
    #Define variables
    
    #Horizon variables: These variables represent where the default horizon is
    #and exist to generate scrolling generated lines between Y1 and Y2 down to the bottom border
    #remember, thumby is only 72 x 40, and confusingly counts from the top down y = 0 -> top of the screen
    HorizonY1 = thumby.display.height - 20 
    HorizonY2 = thumby.display.height - 10
    HorizonMaxCorrection = 19 #adjust this number to set the top of the Horizon
    HorizonMax = thumby.display.height - HorizonMaxCorrection #Horizon max represents the maximum height
    HorizonMin = thumby.display.height - 1
    HorizonMiddle = int(thumby.display.height - (HorizonMaxCorrection/2))
    
    Vertspeed = 2 #speed at which Horizon is adjusted vertically
    Sidespeed = 2 #speed at which Horizon is adjusted horizontally
    CorrectionSpeed = 1
    
    #Alternation for animation of Horizon
    Alternation = 0
    AlternationMax = 3
    

    
    #Draw the horizon:
    thumby.display.fill(0) #clear the screen so objects can be printed
    
    #Define The Sprites
    
    #JetVariables
    #Jet Screen variables determine the position of the Jet on the screen. The jet must mildly move
    #to give the illusion of fluid movement. 
    JetXBound = 8 #this is the amount the jet is allowed to move while wiggling around in either direction
    JetYBound = 3 
    JetYAdjustment = 5 #Vertical adjustment for where the jet ought to be based on sprite size, and also wherever I feel like it
    JetXAdjustment = 5 #Horizontal adjustment for where the jet ought to be based on sprite size ONLY. 
    JetXSpriteSize = 10 #The sprite size is necessary for confusing centering calculations. 
    JetYSpriteSize = 4
    JetMaxX = int(thumby.display.width/2) + JetXBound -JetXAdjustment #The jet is centered horizontally
    JetMinX = int(thumby.display.width/2) - JetXBound -JetXAdjustment #adjust the jet placement for width of the jet
    JetMiddleX = int(thumby.display.width/2) - JetXAdjustment
    
    JetMaxY = int(thumby.display.height/2) - JetYBound - JetYAdjustment - 2 #The jet is NOT centered vertically, it is offset
    JetMinY = int(thumby.display.height/2) + JetYBound + JetYAdjustment +2
    JetMiddleY = int(thumby.display.height/2) + JetYAdjustment
    
    JetX = (thumby.display.width/2)
    JetY = (thumby.display.height/2) + JetYAdjustment
    
    #Mess with the jet speeds here!
    JetVertSpeed = 3
    JetSideSpeed = 3
    JetCorrectionSpeed = 1
    JetTimer = time.ticks_ms() #This timer represents when to flash the animation
    
    #The "Real" coordinate plane represents where the Jet really is, this is used to determine impact
    #Due to 
    JetRealXBound = 10 #this represents the amount in either direction the jet can fly
    JetRealXBoundOffset = 2*JetRealXBound #this number is necessary for calculations between the real and screen coordinate planes.
    
    JetRealX = int((int(thumby.display.width) + (JetRealXBound*2))/2   - JetXSpriteSize/2)
    JetRealY = 20
    JetRealZ = -20 #The plane is at 0, but should it be? we can render objects passing the player. 

    JetRealXMax = int(thumby.display.width) + (JetRealXBound*2) 
    JetRealXMin = 0
    JetRealXMiddle = int((int(thumby.display.width) + (JetRealXBound*2))/2   - JetXSpriteSize/2) #since the bounds take place off screen equally, it can be left the same. 
    JetRealYMax = JetMaxY #The Y coordinate is unchanged, since this would lead to confusing rendering. 
    JetRealYMin = JetMinY
    JetRealYMiddle = JetMiddleY
    JetRealVertSpeed = JetVertSpeed #This number should remain the same since Y isn't changing very much. 
    JetRealSideSpeed = JetSideSpeed #keepiing this the same keeps everything the same.  
    #JetRealCorrectionSpeed = 1
    
    #JET SPRITES
    #-0-0-0-00-0-0-0-0-0
    #These sprites are 10x4
    #Jet Center Maps
    # BITMAP: width: 10, height: 4
    JetDefaultMap = bytearray([4,4,5,10,15,15,10,5,4,4])# BITMAP: width: 10, height: 4
    JetDefaultMapEngineOn = bytearray([4,4,1,4,11,11,4,1,4,4])
    #Jet Left Map
    JetLeftMap01 = bytearray([4,5,7,14,15,15,14,5,4,4]) 
    JetLeftMap02= bytearray([4,5,7,10,15,15,10,5,4,4])
    JetLeftMap = JetLeftMap01 + JetLeftMap02
    
    #Jet Right Map
    # BITMAP: width: 10, height: 4
    JetRightMap01 = bytearray([4,4,5,10,15,15,10,7,5,4])
    JetRightMap02 = bytearray([4,4,5,14,15,15,14,7,5,4])
    JetRightMap = JetRightMap01 + JetRightMap02
    # BITMAP: width: 10, height: 4

    JetCenterMap = JetDefaultMap+JetDefaultMapEngineOn
    JetSpriteMapToUse = JetCenterMap
    JetSpriteCurrentFrame = 0
    JetSpriteFrameCounter = 0 ##There is a built in counter tied to frame rate, this determines how frequently the sprite will change. 
    JetSpriteFrameCounterSpacing = 2 #CHANGE THIS NUMBER TO MAKE THE JET SPRITES CHANGE BETTER

    
    
    #EnemyVariables
    UniqueIdentifier = 0 #The unique identifier 
    
    #The master objectlist
    #=-=-=-=-=-=-=-=-=-=-=-=--=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=
    #[ [[realX, realY,realZ], [Width, Height], [VectorX, VectorY,VectorZ], [Velocity, Acceleration], [[rangestart,rangeend,graphictopull]],{Sprite Dictionary}],[derendering distance min, derendering distance max, UniqueIdentifier, EnemyTypeInt]
    #A sprite dictionary must exist as {"Spritename": [[Bytemap list], Width, Height,counters between frames, current counter, currentFrame]
    
    MasterObjectList = []
    
    #Sun Object
    SunByteMap01 = bytearray([24,66,24,189,189,24,66,24])
    SunByteMap02 = bytearray([56,0,25,189,189,152,0,28])
    SunByteMap = SunByteMap01 + SunByteMap02
    #keep dictionary names short (1 letter), each additoinal check slows down the game
    SunSpriteDictionary = { "S": [[SunByteMap],8,8,9,0,0]}
    ObjectSun = [[-10,8, -5], [1,1], [0,0,0], [0,0], [[-100,100, "S"]], SunSpriteDictionary,[-100,100] ,-2,0]
    MasterObjectList.append(ObjectSun)
    
    #Test to add in multiple suns to test power of rendering engine
    for i in range(0,9):
        tempSunList = ObjectSun.copy()
        x = random.randint(0, JetRealXBoundOffset + thumby.display.width)
        y = random.randint(0, JetMinY)
        tempSunList[0] = [x,y,-5]
        #MasterObjectList.append(tempSunList)
        
    #Bullets
    bulletXSpriteSize = 6
    bulletYSpriteSize = 3
    bulletAnimationInProgress = False #No need to run the loop over and over
    bulletCurrentFrame = 0
    bulletFrameCounter = 0
    bulletFrameCounterSpacing = 0
    bulletFrameMax = 0
    
    # BITMAP: width: 6, height: 3
    bulletByteMap01 = bytearray([4,0,0,0,0,4])
    # BITMAP: width: 6, height: 3
    bulletByteMap02 = bytearray([0,2,0,0,2,0])
    # BITMAP: width: 6, height: 3
    bulletByteMap03 = bytearray([0,0,1,1,0,0])
    bulletSpriteMap = bulletByteMap01 + bulletByteMap02 + bulletByteMap03
    
    
    #Bird Object (Birds are evil!)
     # BITMAP: width: 7, height: 7
    BirdByteMap01 = bytearray([4,2,4,8,4,2,4])
    # BITMAP: width: 7, height: 7
    BirdByteMap02= bytearray([1,2,4,8,4,2,1])
    # BITMAP: width: 7, height: 7
    BirdByteMap03 = bytearray([32,32,16,8,16,32,32])
    # BITMAP: width: 7, height: 7
    BirdByteMap04 = bytearray([64,32,16,8,16,32,64])
    BirdByteMap = BirdByteMap01 + BirdByteMap02 + BirdByteMap03 + BirdByteMap04
    
    BirdFarByteMap01 = bytearray([0,8,4,8,4,8,0])
    # BITMAP: width: 7, height: 7
    BirdFarByteMap02 = bytearray([0,2,4,8,4,2,0])
    # BITMAP: width: 7, height: 7
    BirdFarByteMap03 = bytearray([0,16,16,8,16,16,0])
    # BITMAP: width: 7, height: 7
    BirdFarByteMap04 = bytearray([0,32,16,8,16,32,0])
    BirdFarByteMap = BirdFarByteMap01 + BirdFarByteMap02 + BirdFarByteMap03 + BirdFarByteMap04
    
    # BITMAP: width: 7, height: 7
    BirdVeryFarByteMap01 = bytearray([0,0,8,8,8,0,0])
    # BITMAP: width: 7, height: 7
    BirdVeryFarByteMap02 = bytearray([0,0,4,8,4,0,0])
    # BITMAP: width: 7, height: 7
    BirdVeryFarByteMap03 = bytearray([0,0,16,8,16,0,0])
    BirdVeryFarByteMap04 =  bytearray([0,0,16,8,16,0,0])
    BirdVeryFarByteMap = BirdVeryFarByteMap01 + BirdVeryFarByteMap02 + BirdVeryFarByteMap03 + BirdVeryFarByteMap04

    #A sprite dictionary must exist as {"Spritename": [[Bytemap list], Width, Height,counters between frames, current counter, currentFrame]
    BirdSpriteDictionary = {"B1": [ [BirdVeryFarByteMap],7,7, 23, 0, 0], "B2": [ [BirdFarByteMap],7,7, 23, 0, 0],"B3": [ [BirdByteMap],7,7, 23, 0, 0]}
    BirdRangeList = [ [-100,-50, "B1"], [-50,-25, "B2"], [-25,100,"B3"] ]
    ObjectBird = [ [61,5,-20], [7,7], [0,0,0], [0,0], BirdRangeList, BirdSpriteDictionary, [-100,100], 0, -1]
    #MasterObjectList.append(ObjectBird)
    
    #VectorList =-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=
    #Vectors allow directions for common objects, they are stored as lists. [x,y,z]
    #remember, positive is in the right direction, and positive is down, and z positive is pointed towards the screen
    VN = [0,-1,0] #Vector for cardinal directions of the compass
    VS = [0,1,0]
    VE = [1,0,0]
    VW = [-1,0,0]
    VNW = [-1, -1, 0]
    VNE = [1,-1,0]
    VSW = [-1,1,0]
    VSE = [1, 1,0]
    VIN = [0,0,-1] #A vector heading INTO the screeen
    VOUT = [0,0,1] # a vector heading OUT of the screen. 
    
    #Safe box =-=-=-=-=-=-=-=-=-=-=-=-=-=-
    #It would be dumb to spawn in enemies where the player can freely roam the screen, this means all spawns
    #should happen outside of the screen OR far away from the player heading towards them
    
    #YPositions (remember, sprite size is 7x7) ENEMIES SHOULD NEVER SPAWN BELOW
    Y0 = -8
    Y1= 0
    Y2=7
    Y3=14
    Y4 = 21
    
    #XPositions (enemies should always spawn offscreen)
    XL =  0 #JetRealXMin - JetRealXBoundOffset - 7 - 14
    XR = JetRealXMax + JetRealXBoundOffset + 7 + 14
    
    #ZPositions (enemies either spawn at JetZ or far away) NEVER BEHIND THE PLAYER
    ZO = -99
    ZJ = JetRealZ
    
    

    
    
    
    
    #LEVEL LIST =-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=
    MaxEnemies = 11
    CurrentEnemies = 0
    
    #[ [ScoreRangeMin, ScoreRangeMax],[[enemyobjectlist, position, vector, velocity array]],[interval to spawn at, current score][spawned] [use once? 0 ]]
    MasterLevelList = []
    
    TestList= [ [0,9999999999999], [[ObjectBird, [61,-20,-20], [0,1,0], [1,0]]], [100,0], [False], 1 ]
    
    #MasterLevelList.append(TestList)
    
    Level1 = [ [1,9999999999999], [[ObjectBird, [XR,Y2,ZJ], VW, [0.5,0]]], [100,0], [False], 0 ]
    Level3 = [ [2,9999999999999], [[ObjectBird, [10,10,ZJ], [0,0,0], [0.5,0]]], [100,0], [False], 0 ]
    Level2 = [ [3,9999999999999], [[ObjectBird, [XL,Y2,ZJ], VE, [0.5,0]]], [100,0], [False], 0 ]
    LevelRogue = [ [30,9999999999999], [[ObjectBird, [XL,Y2,ZJ], VE, [0.5,0]]], [100,0], [False], 0 ]
    MasterLevelList.append(Level1)
    MasterLevelList.append(Level2)
    MasterLevelList.append(Level3)
    
    #TitleScreen =-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=
    
    # BITMAP: width: 18, height: 18
    TitleScreenPlaneWingsClosedMap = bytearray([0,0,0,0,0,0,192,240,255,255,240,192,0,0,0,0,0,0,0,96,112,184,222,239,255,255,127,127,255,255,239,222,184,112,96,0,0,0,0,0,1,1,0,3,0,0,3,0,1,1,0,0,0,0])
    # BITMAP: width: 18, height: 18
    TitleScreenPlaneWingsOpenMap = bytearray([0,0,0,0,0,0,192,240,255,255,240,192,0,0,0,0,0,0,48,56,24,156,206,239,255,255,127,127,255,255,239,206,156,24,56,48,0,0,0,0,1,1,0,3,0,0,3,0,1,1,0,0,0,0])
    # BITMAP: width: 72, height: 21
    TitleScreenNoStarMap = bytearray([1,3,11,19,75,147,75,147,75,147,75,3,255,255,3,3,254,255,3,3,255,254,0,255,255,99,99,127,62,0,0,0,3,3,255,255,3,3,0,255,255,96,96,255,255,0,255,255,0,0,255,255,0,255,255,124,240,124,255,255,3,75,147,75,147,75,147,75,19,11,3,1,
               0,0,0,0,0,0,2,4,18,52,50,48,55,55,48,48,51,55,54,54,55,51,48,55,55,48,48,48,48,48,48,48,48,16,7,7,0,0,16,55,55,48,48,55,55,48,51,55,54,54,55,51,48,55,55,48,49,48,55,55,48,50,52,18,4,2,0,0,0,0,0,0,
               0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0])
    # BITMAP: width: 72, height: 21
    TitleScreenStarMap = bytearray([1,3,11,19,75,147,75,147,75,147,75,3,255,255,3,3,254,255,3,3,255,254,0,255,255,99,99,127,62,0,0,0,3,3,255,255,3,3,0,255,255,96,96,255,255,0,255,255,0,0,255,255,0,255,255,124,240,124,255,255,3,75,147,75,147,75,147,75,19,11,3,1,
               0,0,0,0,0,0,2,4,18,52,50,48,55,55,48,48,51,55,54,54,55,51,48,55,55,48,48,48,48,48,48,176,176,144,199,247,240,192,144,183,183,48,48,55,55,48,51,55,54,54,55,51,48,55,55,48,49,48,55,55,48,50,52,18,4,2,0,0,0,0,0,0,
               0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,25,31,15,7,7,15,31,25,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0])
    # BITMAP: width: 72, height: 21
    TitleScreenGoMap = bytearray([1,3,11,19,75,147,75,147,75,147,75,3,255,255,3,3,254,255,3,3,255,254,0,255,255,99,99,127,62,0,0,0,3,3,255,255,3,3,0,255,255,96,96,255,255,0,255,255,0,0,255,255,0,255,255,124,240,124,255,255,3,75,147,75,147,75,147,75,19,11,3,1,
               0,0,0,0,0,0,2,4,18,52,50,48,55,55,48,48,51,55,54,54,55,51,48,55,55,48,48,48,48,48,48,176,176,144,135,7,128,128,144,183,55,176,48,55,55,48,51,55,54,54,55,51,48,55,55,48,49,48,55,55,48,50,52,18,4,2,0,0,0,0,0,0,
               0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,15,8,10,14,0,15,8,8,15,0,11,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0])
    #Title Screen 
    TitleScreenSprite = thumby.Sprite(72,21, TitleScreenNoStarMap,0,19)
    TitleScreenSpriteStar = thumby.Sprite(72,21, TitleScreenStarMap,0,19)
    TitleScreenSpriteGo = thumby.Sprite(72,21, TitleScreenGoMap,0,19)
    Timer1 = time.ticks_ms() #used to blink the star repeatedly
    Timer2 = time.ticks_ms() #used to open the wings on the plane
    Star = False
    TitleScreenPlaneYAdjust = 0 #Variable to move the plane into position
    #=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=
    
    TitleScreen = True
    
    #GameOverScreen =-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=
    
    # BITMAP: width: 72, height: 40
    gameOverScreenByteMap = bytearray([16,112,56,112,18,14,7,14,18,112,56,112,16,1,5,21,85,85,85,65,95,65,64,95,81,95,64,95,69,71,64,64,65,159,129,192,159,132,95,64,95,80,95,64,95,78,95,64,87,85,93,65,85,85,85,21,5,1,16,112,56,112,18,14,7,14,18,112,56,112,16,0,
           248,64,64,64,248,0,8,8,248,8,8,0,240,8,8,136,144,0,248,64,64,64,248,0,0,176,176,0,0,0,0,0,0,0,3,1,3,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,
           227,0,0,0,3,0,194,34,35,34,194,0,193,34,34,34,65,0,35,32,224,32,35,0,0,193,193,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,
           15,8,8,8,8,0,15,1,1,1,15,0,4,9,9,9,6,0,0,0,15,0,0,0,0,6,6,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,
           127,9,25,41,70,0,127,73,73,65,65,0,38,73,73,73,50,0,1,1,127,1,1,0,126,9,9,9,126,0,127,9,25,41,70,0,1,1,127,1,1,0,2,1,81,9,6,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0])
    # BITMAP: width: 72, height: 40
    gameOverScreenSwipeByteMap01= bytearray([0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,192,240,255,255,240,192,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,
            0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,128,248,248,128,0,0,0,0,0,0,0,48,56,24,156,206,239,255,221,65,65,221,255,239,206,156,24,56,48,0,0,0,0,0,0,0,128,248,248,128,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,
            0,0,0,0,0,0,0,0,0,128,192,192,224,112,120,254,15,15,175,79,254,120,112,224,192,192,128,0,0,0,0,1,1,0,251,0,0,251,0,1,1,0,0,0,0,128,192,192,224,112,120,254,15,15,175,143,254,120,112,224,192,192,128,0,0,0,0,0,0,0,0,0,
            0,0,0,0,0,0,0,0,0,1,1,0,4,14,15,7,222,2,3,222,7,15,14,4,0,1,1,0,0,0,0,192,96,112,115,240,240,115,112,96,192,0,0,0,0,1,1,0,4,14,15,7,222,2,3,223,7,15,14,4,0,1,1,0,0,0,0,0,0,0,0,0,
            0,0,0,32,32,32,32,32,32,32,32,32,32,32,32,32,47,32,32,47,32,32,32,32,32,32,32,32,32,32,0,7,62,62,30,51,51,30,62,62,7,32,32,32,32,32,32,32,32,32,32,32,47,32,32,47,32,32,32,32,32,32,32,32,32,32,32,32,32,0,0,0])
    # BITMAP: width: 72, height: 40
    gameOverScreenSwipeByteMap02 = bytearray([0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,192,240,255,255,240,192,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,
            0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,128,248,248,128,0,0,0,0,0,0,0,48,56,24,156,206,239,255,221,65,65,221,255,239,206,156,24,56,48,0,0,0,0,0,0,0,128,248,248,128,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,
            0,0,0,0,0,0,0,0,0,128,192,192,224,112,120,254,15,15,175,79,254,120,112,224,192,192,128,0,0,0,0,1,1,0,3,0,0,3,0,1,1,0,0,0,0,128,192,192,224,112,120,254,15,15,175,143,254,120,112,224,192,192,128,0,0,0,0,0,0,0,0,0,
            0,0,0,0,0,0,0,0,0,1,1,0,4,14,15,7,30,2,3,30,7,15,14,4,0,1,1,0,0,0,0,192,96,112,112,240,240,112,112,96,192,0,0,0,0,1,1,0,4,14,15,7,30,2,3,31,7,15,14,4,0,1,1,0,0,0,0,0,0,0,0,0,
            0,0,0,32,32,32,32,32,32,32,32,32,32,32,32,32,32,32,32,32,32,32,32,32,32,32,32,32,32,32,0,7,62,62,30,51,51,30,62,62,7,32,32,32,32,32,32,32,32,32,32,32,32,32,32,32,32,32,32,32,32,32,32,32,32,32,32,32,32,0,0,0])
    

    #MUSIC
    #=-=-=-=-=-=-=-=--=-=-=-=--=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-
    #Music effects, meant so that when the function is not yet done it does not run
    #    freqs = [0, 262, 294, 330, 349, 392, 440, 494]
    #    notes = ["-", "C", "D", "E", "F", "G", "A", "B"]
    #Music is stored as a list containing lists of frequency and duration in milliseconds
    #Remember, Frequency's minimal value is ZERO!
    
    MusicPlaying = False
    GameOverMusicPlaying = False
    TitleScreen = True
    GameOver = False
    MasterObjectListCopy = MasterObjectList.copy()
    MasterLevelListCopy = MasterLevelList.copy()
    Initizalization = False #Get out of the initilalization loop!


#Mess with the sound here!
class SoundEffects:
    def TitleMusic():
        global MusicPlaying
        
        if MusicPlaying == False: #check to see the music is not playing
            MusicPlaying = True
            TitleMusicList = [349,330,262,294]
            for x in TitleMusicList:
                thumby.audio.playBlocking(int(x*2), 210)
    def GameOverMusic():
        global GameOverMusicPlaying
        if GameOverMusicPlaying == False:
            GameOverMusicPlaying = True
            TitleMusicList = [349,330,262,262]
            for x in TitleMusicList:
                thumby.audio.playBlocking(int(x*2), 260)
            thumby.audio.playBlocking(int(294*2), 655)
    def ShootSound():
        #thumby.audio.stop()
        #print("I am playing sound!")
        thumby.audio.play(random.randint(525,530), 122)
    def KillSound():
        thumby.audio.play(random.randint(420,460), 122)

#Mess with how the game renders stuff here!
class Game:
    
    def BulletCollisionDetection(Object1XInput, Object1YInput, Object1Width, Object1Height):
        
        global JetRealX
        global JetRealY
        global JetX
        global JetY
        global bulletXSpriteSize
        global bulletYSpriteSize
        
        #Adjust the 'real' coordinates into local coordinates. 
        Object1X = Object1XInput - JetRealX + JetX
        Object1Y = Object1YInput - JetRealY + JetY
        
        xcollisiontrue = False
        ycollisiontrue = False
        Object2Width = bulletXSpriteSize +4 #These are hard coded for the bullets, they may be subject to change. 
        Object2Height = bulletYSpriteSize
        Object2X = int(JetX + (Object2Width/2))
        Object2Y = JetY - Object2Height
 
        #we can reduce calculations, we know for sure that if the minimum location of an object is beyond another's maximum
        #then mathmatically the two objects cannot collide.
        if (Object1X > (Object2X +Object2Width)) or ((Object1X + Object1Width) < Object2X) or (Object1Y > (Object2Y + Object2Height)) or ((Object1Y + Object1Height) < Object2Y):
            #print("Early falsehood detected")
            return False
        else:
            #print("Full scan required")
            for i1 in range(Object1X, Object1Width +Object1X +1): #remember, python ignores the last number, add a +1
                #print(i1)
                for j1 in range(Object2X, Object2Width +Object2X+1):
                    #print(j1)
                    if i1 == j1:
                        xcollisiontrue = True
                        #print("X collision true!")
        if xcollisiontrue == False: #no point running an intensive calculation if we know it is false
            #print("X collision is false!")
            return False
        elif xcollisiontrue == True: #no point running the collision if we know it is false
            #print("Attempting Y collision check")
            for i2 in range(Object1Y, Object1Height +Object1Y+1):
                #print(i2)
                for j2 in range(Object2Y, Object2Height +Object2Y+1):
                    if i2 ==j2:
                        ycollisiontrue = True
                        #print("Y Collision True")
        if ycollisiontrue == False:
            return False
        else:
            return True
    #This function brings the Horizon back into balance
    def HorizonMaxOrMinChecker():
        global HorizonY1
        global HorizonY2
        global HorizonMax
                #The Horizon can only tilt so far, check if it has tilted too far and stop it from tilting further
        if HorizonY1 < HorizonMax:
            HorizonY1 = HorizonMax
        if HorizonY2 < HorizonMax:
            HorizonY2 = HorizonMax
        
        #The min is a max due to my confusion. It just works
        if HorizonY1 > HorizonMin:
            HorizonY1 = HorizonMin
        if HorizonY2 > HorizonMin:
            HorizonY2 = HorizonMin
    #This function brings the X and Y coordinates back if they exceed their limits
    def XAndYMaxOrMinChecker():
        global JetX
        global JetMaxX
        global JetMinX
        global JetRealX
        global JetRealXMax
        global JetRealXMin
        global JetY
        global JetMaxY
        global JetMinY
        #If Jet screen location is greater than maximum, it must be reset
        if JetX > JetMaxX:
            JetX = JetMaxX
        elif JetX < JetMinX:
            JetX = JetMinX
            
        if JetY < JetMaxY:
            JetY = JetMaxY
        elif JetY > JetMinY:
            JetY = JetMinY
            
        #if Jet real location is greater than the maximum is must be reset. 
        if JetRealX > JetRealXMax:
            JetRealX = JetRealXMax
        elif JetRealX < JetRealXMin:
            JetRealX = JetRealXMin
            
    def InputDetect():
        global HorizonY1
        global HorizonY2
        #global HorizonMax
        #global Alternation
        global CorrectionSpeed
        global HorizonMiddle
        global JetX
        global JetY
        global JetVertSpeed
        global JetSideSpeed
        #global JetMaxX
        #global JetMinX
        #global JetMaxY
        #global JetMinY
        global JetMiddleX
        global JetMiddleY
        
        #bring the real coordinate plane into the function. 
        global JetRealX
        global JetRealXMiddle
        #global JetRealXMax
        #global JetRealXMin
        
        global JetRealY
        #global JetRealYMin
        #global JetRealYMiddle
        #global JetRealYMax
        #global JetRealYMin
        global JetRealSideSpeed
        #global JetRealVertSpeed
        #global JetRealCorrectionSpeed
        
        
        #global MasterObjectList
        #global ObjectBullet
        
        #Jet Sprites ( Assign current map to current direction!)
        global JetSpriteMapToUse
        global JetCenterMap
        global JetLeftMap
        global JetRightMap
        
        JetSpriteMapToUse = JetCenterMap #Default set the current sprite to center!
        
        if thumby.buttonL.pressed():
            HorizonY1 -= Sidespeed
            HorizonY2 += Sidespeed
            JetX -= JetSideSpeed
            JetRealX -= JetRealSideSpeed
            JetSpriteMapToUse = JetLeftMap
            Game.HorizonMaxOrMinChecker() #by shifting the checkers into the if statements, we can save processing power
            Game.XAndYMaxOrMinChecker()
            
        if thumby.buttonR.pressed():
            HorizonY1 += Sidespeed
            HorizonY2 -= Sidespeed
            JetX += JetSideSpeed
            JetRealX += JetRealSideSpeed
            JetSpriteMapToUse = JetRightMap
            Game.HorizonMaxOrMinChecker()
            Game.XAndYMaxOrMinChecker()
            
        if thumby.buttonU.pressed():
            HorizonY1 += Vertspeed
            HorizonY2 += Vertspeed
            JetY -= JetVertSpeed
            #JetRealY -= JetRealVertSpeed
            Game.HorizonMaxOrMinChecker()
            Game.XAndYMaxOrMinChecker()
            
        if thumby.buttonD.pressed():
            HorizonY1 -= Vertspeed
            HorizonY2 -= Vertspeed
            JetY += JetVertSpeed
            Game.HorizonMaxOrMinChecker()
            Game.XAndYMaxOrMinChecker()
            #JetRealY += JetRealVertSpeed
        if thumby.buttonA.pressed():
            Game.Shoot()

            
        #The game must be self correcting, or the player will get lost,
        #THIS MUST BE DONE CONSTANTLY
        if HorizonY1 > HorizonMiddle:
            HorizonY1 -= CorrectionSpeed
        elif HorizonY1 < HorizonMiddle:
            HorizonY1 += CorrectionSpeed
            
        if HorizonY2 > HorizonMiddle:
            HorizonY2 -= CorrectionSpeed
        elif HorizonY2 < HorizonMiddle:
            HorizonY2 += CorrectionSpeed
        
        
        #Correction for plane screen location to recenter plane
        #THIS MUST BE DONE CONSTANTLY, NO SAVINGS TO BE HAD ON COMPUTATION
        if JetX > JetMiddleX:
            JetX -= JetCorrectionSpeed
        elif JetX < JetMiddleX:
            JetX += JetCorrectionSpeed
        
        if JetY > JetMiddleY:
            JetY -= JetCorrectionSpeed
        elif JetY < JetMiddleY:
            JetY += JetCorrectionSpeed
            
        if JetRealX > JetRealXMiddle:
            JetRealX -= JetCorrectionSpeed
        elif JetRealX < JetRealXMiddle:
            JetRealX += JetCorrectionSpeed

        JetRealY = int(JetY)
        
        
    def HorizonScroll():
        global Alternation
        global AlternationMax
        LineY1ToDraw = HorizonY1 #set starting line to current horizon
        LineY2ToDraw = HorizonY2 
        tempsubtraction = 3

        
        #Draw the base horizon line seperately so the Horizon is constant. 
        thumby.display.drawLine(0,LineY1ToDraw,thumby.display.width, LineY2ToDraw,1)
        #Draw the lines below the Horizon 'alternating' so that they create the illusion of scrolling
        if Alternation < AlternationMax:
            Alternation +=1
        else:
            Alternation = 0 
 
            
        for x in range(0, 15): #Generate lines representing the scrolling Horizon
            thumby.display.drawLine(0,LineY1ToDraw + Alternation,thumby.display.width, LineY2ToDraw+Alternation,1)
            LineY1ToDraw += tempsubtraction #increases the Y, which prints each out at designated spacing
            LineY2ToDraw += tempsubtraction
    
    def Shoot():
        global Shoot
        Shoot = True
        
    def JetDraw():
        #global JetDefaultMap
        #global JetDefaultMapEngineOn
        global JetSpriteMapToUse
        global JetSpriteCurrentFrame
        global JetSpriteFrameCounter
        global JetSpriteFrameCounterSpacing
        global JetX 
        global JetY
        #global JetRealX #the coordinate plane that is supposed to exist, not the one that is merely broadcast on screen. 
        #global JetRealY
        #global JetRealZ
        #global JetTimer
        
        
        JetSpriteToUse = thumby.Sprite(10, 4, JetSpriteMapToUse, JetX, JetY,0)
        JetSpriteToUse.setFrame(JetSpriteCurrentFrame)
        if JetSpriteFrameCounter < JetSpriteFrameCounterSpacing:
            JetSpriteFrameCounter += 1
        else:
            JetSpriteCurrentFrame = JetSpriteToUse.getFrame() + 1
            JetSpriteFrameCounter = 0
        thumby.display.drawSprite(JetSpriteToUse)
        
        #Display the current coordinates at the top of the screen for ease of use.
        #Remember, the Font is 5x7
        #debugging tool for live jet coordinates. 
        #JetCoordinateString = "("+ str(JetRealX) + "," + str(JetRealY) + "," +str(JetRealZ) + ")"
        #thumby.display.drawText(JetCoordinateString, 0, 0, 1)
    
    
    #This function will place every object on screen using the built in list. 
    #The list will be built as follows:
    #A sprite dictionary must exist as {"Spritename": [[Bytemap list], Width, Height,counters between frames, current counter, currentFrame]
    #[ [[realX, realY,realZ], [Width, Height], [VectorX, VectorY,VectorZ], [Velocity, Acceleration], [[rangestart,rangeend,graphictopull]],{Sprite Dictionary}],[Derendering distance min, derendinerg distance max], UniqueIdentifier, EnemyTypeInt]
    #Because it is a list, more enemies can be appended to the list
    #List[i][0] contains the actual coordinates in the real coordinate plane, the printer will print on the screen as adjusted to the 'screen' coordinate
    #plane
    #accorindg to the right hand coordinate system, the positive direction of the Z axis faces OUT of the screen towards the player!
    #List[i][1]contains the width and height, which is input into the collision detection function (which is ran against all other objects in the list)
    #List[i][2]contains the unit vectors which indicate where the object is going
    #List[i][3]contains the objects velocity and acceleration, the acceleration is added to the velocity each calculations
    #the velocity is multiplied by the unit vector to update the realx, realy, and realz coordinates of List[i][1]
    #List[i][4] contains the sprite ranges, these are lists of z coordinates, and the graphic to pull. 
    #List[i][4][j] is meant to be iterated through, determining where List[i][0][2] is between List[i][4][j][0] and List[i][4][j][1]
    #List[i][4][j][2] represents the STRING of the sprite to call from the sprite dictionary.
    #List[i][5]["STRING"][0] will pull the requested bytemap from the dictionary, this string can then be used for the spritetoprint at realcoordinate plane
    #List[i][-1] contains the 'EnemyTypeInt', positive ints are good guys, negative ints are bad guys, checking if the enemy types multipled by each other
    #is a negative number allows you to quickly determine if the more sophisticated calculations should even be run. (ex. bullet into bad guy), bad guy into good guy
    #0 represents scenery. (Theoretically we can put scenery in game, though this will likely cause lag)
    #[i][-2] contains the unique identifier for the list as a whole, this allows the list to be removed since it is the only list with its unique values.
    
    
    
    def ObjectRenderer(OList):
        for i in OList: #the iterate through each object in the list of lists. 
            #retrieve the real coordinate plane from the array. Round to ints. 
            x = int(i[0][0])
            y = int(i[0][1])
            z = int(i[0][2])
            tempWidth = i[1][0]
            tempHeight = i[1][1]
            tempCollisionDetected = False
            
            #Derender an object so we don't have to deal with it if beyond the rendering distance contained in i[-3]
            if (z<i[-3][0]) or z > i[-3][1] or y > 50 or y < -50 or x>200 or x < -50:
                global CurrentEnemies
                CurrentEnemies -= 1
                OList.remove(i) #Delete myself! 
                continue 
            
            
            global JetRealX 
            global JetRealY
            global JetX
            global JetY 
            global Shoot
            
            #Collision Detection With Jet! and Bullets
            #determine if collision detection should even be run
            if i[-1] < 0: #collision with Jet should not be calculated unless i is an enemy
                global JetRealX 
                global JetRealY
                global JetRealZ
                global JetXSpriteSize #width
                global JetYSpriteSize #height
                #print("Determining collision with Jet!")
                tempCollisionDetected = Game.CollisionDetection(x,y, tempWidth, tempHeight, JetRealX, JetRealY, JetXSpriteSize, JetYSpriteSize, z, JetRealZ)
                if tempCollisionDetected == True: #Jet has hit an enemy object
                    global Gamerunning #in the future this can be replaced with a flashing screen or something to inciate health. 
                    #For now skip to gameover. 
                    GameOver = True
                    print("GameOver is: ", GameOver)
                    Gamerunning = False
                    print("Gamerunning is: ", Gamerunning)
                
                #Bulletcollision detection
                tempCollisionDetected = Game.BulletCollisionDetection(x,y, tempWidth, tempHeight)
                if (tempCollisionDetected == True) and (Shoot == True): #only delete yourself if collision detected and shooting is active in dangerzone!
                    global CurrentEnemies
                    CurrentEnemies -= 1
                    SoundEffects.KillSound()
                    OList.remove(i) #Delete myself! 
                    continue 
                #Collision Detection with bullets!
                
                #Oddly enough, constant lag is preferable, so this will be run continuously.
                        
            #Render The Object In The ObjectList!
            #=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-==
            #retrieve the byte array from the lists in i[4], make sure to go through every list. 
            tempByteArrayName = i[4][0][-1]
            
            for j in i[4]:
                #print("J is: ", j)
                if (z >= j[0]) and (z < j[1]):
                    tempByteArrayName = j[2]
                    
            #retrive and assemble the tempbytearray
            #A sprite dictionary must exist as {"Spritename": [[Bytemap list], Width, Height,counters between frames, current counter, currentFrame]
            tempDictionaryItem = i[5][tempByteArrayName] #retrieving the list over and over slows the game
            tempByteArray = tempDictionaryItem[0][0]

            #for j in i[5][tempByteArrayName][0][1:]:
                #tempByteArray = tempByteArray + j # dynamically rendering the byte array might be hardware inte
            #Retrieve the sprite counter
            tempMaxCounter = tempDictionaryItem[-3]
            tempCurrentCounter = tempDictionaryItem[-2]
            if tempCurrentCounter > tempMaxCounter:
                i[5][tempByteArrayName][-2] = 0 
                i[5][tempByteArrayName][-1] += 1 #update the frame counter
            else:
                i[5][tempByteArrayName][-2] += 1
                
            tempSpriteFrameCounter = i[5][tempByteArrayName][-1]   #retrieve the current updated counter (if updated)
            #print the object at the adjusted location
            tempSpriteWidth = tempDictionaryItem[1]
            tempSpriteHeight = tempDictionaryItem[2]
            #Adjust the sprites coordinates to show where they go
            tempadjustedx = x - JetRealX + JetX
            tempadjustedy = y - JetRealY + JetY
            tempSprite = thumby.Sprite(tempSpriteWidth, tempSpriteHeight, tempByteArray, tempadjustedx, tempadjustedy,0)
            tempSprite.setFrame(tempSpriteFrameCounter)
            thumby.display.drawSprite(tempSprite)
            
            #sprite has been displayed, and collision has been detected now adjust the coordinates for the next calculation
            #adjust the real coordinates by the velocity, increase velocity by acceleration
            tempVelocity = i[3][0] + i[3][1]
            i[3][0] = tempVelocity #acceleration has been applied, put velocity back in the array
            #apply velocity by the unit vector stored in i[2] to the coordinates stored in i[0] to generate new coordinates
            i[0][0] = i[0][0] + tempVelocity * i[2][0]
            i[0][1] = i[0][1] + tempVelocity * i[2][1]
            i[0][2] = i[0][2] + tempVelocity * i[2][2]
            
        
    
    #define a function for the purpose of determining if two objects have collided.
    
    def CollisionDetection(Object1X, Object1Y, Object1Width, Object1Height, Object2X,Object2Y, Object2Width,Object2Height, Object1Z, Object2Z):
        xcollisiontrue = False
        ycollisiontrue = False
        zcollisiontrue = False
        
        if Object1Z == Object2Z:
            zcollisiontrue = True
            #print("Z collision true!")
        else:
            #print("Oopsie, returned false!")
            return False
            
        #print(Object1X)
        #print(Object1Width)
        #we can reduce calculations, we know for sure that if the minimum location of an object is beyond another's maximum
        #then mathmatically the two objects cannot collide.
        if (Object1X > (Object2X +Object2Width)) or ((Object1X + Object1Width) < Object2X) or (Object1Y > (Object2Y + Object2Height)) or ((Object1Y + Object1Height) < Object2Y):
            return False
        else:
            for i1 in range(Object1X, Object1Width +Object1X +1): #remember, python ignores the last number, add a +1
                #print(i1)
                for j1 in range(Object2X, Object2Width +Object2X+1):
                    #print(j1)
                    if i1 == j1:
                        xcollisiontrue = True
                        #print("X collision true!")
        if xcollisiontrue == False: #no point running an intensive calculation if we know it is false
            #print("X collision is false!")
            return False
        elif xcollisiontrue == True: #no point running the collision if we know it is false
            #print("Attempting Y collision check")
            for i2 in range(Object1Y, Object1Height +Object1Y+1):
                #print(i2)
                for j2 in range(Object2Y, Object2Height +Object2Y+1):
                    if i2 ==j2:
                        ycollisiontrue = True
                        #print("Y Collision True")
        if ycollisiontrue == False:
            return False
        else:
            return True
    def HighScoreUpdate():
        global highScoreLocal
        global currentScore
        
        if currentScore > highScoreLocal: #if the current score is the highest score, replace it with the current score
            highScoreLocal = currentScore
        if (thumby.saveData.hasItem("highscore")):
            #print("Ey there's a high score here!")
            highScoreLocaltemp = int(thumby.saveData.getItem("highscore"))
            if highScoreLocaltemp > highScoreLocal:
                highScoreLocal = highScoreLocaltemp
                thumby.saveData.setItem("highscore",highScoreLocal)
                thumby.saveData.save()
        else:
                thumby.saveData.setItem("highscore",highScoreLocal)
                thumby.saveData.save()
        


    
        #The renderer is intensive, it is easier to render the bullets and advance their frames seperately.
    def BulletAnimation():
        global JetX
        global JetY
        global bulletXSpriteSize
        global bulletYSpriteSize
        global JetXSpriteSize
        global JetYSpriteSize
        global bulletAnimationInProgress
        global Shoot
        
        global bulletSpriteMap
        global bulletFrameCounter
        global bulletCurrentFrame
        global bulletFrameCounterSpacing
        global bulletFrameMax
        
        #remember, the coordinate plane starts in the upper left hand corner, and we want to 
        #animate the bullets ABOVE the current jet
        x = JetX + int(JetXSpriteSize/2) - int(bulletXSpriteSize/2)
        y = JetY - bulletYSpriteSize
        
        if Shoot == True:
                #Fire button is held down, but an animation is currently running, therefore:
            if bulletAnimationInProgress == False:
                #print("Ay Shoot is true, begin the animation")
                #Fire button is held down, but no bullet has started 
                bulletCurrentFrame = 0 #the bullet restarts
                bulletAnimationInProgress = True #A bullet animation has started.
                SoundEffects.ShootSound()
        
        #These exist outside of an if statement because constant lag is prefferable to lag spikes.
        tempSprite = thumby.Sprite(bulletXSpriteSize, bulletYSpriteSize, bulletSpriteMap, x,y, 0)
        tempSprite.setFrame(bulletCurrentFrame)
        if bulletAnimationInProgress == True: #The bullet animation is running, update and draw it
            #print("Ay I'm rendering a bullet")

            thumby.display.drawSprite(tempSprite)
            
            if bulletFrameCounter < bulletFrameCounterSpacing:
                #print("Advancing the bullet Frame counter")
                
                bulletFrameCounter += 1
            else:
                #print("Ay stop drawing that bullet")
                bulletFrameCounter = 0
                bulletCurrentFrame = tempSprite.getFrame() + 1
                if bulletCurrentFrame > bulletFrameMax:
                    bulletFrameMax = bulletCurrentFrame
                elif bulletCurrentFrame == bulletFrameMax:
                    #print("Ay stop the animation, it's over!")
                    bulletAnimationInProgress = False #maximum frames have been reached, do not ru
    #The objective of the spawn enemy function is to spawn predefined object lists at newly defined
    #directional vectors, positions, and velocities. 
    #Spawning should occur every time that the 'score' increases above a certain amount.
    #the level list is a list of lists
    #format should be:
    #[ [ScoreRangeMin, ScoreRangeMax],[[enemyobjectlist, position, vector, velocity array]],[interval to spawn at, current score][spawned] [use once? 0 ]]
    #i[-1] represents whether the enemies should be spawned infinitely based on i[-3]  0 means not infinite, 1 means YES
    #if the enemy is spawned because Score is within the range defined in i[0], the enemy is marked spawned in i[-2]
    #if the enemy is spawned and is marked to not be respawned, the list should be deleted from the level list. 
    
    
    def SpawnEnemy(Score, LevelList, ObjectList):
        global CurrentEnemies
        global MaxEnemies
        for i in LevelList:
           # print(i[0][0])
            #if the enemy is spawned and only meant to be spawned once, do not spawn again. 
            if i[-1] == 0 and i[-2] == True:
                LevelList.remove(i) #removing the enemy from the list makes the list run faster
                #print("Removed Level List ", i[0][0])
                continue
                
            #only run the program because the level list has tripped into the correct range.
            #[enemyobjectlist, position, vector, velocity array]
            #[ [[realX, realY,realZ], [Width, Height], [VectorX, VectorY,VectorZ], [Velocity, Acceleration], [[rangestart,rangeend,graphictopull]],{Sprite Dictionary}],[Derendering distance min, derendinerg distance max], UniqueIdentifier, EnemyTypeInt]
            

            if Score > i[0][0] and Score <= i[0][1] and CurrentEnemies < MaxEnemies:
                if i[-1] == 0 or i[-3][-1] > i[-3][0]: #if infinitely spawning or spawning within the score counter
                    i[-3][-1] = 0 # spawn successful, reset spawn counter if applicable (do it anyway)
                    for j in i[1]:
                        tempObjectList = j[0].copy()
                        tempObjectList[0] = j[1].copy() #copy the position list, since it is a list of lists, must be deep copied
                        tempObjectList[2] = j[2].copy() #copy the vectory list
                        tempObjectList[3] = j[3].copy() #copy the velocity and accerlation array
                        tempObjectList[-2] = Score #score can double as the unique identifier
                        ObjectList.append(tempObjectList.copy())
                        CurrentEnemies += 1
                        #print("Enemy ", i[0][0], " Spawned")
                    i[-2] = True #set spawn to true (important for level list)
                i[-3][-1] += 1 #increase the score interval counter
            
        #different enemy types should be spawn based upon score
        #the higher the score, the faster and more enemies there should be.
        
        #Wow, that was nice, time to add items to the list randomly if the list is empty
        #When the list is empty, enter 'rogue-lite' mode where items are added to the list
        #Since only a maximum level of enemies can be spawned, there's no issue. 
        if len(LevelList) == 0 and CurrentEnemies < MaxEnemies:
            global XR
            global XL
            global ZO
            global ZJ
            global Y0
            global Y4
            global ObjectBird
            #choose if this is a side scrolling enemy (spawns only at bounds) OR
            #a screen out scrolling enemy
            
            #position coordinates
            tempz = random.choice([ZO,ZJ])

            tempy = random.randint(Y0+16, Y4)
            
            #vector coordinates
            tempvx = random.randint(-1,1)
            tempvy = random.randint(-1,1)
            
            if tempz == ZJ: #which means must spawn on edges, and head to middle
                tempvz = 0 #no movement within the layer
                tempx = random.choice([XL - 40, XR+40])
                tempy = random.randint(Y0+16, Y4 + 8)
                if tempx == XL - 40:
                    tempvx = 1
                elif tempx == XR +40:
                    tempvx = -1
            else:
                tempvz = 1 #movement out of the screen, 
                tempx = random.randint(XL-30,XR +30)
                tempy = random.randint(Y0+16, Y4)
                tempvx = 0
                tempvy = 0

            
            tempposlist = [tempx,tempy, tempz]
            tempvlist = [tempvx,tempvy,tempvz]
            
            LevelRogue = [ [15,9999999999999], [[ObjectBird, tempposlist , tempvlist, [0.5 +random.random(),0]]], [100,0], [False], 0 ]
            templist = LevelRogue.copy()
            
            for j in templist[1]:
                tempObjectList = j[0].copy()
                tempObjectList[0] = j[1].copy() #copy the position list, since it is a list of lists, must be deep copied
                tempObjectList[2] = j[2].copy() #copy the vectory list
                tempObjectList[3] = j[3].copy() #copy the velocity and accerlation array
                tempObjectList[-2] = Score #score can double as the unique identifier
                ObjectList.append(tempObjectList.copy())
                CurrentEnemies += 1
                
            
        
    #bad news, the spawn function permanently alters the lists the level list contains: solution:
    #manually set all items in the levellist to say they have not been spawned
    def Level_List_Reset(LevelList):
        for i in LevelList:
            i[-2] = False #by setting everything to say it has NOT been spawned, it therefore has not. 
        
            
Initizalization2 = True
#print("This game sessions random ID is:", random.randint(0,100))
RunForever = True
while(RunForever == True):
    #TitleScreen
    #This new initialization loop is a poorly made copy of the first one, I apologize. 
    while(Initizalization2 == True):
        Timer1 = time.ticks_ms() #used to blink the star repeatedly
        Timer2 = time.ticks_ms()
        BulletCount = 0
        MasterObjectList = MasterObjectListCopy.copy()
        MasterLevelListCopy = MasterLevelList.copy()
        Game.Level_List_Reset(MasterLevelListCopy)
        currentScore = 0
        MusicPlaying = False
        GameOverMusicPlaying = False
        TitleScreenPlaneYAdjust = 0
        TitleScreen = True
        Transition = False

        JetRealX = int((int(thumby.display.width) + (JetRealXBound*2))/2   - JetXSpriteSize/2)
        JetRealY = 20
        JetRealZ = -20
        JetX = (thumby.display.width/2)
        JetY = (thumby.display.height/2) + JetYAdjustment
        BlinkBool = False
        gameOverYAdjust = 0
        CurrentEnemies = 0
        Initizalization2 = False
        
        
    
    while(TitleScreen == True):
        thumby.display.fill(0)
        #Print the plane
        #End the title screen
        if thumby.inputPressed() or  thumby.inputJustPressed():
            TitleScreen = False
            Transition = True
            thumby.audio.playBlocking( 783, 210)
            thumby.audio.playBlocking( 783, 210)
            thumby.audio.playBlocking( 880, 210)
            
        if TitleScreen == True:
            if TitleScreenPlaneYAdjust < 72:
                TitleScreenPlaneWingsClosedSprite = thumby.Sprite(18,18, TitleScreenPlaneWingsClosedMap,36-9, 72 - TitleScreenPlaneYAdjust)
                thumby.display.drawSprite(TitleScreenPlaneWingsClosedSprite)
                TitleScreenPlaneYAdjust += 3 #rate at which the plane ascends
                Timer2 = time.ticks_ms()
            else:
        
                if time.ticks_ms() - Timer2 > 900:
                    SoundEffects.TitleMusic()
                    TitleScreenPlaneWingsOpenSprite = thumby.Sprite(18,18, TitleScreenPlaneWingsOpenMap,36-9, 72 - TitleScreenPlaneYAdjust)
                    thumby.display.drawSprite(TitleScreenPlaneWingsOpenSprite)
                else:
                    TitleScreenPlaneWingsClosedSprite = thumby.Sprite(18,18, TitleScreenPlaneWingsClosedMap,36-9, 72 - TitleScreenPlaneYAdjust)
                    thumby.display.drawSprite(TitleScreenPlaneWingsClosedSprite)
        #Blink the star
        if time.ticks_diff(time.ticks_ms(),Timer1) > 800: #800 milliseconds of star blinkage
            if Star == False:
                Star = True
            else:
                Star = False
            Timer1 = time.ticks_ms()
        if Star == False:
            thumby.display.drawSprite(TitleScreenSprite)
        else:
            thumby.display.drawSprite(TitleScreenSpriteStar)
    
        thumby.display.update()
    #Transition screen
    
    while(Transition == True):
        thumby.display.fill(0)    
        TitleScreenPlaneWingsClosedSprite = thumby.Sprite(18,18, TitleScreenPlaneWingsClosedMap,36-9, 72 - TitleScreenPlaneYAdjust)
        thumby.display.drawSprite(TitleScreenPlaneWingsClosedSprite)
        TitleScreenPlaneYAdjust += 3
        if TitleScreenPlaneYAdjust > (72+25):
            Transition = False
            Gamerunning = True
        if time.ticks_diff(time.ticks_ms(),Timer1) > 800: #800 milliseconds of star blinkage
            if Star == False:
                Star = True
            else:
                Star = False
            Timer1 = time.ticks_ms()
        if Star == False:
            thumby.display.drawSprite(TitleScreenSprite)
        else:
            thumby.display.drawSprite(TitleScreenSpriteGo)
    
        thumby.display.update()    
        
    #Actual Gameplay Loop Goes Here
    while(Gamerunning == True):
        thumby.display.fill(0) #clear graphics so new ones can be printed
        Shoot = False
        currentScore += 1*ScoreModifier
        Game.SpawnEnemy(currentScore, MasterLevelListCopy, MasterObjectList)
        Game.InputDetect()
        Game.HorizonScroll()
        Game.ObjectRenderer(MasterObjectList)
        Game.JetDraw()
        Game.BulletAnimation()
        thumby.display.update()
    
    #print("Gamerunning Loop has ended")
    if Initizalization2 == False:
        GameOver = True
        
        
    while(GameOver == True):

        #print("The game has ended, show post screen card")
        Game.HighScoreUpdate()
        scoreString = str(int(currentScore))
        highScoreString = str(int(highScoreLocal))
        thumby.display.fill(0)

        GameOverSwipeBackGroundSprite = thumby.Sprite(72,40, gameOverScreenSwipeByteMap01 + gameOverScreenSwipeByteMap02,0,0 - gameOverYAdjust,-1)
        GameOverBackgroundSprite = thumby.Sprite(72,40, gameOverScreenByteMap,0,40 - gameOverYAdjust,-1)

        thumby.display.drawSprite(GameOverSwipeBackGroundSprite)
        thumby.display.drawSprite(GameOverBackgroundSprite)
        GameOverSwipeBackGroundSprite.setFrame(GameOverSwipeBackGroundSprite.currentFrame + 1) #I don't know why, the frames won't change??
        thumby.display.drawText(highScoreString, 29, 40 + 11 - gameOverYAdjust, 1)
        thumby.display.drawText(scoreString, 29, 40 + 21 - gameOverYAdjust,1)
        thumby.display.drawText("(A)",54,40 + 32 - gameOverYAdjust,1)
        thumby.display.update()
        SoundEffects.GameOverMusic()
        #print("Game is over wtf")

        if gameOverYAdjust < 40:
            #print("I am adjusting gameover Y!")
            gameOverYAdjust += 1
        if thumby.buttonA.pressed():
            #rint("Starting a new game!")
            Initizalization2 = True
            GameOver = False
        #print("Game over is:", GameOver)
        
    print("Still in the regular loop")
print("Not sure how this happened, got outside of perpetual loop")
    


