import thumby
import time
import math 
import random
# Screen size
SCREEN_W = 72
SCREEN_H = 40

# -----------------
# PARTICLES
# -----------------
particles = []
MAX_PARTICLES = 12

def spawn_particles(x, y):
    for i in range(MAX_PARTICLES):
        vx = random.uniform(-1.5, 1.5)
        vy = random.uniform(-1.5, 1.5)
        life = random.randint(10, 20)
        particles.append([x, y, vx, vy, life])

game_over = False

# -----------------
# SPRITES
# -----------------

strip_bitmap = bytearray([5,4,5,4,5,4,5,4,5,4,5,4,5,4,5,4,5,4,5,4,5,4,5,4,5,4,5,4,5,4,5,4,5,4,5,4,5,4,5,4,5,4,5,4,5,4,5,4,5,4,5,4,5,4,5,4,5,4,5,4,5,4,5,4,5,4,5,4,5,4,5,4])

strip = thumby.Sprite(72, 3, strip_bitmap)
enemy_frame = 0
enemy_anim_timer = 0
enemy_anim_speed = 3  # lower = faster animation


ship_bitmap = bytearray([64,112,224,176,156,176,224,112,64,
           0,1,0,1,0,1,0,1,0]) # 9x9 = 81 bits -> 11 bytes

ship = thumby.Sprite(9, 9, ship_bitmap)


enemy_bitmap_1 = bytearray([8,12,106,42,15,43,43,15,42,106,12,8])

enemy_bitmap_2 = bytearray([8,12,106,42,15,43,43,15,42,106,12,8])

enemy_bitmap_3 = bytearray([8,12,10,42,111,43,43,111,42,10,12,8])


enemy_bitmap_4 = bytearray([8,12,10,10,47,107,107,47,10,10,12,8])
enemy = thumby.Sprite(12, 7, enemy_bitmap_1+enemy_bitmap_2+enemy_bitmap_3+enemy_bitmap_4+enemy_bitmap_3+enemy_bitmap_2)
# 5x5 bullet sprite
# BITMAP: width: 5, height: 5
bullet_bitmap = bytearray([0,2,21,8,0]) # 25 bits -> 4 bytes

# BITMAP: width: 72, height: 40
menu_bitmap = bytearray([0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,128,128,128,240,112,112,112,112,112,254,254,254,254,126,126,126,126,126,254,254,254,240,112,112,112,112,112,128,128,128,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,
           0,0,0,0,0,0,0,0,0,0,0,0,0,60,92,92,95,95,95,92,93,93,93,93,93,95,95,95,92,93,93,93,93,93,95,95,95,92,93,93,93,93,93,95,95,95,92,92,92,96,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,
           0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,15,23,23,127,191,191,207,23,23,24,0,0,15,23,23,23,23,23,24,0,0,15,23,23,127,191,191,207,23,23,24,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,
           0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,
           0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0])

menu = thumby.Sprite(72, 40, menu_bitmap, 0, 0)

bullet = thumby.Sprite(5, 5, bullet_bitmap)

# -----------------
# PLAYER
# -----------------
ship.x = 32
ship.y = 30
ship_dir = 1
ship_speed = 0.5
enemy.x = 0
enemy.y = 0

enemy_dir = 1        # 1 = right, -1 = left
enemy_speed = 1.5
enemy_drop = 3       # how much lower it gets each pass

score = 0

enemy_alive = True
enemy_respawn_delay = 60   # ~1 second at 60 FPS
enemy_respawn_timer = 0

strip.x = 0
strip.y = 37

# -----------------
# BULLET
# -----------------
bullet_active = False
bullet_speed = 2
started = False
def reset_game():
    global score, enemy_alive, enemy_respawn_timer
    global ship, enemy, bullet_active, particles, game_over

    score = 0
    enemy_alive = True
    enemy_respawn_timer = 0
    enemy.x = 0
    enemy.y = 0

    ship.x = 32
    ship.y = 30

    bullet_active = False
    particles = []
    game_over = False

