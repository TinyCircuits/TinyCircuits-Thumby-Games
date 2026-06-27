import thumby
import time
import random
import math
import sys

menu_options = ["Start", "Quit"]
selected_index = 0
blink_timer = 0

bitmap0 = bytearray([2,7,7,255,255,7,7,2,254,255,254,24,254,255,254,0,254,255,254,224,254,255,254,0,254,255,254,56,120,56,254,255,254,0,254,255,255,153,153,255,246,0,254,255,254,0,254,255,254,224,254,255,254,0,206,223,223,219,251,251,250,0,0,0,
           0,0,0,1,1,0,0,0,0,1,0,0,0,1,0,0,0,1,1,1,1,1,0,0,0,1,0,0,0,0,0,1,0,0,0,1,1,1,1,1,0,0,0,1,0,0,0,1,1,1,1,1,0,0,0,1,1,1,1,1,0,0,0,0])
bitmap_height = 9

def draw_menu():
    global blink_timer
    thumby.display.fill(0)
    title_x = 4
    title_y = 0
    thumby.display.blit(bitmap0, title_x, title_y, 64, 9, 12, 0, 12)
    for _ in range(2):
        y = random.randint(0, 39)
        for x in range(72):
            if random.random() > 0.95:
                thumby.display.setPixel(x, y, 1)
    for i, option in enumerate(menu_options):
        y = 20 + i * 10
        if i == selected_index:
            if blink_timer % 10 < 5:
                thumby.display.drawText(">" + option, 5, y, 1)
        else:
            thumby.display.drawText(option, 5, y, 1)
    thumby.display.update()
    blink_timer += 1

def run_menu():
    global selected_index
    while True:
        draw_menu()
        if thumby.buttonU.pressed():
            selected_index = (selected_index - 1) % len(menu_options)
            time.sleep(0.15)
        if thumby.buttonD.pressed():
            selected_index = (selected_index + 1) % len(menu_options)
            time.sleep(0.15)
        if thumby.buttonA.pressed():
            if menu_options[selected_index] == "Start":
                thumby.display.fill(0)
                thumby.display.drawText("Loading...", 5, 20, 1)
                thumby.display.update()
                time.sleep(0.7)
                break
            elif menu_options[selected_index] == "Quit":
                thumby.display.fill(0)
                thumby.display.drawText("Loading...", 6, 20, 1)
                thumby.display.update()
                time.sleep(0.7)
                sys.exit()
        time.sleep(0.05)

SCREEN_WIDTH = 72
SCREEN_HEIGHT = 40

player_x = SCREEN_HEIGHT // 2
player_y = SCREEN_HEIGHT // 2
player_speed = 2
player_size = 3

hex_center_x = SCREEN_WIDTH // 2
hex_center_y = SCREEN_HEIGHT // 2
hex_radius = 12
hex_rotation = 0
rotation_speed = 0.03
rotation_direction = 1

circle_size = 2
pulse_time = 0.0
pulse_speed = 0.01

phase = 1
kills = 0
kills_needed = 5
enemy_count = 6

enemies = []
bullets = []

shoot_cooldown = 0
shoot_delay = 0.1

shapes = []
shape_radii = [int(hex_radius * 0.5), int(hex_radius * 0.75), int(hex_radius * 0.95)]

def spawn_shape():
    if len(shapes) >= 3:
        return
    idx = len(shapes)
    shape = {
        'type': random.choice(['triangle', 'square']),
        'angle': random.uniform(0, math.pi * 2),
        'speed': random.uniform(0.02, 0.15) * random.choice([-1, 1]),
        'radius': shape_radii[idx]
    }
    shapes.append(shape)

