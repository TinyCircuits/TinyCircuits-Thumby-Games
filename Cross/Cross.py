import sys
import time
import thumbyButton as buttons
import ujson
import random
from math import *

sys.path.append("/Games/Cross")

from player import Player
from collCheck import CollisionChecker
from thumbyGrayscale import display, Sprite
import sprites

pw, ph = 11, 13
debug = 0

la = ""
counter = 0
count = 0
frame = 0
frameLimit = 0
lockLimit = 0
frameStart = 0

with open("/Games/Cross/lvlData.txt", "r") as file:
    colliders = ujson.load(file)["colliders"]

display.setFont("/lib/font3x5.bin", 3, 5, 1)
display.setFPS(30)

def clip(x1, y1, x2, y2):
    if (x1 < -1):
        x1 = -1
    if (x1 > 72):
        x1 = 72
    if (x2 < -1):
        x2 = -1
    if (x2 > 72): 
        x2 = 72
    if (y1 < -1):
        y1 = -1
    if (y1 > 40):
        y1 = 40
    if (y2 < -1):
        y2 = -1
    if (y2 > 40):
        y2 = 40
    
    return x1, y1, x2, y2

def isBoxOffscreen(x1, y1, w, h):
    return (x1 + w < 0 or x1 > 72 or y1 + h < 0 or y1 > 40)

def draw_colliders(colliders, camera, debug):
    objDrawn = 0
    screen_width = 77
    screen_height = 45
    
    x1, y1, x2, y2 = 0, 0, 0, 0
    
    for collider in colliders:
        x, y, w, h = collider
        
        x1, y1 = x + camera[0], y + camera[1]
        x2, y2 = x1 + w, y1

        if isBoxOffscreen(x1, y1, w, h):
            continue
        
        display.drawLine(x1, y1, x2, y2, 1)
        
        x1 = x2
        y2 = y1 + h
        x1, y1, x2, y2 = clip(x1, y1, x2, y2)
        display.drawLine(x1, y1, x2, y2, 1)
        
        x1, y1 = x + camera[0], y + camera[1] + h
        x2 = x1 + w + 1
        x1, y1, x2, y2 = clip(x1, y1, x2, y2)
        display.drawLine(x1, y1, x2, y2, 1)
        
        y1 = y + camera[1]
        x2, y2 = x1, y1 + h
        x1, y1, x2, y2 = clip(x1, y1, x2, y2)
        display.drawLine(x1, y1, x2, y2, 1)
        
        objDrawn += 1
        
    if debug == 1:
        display.drawText("Obj: " + str(objDrawn), 40, 2, 1)


CrossFrames = {
    "Idle": [
        bytearray(sprites.idle1[0]), bytearray(sprites.idle1[1]),
        bytearray(sprites.idle2[0]), bytearray(sprites.idle2[1])
    ],
    "Walk": [
        bytearray(sprites.walk1[0]), bytearray(sprites.walk1[1]),
        bytearray(sprites.walk2[0]), bytearray(sprites.walk2[1]),
        bytearray(sprites.walk3[0]), bytearray(sprites.walk3[1]),
        bytearray(sprites.walk4[0]), bytearray(sprites.walk4[1]),
        bytearray(sprites.walk5[0]), bytearray(sprites.walk5[1])
    ],
    "Spin": [
        bytearray(sprites.spin1[0]), bytearray(sprites.spin1[1]),
        bytearray(sprites.spin2[0]), bytearray(sprites.spin2[1]),
        bytearray(sprites.spin3[0]), bytearray(sprites.spin3[1]),
        bytearray(sprites.spin4[0]), bytearray(sprites.spin4[1]),
        bytearray(sprites.spin5[0]), bytearray(sprites.spin5[1]),
        bytearray(sprites.spin6[0]), bytearray(sprites.spin6[1])
    ],
    "Jump": [
        bytearray(sprites.jump1[0]), bytearray(sprites.jump1[1])
    ],
    "Fall": [
        bytearray(sprites.fall1[0]), bytearray(sprites.fall1[1])
    ]
}

def check():
    sprite_frames = [
        (sprites.idle1, 'idle1'),
        (sprites.idle2, 'idle2'),
        (sprites.walk1, 'walk1'),
        (sprites.walk2, 'walk2'),
        (sprites.walk3, 'walk3'),
        (sprites.walk4, 'walk4'),
        (sprites.walk5, 'walk5'),
        (sprites.jump1, 'jump1'),
        (sprites.fall1, 'fall1'),
        (sprites.spin1, 'spin1'),
        (sprites.spin2, 'spin2'),
        (sprites.spin3, 'spin3'),
        (sprites.spin4, 'spin4'),
        (sprites.spin5, 'spin5'),
        (sprites.spin6, 'spin6'),
    ]
    
    for frame_data, frame_name in sprite_frames:
        plane0 = bytearray(frame_data[0])
        plane1 = bytearray(frame_data[1])
        
        width_plane0 = len(plane0)
        width_plane1 = len(plane1)
        
        assert width_plane0 == 26, f"Width of plane 0 in frame {frame_name} is {width_plane0}, expected 26"
        assert width_plane1 == 26, f"Width of plane 1 in frame {frame_name} is {width_plane1}, expected 26"
        
        print(f"Frame {frame_name}: Byte size of plane 0 = {width_plane0}, plane 1 = {width_plane1}")
