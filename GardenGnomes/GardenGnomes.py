import thumby
import math
import random

# --- Custom Weighted Random Selection (MicroPython compatible) ---
def weighted_choice(weights):
    total = sum(weights)
    r = random.randint(0, total - 1)
    upto = 0
    for i, w in enumerate(weights):
        if r < upto + w:
            return i
        upto += w
    return 0

# --- 4 Character Sprite Sets (8 Smooth Rotation Frames Each) ---
gnome_frames = [
    # 0. Normal Garden Gnome
    [
        bytearray([28, 62, 127, 119, 62, 54, 126, 66]),
        bytearray([14, 30, 63, 125, 126, 62, 28, 12]),
        bytearray([14, 30, 63, 255, 255, 63, 30, 14]),
        bytearray([12, 28, 62, 126, 125, 63, 30, 14]),
        bytearray([66, 126, 54, 62, 119, 127, 62, 28]),
        bytearray([24, 56, 124, 251, 254, 124, 56, 24]),
        bytearray([56, 124, 254, 255, 254, 124, 56, 24]),
        bytearray([24, 56, 124, 254, 251, 124, 56, 24])
    ],
    # 1. Mini Garden Gnome
    [
        bytearray([14, 30, 63, 59, 30, 27, 63, 33]),
        bytearray([8, 20, 46, 126, 126, 46, 20, 8]),
        bytearray([6, 14, 31, 127, 127, 31, 14, 6]),
        bytearray([4, 10, 23, 63, 63, 23, 10, 4]),
        bytearray([33, 63, 27, 30, 59, 63, 30, 14]),
        bytearray([16, 40, 92, 252, 252, 92, 40, 16]),
        bytearray([24, 56, 126, 255, 126, 56, 24, 12]),
        bytearray([12, 28, 63, 127, 63, 28, 12, 6])
    ],
    # 2. Big Garden Gnome
    [
        bytearray([60, 126, 255, 247, 126, 110, 255, 129]),
        bytearray([30, 63, 127, 255, 255, 127, 63, 30]),
        bytearray([28, 62, 127, 255, 255, 127, 62, 28]),
        bytearray([24, 56, 124, 254, 254, 124, 56, 24]),
        bytearray([129, 255, 110, 126, 247, 255, 126, 60]),
        bytearray([30, 63, 127, 255, 255, 127, 63, 30]),
        bytearray([56, 124, 254, 255, 255, 254, 124, 56]),
        bytearray([48, 104, 220, 254, 254, 220, 104, 48])
    ],
    # 3. Tall Gnome
    [
        bytearray([0, 8, 254, 111, 126, 232, 0, 0]),
        bytearray([32, 48, 250, 116, 30, 30, 4, 0]),
        bytearray([36, 60, 60, 20, 62, 28, 28, 8]),
        bytearray([4, 12, 15, 62, 52, 120, 52, 0]),
        bytearray([0, 0, 23, 126, 246, 127, 16, 0]),
        bytearray([0, 32, 120, 120, 46, 95, 12, 4]),
        bytearray([16, 56, 56, 124, 40, 60, 60, 36]),
        bytearray([0, 44, 62, 44, 124, 240, 48, 32])
    ]
]

# --- Interactive Object Sprites ---
spr_mud = bytearray([126, 255, 255, 126, 60, 24, 126, 255]) # 0: Mud Hazard
spr_mush = bytearray([28, 62, 127, 255, 54, 54, 28, 0])       # 1: Mushroom Spring
spr_log = bytearray([60, 126, 255, 219, 219, 255, 126, 60])   # 2: Log Cannon
spr_flower = bytearray([66, 126, 255, 126, 66, 24, 60, 24])   # 3: Magic Flower
spr_gem = bytearray([24, 60, 126, 255, 126, 60, 24, 0])       # 4: Crystal Gem
spr_tramp = bytearray([126, 60, 24, 126, 255, 126, 60, 0])    # 5: Super Trampoline
sprites = [spr_mud, spr_mush, spr_log, spr_flower, spr_gem, spr_tramp]

object_weights = [3, 10, 7, 10, 5, 4]