thumby.display.setFPS(60)
while True:
    thumby.display.fill(0)
    
    if not started:
        thumby.display.fill(0)
        thumby.display.drawSprite(menu)
        thumby.display.drawText("Press Start", 5, 25, 1)
        thumby.display.update()
        
        if thumby.inputJustPressed():
            started = True
        
        continue
        
    if game_over:
        thumby.display.fill(0)
        thumby.display.drawText("GAME OVER", 10, 12, 1)
        thumby.display.drawText("S:" + str(score), 0, 0, 1)
        thumby.display.drawText("A - AGAIN", 10, 22, 1)
        thumby.display.drawText("B - QUIT", 10, 32, 1)
        thumby.display.update()
    
        if thumby.buttonA.justPressed():
            reset_game()
        if thumby.buttonB.justPressed():
            thumby.reset()
    
        time.sleep(0.05)
        continue

    thumby.display.drawText(str(score), 0, 0, 1)

    # --- AUTO MOVE SHIP ---
    ship.x += ship_dir * ship_speed

    # Bounce off walls
    if ship.x <= 0:
        ship.x = 0
        ship_dir = 1
    elif ship.x >= SCREEN_W - ship.width:
        ship.x = SCREEN_W - ship.width
        ship_dir = -1

    # --- BUTTON PRESS ---
    if (thumby.buttonA.justPressed() or
        thumby.buttonB.justPressed() or
        thumby.buttonL.justPressed() or
        thumby.buttonR.justPressed() or
        thumby.buttonU.justPressed() or
        thumby.buttonD.justPressed()):

        if not bullet_active:
            bullet.x = ship.x + 2
            bullet.y = ship.y - 5
            bullet_active = True

            # Change direction ONLY when firing
            ship_dir *= -1
            
# --- ENEMY MOVE ---

# --- ENEMY ANIMATION ---
    if enemy_alive:
        enemy_anim_timer += 1
        if enemy_anim_timer >= enemy_anim_speed:
            enemy_anim_timer = 0
            enemy_frame += 1
            enemy.setFrame(enemy_frame)

    if enemy_alive:
        enemy.x += enemy_dir * enemy_speed
    
        if enemy.x <= -12:
            enemy.x = 0
            enemy_dir = 1
            enemy.y += enemy_drop
        elif enemy.x >= SCREEN_W:
            enemy.x = SCREEN_W
            enemy_dir = -1
            enemy.y += enemy_drop


    # --- BULLET MOVE ---
    if bullet_active:
        bullet.y -= bullet_speed
        if bullet.y < -bullet.height:
            bullet_active = False
        else:
            thumby.display.drawSprite(bullet)
            
    # --- ENEMY RESPAWN ---
    if not enemy_alive:
        enemy_respawn_timer -= 1
        if enemy_respawn_timer <= 0:
            enemy_alive = True
            enemy.x = 0
            enemy.y = 0

            
    # --- BULLET HIT ENEMY ---
# --- BULLET HIT ENEMY ---
    if bullet_active and enemy_alive:
        if (bullet.x < enemy.x + enemy.width and
            bullet.x + bullet.width > enemy.x and
            bullet.y < enemy.y + enemy.height and
            bullet.y + bullet.height > enemy.y):
    
            spawn_particles(enemy.x + enemy.width // 2,
                            enemy.y + enemy.height // 2)
    
            score += 1
            bullet_active = False
            enemy_alive = False
            enemy_respawn_delay = random.randint(30, 90)
            enemy_respawn_timer = enemy_respawn_delay


    if enemy_alive:
        thumby.display.drawSprite(enemy)
        
        

    thumby.display.drawSprite(strip)
    
    thumby.display.drawSprite(ship)
    
        # --- PARTICLE UPDATE ---
    for p in particles[:]:
        p[0] += p[2]
        p[1] += p[3]
        p[4] -= 1
    
        # gravity (optional, looks nice)
        p[3] += 0.1
    
        if p[4] <= 0:
            particles.remove(p)
        else:
            thumby.display.setPixel(int(p[0]), int(p[1]), 1)
            
    if enemy_alive and not game_over:
        if (ship.x < enemy.x + enemy.width and
            ship.x + ship.width > enemy.x and
            ship.y < enemy.y + enemy.height and
            ship.y + ship.height > enemy.y):
    
            spawn_particles(ship.x + ship.width // 2,
                            ship.y + ship.height // 2)
            game_over = True

        

    thumby.display.update()


