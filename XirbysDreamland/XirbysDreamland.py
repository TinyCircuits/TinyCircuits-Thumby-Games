############################################################################
#                      __  ___      _           
#                      \ \/ (_)_ __| |__  _   _ 
#                       \  /| | '__| '_ \| | | |
#                       /  \| | |  | |_) | |_| |
#                      /_/\_\_|_|  |_.__/ \__, |
#                                         |___/ 
#
#              / \ / \ / \ / \   / \ / \ / \ / \ / \ / \ 
#             (  C  o  c  o   ) ( C   l   o  u   d   s  )
#              \ / \ / \ / \ /   \ / \ / \ / \ / \ / \_/ 
#   ˚☽                                     
#            ☆                          ☆                 ☆            ☆
#               Volume 1. Coco Clouds - Xirby's Dreamland                  
############################################################################

#                              Written by Sarah Bass
#                Check out my other games for Android, Fitbit, and more
#                           https://github.com/SarahBass
################
#####IMPORTS####
################
import thumby
import gc
import time
import utime
import machine

#Game Maintenance-------------------------# 
machine.freq(125000000)
gc.enable()

#Global Variables-------------------------# 
BGMOffset = utime.ticks_us()

#Button Short Keys
U = thumby.buttonU
D = thumby.buttonD
L = thumby.buttonL
R = thumby.buttonR
B = thumby.buttonB
A = thumby.buttonA

#Secret Code to Skip Introduction
secret_code_sequence = ["U", "U", "D", "D", "L", "R", "L", "R", "B", "A"]
button_press_sequence = []

#Game Variables
abutton = 0
GameRunning = False
mover = 0
looper = True
mover2=0
Scene=0
width=16
height=16
xPosition = int((thumby.display.width/2) - (width/2))
yPosition = int((thumby.display.height/2) - (height/2))
itemSpawn = [20, 30, 25, 0, 10, 5, 18, 15, 4, 5, 8, 9 ]
enemySpawn = [20, 10,0, 5, 15]
itemSpawnX=[0, 5, 10, 15, 20, 25, 30, 35, 40, 45, 50, 60, 65, 70, 12]
move=0
gamespeed = 10
level = 0
speedup=1
turn=0
boss=0
HP=50
attack=0
stars=0
hearts=0
#Better Organization would be to store the music, graphics, and draw functions in a separate .py
#Then call the .py and load the graphics 
#I have everything locally stored for simplicity

#-=x=-=x=-=x=-=x=-=x=-=x=-=x=-=x=-=x=-=x=-=x=-=x=-=x=-=x=-=x=--=x=
#                        GAME STORAGE                            # 
#-=x=-=x=-=x=-=x=-=x=-=x=-=x=-=x=-=x=-=x=-=x=-=x=-=x=-=x=-=x=--=x=

#####################
#    Music          #
#####################

MusicNoteDict = {
    0: 1046,
    "B2": 123,
    "C3": 130,
    "CS3": 138,
    "D3": 147,
    "DS3": 155,
    "E3": 165,
    "F3": 175,
    "FS3": 185,
    "G3": 196,
    "GS3": 207,
    "AS3": 233,
    "Bf3": 233,
    "A3": 220,
    "B3": 247,
    "AS4": 466,
    "A4": 440,
    "C4": 261,
    "CS4": 277,
    "D4": 294,
    "DS4": 311,
    "E4": 330,
    "F4": 349,
    "FS4": 370,
    "G4": 392,
    "GS4": 415,
    "Bf4": 466,
    "An4": 440,
    "B4": 494,
    "C5": 523,
    "CS5": 554,
    "D5": 587,
    "DS5": 622,
    "E5": 659,
    "F5": 698,
    "FS5": 740,
    "G5": 784,
    "GS5": 831,
    "An5": 880,
    "B5": 988,
    "C6": 1046
}

#Introduction Theme
SongList1 = [
    # Original Opening Music Designed by Myself
    "B3", "E4", "FS4", "GS4", "B3", "E4", "FS4", "GS4",
    "B4", "E5", "FS5", "GS5", "B4", "E5", "FS5", "GS5",
    # Original Boss Music Designed by Myself
    "C4", "G3", "AS3", "A3",
    "G3", "C3", "C3", "G3", "G3", "G3",
    "C4", "G3", "AS3", "A3",
    "G3",
    "C4", "G3", "AS3", "A3",
    "G3", "C3", "C3", "G3", "G3", "G3",
    "F3", "E3", "D3", "C3",
    # Xirby Remix Main Game - Composed by taking Sheet Music notes, remixing lines, and lowering an octave
    "DS5", "D5", "C5", "Bf4", "F4", "D4", "GS4", "Bf4", "C5", "D5", "B4", 0,
    "C5", 0, "G4", 0, "DS4", "D4", "C4", 0, "C4", "D4", "DS4", "C4", "Bf3", "C4", "G3", 0,
    "C5", 0, "G4", 0, "DS4", "D4", "C4", "C4", "D4", "DS4", "F4", "D4", "Bf3", "C4", "G3", "C4", 0,
    "C5", 0, "G4", 0, "D4", "F4", "G4", "C4", "D4", "F4", "D4", "Bf3", "C4", 0,
    # Xirby Remix Part 2  Composed by taking Sheet Music notes, remixing lines, and lowering an octave
    "DS4", "DS4", "DS4", "DS4", "F4", "G4", "G4", "G4", "F4", "DS4", "D4", "D4", "D4", "D4", "DS4", "D4",
    "DS4", "D4", "C4", "C4", "C4", "C4", "D4", "DS4", "DS4", "DS4", "D4", "C4", "Bf3", "Bf3", "Bf3", "Bf3", "C4", "D4",
    "D5", "F5", "G5", "D5", "F5", "G5", "D5", "F5", "D5", "F5", "G5", "C6", "B5", 0
]
#Waiting and Boss Music Composed by myself based on Beat of Bagpipes
SongList2 = ["C4", "G3", "AS3", "A3",
"G3", "C3", "C3", "G3", "G3", "G3",
"C4", "G3", "AS3", "A3",
"G3",
"C4", "G3", "AS3", "A3",
"G3", "C3", "C3", "G3", "G3", "G3",
"F3", "E3", "D3", "C3"]
#Game Music Main (Removed Shrill Stops)
SongList3 = [ "DS5", "D5", "C5", "Bf4", "F4", "D4", "GS4", "Bf4", "C5", "D5", "B4","B4",
"C5","C5", "G4","G4", "DS4", "D4", "C4","C4", "C4", "D4", "DS4", "C4", "Bf3", "C4", "G3","G3",
"C5", "G4", "DS4", "D4", "C4", "C4", "D4", "DS4", "F4", "D4", "Bf3", "C4", "G3", "C4",
"C5","C5", "G4","G4", "D4", "F4", "G4", "C4", "D4", "F4", "D4", "Bf3", "C4","C4",
"DS4", "DS4", "DS4", "DS4", "F4", "G4", "G4", "G4", "F4", "DS4", "D4", "D4", "D4", "D4", "DS4", "D4",
"DS4", "D4", "C4", "C4", "C4", "C4", "D4", "DS4", "DS4", "DS4", "D4", "C4", "Bf3", "Bf3", "Bf3", "Bf3", "C4", "D4",
"D5", "F5", "G5", "D5", "F5", "G5", "D5", "F5", "D5", "F5", "G5", "C6", "B5", "B5"]
#Higher Pitch Waiting Song with more notes 
SongList4 =[
"C5", "G4", "AS4", "A4",
"G4", "C4", "C4", "G4", "G4", "G4",
"C5", "G4", "AS4", "A4",
"G4",
"C5", "G4", "AS4", "A4",
"G4", "C4", "C4", "G4", "G4", "G4",
"F4", "E4", "D4", "C4",
"C4", "D5", "D5", "D5", "D5", "D5",
"D5", "D5", "D5", "C5", "E5",
"C5", "C5", "E5", "E5", "C5",
"F5", "D5", "D5", "E5",
"C5", "D5", "E5", "D5", "C5"]

#Continue Screen Original Song Composed by myself 
SongList5=["B2", "E3", "FS3", "GS3", "B2", "E3", "FS3", "GS3",
    "B3", "E4", "FS4", "GS4", "B3", "E4", "FS4", "GS4"]

