# Silicon8 for Thumby
# By Timendus
#
# An interpreter for CHIP-8, SCHIP and XO-CHIP in MicroPython for the Thumby
# playable keychain by TinyCircuits.
#
# See https://github.com/Timendus/thumby-silicon8 for more information and
# licensing information.

import thumby

splash = bytearray([
    0,0,0,0,0,0,0,224,248,60,14,14,7,7,3,3,7,7,14,14,12,0,0,0,0,0,32,32,192,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,224,240,120,28,14,6,6,6,14,28,120,240,224,0,
    0,0,0,0,0,0,0,15,31,56,112,96,96,224,192,192,192,128,128,0,0,0,0,0,0,0,0,0,255,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,7,15,30,184,240,224,224,224,240,184,30,15,7,0,
    0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,1,3,15,254,248,0,0,196,64,0,0,255,0,0,196,64,0,0,0,128,64,64,64,0,0,0,128,64,64,128,0,0,0,192,64,64,64,128,0,0,0,252,254,15,3,1,0,0,0,1,3,15,254,252,0,
    0,48,112,112,224,224,192,192,192,192,192,192,192,192,224,96,112,56,28,15,7,1,0,0,63,0,0,0,63,0,0,63,0,0,0,15,16,32,32,32,0,0,15,16,32,32,16,15,0,0,63,0,0,0,0,63,0,0,3,7,15,28,56,48,48,48,56,28,15,7,3,0,
    0,60,66,66,66,0,124,16,16,124,0,122,0,124,20,20,8,0,40,84,84,40,0,0,0,66,126,66,0,124,4,4,120,0,62,68,0,56,84,84,88,0,124,8,4,0,124,20,20,8,0,124,8,4,0,56,84,84,88,0,62,68,0,56,84,84,88,0,124,8,4,0
])

# Stop sound and show splash while we wait ;)
thumby.audio.stop()
thumby.display.setFPS(0)
thumby.display.blit(splash, 0, 0, 72, 40, -1, 0, 0)
thumby.display.update()

# Fix import path so it finds our modules above all else
import sys
sys.path.insert(0, '/Games/Silicon8')

import time
import gc
import machine
import thumbyinterface
import roms
import cpu
import menu

gc.enable()

index = 0
scroll = 0

def gb_collect():
    print("Free memory before garbage collect:", gc.mem_free())
    gc.collect()
    print("Free memory after garbage collect:", gc.mem_free())

def runSilicon8():
    global index, scroll
    # Ask user to choose a ROM
    while True:
        gb_collect()
        program, index, scroll = menu.Menu(index, scroll).choose(roms.catalog())
        if not program["file"]:
            return False
        if menu.Confirm().choose(program):
            break

    gb_collect()

    # Instantiate interpreter
    instance = cpu.CPU()

    # Set up 60Hz interrupt handler
    timer = machine.Timer()
    timer.init(mode=timer.PERIODIC, period=17, callback=instance.clockTick)

    # Start the interpreter
    thumbyinterface.setKeys(program["keys"])
    instance.reset(program["type"])
    thumby.display.fill(0)
    thumby.display.update()
    instance.run(roms.load(program))
    return True

while runSilicon8():
    pass

thumby.reset()
