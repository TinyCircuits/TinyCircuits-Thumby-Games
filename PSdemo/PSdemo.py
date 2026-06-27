from sys import path as syspath
syspath.append("/Games/PSdemo") #fix imports

import machine
machine.freq(125000000) #ensure this is running at full speed

import thumby
thumby.display.update() #clear the screen ASAP

try:
    import emulator
    print("Emulator detected!\nThis cannot run because of hardware emulation limitations.\nSorry!")
    thumby.display.drawText("This doesn't", 0, 0, 1)
    thumby.display.drawText(" work under ", 0, 8, 1)
    thumby.display.drawText(" emulation. ", 0, 16, 1)
    thumby.display.drawText("   Sorry!   ", 0, 24, 1)
    while True:
        thumby.display.update()
except ImportError:
    print("Emulator not detected. Enjoy!")

from time import sleep_ms, sleep_us
from _thread import start_new_thread #only for oscilloscope
import polysynth
import midi
import logo


logo.start() #hide the loading time with the logo
machine.freq(220000000) #overclock while loading

print("\n*** Song 1 ***")
#there isn't enough memory to preload the entire song anymore, so it must be opened as a stream.
song1 = midi.loadstream(open("/Games/PSdemo/moontheme.mid", "rb"), reserve={0:[0,1,8], 1:[2], 2:[3], 3:[4,5,6]}, callbacks={7:polysynth.enabled})

instruments1 = {
#0:polysynth.instrument(), #square 1
1:polysynth.instrument(vibspeed=7.5, vibamount=0.4), #square 1 vibrato
#2:polysynth.instrument(), #square 2
#3:polysynth.instrument(), #triangle
4:polysynth.instrument(detune=57), #drum low
5:polysynth.instrument(detune=95), #drum mid
6:polysynth.instrument(detune=150), #drum high
#7:polysynth.instrument(), #set channel count callback
8:polysynth.instrument(rise=11.25), #square 1 pitch bend - rises by 15 notes over 1.33 seconds. Using rise for now in lieu of proper MIDI pitch bend.
}

print("\n*** Song 2 ***")
#this song can be entirely loaded - this will reduce the risk of stuttering.
song2 = midi.load(open("/Games/PSdemo/evergreen.mid", "rb"))

instruments2 = {
0:polysynth.instrument(phaselock=True), #main lead
1:polysynth.instrument(vibspeed=6, vibamount=0.25), #main lead vibrato
2:polysynth.instrument(phaselock=True), #main lead double
3:polysynth.instrument(vibspeed=6, vibamount=0.25), #main lead vibrato double
4:polysynth.instrument(phaselock=True), #bass
5:polysynth.instrument(phaselock=True), #bass double
6:polysynth.instrument(detune=0.02), #channel 2 backing
7:polysynth.instrument(detune=-0.06), #channel 4 backing
8:polysynth.instrument(detune=0.1), #main lead echo
9:polysynth.instrument(detune=0.1, vibspeed=6, vibamount=0.25), #main lead echo vibrato
}

machine.freq(125000000) #back to normal speed


# BITMAP: width: 30, height: 8
mixertext = bytearray([127,2,4,2,127,0,65,127,65,0,119,8,119,0,127,73,65,0,127,9,118,0,36,0,0,0,0,0,0,0])


def transition(colour):
    for frame in range(8):
        for x in range(0, 72+40, 8):
            thumby.display.drawLine(x+frame, 0, x+frame-40, 40, colour)
        thumby.display.update()