#End Screen - Composed by myself on a Kalimba then translated !
SongList6=[
    "C5", "B4", "C5", "B4", "G4",  
    "A4", "G4", "A4", "G4", "C4",  
    "F4", "E4", "F4", "E4", "C4",  
    "D4", "B4", "A4", "G4", "F4", "E4", "D4", 
    "C5", "B4", "C5", "B4", "G4",  
    "A4", "G4", "A4", "G4", "C4",  
    "F4", "E4", "D4", "E4", "F4", "E4", "D4", "C4", 
    "A4", "G4", "A4", "G4", "C4",  
    "F4", "E4", "D4", "E4", "G4", 
    "A4", "G4", "F4", "E4", "C5","C5", "B4", "B4",  

    "C5", "B4", "C5", "B4", "C5", 
    "D5", "C5", "B4", "C5", "E5", 


    "E5", "D5", "C5", "B4", "C5", "D5", "D5", "C5",
     "B4", "A4", "G4", "F4", "E4", "D4",  

    "C5", "B4", "C5", "B4", "G4", 
    "A4", "G4", "A4", "G4", "C4",  
    "F4", "E4", "F4", "E4", "C4",  
    "D4", "B4", "A4", "G4", "F4", "E4", "D4",  

    "C5", "B4", "C5", "B4", "G4",  
    "A4", "G4", "A4", "G4", "C4",  

    "F4", "E4", "D4", "E4", "F4", "E4", "D4", "C4" , "C4", 
    
    
    "C4", "B3", "C4", "B3", "G3",  
    "A3", "G3", "A3", "G3", "C3", 
    "F3", "E3", "F3", "E3", "C3",  
    "D3", "B3", "A3", "G3", "F3", "E3", "D3",  
    "C4", "B3", "C4", "B3", "G3",  
    "A3", "G3", "A3", "G3", "C3",  
    "F3", "E3", "D3", "E3", "F3", "E3", "D3", "C3",  
    "A3", "G3", "A3", "G3", "C3",  
    "F3", "E3", "D3", "E3", "G3",  
    "A3", "G3", "F3", "E3", "C4", "C4", "B3", "B3",  

    "C4", "B3", "C4", "B3", "C4",  
    "D4", "C4", "B3", "C4", "E4", 

    "E4", "D4", "C4", "B3", "C4", "D4", "D4", "C4",  
    "B3", "A3", "G3", "F3", "E3", "D3",  

    "C4", "B3", "C4", "B3", "G3",  
    "A3", "G3", "A3", "G3", "C3",  
    "F3", "E3", "F3", "E3", "C3", 
    "D3", "B3", "A3", "G3", "F3", "E3", "D3",  

    "C4", "B3", "C4", "B3", "G3", 
    "A3", "G3", "A3", "G3", "C3",  

    "F3", "E3", "D3", "E3", "F3", "E3", "D3", "C3", "C3"]


    
# Note durations 
#(using a standard quarter note duration of 200ms for simplicity)
def PlayMusic(utimeTicksUS, SongList):
    NoteLengthMS = 200
    NoteLengthUS = NoteLengthMS * 1000 
    SongLength = len(SongList) * NoteLengthUS
    CurSongBeat = int((utimeTicksUS % SongLength)/NoteLengthUS)
    CurNote = SongList[CurSongBeat] 
    CurFreq = MusicNoteDict[CurNote]
    #print(CurFreq)
    thumby.audio.play(CurFreq, NoteLengthMS)
    return


#####################################
########### SPRITE ARRAYS ###########
#####################################

#I actually hand created all of this artwork in Pixaki on the ipad to fit this tiny 72x40 screen
#It was a lot of work to animate all of these scenes!
#The end product looks really great though :`-)
# 5x9 for 1 frames
FreakLogo = bytearray([131,125,78,117,131,0,1,1,1,0])
# 69x36 for 1 frames
GameTitle = bytearray([255,255,255,255,255,31,207,207,159,63,127,15,199,247,247,39,15,231,231,231,7,3,51,59,249,249,29,29,189,249,123,33,9,29,253,253,253,157,157,253,249,123,3,1,29,125,249,227,231,251,61,29,0,14,224,243,247,55,55,247,239,31,255,255,255,255,255,255,255,255,255,255,255,255,252,121,3,199,224,248,62,31,7,224,224,192,1,15,127,254,240,0,0,63,127,127,3,7,15,30,60,16,0,31,63,63,49,49,63,63,62,12,0,0,0,63,63,1,0,0,60,124,112,224,255,127,120,0,248,254,255,255,255,255,255,255,255,255,255,255,255,255,255,127,56,51,23,3,128,192,192,192,192,129,1,1,192,240,48,16,0,0,0,248,28,60,240,192,0,248,60,248,240,56,60,248,0,0,0,192,254,127,15,3,0,192,240,188,134,254,0,0,0,224,192,1,3,227,7,7,15,207,207,223,191,63,127,243,225,204,30,126,198,134,12,188,248,243,7,12,249,255,63,57,112,7,223,223,211,219,192,231,231,241,249,249,243,246,240,248,248,251,248,248,251,248,240,192,223,223,216,208,208,195,249,248,248,240,247,243,248,128,191,129,227,207,191,128,152,63,111,32,48,153,207,224,15,15,15,15,12,9,3,6,3,11,9,12,14,14,14,14,15,14,14,15,15,15,15,15,15,15,15,15,15,15,15,15,15,15,15,15,15,15,15,15,15,15,15,15,15,15,15,15,15,15,15,15,15,15,15,15,15,15,15,15,15,15,15,15,15,15,15,15,15])

###Xirby###
#16X16 for 1 frames
Xirbystarsmall = bytearray([255,31,231,217,190,158,166,190,166,193,251,253,253,131,127,127,255,255,142,181,187,223,223,239,223,191,191,127,15,243,251,252])
# 16x16 for 1 frames
Xirbystarblack= bytearray([31,239,39,89,190,158,166,190,166,65,61,2,2,125,131,127,255,142,117,74,68,160,160,208,160,64,64,64,112,12,247,248])
# 16x16 for 1 frames
Xirbymask = bytearray([0,0,224,248,254,254,254,254,254,248,248,252,252,128,0,0,0,0,0,49,59,31,31,15,31,63,63,127,15,3,3,0])
#25X30 for 1 frames
Xirbyumbrella = bytearray([255,255,255,255,255,255,255,255,255,255,143,183,59,13,5,198,226,242,122,26,130,225,241,135,31,255,255,63,223,223,223,191,223,223,223,223,191,223,223,198,128,56,253,248,249,243,243,231,243,240,255,255,4,123,255,227,191,255,227,63,191,63,127,127,159,227,252,255,255,255,255,255,255,255,255,63,63,56,59,56,57,59,59,59,56,57,57,59,56,63,63,63,63,63,63,63,63,63,63,63])
# 72x30 for 2 frames
Xirbyheadphones = bytearray([255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,223,255,119,255,223,255,255,255,255,255,255,255,255,255,255,207,31,191,127,255,255,255,255,255,255,255,255,255,127,127,127,127,127,127,127,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,191,255,239,255,191,255,255,255,191,95,30,153,199,255,63,207,199,11,229,242,250,120,184,253,125,189,253,253,248,224,205,29,57,147,199,143,127,255,87,87,87,87,87,87,87,87,87,87,87,87,87,87,87,87,87,87,87,87,87,87,87,87,87,87,87,87,87,87,87,87,87,87,87,87,86,87,87,87,87,87,87,87,87,87,87,87,64,27,251,243,207,191,127,254,247,255,254,255,255,63,207,231,243,251,243,231,15,3,80,87,63,63,63,63,63,63,63,63,63,63,63,63,63,63,63,63,63,63,63,63,63,63,63,63,63,63,63,63,63,63,63,63,63,63,63,63,63,63,63,63,63,63,63,63,63,63,63,55,35,2,1,3,15,15,7,0,3,3,3,3,1,6,15,15,15,7,1,1,0,32,32,50,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,87,255,119,255,87,255,255,255,255,255,255,255,255,255,255,255,249,195,55,239,255,255,255,255,255,255,255,255,255,127,127,127,127,127,127,127,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,175,255,239,255,175,255,255,247,235,227,243,248,255,63,207,199,11,229,242,250,56,216,253,61,221,253,253,248,224,205,29,57,147,199,143,127,255,87,87,87,87,87,87,87,87,87,87,87,87,87,87,87,87,87,87,87,87,87,87,87,87,87,87,87,87,87,87,87,87,87,87,87,86,87,86,87,86,87,87,87,87,87,87,87,87,64,27,251,243,207,191,127,255,251,255,255,255,255,63,207,231,243,251,243,231,15,3,80,87,63,63,63,63,63,63,63,63,63,63,63,63,63,63,63,63,63,63,63,63,63,63,63,63,63,63,63,63,63,63,63,63,63,63,63,63,63,63,63,63,63,63,63,63,63,63,63,59,51,48,33,35,15,15,7,0,3,3,3,3,1,6,15,15,15,7,1,1,0,32,32,50])
Spr = thumby.Sprite(72, 30, Xirbyheadphones)

###Foreground Objects####
# 12x10 for 1 frames
starblack = bytearray([255,239,207,15,7,129,129,7,15,207,239,255,3,3,3,2,3,3,3,3,2,3,3,3])
# 12x10 for 1 frames
starwhite = bytearray([239,215,55,247,249,254,126,249,247,55,215,239,3,3,2,1,1,0,2,1,1,2,3,3])
# 12x10 for 1 frames
starmask = bytearray([0,16,48,240,248,126,126,248,240,48,16,0,0,0,0,1,0,0,0,0,1,0,0,0])