def draw_shapes():
    for s in shapes:
        s['angle'] += s['speed']
        r = s['radius']
        if s['type'] == "triangle":
            for i in range(3):
                a1 = s['angle'] + (2 * math.pi / 3) * i
                a2 = s['angle'] + (2 * math.pi / 3) * ((i + 1) % 3)
                x1 = int(hex_center_x + math.cos(a1) * r)
                y1 = int(hex_center_y + math.sin(a1) * r)
                x2 = int(hex_center_x + math.cos(a2) * r)
                y2 = int(hex_center_y + math.sin(a2) * r)
                thumby.display.drawLine(x1, y1, x2, y2, 1)
        else:
            for i in range(4):
                a1 = s['angle'] + (math.pi / 2) * i
                a2 = s['angle'] + (math.pi / 2) * ((i + 1) % 4)
                x1 = int(hex_center_x + math.cos(a1) * r)
                y1 = int(hex_center_y + math.sin(a1) * r)
                x2 = int(hex_center_x + math.cos(a2) * r)
                y2 = int(hex_center_y + math.sin(a2) * r)
                thumby.display.drawLine(x1, y1, x2, y2, 1)

def spawn_enemies():
    global pulse_time
    enemies.clear()
    pulse_time = 0.0
    for i in range(enemy_count):
        enemies.append({
            'angle': math.pi / 3 * i,
            'offset': random.uniform(0, math.pi * 2),
            'phase_offset': random.uniform(0, math.pi * 2),
            'alive': True
        })

def reset_game():
    global player_x, player_y, phase, kills, kills_needed, enemy_count
    global hex_rotation, rotation_speed, pulse_time, pulse_speed, bullets, shoot_cooldown, rotation_direction, shapes
    player_x = 5
    player_y = SCREEN_HEIGHT // 2
    phase = 1
    kills = 0
    kills_needed = 5
    enemy_count = 3
    rotation_speed = 0.02
    pulse_speed = 0.03
    pulse_time = 0.1
    rotation_direction = 1
    shoot_cooldown = 0
    bullets.clear()
    shapes.clear()
    spawn_enemies()

def draw_player(px, py):
    dx = hex_center_x - px
    dy = hex_center_y - py
    angle = math.atan2(dy, dx)
    tip_x = int(px + math.cos(angle) * player_size)
    tip_y = int(py + math.sin(angle) * player_size)
    left_x = int(px + math.cos(angle + 2.5) * player_size)
    left_y = int(py + math.sin(angle + 2.5) * player_size)
    right_x = int(px + math.cos(angle - 2.5) * player_size)
    right_y = int(py + math.sin(angle - 2.5) * player_size)
    thumby.display.drawLine(tip_x, tip_y, left_x, left_y, 1)
    thumby.display.drawLine(left_x, left_y, right_x, right_y, 1)
    thumby.display.drawLine(right_x, right_y, tip_x, tip_y, 1)

def get_hex_points(radius, rotation):
    points = []
    for i in range(6):
        angle = math.pi / 3 * i + rotation
        x = int(hex_center_x + math.cos(angle) * radius)
        y = int(hex_center_y + math.sin(angle) * radius)
        points.append((x, y))
    return points

circle_offsets = []
for dx in range(-circle_size, circle_size + 1):
    for dy in range(-circle_size, circle_size + 1):
        if abs(dx) == circle_size or abs(dy) == circle_size:
            circle_offsets.append((dx, dy))

def shoot_bullet(px, py):
    dx = hex_center_x - px
    dy = hex_center_y - py
    dist = (dx*dx + dy*dy) ** 0.5
    if dist == 0:
        return
    vx = (dx / dist) * 2
    vy = (dy / dist) * 2
    bullets.append({'x': px, 'y': py, 'vx': vx, 'vy': vy})

def update_bullets():
    for b in bullets[:]:
        b['x'] += b['vx']
        b['y'] += b['vy']
        x = int(b['x'])
        y = int(b['y'])
        if 0 <= x < SCREEN_WIDTH and 0 <= y < SCREEN_HEIGHT:
            thumby.display.setPixel(x, y, 1)
        else:
            bullets.remove(b)

