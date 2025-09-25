from thumbyGraphics import display
import thumbyButton as buttons
import time, random

# FPS for smooth movement
display.setFPS(60)

# Lane positions (center X for player)
lanes = [20, 36, 52]
player_lane = 1  # Start in middle lane
player_y = 30    # Player's fixed Y position

# Obstacles: list of (lane, y)
obstacles = []

# Game variables
score = 0
speed = 0.1  # Start a bit faster
max_speed = 100.0  # Cap the speed so it doesn't get too fast
acceleration = 0.001  # How much speed increases every frame
spawn_timer = 0

# Lane switch cooldown (in frames)
lane_switch_cooldown = 0
lane_switch_delay = 0  # Smaller number = faster switching



# Game loop

while not buttons.buttonA.justPressed():
    display.setFPS(60)
    display.fill(0)
    display.setFont("/lib/font8x8.bin", 8, 8, display.textSpaceWidth)
    display.drawText("THUMBWAY", 1, 5, 1)
    display.drawText("SURFERS", 5, 15, 1)
    display.setFont("/lib/font3x5.bin", 3, 5, display.textSpaceWidth)
    display.drawText("PRESS A", 1, 34, 1)
    display.update()
while True:
    # ---- INPUT ----
    if lane_switch_cooldown == 0:
        if buttons.buttonL.justPressed():
            player_lane = max(0, player_lane - 1)
            lane_switch_cooldown = lane_switch_delay
        elif buttons.buttonR.justPressed():
            player_lane = min(2, player_lane + 1)
            lane_switch_cooldown = lane_switch_delay
    else:
        lane_switch_cooldown -= 1

    # ---- UPDATE ----
    spawn_timer += 1
    if spawn_timer > 90:
        spawn_timer = 0
        obstacles.append([random.randint(0, 2), -8])

    # Move obstacles
    for obs in obstacles:
        obs[1] += speed

    # Remove off-screen obstacles
    obstacles = [o for o in obstacles if o[1] < 40]

    # Collision detection
    for o in obstacles:
        if o[0] == player_lane and abs(o[1] - player_y) < 6:
            display.fill(0)
            display.setFont("/lib/font8x8.bin", 8, 8, display.textSpaceWidth)
            display.drawText("GAMEOVER", 0, 5, 1)
            display.setFont("/lib/font5x7.bin", 5, 7, display.textSpaceWidth)
            display.drawText("Score:"+str(score), 1, 15, 1)
            display.setFont("/lib/font3x5.bin", 3, 5, display.textSpaceWidth)
            display.drawText("PRESS B", 1, 34, 1)
            display.update()
            while not buttons.buttonB.justPressed():
              time.sleep(0.00001)
            # Reset game
            player_lane = 1
            obstacles = []
            speed = 0.25
            score = 0
            lane_switch_cooldown = 0
            spawn_timer = 0

    # Increase speed gradually, capped at max_speed
    if speed < max_speed:
        speed += acceleration
    if buttons.buttonB.justPressed():
        while not buttons.buttonA.justPressed():
            display.fill(0)
            display.setFont("/lib/font8x8.bin", 8, 8, display.textSpaceWidth)
            display.drawText(str('PAUSE'), 14, 15, 1)
            display.update()
    # ---- DRAW ----
    display.fill(0)
    display.drawText(str(score), 0, 0, 1)

    # Draw lanes (optional)
    display.drawLine(28, 0, 28, 40, 1)
    display.drawLine(44, 0, 44, 40, 1)

    # Draw player
    display.drawFilledRectangle(lanes[player_lane]-3, player_y-3, 6, 6, 1)

    # Draw obstacles
    for o in obstacles:
        display.drawFilledRectangle(lanes[o[0]]-3, int(o[1])-3, 6, 6, 1)

    display.update()
    score += 1