###Background Objects###
# 16x16 for 1 frames
enemySprite = bytearray([255,113,109,29,139,199,71,129,134,65,199,151,19,75,113,254,190,157,205,192,217,227,242,193,49,194,243,225,212,173,157,254])
# 16x16 for 1 frames
enemyMask = bytearray([0,142,158,254,252,248,248,254,255,254,248,248,252,188,140,0,1,3,51,63,63,31,15,63,255,63,15,31,59,115,99,1])
#20x23 for 1 frames
moon= bytearray([255,63,223,239,247,251,253,253,253,254,254,62,206,246,250,253,255,255,255,255,128,127,251,255,252,247,239,247,252,255,251,224,159,127,255,255,255,255,255,255,127,126,125,123,119,111,95,95,95,63,63,63,63,63,62,93,93,91,107,119])
# 23x3 for 1 frames
hazeblit = bytearray([4,0,5,0,4,0,5,0,4,0,5,0,4,0,5,0,4,0,5,0,4,0,5])
# 23x3 for 1 frames
haze = bytearray([3,7,2,7,3,7,2,7,3,7,2,7,3,7,2,7,3,7,2,7,3,7,2])
# 8 x 7 for 1 frame
heart = bytearray([113,110,94,61,60,94,110,113])
# 8x7 for 1 frames
blackheart = bytearray([113,96,64,1,0,64,96,113])
# 8x7 for 1 frames
whiteheart = bytearray([14,31,63,126,127,63,31,14])
# 11x13 for 1 frames
sparkleybig = bytearray([191,255,191,255,191,10,191,255,191,255,191,31,31,31,31,31,10,31,31,31,31,31])
# 11x13 for 1 frames
sparkleysmall = bytearray([255,255,191,255,191,11,191,255,191,255,255,31,31,31,31,31,26,31,31,31,31,31])
# 11x13 for 1 frames
sparkleybigblit = bytearray([64,0,64,0,64,245,64,0,64,0,64,0,0,0,0,0,21,0,0,0,0,0])
# 11x13 for 1 frames
sparkleysmallblit = bytearray([0,0,64,0,64,244,64,0,64,0,0,0,0,0,0,0,5,0,0,0,0,0])
# 44x13 for 1 frames
sparkleattack = bytearray([64,0,64,0,64,245,64,0,64,0,64,0,0,64,0,64,244,64,0,64,0,0,0,0,0,0,64,240,64,0,0,0,0,0,0,0,0,0,64,0,0,0,0,0,0,0,0,0,0,21,0,0,0,0,0,0,0,0,0,0,5,0,0,0,0,0,0,0,0,0,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0])
SkySets = [
    bytearray([255,127,127,127,63,191,191,223,207,239,119,247,119,247,119,247,119,247,239,239,247,247,119,247,123,251,91,251,91,187,83,243,83,179,119,247,247,143,191,191,191,191,191,191,127,127,127,255,14,13,13,13,9,11,9,11,9,11,9,7,5,3,5,7,5,3,5,7,5,3,5,7,5,3,5,7,5,3,5,7,5,3,5,7,5,11,9,11,9,11,9,11,13,13,13,14]),
    bytearray([255,255,255,255,191,31,95,95,79,239,239,247,247,251,251,251,251,251,251,251,247,247,251,251,251,253,253,253,253,253,253,249,249,249,251,251,187,231,175,239,239,175,239,95,95,191,255,255,15,15,15,15,15,15,15,15,14,14,14,14,14,14,13,13,13,13,13,13,12,13,13,12,13,13,12,13,13,12,13,13,13,12,13,13,13,14,14,14,14,14,14,15,15,15,15,15]),
    bytearray([255,255,255,255,255,255,127,127,63,191,223,223,223,239,239,239,239,239,239,223,239,239,239,247,247,247,247,231,239,239,239,239,239,159,191,191,191,191,127,127,255,255,255,255,255,255,255,255,15,15,15,15,15,14,12,13,13,13,13,13,13,11,11,11,11,11,11,11,11,11,11,11,9,11,11,10,9,10,11,9,10,13,13,13,13,13,13,13,14,15,15,15,15,15,15,15])
]
#Expensive Boss Sequence
# 72x40 for 1 frames
Boss0 = bytearray([56,12,0,192,240,248,252,254,31,7,3,49,96,48,0,0,0,0,128,192,224,240,240,248,120,60,60,28,30,142,142,143,207,199,199,199,195,67,67,67,67,195,195,131,131,131,131,7,7,7,15,15,31,63,127,255,254,252,248,240,224,192,128,1,115,67,67,70,126,56,0,0,0,0,254,255,255,255,15,0,0,0,0,0,0,192,240,252,62,31,7,3,3,1,225,240,120,28,6,7,3,1,1,1,0,0,224,184,8,4,68,196,8,16,32,192,128,1,3,3,7,14,28,56,112,224,192,0,1,3,15,31,63,255,255,255,254,248,128,28,54,98,72,72,0,0,127,255,255,255,128,0,0,0,0,0,0,255,255,248,128,0,0,0,0,0,127,225,192,128,0,0,0,60,14,142,140,252,48,1,2,2,2,1,0,0,0,129,255,254,60,0,0,0,0,0,0,1,199,254,248,0,0,0,0,0,15,255,255,255,255,254,0,192,198,140,48,32,0,3,31,127,255,254,248,240,224,192,128,0,3,7,15,30,60,56,120,112,96,192,193,193,195,195,195,195,195,195,193,192,192,192,224,224,240,112,56,60,30,15,7,0,0,0,128,192,224,240,124,62,15,3,0,0,0,0,0,128,192,255,255,255,255,99,112,48,1,3,62,99,65,3,2,14,248,3,7,15,31,127,255,254,156,24,56,112,224,192,192,128,128,24,48,24,0,128,192,96,97,97,49,49,49,48,48,48,56,24,24,24,12,12,6,6,131,131,129,193,248,248,254,238,194,238,224,240,248,252,254,255,255,255,247,251,219,193,131,6,0,1])
# 72x40 for 1 frames
Boss1 = bytearray([0,0,0,0,128,192,32,48,48,48,48,48,112,96,224,192,198,138,8,24,16,8,8,136,232,248,248,124,62,31,15,7,3,193,192,240,248,252,30,7,3,1,0,128,248,252,6,3,3,3,7,7,15,254,248,192,128,249,253,221,29,125,57,1,129,131,135,207,255,126,124,56,0,0,0,0,1,6,4,0,128,128,128,128,128,128,128,1,3,3,7,7,134,206,238,255,127,63,31,0,0,0,0,192,255,255,127,3,1,0,124,126,207,135,6,3,1,0,112,252,158,142,134,6,28,60,231,131,163,243,99,7,254,254,254,223,207,231,231,199,4,6,0,0,0,0,0,0,0,252,134,3,1,0,0,128,192,0,1,193,113,31,126,255,15,1,0,0,0,0,126,255,255,7,7,1,1,0,0,0,0,0,0,0,193,255,127,0,3,14,24,48,113,97,231,227,224,240,248,253,125,28,14,79,231,231,198,70,14,60,248,241,131,6,0,0,0,0,0,0,0,0,1,1,1,2,131,129,0,0,0,7,4,4,0,7,15,156,24,56,240,224,0,7,31,30,56,112,224,192,128,0,0,0,0,15,31,31,188,176,240,112,0,0,0,192,224,112,48,48,56,56,56,60,60,60,113,243,225,224,224,126,35,57,121,226,0,0,0,0,0,0,0,0,12,14,2,1,1,7,12,24,48,32,96,64,192,192,96,33,49,17,17,48,120,24,24,24,24,28,28,31,15,0,0,0,56,240,224,192,128,140,140,152,24,24,24,14,135,128,192,192,240,248,252,230,206,222,204,224,255,255,253,248,243,255,246,192,130,0])
# 72x40 for 1 frames
Boss2 = bytearray([0,248,12,244,4,148,4,244,4,164,132,244,148,148,148,148,148,148,148,148,244,4,248,0,0,0,0,0,224,32,224,0,0,192,192,240,248,252,30,7,3,1,0,128,248,252,6,3,3,3,7,7,15,254,248,192,128,128,240,216,25,49,1,1,129,131,231,255,255,126,252,248,0,1,3,2,62,2,142,2,6,254,2,254,6,2,254,2,30,70,2,6,254,2,1,0,0,0,0,0,3,2,6,194,255,255,127,3,1,128,0,128,1,3,2,3,1,0,0,0,0,0,0,0,0,248,31,7,31,255,31,7,30,254,254,255,255,255,255,255,221,55,205,3,128,192,224,224,225,112,112,112,96,225,224,192,0,0,5,0,0,0,0,0,81,0,0,0,0,0,14,1,1,3,3,1,1,0,0,0,0,1,3,1,0,0,0,0,0,8,24,48,112,96,224,96,96,113,255,252,255,255,31,252,255,223,247,223,255,255,255,255,187,103,152,0,7,3,1,128,128,196,198,198,204,136,15,7,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,30,158,222,222,223,223,159,191,63,127,255,255,255,255,123,230,25,0,252,126,15,7,3,1,33,49,29,7,15,4,0,0,0,3,6,3,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,128,192,240,255,255,255,255,255,255,255,255,254,240,247,255,255,247,204,179,0])
# 72x40 for 1 frames
Boss3 = bytearray([0,248,12,244,4,148,4,244,4,164,132,244,148,148,148,148,148,148,148,148,148,148,148,148,148,148,148,244,4,248,0,0,0,0,120,252,196,196,192,192,64,96,32,48,56,28,12,14,135,131,131,131,129,129,129,129,129,49,249,249,249,217,153,57,19,131,131,131,199,255,254,248,0,1,3,2,2,46,2,6,14,2,6,30,126,6,14,254,2,126,6,254,2,6,94,2,2,6,62,2,2,1,0,0,0,56,110,67,193,0,0,0,0,192,224,240,60,30,14,7,7,3,3,3,7,255,31,63,31,255,31,63,31,255,255,255,255,255,255,255,223,55,207,3,0,128,224,120,60,30,14,30,124,96,64,6,12,6,0,0,0,0,0,1,0,0,0,0,0,0,10,0,0,0,0,3,2,2,3,1,1,0,0,0,7,31,63,32,48,16,28,7,129,195,224,96,96,113,255,252,255,255,31,252,255,255,223,255,255,255,255,255,187,103,152,0,30,31,135,192,224,112,48,56,56,248,240,160,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,4,6,3,0,0,0,0,0,30,254,126,254,127,255,63,254,31,31,62,127,255,255,123,230,25,0,56,28,31,15,3,0,0,0,6,3,3,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,128,192,240,225,192,249,192,193,248,224,248,255,248,240,255,255,247,204,179,0])
##############################################################
########### Game Animation Functions #########################
##############################################################
gc.collect

