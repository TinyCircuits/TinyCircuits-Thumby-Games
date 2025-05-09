# Audio engine as developed by Transistortestor for Thumby Color and back ported by me with their
# support to the original Thumby.


# Implements raw 4-bit IMA ADPCM using more or less the standard way. 
# Files for this were processed as follows:
# 1) Convert to 15625 Hz Mono, volume boosted, and pitch increased in Audacity
# 2) Exported as wav file with IMA ADPCM encoding
# 3) Converted to IMA with SoX (Sound eXchange):
# 4) sox inputfilename outputfilename.ima

# Ported by Ace Geiger 2025
# All comments below are from Transistortestor unless otherwise noted.


#there is a slight tick every time a buffer is filled - I suspect that running the audio loop entirely in RAM will likely eliminate it.
#the only part that still runs from flash is setting the pulse width, but configuring PWM with raw register writes if a hassle so it's been left for now.

import time
import struct
import _thread
import array

bufsize = 800 #enough for 6 frames at 30 FPS at 8 KHz
sampledelay = 125 #microseconds between samples
buf1 = bytearray(bufsize)
buf2 = bytearray(bufsize)
data = None
playing = False

#current buffer, pos in buffer, bufsize, current sample, total samples, buf1NeedsFilling, buf2NeedsFilling
bufstate = array.array("I", [0, 0, bufsize, 0, 0, 1, 1])

IMAindextable = array.array("i", [ #it appears that only ptr32 works with signed numbers in viper
    -1, -1, -1, -1, 2, 4, 6, 8,
    -1, -1, -1, -1, 2, 4, 6, 8
])

IMAsteptable = array.array("h", [
    7, 8, 9, 10, 11, 12, 13, 14, 16, 17, 
    19, 21, 23, 25, 28, 31, 34, 37, 41, 45, 
    50, 55, 60, 66, 73, 80, 88, 97, 107, 118, 
    130, 143, 157, 173, 190, 209, 230, 253, 279, 307,
    337, 371, 408, 449, 494, 544, 598, 658, 724, 796,
    876, 963, 1060, 1166, 1282, 1411, 1552, 1707, 1878, 2066, 
    2272, 2499, 2749, 3024, 3327, 3660, 4026, 4428, 4871, 5358,
    5894, 6484, 7132, 7845, 8630, 9493, 10442, 11487, 12635, 13899, 
    15289, 16818, 18500, 20350, 22385, 24623, 27086, 29794, 32767
])

@micropython.viper
def audioloop():
    from machine import PWM, Pin
    pwm = PWM(Pin(28))
    pwm.freq(120000) # changed from pwm = PWM(Pin(28), freq=120000) to support microPython 1.19 and original Thumby -ace
    setwidth = pwm.duty_u16 #Redefining these reduces clicks. Directly writing to the register would be better, but this works.
    #curtime = time.ticks_us
    curtime = ptr32(0x40054028) #location of microsecond register, as per RP2040 datasheet and transistortestor (TIMERAWL of TIMER0) -ace
    state:ptr32 = ptr32(bufstate)
    b1:ptr8 = ptr8(buf1)
    b2:ptr8 = ptr8(buf2)
    delay:int = int(sampledelay)
    #nexttime:int = int(curtime()) + delay
    nexttime:int = (curtime[0] & 0x3fffffff) #mask off highest bit so it can't be treated as signed - should be 7 instead of 3 but can't due to viper funkiness
    
    indextable:ptr32 = ptr32(IMAindextable)
    steptable:ptr16 = ptr16(IMAsteptable)
    prediction:int = 32768 #would normally be 0 and signed, but since duty_u16 is unsigned, the offset is built-in here. Over/underflow checks have been changed accordingly.
    index:int = 0
    step:int = steptable[index]
    delta:int = 0
    diff:int = 0
    
    while state[3] < state[4]: #still playing
        if state[0]: #second buffer
            delta = b2[state[1]]
        else: #first buffer
            delta = b1[state[1]]
        
        if state[3] & 1: #odd sample
            delta &= 0b1111 #NOTE: Some variants of IMA ADPCM swap which half is processed first
            state[1] += 1 #increment bufpos
            if state[1] >= state[2]: #if end of buffer
                state[5+state[0]] = 1 #set flag
                state[0] ^= 1 #swap buffers
                state[1] = 0 #reset bufpos
        else:
            delta >>= 4
        
        state[3] += 1 #increment sample number
        
        diff = step >> 3 #calculate next sample
        if delta & 0b100: diff += step
        if delta & 0b10: diff += (step >> 1)
        if delta & 0b1: diff += (step >> 2)
        if delta & 0b1000:
            prediction -= diff
            if prediction < 0: prediction = 0 #cap to valid range (normally -32768 with no offset)
        else:
            prediction += diff
            if prediction > 65535: prediction = 65535 #normally 32767 with no offset
        
        index += indextable[delta] #update state
        if index < 0: index = 0
        elif index > 88: index = 88
        step = steptable[index]
        
        #while int(curtime()) < nexttime: pass
        while (curtime[0] & 0x3fffffff) < nexttime or (curtime[0] & 0x3fffffff) - nexttime > 0x1fffffff: pass #wait for next sample, or for overflow
        setwidth(prediction) #TODO: Replace this line with raw register writes
        nexttime += delay
        nexttime &= 0x3fffffff #keep within valid range
    
    setwidth(0)
    pwm.deinit()
    print("Thread ended")
    stop()


def fillbufs():
    global bufstate
    if bufstate[5]: #5 and 6 are the buffer empty flags
        data.readinto(buf1)
        bufstate[5] = 0
        print("buf1 filled")
    if bufstate[6]:
        data.readinto(buf2)
        bufstate[6] = 0
        print("buf2 filled")


validrates = [15625, 12500, 10000, 8000, 6250, 5000, 4000] #not exhaustive - anything that evenly divides 1000000, provided fillbuffs() is called often enough to keep up
def load(f, samplerate, samplecount):
    global data, buf1, buf2, bufstate, sampledelay
    if not samplerate in validrates:
        print("Unsupported sample rate")
        return
    sampledelay = 1000000//samplerate
    data = f
    buf1 = bytearray(bufsize)
    buf2 = bytearray(bufsize)
    #current buffer, pos in buffer, bufsize, current sample, total samples, buf1NeedsFilling, buf2NeedsFilling
    bufstate = array.array("I", [0, 0, bufsize, 0, samplecount, 1, 1])
    fillbufs()
    print("loaded")


def play():
    global playing
    playing = True
    _thread.start_new_thread(audioloop, ())


def stop():
    global playing
    playing = False
    bufstate[3] = bufstate[4] #set current sample to limit