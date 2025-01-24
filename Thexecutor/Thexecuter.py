# Thexecutor

# Soundboard type game featuring the sweet scifi sounds of the 80s and 90s.
# These sounds were common on various electonic toys and keychains
# such as the Executor and Echo Keyller.

# Sounds were extracted from this youtube video
# https://www.youtube.com/watch?v=iMzkV-mqoFI
# They were processed in Audacity to boost the volume and increase the pitch
# so that they are a little easier to hear on the Thumby. Encoding details
# are provided in the comments of audio.py

# Special thanks and credit to Transistortester for their audio engine which
# was developed for their Bad Apple demo

# Menu was inspired by Memory Match Thumby game by Ted Frazier

# Bitmaps for the menu were drawn by my 5th grade son. Got to get them while they are young.

# Written by Ace Geiger 2025

from sys import path as syspath
syspath.append("/Games/Thexecutor") #fix imports

import thumby
import audio
from time import sleep_ms
from os import listdir, stat #os.path.isfile doesn't exist in micropython

# Icons

# BITMAP: width: 14, height: 14
blaster = bytearray([80,240,208,208,240,208,208,240,208,208,208,240,240,0,
           0,0,0,0,0,0,7,4,5,14,16,16,31,0])

# BITMAP: width: 14, height: 14
assaultRifle = bytearray([7,13,27,55,238,220,184,112,224,192,128,0,0,0,
           0,0,0,0,15,9,11,15,63,35,35,63,0,0])

# BITMAP: width: 14, height: 14
freezeRay = bytearray([132,213,74,202,85,68,192,64,64,64,64,64,64,128,
            3,6,4,6,5,4,6,5,12,62,34,34,34,63])
           
# BITMAP: width: 14, height: 14
communicator = bytearray([0,0,0,255,8,136,72,40,72,136,72,248,0,0,
           0,0,0,63,37,36,60,36,36,60,44,63,0,0])

# BITMAP: width: 14, height: 14
analyzer = bytearray([48,200,132,66,33,17,145,145,17,33,66,132,200,48,
            0,1,2,14,17,41,36,36,41,17,14,2,1,0])

# BITMAP: width: 14, height: 14
bombsAway = bytearray([192,96,176,248,236,244,244,244,252,248,250,238,199,10,
            7,15,31,63,63,63,63,63,63,63,31,15,7,0])

# BITMAP: width: 14, height: 14
machineGun = bytearray([252,244,244,252,80,80,248,248,80,80,248,248,80,64,
            3,3,3,3,3,1,1,1,1,1,1,1,1,0])

# BITMAP: width: 14, height: 14
autoLaser = bytearray([0,240,8,104,104,8,240,8,240,8,255,248,255,240,
            0,0,1,1,1,1,0,1,0,1,1,1,1,0])

#set FPS
thumby.display.setFPS(25)

#initialize
startup = True
exit = False
playaudio = thumby.audio.enabled
table = [0, 0, 0, 0, 0, 0, 0, 0]
selectedSquare = 0# Top left
audioPath = "/Games/Thexecutor/assets/blaster.ima"
audioLoaded = False

#some constants
squareSize = 18
xPadding = 0
yPadding = 2

try:
    import emulator
    print("Emulator detected - audio disabled")
    playaudio = False
except ImportError:
    pass
        
def fullDisplayUpdate():
    thumby.display.fill(0)
    drawMenu()
    drawSelection()
    thumby.display.update()
    
def drawMenu():
    thumby.display.blit(blaster, 2, 4, 14, 14, 0, 0, 0)
    thumby.display.blit(assaultRifle, 20 , 4, 14, 14, 0, 0, 0)
    thumby.display.blit(freezeRay, 38, 4, 14, 14, 0, 0, 0)
    thumby.display.blit(communicator, 56, 4, 14, 14, 0, 0, 0)
    thumby.display.blit(analyzer, 2, 22, 14, 14, 0, 0, 0)
    thumby.display.blit(bombsAway, 20, 22, 14, 14, 0, 0, 0)
    thumby.display.blit(machineGun, 38, 22, 14, 14, 0, 0, 0)
    thumby.display.blit(autoLaser, 56, 22, 14, 14, 0, 0, 0)
    
