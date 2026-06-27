import thumby, random, math, time

def current_time():
    """Return the current time in seconds using time.ticks_ms()."""
    return time.ticks_ms() / 1000.0

# Level and sprite dimensions
LEVEL_WIDTH  = 12
LEVEL_HEIGHT = 12
OBSTACLE_PROB = 0.2
NUM_SPAWNERS = 3

PLAYER_WIDTH    = 9
PLAYER_HEIGHT   = 9
ENEMY_WIDTH     = 9
ENEMY_HEIGHT    = 9
OBSTACLE_WIDTH  = 5
OBSTACLE_HEIGHT = 5
RETICLE_WIDTH   = 3
RETICLE_HEIGHT  = 3
BULLET_WIDTH    = 1
BULLET_HEIGHT   = 1

SPAWNER_WIDTH   = 8  
SPAWNER_HEIGHT  = 8
AMMOBOX_WIDTH   = 5
AMMOBOX_HEIGHT  = 5

SCALE = 2
HALF_TILE_WIDTH  = 6
HALF_TILE_HEIGHT = 3
CENTER_X = 36
CENTER_Y = 20

# Stratagem codes and cooldowns
ammo_code      = ["D", "D", "U", "R"]    # Ammo drop – 5 sec
turret_code    = ["D", "L", "D", "U"]    # Turret – 15 sec
airstrike_code = ["U", "R", "D", "R"]    # Airstrike – 10 sec
weapon_code    = ["D", "L", "U", "D"]    # Weapon pickup – 60 sec

last_ammo_time     = 0
last_turret_time   = 0
last_airstrike_time = 0

last_weapon_time    = -60


code_menu_open = False
code_input = []
b_prev = False
d_prev = False
u_prev = False
r_prev = False
l_prev = False
wrong_stratagem_flag = False
wrong_stratagem_start = 0
wrong_stratagem_duration = 1.5

turrets = []
weapon_pickups = []

final_stage = False         
final_stage_start = 0       
last_final_spawn_time = 0   
ship = None                 
player_spawn = (0, 0)       

def show_stratagem_codes():
    """Display a screen listing each stratagem code until the player presses a button."""
    thumby.display.fill(0)
    thumby.display.drawText("CODES", 2, 0, 1)
    thumby.display.drawText("S: D D U R", 2, 8, 1)
    thumby.display.drawText("T: D L D U", 2, 16, 1)
    thumby.display.drawText("O: U R D R", 2, 24, 1)
    thumby.display.drawText("W: D L U D", 2, 32, 1)
    thumby.display.update()
    while not (thumby.buttonA.pressed() or thumby.buttonB.pressed() or 
               thumby.buttonU.pressed() or thumby.buttonD.pressed() or 
               thumby.buttonL.pressed() or thumby.buttonR.pressed()):
        time.sleep(0.1)
    while (thumby.buttonA.pressed() or thumby.buttonB.pressed() or 
           thumby.buttonU.pressed() or thumby.buttonD.pressed() or 
           thumby.buttonL.pressed() or thumby.buttonR.pressed()):
        time.sleep(0.1)

def iso_transform(grid_x, grid_y, cam_x, cam_y):
    """Convert grid coordinates to screen coordinates using isometric projection."""
    rel_x = grid_x - cam_x
    rel_y = grid_y - cam_y
    screen_x = int((rel_x - rel_y) * HALF_TILE_WIDTH * SCALE + CENTER_X)
    screen_y = int((rel_x + rel_y) * HALF_TILE_HEIGHT * SCALE + CENTER_Y)
    return screen_x, screen_y

def drawRect(x, y, w, h, color):
    thumby.display.drawLine(x, y, x+w-1, y, color)
    thumby.display.drawLine(x, y+h-1, x+w-1, y+h-1, color)
    thumby.display.drawLine(x, y, x, y+h-1, color)
    thumby.display.drawLine(x+w-1, y, x+w-1, y+h-1, color)

def fillRect(x, y, w, h, color):
    for j in range(h):
        thumby.display.drawLine(x, y+j, x+w-1, y+j, color)