def drawOpening():
    #Title of Fake Companies
    thumby.display.brightness(50)
    thumby.display.setFPS(1)
    thumby.display.fill(1)
    thumby.display.update()
    thumby.display.setFont("/lib/font3x5.bin", 3, 5, 0)
    thumby.display.drawText("(c) '95, Xintendo", 5, 10, 0)
    thumby.display.update()
    thumby.display.drawText("(c) '95, Creaturesinc", 5, 16, 0)
    thumby.display.update()
    thumby.display.drawText("(c) '95, GAME XREAK", 5, 23, 0)
    thumby.display.update()
    thumby.display.fill(0)    
    thumby.display.update()
    #Classic Xokemon Opening from Xameboy
    thumby.display.drawFilledRectangle(15, 10, 40, 20, 1)  
    thumby.display.blit(FreakLogo, 32, 10, 5, 9, 1, 0, 0)
    thumby.display.drawText("GAME XREAK", 20, 21, 0)
    thumby.display.setFPS(10)
    thumby.display.update()
    thumby.display.blit(starmask, 60, 5, 12, 10, 0, 0, 0)
    thumby.audio.playBlocking(430, 100)
    thumby.display.update()
    thumby.display.blit(starblack, 60, 5, 12, 10, 1, 0, 0)
    thumby.audio.playBlocking(566, 50)
    thumby.display.update()
    thumby.display.blit(starwhite, 50, 10, 12, 10, 1, 0, 0)
    thumby.display.blit(starmask, 50, 10, 12, 10, 0, 0, 0)
    thumby.audio.playBlocking(615, 100)
    thumby.display.update()
    thumby.display.blit(starwhite, 40, 20, 12, 10, 1, 0, 0)
    thumby.display.blit(starmask, 40, 20, 12, 10, 0, 0, 0)
    thumby.audio.playBlocking(794, 125)
    thumby.display.update()
    thumby.display.blit(starwhite, 30, 25, 12, 10, 1, 0, 0)
    thumby.display.blit(starmask, 30, 25, 12, 10, 0, 0, 0)
    thumby.audio.playBlocking(540, 200)
    thumby.display.update()
    thumby.display.blit(starmask, 20, 30, 12, 10, 0, 0, 0)
    thumby.audio.playBlocking(370, 100)
    thumby.display.update()
    thumby.display.setFPS(5)
    thumby.display.fill(0) 
    thumby.display.drawFilledRectangle(15, 10, 40, 20, 1) 
    thumby.display.blit(FreakLogo, 32, 10, 5, 9, 1, 0, 0)
    thumby.display.drawText("GAME FREAK", 20, 21, 0)
    thumby.display.update()
    thumby.display.blit(hazeblit, 20, 30, 23, 3, 0, 1, 1)
    thumby.display.blit(hazeblit, 30, 30, 23, 3, 0, 1, 1)
    thumby.display.update()
    thumby.display.blit(hazeblit, 25, 32, 23, 3, 0, 0, 1)
    thumby.display.update()
    #Mimic a classic opening sequence
    brightness = 1
    thumby.display.setFPS(30)
    thumby.display.fill(1) # fill screen with white pixels
    opensequence=True
    while(opensequence):
        thumby.display.brightness(brightness)
        thumby.display.update()
        brightness += 1
        if brightness >= 127:
            brightness = 1
            opensequence = False
    thumby.display.update()
    #Xintendo Drop
    #I believe the classic Ding plays C1 to C7 as a sound test
    thumby.display.update()
    thumby.display.setFont("/lib/font8x8.bin", 8, 8, 0)
    thumby.display.setFPS(2)
    thumby.display.fill(1)
    thumby.display.drawText("Xintendo", 5, 0, 0)
    thumby.display.update()
    thumby.display.fill(1)
    thumby.display.drawText("Xintendo", 5, 10, 0)
    thumby.display.update()
    thumby.display.fill(1)
    thumby.display.drawText("Xintendo", 5, 15, 0)
    thumby.display.update()
    thumby.display.fill(1)
    thumby.display.drawText("Xintendo", 5, 15, 0)
    thumby.display.update()
    looper=True
    mover=0

def drawGameTitleScreen():
 # (sprite, xPosition, yPosition, width, height, key, XMirror, YMirror)
    thumby.display.blit(GameTitle, 2, 10 - (mover * 2), 69, 36, 1, 0, 0)
    thumby.display.drawText("Vol. 1.", 140 - (mover * 5), 10, 0)
    thumby.display.drawText("Coco Clouds", 140 - (mover * 5), 16, 0)
    thumby.display.blit(haze, 10 + mover, y_position - 140, 23, 3, 1, 0, 0)
    thumby.display.blit(haze, 40 - mover, y_position - 140, 23, 3, 1, 1, 0)
    thumby.display.blit(Xirbystarsmall, 135 - (mover * 6), 10, 16, 16, 1, 0, 0)
    thumby.display.blit(SkySets[0], -10, y_position - 120, 48, 12, 1, 0, 0)
    thumby.display.blit(SkySets[0], 40, y_position - 110, 48, 12, 1, 1, 0)
    thumby.display.blit(Xirbystarsmall, (-205) + (mover * 5), 10, 16, 16, 1, 1, 0)
    thumby.display.blit(SkySets[1], 5, y_position - 80, 48, 12, 1, 0, 0)
    thumby.display.blit(SkySets[2], 30, y_position - 70, 48, 12, 1, 1, 0)
    thumby.display.blit(enemySprite, (500) - (mover * 5), 10, 16, 16, 1, 0, 0)
    thumby.display.blit(Xirbyumbrella, 300 - (mover * 2), y_position - 70, 25, 30, 1, 0, 0)
    thumby.display.blit(starwhite, 45, y_position - 40, 12, 10, 1, 0, 0)
    thumby.display.blit(starwhite, 60, y_position - 25, 12, 10, 1, 1, 0)
    thumby.display.blit(starwhite, 2, y_position - 30, 12, 10, 1, 0, 0)
    thumby.display.drawText("Original Music", 15, y_position - 25, 0)
    thumby.display.drawText(" Art Design", 15, y_position - 15, 0)
    thumby.display.drawText("   Code", 15, y_position - 5, 0)
    thumby.display.drawText(" ~ S A R A H  B A S S ~ ", 0, y_position + 5, 0)
    thumby.display.blit(moon, 50, y_position + 15, 20, 23, 1, 1, 0)
    thumby.display.drawText(" E N J O Y ~ ! ", 15, y_position + 30, 0)