# --- Physics (real units: 10 px = 1 metre, 30 frames = 1 second) ---
PX_PER_M    = 10.0
SCORE_PX    = 6.5                           # px per score point (lower = counter runs faster)
GRAVITY     = 9.81 * PX_PER_M / 900.0      # px/frame^2  (~0.109)
GROUND_Y    = 28.0                          # y of the gnome's FEET when on the ground
DEG2RAD     = 3.14159 / 180.0
BOUNCE_MIN  = 1.2                           # slower impacts just land and roll
ROLL_K      = 9.5                           # deg/frame of tumble per px/frame of speed
HOP_SPEED   = 2.4                           # ground hop
SLAM_SPEED  = 4.0                           # mid-air dive
SLAM_CD     = 90                            # 3 seconds at 30 FPS (3 * 30 = 90 frames)[cite: 1]
CANNON_SPEED = 17.0
STOP_FRAMES = 30

# Per gnome:     NORMAL  MINI   BIG    TALL
TERM_VEL = [16.0,  11.5,  22.0,  12.5]      # terminal velocity (px/frame): bigger = heavier / less drag
REST     = [0.50,  0.65,  0.38,  0.45]      # bounciness
MU       = [0.22,  0.18,  0.20,  0.25]      # increased ground friction
LIFT     = [0.0,   0.0,   0.0,   0.0007]    # glide lift (tall gnome)
DRAG_K   = [GRAVITY / (v * v) for v in TERM_VEL]   # quadratic air drag: a = -k*|v|*v

# --- Distant Sprites (5x5) Zoomed OUT ---
sm_gnomes = [
    bytearray([4, 14, 31, 14, 4]), 
    bytearray([0, 4, 14, 4, 0]),    
    bytearray([14, 31, 31, 31, 14]),
    bytearray([4, 12, 28, 12, 4])
]
sm_sprites = [
    bytearray([28, 62, 62, 28, 0]), 
    bytearray([14, 31, 31, 8, 8]),   
    bytearray([30, 21, 21, 30, 0]), 
    bytearray([4, 14, 31, 4, 4]),
    bytearray([12, 30, 63, 30, 12]),
    bytearray([62, 28, 56, 28, 62])
]

# --- Game Variables ---
state = 0
menu_sel = 0
gnome_x = 0.0
gnome_y = 0.0
vx = 0.0
vy = 0.0
rot = 0.0        
rot_v = 0.0      
distance = 0
high_score = 0
objects = []

camera_x = 0.0
camera_y = 0.0
current_scale = 1.0  
slam_cooldown = 0  
cannon_timer = 0
cannon_holding = False
floaty_timer = 0
b_press_frames = 0
frame_count = 0

catapult_world_x = 10.0
beam_angle = -0.7      
sling_angle = 1.2      
launch_substate = 0   
power_val = 0.0
power_dir = 12.0      
angle_val = 0.0
angle_dir = 15.0      
auto_anim_timer = 0

selected_gnome = 0 
bg_on = True
stop_timer = 45       # 1.5 seconds at 30 FPS
death_world_x = 0.0
death_world_y = 0.0
bonus = 0
run_dist = 0
mud_timer = 0

def reset_game():
    global state, gnome_x, gnome_y, vx, vy, rot, rot_v, distance, objects
    global camera_x, camera_y, current_scale, slam_cooldown, cannon_timer, cannon_holding, floaty_timer, b_press_frames
    global beam_angle, sling_angle, launch_substate, power_val, power_dir, angle_val, angle_dir, auto_anim_timer, stop_timer, frame_count, death_world_x, death_world_y
    global bonus, run_dist, mud_timer
    state = 0
    gnome_x = catapult_world_x
    gnome_y = 28.0 
    vx = 0.0
    vy = 0.0
    rot = 0.0
    rot_v = 0.0
    distance = 0
    camera_x = 0.0
    camera_y = 0.0
    current_scale = 1.0
    slam_cooldown = 0
    cannon_timer = 0
    cannon_holding = False
    floaty_timer = 0
    b_press_frames = 0
    frame_count = 0
    beam_angle = -0.7
    sling_angle = 1.2
    launch_substate = 0
    power_val = 0.0
    power_dir = 12.0
    angle_val = 0.0
    angle_dir = 15.0
    auto_anim_timer = 0
    stop_timer = STOP_FRAMES
    bonus = 0
    run_dist = 0
    mud_timer = 0
    death_world_x = 0.0
    death_world_y = 0.0
    objects = []

