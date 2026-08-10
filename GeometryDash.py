#Geometry Dash for the thumby by Nathan Goodin
#Copy and paste directly into the thumby code editor to edit this.
#Inspired by the game 'zig' from the thumby arcade :)


import thumby
import random

thumby.display.setFPS(30)

debug, player_y, score, spikeTick, screen, moveSpeed, highscore, spikeSpeed = 0, 20, 0, 0, "menu", 1, 0, 1
is_mini, gamemode, ufo_vel, cube_vel, portal_timer = False, 1, 0.0, 0.0, 0
portal_spawn_time = random.randint(300, 450)
portal_active, portal_x, portal_y, portal_type = False, -20, 10, 1
spike_x, spike_y, spike_is_double = 80, 20, False
spike2_x, spike2_y, spike2_is_double = 80, 20, False

# Wave trail array keeping track of [x, y] coordinates
trail = []

# Jump Orb tracking variables
orb_active = False
orb_x = -10
orb_y = 23 # Fixed height line for natural cube integration
orb_timer = 0

def safe_play_audio(freq, duration):
    try: thumby.audio.stop()
    except: pass
    thumby.audio.play(int(freq), int(duration))

def draw_hazards(gamemode, s1x, s1y, s1d, s2x, s2y, s2d):
    for sx, sy, sd in [(s1x, s1y, s1d), (s2x, s2y, s2d)]:
        if gamemode == 3:
            thumby.display.drawLine(sx, sy + 6, sx + 3, sy, 1)
            thumby.display.drawLine(sx + 3, sy, sx + 6, sy + 6, 1)
            thumby.display.drawLine(sx, sy + 6, sx + 6, sy + 6, 1)
            if sd:
                thumby.display.drawLine(sx + 6, sy + 6, sx + 9, sy, 1)
                thumby.display.drawLine(sx + 9, sy, sx + 12, sy + 6, 1)
                thumby.display.drawLine(sx + 6, sy + 6, sx + 12, sy + 6, 1)
        else: thumby.display.drawRectangle(sx, sy, 6, 6, 1)

def draw_player(gamemode, is_mini, px, py, p_size):
    if gamemode == 1:
        if is_mini:
            thumby.display.drawLine(px, py, px + 4, py + 2, 1)
            thumby.display.drawLine(px, py + 4, px + 4, py + 2, 1)
            thumby.display.drawLine(px, py, px, py + 4, 1)
        else:
            thumby.display.drawLine(px, py, px + 6, py + 3, 1)
            thumby.display.drawLine(px, py + 6, px + 6, py + 3, 1)
            thumby.display.drawLine(px, py, px, py + 6, 1)
    elif gamemode == 2:
        if is_mini:
            thumby.display.drawRectangle(px, py + 1, 5, 2, 1)
            thumby.display.drawLine(px + 1, py, px + 3, py, 1)
        else:
            thumby.display.drawRectangle(px, py + 2, 7, 3, 1)
            thumby.display.drawLine(px + 2, py + 1, px + 4, py + 1, 1)
    elif gamemode == 3: thumby.display.drawRectangle(px, py, p_size, p_size, 1)