def draw_background(scene, mover2):
    if scene == 0:
        return [
            {"sprite": SkySets[0], "x": 10 - mover2, "y": 5, "width": 48, "height": 12, "key": 1, "xMirror": 0, "yMirror": 0},
            {"sprite": SkySets[1], "x": 50 - mover2, "y": 20, "width": 48, "height": 12, "key": 1, "xMirror": 0, "yMirror": 0},
            {"sprite": SkySets[2], "x": 30 - mover2, "y": 1, "width": 48, "height": 12, "key": 1, "xMirror": 0, "yMirror": 0},
            {"sprite": SkySets[0], "x": 70 - mover2, "y": 5, "width": 48, "height": 12, "key": 1, "xMirror": 0, "yMirror": 0},
            {"sprite": SkySets[1], "x": 120 - mover2, "y": 20, "width": 48, "height": 12, "key": 1, "xMirror": 0, "yMirror": 0},
            {"sprite": SkySets[2], "x": 100 - mover2, "y": 1, "width": 48, "height": 12, "key": 1, "xMirror": 0, "yMirror": 0},
            {"sprite": SkySets[0], "x": 72 - (mover2 * 2), "y": 5, "width": 48, "height": 12, "key": 1, "xMirror": 1, "yMirror": 0},
            {"sprite": SkySets[1], "x": 140 - (mover2 * 3), "y": 20, "width": 48, "height": 12, "key": 1, "xMirror": 1, "yMirror": 0},
            {"sprite": SkySets[2], "x": 95 - (mover2 * 2), "y": 1, "width": 48, "height": 12, "key": 1, "xMirror": 1, "yMirror": 0},
            {"sprite": haze, "x": 1 - mover2, "y": 1, "width": 23, "height": 3, "key": 1, "xMirror": 0, "yMirror": 0},
            {"sprite": haze, "x": 1 - mover2, "y": 40, "width": 23, "height": 3, "key": 1, "xMirror": 1, "yMirror": 0},
            {"sprite": haze, "x": 110 - mover2, "y": 40, "width": 23, "height": 3, "key": 1, "xMirror": 1, "yMirror": 0},
            {"sprite": haze, "x": 20 - (mover2 * 2), "y": 20, "width": 23, "height": 3, "key": 1, "xMirror": 1, "yMirror": 0},
            {"sprite": haze, "x": 80 - (mover2 * 2), "y": 20, "width": 23, "height": 3, "key": 1, "xMirror": 0, "yMirror": 0},
            {"sprite": haze, "x": 1 - mover2, "y": 35, "width": 23, "height": 3, "key": 1, "xMirror": 1, "yMirror": 0},
            {"sprite": haze, "x": 120 - (mover2 * 2), "y": 5, "width": 23, "height": 3, "key": 1, "xMirror": 1, "yMirror": 0},
            {"sprite": haze, "x": 140 - (mover2 * 2), "y": 15, "width": 23, "height": 3, "key": 1, "xMirror": 0, "yMirror": 1},
            {"sprite": haze, "x": 160 - (mover2 * 2), "y": 25, "width": 23, "height": 3, "key": 1, "xMirror": 1, "yMirror": 1},
            {"sprite": starwhite, "x": 72 - mover2, "y": 10, "width": 12, "height": 10, "key": 1, "xMirror": 0, "yMirror": 0},
            {"sprite": starmask, "x": 72 - mover2, "y": 10, "width": 12, "height": 10, "key": 0, "xMirror": 0, "yMirror": 0},
            {"sprite": starblack, "x": 50 - (mover2 * 2), "y": -50 + (mover2 * 2), "width": 12, "height": 10, "key": 1, "xMirror": 0, "yMirror": 0}
        ]
    elif scene == 1:
        return [
            {"sprite": SkySets[0], "x": 72 - mover2, "y": 5, "width": 48, "height": 12, "key": 1, "xMirror": 0, "yMirror": 0},
            {"sprite": SkySets[1], "x": 100 - (mover2 * 2), "y": 20, "width": 48, "height": 12, "key": 1, "xMirror": 0, "yMirror": 0},
            {"sprite": SkySets[2], "x": 100 - mover2, "y": 1, "width": 48, "height": 12, "key": 1, "xMirror": 0, "yMirror": 0},
            {"sprite": haze, "x": 144 - (mover2 * 2), "y": 20, "width": 23, "height": 3, "key": 0, "xMirror": 0, "yMirror": 0},
            {"sprite": haze, "x": 90 - (mover2 * 2), "y": 20, "width": 23, "height": 3, "key": 1, "xMirror": 0, "yMirror": 0},
            {"sprite": starblack, "x": 50 - (mover2 * 2), "y": -50 + (mover2 * 2), "width": 12, "height": 10, "key": 1, "xMirror": 0, "yMirror": 0}
        ]
    elif scene == 3:
         return [
            {"sprite": hazeblit, "x": 25, "y": 40-mover2, "width": 12, "height": 10, "key": 0, "xMirror": 1, "yMirror": 0},
            {"sprite": hazeblit, "x": 5, "y": 40-mover2, "width": 12, "height": 10, "key": 0, "xMirror": 0, "yMirror": 1},
            {"sprite": hazeblit, "x": 40, "y": 60-mover2, "width": 12, "height": 10, "key": 0, "xMirror": 1, "yMirror": 0},
            {"sprite": hazeblit, "x": 20, "y": 40-(mover2*2), "width": 12, "height": 10, "key": 0, "xMirror": 1, "yMirror": 0},
            {"sprite": hazeblit, "x": 10, "y": 50-mover2, "width": 12, "height": 10, "key": 0, "xMirror": 0, "yMirror": 0},
            {"sprite": hazeblit, "x": 50, "y": 50-(mover2*2), "width": 12, "height": 10, "key": 0, "xMirror": 0, "yMirror": 1},
            {"sprite": hazeblit, "x": 20, "y": 60-mover2, "width": 12, "height": 10, "key": 0, "xMirror": 1, "yMirror": 0},
            {"sprite": hazeblit, "x": 60, "y": 70-mover2, "width": 12, "height": 10, "key": 0, "xMirror": 0, "yMirror": 0},
            {"sprite": hazeblit, "x": 50, "y": 80-(mover2*2), "width": 12, "height": 10, "key": 0, "xMirror": 0, "yMirror": 1},
            {"sprite": hazeblit, "x": 40, "y": 60-mover2, "width": 12, "height": 10, "key": 0, "xMirror": 0, "yMirror": 0},
            {"sprite": hazeblit, "x": 20, "y": 80-(mover2*2), "width": 12, "height": 10, "key": 0, "xMirror": 1, "yMirror": 0},
            {"sprite": hazeblit, "x": 10, "y": 90-mover2*2, "width": 12, "height": 10, "key": 0, "xMirror": 0, "yMirror": 0},
            {"sprite": hazeblit, "x": 50, "y": 100-(mover2*2), "width": 12, "height": 10, "key": 0, "xMirror": 0, "yMirror": 1},
            {"sprite": sparkleysmallblit, "x": 50, "y": 100-(mover2*2), "width": 11, "height": 13, "key": 0, "xMirror": 0, "yMirror": 1},
            {"sprite": sparkleybigblit, "x": 50, "y": 100-(mover2*2), "width": 11, "height": 13, "key": 0, "xMirror": 0, "yMirror": 1},
            {"sprite": sparkleysmallblit, "x": 10, "y": 100-(mover2*2), "width": 11, "height": 13, "key": 0, "xMirror": 0, "yMirror": 1},
            {"sprite": sparkleybigblit, "x": 30, "y": 100-(mover2*2), "width": 11, "height": 13, "key": 0, "xMirror": 0, "yMirror": 1},
            {"sprite": sparkleysmallblit, "x": 60, "y": 120-(mover2*2), "width": 11, "height": 13, "key": 0, "xMirror": 0, "yMirror": 1},
            {"sprite": sparkleybigblit, "x": 50, "y": 140-(mover2*2), "width": 11, "height": 13, "key": 0, "xMirror": 0, "yMirror": 1},
            {"sprite": sparkleysmallblit, "x": 10, "y": 150-(mover2*2), "width": 11, "height": 13, "key": 0, "xMirror": 0, "yMirror": 1},
            {"sprite": sparkleybigblit, "x": 0, "y": 160-(mover2*2), "width": 11, "height": 13, "key": 0, "xMirror": 0, "yMirror": 1},
            {"sprite": sparkleysmallblit, "x": 20, "y": 170-(mover2*2), "width": 11, "height": 13, "key": 0, "xMirror": 0, "yMirror": 1},
            {"sprite": sparkleybigblit, "x": 35, "y": 180-(mover2*2), "width": 11, "height": 13, "key": 0, "xMirror": 0, "yMirror": 1},
            {"sprite": sparkleysmallblit, "x": 55, "y": 200-(mover2*2), "width": 11, "height": 13, "key": 0, "xMirror": 0, "yMirror": 1},
            {"sprite": sparkleybigblit, "x": 35, "y": 220-(mover2*2), "width": 11, "height": 13, "key": 0, "xMirror": 0, "yMirror": 1},
            {"sprite": sparkleysmallblit, "x": 65, "y": 240-(mover2*2), "width": 11, "height": 13, "key": 0, "xMirror": 0, "yMirror": 1},
            {"sprite": sparkleybigblit, "x": 0, "y": 250-(mover2*2), "width": 11, "height": 13, "key": 0, "xMirror": 0, "yMirror": 1},
            {"sprite": sparkleysmallblit, "x": 62, "y": 260-(mover2*2), "width": 11, "height": 13, "key": 0, "xMirror": 0, "yMirror": 1},
            {"sprite": sparkleybigblit, "x": 52, "y": 280-(mover2*2), "width": 11, "height": 13, "key": 0, "xMirror": 0, "yMirror": 1}
        ]
    elif scene == 5:
             return [
            {"sprite": SkySets[0], "x": 25, "y": 40-mover2, "width": 48, "height": 12, "key": 1, "xMirror": 1, "yMirror": 0},
            {"sprite": SkySets[1], "x": 5, "y": 40-mover2, "width": 48, "height": 12, "key": 1, "xMirror": 0, "yMirror": 1},
            {"sprite": SkySets[2], "x": 40, "y": 60-mover2, "width": 48, "height": 12, "key": 1, "xMirror": 1, "yMirror": 0},
            {"sprite": SkySets[0], "x": 20, "y": 40-(mover2*2), "width": 48, "height": 12, "key": 1, "xMirror": 1, "yMirror": 0},
            {"sprite": SkySets[1], "x": 10, "y": 50-mover2, "width": 48, "height": 12, "key": 1, "xMirror": 0, "yMirror": 0},
            {"sprite": SkySets[2], "x": 50, "y": 50-(mover2*2), "width": 48, "height": 12, "key": 1, "xMirror": 0, "yMirror": 1},
            {"sprite": SkySets[0], "x": 20, "y": 60-mover2, "width": 48, "height": 12, "key": 1, "xMirror": 1, "yMirror": 0},
            {"sprite": SkySets[1], "x": 60, "y": 70-mover2, "width": 48, "height": 12, "key": 1, "xMirror": 0, "yMirror": 0},
            {"sprite": SkySets[2], "x": 50, "y": 80-(mover2*2), "width": 48, "height": 12, "key": 1, "xMirror": 0, "yMirror": 1},
            {"sprite": blackheart, "x": 65, "y": 150-(mover2*2), "width": 8, "height": 7, "key": 1, "xMirror": 0, "yMirror": 0},
            {"sprite": starblack, "x": 20, "y": 80-(mover2*2), "width": 12, "height": 10, "key": 1, "xMirror": 1, "yMirror": 0},
            {"sprite": enemySprite, "x": 1, "y":110-(mover2*2), "width": 16, "height": 16, "key": 1, "xMirror": 0, "yMirror": 0},
            {"sprite": blackheart, "x": 50, "y": 100-(mover2*2), "width": 8, "height": 7, "key": 1, "xMirror": 0, "yMirror": 0},
            {"sprite": sparkleysmall, "x": 50, "y": 100-(mover2*2), "width": 11, "height": 13, "key": 1, "xMirror": 0, "yMirror": 1},
            {"sprite": sparkleybig, "x": 50, "y": 100-(mover2*2), "width": 11, "height": 13, "key": 1, "xMirror": 0, "yMirror": 1},
            {"sprite": sparkleysmall, "x": 10, "y": 100-(mover2*2), "width": 11, "height": 13, "key": 1, "xMirror": 0, "yMirror": 1},
            {"sprite": sparkleybig, "x": 30, "y": 100-(mover2*2), "width": 11, "height": 13, "key": 1, "xMirror": 0, "yMirror": 1},
            {"sprite": sparkleysmall, "x": 60, "y": 120-(mover2*2), "width": 11, "height": 13, "key": 1, "xMirror": 0, "yMirror": 1},
            {"sprite": sparkleybig, "x": 50, "y": 140-(mover2*2), "width": 11, "height": 13, "key": 1, "xMirror": 0, "yMirror": 1},
            {"sprite": sparkleysmall, "x": 10, "y": 150-(mover2*2), "width": 11, "height": 13, "key": 1, "xMirror": 0, "yMirror": 1},
            {"sprite": sparkleybig, "x": 0, "y": 160-(mover2*2), "width": 11, "height": 13, "key": 1, "xMirror": 0, "yMirror": 1},
            {"sprite": sparkleysmall, "x": 20, "y": 170-(mover2*2), "width": 11, "height": 13, "key": 1, "xMirror": 0, "yMirror": 1},
            {"sprite": sparkleybig, "x": 35, "y": 180-(mover2*2), "width": 11, "height": 13, "key": 1, "xMirror": 0, "yMirror": 1},
            {"sprite": sparkleysmall, "x": 55, "y": 200-(mover2*2), "width": 11, "height": 13, "key": 1, "xMirror": 0, "yMirror": 1},
            {"sprite": sparkleybig, "x": 35, "y": 220-(mover2*2), "width": 11, "height": 13, "key": 1, "xMirror": 0, "yMirror": 1},
            {"sprite": sparkleysmall, "x": 65, "y": 240-(mover2*2), "width": 11, "height": 13, "key": 1, "xMirror": 0, "yMirror": 1},
            {"sprite": sparkleybig, "x": 0, "y": 250-(mover2*2), "width": 11, "height": 13, "key": 1, "xMirror": 0, "yMirror": 1},
            {"sprite": sparkleysmall, "x": 62, "y": 260-(mover2*2), "width": 11, "height": 13, "key": 1, "xMirror": 0, "yMirror": 1},
            {"sprite": sparkleybig, "x": 10, "y": 280-(mover2*2), "width": 11, "height": 13, "key": 1, "xMirror": 0, "yMirror": 1}
        ]