#check()

p = Player(0, 0, 10, 20)
Cross = Sprite(
    13, 13,
    (
        CrossFrames["Idle"][0] + CrossFrames["Idle"][2] +
        CrossFrames["Walk"][0] + CrossFrames["Walk"][2] + CrossFrames["Walk"][4] + CrossFrames["Walk"][6] + CrossFrames["Walk"][8] +
        CrossFrames["Jump"][0] + CrossFrames["Fall"][0] + 
        CrossFrames["Spin"][0] + CrossFrames["Spin"][2] + CrossFrames["Spin"][4] + CrossFrames["Spin"][6] + CrossFrames["Spin"][8] + CrossFrames["Spin"][10],
        
        CrossFrames["Idle"][1] + CrossFrames["Idle"][3] +
        CrossFrames["Walk"][1] + CrossFrames["Walk"][3] + CrossFrames["Walk"][5] + CrossFrames["Walk"][7] + CrossFrames["Walk"][9] +
        CrossFrames["Jump"][1] + CrossFrames["Fall"][1] +
        CrossFrames["Spin"][1] + CrossFrames["Spin"][3] + CrossFrames["Spin"][5] + CrossFrames["Spin"][7] + CrossFrames["Spin"][9] + CrossFrames["Spin"][11]
    ),
    0, 0
)

def animate(p, la):
    global lockLimit, frameLimit, frame, counter, count, frameStart
    if lockLimit >= 1:
        p.anim = la

    if p.anim == la:
        if counter >= count:
            frame += 1
            counter = 0
            if frame >= frameLimit:
                frame = frameStart
                lockLimit -= 1
        counter += 1
    else:
        if lockLimit >= 1:
            return
        
        p.dash = 1
        lockLimit = 0
        counter = 0
        frame = 0

        if p.anim == "Idle":
            count = 4
            frameLimit = 2
            frameStart = 0
            lockLimit = 0
        elif p.anim == "Walk":
            count = 4
            frameLimit = 7
            frameStart = 2
            lockLimit = 0
        elif p.anim == "Spin":
            count = 2
            frameLimit = 15
            frameStart = 9
            lockLimit = 2
            p.dash = 0
        elif p.anim == "Jump":
            count = 4
            frameLimit = 8
            frameStart = 7
            lockLimit = 0
        elif p.anim == "Fall":
            count = 4
            frameLimit = 9
            frameStart = 8
            lockLimit = 0
        frame = frameStart
    print(p.anim, la)
    print(lockLimit, frameLimit, frame, count, counter)

while True:
    display.update()
    display.fill(0)
    
    Cross.key = 0
    la = p.anim
    p.move(ph)
    
    for collider in colliders:
        collision_type = CollisionChecker.check_collision(p.positions, pw, ph, collider)
        if collision_type:
            if collision_type == "feet":
                p.positions[1] = collider[1] - ph - 1
                p.speed[1] = 1
                p.falling = 0
                if p.anim != "Spin":
                    if not (buttons.buttonR.pressed() or buttons.buttonL.pressed()):
                        p.anim = "Idle"
                    else:
                        p.anim = "Walk"
            elif collision_type == "head":
                p.positions[1] = collider[1] + collider[3] + 1
                p.speed[1] = 0
            elif collision_type == "left_side":
                p.positions[0] = collider[0] - pw - 1
                p.speed[0] = 0
            elif collision_type == "right_side":
                p.positions[0] = collider[0] + collider[2] + 1
                p.speed[0] = 0
    
    p.update_camera(ph)
    draw_colliders(colliders, p.camera, debug)
    
    Cross.mirrorX = p.dir
    Cross.x, Cross.y = (p.positions[0] - 1) + p.camera[0], p.positions[1] + p.camera[1]
    
    animate(p, la)
    
    Cross.setFrame(frame)
    display.drawSprite(Cross)
    
    display.drawLine(0, 40 + p.camera[1], 72, 40 + p.camera[1], 2)
    
    if debug == 1:
        display.drawText("X: " + str(p.positions[0]), 2, 2, 1)
        display.drawText("Y: " + str(p.positions[1]), 2, 8, 1)
        display.drawText("xVel: " + str(round(p.speed[0])), 2, 14, 1)
        display.drawText("yVel: " + str(round(p.speed[1])), 2, 20, 1)
        display.drawText("Dash: " + str(p.dash), 2, 26, 1)
        display.drawText("Frame: " + str(frame), 2, 32, 1)