import time
import thumby
import math
import random

thumby.display.setFPS(30)
map_size = ((0,0),(72,40))
player_shots = []
boss_shots = []
enemies = []
bosses = []
stars = []
explosions = []
kills = 0
boss_kills = 0
boss_time = 0
f = 0
end_tick = -1

class player():
    def __init__(self):
        # BITMAP: width: 8, height: 7
        bm = bytearray([73,119,119,93,73,93,28,8])
        self.sprite = thumby.Sprite(8,7,bm)
        self.sprite.x = 10
        self.sprite.y = 17
        self.cooldown = 0
        self.lives = 3
        self.flicker = 0
        
    def input(self):
        if self.cooldown > 0:
            self.cooldown -= 1
        if thumby.buttonL.pressed() and self.sprite.x > 0:
            self.sprite.x -= 1
        if thumby.buttonR.pressed() and self.sprite.x < 64:
            self.sprite.x += 1
        if thumby.buttonU.pressed() and self.sprite.y > 0:
            self.sprite.y -= 1
        if thumby.buttonD.pressed() and self.sprite.y < 33:
            self.sprite.y += 1
        if thumby.buttonA.pressed() and self.cooldown == 0:
            player_shots.append(fire(self.sprite.x+8,self.sprite.y+3))
            self.cooldown += 12
            

class fire():
    def __init__(self,x,y):
    # BITMAP: width: 2, height: 1
        self.sprite = thumby.Sprite(2,1,bytearray([1,1]))
        self.sprite.x = x
        self.sprite.y = y
        
            

class enemy():
    def __init__(self, etype, x, y):
        enemy1bitmap = bytearray([12,30,63,45,12,30]) # BITMAP: width: 6, height: 6
        enemy2bitmap = bytearray([33,45,63,12,30,63])# BITMAP: width: 6, height: 6
        enemy3bitmap = bytearray([8,62,127,127,93,73,107])# BITMAP: width: 7, height: 7
        enemy4bitmap = bytearray([42,28,54,99,119,85,93])# BITMAP: width: 7, height: 7
        e_array = [enemy1bitmap,enemy2bitmap,enemy3bitmap,enemy4bitmap]
        xy = 6 if etype < 2 else 7
        self.sprite = thumby.Sprite(xy,xy,e_array[etype])
        self.sprite.x = x
        self.sprite.y = y
        self.xy = xy


class boss():
    def __init__(self, etype, x, y):
        boss1bitmap  = bytearray([144,153,249,157,15,255,253,8,0,9,9,11,15,15,11,1])# BITMAP: width: 8, height: 12
        boss2bitmap  =  bytearray([145,153,149,247,255,109,104,96,8,9,10,14,15,11,1,0]) # BITMAP: width: 8, height: 12
        bm_choice = boss1bitmap if etype==1 else boss2bitmap
        self.life = 20
        self.sprite = thumby.Sprite(8,12,bm_choice)
        self.sprite.x = x
        self.sprite.y = y
        self.direc = 0
        
    def fire_loc(self):
        gun = random.randint(0,3)
        y_opt = [0,4,7,11]
        x = self.sprite.x -1
        y = self.sprite.y + y_opt[gun]
        return x,y
        
class star():
    def __init__(self,y):
        self.sprite = thumby.Sprite(1,1,bytearray([1]))
        self.sprite.x = 72
        self.sprite.y = y