def update_enemies():
    global pulse_time, kills, phase, rotation_speed, pulse_speed, kills_needed, enemy_count, rotation_direction
    pulse_time += pulse_speed
    base_radius = hex_radius
    pulse_amplitude = 20
    min_radius = 6
    any_alive = False
    for e in enemies:
        if not e['alive']:
            local_wave = math.sin(pulse_time + e['offset'] + e['phase_offset'])
            if abs(local_wave) < 0.2:
                e['angle'] = random.uniform(0, math.pi * 2)
                e['offset'] = random.uniform(0, math.pi * 2)
                e['phase_offset'] = random.uniform(0, math.pi * 2)
                e['alive'] = True
            continue
        any_alive = True
        angle = e['angle'] + hex_rotation
        local_wave = math.sin(pulse_time + e['offset'] + e['phase_offset'])
        local_radius = base_radius + local_wave * pulse_amplitude
        if local_radius < min_radius:
            local_radius = min_radius
        ex = int(hex_center_x + math.cos(angle) * local_radius)
        ey = int(hex_center_y + math.sin(angle) * local_radius)
        for dx in range(-1, 2):
            for dy in range(-1, 2):
                px = ex + dx
                py = ey + dy
                if 0 <= px < SCREEN_WIDTH and 0 <= py < SCREEN_HEIGHT:
                    thumby.display.setPixel(px, py, 1)
        if abs(ex - player_x) < 3 and abs(ey - player_y) < 3:
            thumby.display.fill(0)
            thumby.display.drawText("GAME OVER", 10, 20, 1)
            thumby.display.update()
            time.sleep(2)
            run_menu()
            reset_game()
            return
        for b in bullets[:]:
            if abs(b['x'] - ex) < 2 and abs(b['y'] - ey) < 2:
                bullets.remove(b)
                e['alive'] = False
                kills += 1
                if kills >= kills_needed:
                    phase += 1
                    kills = 0
                    kills_needed += 5
                    rotation_speed += 0.01
                    pulse_speed += 0.005
                    enemy_count = min(enemy_count + 1, 12)
                    if random.random() < 0.5:
                        rotation_direction *= -1
                    spawn_enemies()
                    if phase % 5 == 0 and len(shapes) < 3:
                        spawn_shape()
    if not any_alive:
        spawn_enemies()

run_menu()
reset_game()
player_vx = 0
player_vy = 0

while True:
    thumby.display.fill(0)
    dt = 0.03
    hex_rotation += rotation_speed * rotation_direction
    hex_points = get_hex_points(hex_radius, hex_rotation)
    for i in range(6):
        x1, y1 = hex_points[i]
        x2, y2 = hex_points[(i + 1) % 6]
        thumby.display.drawLine(x1, y1, x2, y2, 1)
    for x, y in hex_points:
        for dx, dy in circle_offsets:
            px = x + dx
            py = y + dy
            if 0 <= px < SCREEN_WIDTH and 0 <= py < SCREEN_HEIGHT:
                thumby.display.setPixel(px, py, 1)
    draw_shapes()
    if shoot_cooldown > 0:
        shoot_cooldown -= dt
    if thumby.buttonA.pressed() and shoot_cooldown <= 0:
        dx = hex_center_x - player_x
        dy = hex_center_y - player_y
        angle = math.atan2(dy, dx)
        tip_x = player_x + math.cos(angle) * player_size
        tip_y = player_y + math.sin(angle) * player_size
        shoot_bullet(tip_x, tip_y)
        shoot_cooldown = shoot_delay
    draw_player(player_x, player_y)
    update_bullets()
    update_enemies()
    friction = 0.92
    accel = 0.6
    if "player_vx" not in globals():
        player_vx = 0
        player_vy = 0
    if thumby.buttonL.pressed():
        player_vx -= accel
    if thumby.buttonR.pressed():
        player_vx += accel
    if thumby.buttonU.pressed():
        player_vy -= accel
    if thumby.buttonD.pressed():
        player_vy += accel
    player_vx *= friction
    player_vy *= friction
    player_x += player_vx
    player_y += player_vy
    if player_x < player_size:
        player_x = player_size
        player_vx = 0
    if player_x > SCREEN_WIDTH - player_size:
        player_x = SCREEN_WIDTH - player_size
        player_vx = 0
    if player_y < player_size:
        player_y = player_size
        player_vy = 0
    if player_y > SCREEN_HEIGHT - player_size:
        player_y = SCREEN_HEIGHT - player_size
        player_vy = 0
    phase_str = str(phase)
    thumby.display.drawText(phase_str, SCREEN_WIDTH - 8, 0, 1)
    thumby.display.update()
    time.sleep(dt)