reset_game()
thumby.display.setFPS(30)

while True:
    if state != 3:
        thumby.display.fill(0) 
    frame_count += 1

    if state == 0:
        thumby.display.drawText("GNOME FLY", 12, 0, 1)  
        
        char_names = ["NORM", "MINI", "BIG", "TALL"]
        menu_items = ["PLAY", "CHAR:" + char_names[selected_gnome], "BG:" + ("ON" if bg_on else "OFF"), "TUTORIAL"]
        
        for i in range(4):
            prefix = ">" if menu_sel == i else " "
            thumby.display.drawText(prefix + menu_items[i], 2, 9 + (i * 8), 1)

        thumby.display.blit(gnome_frames[selected_gnome][0], 56, 17, 8, 8, 0, 0, 0)

        if thumby.buttonU.justPressed():
            menu_sel = (menu_sel - 1) % 4
        if thumby.buttonD.justPressed():
            menu_sel = (menu_sel + 1) % 4

        if thumby.buttonA.justPressed():
            if menu_sel == 0:
                state = 1  
            elif menu_sel == 1:
                selected_gnome = (selected_gnome + 1) % 4
            elif menu_sel == 2:
                bg_on = not bg_on
            elif menu_sel == 3:
                state = 4  

        if thumby.buttonB.justPressed():
            selected_gnome = (selected_gnome + 1) % 4

    elif state == 4:
        thumby.display.drawText("HOW TO  1/3", 0, 0, 1)
        thumby.display.drawText("A:STOP POWER", 0, 8, 1)
        thumby.display.drawText("A:STOP ANGLE", 0, 16, 1)
        thumby.display.drawText("A/B:HOP/DIVE", 0, 24, 1)
        thumby.display.drawText("A:NEXT B:ESC", 0, 32, 1)

        if thumby.buttonA.justPressed():
            state = 5
        elif thumby.buttonB.justPressed():
            state = 0

    elif state == 5:
        thumby.display.drawText("ITEMS   2/3", 0, 0, 1)
        thumby.display.drawText("MUSH:SPRING", 0, 8, 1)
        thumby.display.drawText("FLOWER:BOOST", 0, 16, 1)
        thumby.display.drawText("MUD:SLOWS!", 0, 24, 1)
        thumby.display.drawText("A:NEXT B:ESC", 0, 32, 1)

        if thumby.buttonA.justPressed():
            state = 6
        elif thumby.buttonB.justPressed():
            state = 0

    elif state == 6:
        thumby.display.drawText("ITEMS   3/3", 0, 0, 1)
        thumby.display.drawText("LOG:CANNON", 0, 8, 1)
        thumby.display.drawText("GEM:+25 PTS", 0, 16, 1)
        thumby.display.drawText("TRAMP:BOUNCE", 0, 24, 1)
        thumby.display.drawText("A:NEXT B:ESC", 0, 32, 1)

        if thumby.buttonA.justPressed():
            state = 4
        elif thumby.buttonB.justPressed():
            state = 0

    elif state == 1:
        mast_x = 35
        pivot_y = 13
        beam_len_long = 16
        beam_len_short = 8
        sling_len = 8

        if launch_substate == 0:
            thumby.display.drawText("SET POWER", 10, 0, 1)
            
            power_val += power_dir
            if power_val >= 100.0:
                power_val = 100.0
                power_dir = -12.0
            elif power_val <= 0.0:
                power_val = 0.0
                power_dir = 12.0
                
            thumby.display.drawRectangle(4, 25, 64, 9, 1)
            fill_width = int((power_val / 100.0) * 60)
            if fill_width > 0:
                thumby.display.drawFilledRectangle(6, 27, fill_width, 5, 1)
                for tx_mark in range(10, 60, 10):
                    if tx_mark < fill_width + 6:
                        thumby.display.drawLine(tx_mark, 27, tx_mark, 31, 0)

            if thumby.buttonA.justPressed():
                launch_substate = 1

        elif launch_substate == 1:
            thumby.display.drawText("SET ANGLE", 10, 0, 1)
            
            angle_val += angle_dir
            if angle_val >= 100.0:
                angle_val = 100.0
                angle_dir = -15.0
            elif angle_val <= 0.0:
                angle_val = 0.0
                angle_dir = 15.0
                
            thumby.display.drawRectangle(4, 25, 64, 9, 1)
            fill_width = int((angle_val / 100.0) * 60)
            if fill_width > 0:
                thumby.display.drawFilledRectangle(6, 27, fill_width, 5, 1)
                for tx_mark in range(10, 60, 10):
                    if tx_mark < fill_width + 6:
                        thumby.display.drawLine(tx_mark, 27, tx_mark, 31, 0)

            if thumby.buttonA.justPressed():
                launch_substate = 2
                auto_anim_timer = 0

        elif launch_substate == 2:
            thumby.display.drawText("LAUNCHING", 9, 0, 1)
            auto_anim_timer += 1
            
            progress = auto_anim_timer * 0.18
            decay_factor = max(0.1, 1.0 - (auto_anim_timer * 0.015))
            
            beam_angle = -0.7 + (1.3 * math.sin(progress)) * decay_factor
            sling_angle = 1.2 + (math.cos(progress * 1.3) * 0.6)

            if auto_anim_timer > 22:
                angle_ratio = angle_val / 100.0
                launch_rad = (10.0 + angle_ratio * 60.0) * DEG2RAD   # 10..70 deg

                launch_mps = 10.0 + power_val * 0.2                  # 10..30 m/s
                launch_speed = launch_mps * PX_PER_M / 30.0          # px/frame

                vx = math.cos(launch_rad) * launch_speed
                vy = -math.sin(launch_rad) * launch_speed
                rot_v = launch_speed * 0.6
                state = 2

        thumby.display.drawLine(0, 36, 72, 36, 1) 
        thumby.display.drawRectangle(20, 32, 6, 4, 1)
        thumby.display.drawRectangle(44, 32, 6, 4, 1)
        thumby.display.drawLine(23, 32, mast_x, pivot_y, 1) 
        thumby.display.drawLine(47, 32, mast_x, pivot_y, 1) 
        thumby.display.drawLine(mast_x, pivot_y, mast_x, 32, 1) 
        
        tip_x = int(mast_x - math.cos(beam_angle) * beam_len_long)
        tip_y = int(pivot_y - math.sin(beam_angle) * beam_len_long)
        cw_x = int(mast_x + math.cos(beam_angle) * beam_len_short)
        cw_y = int(pivot_y + math.sin(beam_angle) * beam_len_short)
        
        thumby.display.drawLine(cw_x, cw_y, tip_x, tip_y, 1)
        thumby.display.drawRectangle(cw_x - 3, cw_y, 6, 8, 1)
        
        pouch_x = int(tip_x + math.sin(sling_angle) * sling_len)
        pouch_y = int(tip_y + math.cos(sling_angle) * sling_len)
        
        thumby.display.drawLine(tip_x, tip_y, pouch_x, pouch_y, 1)
        thumby.display.drawRectangle(pouch_x - 2, pouch_y - 2, 5, 5, 1) 
        
        gnome_x = catapult_world_x + ((pouch_x - mast_x) / current_scale)
        gnome_y = pouch_y + 4      # feet position
        thumby.display.blit(gnome_frames[selected_gnome][0], pouch_x - 4, pouch_y - 4, 8, 8, 0, 0, 0)

    elif state == 2 or state == 3:
        if state == 2:
            if slam_cooldown > 0: slam_cooldown -= 1
            if floaty_timer > 0: floaty_timer -= 1
            if b_press_frames > 0: b_press_frames -= 1
            if mud_timer > 0: mud_timer -= 1

            if thumby.buttonB.justPressed():
                if b_press_frames > 0:
                    reset_game()
                    continue
                else:
                    b_press_frames = 30

            if cannon_holding:
                cannon_timer -= 1
                vx = 0.0
                vy = 0.0
                rot_v = 0.0
                if cannon_timer <= 0:
                    cannon_holding = False
                    cannon_rad = (14.0 + random.random() * 6.0) * DEG2RAD
                    vx = math.cos(cannon_rad) * CANNON_SPEED
                    vy = -math.sin(cannon_rad) * CANNON_SPEED
                    rot_v = 14.0
            else:
                # A/B: hop when on the ground, dive-slam when airborne
                if (thumby.buttonA.justPressed() or thumby.buttonB.justPressed()) and slam_cooldown == 0:
                    if gnome_y >= GROUND_Y - 0.5:
                        vy = -HOP_SPEED
                    else:
                        if vy < 0: vy = 0.0
                        vy += SLAM_SPEED
                    rot_v += 10
                    slam_cooldown = SLAM_CD

                # forces: gravity + quadratic air drag (+ glide lift for TALL)
                g = GRAVITY * (0.5 if floaty_timer > 0 else 1.0)
                spd = math.sqrt(vx * vx + vy * vy)
                k = DRAG_K[selected_gnome]
                lift = 0.0
                if vy > 0:
                    lift = LIFT[selected_gnome] * vx * vx
                    if lift > g * 0.8: lift = g * 0.8

                vx -= k * spd * vx
                vy += g - lift - k * spd * vy

                if vx > 22.0: vx = 22.0
                if vy > 22.0: vy = 22.0

                gnome_x += vx
                gnome_y += vy
                rot += rot_v
                rot_v *= 0.998          # spin is conserved in the air

            # ground contact: bounce with friction, then roll to a stop
            if not cannon_holding and gnome_y >= GROUND_Y and vy >= 0:
                gnome_y = GROUND_Y
                if vy > BOUNCE_MIN:
                    e = REST[selected_gnome]
                    dv = MU[selected_gnome] * (1.0 + e) * vy     # friction impulse during impact
                    if dv > vx * 0.6: dv = vx * 0.6
                    vx -= dv
                    vy = -vy * e
                    rot_v = rot_v * 0.5 + min(vx * ROLL_K, 40.0) * 0.5
                    stop_timer = STOP_FRAMES
                else:
                    vy = 0.0
                    decel = MU[selected_gnome] * GRAVITY
                    if mud_timer > 0: decel = 0.10
                    vx -= decel
                    if vx < 0: vx = 0.0
                    rot_v = min(vx * ROLL_K, 40.0)               # rolling without slipping
                    if vx < 0.15:
                        vx = 0.0
                        stop_timer -= 1
                        if stop_timer <= 0:
                            death_world_x = gnome_x
                            death_world_y = gnome_y
                            state = 3
                    else:
                        stop_timer = STOP_FRAMES

            target_scale = 1.0 if gnome_y >= -15 else 0.45
            current_scale += (target_scale - current_scale) * 0.15

            camera_x = gnome_x - (15 / current_scale)

            if vy < 0:
                target_camera_y = gnome_y - (20 / current_scale)
            else:
                target_camera_y = gnome_y - (10 / current_scale)

            camera_y += (target_camera_y - camera_y) * 0.2
            if camera_y > 0: camera_y = 0

            cur_run = int((gnome_x - catapult_world_x) / SCORE_PX)
            if cur_run > run_dist: run_dist = cur_run
            distance = run_dist + bonus
            if distance > high_score: high_score = distance

            if len(objects) < 12:
                last_x = objects[-1]['x'] if objects else camera_x + 72
                new_x = last_x + random.randint(90, 190)
                rand_type = weighted_choice(object_weights)
                objects.append({'x': new_x, 'type': rand_type, 'hit': False})

            objects = [o for o in objects if o['x'] > camera_x - 15]

        ground_screen_y = int((28 - camera_y) * current_scale)
        if ground_screen_y > 38: ground_screen_y = 38
        if ground_screen_y < 20: ground_screen_y = 35

        if bg_on:
            alt = int(28 - gnome_y)
            
            house_scroll_offset = 0
            if alt > 55:
                house_scroll_offset = int((alt - 55) * 0.7)
                if house_scroll_offset > 45: house_scroll_offset = 45

            if alt <= 75:
                far_offset = (int(camera_x) * 3) // 100 % 60
                for i in range(-60, 140, 60):
                    fx = int((i - far_offset) * current_scale)
                    fy = int((14 - camera_y * 0.05) * current_scale) - house_scroll_offset
                    if fy < ground_screen_y + 10:
                        thumby.display.drawRectangle(fx, fy + 3, 12, 5, 1)
                        thumby.display.drawLine(fx, fy + 3, fx + 6, fy, 1)
                        thumby.display.drawLine(fx + 6, fy, fx + 12, fy + 3, 1)

                fence_base_y = ground_screen_y - 6 - house_scroll_offset
                scenery_base_y = fence_base_y - 14  

                mid_offset = (int(camera_x) * 12) // 100 % 56
                for i in range(-56, 130, 56):
                    hx = int((i - mid_offset) * current_scale)
                    hy = int((scenery_base_y - camera_y * 0.15) * current_scale)
                    if hy < ground_screen_y + 10:
                        
                        thumby.display.drawFilledRectangle(hx - 2, hy - 4, 52, 20, 0)

                        thumby.display.drawRectangle(hx, hy + 5, 12, 10, 1) 
                        thumby.display.drawLine(hx, hy + 5, hx + 6, hy, 1)     
                        thumby.display.drawLine(hx + 6, hy, hx + 12, hy + 5, 1) 
                        thumby.display.drawRectangle(hx + 8, hy - 3, 3, 6, 1)  
                        thumby.display.drawRectangle(hx + 4, hy + 7, 4, 4, 1)  
                        thumby.display.setPixel(hx + 6, hy + 9, 1)            

                        px = hx + 18
                        thumby.display.drawLine(px + 3, hy + 12, px + 3, hy + 15, 1) 
                        thumby.display.drawLine(px + 3, hy + 2, px, hy + 7, 1)       
                        thumby.display.drawLine(px + 3, hy + 2, px + 6, hy + 7, 1)   
                        thumby.display.drawLine(px, hy + 7, px + 6, hy + 7, 1)
                        thumby.display.drawLine(px + 3, hy + 5, px - 2, hy + 11, 1)  
                        thumby.display.drawLine(px + 3, hy + 5, px + 8, hy + 11, 1)  
                        thumby.display.drawLine(px - 2, hy + 11, px + 8, hy + 11, 1)

                        tx = hx + 30
                        thumby.display.drawLine(tx + 5, hy + 8, tx + 3, hy + 15, 1) 
                        thumby.display.drawLine(tx + 2, hy + 8, tx + 8, hy + 8, 1)   
                        thumby.display.drawLine(tx, hy + 6, tx + 2, hy + 8, 1)
                        thumby.display.drawLine(tx + 8, hy + 8, tx + 10, hy + 6, 1)
                        thumby.display.drawLine(tx, hy + 6, tx + 4, hy + 3, 1)
                        thumby.display.drawLine(tx + 4, hy + 3, tx + 10, hy + 6, 1)
                        thumby.display.setPixel(tx + 3, hy + 5, 1) 

                        cx = hx + 43
                        thumby.display.drawRectangle(cx, hy + 4, 14, 11, 1) 
                        thumby.display.drawLine(cx, hy + 4, cx + 7, hy - 2, 1) 
                        thumby.display.drawLine(cx + 7, hy - 2, cx + 14, hy + 4, 1) 
                        thumby.display.drawRectangle(cx + 2, hy + 6, 4, 4, 1)  
                        thumby.display.drawRectangle(cx + 8, hy + 6, 4, 4, 1)  
                        thumby.display.drawRectangle(cx + 5, hy + 10, 4, 5, 1) 

                fence_offset = (int(camera_x) * 50) // 100 % 12
                for fx_pos in range(-12, 84, 12):
                    f_draw_x = fx_pos - fence_offset
                    thumby.display.drawLine(f_draw_x, fence_base_y, f_draw_x, fence_base_y + 6, 1)
                    thumby.display.setPixel(f_draw_x, fence_base_y - 1, 1)
                    thumby.display.drawLine(f_draw_x, fence_base_y + 2, f_draw_x + 12, fence_base_y + 2, 1)
                    thumby.display.drawLine(f_draw_x, fence_base_y + 5, f_draw_x + 12, fence_base_y + 5, 1)
                    
            if alt >= 75 and alt <= 150:
                cloud_parallax = (int(camera_x) * 5) // 100 % 80
                for cx_p in [10, 30, 50, 70]:
                    c_x = (cx_p - cloud_parallax) % 80 - 10
                    c_y = (cx_p * 3) % 25 + 2
                    
                    thumby.display.drawLine(c_x + 3, c_y + 4, c_x + 12, c_y + 4, 1)
                    thumby.display.setPixel(c_x + 2, c_y + 3, 1)
                    thumby.display.setPixel(c_x + 13, c_y + 3, 1)
                    thumby.display.setPixel(c_x + 1, c_y + 2, 1)
                    thumby.display.setPixel(c_x + 14, c_y + 2, 1)
                    thumby.display.drawLine(c_x + 2, c_y + 1, c_x + 5, c_y + 1, 1)
                    thumby.display.drawLine(c_x + 7, c_y, c_x + 11, c_y, 1)
                    thumby.display.setPixel(c_x + 6, c_y + 1, 1)
                    thumby.display.setPixel(c_x + 12, c_y + 1, 1)
                    thumby.display.setPixel(c_x + 5, c_y + 2, 1)
                    thumby.display.setPixel(c_x + 6, c_y + 3, 1)
                    
            if alt >= 100 and alt <= 210:
                star_offset = (int(camera_x) * 2) // 100 % 72
                for sx_p in [10, 25, 42, 58]:
                    p_x = (sx_p - star_offset) % 72
                    p_y = (sx_p * 2) % 35  
                    thumby.display.setPixel(p_x, p_y, 1)
                    
            if alt > 190 and alt <= 270:
                star_offset = (int(camera_x) * 3) // 100 % 72
                for sx_p in [15, 38, 55]:
                    p_x = (sx_p - star_offset) % 72
                    p_y = (sx_p * 5) // 2 % 35  
                    thumby.display.drawFilledRectangle(p_x, p_y, 2, 2, 1)
            elif alt > 270:
                star_offset = (int(camera_x) * 4) // 100 % 72
                for sx_p in [20, 50]:
                    p_x = (sx_p - star_offset) % 72
                    p_y = (sx_p * 9) // 5 % 35  
                    thumby.display.drawFilledRectangle(p_x, p_y, 3, 3, 1)

        alt_check = int(28 - gnome_y)
        if alt_check <= 50:
            thumby.display.drawLine(0, ground_screen_y, 72, ground_screen_y, 1)
            
            dirt_offset = int(camera_x * current_scale) % 8
            for d_x in range(0, 80, 8):
                dx_draw = d_x - dirt_offset
                thumby.display.drawLine(dx_draw, ground_screen_y + 2, dx_draw + 2, ground_screen_y + 2, 1)
                thumby.display.setPixel(dx_draw + 5, ground_screen_y + 3, 1)

            for gx_pos in range(0, 72, 12):
                tuft_x = (gx_pos - int(camera_x * current_scale)) % 72
                
                thumby.display.drawLine(tuft_x, ground_screen_y, tuft_x, ground_screen_y - 3, 1) 
                thumby.display.setPixel(tuft_x - 1, ground_screen_y - 1, 1)                      
                thumby.display.setPixel(tuft_x - 2, ground_screen_y - 2, 1)                      
                thumby.display.setPixel(tuft_x + 1, ground_screen_y - 1, 1)                      
                thumby.display.setPixel(tuft_x + 2, ground_screen_y - 2, 1)                      
                
                thumby.display.drawLine(tuft_x + 6, ground_screen_y, tuft_x + 6, ground_screen_y - 2, 1)
                thumby.display.setPixel(tuft_x + 7, ground_screen_y - 1, 1)

        is_zoomed_out = current_scale < 0.75
        size = 5 if is_zoomed_out else 8
        active_sprites = sm_sprites if is_zoomed_out else sprites

        for o in objects:
            sx = int((o['x'] - camera_x) * current_scale)
            sy = ground_screen_y - size
            
            if -10 < sx < 80 and -10 < sy < 45:
                thumby.display.blit(active_sprites[o['type']], sx, sy, size, size, 0, 0, 0)

                if (state == 2 and not o['hit'] and not cannon_holding and gnome_y >= GROUND_Y - 3
                        and o['x'] - gnome_x < 7 and gnome_x - o['x'] < 7 + vx):
                    o['hit'] = True
                    t = o['type']
                    impact = vy if vy > 0 else 0.0
                    if t == 0:   # Mud: sticky, drags speed away
                        vx *= 0.3
                        mud_timer = 25
                        if vx < 0.6:
                            death_world_x = gnome_x
                            death_world_y = gnome_y
                            state = 3
                    elif t == 1: # Mushroom: springy rebound
                        gnome_y = GROUND_Y - 2
                        vy = -min(max(impact * 0.9, 3.5), 8.5)
                        vx += 0.8
                        rot_v += 6
                    elif t == 2: # Log Cannon
                        cannon_holding = True
                        cannon_timer = 15
                        gnome_x = o['x']
                    elif t == 3: # Magic Flower
                        gnome_y = GROUND_Y - 2
                        if selected_gnome == 2:
                            floaty_timer = 90
                            vy = -3.0
                        else:
                            vy = -5.5
                            vx += 2.5
                            rot_v += 8
                    elif t == 4: # Gem
                        bonus += 25
                    elif t == 5: # Trampoline
                        gnome_y = GROUND_Y - 2
                        vy = -min(max(impact * 0.95, 5.0), 9.5)
                        rot_v += 6

        if state != 3:
            spin_frame = int(abs(rot) / 22.5) % 8
            g_sprite = sm_gnomes[selected_gnome] if is_zoomed_out else gnome_frames[selected_gnome][spin_frame]
            gx = int((gnome_x - camera_x) * current_scale)
            gy = int((gnome_y - camera_y) * current_scale) - size
            if state == 2 and not is_zoomed_out and alt_check <= 40:
                sh_w = 8 - alt_check // 6          # shadow shrinks with height
                if sh_w < 2: sh_w = 2
                sh_x = gx + 4 - sh_w // 2
                thumby.display.drawLine(sh_x, ground_screen_y + 1, sh_x + sh_w, ground_screen_y + 1, 1)
            thumby.display.blit(g_sprite, gx, gy, size, size, -1, 0, 0)

        thumby.display.drawText("D:" + str(distance), 0, 0, 1)
        
        hi_text = "H:" + str(high_score)
        thumby.display.drawText(hi_text, 72 - (len(hi_text) * 6), 0, 1)
        
        current_altitude = int(28 - gnome_y)
        if current_altitude > 10 and state != 3:
            thumby.display.drawText("A:" + str(int(current_altitude / PX_PER_M)) + "M", 0, 8, 1)
        
        thumby.display.drawLine(31, 22, 41, 22, 0) 
        if slam_cooldown == 0: 
            thumby.display.drawLine(33, 22, 39, 22, 1) 
        else: 
            thumby.display.setPixel(31 + ((SLAM_CD - slam_cooldown) * 8) // SLAM_CD, 22, 1)

        if state == 3:
            thumby.display.drawFilledRectangle(0, 0, 72, 40, 0)
            thumby.display.drawRectangle(0, 0, 72, 40, 1)
            thumby.display.drawText("GAME OVER", 12, 6, 1)
            thumby.display.drawText("SCORE:" + str(distance), 12, 16, 1)
            thumby.display.drawText("HI:" + str(high_score), 12, 26, 1)

            if thumby.buttonA.justPressed() or thumby.buttonB.justPressed(): 
                reset_game()

    th_display = thumby.display.update()