def getPosition(square):  # Top left corner of the square
    tablePosition = [(square % 4) * squareSize, int(square / 4) * squareSize]  # Adjusted for 4 columns
    return [int(tablePosition[0] + xPadding), tablePosition[1] + yPadding]
        
def drawSelection():
    position = getPosition(selectedSquare)
    thumby.display.drawRectangle(position[0], position[1], squareSize, squareSize, 1)
        
def updateSelectedSquare(value):
    global audioLoaded
    if audio.playing == False:
        audioLoaded = False #need to load new audio file when selecting new sound
    global selectedSquare
    global audioPath
    newValue = selectedSquare + value
    if newValue >= 0 and newValue < len(table):
        selectedSquare = newValue
    if selectedSquare == 0:
        audioPath = "/Games/Thexecutor/assets/blaster.ima"
    if selectedSquare == 1:
        audioPath = "/Games/Thexecutor/assets/assaultRifle.ima"
    if selectedSquare == 2:
        audioPath = "/Games/Thexecutor/assets/freezeRay.ima"
    if selectedSquare == 3:
        audioPath = "/Games/Thexecutor/assets/communicator.ima"
    if selectedSquare == 4:
        audioPath = "/Games/Thexecutor/assets/analyzer.ima"
    if selectedSquare == 5:
        audioPath = "Games/Thexecutor/assets/bombsAway.ima"
    if selectedSquare == 6:
        audioPath = "Games/Thexecutor/assets/machineGun.ima"
    if selectedSquare == 7:
        audioPath = "Games/Thexecutor/assets/autoLaser.ima"
        
def userInput():
    if thumby.buttonU.justPressed():
        updateSelectedSquare(-4)  # Move up (4 columns)
    if thumby.buttonD.justPressed():
        updateSelectedSquare(4)  # Move down (4 columns)
    if thumby.buttonL.justPressed():
        updateSelectedSquare(-1)  # Move left
    if thumby.buttonR.justPressed():
        updateSelectedSquare(1)  # Move right
    if thumby.buttonA.justPressed(): # Play audio
        if audio.playing == False:
            if playaudio:
                global audioLoaded
                audioLoaded = False #need to load file after sound is played
                audio.play()
        # if audio.playing == True:
        #     if playaudio:
        #         audio.stop()
        #         af = open(audioPath, "rb")
        #         audiosamples = stat(audioPath)[6] * 2
        #         audio.load(af,15625,audiosamples)
        #         audioLoaded = True
                
    if thumby.buttonB.justPressed():
        global exit
        audio.stop()
        sleep_ms(500) #gives time for audio thread to clean itself up
        exit = True
        
#Splash Screen
        
thumby.display.fill(0)
thumby.display.drawText("Thexecutor", 7, 1, 1)
thumby.display.drawLine(7,10,65,10,1)
thumby.display.drawText("A:Play Sound", 0, 20, 1)
thumby.display.drawText("B:Quit", 20, 32, 1)
thumby.display.update()

while startup:
    if thumby.buttonA.justPressed():
        startup = False
        while thumby.inputPressed():
            sleep_ms(5)
    if thumby.buttonB.justPressed():
        exit = True
        startup = False
        
#Main Loop
    
while not exit:
    fullDisplayUpdate()
    userInput()
    if audio.playing:
        audio.fillbufs()
    if (audio.playing == False and audioLoaded == False):
        af = open(audioPath, "rb")
        audiosamples = stat(audioPath)[6] * 2
        audio.load(af,15625,audiosamples)
        audioLoaded = True

print("Exiting...")