def draw_stratagem_menu_overlay():
    menu_x = 50
    menu_y = 2
    square_size = 4
    spacing = 2
    thumby.display.drawText("", menu_x - 30, menu_y, 1)
    for i in range(4):
        x = menu_x + i*(square_size+spacing)
        drawRect(x, menu_y, square_size, square_size, 1)
    now = current_time()
    remaining_ammo = int((last_ammo_time + 5) - now)
    if now < last_ammo_time + 5:
        thumby.display.drawText("S:" + str(max(0, remaining_ammo)), menu_x - 30, menu_y+10, 1)
    remaining_turret = int((last_turret_time + 15) - now)
    if now < last_turret_time + 15:
        thumby.display.drawText("T:" + str(max(0, remaining_turret)), menu_x - 30, menu_y+20, 1)
    remaining_airstrike = int((last_airstrike_time + 10) - now)
    if now < last_airstrike_time + 10:
        thumby.display.drawText("O:" + str(max(0, remaining_airstrike)), menu_x - 30, menu_y+30, 1)
    remaining_weapon = int((last_weapon_time + 60) - now)
    if now < last_weapon_time + 60:
        thumby.display.drawText("W:" + str(max(0, remaining_weapon)), menu_x - 30, menu_y+40, 1)

def draw_stratagem_menu_input(code_in):
    menu_x = 50
    menu_y = 2
    square_size = 4
    spacing = 2
    for i in range(len(code_in)):
        x = menu_x + i*(square_size+spacing)
        fillRect(x, menu_y, square_size, square_size, 1)

