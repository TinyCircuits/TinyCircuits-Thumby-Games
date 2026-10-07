import thumby
import time
import random

# ---------------- WORLD ----------------
W, H, BLOCK = 24, 10, 3
world = [[1 if y > 6 else 0 for x in range(W)] for y in range(H)]

def solid(x, y):
    return x < 0 or x >= W or y < 0 or y >= H or world[y][x] != 0

# ---------------- PLAYER ----------------
px, py = 2, 4
hearts = 5
fly = False
armor = 0
max_armor = 3
fall_distance = 0
was_falling = False
regen_timer = 0
regen_interval = 50

# Triple-A tracking
a_count = 0
a_timer = 0

# ---------------- INVENTORY ----------------
inventory = False
inventory_items = [
    ["Pickaxe", -1],
    ["Sword", -1],
    ["Dirt", 0],
    ["Wood", 0],
    ["Armor", 0]
]
selected = 0

game_over = False

# ---------------- VILLAGE ----------------
villagers = []
village_start = 18
village_width = 4

def make_village(x0):
    global villagers
    for x in range(x0, min(x0 + village_width, W)):
        for y in range(5, 7):
            world[y][x] = 1
    villagers[:] = [(x0 + 1, 4), (x0 + 2, 4)]

# ---------------- ZOMBIES ----------------
zombies = []
zombie_spawn_timer = 600
zombie_spawn_interval = 600
safe_zone_start = village_start - 6
zombie_hit_cooldown = {}
hit_interval = 10

# ---------------- CLOUDS ----------------
clouds = [
    {"x": 0, "y": 1, "w": 6, "h": 2},
    {"x": 12, "y": 0, "w": 5, "h": 2},
]
cloud_speed = 0.05

# ---------------- INVENTORY HELPERS ----------------
def add_item(name, amount=1):
    for item in inventory_items:
        if item[0] == name:
            item[1] += amount
            return

def has_item(name, amount):
    for item in inventory_items:
        if item[0] == name and item[1] >= amount:
            return True
    return False

def remove_item(name, amount):
    for item in inventory_items:
        if item[0] == name:
            item[1] -= amount
            if item[1] < 0:
                item[1] = 0
            return

# ---------------- RESET ----------------
def reset_game():
    global px, py, hearts, fly, inventory, selected, villagers, zombies, game_over, zombie_spawn_timer, zombie_hit_cooldown, armor
    px, py = 2, 4
    hearts = 5
    fly = False
    armor = 0
    inventory = False
    selected = 0
    villagers = []
    zombies = []
    zombie_hit_cooldown.clear()
    zombie_spawn_timer = zombie_spawn_interval
    for y in range(H):
        for x in range(W):
            world[y][x] = 1 if y > 6 else 0
    for item in inventory_items:
        if item[1] != -1:
            item[1] = 0
    game_over = False

# ---------------- MINING ----------------
def mine_block(x, y):
    if 0 <= x < W and 0 <= y < H:
        if world[y][x] == 1:
            world[y][x] = 0
            if 5 <= y <= 6 and village_start <= x < village_start + village_width:
                add_item("Wood")
            else:
                add_item("Dirt")

# ---------------- PLACING ----------------
def place_block(x, y):
    if 0 <= x < W and 0 <= y < H:
        if world[y][x] == 0:
            world[y][x] = 1
            return True
    return False

# ---------------- ITEM ICONS ----------------
def draw_icon(name, x, y, color):
    if name == "Dirt":
        thumby.display.drawFilledRectangle(x, y, 4, 4, color)
    elif name == "Wood":
        thumby.display.drawRectangle(x, y, 4, 4, color)
    elif name == "Pickaxe":
        thumby.display.drawLine(x, y, x+4, y+4, color)
    elif name == "Sword":
        thumby.display.drawLine(x, y+4, x+4, y, color)
    elif name == "Armor":
        thumby.display.drawRectangle(x, y, 5, 5, color)

