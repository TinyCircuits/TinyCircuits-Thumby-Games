#TODO:
# -safer threading
# -fix a very rare problem where the audio stops for no obvious reason - only happened twice ever, couldn't trace it.
#  In both cases the audio stopped (completely silent) and buffers stopped being filled, but there were no error messages and the thread didn't exit.
# -less hardcoded stuff

import time
import thumby
import struct
import _thread
import zlib

bufsize = 800 #enough for 6 frames at 30 FPS
buf1 = bytearray(bufsize)
buf2 = bytearray(bufsize)
data = None
playing = False
lengths = [] #compressed size of each audio block, in reverse

#current buffer, pos in buffer, bufsize, current sample, total samples, buf1NeedsFilling, buf2NeedsFilling
bufstate = bytearray(struct.pack("<IIIIIII", 0, 0, bufsize, 0, 0, 1, 1))

@micropython.viper
def audioloop():
    from machine import PWM, Pin
    swBuzzer = PWM(Pin(28))
    setwidth = swBuzzer.duty_u16 #redefining these rather than using thumby.audio reduces clicking
    curtime = time.ticks_us
    state:ptr32 = ptr32(bufstate)
    b1:ptr8 = ptr8(buf1)
    b2:ptr8 = ptr8(buf2)
    delay:int = 1000000//8000
    nexttime:int = int(curtime()) + delay
    sample:int = 0
    
    while state[3] < state[4]: #still playing
        if not state[0]: #first buffer
            if state[3] & 1: #odd sample
                sample += (b1[state[1]] & 0b1111)
                state[3] += 1
                state[1] += 1
                if state[1] >= state[2]: #end of buffer
                    state[5+state[0]] = 1 #set flag
                    state[0] ^= 1 #swap buffers
                    state[1] = 0
            else: #even sample
                sample += (b1[state[1]] & 0b11110000) >> 4
                state[3] += 1
        else:
            if state[3] & 1: #odd sample
                sample += (b2[state[1]] & 0b1111)
                state[3] += 1
                state[1] += 1
                if state[1] >= state[2]: #end of buffer
                    state[5+state[0]] = 1 #set flag
                    state[0] ^= 1 #swap buffers
                    state[1] = 0
            else: #even sample
                sample += (b2[state[1]] & 0b11110000) >> 4
                state[3] += 1
        
        sample &= 0b1111
        while int(curtime()) < nexttime: pass
        setwidth(sample << 12)
        nexttime += delay
    
    print("Thread ended")
    stop()


@micropython.viper
def copyfrom(b1, b2): #copy b1 to b2
    i:int = 0
    p1:ptr8 = ptr8(b1)
    p2:ptr8 = ptr8(b2)
    for i in range(int(len(b2))):
        p2[i] = p1[i]


def fillbufs():
    global bufstate
    if bufstate[20]: #20 and 24 are the buffer empty flags
        if len(lengths):
            decompressed = zlib.decompress(data.read(lengths.pop()))
            copyfrom(decompressed, buf1)
        bufstate[20] = 0
        print("buf1 filled")
    if bufstate[24]:
        if len(lengths):
            decompressed = zlib.decompress(data.read(lengths.pop()))
            copyfrom(decompressed, buf2)
        bufstate[24] = 0
        print("buf2 filled")


def load(f):
    global data, buf1, buf2, bufstate, lengths
    data = f
    size, tablesize = struct.unpack("<IH", data.read(6))
    table = data.read(tablesize)
    lengths = []
    for block in range(0, tablesize, 2):
        lengths.append(table[block] + (table[block+1] << 8))
    lengths.reverse()
    buf1 = bytearray(bufsize)
    buf2 = bytearray(bufsize)
    #current buffer, pos in buffer, bufsize, current sample, total samples, buf1NeedsFilling, buf2NeedsFilling
    bufstate = bytearray(struct.pack("<IIIIIII", 0, 0, bufsize, 0, size, 1, 1))
    fillbufs()


def play():
    global playing
    playing = True
    thumby.audio.set(80000)
    _thread.start_new_thread(audioloop, ())


def stop():
    global playing
    playing = False
    bufstate[12] = bufstate[16] #set current sample to limit
    bufstate[13] = bufstate[17]
    bufstate[14] = bufstate[18]
    bufstate[15] = bufstate[19] #most significant last in case it's clobbered - should really acquire a lock for this
    #time.sleep_ms(500)
    thumby.audio.set(1000) #make audible to tell if it fails to stop correctly
    thumby.audio.stop()

