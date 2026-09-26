# FlightSim.py
# A mostly-featured flight simulator for Thumby, built on top of (and
# fixing/extending) TinyCircuits' "Foxgine" 3D tech demo.
#
# Controls:
#   D-Pad Up/Down    - pitch (climb / dive)
#   D-Pad Left/Right - turn (yaw + bank)
#   A                - throttle up
#   B                - throttle down / brake
#
# Take off down the runway, fly through the 4 checkpoint gates, then try
# to bring it back down on the runway gently (low speed, wings level,
# nose level) for a landing. Stall by flying too slow, or crash into
# the ground/mountains, and you'll need to restart.

import thumbyButton as buttons
from math import sin, cos
from sys import path as syspath
syspath.insert(0, '/Games/FlightSim')

from thumbyGrayscale import display
from engine3d import Renderer
from plane import Plane
import world

W, H = 72, 40
CX, CY = W // 2, H // 2
DT = 1 / 30

display.setFont("/lib/font3x5.bin", 3, 5, 1)
display.setFPS(30)

renderer = Renderer(display, W, H, fov=55, near=0.2)
renderer.fill_mode = False  # wireframe by default - lighter on Thumby's CPU

STATIC_ENTITIES = world.build_static_entities()

STATE_MENU = 0
STATE_FLYING = 1
STATE_DONE = 2  # crashed or landed

state = STATE_MENU
plane = None
checkpoints = None
flash_timer = 0.0


def new_game():
    global plane, checkpoints
    plane = Plane(world.START_POS, world.START_YAW)
    checkpoints = world.build_checkpoints()


def update_checkpoints():
    for cp in checkpoints:
        if cp.passed:
            continue
        dx = plane.pos[0] - cp.pos[0]
        dy = plane.pos[1] - cp.pos[1]
        dz = plane.pos[2] - cp.pos[2]
        if dx * dx + dy * dy + dz * dz < cp.radius * cp.radius:
            cp.passed = True


def score():
    return sum(1 for cp in checkpoints if cp.passed)


def draw_hud():
    display.drawText(str(int(plane.pos[1])), 2, 2, 3)
    display.drawText("ALT", 2, 8, 2)

    spd = str(int(plane.speed * 10))
    display.drawText(spd, W - 4 * len(spd) - 2, 2, 3)
    display.drawText("SPD", W - 20, 8, 2)

    heading = int((plane.yaw * 180 / 3.14159265) % 360)
    display.drawText(str(heading), 2, H - 12, 3)
    display.drawText("HDG", 2, H - 6, 2)

    cp_text = str(score()) + "/" + str(len(checkpoints))
    display.drawText(cp_text, W - 4 * len(cp_text) - 2, H - 6, 3)

    if plane.stalling:
        if (flash_timer % 0.6) < 0.3:
            display.drawText("STALL", CX - 9, 18, 3)


def draw_horizon():
    # a simple artificial-horizon line: shifts with pitch, tilts with roll,
    # using the same convention as the camera in engine3d.py
    pitch_px = plane.pitch * 22
    sr, cr = sin(plane.roll), cos(plane.roll)
    half_w = 30
    x0 = -half_w
    y0 = pitch_px
    x1 = half_w
    y1 = pitch_px
    x0r = x0 * cr - y0 * sr
    y0r = x0 * sr + y0 * cr
    x1r = x1 * cr - y1 * sr
    y1r = x1 * sr + y1 * cr
    display.drawLine(CX + int(x0r), CY - int(y0r), CX + int(x1r), CY - int(y1r), 3)


def draw_menu():
    display.drawText("FOX FLIGHT SIM", 2, 4, 3)
    display.drawText("U/D: pitch", 4, 14, 2)
    display.drawText("L/R: turn", 4, 20, 2)
    mode = "FILL" if renderer.fill_mode else "WIRE"
    display.drawText("B: style " + mode, 4, 26, 2)
    if (flash_timer % 1.0) < 0.6:
        display.drawText("Press A to fly", 4, 33, 3)


def draw_end_screen():
    if plane.landed:
        display.drawText("LANDED!", 16, 10, 3)
        display.drawText("SCORE " + str(score()) + "/" + str(len(checkpoints)), 6, 20, 2)
    else:
        display.drawText("CRASHED!", 12, 10, 3)
    if (flash_timer % 1.0) < 0.6:
        display.drawText("Press A: retry", 4, 30, 2)


while True:
    display.update()
    display.fill(0)
    flash_timer += DT

    if state == STATE_MENU:
        draw_menu()
        if buttons.buttonB.justPressed():
            renderer.fill_mode = not renderer.fill_mode
        if buttons.buttonA.justPressed():
            new_game()
            state = STATE_FLYING

    elif state == STATE_FLYING:
        plane.update(DT, buttons)
        update_checkpoints()

        cam_pos = plane.pos
        entities = STATIC_ENTITIES + world.checkpoint_entities(checkpoints)
        renderer.draw(entities, cam_pos, plane.yaw, plane.pitch, plane.roll)

        draw_horizon()
        draw_hud()

        if plane.crashed or plane.landed:
            state = STATE_DONE

    elif state == STATE_DONE:
        cam_pos = plane.pos
        entities = STATIC_ENTITIES + world.checkpoint_entities(checkpoints)
        renderer.draw(entities, cam_pos, plane.yaw, plane.pitch, plane.roll)
        draw_end_screen()

        if buttons.buttonA.justPressed():
            state = STATE_MENU