def draw_ship(ship, player):

    ship_sprite = bytearray([
        0b000110000,
        0b001111000,
        0b011111100,
        0b111111100,
        0b111111100,
        0b111111100,
        0b111111100,
        0b101111110,
        0b100111111
    ])
    SHIP_WIDTH = 9
    SHIP_HEIGHT = 9
    sx, sy = iso_transform(ship["x"], ship["y"], player.x, player.y)
    thumby.display.blit(ship_sprite, sx - (SHIP_WIDTH * SCALE // 2),
                        sy - (SHIP_HEIGHT * SCALE // 2), SHIP_WIDTH, SHIP_HEIGHT, 0, SCALE, 0)

obstacle_sprite = bytearray([
    0b01010,
    0b01111,
    0b11110,
    0b01111,
    0b01010
])
bullet_sprite  = bytearray([0b1])
reticle_sprite = bytearray([
    0b010,
    0b111,
    0b010
])
spawner_sprite = bytearray([
    0b00100,
    0b01010,
    0b10101,
    0b01010,
    0b00100
])
ammo_box_sprite = bytearray([
    0b00100,
    0b11100,
    0b11111,
    0b11100,
    0b00100
])
health_box_sprite = bytearray([
    0b01010,
    0b11111,
    0b11111,
    0b01110,
    0b00100
])
player_sprite = bytearray([
    0b0000000000000,
    0b0000000000000,
    0b0000000000000,
    0b1111111111110,
    0b0000000111111,
    0b0000000111101,
    0b1111111111001,
    0b0000000100000,
    0b0000000100000
])
enemy_sprite = bytearray([
    0b000001000,
    0b000011000,
    0b111111100,
    0b000011110,
    0b000011111,
    0b000011111,
    0b111111110,
    0b000011100,
    0b000001000
])
weapon_pickup_sprite = bytearray([
    0b0110,
    0b1001,
    0b1001,
    0b0110
])


class Player:
    def __init__(self, x, y):
        self.x = x  
        self.y = y
        self.speed = 0.1  
        self.health = 100
        self.ammo = 50
        self.facing = (1, 0)
        self.weapon_type = "default"
    def move(self, dx, dy, level):
        if code_menu_open:
            return
        new_x = self.x + dx
        new_y = self.y + dy
        if new_x < 0 or new_x >= LEVEL_WIDTH or new_y < 0 or new_y >= LEVEL_HEIGHT:
            return
        if level[int(new_y)][int(new_x)] == 1:
            return
        self.x = new_x
        self.y = new_y
        if dx or dy:
            length = math.sqrt(dx*dx + dy*dy)
            self.facing = (dx/length, dy/length)

class Enemy:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.speed = 0.05
        self.direction = random.choice([(1,0), (-1,0), (0,1), (0,-1)])
        self.health = 3  
    def update(self, level, player):
        distance = math.sqrt((self.x - player.x)**2 + (self.y - player.y)**2)
        if distance < 3:
            dx = player.x - self.x
            dy = player.y - self.y
            mag = math.sqrt(dx*dx + dy*dy)
            if mag > 0:
                self.direction = (dx/mag, dy/mag)
        else:
            if random.random() < 0.02:
                self.direction = random.choice([(1,0), (-1,0), (0,1), (0,-1)])
        new_x = self.x + self.direction[0] * self.speed
        new_y = self.y + self.direction[1] * self.speed
        if new_x < 0 or new_x >= LEVEL_WIDTH or new_y < 0 or new_y >= LEVEL_HEIGHT:
            self.direction = (-self.direction[0], -self.direction[1])
            return
        if level[int(new_y)][int(new_x)] == 1:
            self.direction = (-self.direction[0], -self.direction[1])
            return
        self.x = new_x
        self.y = new_y

class Bullet:
    def __init__(self, x, y, vx, vy, turret_bullet=False, damage=1):
        self.x = x
        self.y = y
        self.vx = vx
        self.vy = vy
        self.speed = 0.2
        self.turret_bullet = turret_bullet
        self.damage = damage
    def update(self):
        self.x += self.vx * self.speed
        self.y += self.vy * self.speed

class Spawner:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.health = 10
        self.spawn_interval = 2.5
        self.last_spawn_time = current_time()
    def update(self, level, player):
        new_enemies = []
        now = current_time()
        if now - self.last_spawn_time >= self.spawn_interval:
            self.last_spawn_time = now
            new_enemies.append(Enemy(self.x, self.y))
            new_enemies.append(Enemy(self.x, self.y))
        return new_enemies

class AmmoBox:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.sprite = ammo_box_sprite

class HealthBox:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.sprite = health_box_sprite

class Turret:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.spawn_time = current_time()
        self.lifetime = 30       #
        self.fire_interval = 0.5 
        self.last_fire_time = current_time()
        self.range = 4.0         
    def update(self, enemies, bullets):
        now = current_time()
        if now - self.spawn_time >= self.lifetime:
            return False
        if now - self.last_fire_time >= self.fire_interval:
            target = None
            min_dist = float('inf')
            for enemy in enemies:
                d = math.sqrt((enemy.x - self.x)**2 + (enemy.y - self.y)**2)
                if d <= self.range and d < min_dist:
                    target = enemy
                    min_dist = d
            if target:
                dx = target.x - self.x
                dy = target.y - self.y
                mag = math.sqrt(dx*dx + dy*dy)
                if mag > 0:
                    vx = dx/mag
                    vy = dy/mag
                else:
                    vx, vy = 0, 0
                bullets.append(Bullet(self.x, self.y, vx, vy, turret_bullet=True, damage=1))
                self.last_fire_time = now
        return True

def draw_turret(turret, player):
    sx, sy = iso_transform(turret.x, turret.y, player.x, player.y)
    fillRect(sx-2, sy-2, 4, 4, 1)

class WeaponPickup:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.ammo = 300
        self.damage = 3
        self.sprite = weapon_pickup_sprite
    def draw(self, player):
        sx, sy = iso_transform(self.x, self.y, player.x, player.y)
        thumby.display.blit(self.sprite, sx - (4 * SCALE // 2), sy - (4 * SCALE // 2), 4, 4, 0, SCALE, 0)


def runGame():
    global last_ammo_time, last_turret_time, last_airstrike_time, last_weapon_time
    global code_menu_open, code_input, b_prev, d_prev, u_prev, r_prev, l_prev
    global wrong_stratagem_flag, wrong_stratagem_start, turrets, weapon_pickups
    global final_stage, final_stage_start, last_final_spawn_time, ship, player_spawn

    code_menu_open = False
    code_input = []
    b_prev = False
    last_ammo_time = 0
    last_turret_time = 0
    last_airstrike_time = 0
    last_weapon_time = -60
    d_prev = u_prev = r_prev = l_prev = False
    wrong_stratagem_flag = False
    wrong_stratagem_start = 0
    turrets = []
    weapon_pickups = []
    final_stage = False
    final_stage_start = 0
    last_final_spawn_time = 0
    ship = None

    try:
        thumby.display.setFont(thumby.font3x5)
    except:
        pass

    level = [[0 for _ in range(LEVEL_WIDTH)] for _ in range(LEVEL_HEIGHT)]
    for y in range(LEVEL_HEIGHT):
        for x in range(LEVEL_WIDTH):
            if random.random() < OBSTACLE_PROB:
                level[y][x] = 1
    player_start = (0, 0)
    player_spawn = player_start
    level[player_start[1]][player_start[0]] = 0

    player = Player(player_start[0], player_start[1])
    player.weapon_type = "default"

    enemies = []
    for i in range(3):
        while True:
            ex = random.randint(0, LEVEL_WIDTH-1)
            ey = random.randint(0, LEVEL_HEIGHT-1)
            if level[ey][ex] == 0 and (ex, ey) != (int(player.x), int(player.y)):
                break
        enemies.append(Enemy(ex, ey))
    bullets = []
    ammo_boxes = []
    health_boxes = []

    spawners = []
    for i in range(NUM_SPAWNERS):
        while True:
            sx = random.randint(0, LEVEL_WIDTH-1)
            sy = random.randint(0, LEVEL_HEIGHT-1)
            if level[sy][sx] == 0 and (sx, sy) != (player_start[0], player_start[1]):
                break
        spawners.append(Spawner(sx, sy))

    spawn_events = []
    fire_ready = True
    b_prev = False


    while True:

        if thumby.buttonA.pressed() and thumby.buttonB.pressed():
            show_stratagem_codes()
            while thumby.buttonA.pressed() or thumby.buttonB.pressed():
                time.sleep(0.1)

        if not final_stage and len(spawners) == 0:
            final_stage = True
            final_stage_start = current_time()
            last_final_spawn_time = current_time()

        for pickup in weapon_pickups[:]:
            if math.sqrt((player.x - pickup.x)**2 + (player.y - pickup.y)**2) < 0.5:
                player.weapon_type = "special"
                player.ammo = pickup.ammo
                weapon_pickups.remove(pickup)

        if player.weapon_type == "special" and player.ammo <= 0:
            player.weapon_type = "default"

        b_current = thumby.buttonB.pressed()
        if b_current and not b_prev:
            code_menu_open = not code_menu_open
            if code_menu_open:
                code_input = []
                d_prev = u_prev = r_prev = l_prev = False
            time.sleep(0.2)
        b_prev = b_current

        if code_menu_open:
            now = current_time()
            can_use_ammo = now >= last_ammo_time + 5
            can_use_turret = now >= last_turret_time + 15
            can_use_airstrike = now >= last_airstrike_time + 10
            can_use_weapon = now >= last_weapon_time + 60
            if can_use_ammo or can_use_turret or can_use_airstrike or can_use_weapon:
                if thumby.buttonD.pressed() and not d_prev:
                    code_input.append("D")
                d_prev = thumby.buttonD.pressed()
                if thumby.buttonU.pressed() and not u_prev:
                    code_input.append("U")
                u_prev = thumby.buttonU.pressed()
                if thumby.buttonR.pressed() and not r_prev:
                    code_input.append("R")
                r_prev = thumby.buttonR.pressed()
                if thumby.buttonL.pressed() and not l_prev:
                    code_input.append("L")
                l_prev = thumby.buttonL.pressed()

                if len(code_input) >= 4:
                    if code_input[:4] == ammo_code:
                        if can_use_ammo:
                            spawn_x = player.x + 1 if player.x+1 < LEVEL_WIDTH else player.x
                            spawn_y = player.y
                            ammo_boxes.append(AmmoBox(spawn_x, spawn_y))
                            last_ammo_time = now
                            code_menu_open = False
                            code_input = []
                        else:
                            code_input = []
                    elif code_input[:4] == turret_code:
                        if can_use_turret:
                            turrets.append(Turret(player.x, player.y))
                            last_turret_time = now
                            code_menu_open = False
                            code_input = []
                        else:
                            code_input = []
                    elif code_input[:4] == airstrike_code:
                        if can_use_airstrike:
                            new_enemy_list = []
                            for enemy in enemies:
                                d = math.sqrt((enemy.x - player.x)**2 + (enemy.y - player.y)**2)
                                if d >= 3:
                                    new_enemy_list.append(enemy)
                            enemies = new_enemy_list
                            last_airstrike_time = now
                            code_menu_open = False
                            code_input = []
                        else:
                            code_input = []
                    elif code_input[:4] == weapon_code:
                        if can_use_weapon:
                            pickup_x = player.x + 1 if player.x+1 < LEVEL_WIDTH else player.x
                            pickup_y = player.y
                            weapon_pickups.append(WeaponPickup(pickup_x, pickup_y))
                            last_weapon_time = now
                            code_menu_open = False
                            code_input = []
                        else:
                            code_input = []
                    else:
                        wrong_stratagem_flag = True
                        wrong_stratagem_start = now
                        code_input = []
        else:
            dx = 0
            dy = 0
            if thumby.buttonU.pressed():
                dy = -player.speed
            if thumby.buttonD.pressed():
                dy = player.speed
            if thumby.buttonL.pressed():
                dx = -player.speed
            if thumby.buttonR.pressed():
                dx = player.speed
            player.move(dx, dy, level)
            if thumby.buttonA.pressed() and fire_ready and player.ammo > 0:
                bx = player.x
                by = player.y
                vx, vy = player.facing
                dmg = 1 if player.weapon_type == "default" else 3
                bullets.append(Bullet(bx, by, vx, vy, turret_bullet=False, damage=dmg))
                player.ammo -= 1
                fire_ready = False
            if not thumby.buttonA.pressed():
                fire_ready = True

        if wrong_stratagem_flag and current_time() - wrong_stratagem_start >= wrong_stratagem_duration:
            wrong_stratagem_flag = False

        if final_stage:
            if current_time() - last_final_spawn_time >= 1.0 and len(enemies) < 12:
                offset_x = random.randint(-2, 2)
                offset_y = random.randint(-2, 2)
                new_ex = player.x + offset_x
                new_ey = player.y + offset_y
                if 0 <= new_ex < LEVEL_WIDTH and 0 <= new_ey < LEVEL_HEIGHT:
                    if level[int(new_ey)][int(new_ex)] == 0:
                        enemies.append(Enemy(new_ex, new_ey))
                last_final_spawn_time = current_time()
            if current_time() - final_stage_start >= 30 and ship is None:
                ship = {"x": player_spawn[0], "y": player_spawn[1]}
            if ship is not None:
                dship = math.sqrt((player.x - ship["x"])**2 + (player.y - ship["y"])**2)
                if dship < 2:
                    thumby.display.fill(0)
                    thumby.display.drawText("YOU WIN!", 10, 20, 1)
                    thumby.display.update()
                    time.sleep(2)
                    break
            if ship is None:
                time_elapsed = current_time() - final_stage_start
                time_left = max(0, 30 - int(time_elapsed))
                thumby.display.drawText("SURVIVE:" + str(time_left), 10, 30, 1)

        # Game Updates: Bullets, Enemies, Spawners, Turrets
        for bullet in bullets[:]:
            bullet.update()
            if bullet.x < 0 or bullet.x >= LEVEL_WIDTH or bullet.y < 0 or bullet.y >= LEVEL_HEIGHT:
                bullets.remove(bullet)
                continue
            if level[int(bullet.y)][int(bullet.x)] == 1:
                bullets.remove(bullet)
                continue
            for enemy in enemies[:]:
                if math.sqrt((bullet.x - enemy.x)**2 + (bullet.y - enemy.y)**2) < 0.5:
                    if bullet.turret_bullet:
                        enemy.health = 0
                    else:
                        enemy.health -= bullet.damage
                    if enemy.health <= 0:
                        enemies.remove(enemy)
                    if bullet in bullets:
                        bullets.remove(bullet)
                    if random.random() < 0.5 and player.weapon_type == "default":
                        player.ammo += 5
                    if spawners:
                        delay = 1.0 + 0.5 * (NUM_SPAWNERS - len(spawners))
                        spawn_time = current_time() + delay
                        chosen_spawner = random.choice(spawners)
                        spawn_events.append((spawn_time, chosen_spawner))
                    break
            for spawner in spawners[:]:
                if math.sqrt((bullet.x - spawner.x)**2 + (bullet.y - spawner.y)**2) < 0.3:
                    spawner.health -= 1
                    if bullet in bullets:
                        bullets.remove(bullet)
                    if spawner.health <= 0:
                        spawners.remove(spawner)
                    break

        for enemy in enemies:
            enemy.update(level, player)
            if math.sqrt((player.x - enemy.x)**2 + (player.y - enemy.y)**2) < 0.5:
                player.health -= 1
                if player.health < 0:
                    player.health = 0

        for spawner in spawners:
            new_enemies = spawner.update(level, player)
            for new_enemy in new_enemies:
                if len(enemies) < 12:
                    enemies.append(new_enemy)

        for event in spawn_events[:]:
            spawn_time, spawner_obj = event
            if current_time() >= spawn_time:
                if spawner_obj in spawners and len(enemies) < 12:
                    enemies.append(Enemy(spawner_obj.x, spawner_obj.y))
                spawn_events.remove(event)

        for turret in turrets[:]:
            if not turret.update(enemies, bullets):
                turrets.remove(turret)

        for ammo_box in ammo_boxes[:]:
            if math.sqrt((player.x - ammo_box.x)**2 + (player.y - ammo_box.y)**2) < 0.5:
                if player.weapon_type == "default":
                    player.ammo += 10
                player.health = min(player.health + 50, 100)
                ammo_boxes.remove(ammo_box)

        for health_box in health_boxes[:]:
            if math.sqrt((player.x - health_box.x)**2 + (player.y - health_box.y)**2) < 0.5:
                player.health = min(player.health + 20, 100)
                health_boxes.remove(health_box)

        thumby.display.fill(0)
        for gy in range(LEVEL_HEIGHT):
            for gx in range(LEVEL_WIDTH):
                if level[gy][gx] == 1:
                    sx, sy = iso_transform(gx, gy, player.x, player.y)
                    thumby.display.blit(obstacle_sprite,
                        sx - (OBSTACLE_WIDTH * SCALE // 2),
                        sy - (OBSTACLE_HEIGHT * SCALE // 2),
                        OBSTACLE_WIDTH, OBSTACLE_HEIGHT, 0, SCALE, 0)
        for spawner in spawners:
            sx, sy = iso_transform(spawner.x, spawner.y, player.x, player.y)
            thumby.display.blit(spawner_sprite,
                        sx - (SPAWNER_WIDTH * SCALE // 2),
                        sy - (SPAWNER_HEIGHT * SCALE // 2),
                        SPAWNER_WIDTH, SPAWNER_HEIGHT, 0, SCALE, 0)
        for ammo_box in ammo_boxes:
            sx, sy = iso_transform(ammo_box.x, ammo_box.y, player.x, player.y)
            thumby.display.blit(ammo_box.sprite,
                        sx - (AMMOBOX_WIDTH * SCALE // 2),
                        sy - (AMMOBOX_HEIGHT * SCALE // 2),
                        AMMOBOX_WIDTH, AMMOBOX_HEIGHT, 0, SCALE, 0)
        for health_box in health_boxes:
            sx, sy = iso_transform(health_box.x, health_box.y, player.x, player.y)
            thumby.display.blit(health_box.sprite,
                        sx - (AMMOBOX_WIDTH * SCALE // 2),
                        sy - (AMMOBOX_HEIGHT * SCALE // 2),
                        AMMOBOX_WIDTH, AMMOBOX_HEIGHT, 0, SCALE, 0)
        for pickup in weapon_pickups:
            pickup.draw(player)
        for turret in turrets:
            draw_turret(turret, player)
        for enemy in enemies:
            sx, sy = iso_transform(enemy.x, enemy.y, player.x, player.y)
            thumby.display.blit(enemy_sprite,
                        sx - (ENEMY_WIDTH * SCALE // 2),
                        sy - (ENEMY_HEIGHT * SCALE // 2),
                        ENEMY_WIDTH, ENEMY_HEIGHT, 0, SCALE, 0)
        for bullet in bullets:
            sx, sy = iso_transform(bullet.x, bullet.y, player.x, player.y)
            thumby.display.blit(bullet_sprite,
                        sx - (BULLET_WIDTH * SCALE // 2),
                        sy - (BULLET_HEIGHT * SCALE // 2),
                        BULLET_WIDTH, BULLET_HEIGHT, 0, SCALE, 0)
        sx, sy = iso_transform(player.x, player.y, player.x, player.y)
        thumby.display.blit(player_sprite,
                        sx - (PLAYER_WIDTH * SCALE // 2),
                        sy - (PLAYER_HEIGHT * SCALE // 2),
                        PLAYER_WIDTH, PLAYER_HEIGHT, 0, SCALE, 0)
        reticle_distance = 0.8
        rx = player.x + player.facing[0] * reticle_distance
        ry = player.y + player.facing[1] * reticle_distance
        r_sx, r_sy = iso_transform(rx, ry, player.x, player.y)
        thumby.display.blit(reticle_sprite,
                        r_sx - (RETICLE_WIDTH * SCALE // 2),
                        r_sy - (RETICLE_HEIGHT * SCALE // 2),
                        RETICLE_WIDTH, RETICLE_HEIGHT, 0, SCALE, 0)
        tl = iso_transform(-0.5, -0.5, player.x, player.y)
        tr = iso_transform(LEVEL_WIDTH - 0.5, -0.5, player.x, player.y)
        br = iso_transform(LEVEL_WIDTH - 0.5, LEVEL_HEIGHT - 0.5, player.x, player.y)
        bl = iso_transform(-0.5, LEVEL_HEIGHT - 0.5, player.x, player.y)
        thumby.display.drawLine(tl[0], tl[1], tr[0], tr[1], 1)
        thumby.display.drawLine(tr[0], tr[1], br[0], br[1], 1)
        thumby.display.drawLine(br[0], br[1], bl[0], bl[1], 1)
        thumby.display.drawLine(bl[0], bl[1], tl[0], tl[1], 1)
        thumby.display.drawText("H:" + str(player.health), 0, 0, 1)
        thumby.display.drawText("A:" + str(player.ammo), 0, 8, 1)
        if code_menu_open:
            draw_stratagem_menu_overlay()
            draw_stratagem_menu_input(code_input)
            if wrong_stratagem_flag:
                thumby.display.drawText("INVALID", 30, 8, 1)
        if final_stage and ship is not None:
            draw_ship(ship, player)
            thumby.display.drawText("EXTRACT", 10, 30, 1)
        if final_stage and ship is None:
            time_elapsed = current_time() - final_stage_start
            time_left = max(0, 30 - int(time_elapsed))
            thumby.display.drawText("SURVIVE:" + str(time_left), 10, 30, 1)
        thumby.display.update()

        if player.health <= 0:
            thumby.display.drawText("GAME OVER", 10, 20, 1)
            thumby.display.update()
            time.sleep(2)
            break
        if ship is not None:
            dship = math.sqrt((player.x - ship["x"])**2 + (player.y - ship["y"])**2)
            if dship < 2:
                thumby.display.fill(0)
                thumby.display.drawText("YOU WIN!", 10, 20, 1)
                thumby.display.update()
                time.sleep(2)
                break

        time.sleep(0.02)

while True:
    runGame()
    # Reset globals on game restart.
    code_menu_open = False
    code_input = []
    b_prev = False
    last_ammo_time = 0
    last_turret_time = 0
    last_airstrike_time = 0
    last_weapon_time = -60
    d_prev = u_prev = r_prev = l_prev = False
    wrong_stratagem_flag = False
    wrong_stratagem_start = 0
    turrets = []
    weapon_pickups = []
    final_stage = False
    ship = None
    while not thumby.buttonA.pressed():
        thumby.display.fill(0)
        thumby.display.drawText("PRESS A", 5, 20, 1)
        thumby.display.update()
        time.sleep(0.1)
