import thumby
import time
import random

# random.seed(2)

# --- CONFIG ---
SPRITE_SIZE = 9
GAP = 9
CELL = SPRITE_SIZE + GAP

WORLD_W = 20
WORLD_H = 20

MOVE_MIN = 5
MOVE_MAX = 25
GAME_DURATION = 30

FRAME_TIME = 50 # real device
# FRAME_TIME = 20 # emulator


SCREEN_W = 72
SCREEN_H = 40

DIRS = {
    "UP":    (0, -1, thumby.buttonU),
    "DOWN":  (0,  1, thumby.buttonD),
    "LEFT":  (-1, 0, thumby.buttonL),
    "RIGHT": (1,  0, thumby.buttonR),
}

# ---------------------------------------------------------
# Shape bitmaps
# ---------------------------------------------------------
# BITMAP: width: 9, height: 9
bitmap15 = bytearray([34,81,138,68,32,16,8,132,66,
            0,0,0,0,0,0,1,0,0])
SHAPE_BITMAPS = [
    bytearray([56,198,130,1,1,1,130,198,56,
           0,0,0,1,1,1,0,0,0]),  # circle
    bytearray([0,0,255,255,255,255,255,0,0,
           0,0,1,1,1,1,1,0,0]),  # tall rectangle
    bytearray([124,124,124,124,124,124,124,124,124,
           0,0,0,0,0,0,0,0,0]),  # phat rectangle
    bytearray([255,255,255,255,255,255,255,255,255,
           1,1,1,1,1,1,1,1,1]),  # square
    bytearray([56,56,56,255,255,255,56,56,56,
           0,0,0,1,1,1,0,0,0]),  # plus sign
    bytearray([131,199,238,124,56,124,238,199,131,
           1,1,0,0,0,0,0,1,1]),  # x sign
    bytearray([0,192,240,252,255,252,240,192,0,
           1,1,1,1,1,1,1,1,1]),  # triangle pointing up
    bytearray([255,254,254,124,124,56,56,16,16,
           1,0,0,0,0,0,0,0,0]),  # triangle pointing right
    bytearray([16,16,56,56,124,124,254,254,255,
           0,0,0,0,0,0,0,0,1]),  # triangle pointing left
    bytearray([16,56,124,254,255,254,124,56,16,
           0,0,0,0,1,0,0,0,0]),  # diamond
    bytearray([0,34,34,34,136,136,136,0,0,
            0,0,0,0,0,0,0,0,0]),  # horizontal segments
    bytearray([0,112,0,14,0,112,0,14,0,
            0,0,0,0,0,0,0,0,0]),  # vertical segments
    bytearray([0,32,6,194,12,24,144,2,0,
            0,0,0,0,0,0,0,0,0]),  # sum random shit 1
    bytearray([0,8,64,194,10,24,32,134,2,
            0,0,0,0,0,0,0,0,1]),  # sum random shit 2
    bytearray([34,81,138,68,32,16,8,132,66,
            0,0,0,0,0,0,1,0,0]),  # zig-zag
]

# Pre‑create sprite objects for speed
SHAPES = [
    thumby.Sprite(SPRITE_SIZE, SPRITE_SIZE, bytearray(bitmap))
    for bitmap in SHAPE_BITMAPS
]

def pick_random_direction_and_shape():
    name = random.choice(list(DIRS.keys()))
    dx, dy, _ = DIRS[name]
    speed = random.randint(MOVE_MIN, MOVE_MAX)
    shape = random.choice(SHAPES)
    return name, dx, dy, speed, shape

def wait_for_button():
    while True:
        if thumby.buttonA.justPressed():
            return
        if thumby.buttonB.justPressed():
            thumby.reset()
        time.sleep_ms(FRAME_TIME)

def get_visible_direction(dx, dy):
    if dx > 0: return "LEFT"
    if dx < 0: return "RIGHT"
    if dy > 0: return "UP"
    if dy < 0: return "DOWN"
    return None