def update_background(scene, mover2):
    sprites_positions = draw_background(scene, mover2)
    for item in sprites_positions:
        thumby.display.blit(item["sprite"], item["x"], item["y"], item["width"], item["height"], item["key"], item["xMirror"], item["yMirror"])

def update_MenuScreen(secret, level):
    thumby.display.fill(1)
    thumby.display.setFont("/lib/font3x5.bin", 3, 5, 0)
    if level==5:
        thumby.display.drawText("~~ G A M E O V E R ~~", 1,5, 0)
        thumby.display.drawText("    P r e s s  B  ", 1,15, 0)
    elif secret == True:
        thumby.display.drawText("S e c r e t C o d e", 1,1, 0)
        thumby.display.drawText("P R E S S  B ", 1,10, 0)
        thumby.display.drawText("S u p e r  M o d e", 1,20, 0)
        thumby.display.blit(moon, 50, 8, 20, 23, 1, 1, 0)
    else:    
        thumby.display.drawText("~~ P L A Y  G U I D E ~~", 1,5, 0)
        thumby.display.drawText("H E A R T S : " + str(hearts)+ " / 3 5", 1,15, 0)
        thumby.display.drawText("L E V E L :" + str(level) , 1,22, 0)
            
        
# Function to check if the secret code has been entered
def check_secret_code():
    global button_press_sequence
    if button_press_sequence == secret_code_sequence:
        return True
    # Reset the sequence if it reaches length and is not a match
    elif len(button_press_sequence) > len(secret_code_sequence):
        button_press_sequence = []  
    return False    
    

def update_Boss(boss):
    thumby.display.fill(0)
    if boss == 0:
        thumby.display.blit(Boss0, 0, 0, 72, 40, 0, 0, 0)
    if boss == 1:
        thumby.display.blit(Boss1, 0, 0, 72, 40, 0, 0, 0)
    if boss == 2:
        thumby.display.blit(Boss2, 0, 0, 72, 40, 0, 0, 0)
    if boss == 3:
        thumby.display.blit(Boss3, 0, 0, 72, 40, 0, 0, 0)
 
def update_Hearts(Scene):
          #Draw Hearts (Kirby's Health)
    thumby.display.drawRectangle(5, 30, 60, 10, 0)
    thumby.display.drawFilledRectangle(6, 31, 58, 9, 1)
    if Scene==0:   
        thumby.display.blit(heart, 10, 32, 8, 7, 1, 0, 0)
        thumby.display.blit(heart, 20, 32, 8, 7, 1, 0, 0)
        thumby.display.blit(heart, 30, 32, 8, 7, 1, 0, 0)
        thumby.display.blit(heart, 40, 32, 8, 7, 1, 0, 0)
        thumby.display.blit(heart, 50, 32, 8, 7, 1, 0, 0)
    else:    
        thumby.display.blit(blackheart, 10, 32, 8, 7, 1, 0, 0)
        thumby.display.blit(blackheart, 20, 32, 8, 7, 1, 0, 0)
        thumby.display.blit(blackheart, 30, 32, 8, 7, 1, 0, 0)
        thumby.display.blit(blackheart, 40, 32, 8, 7, 1, 0, 0)
        thumby.display.blit(blackheart, 50, 32, 8, 7, 1, 0, 0)
        


#####################################################
########### ENEMY and XIRBY #########################
#####################################################

#When Collide inflict Health
#Black Hearts
class Item:
    def __init__(self, width=8, height=7):
        self.x = 72
        self.y = itemSpawn[0]
        self.width = width
        self.height = height

    def check_collision(self, xirby):
        return (
            self.x < xirby.x + xirby.width and
            self.x + self.width > xirby.x and
            self.y < xirby.y + xirby.height and
            self.y + self.height > xirby.y)


#When Collide inflict Damage. 
#Stars are used instead of the original 16x16 enemy designed becuase of screen size issues
#White and Black Stars used for different backgrounds
class Enemy:
    def __init__(self, width=12, height=10):
        self.x = 72
        self.y = enemySpawn[0]
        self.width = width
        self.height = height

    def check_collision(self, xirby):
        return (
            self.x < xirby.x + xirby.width and
            self.x + self.width > xirby.x and
            self.y < xirby.y + xirby.height and
            self.y + self.height > xirby.y)


class Xirby:
    def __init__(self, width=16, height=16):
        self.width = width
        self.height = height
        self.x = int((thumby.display.width / 2) - (width / 2))
        self.y = int((thumby.display.height / 2) - (height / 2))
        self.health = 0 # x value of rectangle
        #White Healthbar starts at (6, 31) then covers hearts as it's drawn longer
        #thumby.display.drawFilledRectangle(6, 31, 58-damage, 9, 1)
        #When healthbar reaches 58 length, Game Over (Scene= 5)

    def take_damage(self, damage=1):
        self.health += damage
        
    def take_health(self, healing=1):
        self.health -= healing    

xirby = Xirby()
enemy = Enemy()
item = Item()
item2 = Item()

#-=x=-=x=-=x=-=x=-=x=-=x=-=x=-=x=-=x=-=x=-=x=-=x=-=x=-=x=-=x=--=x=
#                        OPENING SEQUENCE                         # 
#-=x=-=x=-=x=-=x=-=x=-=x=-=x=-=x=-=x=-=x=-=x=-=x=-=x=-=x=-=x=--=x=

#######################
# START TitleScreen   #
#######################