lfsrstate = 1
@micropython.viper
def partialrandom(threshold:int): #write random pixels to the screen with a weighted random chance
    global lfsrstate
    screen:ptr8 = ptr8(thumby.display.display.buffer)
    pos:int = 0
    bit:int = 0
    lfsr:int = int(lfsrstate)
    temp:int = 0
    for pos in range(72*40//8):
        for bit in range(8):
            temp = ((lfsr & 1) << 21) ^ lfsr
            lfsr = (lfsr >> 1) | (temp & (1<<21))
            if lfsr&127 < threshold:
                screen[pos] &= (1<<bit) ^ 255
                screen[pos] |= (lfsr & 1) << bit
    lfsrstate = lfsr


waveforms = bytearray(72//2*3)
offsets = bytearray([i*2 for i in polysynth.unusedpins])
oscommand = bytearray(1) #thread communication - set 1 to start capture, 2 to exit
@micropython.viper
def oscillothread():
    i:int = 0
    pin:int = 0
    buf:ptr8 = ptr8(waveforms)
    bufsize:int = int(len(waveforms))
    ports:ptr32 = ptr32(0x40014000) #location of GPIO registers - this bypasses machine.Pin
    off:ptr8 = ptr8(offsets)
    ticks_us:ptr32 = ptr32(0x40054028) #location of microsecond register (TIMERAWL) - time.sleep_us causes instability
    lasttime:int = ticks_us[0] & 0x3fffffff #mask off upper bits to make room for signed comparisons
    cmd = ptr8(oscommand)
    while True:
        cmd[0] = 0
        for i in range(bufsize): waveforms[i] = 0 #clear buffer
        
        for i in range(bufsize):
            for pin in range(7):
                buf[i] |= (ports[off[pin]]>>9 & 1) << pin #bit 9 is the output as per the RP2040 datasheet
            #sleep(200)
            while -200 < (ticks_us[0] & 0x3fffffff) - lasttime < 200: pass #wait 200 microseconds, accommodating timer overflows
            lasttime = ticks_us[0] & 0x3fffffff
        
        while cmd[0] == 0: pass #wait for signal to continue
        if cmd[0] > 1: break
    print("Oscilloscope thread ended")
    cmd[0] = 0


@micropython.viper
def oscillorender():
    i:int = 0
    j:int = 0
    screen:ptr8 = ptr8(thumby.display.display.buffer)
    capture:ptr8 = ptr8(waveforms)
    bit:int = 0
    pos:int = 0
    offset:int = 0
    for i in range(7):
        bit = 1<<i
        for offset in range(72//4, int(len(waveforms))-72//4):
            if capture[offset] & bit == 0 and capture[offset+1] & bit: break #find a rising edge
        offset -= 72//4
        for j in range(72//2-1):
            if capture[j+offset] & bit: screen[pos] |= 1
            else: screen[pos] |= 0b1000000
            if capture[j+offset] & bit != capture[j+offset+1] & bit: screen[pos] |= 0b1111111
            pos += 1
        pos += 1


scrollsurf = bytearray(72)
@micropython.viper
def scrolltick():
    buf:ptr8 = ptr8(scrollsurf)
    i:int = 0
    for i in range(int(len(scrollsurf))):
        buf[i] <<= 1


def wavescreen(): #main screen drawing
    thumby.display.fill(0)
    oscillorender()
    oscommand[0] = 1 #send signal to capture next section
    thumby.display.blit(mixertext, 72//2 + 5, 8*3, 30, 8, -1, 0, 0)
    thumby.display.drawText(str(polysynth.enabled()), 72-6, 8*3, 1)
    
    scrolltick()
    for i in polysynth.notes:
        if i != None and 0 <= i-31 < 72: #31 just barely fits all notes in these songs on screen. 36 is better in general.
            scrollsurf[i-31] |= 1
    thumby.display.blit(scrollsurf, 0, 8*4, 72, 8, -1, 0, 0)


def intro():
    pitch = 100
    
    polysynth.configure([polysynth.NOISE]) #set up with one static channel
    polysynth.enabled(1) #turn on one channel
    
    polysynth.setpitch(0, 8000) #set channel 0 to 8kHz
    sleep_ms(5) #delay for long enough to sound like a click
    polysynth.setpitch(0, 0) #turn off the channel
    
    for x in range(0, 72//3, 5): #horizontal expanding section
        partialrandom(255)
        thumby.display.drawFilledRectangle(0, 0, 72, 19, 0)
        thumby.display.drawFilledRectangle(0, 20, 72, 20, 0)
        thumby.display.drawFilledRectangle(0, 19, 72//2-x, 1, 0)
        thumby.display.drawFilledRectangle(72//2+x+1, 19, 72//2, 1, 0)
        thumby.display.update()
        pitch *= 1.45
        polysynth.setpitch(0, pitch)
        if thumby.buttonA.justPressed(): return
    
    for y in range(0, 20, 3): #vertical expanding section
        partialrandom(255)
        thumby.display.drawFilledRectangle(0, 0, 72, 20-y, 0)
        thumby.display.drawFilledRectangle(0, 20+y+1, 72, 20, 0)
        thumby.display.update()
        pitch *= 1.45
        polysynth.setpitch(0, pitch)
        if thumby.buttonA.justPressed(): return
    
    for i in range(120): #display a few seconds of static
        partialrandom(255)
        thumby.display.update()
        if thumby.buttonA.justPressed(): return
    
    fadestep = 7 * 15
    for i in range(7):
        polysynth.enabled(i+1) #gradually turn on more channels to reduce the volume
        for j in range(15):
            fadestep -= 1
            wavescreen()
            partialrandom(fadestep)
            thumby.display.update()
        if thumby.buttonA.justPressed(): return


start_new_thread(oscillothread, ())

logo.finish()
thumby.display.setFPS(30)
transition(0)
sleep_ms(1000)

intro()
polysynth.stop()

for i in range(60):
    wavescreen()
    thumby.display.update()

#set up for first song
polysynth.configure([polysynth.SQUARE, polysynth.SQUARE, polysynth.SQUARE, polysynth.NOISE])
polysynth.enabled(4) #this has to be specified since streams can't know how many channels will be needed
polysynth.playstream(song1, instruments1) #play the first song

while polysynth.playing:
    wavescreen()
    thumby.display.update()
    if thumby.buttonA.justPressed(): break
polysynth.stop()

for i in range(8):
    wavescreen()
    thumby.display.update()
sleep_ms(2000)


#set up for second song
polysynth.configure()
polysynth.play(song2, instruments2) #play the second song

while polysynth.playing:
    wavescreen()
    thumby.display.update()
    if thumby.buttonA.justPressed(): break
polysynth.stop()

for i in range(8):
    wavescreen()
    thumby.display.update()


oscommand[0] = 2 #stop capture thread
sleep_ms(1000)

transition(0)