class explosion():
    def __init__(self,x,y):
        # BITMAP: width: 8, height: 8
        e1 = bytearray([0,0,0,24,24,0,0,0])
        e2 = bytearray([0,24,36,90,90,36,24,0])
        e3 = bytearray([36,90,165,90,90,165,90,36])
        e4 = bytearray([36,90,165,66,66,165,90,36])
        e5 = bytearray([36,66,129,0,0,129,66,36])
        self.life = 15
        self.sprite = thumby.Sprite(8,8,e1+e2+e3+e4+e5,key=0)
        self.sprite.x = x
        self.sprite.y = y

    def update(self):
        self.life = self.life - 1
        self.sprite.setFrame(5-(self.life+3)//3)


def overlap_box(a,b): # a = ((x1,y1),(x2,y2))
    if a[0][0] > b[1][0] or a[1][0] < b[0][0] or a[0][1] > b[1][1] or a[1][1] < b[0][1]:
        return False
    else: return True
    
def update_player_shots(player_shots):
    cont = []
    for i in range(len(player_shots)):
        current = player_shots.pop(0)
        current.sprite.x += 1
        if current.sprite.x < 73:
            cont.append(current)
            thumby.display.drawSprite(current.sprite)
    return cont
    
def update_boss_shots(boss_shots):
    cont = []
    for i in range(len(boss_shots)):
        current = boss_shots.pop(0)
        current.sprite.x -= 1
        if current.sprite.x > -2:
            cont.append(current)
            thumby.display.drawSprite(current.sprite)
    return cont
    
def update_stars(stars,create):
    # Move existing stars left
    out_stars = []
    for s in stars:
        s.sprite.x -= 1
        if s.sprite.x > -1:
            out_stars.append(s)
    # Generate new stars
    new = random.randint(-10,1)
    if new > 0 and create == 1:
        for i in range(new):
            out_stars.append(star(random.randint(0,39)))
    # Display stars
    for s in stars:
        thumby.display.drawSprite(s.sprite)
    # Return stars array
    return out_stars
    
def enemy_block():
    es = []
    x = random.randint(1,3)
    y = random.randint(1,3)
    etype = random.randint(0,3)
    start_y = random.randint(1,9)
    prior_y = start_y-1 if start_y>5 else start_y+1
    for i in range(x):
        for j in range(y):
            xs = 73 + i * 10
            ys = start_y + j * 10
            e = enemy(etype, xs, ys)
            es.append(e)
    y_range = [0,(4-y)*10+3]
    return([prior_y,start_y], es, y_range)
    
def update_enemy_block(enemies,tock):
    es = enemies[1]
    ys = enemies[0]
    yr = enemies[2]
    ydelta = 0
    if tock%2 == 0:
        if ys[-1] > yr[0] and ys[-1] < yr[1]:
            if random.random() < .97:
                ydelta = ys[-1] - ys[-2]
            else:
                ydelta = ys[-2] - ys[-1]
        else:
            ydelta = ys[-2] - ys[-1]
        for e in es:
            e.sprite.y += ydelta
            e.sprite.x -=1
        ys.append(ys[-1]+ydelta)
    return(ys,es)
    
def strip_enemies(en):
    es = en[1]
    delete = True
    for e in es:
        if e.sprite.x > -8:
            delete = False
    return delete

def update_enemies(enemies, create):
    # Create enemies
    if len(enemies) == 0 and create == 1:
        # add boss logic (?)
        if random.random() < 0.05:
            ys,en, yr = enemy_block()
            enemies.append([ys,en, yr])
    else: # Update enemies
        for i in range(len(enemies)):
            yr = enemies[i][2]
            ys,en = update_enemy_block(enemies[i],f)
            enemies[i] = [ys,en,yr]
            for e in en:
                thumby.display.drawSprite(e.sprite)
    # Delete enemies killed
    enemies_temp = []
    for i in range(len(enemies)):
        if strip_enemies(enemies[i]) == False:
            enemies_temp.append(enemies[i])
    enemies = enemies_temp
    return enemies
    
def destroy_enemies(player_shots, enemies):
    shots_temp = []
    exps = []
    l1 = 0
    for i in enemies:
        l1 += len(i[1])
    for shot in player_shots:
        delete_shot = False
        a = ((shot.sprite.x, shot.sprite.y), (shot.sprite.x+1, shot.sprite.y))
        for en_idx in range(len(enemies)):
            es_temp = []
            es = enemies[en_idx][1]
            for e in es:
                b = ((e.sprite.x, e.sprite.y), (e.sprite.x+e.xy-1, e.sprite.y+e.xy-1))
                if overlap_box(a,b): # a = ((x1,y1),(x2,y2))
                    ex = explosion(e.sprite.x, e.sprite.y)
                    exps.append(ex)
                    delete_shot = True
                else:
                    es_temp.append(e)
            enemies[en_idx][1] = es_temp
        if delete_shot == False:
            shots_temp.append(shot)
    player_shots = shots_temp
    l2 = 0
    for i in enemies:
        l2 += len(i[1])
    kills = l1-l2
    return player_shots, enemies, exps, kills

def update_explosions(exps):
    keep_exps = []
    for e in exps:
        e.update()
        thumby.display.drawSprite(e.sprite)
        if e.life > 0:
            keep_exps.append(e)
    return keep_exps


def boss_update(bosses, player_shots, exps, boss_shots, f):
    boss_out = []
    b = bosses[0]
    # Move boss
    if b.sprite.x > 60:
        b.sprite.x -= 0.5
    elif f%2==0:
        if b.direc == 0:
            if b.sprite.y >0:
                b.sprite.y -= 1
            else: b.direc = 1
        else:
            if b.sprite.y < 28:
                b.sprite.y += 1
            else: b.direc = 0
    if b.life > 0:
        boss_out.append(b)
    # Check player attacks
    bxy = ((b.sprite.x, b.sprite.y), (b.sprite.x+7,b.sprite.y+11))
    shots_temp = []
    for shot in player_shots:
        delete_shot = False
        a = ((shot.sprite.x, shot.sprite.y), (shot.sprite.x+1, shot.sprite.y))
        if overlap_box(a,bxy):
            ex = explosion(shot.sprite.x-2, shot.sprite.y-3)
            exps.append(ex)
            b.life -= 1
            delete_shot = True
        if delete_shot == False:
            shots_temp.append(shot)
    # Create boss attacks
    if f%20 == 0 and b.life > 0 and b.sprite.x < 61:
        x,y = b.fire_loc()
        boss_shots.append(fire(x,y))
    return boss_out, shots_temp, exps, boss_shots


def draw_boss_health(bosses):
    b = bosses[0]
    max_life = 20
    current_life = b.life
    x = 70
    ymin = int(39-39*(current_life/max_life))
    thumby.display.drawLine(x, ymin, x, 39, 1)
    thumby.display.drawLine(x+1, ymin, x+1, 39, 1)
    

def draw_life_sprites(p1):
    l = p1.lives
    for i in range(l):
        life_icon = thumby.Sprite(3,3,bytearray([2,7,2]), 1, 1+4*i)
        thumby.display.drawSprite(life_icon)
    

def check_player_death(p1, all_en_sprites):
    hit = False
    a = ((p1.sprite.x,p1.sprite.y),(p1.sprite.x+p1.sprite.width-1,p1.sprite.y+p1.sprite.height-1))
    for b_sprite in all_en_sprites:
        b = ((b_sprite.sprite.x,b_sprite.sprite.y),\
                (b_sprite.sprite.x+b_sprite.sprite.height-1,\
                b_sprite.sprite.y+b_sprite.sprite.height-1))
        d = overlap_box(a,b)
        if d == True:
            hit = True
    return(hit)
    

def update_player(p1, bosses, enemies, boss_shots, exps):
    if p1.lives > 0:
        all_enemy_sprites = []
        if len(bosses) > 0:
            all_enemy_sprites += bosses
        if len(enemies) > 0:
            all_enemy_sprites += enemies[0][1]
        if len(boss_shots) > 0:
            all_enemy_sprites += boss_shots
        hit = check_player_death(p1, all_enemy_sprites)
    if hit and p1.flicker == 0:
        p1.lives -= 1
        if p1.lives > 0:
            p1.flicker += 60
    if p1.flicker > 0 and p1.lives > 0:
        if p1.flicker % 2 == 0:
            thumby.display.drawSprite(p1.sprite)
        p1.flicker -= 1
    elif p1.flicker == 0 and p1.lives > 0: 
        thumby.display.drawSprite(p1.sprite)
    elif p1.lives == 0:
        e = explosion(p1.sprite.x, p1.sprite.y)
        exps.append(e)
        
    draw_life_sprites(p1)
    return p1,exps
    

p1 = player()

thumby.display.fill(0) # Fill canvas to black
thumby.display.drawText('Micro', 6, 2, 1)
thumby.display.drawText('Gradient', 18, 10, 1)
thumby.display.drawLine(0, 19, 72, 19, 1)
# BITMAP: width: 72, height: 20
sbm = bytearray([0,0,0,0,0,0,0,0,0,0,112,8,8,112,8,120,0,122,0,48,72,72,0,120,\
                 8,0,48,72,72,48,0,48,72,72,240,0,120,8,0,104,104,112,0,56,72,\
                 126,0,122,0,48,88,88,0,112,8,8,112,0,8,126,72,0,0,0,0,0,0,0,0,\
                 0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,128,128,0,192,32,32,\
                 192,0,232,0,32,248,32,0,249,33,32,192,0,224,0,0,224,0,248,32,\
                 224,0,128,128,0,232,0,192,32,32,192,0,0,0,0,0,0,0,0,0,0,0,0,0,\
                 0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,1,0,0,5,5,3,0,1,\
                 0,0,1,1,0,1,0,0,1,0,0,1,1,1,0,1,1,0,0,1,1,0,1,0,0,1,1,0,0,0,0,\
                 0,0,0,0,0,0,0,0,0,0,0,0,0,0])
thumby.display.drawSprite(thumby.Sprite(72,20,sbm,0,20))
thumby.display.update()
time.sleep(1.5)


while True:
    paused = False
    if thumby.buttonB.pressed():
        paused = True
        while paused:
            if thumby.buttonA.pressed():
                paused = False
            thumby.display.fill(0)
            thumby.display.drawText('- Paused -', 6, 17, 1)
            thumby.display.update()
            
    
    f += 1
    if f == 100:
        f = 0
    thumby.display.fill(0) # Fill canvas to black
    p1.input()
    
    #print(kills, (kills+1)%10)
    
    if kills//100 > boss_kills:
        boss_time = 1
    if boss_time == 0:
        enemies = update_enemies(enemies, 1)
        player_shots = update_player_shots(player_shots)
        player_shots, enemies, exps, k = destroy_enemies(player_shots, enemies)
        explosions = explosions + exps
        kills += k
        explosions = update_explosions(explosions)
        stars = update_stars(stars,1)
        boss_shots = update_boss_shots(boss_shots)
        
    elif boss_time == 1:
        enemies = update_enemies(enemies, 0)
        player_shots = update_player_shots(player_shots)
        player_shots, enemies, exps, k = destroy_enemies(player_shots, enemies)
        explosions = explosions + exps
        kills += k
        explosions = update_explosions(explosions)
        stars = update_stars(stars,0)
        
        if len(bosses) == 0:
            bosses.append(boss(random.randint(1,2),120,13))
        elif len(bosses) == 1:
            thumby.display.drawSprite(bosses[0].sprite)
            draw_boss_health(bosses)
            bosses, player_shots, explosions, boss_shots = \
                    boss_update(bosses,player_shots, explosions, boss_shots, f)
        if len(bosses) == 0:
            boss_time = 0
            boss_kills += 1
        boss_shots = update_boss_shots(boss_shots)

    
    # Game over screen

    if p1.lives > 0:
        p1,explosions = update_player(p1, bosses, enemies, boss_shots, explosions)
    elif end_tick == -1 and p1.lives == 0:
        end_tick = f
    elif p1.lives ==0:
        if (end_tick + 30) < 100:
            end_game_tick = end_tick + 30  
        else: end_game_tick = end_tick -70
        if f == end_game_tick:
            exit = False
            while exit == False:
                if thumby.buttonA.pressed():
                    exit = True
                    p1 = player()
                    player_shots = []
                    boss_shots = []
                    enemies = []
                    bosses = []
                    stars = []
                    explosions = []
                    kills = 0
                    boss_kills = 0
                    boss_time = 0
                    f = 0
                    end_tick = -1
                thumby.display.fill(0) # Fill canvas to black
                thumby.display.drawText('Game Over!!!', 1, 1, 1)
                thumby.display.drawLine(0, 11, 72, 11, 1)
                thumby.display.drawText('Kills: '+str(kills), 1, 14, 1)
                thumby.display.drawText('Bosses: '+str(boss_kills), 1, 23, 1)
                thumby.display.drawText('New Game:"A"', 1, 32, 1)
                thumby.display.update()
    

    thumby.display.update()
    
    