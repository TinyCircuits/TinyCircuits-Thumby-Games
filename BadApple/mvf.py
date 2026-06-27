#TODO:
# -eliminate the excessive amount of global variables
# -speed up LUT generation (probably viper)
# -arbitrary positioning of the video (could be movable while playing with fast LUTs)
# -reduce allocations
# -general cleanup

import struct
import time
import thumby
import gc
from micropython import mem_info


def printmem(reason=None):
    totalmem = 192064 #192064 is the total reported by mem_info
    print("\n" + "="*79)
    if reason: print(f"***{reason}***")
    print(f"{(totalmem-gc.mem_free())/totalmem*100}% RAM used")
    mem_info()
    print("="*79)


width = 0
height = 0
framerate = 30
framecount = 0
framezero = 0 #offset of frame 0
curframe = 0 #frames displayed
metadata = "" #embedded text
framequeue = []
data = None
stopped = False

displaywidth = thumby.display.width
displayheight = thumby.display.height
xpos = int(displaywidth/2 - width/2)
ypos = int(displayheight/2 - height/2)
hIndexLUT = bytearray(width*height*2) #gets interpreted as little endian
hBitLUT = bytearray(width*height)
vIndexLUT = bytearray(width*height*2) #gets interpreted as little endian
vBitLUT = bytearray(width*height)


def makeluts():
    global hIndexLUT, hBitLUT, vIndexLUT, vBitLUT
    hIndexLUT = bytearray(width*height*2) #gets interpreted as little endian
    hBitLUT = bytearray(width*height)
    vIndexLUT = bytearray(width*height*2) #gets interpreted as little endian
    vBitLUT = bytearray(width*height)
    
    print("[MVF] Generating horizontal LUT")
    i = 0
    for y in range(height): #horizontal scanning
        y += ypos
        for x in range(width):
            if y & 1: x = width - x - 1 #snake back on odd rows
            x += xpos
            index = (y >> 3) * displaywidth + x
            bit = 1 << (y & 7)
            hIndexLUT[i*2] = index & 255
            hIndexLUT[i*2+1] = index >> 8
            hBitLUT[i] = bit
            i += 1
    
    print("[MVF] Generating vertical LUT")
    i = 0
    for x in range(width): #vertical scanning
        x += xpos
        for y in range(height):
            if x & 1: y = height - y - 1 #snake back on odd columns
            y += ypos
            index = (y >> 3) * displaywidth + x
            bit = 1 << (y & 7)
            vIndexLUT[i*2] = index & 255
            vIndexLUT[i*2+1] = index >> 8
            vBitLUT[i] = bit
            i += 1


def decodevlq(data): #takes a file-like object, returns an int.
    total = 0
    nextbyte = ord(data.read(1))
    while nextbyte >= 128:
        total += nextbyte & 127
        total <<= 7
        nextbyte = ord(data.read(1))
    total += nextbyte
    return total


@micropython.viper
def clearscreen(): #clear video area without touching any other pixels
    display = ptr8(thumby.display.display.buffer)
    index = ptr16(hIndexLUT)
    bit = ptr8(hBitLUT)
    i:int = 0
    limit:int = int(width*height)
    while i < limit:
        display[index[i]] &= (bit[i] ^ 255)
        i += 1


@micropython.viper
def decodeiframe(framedata, scandir:int, runtype:int, bgcolour:int):
    if scandir:
        index = ptr16(vIndexLUT)
        bit = ptr8(vBitLUT)
    else:
        index = ptr16(hIndexLUT)
        bit = ptr8(hBitLUT)
    display = ptr8(thumby.display.display.buffer)
    data = ptr8(framedata)
    datapos = 0
    limit:int = int(width*height)
    colour:int = bgcolour
    num:int = 0
    nextbyte:int = 0
    i:int = 0
    while i < limit:
        num = 0
        nextbyte = data[datapos]
        datapos += 1
        while nextbyte & 128: #decode vlq number
            num += nextbyte & 127
            num <<= 7
            nextbyte = data[datapos]
            datapos += 1
        num += nextbyte
        
        while num > 0:
            if colour: display[index[i]] |= bit[i] #set white
            else: display[index[i]] &= (bit[i] ^ 255) #set black
            if runtype == 0: colour = bgcolour #reset after 1 pixel for pixel setting mode
            num -= 1
            i += 1
            if i == limit: break #technically not necessary, but needed to comply with the specs
        
        colour ^= 1


