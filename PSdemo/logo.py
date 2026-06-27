#asynchronously plays a logo video while stuff loads

import thumbyGraphics
from machine import Timer

data = open("/Games/PSdemo/logo.bin", "rb")
framecount = ord(data.read(1))
frame = 0

def drawframe(dummy):
    global frame
    diff = 0
    pos = 0
    while True:
        step = ord(data.read(1))
        pos += step & 127
        if pos >= 360: break #end of screen buffer
        if step & 128: diff = ord(data.read(1))
        thumbyGraphics.display.display.buffer[pos] ^= diff
    frame += 1
    if frame >= framecount:
        frametimer.deinit()
        data.close()
    thumbyGraphics.display.update()

frametimer = Timer()

def start():
    frametimer.init(freq=30, mode=Timer.PERIODIC, callback=drawframe)

def finish():
    while frame < framecount: pass
