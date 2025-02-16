#asynchronously plays a logo video while stuff loads
from time import sleep
from grayscale import display, Sprite
from machine import Timer
from gc import collect
loc = "/Games/ThumbCommander/"

framecount = 0
frame = 0
intro_sprite = 0

def __init__():
    global frame, framecount, intro_sprite
    display.fill(0)
    display.update()
    intro_sprite = Sprite(74,30,(loc+"intro_74.BIT.bin",loc+"intro_74.SHD.bin"),0,5)
    framecount = intro_sprite.frameCount
    
def drawframe(dummy):
    global frame, framecount, intro_sprite
    intro_sprite.setFrame(frame)
    display.drawSprite(intro_sprite)
    display.update()
    frame += 1
    if frame >= framecount:
        frametimer.deinit()
        sleep(1)
        collect()
        
frametimer = Timer()

def start():
    frametimer.init(freq=8, mode=Timer.PERIODIC, callback=drawframe)

def finish():
    while frame < framecount: pass