# ---------------- MAIN LOOP ----------------
while True:
    thumby.display.fill(0)

    # ---------------- MOVE CLOUDS ----------------
    for cloud in clouds:
        cloud["x"] -= cloud_speed
        if cloud["x"] + cloud["w"] < 0:
            cloud["x"] = W
        thumby.display.drawFilledRectangle(
            int(cloud["x"] * BLOCK),
            int(cloud["y"] * BLOCK),
            cloud["w"] * BLOCK,
            cloud["h"] * BLOCK,
            1
        )

    # ---------------- GAME OVER ----------------
    if game_over:
        thumby.display.drawText("GAME OVER", 12, 14, 1)
        thumby.display.drawText("A=Respawn", 8, 24, 1)
        thumby.display.update()
        if thumby.buttonA.justPressed():
            reset_game()
        time.sleep(0.1)
        continue

    # ---------------- INVENTORY TOGGLE ----------------
    if thumby.buttonB.justPressed():
        inventory = not inventory

    # ---------------- INVENTORY MODE ----------------
    if inventory:
        # Move selection
        if thumby.buttonU.justPressed():
            selected = (selected - 1) % len(inventory_items)
        if thumby.buttonD.justPressed():
            selected = (selected + 1) % len(inventory_items)

        # Draw inventory grid
        cols = 2
        slot_w, slot_h = 30, 12
        for i, item in enumerate(inventory_items):
            name, count = item
            col = i % cols
            row = i // cols
            x = 6 + col * slot_w
            y = 10 + row * slot_h
            thumby.display.drawRectangle(x, y, 26, 10, 1)
            if i == selected:
                thumby.display.drawFilledRectangle(x, y, 26, 10, 1)
            draw_icon(name, x+2, y+2, 0 if i == selected else 1)
            if count != -1:
                thumby.display.drawText(str(count), x+14, y+2, 0 if i == selected else 1)

        # Inventory actions
        if thumby.buttonA.justPressed():
            name, count = inventory_items[selected]

            # Craft armor: 3 wood -> 1 armor
            if name == "Armor" and has_item("Wood", 3):
                remove_item("Wood", 3)
                add_item("Armor", 1)

            # Place block
            if name in ("Dirt", "Wood") and count > 0:
                tx, ty = px, py + 1
                if thumby.buttonL.pressed():
                    tx, ty = px - 1, py
                elif thumby.buttonR.pressed():
                    tx, ty = px + 1, py
                if place_block(tx, ty):
                    remove_item(name, 1)

            # Equip armor
            if name == "Armor" and count > 0:
                if armor < max_armor:
                    armor += 1
                    remove_item("Armor", 1)

            # Attack zombies
            if name == "Sword":
                attack_x = px
                if thumby.buttonL.pressed():
                    attack_x = px - 1
                elif thumby.buttonR.pressed():
                    attack_x = px + 1
                zombies[:] = [z for z in zombies if z[0] != attack_x or z[1] != py]

    # ---------------- GAME MODE ----------------
    else:
        if thumby.buttonL.pressed() and not solid(px - 1, py):
            px -= 1
        if thumby.buttonR.pressed() and not solid(px + 1, py):
            px += 1
            if px == 16:
                make_village(village_start)

        # ---------------- GRAVITY + FALL DAMAGE ----------------
        if not fly:
            if not solid(px, py + 1):
                py += 1
                fall_distance += 1
                was_falling = True
            else:
                if was_falling:
                    if fall_distance > 2:
                        damage = (fall_distance - 2) // 2
                        reduced = max(0, damage - armor)
                        hearts -= reduced
                        if hearts <= 0:
                            game_over = True
                    fall_distance = 0
                    was_falling = False

        # Mining
        if inventory_items[selected][0] == "Pickaxe":
            if thumby.buttonU.justPressed():
                mine_block(px, py - 1)
            elif thumby.buttonD.justPressed():
                mine_block(px, py + 1)
            elif thumby.buttonL.justPressed():
                mine_block(px - 1, py)
            elif thumby.buttonR.justPressed():
                mine_block(px + 1, py)

    # ---------------- TRIPLE A FLY ----------------
    if thumby.buttonA.justPressed():
        a_count += 1
        a_timer = 10

    if a_timer > 0:
        a_timer -= 1
    else:
        if a_count >= 3:
            fly = not fly
        a_count = 0

    if fly:
        if thumby.buttonU.pressed() and py > 0:
            py -= 1
        if thumby.buttonD.pressed() and py + 1 < H:
            py += 1
        fall_distance = 0
        was_falling = False

    # ---------------- ZOMBIE SPAWN ----------------
    if zombie_spawn_timer > 0:
        zombie_spawn_timer -= 1
    else:
        spawn_x = W - 1
        if spawn_x >= safe_zone_start:
            spawn_x = safe_zone_start - 1
        zombies.append([spawn_x, 4, 0])
        zombie_spawn_timer = zombie_spawn_interval

    # ---------------- ZOMBIE MOVEMENT & DAMAGE ----------------
    for z in zombies:
        zx, zy, age = z
        age += 1

        # Movement
        if zx > px and not solid(zx-1, zy):
            zx -= 1
        elif zx < px and not solid(zx+1, zy):
            zx += 1
        if not solid(zx, zy+1):
            zy += 1

        # Cooldown tracking
        zid = id(z)
        if zid not in zombie_hit_cooldown:
            zombie_hit_cooldown[zid] = 0

        if zx == px and zy == py:
            if zombie_hit_cooldown[zid] == 0:
                # Damage chance decreases as zombie ages
                if age < 200:
                    hit_chance = 0.9
                elif age < 400:
                    hit_chance = 0.6
                elif age < 600:
                    hit_chance = 0.3
                else:
                    hit_chance = 0.1

                if random.random() < hit_chance:
                    hearts -= max(0, 1 - armor)
                zombie_hit_cooldown[zid] = hit_interval
                if hearts <= 0:
                    game_over = True
        else:
            zombie_hit_cooldown[zid] = max(0, zombie_hit_cooldown[zid]-1)

        if zombie_hit_cooldown[zid] > 0:
            zombie_hit_cooldown[zid] -= 1

        z[0], z[1], z[2] = zx, zy, age

    # ---------------- DRAW WORLD ----------------
    for y in range(H):
        for x in range(W):
            if world[y][x]:
                thumby.display.drawFilledRectangle(x*BLOCK, y*BLOCK, BLOCK, BLOCK, 1)

    # PLAYER
    thumby.display.drawFilledRectangle(px*BLOCK, py*BLOCK, BLOCK, BLOCK, 1)

    # Villagers
    for vx, vy in villagers:
        thumby.display.drawRectangle(vx*BLOCK, vy*BLOCK, BLOCK, BLOCK, 1)

    # Zombies
    for zx, zy, _ in zombies:
        thumby.display.drawRectangle(zx*BLOCK, zy*BLOCK, BLOCK, BLOCK, 1)

    # ---------------- HOTBAR ----------------
    hotbar_slots = 4
    for i in range(hotbar_slots):
        if i >= len(inventory_items):
            break
        name, count = inventory_items[i]
        x = 2 + i * 16
        y = 32
        thumby.display.drawRectangle(x, y, 14, 8, 1)
        if i == selected and not inventory:
            thumby.display.drawFilledRectangle(x, y, 14, 8, 1)
        draw_icon(name, x+2, y+2, 0 if i == selected and not inventory else 1)

    # ---------------- HEARTS & ARMOR ----------------
    for i in range(hearts):
        thumby.display.drawFilledRectangle(2+i*6, 2, 4,4,1)
    for i in range(armor):
        thumby.display.drawRectangle(2+i*6, 8, 4,4,1)

    # ---------------- HEART REGEN ----------------
    touching_zombie = any(z[0] == px and z[1] == py for z in zombies)
    if hearts < 5 and not touching_zombie:
        regen_timer += 1
        if regen_timer >= regen_interval:
            hearts += 1
            regen_timer = 0
    else:
        regen_timer = 0

    thumby.display.update()
    time.sleep(0.1)