#Title Screen is used to give player chance to enter secret code
#up,up,down,down,left,right,left,right,b,a (select start) 
#Many of the old games had Title Credits instead of end credits for Debugging
#I used this code to debug my game and jump to the levels I needed

gc.collect() 
drawOpening()
gc.collect() 
thumby.display.setFPS(5)
thumby.display.setFont("/lib/font3x5.bin", 3, 5, 0)
thumby.display.setFPS(10)
while looper:
    thumby.display.fill(1)
    t0 = utime.ticks_us() # Check the time
    PlayMusic(t0 - BGMOffset, SongList1)
    y_position = 197 - mover
    if y_position >= 0:
        drawGameTitleScreen()
        if D.pressed() or U.pressed():
            thumby.display.setFPS(40)
        if R.pressed() or L.pressed():
            thumby.display.setFPS(10)    
        if U.justPressed():
            button_press_sequence.append("U")
        elif D.justPressed():
            button_press_sequence.append("D")
        elif L.justPressed():
            button_press_sequence.append("L")
        elif R.justPressed():
            button_press_sequence.append("R")
        elif B.justPressed():
            button_press_sequence.append("B")
        elif A.justPressed():
            button_press_sequence.append("A")
        if check_secret_code() == True:
            looper = False
            abutton=abutton+1
            GameRunning = True
            Scene == 0
        gc.collect()
        #print('Memory Free:', "{:,}".format(gc.mem_free()), 'bytes')
        #print('Memory Allocated:', "{:,}".format(gc.mem_alloc()), 'bytes')
        #print("Secret Code:",button_press_sequence)
        #print("check code:", check_secret_code())
        thumby.display.update()
    else:
        looper = False
        thumby.display.fill(1)
        gc.collect()
    mover += 1
    thumby.display.update()
while (abutton == 0):
    #print('Memory Free:', "{:,}".format(gc.mem_free()), 'bytes')
    #print('Memory Allocated:', "{:,}".format(gc.mem_alloc()), 'bytes')
    thumby.display.setFPS(10)
    gc.collect() 
    t0 = utime.ticks_us() # Check the time
    PlayMusic(t0 - BGMOffset, SongList2)
    Spr.setFrame(Spr.currentFrame+1)
    thumby.display.drawSprite(Spr)
    thumby.display.setFont("/lib/font3x5.bin", 3, 5, 0)
    thumby.display.drawText("Vol 1.", 1,2, 0)
    thumby.display.drawText("CocoClouds", 1,10, 0)
    thumby.display.setFont("/lib/font5x7.bin", 5, 7, 0)
    thumby.display.drawText("PRESS START", 5,32, 0)
    thumby.display.update()
    if A.pressed():
        abutton=abutton+1
        GameRunning = True
    thumby.display.update()

