import thumby
import random
import time

# Set up screen frames per second (FPS)
thumby.display.setFPS(30)

# Game States: "START_PAGE", "RACING", "GAME_OVER"
game_state = "START_PAGE"

# Performance & Layout Variables
score = 0
speed_factor = 0.0      # For road motion simulation
enemy_speed = 0.8       # Easier starting speed

# Player Attributes
player_x = 0            # Offset from center of road (-25 to 25)
player_y = 31

# Rival Attributes
enemy_road_x = 0        # Target position on the road path (-20 to 20)
enemy_z = 0             # 0 = horizon (far away), 40 = screen bottom (close)

# --- RENDERING ENGINE FUNCTIONS ---

def draw_start_page():
    thumby.display.drawRectangle(0, 0, 72, 40, 1)
    
    # Updated title to "F1 DRIVE" and centered perfectly
    thumby.display.drawText("F1 DRIVE", 14, 5, 1)
    thumby.display.drawText("BY REHAAN", 11, 16, 1)
    
    # Flashing prompt sequence
    if int(time.ticks_ms() / 350) % 2 == 0:
        thumby.display.drawText("PRESS A", 16, 28, 1)

def draw_pseudo_3d_road(offset):
    # Horizon line
    thumby.display.drawLine(0, 14, 72, 14, 1)
    
    # Draw converging road perspective lines
    for y in range(14, 40):
        progress = (y - 14) / 26.0
        road_width = int(8 + (44 * progress))
        center_x = 36 - int(offset * progress)
        
        left_bound = center_x - (road_width // 2)
        right_bound = center_x + (road_width // 2)
        
        # FIXED LINE 50: Proper boundary layout checks
        if left_bound >= 0 and left_bound < 72:
            thumby.display.setPixel(left_bound, y, 1)
        if right_bound >= 0 and right_bound < 72:
            thumby.display.setPixel(right_bound, y, 1)
            
        # Moving motion track ticks along the shoulders
        if int(y + speed_factor) % 6 < 3:
            if left_bound - 1 >= 0: thumby.display.setPixel(left_bound - 1, y, 1)
            if right_bound + 1 < 72: thumby.display.setPixel(right_bound + 1, y, 1)

def draw_retro_player(steer_dir):
    bx = 32
    by = player_y
    
    # Main Engine Core
    thumby.display.drawRectangle(bx, by, 8, 4, 1)
    thumby.display.drawRectangle(bx+2, by-4, 4, 4, 1) # Cockpit
    thumby.display.drawLine(bx+3, by-6, bx+4, by-6, 1) # Nose
    
    # Rear Wing
    thumby.display.drawLine(bx-3, by, bx+10, by, 1)
    thumby.display.drawRectangle(bx-3, by-2, 2, 4, 1)
    thumby.display.drawRectangle(bx+9, by-2, 2, 4, 1)
    
    # Front Wing
    thumby.display.drawLine(bx+1, by-5, bx+6, by-5, 1)
    
    # Wheels based on steering position
    if steer_dir == "LEFT":
        thumby.display.drawRectangle(bx-2, by+2, 2, 3, 1) 
        thumby.display.drawRectangle(bx+8, by+2, 2, 3, 1) 
        thumby.display.drawRectangle(bx+1, by-4, 1, 2, 1) 
        thumby.display.drawRectangle(bx+6, by-4, 1, 2, 1)
    elif steer_dir == "RIGHT":
        thumby.display.drawRectangle(bx-2, by+2, 2, 3, 1) 
        thumby.display.drawRectangle(bx+8, by+2, 2, 3, 1) 
        thumby.display.drawRectangle(bx+2, by-4, 1, 2, 1) 
        thumby.display.drawRectangle(bx+5, by-4, 1, 2, 1) 
    else: 
        thumby.display.drawRectangle(bx-2, by+2, 2, 3, 1) 
        thumby.display.drawRectangle(bx+8, by+2, 2, 3, 1) 
        thumby.display.drawRectangle(bx+1, by-4, 2, 2, 1) 
        thumby.display.drawRectangle(bx+5, by-4, 2, 2, 1)

def draw_retro_enemy(rz, rx_offset, p_offset):
    screen_y = int(14 + rz)
    if screen_y < 14 or screen_y > 40: return 0, 0, 0, 0
    
    scale_ratio = rz / 26.0
    
    # Calculate screen position based on perspective lines
    center_road_x = 36 - int(p_offset * scale_ratio)
    road_span = int(8 + (44 * scale_ratio))
    enemy_w = int(2 + (10 * scale_ratio))
    target_screen_x = center_road_x + int((rx_offset / 25.0) * (road_span // 2)) - (enemy_w // 2)
    
    # --- RENDER DETAILED RIVAL CARS BASED ON DISTANCE ---
    if rz < 6:
        thumby.display.drawRectangle(target_screen_x, screen_y - 2, 3, 2, 1)
        enemy_h = 2
    elif rz < 15:
        thumby.display.drawRectangle(target_screen_x + 1, screen_y - 4, 3, 4, 1) 
        thumby.display.drawLine(target_screen_x, screen_y - 1, target_screen_x + 4, screen_y - 1, 1) 
        thumby.display.setPixel(target_screen_x, screen_y - 3, 1) 
        thumby.display.setPixel(target_screen_x + 4, screen_y - 3, 1) 
        enemy_h = 4
    else:
        ex = target_screen_x
        ey = screen_y
        
        thumby.display.drawRectangle(ex + 2, ey - 6, 6, 5, 1)
        thumby.display.drawRectangle(ex + 3, ey - 9, 4, 3, 1) 
        thumby.display.drawLine(ex + 4, ey - 11, ex + 5, ey - 11, 1) 
        
        thumby.display.drawLine(ex - 1, ey - 6, ex + 10, ey - 6, 1)
        thumby.display.drawRectangle(ex - 1, ey - 8, 2, 3, 1)
        thumby.display.drawRectangle(ex + 9, ey - 8, 2, 3, 1)
        
        thumby.display.drawLine(ex + 2, ey - 10, ex + 7, ey - 10, 1)
        
        thumby.display.drawRectangle(ex, ey - 3, 2, 3, 1)     
        thumby.display.drawRectangle(ex + 8, ey - 3, 2, 3, 1) 
        thumby.display.drawRectangle(ex + 1, ey - 9, 2, 2, 1) 
        thumby.display.drawRectangle(ex + 7, ey - 9, 2, 2, 1) 
        enemy_h = 11

    return target_screen_x, screen_y - enemy_h, enemy_w, enemy_h

# --- MAIN ENGINE CODE LOOP ---
while True:
    thumby.display.fill(0)
    
    if game_state == "START_PAGE":
        draw_start_page()
        if thumby.buttonA.pressed():
            game_state = "RACING"
            score = 0
            enemy_z = 0
            enemy_road_x = random.randint(-15, 15)
            enemy_speed = 0.8
            player_x = 0
            time.sleep(0.2)
            
    elif game_state == "RACING":
        speed_factor = (speed_factor + 1.2) % 12
        
        steering = "STRAIGHT"
        if thumby.buttonL.pressed():
            player_x -= 1.5
            steering = "LEFT"
        if thumby.buttonR.pressed():
            player_x += 1.5
            steering = "RIGHT"
            
        if player_x < -25: player_x = -25
        if player_x > 25: player_x = 25
        
        draw_pseudo_3d_road(player_x)
        
        enemy_z += enemy_speed
        
        if enemy_z > 26:
            enemy_z = 0
            enemy_road_x = random.randint(-18, 18)
            score += 1
            enemy_speed += 0.03 
            
        ex, ey, ew, eh = draw_retro_enemy(enemy_z, enemy_road_x, player_x)
        draw_retro_player(steering)
        
        # Hitbox Collision Logic (Easy Mode)
        if enemy_z > 20 and enemy_z < 25:
            p_left = 34  
            p_right = 38 
            e_left = ex + 2
            e_right = ex + ew - 2
            
            if (p_left < e_right and p_right > e_left):
                game_state = "GAME_OVER"
                
        thumby.display.drawText(str(score), 2, 2, 1)
        
    elif game_state == "GAME_OVER":
        thumby.display.drawText("CRASH!", 18, 5, 1)
        thumby.display.drawText("Score: " + str(score), 12, 18, 1)
        thumby.display.drawText("A to Retry", 8, 30, 1)
        
        if thumby.buttonA.pressed():
            game_state = "START_PAGE"
            time.sleep(0.2)
            
    thumby.display.update()