while(1):
    thumby.display.fill(0)
    thumby.display.drawLine(0, 0, 72, 0, 1)
    thumby.display.drawLine(0, 39, 72, 39, 1)
    if thumby.buttonD.pressed() and thumby.buttonA.pressed(): debug = 1
        
    if screen == "menu":
        thumby.display.drawText("GD wave", 15, 6, 1)
        thumby.display.drawText("Press A/B", 9, 30, 1)
        thumby.display.drawText("Hi: %d" % highscore, 9, 20, 1)
        if thumby.actionJustPressed(): 
            safe_play_audio(300, 50)
            screen = "game"
            trail = []
            orb_active = False
            orb_timer = 0
            
    if screen == "game":
        score += 1
        thumby.display.drawText("%d" % (score // 30), 4, 30, 1)
        draw_hazards(gamemode, int(spike_x), int(spike_y), spike_is_double, int(spike2_x), int(spike2_y), spike2_is_double)
        
        # Jump Orb Management Engine
        if gamemode == 3:
            orb_timer += 1
            if orb_timer >= 150 and not orb_active:
                orb_timer = 0
                if int(spike_x) < 65 and int(spike2_x) < 65:
                    orb_active = True
                    orb_x = 75
            
            if orb_active:
                orb_x -= spikeSpeed
                thumby.display.drawLine(int(orb_x) + 1, int(orb_y), int(orb_x) + 3, int(orb_y), 1)
                thumby.display.drawLine(int(orb_x) + 1, int(orb_y) + 4, int(orb_x) + 3, int(orb_y) + 4, 1)
                thumby.display.drawLine(int(orb_x), int(orb_y) + 1, int(orb_x), int(orb_y) + 3, 1)
                thumby.display.drawLine(int(orb_x) + 4, int(orb_y) + 1, int(orb_x) + 4, int(orb_y) + 3, 1)
                thumby.display.setPixel(int(orb_x) + 2, int(orb_y) + 2, 1)
                
                if int(orb_x) >= 14 and int(orb_x) <= 26:
                    if thumby.actionPressed():
                        orb_active = False
                        cube_vel = -3.5     
                        safe_play_audio(800, 60)
                
                if orb_x < -6:
                    orb_active = False
        else:
            orb_active = False
            orb_timer = 0

        # Fixed trail processing logic to handle [x, y] coordinates correctly
        if gamemode == 1:
            updated_trail = []
            for point in trail:
                point[0] -= spikeSpeed # Move X coordinate left
                if point[0] >= 0:      # Only keep visible pieces
                    updated_trail.append(point)
                    thumby.display.setPixel(int(point[0]), int(point[1]), 1)
                    thumby.display.setPixel(int(point[0]), int(point[1] + 1), 1)
            trail = updated_trail
        else:
            trail = []

        portal_timer += 1
        if portal_timer >= portal_spawn_time and not portal_active:
            portal_active, portal_x, portal_y = True, 85, random.randint(6, 18)
            portal_type = random.randint(1, 5)
            portal_timer, portal_spawn_time = 0, random.randint(300, 450)

        if portal_active:
            portal_x -= spikeSpeed
            thumby.display.drawRectangle(int(portal_x), int(portal_y), 5, 17, 1)
            lbls = ["M", "R", "U", "W", "C"]
            thumby.display.drawText(lbls[portal_type-1], int(portal_x - 6), int(portal_y + 4), 1)

            if portal_x < 26 and portal_x > 14:
                if player_y + 6 >= portal_y and player_y <= portal_y + 16:
                    prev_mode = gamemode
                    if portal_type == 1 and not is_mini: is_mini = True
                    elif portal_type == 2 and is_mini: is_mini = False
                    elif portal_type == 3 and gamemode != 2: gamemode, ufo_vel = 2, 0.0
                    elif portal_type == 4 and gamemode != 1: gamemode = 1
                    elif portal_type == 5 and gamemode != 3: gamemode, cube_vel = 3, 0.0
                    if gamemode != prev_mode: trail = []
                    safe_play_audio(500, 150)
            if portal_x < -10: portal_active = False

        if spikeTick < 200:
            spikeTick += 1; spike_x -= spikeSpeed; spike2_x -= spikeSpeed
            if spikeTick == 100: spike2_is_double, spike2_y, spike2_x = (random.random() < 0.5), (33 if gamemode == 3 else random.randint(5, 26)), 80
        else:
            spikeTick = 0; spike_is_double = (random.random() < 0.5)
            spike_y, spike_x = (33 if gamemode == 3 else random.randint(5, 26)), 80

        if gamemode == 1:
            current_speed = 2 if is_mini else 1
            if thumby.actionPressed(): player_y -= current_speed
            else: player_y += current_speed
            for sy in [spike_y, spike2_y]:
                if int(spike_x) <= 20 + (4 if is_mini else 6) and int(spike_x) + 6 > 20:
                    if player_y + (4 if is_mini else 6) >= int(sy) and player_y < int(sy): player_y = int(sy) - (4 if is_mini else 6)
            if player_y < 1: player_y = 1
            elif player_y > 33: player_y = 33
            
            trail_offset_y = 2 if is_mini else 3
            # Store point as an [x, y] list item
            trail.append([20.0, player_y + trail_offset_y])
            
        elif gamemode == 2:
            ufo_vel += 0.25
            if ufo_vel > 2.0: ufo_vel = 2.0
            if thumby.actionJustPressed(): ufo_vel = -2.0; safe_play_audio(700, 40)
            player_y += ufo_vel
            for sy in [spike_y, spike2_y]:
                if int(spike_x) <= 20 + 6 and int(spike_x) + 6 > 20:
                    if player_y + 5 >= int(sy) and player_y < int(sy): player_y = int(sy) - 5; ufo_vel = 0.0
            if player_y < 1: player_y = 1; ufo_vel = 0.0
            elif player_y > 33: player_y = 33; ufo_vel = 0.0
        elif gamemode == 3:
            cube_vel += 0.25
            if cube_vel > 3.0: cube_vel = 3.0
            if thumby.actionPressed() and player_y >= 33: cube_vel = -3.0; safe_play_audio(650, 45)
            player_y += cube_vel
            if player_y > 33: player_y = 33; cube_vel = 0.0

        p_size, player_x = (4 if is_mini else 6), 20
        draw_player(gamemode, is_mini, player_x, int(player_y), p_size)
            
        for sx, sy, sd in [(spike_x, spike_y, spike_is_double), (spike2_x, spike2_y, spike2_is_double)]:
            hx = 12 if (gamemode == 3 and sd) else 6
            if int(sx) <= player_x + p_size and int(sx) + hx > player_x:
                if player_y + p_size > int(sy) and player_y < int(sy) + 6:
                    if gamemode == 3: spike_y, spike2_y = 100, 100; screen = "death"
                    else:
                        if int(sx) > player_x + 1 and int(sx) < player_x + p_size:
                            if player_y + p_size - 1 > int(sy) and player_y + 1 < int(sy) + 6: spike_y, spike2_y = 100, 100; screen = "death"
                            
    if screen == "death":
        thumby.display.drawText("You died!", 9, 2, 1); thumby.display.drawText("Scr: %d" % (score // 30), 3, 14, 1)
        if (score // 30) > highscore: highscore = int(score // 30)
        thumby.display.drawText("Press A&B", 9, 30, 1)
        if thumby.buttonA.pressed() and thumby.buttonB.pressed():
            score, spikeTick, player_y, ufo_vel, cube_vel = 0, 400, 20, 0.0, 0.0
            is_mini, gamemode, portal_active = False, 1, False; screen = "game"
            trail = []
            orb_active = False
            orb_timer = 0
            
    thumby.display.update()