@micropython.viper
def decodepframe(framedata, scandir:int, runtype:int):
    if scandir:
        index = ptr16(vIndexLUT)
        bit = ptr8(vBitLUT)
    else:
        index = ptr16(hIndexLUT)
        bit = ptr8(hBitLUT)
    display = ptr8(thumby.display.display.buffer)
    data = ptr8(framedata)
    datapos = 0
    limit:int = int(width*height)
    num:int = 0
    nextbyte:int = 0
    i:int = 0
    if runtype == 0: #pixel setting mode
        while i < limit:
            num = 0
            nextbyte = data[datapos]
            datapos += 1
            while nextbyte & 128: #decode vlq number
                num += nextbyte & 127
                num <<= 7
                nextbyte = data[datapos]
                datapos += 1
            num += nextbyte
            
            i += num #go to pixel
            if i >= limit: break
            display[index[i]] ^= bit[i] #flip colour
    
    else: #run setting mode
        while i < limit:
            num = 0
            nextbyte = data[datapos]
            datapos += 1
            while nextbyte & 128: #decode vlq number
                num += nextbyte & 127
                num <<= 7
                nextbyte = data[datapos]
                datapos += 1
            num += nextbyte
            
            i += num #go to start of run
            if i >= limit: break
            
            num = 0
            nextbyte = data[datapos]
            datapos += 1
            while nextbyte & 128: #decode vlq number
                num += nextbyte & 127
                num <<= 7
                nextbyte = data[datapos]
                datapos += 1
            num += nextbyte
            
            while num > 0:
                display[index[i]] ^= bit[i] #flip colour
                num -= 1
                i += 1
                if i == limit: break 


def nextframe():
    global curframe
    if curframe >= framecount: return
    if curframe == 0: clearscreen()
    
    if len(framequeue) == 0:
        header = ord(data.read(1))
        framequeue.append(((header&8)>>3, (header&4)>>2, (header&2)>>1, header&1)) #second frame
        framequeue.append(((header&128)>>7, (header&64)>>6, (header&32)>>5, (header&16)>>4)) #first frame
    
    f = framequeue.pop()
    framelen = decodevlq(data)
    framedata = bytearray(data.read(framelen))
    
    if f[0]: #iframe
        decodeiframe(framedata, f[1], f[2], f[3])
    else: #pframe
        if f[3]: #has offset
            print("[MVF] Offset frames not supported. Remember to encode with scheme 1 and level 0")
            curframe = framecount
            return
        decodepframe(framedata, f[1], f[2])
    
    curframe += 1


def playing():
    if stopped: return False
    return curframe < framecount


def stop(): #future feature - store the last frame to resume playback flawlessly
    global stopped
    stopped = True


def reset(): #seek to frame 0
    global curframe, framequeue
    curframe = 0
    framequeue = []
    data.seek(framezero)


def load(f=None): #takes a file-like object seeked to the start of an MVF file
    global width, height, framerate, framecount, metadata, lastframe, curframe, framequeue, data, xpos, ypos, framezero
    if f == None: f = data
    else: data = f
    if data.read(4) != b"MVF\x00":
        print("[MVF] Not an MVF file, or unsupported future revision")
        return
    
    metalen = struct.unpack("<H", data.read(2))[0]
    metadata = data.read(metalen)
    oldwidth, oldheight = width, height
    width, height, framerate, framecount, scheme = struct.unpack("<HHBIB", data.read(10))
    if scheme != 1:
        print("[MVF] Unsupported compression scheme. Remember to encode with scheme 1 and level 0")
        return
    
    curframe = 0
    framequeue = []
    xpos = int(displaywidth/2 - width/2)
    ypos = int(displayheight/2 - height/2)
    framezero = data.tell()
    
    print(f"[MVF] Loaded video - {width}x{height}, {framecount} frames at {framerate} FPS")
    if oldwidth != width or oldheight != height: makeluts()


def play(callback=None, usegc=True):
    global stopped
    stopped = False
    oldframerate = thumby.display.frameRate
    thumby.display.setFPS(0) #use our own frame limiter for this
    #nexttime = time.ticks_ms()
    starttime = time.ticks_ms()
    
    #frames = 0
    #fpstimer = time.ticks_ms()
    
    while playing():
        #nexttime += 1000.0/framerate #can't use this with audio - cumulative error causes desync
        nexttime = starttime + (1000*curframe)/framerate #breaks pausing but that won't work with audio anyway
        if usegc: gc.collect()
        nextframe()
        if callback: callback()
        thumby.display.update()
        delayed = False
        while time.ticks_ms() < nexttime: #costly but reduces stutter in emulation
            delayed = True
            #time.sleep_ms(1)
        #if not delayed: print("Frame delay not necessary - May be overloaded, or timer too imprecise")
        
        #frames += 1
        #if time.ticks_ms() > fpstimer:
        #    print(frames)
        #    fpstimer += 1000
        #    frames = 0
    
    thumby.display.setFPS(oldframerate)