#######################
# STOP TitleScreen    #
#######################
    
    
#-=x=-=x=-=x=-=x=-=x=-=x=-=x=-=x=-=x=-=x=-=x=-=x=-=x=-=x=-=x=--=x=
#                        START OF GAME                           # 
#-=x=-=x=-=x=-=x=-=x=-=x=-=x=-=x=-=x=-=x=-=x=-=x=-=x=-=x=-=x=--=x=
thumby.display.setFPS(10)
secret = check_secret_code()
#xirbySprite = Xirbystarsmall
while GameRunning:
    thumby.display.setFPS(gamespeed)
    thumby.display.fill(1)
    t0 = utime.ticks_us() 
    mover2+=1
    
    #Step 1: update variables, check time, and iterate values
    
    #Step 2:
    #The Following Code calls the Background Layers
    #It also uses if statements to control gameplay, music and controls
    #5 Layers of the background:
    #1.Fill Color Static
    #2.Moving Background (clear) Blit
    #3.Enemies and Items -Masked Blit
    #4.Health Meter - Masked Blit
    #5.Xirby in Foreground -Masked blit

    #Step 3:
    #Call Garbage Collect at end and Update

    
    if Scene == 0:
        PlayMusic(t0 - BGMOffset, SongList4)
        update_background(Scene, mover2)
        update_Hearts(Scene)
        xirby.heatlh=0
        hearts=0
        level=0
        if mover2 >= 160:
            mover2 = 0
            Scene = 1
            level=0
    elif Scene == 1:
        PlayMusic(t0 - BGMOffset, SongList3)
        update_background(Scene, mover2)
        update_Hearts(Scene)
        thumby.display.drawFilledRectangle(6, 31, xirby.health, 9, 1)     
        if xirby.health >= 58:
            Scene=5
            
        if mover2 >= 144:
            mover2 = 0
        
        level=1
            
        #Display Simple Heart
        thumby.display.blit(whiteheart, 100-(mover2*2),itemSpawn[hearts%11], item2.width, item2.height, 0, 0, 0)
        thumby.display.blit(heart, 100-(mover2*2),itemSpawn[hearts%11], item2.width, item2.height, 1, 0, 0)
        item2.x= 100-(mover2*2)
        item2.y = itemSpawn[hearts%11]   
        
        #Display Blip Heart
        if mover2%2==0:
            thumby.display.blit(whiteheart, 200-(mover2*3),itemSpawn[(5+hearts)%11], item.width, item.height, 0, 0, 0)
            thumby.display.blit(heart, 200-(mover2*3),itemSpawn[(5+hearts)%11], item.width, item.height, 1, 0, 0)
        else:
            thumby.display.blit(blackheart, 200-(mover2*3),itemSpawn[(5+hearts)%11], item.width, item.height, 1, 0, 0)
        item.x= 200-(mover2*3)
        item.y = itemSpawn[(5+hearts)%11]
            
        #Enemy Spawn
        #Bounce Attack - Black star 
        if hearts > 15 and Scene==1:
            thumby.display.blit(starblack, 300-(mover2*3), enemySpawn[(mover2%5)], enemy.width, enemy.height, 1, 0, 0)
            enemy.x = 300-(mover2*3)
            enemy.y= enemySpawn[(mover2%5)]
        else:
            thumby.display.blit(enemyMask, 300-(mover2*3)+stars-hearts, enemySpawn[(stars%5)], 16, 16, 0, 0, 0)
            thumby.display.blit(enemySprite, 300-(mover2*3)+stars-hearts, enemySpawn[(stars%5)], 16, 16, 1, 0, 0)
            enemy.x = 300-(mover2*3)+stars-hearts
            enemy.y= enemySpawn[(stars%5)]        
            
            #change Scenes
        if hearts>=25 and xirby.health < 58:
            Scene=3
    elif Scene == 2:
        PlayMusic(t0 - BGMOffset, SongList5)
        update_MenuScreen(secret, level)
        update_Hearts(Scene)
        thumby.display.drawFilledRectangle(6, 31, xirby.health, 9, 1)          
    elif Scene == 3:
        secret=False
        thumby.display.fill(0)
        PlayMusic(t0 - BGMOffset, SongList4)
        update_background(Scene, mover2)
        update_Hearts(Scene)
        thumby.display.drawFilledRectangle(6, 31, xirby.health, 9, 1)
        if xirby.health > 58:
            Scene=5
        if hearts>=35 and xirby.health < 58:
            Scene=4    
        if mover2 >= 144:
            mover2 = 0
        level=3
            
        thumby.display.blit(enemyMask,itemSpawnX[(10+stars)%15], 200-(mover2*4), 16, 16, 0, 0, 0)
        thumby.display.blit(enemySprite,itemSpawnX[(10+stars)%15], 200-(mover2*4), 16, 16, 1, 0, 0)
        enemy.y= 200-(mover2*4)
        enemy.x = itemSpawnX[(10+stars)%15]       
            
        thumby.display.blit(whiteheart,itemSpawnX[hearts%15],100-mover2*2, item2.width, item2.height, 0, 0, 0)
        item2.y= 100-(mover2*2)
        item2.x = itemSpawnX[(hearts%15)]   
        
        #Display Blip Heart
        if mover2%2==0:
            thumby.display.blit(whiteheart, itemSpawnX[(5+hearts)%15],140-(mover2*4), item.width, item.height, 0, 0, 0)
        else:
            thumby.display.blit(blackheart, itemSpawnX[(5+hearts)%15],140-(mover2*4), item.width, item.height, 1, 0, 0)
        item.y= 140-(mover2*4)
        item.x = itemSpawnX[(5+hearts)%15]
            

    elif Scene == 4:
        PlayMusic(t0 - BGMOffset, SongList2)
        gamespeed=14
        if xirby.health > 58:
            Scene=5
        if mover2 >= 144:
            mover2 = 0
            
        enemy.y=20
        enemy.x=60
            
        if mover2%10 == 1 or mover2%10 == 2 or mover2%10 == 3 or mover2%10 == 4:
            boss=2
        else:
            boss=3
        if attack == 1 and xirby.x >35:
            boss=1
            HP -=1
        if HP < 0:
            boss=0
            if  xirby.x >=50  or xirby.x <= 0 or xirby.y >= 50 or xirby.y <= -10:  
                Scene=5
        update_Boss(boss)
        
        thumby.display.blit(whiteheart,itemSpawnX[hearts%11],mover2*2, item2.width, item2.height, 0, 0, 0)
        item2.y= (mover2*2)
        item2.x = itemSpawn[hearts%11]   
         #Display Blip Heart
        if mover2%2==0:
            thumby.display.blit(whiteheart, itemSpawnX[(5+hearts)%15],(mover2*4), item.width, item.height, 0, 0, 0)
        else:
            thumby.display.blit(blackheart, itemSpawnX[(5+hearts)%15],(mover2*4), item.width, item.height, 1, 0, 0)

        if mover2%2==0:
            thumby.display.blit(whiteheart, itemSpawnX[(10+hearts)%15],(mover2*4), item.width, item.height, 0, 0, 0)
        else:
            thumby.display.blit(blackheart, itemSpawnX[(10+hearts)%15],(mover2*4), item.width, item.height, 1, 0, 0)
        
        level=4
        secret = False
    else: 
        #end screen
        thumby.display.fill(1)
        PlayMusic(t0 - BGMOffset, SongList6)
        update_background(Scene, mover2)
        thumby.display.drawRectangle(5, 30, 60, 10, 0)
        thumby.display.drawFilledRectangle(6, 31, 58, 9, 1)
        thumby.display.setFont("/lib/font3x5.bin", 3, 5, 0)
        thumby.display.drawText("G A M E  O V E R", 10,33, 0)
        Scene=5
        level=5
        xirby.health = 0
        if mover2 >= 144:
            mover2 = 0
        secret=True
        
        #Display fun hearts and stars
        thumby.display.blit(whiteheart, 100-(mover2*2),itemSpawn[hearts%11], item2.width, item2.height, 0, 0, 0)
        thumby.display.blit(heart, 100-(mover2*2),itemSpawn[hearts%11], item2.width, item2.height, 1, 0, 0)
        item2.x= 100-(mover2*2)
        item2.y = itemSpawn[hearts%11]   
        #Display Blip Heart
        if mover2%2==0:
            thumby.display.blit(whiteheart, 200-(mover2*3),itemSpawn[(5+hearts)%11], item.width, item.height, 0, 0, 0)
            thumby.display.blit(heart, 200-(mover2*3),itemSpawn[(5+hearts)%11], item.width, item.height, 1, 0, 0)
        else:
            thumby.display.blit(blackheart, 200-(mover2*3),itemSpawn[(5+hearts)%11], item.width, item.height, 1, 0, 0)
        item.x= 200-(mover2*3)
        item.y = itemSpawn[(5+hearts)%11]
            
        thumby.display.blit(starblack, 300-(mover2*3), enemySpawn[(mover2%5)], enemy.width, enemy.height, 1, 0, 0)
        enemy.x = 300-(mover2*3)
        enemy.y= enemySpawn[(mover2%5)]
              

   
  
    
        
    #Game Controls using Button Pad
    if Scene == 0 or Scene ==1 or Scene ==2:
        if  xirby.y >= 50 or xirby.y <= -10:
            xirby.x = xPosition
            xirby.y = yPosition
        if U.pressed():
                xirby.y -= (1 * speedup)
        if D.pressed():
                xirby.y += (1 * speedup)
        if R.pressed():
            gamespeed=30
            speedup=3
        if L.pressed():
            gamespeed=14
            speedup=1
        if A.pressed():
            Scene = 2
            xirby.x = xPosition
            xirby.y = yPosition
        if B.pressed():
            Scene = level
    if Scene == 3 or Scene == 4 or Scene==5:
        if  xirby.x >=50  or xirby.x <= 0 or xirby.y >= 50 or xirby.y <= -10:   
            xirby.x = xPosition
            xirby.y = yPosition
        if R.pressed():
            xirby.x += (3)
            turn=0
        if L.pressed():
            xirby.x -= (3)
            turn=1
        if U.pressed():
            xirby.y -=(5) 
        if D.pressed():
            xirby.y +=(5)
        if A.pressed():
            Scene = 2
            xirby.x = xPosition
            xirby.y = yPosition
            turn=0
            attack=0
        if B.pressed():
             attack=1
             turn=0
             if Scene !=5:
                Scene = level
             else: 
                Scene=0
    
                 
    ## DRAW XIRBY IN FOREGROUND ##
    if Scene != 2: 
        if secret == True:
            if mover2%4 == 0:
                thumby.display.blit(haze, xirby.x-10, xirby.y+10, 23, 3, 1, 0, 0)
                thumby.display.blit(sparkleysmall, xirby.x-17, xirby.y-10, 11, 13, 1, 0, 0)
            elif mover2%4 == 1:
                thumby.display.blit(haze, xirby.x-10,xirby.y+10, 25, 3, 1, 1, 0)
                thumby.display.blit(sparkleybig, xirby.x-17, xirby.y-10, 11, 13, 1, 0, 0)
            elif mover2%4 == 2:
                thumby.display.blit(haze, xirby.x-7, xirby.y+10, 23, 3, 1, 0, 1)
                thumby.display.blit(sparkleysmall, xirby.x+17, xirby.y+10, 11, 13, 1, 0, 0)
            elif mover2%4 == 3:
                thumby.display.blit(haze, xirby.x-9, xirby.y+10, 20, 3, 1, 1, 0)
                thumby.display.blit(sparkleysmall, xirby.x+17, xirby.y-10, 11, 13, 1, 0, 0)
            else:
                thumby.display.blit(sparkleysmall, xirby.x+10, xirby.y-10, 11, 13, 1, 0, 0)
        thumby.display.blit(Xirbymask,xirby.x, xirby.y, width, height, 0, 0, 0)
        if secret == False:    
            thumby.display.blit(Xirbystarsmall,xirby.x, xirby.y, width, height, 1, turn, 0)
            if attack==1:
                if mover2%4 == 0:
                    thumby.display.blit(sparkleattack,xirby.x, xirby.y,   11,      13,  0, 1, 0)
                if mover2%4 == 1:
                    thumby.display.blit(sparkleattack,xirby.x, xirby.y,   22,      13,  0, 1, 0)
                if mover2%4 == 2:
                    thumby.display.blit(sparkleattack,xirby.x, xirby.y,   33,      13,  0, 1, 0)
                if mover2%4 == 3:
                    thumby.display.blit(sparkleattack,xirby.x, xirby.y,   44,      13,  0, 1, 0)
                    attack=0
        if secret == True:
            if mover2%2 == 0:
                thumby.display.blit(Xirbystarsmall,xirby.x, xirby.y, width, height, 1, 0, 0)
            else:
                thumby.display.blit(Xirbystarblack,xirby.x, xirby.y, width, height, 1, 0, 0)
        
   ## Check for Collisions ##
   ##Animates the objects bouncing away from character with Flash Effects##
    if Scene !=2:
        if enemy.check_collision(xirby):
            #print("Collision detected!")
            if Scene !=5:
                xirby.take_damage()
            #print("health:",xirby.health)
            stars+=1
            if Scene== 1:
                thumby.display.blit(Xirbystarblack,xirby.x, xirby.y, width, height, 1, 0, 0)
                thumby.display.blit(starblack, xirby.x+15, xirby.y+10, enemy.width, enemy.height, 1, 0, 0)
                thumby.display.blit(starblack, xirby.x-17, xirby.y-10, enemy.width, enemy.height, 1, 0, 0)
            else:
                thumby.display.blit(Xirbymask,xirby.x, xirby.y, width, height, 0, 0, 0)
                thumby.display.blit(starwhite, xirby.x+15, xirby.y+10, enemy.width, enemy.height, 1, 0, 0)
                thumby.display.blit(starwhite, xirby.x-17, xirby.y-10, enemy.width, enemy.height, 1, 0, 0)    
       
        if item.check_collision(xirby) or item2.check_collision(xirby):
        
            if mover2%2 == 0:
                if Scene== 1:
                    thumby.display.blit(sparkleybig, xirby.x+15, xirby.y+10, 11, 13, 1, 0, 0)
                    thumby.display.blit(sparkleysmall, xirby.x-17, xirby.y-10, 11, 13, 1, 0, 0)
                else:
                    thumby.display.blit(sparkleybigblit, xirby.x+15, xirby.y+10, 11, 13, 0, 0, 0)
                    thumby.display.blit(sparkleysmallblit, xirby.x-17, xirby.y-10, 11, 13, 0, 0, 0)
            else:
                if Scene== 1:
                    thumby.display.blit(sparkleysmall, xirby.x+15,xirby.y+10, 11, 13, 0, 1, 0)
                    thumby.display.blit(sparkleybig, xirby.x-17, xirby.y-10, 11, 13, 0, 0, 0)
                else:
                    thumby.display.blit(sparkleysmallblit, xirby.x+15,xirby.y+10, 11, 13, 0, 1, 0)
                    thumby.display.blit(sparkleybigblit, xirby.x-17, xirby.y-10, 11, 13, 0, 0, 0)
            #print("Heart detected!")
            hearts+=1
            if Scene !=5 and xirby.health <= 0:
                xirby.take_health()
            #print ("hearts:",hearts)
            #print("health:",xirby.health)
        
    
    ###CLEAN and UPDATE ###    
    thumby.display.update()
    gc.collect() 
    #print('Memory Free:', "{:,}".format(gc.mem_free()), 'bytes')
    #print('Memory Allocated:', "{:,}".format(gc.mem_alloc()), 'bytes')
    #Runs at about 78,000 /138,000 which is good enough 

#BLANK SCREEN#
thumby.display.fill(0)
thumby.display.update()
gc.collect() 