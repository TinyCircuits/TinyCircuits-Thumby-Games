import thumby
import time

freq = 523

class Note:
    freqs = [0, 262, 294, 330, 349, 392, 440, 494]
    notes = ["-", "C", "D", "E", "F", "G", "A", "B"]
    notes_lower = ["_", "c", "d", "e", "f", "g", "a", "b"]
    idx = 0
    octave = False
    
    def __init__(self, xPos, yPos):
        self.xPos = xPos
        self.yPos = yPos
        
    def inc(self):
        self.idx += 1
        
        if self.idx >= len(self.notes):
            self.idx = len(self.notes) - 1
        
    def dec(self):
        self.idx -=1
        
        if self.idx < 0:
            self.idx = 0
    
    def draw(self):
        #invert color if octave
        if self.octave:
            thumby.display.drawFilledRectangle(self.xPos, self.yPos + (len(self.notes) - self.idx), 9, 11, 1)
            thumby.display.drawText(self.notes[self.idx], self.xPos + 2, self.yPos + (len(self.notes) - self.idx) + 2, 0)
        else:
            thumby.display.drawRectangle(self.xPos, self.yPos + (len(self.notes) - self.idx), 9, 11, 1)
            thumby.display.drawText(self.notes[self.idx], self.xPos + 2, self.yPos + (len(self.notes) - self.idx) + 2, 1)
        
    def play(self, dur):
        if self.freqs[self.idx] != 0:
            if self.octave:
                freq = self.freqs[self.idx] * 2
            else:
                freq = self.freqs[self.idx]
            thumby.audio.play(freq, dur)
        
    def playBlocking(self, dur):
        if self.freqs[self.idx] != 0:
            if self.octave:
                freq = self.freqs[self.idx] * 2
            else:
                freq = self.freqs[self.idx]
            thumby.audio.playBlocking(freq, dur)
        else:
            time.sleep(dur/1000)
        
    def toggleOctave(self):
        self.octave = not self.octave
        
    def getChar(self):
        if self.octave:
            return self.notes[self.idx]
        else:
            return self.notes_lower[self.idx]
    
    def setChar(self, char):
        try:
            self.idx = self.notes.index(char)
            self.octave = True
        except:
            self.idx = self.notes_lower.index(char)
        

noteSpots = []
curNote = 0
titleScreen = True

#top row
for i in range (0, 8):
    noteSpots.append(Note((9*i) + 1, 0))
#bottom row
for i in range (0, 8):
    noteSpots.append(Note((9*i) + 1, 20))

pressed = False #keeps note from flying up or down

def playMelody(noteSpots, curNote):
    drawCursor(curNote, 0) #remove selection cursor
    s = 0
    for note in noteSpots:
        drawCursor(s, 1)
        thumby.display.update()
        note.playBlocking(200)
        drawCursor(s, 0)
        s += 1
        
def drawCursor(curNote, color):
    if curNote < 8:
        thumby.display.drawLine(noteSpots[curNote].xPos, 19, noteSpots[curNote].xPos + 7, 19, color)
    else:
        thumby.display.drawLine(noteSpots[curNote].xPos, 39, noteSpots[curNote].xPos + 7, 39, color)

def saveSequence(noteSpots):
    saveString = ""
    for note in noteSpots:
        if note.octave:
            saveString += note.getChar().upper()
        else:
            saveString += note.getChar()
    
    #write melody file
    f = open("/Games/MelodyMaker/melody.txt", "w")
    f.write(saveString)
    f.close()
    
def loadSequence():
    loadString = ""
    try:
        f = open("/Games/MelodyMaker/melody.txt")
        loadString = f.read()
        f.close()
    except: #make default melody file
        f = open("/Games/MelodyMaker/melody.txt", "w")
        f.write("BAG_BAG_GGAABAG_")
        f.close()
        loadString = "BAG_BAG_GGAABAG_"
    
    idx = 0
    for char in loadString:
        noteSpots[idx].setChar(char)
        idx += 1
        
loadSequence()

while 1:
    
    #title screen
    while titleScreen:
        thumby.display.fill(0)
        thumby.display.drawText("Melody Maker", 0, 0, 1)
        thumby.display.drawText("by", 29, 10, 1)
        thumby.display.drawText("SuperRiley64", 0, 20, 1)
        thumby.display.drawFilledRectangle(0, 30, 70, 10, 1)
        thumby.display.drawText("Press A", 14, 32, 0)
        if thumby.buttonA.pressed():
            thumby.display.fill(0)
            titleScreen = False
            for note in noteSpots:
                note.draw()
            break
        thumby.display.update()
    
    #input section
    if thumby.buttonU.pressed() and not pressed:
        noteSpots[curNote].inc()
        noteSpots[curNote].play(500)
        pressed = True
    elif thumby.buttonD.pressed() and not pressed:
        noteSpots[curNote].dec()
        noteSpots[curNote].play(500)
        pressed = True
    elif thumby.buttonL.pressed() and not pressed:
        if curNote > 0:
            curNote -= 1
        pressed = True
    elif thumby.buttonR.pressed() and not pressed:
        if curNote < len(noteSpots) - 1:
            curNote += 1
        pressed = True
    elif thumby.buttonA.pressed() and not pressed:
        saveSequence(noteSpots)
        playMelody(noteSpots, curNote)
        pressed = True
    elif thumby.buttonB.pressed() and not pressed:
        noteSpots[curNote].toggleOctave()
        noteSpots[curNote].play(500)
        pressed = True
    elif not thumby.buttonD.pressed() and not thumby.buttonU.pressed() and not thumby.buttonL.pressed() and not thumby.buttonR.pressed() and not thumby.buttonA.pressed() and not thumby.buttonB.pressed():
        pressed = False
    
    #Drawing section
    thumby.display.fill(0)
    
    for note in noteSpots:
        note.draw()
    drawCursor(curNote, 1)
    
    #make the screen look even lol
    thumby.display.drawLine(1, 0, 1, 40, 0)
    
    
    thumby.display.update()