def game_loop():
    score = 0

    cam_x = (WORLD_W * CELL) // 2 - SCREEN_W // 2
    cam_y = (WORLD_H * CELL) // 2 - SCREEN_H // 2

    dir_name, dx, dy, speed, current_shape = pick_random_direction_and_shape()

    start_time = time.ticks_ms()
    last_time = start_time

    while True:
        now = time.ticks_ms()
        dt = (now - last_time) / 1000.0
        last_time = now

        if (now - start_time) / 1000 >= GAME_DURATION:
            return score

        cam_x += dx * speed * dt
        cam_y += dy * speed * dt

        pressed = None
        for name, (_, _, btn) in DIRS.items():
            if btn.justPressed():
                pressed = name

        if pressed:
            if pressed == get_visible_direction(dx, dy):
                score += 1
                thumby.audio.play(400, 60)
            else:
                score -= 2
                thumby.audio.play(1500, 200)
            dir_name, dx, dy, speed, current_shape = pick_random_direction_and_shape()

        # --- DRAW ---
        thumby.display.fill(0)

        gx_min = int((cam_x - SPRITE_SIZE) // CELL)
        gx_max = int((cam_x + SCREEN_W) // CELL)
        gy_min = int((cam_y - SPRITE_SIZE) // CELL)
        gy_max = int((cam_y + SCREEN_H) // CELL)

        for gy in range(gy_min, gy_max + 1):
            for gx in range(gx_min, gx_max + 1):
                sx = gx * CELL
                sy = gy * CELL

                x = int(sx - cam_x)
                y = int(sy - cam_y)

                if x + SPRITE_SIZE <= 0 or x >= SCREEN_W:
                    continue
                if y + SPRITE_SIZE <= 0 or y >= SCREEN_H:
                    continue

                current_shape.x = x
                current_shape.y = y
                thumby.display.drawSprite(current_shape)


        thumby.display.update()
        time.sleep_ms(FRAME_TIME)
        
def menu():
    
    ### INSTRUCTIONS
    thumby.display.drawText("30 seconds", 8, 6, 1)
    thumby.display.drawText("to", 28, 17, 1)
    thumby.display.update()
    time.sleep(1.0)
    thumby.display.fill(0)
    thumby.display.drawText("match all", 8, 6, 1)
    thumby.display.drawText("the ", 28, 15, 1)
    thumby.display.drawText("directions", 4, 24, 1)
    thumby.display.update()
    time.sleep(1.0)
    thumby.display.fill(0)
    ### END OF INSTRUCTIONS
    
    # BITMAP: width: 72, height: 80
    grubol_bitmap = bytearray([255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,63,159,223,207,239,239,239,247,247,247,247,239,239,239,239,239,239,143,63,255,255,255,255,255,255,255,
           255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,3,253,254,255,255,223,189,191,255,255,251,255,255,255,255,255,255,255,255,255,255,254,0,255,255,255,255,255,255,
           255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,127,127,191,159,223,223,207,239,224,207,191,63,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,127,191,207,32,127,255,255,255,255,255,
           255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,7,243,251,249,253,29,238,242,250,253,254,255,255,255,255,255,255,255,255,255,255,255,254,254,254,254,253,253,255,253,253,253,253,253,255,253,254,254,255,255,255,254,240,133,125,253,1,
           255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,63,191,191,188,3,31,224,254,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,0,193,60,
           255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,252,243,247,243,248,252,251,231,191,127,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,127,15,240,254,254,
           255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,254,249,247,135,47,239,239,239,207,223,223,223,223,223,223,223,31,223,223,223,223,223,223,239,239,239,239,231,119,151,227,251,249,252,254,255,255,255,255,
           255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,252,241,135,127,255,255,255,255,255,255,255,255,0,255,255,255,255,255,255,255,127,31,199,241,252,255,255,255,255,255,255,255,255,255,255,
           255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,159,143,167,180,177,183,183,183,183,183,151,199,192,151,183,183,183,183,183,183,176,183,151,199,255,255,255,255,255,255,255,255,255,255,255,
           255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255])
    
    # BITMAP: width: 72, height: 80
    grubol_inverted_bitmap = bytearray([0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,192,96,32,48,16,16,16,8,8,8,8,16,16,16,16,16,16,112,192,0,0,0,0,0,0,0,
           0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,252,2,1,0,0,32,66,64,0,0,4,0,0,0,0,0,0,0,0,0,0,1,255,0,0,0,0,0,0,
           0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,128,128,64,96,32,32,48,16,31,48,64,192,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,128,64,48,223,128,0,0,0,0,0,
           0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,248,12,4,6,2,226,17,13,5,2,1,0,0,0,0,0,0,0,0,0,0,0,1,1,1,1,2,2,0,2,2,2,2,2,0,2,1,1,0,0,0,1,15,122,130,2,254,
           0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,192,64,64,67,252,224,31,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,255,62,195,
           0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,3,12,8,12,7,3,4,24,64,128,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,128,240,15,1,1,
           0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,6,8,120,208,16,16,16,48,32,32,32,32,32,32,32,224,32,32,32,32,32,32,16,16,16,16,24,136,104,28,4,6,3,1,0,0,0,0,
           0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,3,14,120,128,0,0,0,0,0,0,0,0,255,0,0,0,0,0,0,0,128,224,56,14,3,0,0,0,0,0,0,0,0,0,0,
           0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,96,112,88,75,78,72,72,72,72,72,104,56,63,104,72,72,72,72,72,72,79,72,104,56,0,0,0,0,0,0,0,0,0,0,0,
           0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0])
    
    for i in range(41):
        grubol_sprite = thumby.Sprite(72, 80,
                                        grubol_bitmap, 0, 0-40+i)
        
        thumby.display.fill(0)
        thumby.display.drawSprite(grubol_sprite)
        thumby.display.update()
        time.sleep(0.02)
    
    time.sleep(0.5)
    thumby.display.drawText("3", 18, 2, 0)
    thumby.display.update()
    time.sleep(0.5)
    thumby.display.drawSprite(grubol_sprite)
    thumby.display.drawText("Gruboli", 2, 2, 0)
    thumby.display.update()
    time.sleep(0.5)
    thumby.display.drawSprite(grubol_sprite)
    thumby.display.drawText("Milo", 2, 2, 0)
    thumby.display.update()
    time.sleep(0.5)
    thumby.display.drawSprite(grubol_sprite)
    thumby.display.drawText("Move", 2, 2, 0)
    thumby.display.update()
    time.sleep(0.5)
    thumby.display.drawSprite(grubol_sprite)
    thumby.display.drawText("Press", 2, 2, 0)
    thumby.display.drawText("A to", 2, 11, 0)
    thumby.display.drawText("start", 2, 20, 0)
    thumby.display.update()
    time.sleep(0.5)
    grubol_sprite = thumby.Sprite(72, 80,
                                        grubol_inverted_bitmap, 0, 0)
    thumby.display.drawSprite(grubol_sprite)
    thumby.display.drawText("Press", 2, 2, 1)
    thumby.display.drawText("A to", 2, 11, 1)
    thumby.display.drawText("start", 2, 20, 1)
    thumby.display.update()
    time.sleep(0.5)

def main():
    
    is_menu = True
    
    while True:
        
        if is_menu:
            menu()
            while is_menu:
                if thumby.buttonA.justPressed():
                    is_menu = False
        
        score = game_loop()

        thumby.display.fill(0)
        thumby.display.drawText("Time! Score:", 2, 5, 1)
        thumby.display.drawText(str(score), 28, 16, 1)
        thumby.display.drawText("A=restart", 10, 27, 1)
        thumby.display.update()

        wait_for_button()

main()
