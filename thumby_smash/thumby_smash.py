import random, thumby, time, gc
gc.enable()
box = bytearray([0,254,254,254,254,254,254,254,254,254,254,254,254,254,254,0,
            0,127,127,127,127,127,127,127,127,127,127,127,127,127,127,0])
def singleplayer_battle(char, enemy_char, config):
    def character_move(name, jumpheight, attack, health, speed, weight, player_type, state, x, y, direction, a_x, a_y, a_jumpheight, a_attack, a_health, a_speed, a_weight, cooldown, knockback_state, data, config):
        goggles_walk_sprite = bytearray([243,245,246,150,98,108,142,158,110,108,130,22,246,245,243,255,
               255,255,255,191,222,101,155,155,99,93,126,255,255,255,255,255])
        
        goggles_icon = bytearray([243,245,246,6,146,108,110,158,158,108,98,22,246,245,243,255,
                    255,255,255,255,254,253,251,251,251,253,254,255,255,255,255,255])
        goggles_attack_1 = bytearray([243,245,246,6,146,108,110,158,158,108,98,22,246,245,243,255,
                255,255,255,191,222,101,155,155,99,221,238,239,199,171,171,255])
        goggles_attack_2 = bytearray([243,245,246,6,146,108,110,158,158,108,98,22,246,245,243,255,
                255,255,255,191,222,101,155,155,99,221,238,239,199,171,199,255])
        gogglesattackupper = bytearray([243,245,246,6,146,108,110,158,158,108,98,22,246,245,115,255,
                255,255,255,191,222,101,155,155,99,221,238,247,249,242,245,250])
        goggles_trident_side = bytearray([119,119,119,119,99,85,85])
        goggles_trident_up = bytearray([127,120,119,0,119,112,127])
        zap_walk = bytearray([231,231,251,253,27,231,247,119,87,111,31,255,255,255,255,255,
           255,255,255,255,255,254,85,129,85,254,255,255,255,255,255,255])
        zap_hit = bytearray([231,231,251,253,27,231,247,247,215,239,31,255,255,255,255,255,
           255,255,255,255,255,254,253,253,253,254,245,251,213,239,151,223])
        zap_attack_1 = bytearray([231,231,251,253,27,231,247,119,87,111,31,255,255,255,255,255,
               255,255,255,255,255,254,85,129,85,250,251,253,255,255,255,255])
        zap_attack_2 = bytearray([255,255,255,255,255,255,255,63,223,239,239,111,207,55,199,199,
               255,255,255,255,255,255,87,130,85,250,249,251,253,254,255,255])
        zap_attack_upper_frame_1  = bytearray([231,231,251,253,27,231,247,119,87,111,31,255,255,255,255,255,
               255,253,251,247,247,246,85,129,85,246,247,247,251,253,254,255])
        zap_attack_upper_frame_2 = bytearray([231,231,251,253,27,103,87,119,87,111,31,255,255,255,255,255,
               255,253,251,247,247,246,85,129,85,246,247,247,251,253,254,255])
        apex_icon = bytearray([63,222,237,51,219,109,245,245,245,245,109,219,51,237,222,63,
           120,183,207,216,183,108,95,95,95,95,108,183,216,207,183,120])
        apex_walk = bytearray([63,222,237,51,219,109,245,245,245,245,109,219,51,237,222,63,
           120,183,207,216,183,108,95,95,95,95,108,183,216,207,183,120])
        apex_walk_1 = bytearray([63,222,237,51,219,109,245,245,245,245,109,219,51,237,222,63,
           120,183,207,216,183,108,95,95,95,95,108,183,216,207,183,120])
        apex_walk_2 = bytearray([63,222,237,51,219,237,245,181,181,181,237,219,51,237,222,63,
           120,183,207,216,183,111,95,91,91,91,111,183,216,207,183,120])
        apex_walk_3 = bytearray([63,222,237,51,219,237,181,181,181,245,237,219,51,237,222,63,
           120,183,207,216,183,111,91,91,91,95,111,183,216,207,183,120])
        apex_walk_4 = bytearray([63,222,237,51,219,237,245,245,245,245,237,219,51,237,222,63,
           120,183,207,216,183,111,88,95,95,88,111,183,216,207,183,120])
        apex_attack_1 = bytearray([63,222,237,51,219,173,117,245,245,117,173,219,51,237,222,63,
           120,183,207,216,183,111,87,88,88,87,111,183,216,207,183,120])
        apex_attack_2 = bytearray([63,222,237,51,219,237,245,21,21,245,237,219,51,237,222,20,
           120,183,207,216,183,111,95,82,82,95,111,183,216,207,183,120])
        blobbo_walk_1 = bytearray([255,255,255,251,59,219,235,235,235,235,219,59,251,251,255,255,
           255,255,255,224,223,189,183,183,183,183,189,223,224,255,255,255])
        blobbo_walk_2 = bytearray([255,255,255,255,127,127,191,191,191,191,127,127,255,255,255,255,
           255,255,225,222,223,187,175,175,175,175,187,223,222,225,255,255])
        fang_walk_1 = bytearray([207,211,161,205,204,30,246,226,246,254,252,97,3,113,56,255,
           255,255,255,248,246,246,249,132,62,126,126,126,64,0,56,255])
        fang_walk_2 = bytearray([255,211,161,205,204,30,246,226,246,254,252,97,3,113,56,255,
           255,255,255,120,54,54,57,4,62,254,254,254,192,128,56,255])
        fang_attack_1 = bytearray([255,211,161,205,204,30,246,226,246,254,252,97,3,113,56,255,
           239,199,239,232,230,230,233,132,46,110,110,110,64,0,56,255])
        fang_attack_2 = bytearray([7,179,49,205,205,29,246,226,246,254,254,252,61,195,227,248,
           255,254,255,120,54,54,57,4,62,62,184,162,128,128,24,159])
        delta_shift = bytearray([255,255,249,246,143,103,38,6,6,38,103,143,246,249,255,255,
           255,243,247,231,219,92,156,155,155,156,92,219,231,247,243,255])
        delta_walk = bytearray([255,255,249,246,143,103,38,6,6,6,7,15,246,249,255,255,
           255,243,247,231,219,92,156,152,152,156,92,216,231,247,243,255])
        delta_arrow =  bytearray([59,57,0,0,57,59])
        tempestas_attack_1 = bytearray([255,251,5,123,255,7,59,189,189,187,7,255,127,191,255,255,
           255,255,192,255,226,236,14,233,227,7,236,226,255,255,255,255])
        tempestas_walk_1 = bytearray([123,4,123,255,131,57,190,190,56,128,128,192,224,241,255,255,
           255,192,255,126,34,204,222,221,204,34,126,254,255,255,255,255])
        tempestas_walk_2 = bytearray([123,4,123,255,131,57,190,190,56,128,128,192,224,241,255,255,
           255,192,255,126,34,204,222,221,204,162,190,222,255,255,255,255])
        tempestas_walk_3 = bytearray([123,4,123,255,131,57,190,190,56,128,128,192,224,241,255,255,
           255,192,255,158,162,204,222,221,204,34,126,254,255,255,255,255])
        # BITMAP: width: 10, height: 6
        cloud = bytearray([35,45,29,44,30,46,30,28,45,51])
        # BITMAP: width: 4, height: 8
        lightning = bytearray([187,85,238,255])
        # BITMAP: width: 6, height: 6
        spark = bytearray([30,45,51,51,45,30])
        # BITMAP: width: 8, height: 8
        fang_spark = bytearray([215,187,85,170,85,187,215,255])
        # BITMAP: width: 32, height: 8
        charge_beam_right = bytearray([126,189,195,239,247,239,247,239,247,239,247,239,247,239,247,239,247,239,247,239,247,239,247,239,247,239,247,239,247,239,247,239])
        line_2 = bytearray([255,129,255,135,255,129,255,135])
        waves = bytearray([189,219,231,255,189,219,231,255])
        # BITMAP: width: 12, height: 12
        portal = bytearray([7,251,13,246,218,172,182,246,6,253,251,7,
           14,13,11,6,5,5,5,6,7,11,13,14])
        # BITMAP: width: 20, height: 20
        waves_2 = bytearray([127,143,241,254,127,143,241,254,255,255,255,255,254,241,143,127,254,241,143,127,
           240,15,255,255,240,15,255,255,255,255,255,255,255,255,15,240,255,255,15,240,
           15,15,8,7,15,15,8,7,15,15,15,15,7,8,15,15,7,8,15,15])
        is_flipped_x = False
        is_flipped_y = False
        hitdata = [a_x,a_y, a_health]
        is_hit = False
        trident_data = None
        
        #End Match Screen
        def match_screen(outcome):
            match_over = True
            while match_over == True:   
                thumby.display.fill(1)
                thumby.display.drawText(outcome, 20, 12, 0)
                thumby.display.update()
                time.sleep(0.1)
                if thumby.buttonB.pressed():
                    match_over = False
                    battling = False
                    character_select(config)
                    
        #Hit function for most (NOT ALL) damaging attacks       
        def hit(damage, weight, x_knockback, y_knockback, direction, a_x, a_y, a_health):
            knockback_state = int(int(x_knockback - weight) * (health // 50)) 
            a_y += (y_knockback - weight) * health // 50
            a_health -= damage
            return [a_x, a_y, a_health, knockback_state]
            
        A_Pressed = False
        AR_Pressed = False
        AU_Pressed = False
        BU_Pressed = False
        B_Pressed = False
        R_Pressed = False
        L_Pressed = False
        U_Pressed = False
        
        difficulty = config[0]
        
        #if knockback, disable controls: 
        if knockback_state != 0:
                A_Pressed = False
                AR_Pressed = False
                AU_Pressed = False
                BU_Pressed = False
                B_Pressed = False
                R_Pressed = False
                L_Pressed = False
                U_Pressed = False
                knockback_state -= 1
                if direction == 'Right':
                    a_x += 10
                elif direction == 'Left':
                    a_x -= 10
        
        if player_type == 'human':
            if thumby.buttonB.pressed() and thumby.buttonU.pressed():
                BU_Pressed = True
            elif thumby.buttonA.pressed() and thumby.buttonR.pressed():
                AR_Pressed = True
            elif thumby.buttonA.pressed() and thumby.buttonU.pressed():
                AU_Pressed = True
            elif thumby.buttonA.pressed():
                A_Pressed = True
            elif thumby.buttonB.pressed():
                B_Pressed = True
            elif thumby.buttonR.pressed():
                R_Pressed = True
            elif thumby.buttonL.pressed():
                L_Pressed = True
            elif thumby.buttonU.pressed():
                U_Pressed = True
        
        
        #Zap AI
        elif player_type == 'ai' and name == 'zap':
            decision = random.randint(1,2)
            if  x > a_x + 10:
                L_Pressed = True
            elif a_x > x + 10: 
                R_Pressed = True
            if a_y < 20:
                BU_Pressed = True
            else:
                decision = random.randint(1,2)
                if cooldown == 0 and decision == 1:
                    for i in range(16+difficulty):
                        if x + i == a_x or x - i == a_x:
                            for j in range(16+difficulty):
                                if y + j == a_y or y - j == a_y:
                                    A_Pressed = True
          
        #Goggles AI                          
        elif player_type == 'ai' and name == 'goggles':
            decision = random.randint(1,2)
            if  x > a_x + 10:
                L_Pressed = True
            elif a_x > x + 10:
                R_Pressed = True
            if decision == 1:
                U_Pressed = True
            else:
                decision = random.randint(1,3)
                if cooldown == 0 and decision > 1:
                    for i in range(16+difficulty):
                        if x + i == a_x or x - i == a_x:
                            for j in range(16+difficulty):
                                if y + j == a_y or y - j == a_y:
                                    A_Pressed = True
                elif cooldown == 0 and decision == 1:
                   B_Pressed = True 
        
        #Apex AI
        elif player_type == 'ai' and name == 'apex':
            decision = random.randint(1,2)
            if  x > a_x + 20:
                L_Pressed = True
            elif a_x > x + 20:
                R_Pressed = True
            if cooldown == 0 :
                A_Pressed = True
                
        #Fang AI
        elif player_type == 'ai' and name == 'fang':
            if a_x - x > 20 and direction == 'Right' or x - a_x > 20 and direction == 'Left':
                    A_Pressed = True
                    if state == 'charging' and data[0] > 10:
                        A_Pressed = False
            elif a_x > x:
                R_Pressed = True
            elif x > a_x:
                L_Pressed = True
            if cooldown == 0:
                B_Pressed = True
                
        #Tempestas AI
        elif player_type == 'ai' and name == 'tempestas':
            decision = random.randint(1,10)
            if decision > 1 and state != 'cloud':
                if  x > a_x + 30:
                    L_Pressed = True
                elif a_x > x + 30:
                    R_Pressed = True
                if cooldown == 0:
                    A_Pressed = True
            elif decision == 1 and state != 'cloud':
                B_Pressed = True
            if state == 'cloud' and data != None:
                if data > a_x:
                    L_Pressed = True
                elif a_x > data:
                    R_Pressed = True
                for i in range(16+difficulty):
                    if i + data == a_x or i - data == a_x or data == a_x:
                        B_Pressed = True
        #Zap Code        
        if name == 'zap':
            is_hit = False
            current_sprite = zap_walk
            if direction == 'Right':
                current_sprite = zap_walk
                is_flipped_x = False
                state = 'walk_right'
            elif direction == 'Left' and y:
                is_flipped_x = True
                current_sprite = zap_walk
                state = 'walk_left'
            
            if A_Pressed == True and cooldown == 0:
                cooldown = 4
                if direction == 'Right':
                    is_flipped_x = False
                    current_sprite = zap_attack_1
                    state = 'attack_1_right'
                    for i in range(16):
                        if x + i == a_x:
                            for j in range(16):
                                if y + j == a_y:
                                    is_hit = True
                            
                else:
                    is_flipped_x = True
                    current_sprite = zap_attack_1
                    state = 'attack_1_left'
                    for i in range(16):
                        if x + i == a_x:
                            for j in range(16):
                                if y - j == a_y:
                                    is_hit = True
                if is_hit == True:
                    hitdata = hit(15, a_weight, 12, 15, direction, a_x, a_y, a_health)
                    a_x = hitdata[0]
                    a_y = hitdata[1]
                    a_health = hitdata[2]
                    knockback_state = hitdata[3]
                                   
            elif BU_Pressed == True and cooldown == 0:
                if state != 'attack_2_upper_1' and state != 'attack_2_upper_2' and state != 'attack_2_upper_3' and cooldown == 0:
                    cooldown = 10
                    y -= jumpheight
                    for i in range(16):
                        if x + i == a_x or x - i == a_x:
                            for j in range(6):
                                if y + j == a_y or y - j == a_y:
                                    hitdata = hit(4, a_weight, 20, -5, direction, a_x, a_y, a_health)
                                    a_x = hitdata[0]
                                    a_y = hitdata[1]
                                    a_health = hitdata[2]
                                    knockback_state = hitdata[3]
                                    is_hit = True
                    if direction == 'Right':
                        is_flipped_x = False
                        is_flipped_y = False
                        current_sprite = zap_attack_upper_frame_1
                    else:
                        is_flipped_x = True
                        is_flipped_y = False
                        current_sprite = zap_attack_upper_frame_1
            elif B_Pressed == True and cooldown == 0:
                cooldown = 6
                if direction == 'Right':
                    is_flipped_x = False
                    current_sprite = zap_attack_2
                    state = 'attack_2_right'
                    for i in range(16):
                        if x + i == a_x:
                            for j in range(16):
                                if y + j == a_y or y - j == a_y:
                                    is_hit = True
                else:
                    is_flipped_x = True
                    current_sprite = zap_attack_2
                    state = 'attack_2_left'
                    for i in range(16):
                        if x + i == a_x:
                            for j in range(16):
                                if y - j == a_y:
                                    is_hit = True
                if is_hit == True:
                    hitdata = hit(20, a_weight, 15, 5, direction, a_x, a_y, a_health)
                    a_x = hitdata[0]
                    a_y = hitdata[1]
                    a_health = hitdata[2]
                    knockback_state = hitdata[3]
            if is_hit == True and y > 20:
                current_sprite = zap_hit
                if direction == 'Right':
                    is_flipped_x = False
                elif direction == 'Left':
                    is_flipped_x = True
            if R_Pressed == True:
                x += speed
                direction = 'Right'
                state = 'walk_right'
            if L_Pressed == True:
                x -= speed
                direction = 'Left'
                state ='walk_left'
            if U_Pressed == True:
                state == 'jumping'
                if y == 20:
                    y -= jumpheight

        #Goggles Code       
        elif name == 'goggles':
            if direction == 'Right':
                is_flipped_x = False
                current_sprite = goggles_walk_sprite
                state = 'walk_right'
            elif direction == 'Left':
                is_flipped_x = True
                current_sprite = goggles_walk_sprite
                state = 'walk_left'
            if AU_Pressed == True and trident_data == None and cooldown == 0:
                cooldown = 20
                trident_data = [x, y, 'Up', 0, False]
            elif A_Pressed == True and cooldown == 0:
                cooldown = 4
                if direction == 'Right':
                    is_flipped_x = False
                    current_sprite = goggles_attack_1
                    state = 'attack_1_right'
                    for i in range(16):
                        if x + i == a_x:
                            for j in range(16):
                                if y + j == a_y:
                                    hitdata = hit(16, a_weight, 15, 10, direction, a_x, a_y, a_health)
                                    a_x = hitdata[0]
                                    a_y = hitdata[1]
                                    a_health = hitdata[2]
                                    knockback_state = hitdata[3]
                else:
                    is_flipped_x = True
                    current_sprite = goggles_attack_1
                    state = 'attack_1_left'
                    for i in range(16):
                        if x - i == a_x:
                            for j in range(16):
                                if y - j == a_y:
                                    hitdata = hit(16, a_weight, 15, 10, direction, a_x, a_y, a_health)
                                    a_x = hitdata[0]
                                    a_y = hitdata[1]
                                    a_health = hitdata[2]
                                    knockback_state = hitdata[3]
            elif B_Pressed == True:
                in_range = False
                if direction == 'Right':
                    is_flipped_x = False
                    current_sprite = goggles_attack_2
                    state = 'attack_2_right'
                    for i in range(32):
                        if x + i == a_x:
                            for j in range(16):
                                if y - j == a_y:
                                    in_range = True
                    if in_range == True:
                        a_x = x + 10
                                    
                        i = 0
                    for i in range(4):
                        thumby.display.blit(waves, x*i, y+10, 8, 8, 1, 0, 0)
                else:
                    is_flipped_x = True
                    current_sprite = goggles_attack_2
                    state = 'attack_2_left'
                    for i in range(32):
                        if x - i == a_x:
                            for j in range(16):
                                if y - j == a_y:
                                 in_range = True
                    if in_range == True:
                        a_x = x - 10
                    i = 0
                    for i in range(4):
                        thumby.display.blit(waves, x*-1*i, y+10, 8, 8, 1, 0, 0)
            if R_Pressed == True:
                x += speed
                direction = 'Right'
                state = 'walk_right'
            elif L_Pressed == True:
                x -= speed
                direction = 'Left'
                state ='walk_left'
            if U_Pressed == True:
                state == 'jumping'
                if y == 20:
                    y -= jumpheight
                
        #Apex Code
        elif name == 'apex':
            current_sprite = apex_walk
            if R_Pressed == True or L_Pressed == True:
                if state == None:
                    state = 'walk_1'
                    current_sprite = apex_walk_1
                elif state == 'walk_1':
                    state = 'walk_2'
                    current_sprite = apex_walk_2
                elif state == 'walk_2':
                    state = 'walk_3'
                    current_sprite = apex_walk_3
                elif state == 'walk_3':
                    state = 'walk_4'
                    current_sprite = apex_walk_4
                else:
                    state = 'walk_1'
                    current_sprite = apex_walk_1
            elif A_Pressed == True and cooldown == 0:
                cooldown = 20
                current_sprite = apex_attack_1
                thumby.display.blit(waves_2, x-3, y-5, 20, 20, 1, 0, 0)
                for i in range(24):
                        if x + i == a_x:
                            for j in range(16):
                                if y - j == a_y:
                                    a_x += 17 - weight
                                    a_y += 12 - weight
                                    a_health -= attack
                        elif x - i == a_x:
                             for j in range(16):
                                if y - j == a_y:
                                    a_x -= 17 - weight
                                    a_y += 12 - weight
                                    a_health -= attack
            if R_Pressed == True:
                x += speed
                direction = 'Right'
            elif L_Pressed == True:
                x -= speed
                direction = 'Left'
            if U_Pressed == True:
                state == 'jumping'
                if y == 20:
                    y -= jumpheight
           
        #Fang Code
        elif name == 'fang':
             current_sprite = fang_walk_1
             if direction == 'Left':
                 is_flipped_x = False
             else:
                 is_flipped_x = True
             if R_Pressed == True or L_Pressed == True:
                if state == None:
                    state = 'walk_1'
                    current_sprite = fang_walk_1
                elif state == 'walk_1':
                    state = None
                    current_sprite = fang_walk_2
             if state == 'releasing':
                 current_sprite = fang_attack_1
                 data[1] += 1
                 if direction == 'Right':
                     x += 4
                     is_flipped_x = True
                     for i in range(16):
                            if x + i == a_x:
                                for j in range(16):
                                    if y + j == a_y:
                                        hitdata = hit(int(data[0]), a_weight, data[0], 10, direction, a_x, a_y, a_health)
                                        a_x = hitdata[0]
                                        a_y = hitdata[1]
                                        a_health = hitdata[2]
                                        knockback_state = hitdata[3]
                                        break
                 elif direction == 'Left':
                     x -= 4
                     for i in range(16):
                            if x - i == a_x:
                                for j in range(16):
                                    if y - j == a_y:
                                        hitdata = hit(int(data[0]), a_weight, data[0], 10, direction, a_x, a_y, a_health)
                                        a_x = hitdata[0]
                                        a_y = hitdata[1]
                                        a_health = hitdata[2]
                                        knockback_state = hitdata[3]
                                        break
                 if data[1] >= data[0]:
                     data = None
                     state = None
                     
             elif A_Pressed == True and state != 'charging'  and state != 'releasing':
                 state = 'charging'
                 data = [0,0]
             elif A_Pressed == True and state == 'charging'   and state != 'releasing':
                 data[0] += 1
                 thumby.display.blit(fang_spark, x, y-5, 6, 6, 1, 0, 0)
             elif A_Pressed == False and state == 'charging':
                 state = 'releasing'
                 data[1] = 0
             elif B_Pressed == True and cooldown == 0:
                 current_sprite = fang_attack_2
                 cooldown = 6
                 if direction == 'Right':
                     x += 4
                     is_flipped_x = True
                     for i in range(16):
                            if x + i == a_x or x - i == a_x or x == a_x:
                                for j in range(16):
                                    if y + j == a_y or y - j == a_x or y == a_y:
                                        hitdata = hit(10, a_weight, 5, 5, direction, a_x, a_y, a_health)
                                        a_x = hitdata[0]
                                        a_y = hitdata[1]
                                        a_health = hitdata[2]
                                        knockback_state = hitdata[3]
                                        break
             elif R_Pressed == True:
                x += speed
                is_flipped_x = True
                direction = 'Right'
             elif L_Pressed == True:
                is_flipped_x = False
                x -= speed
                direction = 'Left'
                 
        #Tempestas Code
        elif name == 'tempestas':
            current_sprite = tempestas_walk_1
            if state == 'cloud':
                    thumby.display.blit(cloud, data, 10, 10, 6, 1, 0, 0)
                    if R_Pressed == True:
                        data += 5
                    elif L_Pressed == True:
                        data -= 5
                    elif B_Pressed == True:
                        i = 0
                        for i in range(6):
                            thumby.display.blit(lightning, data, i*5, 4, 8, 1, 0, 0)
                            if data == a_x + i or data == a_x or data == a_x - i:
                               hitdata = hit(35, a_weight, 25, 10, direction, a_x, a_y, a_health)
                               a_x = hitdata[0]
                               a_y = hitdata[1]
                               a_health = hitdata[2]
                               knockback_state = hitdata[3]
                               break
                        state = None
                        data = None
                        
            elif R_Pressed == True or L_Pressed == True:
                if state == None:
                    state = 'walk_1'
                    current_sprite = tempestas_walk_1
                elif state == 'walk_1':
                    state = 'walk_2'
                    current_sprite = tempestas_walk_2
                elif state == 'walk_2':
                    state = 'walk_3'
                    current_sprite = tempestas_walk_3
                else:
                    state = 'walk_1'
                    current_sprite = tempestas_walk_1
            elif B_Pressed == True and cooldown == 0:
                cooldown = 30
                state = 'cloud'
                data = x
            if R_Pressed == True and state != 'cloud':
                x += speed
                is_flipped_x = True
                direction = 'Right'
            elif L_Pressed == True and state != 'cloud':
                x -= speed
                direction = 'Left'
            elif U_Pressed == True and state != 'cloud':
                state == 'jumping'
                if y == 20:
                    y -= jumpheight
            elif A_Pressed == True and state != 'cloud' and state != 'spark' and cooldown == 0:
                    cooldown = 16
                    state = 'spark'
                    data = [x+10,y,0,direction]
            elif state == 'spark' and data != None:
                thumby.display.blit(spark, data[0], y, 6, 6, 1, 0, 0)
                if data[2] >= 10:
                    state = None
                else:
                    data[2] += 1
                    if data[3] == 'Right':
                        data[0] += 4
                    elif data[3] == 'Left':
                        data[0] -= 4
                for i in range(6):
                    for j in range(6):
                        if data[0] == a_x + i or data[0] == a_x or data[0] == a_x - i:
                            if data[1] == a_y + j or data[1] == a_y or data[1] == a_y- j:
                                hitdata = hit(7, a_weight, 5, 5, direction, a_x, a_y, a_health)
                                a_x = hitdata[0]
                                a_y = hitdata[1]
                                a_health = hitdata[2]
                                knockback_state = hitdata[3]
                                break
                                break
            if direction == 'Right':
                is_flipped_x = True
                
            #Delta Code
            elif name == 'Delta':
                current_sprite = delta_walk
                    
        y += weight
        
        if config[3] == 'Warp':
            if x > 70:
                x = 0
            if 0 > x:
                x = 70
        elif config[3] == 'Block':
            if x > 70:
                x = 70
            if 0 > x:
                x = 0
            if a_x > 70:
                knockback_state = 0
            if 0 > a_x:
                knockback_state = 0
        elif config[3] == 'Damage':
            if 0 > x:
                health -= 20
            if 70 > x:
                health -= 20
        if y > 20: 
            y = 20
        elif a_y > 20: 
            a_y = 20
        if y > 150:
            health = 0
        elif a_y > 150:
            a_health = 0
        thumby.display.blit(current_sprite, x, y, 16, 16, 1, is_flipped_x, is_flipped_y)         
        #end game code
        if health <= 0 and player_type == 'ai':
            match_screen('win')
        elif health <= 0 and player_type == 'human':
            match_screen('lose')
        elif a_health <= 0 and player_type == 'ai':
            match_screen('lose')
        elif a_health <= 0 and player_type == 'human':
            match_screen('win')
            
        return [state, x, y, direction, a_x, a_y, health,  a_health, knockback_state, cooldown, data]
    battling = True 
    state = None
    ai_state = None
    p_x = 30
    p_y = 20
    p_direction = 'Right'
    ai_x = 60
    ai_y = 20
    ai_direction = 'Right'
    knockback_state = 0
    ai_knockback_state = 0
    
    if char == 'goggles':
        p_jumpheight, p_attack, p_health, p_speed, p_weight = 17, 7, 240, 3, 4
    if char == 'zap':
        p_jumpheight, p_attack, p_health, p_speed, p_weight = 20, 5, 170, 4, 2
    if char == 'apex':
        p_jumpheight, p_attack, p_health, p_speed, p_weight = 15, 9, 200, 2, 6
    if char == 'tempestas':
        p_jumpheight, p_attack, p_health, p_speed, p_weight = 18, 10, 200, 5, 4
    if char == 'fang':
        p_jumpheight, p_attack, p_health, p_speed, p_weight = 15, 12, 250, 3, 4
    if enemy_char == 'goggles':
        a_jumpheight, a_attack, a_health, a_speed, a_weight = 17, 7, 240, 3, 4
    if enemy_char == 'zap':
        a_jumpheight, a_attack, a_health, a_speed, a_weight = 20, 5, 170, 4, 2
    if enemy_char == 'apex':
        a_jumpheight, a_attack, a_health, a_speed, a_weight = 15, 9, 200, 2, 6
    if enemy_char == 'tempestas':
        a_jumpheight, a_attack, a_health, a_speed, a_weight = 18, 10, 200, 5, 4
    if enemy_char == 'fang':
        a_jumpheight, a_attack, a_health, a_speed, a_weight = 15, 12, 250, 3, 4
        
    cooldown = 0
    cooldown = 0
    ai_cooldown = 0
    data = None
    ai_data = None
    
    while battling == True:
        thumby.display.fill(1)
        thumby.display.drawRectangle(0, 36, 100, 2, 0)
        p_health_text = str('You:'  + str(p_health))
        a_health_text = str('Opponent:'  + str(a_health))
        thumby.display.drawText(str(p_health_text), 0, 0, 0)
        thumby.display.drawText(str(a_health_text), 0, 8, 0)
        c_list = None
        c_list = character_move(char, p_jumpheight, p_attack, p_health, p_speed, p_weight, 'human', state, p_x, p_y, p_direction, ai_x, ai_y, a_jumpheight, a_attack, a_health, a_speed, a_weight, cooldown, knockback_state, data, config)
        cooldown = c_list[9]
        if cooldown > 0:
            cooldown -= 1
        state = c_list[0]
        p_x = c_list[1]
        p_y = c_list[2]
        p_direction = c_list[3]
        ai_x = c_list[4]
        ai_y = c_list[5]
        knockback_state = c_list[8]
        data = c_list[10]
        a_health = c_list[7]
        ai_mode = config[1]
        if ai_mode == 0:
            ai_mode = 'ai'
        else:
            ai_mode = 'static'
        ai_c_list = character_move(enemy_char, a_jumpheight, a_attack, a_health, a_speed, a_weight, ai_mode, ai_state, ai_x, ai_y, ai_direction, p_x, p_y, p_jumpheight, p_attack, p_health, p_speed, p_weight, ai_cooldown, ai_knockback_state, ai_data, config)
        ai_cooldown = ai_c_list[9]
 
        if ai_cooldown > 0:
            ai_cooldown -= 1
        ai_state = ai_c_list[0]
        p_x = ai_c_list[4]
        p_y = ai_c_list[5]
        ai_direction = ai_c_list[3]
        ai_x = ai_c_list[1]
        ai_y = ai_c_list[2]
        ai_knockback_state = ai_c_list[8]
        p_health = ai_c_list[7]
        ai_data = ai_c_list[10]
        time.sleep(0.1*config[2])
        thumby.display.update()
        
        
def main_menu():
    
     def config_menu():
         time.sleep(0.1)
         #Default Config on startup, change these values here if you wish to keep them upon powering down the thumby.
         ai_stupidity = 0
         '''AI Mode, 0 for Active, 1 for Static. Active ai moves and attempts to mimic a player, 
         Static AI does not move or attack,but retains the properties of a character'''
         ai_mode = 0
         # The Higher the Value, the slower the game
         game_pace = 1
         #Wall Behaviors: Block, Warp, Damage, also change wall_int to the 0 for Block, 1 for Warp, and 2 For Damage
         
         wall_behavior = 'Block'
         wall_int = 0
         # BITMAP: width: 12, height: 12
         b_button = bytearray([15,247,251,253,14,174,174,94,253,251,247,15,
           15,14,13,11,6,6,6,7,11,13,14,15])
         slider = bytearray([127,99,93,0,93,99,127])
         configmenu = True
         menu_arrow = bytearray([31,31,0,17,27])
         menu = True
         arrow_location = 0
         while configmenu == True:
             if thumby.buttonD.pressed() and arrow_location < 2:
                 arrow_location += 1
             elif thumby.buttonU.pressed() and arrow_location > 0:
                 arrow_location -= 1
             thumby.display.fill(1)
             thumby.display.drawText('AI Config', 0, 0, 0)
             thumby.display.drawText('Game Config', 0, 8, 0)
             thumby.display.drawText('Back', 0, 16, 0)
             if arrow_location == 0:
                 thumby.display.blit(menu_arrow, 15, 0, 5, 5, 1, 0, 0)
             elif arrow_location == 1:
                thumby.display.blit(menu_arrow, 15, 8, 5, 5, 1, 0, 0)
             elif arrow_location == 2:
                thumby.display.blit(menu_arrow, 15, 16, 5, 5, 1, 0, 0)
             time.sleep(0.1)
             if thumby.buttonA.pressed() and arrow_location == 0:
                 ai_config_menu = True
                 while ai_config_menu == True:
                     if thumby.buttonD.pressed() and arrow_location == 0:
                        arrow_location += 1
                     elif thumby.buttonU.pressed() and arrow_location == 1:
                        arrow_location -= 1
                     elif thumby.buttonB.pressed():
                         ai_config_menu = False
                     if arrow_location == 0:
                         thumby.display.blit(menu_arrow, 0, 0, 5, 5, 1, 0, 0)
                         if thumby.buttonR.pressed() and ai_stupidity < 20:
                            ai_stupidity += 1
                         elif thumby.buttonL.pressed() and ai_stupidity > 0:
                            ai_stupidity -= 1
                     elif arrow_location == 1:
                         thumby.display.blit(menu_arrow, 0, 25, 5, 5, 1, 0, 0)
                         if thumby.buttonR.pressed() and ai_mode < 1:
                            ai_mode += 1
                         elif thumby.buttonL.pressed() and ai_mode > 0:
                            ai_mode -= 1
                     thumby.display.drawText('AI Stupidity:', 0, 0, 0)
                     thumby.display.drawText('AI Mode:', 0, 20, 0)
                     thumby.display.drawRectangle(5, 10, 25, 2, 0)
                     thumby.display.drawRectangle(5, 30, 7, 2, 0)
                     thumby.display.blit(slider, ai_stupidity+5, 10, 7, 7, 1, 0, 0)
                     thumby.display.blit(slider, ai_mode+5, 30, 7, 7, 1, 0, 0)
                     thumby.display.drawText(str(ai_stupidity), ai_stupidity, 15, 0)
                     if ai_mode == 0:
                         ai_mode_text = str('Active ' + str(ai_mode))
                     if ai_mode == 1:
                         ai_mode_text = str('Static ' + str(ai_mode))
                     thumby.display.drawText(str(ai_mode_text), ai_mode*10, 35, 0)
                     time.sleep(0.1)
                     thumby.display.update()
                     thumby.display.fill(1)
             elif thumby.buttonA.pressed() and arrow_location == 1:
                 gameplay_config_menu = True
                 while gameplay_config_menu == True:
                     thumby.display.drawText('Game Pace:', 5, 0, 0)
                     thumby.display.drawRectangle(1, 15, 10, 2, 0)
                     thumby.display.blit(slider, game_pace, 15, 7, 7, 1, 0, 0)
                     thumby.display.drawText('Wall Behavior:', 5, 20, 0)
                     thumby.display.drawRectangle(1, 30, 10, 2, 0)
                     thumby.display.blit(slider, wall_int*3, 30, 7, 7, 1, 0, 0)
                     thumby.display.drawText(str(wall_int),wall_int*3, 35, 1)
                     if thumby.buttonD.pressed() and arrow_location == 0:
                        arrow_location += 1
                     elif thumby.buttonU.pressed() and arrow_location == 1:
                        arrow_location -= 1
                     if arrow_location == 0:
                         thumby.display.blit(menu_arrow, 0, 15, 5, 5, 1, 0, 0)
                         if thumby.buttonR.pressed() and game_pace < 10:
                            game_pace += 1
                         elif thumby.buttonL.pressed() and game_pace > 1:
                            game_pace -= 1
                     elif arrow_location == 1:
                         thumby.display.blit(menu_arrow, 0, 30, 5, 5, 1, 0, 0)
                         if thumby.buttonR.pressed() and wall_int < 2:
                            wall_int += 1
                         elif thumby.buttonL.pressed() and wall_int > 0:
                            wall_int -= 1
                     if wall_int == 0:
                         wall_behavior = 'Block'
                     elif wall_int == 1:
                         wall_behavior = 'Warp'
                     elif wall_int == 2:
                         wall_behavior = 'Damage'
                     if thumby.buttonB.pressed():
                             gameplay_config_menu = False
                     time.sleep(0.1)
                     thumby.display.update()
                     thumby.display.fill(1)
                     
             elif thumby.buttonA.pressed() and arrow_location == 2 or thumby.buttonB.pressed():
                 configmenu = False
                 menu = True
                 return [ai_stupidity, ai_mode, game_pace, wall_behavior]
             thumby.display.update()
             thumby.display.fill(1)
             
     menu_arrow = bytearray([31,31,0,17,27])
     menu = True
     arrow_location = 0
     config = None
     while menu == True:
         
         if thumby.buttonD.pressed() and arrow_location == 0:
             arrow_location += 1
         elif thumby.buttonU.pressed() and arrow_location == 1:
             arrow_location -= 1
         thumby.display.fill(1)
         thumby.display.drawText('Thumby', 0, 0, 0)
         thumby.display.drawText('Smash', 0, 8, 0)
         if arrow_location == 0:
             thumby.display.blit(menu_arrow, 15, 20, 5, 5, 1, 0, 0)
         elif arrow_location == 1:
            thumby.display.blit(menu_arrow, 15, 30, 5, 5, 1, 0, 0)
         if thumby.buttonA.pressed():
             if arrow_location == 0:
                 menu = False
             elif arrow_location == 1:
                 config = config_menu()
         thumby.display.drawText('PLAY', 20, 20, 0)
         thumby.display.drawText('CONFIG', 20, 30, 0)
         time.sleep(0.1)
         thumby.display.update()
         thumby.display.fill(1)
     if config == None:
                '''Edit the line below for config defaults when not using the config menu. 
                Refer to lines 550-560 for config menu defaults and for help with syntax'''
                config = [0, 0, 1, 'Block']    
     return config
         
def character_select(config):
    selected_char = None
    select_screen = True
    selected = 0
    offset = 0
    while select_screen == True:
        # BITMAP: width: 16, height: 16
        goggles_icon = bytearray([243,245,246,6,146,108,110,158,158,108,98,22,246,245,243,255,
                255,255,255,255,254,253,251,251,251,253,254,255,255,255,255,255])
        goggles_icon_selected  = bytearray([12,10,9,249,109,147,145,97,97,147,157,233,9,10,12,0,
               0,0,0,0,1,2,4,4,4,2,1,0,0,0,0,0])
        # BITMAP: width: 16, height: 16
        zap_icon = bytearray([251,55,207,111,183,119,247,247,247,119,183,111,215,55,251,251,
                255,240,239,223,190,63,95,7,95,63,190,223,239,240,255,255])
        
        # BITMAP: width: 16, height: 16
        zap_icon_selected = bytearray([4,200,48,144,72,136,8,8,8,136,72,144,40,200,4,4,
                0,15,16,32,65,192,160,248,160,192,65,32,16,15,0,0])
        apex_icon = bytearray([63,222,237,51,219,109,245,245,245,245,109,219,51,237,222,63,
           120,183,207,216,183,108,95,95,95,95,108,183,216,207,183,120])
        # BITMAP: width: 16, height: 16
        apex_icon_selected = bytearray([192,33,18,204,36,146,10,10,10,10,146,36,204,18,33,192,
           135,72,48,39,72,147,160,160,160,160,147,72,39,48,72,135])
        # BITMAP: width: 16, height: 16
        blobbo_icon = bytearray([55,255,255,251,59,219,235,235,235,235,219,59,251,251,255,255,
           255,255,255,224,223,189,183,183,183,183,189,223,224,255,255,255])
        # BITMAP: width: 16, height: 16
        blobbo_icon_selected = bytearray([0,0,0,4,196,36,20,20,20,20,36,196,4,4,0,0,
           0,0,0,31,32,66,72,72,72,72,66,32,31,0,0,0])
        # BITMAP: width: 16, height: 16
        fang_icon = bytearray([255,7,251,253,238,198,238,254,254,238,198,238,253,251,7,255,
           255,254,128,119,79,47,77,111,111,77,47,79,119,128,254,255])
        # BITMAP: width: 16, height: 16
        fang_icon_selected = bytearray([0,248,4,2,17,57,17,1,1,17,57,17,2,4,248,0,
           0,1,127,136,176,208,178,144,144,178,208,176,136,127,1,0])
        thumby.display.fill(1)
        # BITMAP: width: 16, height: 16
        tempestas_icon = bytearray([255,255,63,223,207,71,199,199,199,199,71,207,223,63,255,255,
           255,255,192,191,116,91,95,95,95,95,91,116,191,192,255,255])
        # BITMAP: width: 16, height: 16
        tempestas_icon_selected = bytearray([0,0,192,32,48,184,56,56,56,56,184,48,32,192,0,0,
           0,0,63,64,139,164,160,160,160,160,164,139,64,63,0,0])
        delta_icon = bytearray([255,255,249,6,207,199,198,6,6,198,199,207,6,249,255,255,
           255,63,63,192,192,192,184,184,184,184,192,192,192,63,63,255])
       # BITMAP: width: 16, height: 16
        delta_icon_selected = bytearray([0,0,6,249,48,56,57,249,249,57,56,48,249,6,0,0,
           0,224,224,63,63,63,103,103,103,103,63,63,63,192,192,0])
        question_mark = bytearray([255,255,255,223,239,247,251,251,251,251,251,251,247,111,159,255,
           255,255,255,255,255,255,255,63,35,59,253,253,254,255,255,255])
        # BITMAP: width: 16, height: 16
        question_mark_selected = bytearray([0,0,0,32,16,8,4,4,4,4,4,4,8,144,96,0,
           0,0,0,0,0,0,0,192,220,196,2,2,1,0,0,0])
        chars = [['goggles', goggles_icon, goggles_icon_selected], ['zap', zap_icon, zap_icon_selected], ['apex', apex_icon, apex_icon_selected], ['tempestas', tempestas_icon, tempestas_icon_selected], ['fang', fang_icon, fang_icon_selected], ['random', question_mark, question_mark_selected]]
        for i in range(len(chars)):
            thumby.display.blit(box, (16*i) + 5, 0, 16, 16, 1, 0, 0)
            if selected > 3:
                offset = selected - 2
            elif selected < 3:
                offset = 0
            if i != selected:
                thumby.display.blit(chars[i][1], (16*int(i-offset)) + 5, 0, 16, 16, 1, 0, 0)
            else:
                thumby.display.blit(chars[i][2], (16*int(i-offset)) + 5, 0, 16, 16, 1, 0, 0)
        if thumby.buttonR.pressed() and selected < int(len(chars)-1) :
            selected += 1
        elif thumby.buttonL.pressed() and selected > 0:
            selected -= 1
        elif thumby.buttonB.pressed():
            config = main_menu()
        elif thumby.buttonA.pressed():
            selected_char = chars[selected][0]
            while selected_char == 'random':
                random.seed(time.ticks_us())
                selected_char = random.choice(chars)
                selected_char = selected_char[0]
            random.seed(time.ticks_us())
            enemy_char_data = random.choice(chars)
            enemy_char = enemy_char_data[0]
            while enemy_char == 'random':
                enemy_char_data = random.choice(chars)
                enemy_char = enemy_char_data[0]
            while enemy_char == selected_char:
                enemy_char_data = random.choice(chars)
                enemy_char = enemy_char_data[0]
            thumby.display.fill(1)
            select_screen = False
            for i in range(3):
                thumby.display.fill(1)
                thumby.display.drawText(str(3-i), 30, 15, 0)
                thumby.display.update()
                time.sleep(1)
            singleplayer_battle(selected_char, enemy_char, config)
        thumby.display.drawText(chars[selected][0], 10, 25, 0)
        time.sleep(0.1)
        thumby.display.update()
        i = 0
running = True
while running == True:
    config = main_menu()
    character_select(config)
    time.sleep(1)
