import time
import thumby
import math
import random

    # BITMAP: width: 12, height: 2
horizDoorBmap = bytearray([3,3,3,3,3,3,3,3,3,3,3,3])

    # BITMAP: width: 2, height: 12
vertiDoorBmap = bytearray([255,255,15,15])

    # BITMAP: width: 12, height: 12
stairsBitmap = bytearray([255,1,1,1,129,129,225,225,121,249,31,255,
           15,8,14,14,15,15,9,15,8,15,8,15])

    # BITMAP: width: 14, height: 14
shopBitmap2 = bytearray([24,20,242,29,211,89,95,95,89,211,29,242,20,24,
           0,0,63,32,63,32,36,32,32,63,32,63,0,0])
           


# BITMAP: width: 6, height: 6
fire1 = bytearray([24,60,44,57,30,12])
fire2 = bytearray([14,27,63,54,16,8])
fire3 = bytearray([12,30,39,13,15,6])
fire4 = bytearray([4,2,27,63,54,28])
fireball = thumby.Sprite(6,6,fire1+fire2+fire3+fire4, key=0)

stairsSprite = thumby.Sprite(12,12,stairsBitmap)
stairsSprite.x = 30
stairsSprite.y = 14
storeSprite = thumby.Sprite(14,14,shopBitmap2)
storeSprite.x = 29
storeSprite.y = 13

topDoorSprite = thumby.Sprite(12,2,horizDoorBmap)
bottDoorSprite = thumby.Sprite(12,2,horizDoorBmap)
leftDoorSprite = thumby.Sprite(2,12,vertiDoorBmap)
rightDoorSprite = thumby.Sprite(2,12,vertiDoorBmap)
topDoorSprite.x = 30
topDoorSprite.y = 0
bottDoorSprite.x = 30
bottDoorSprite.y = 38
leftDoorSprite.x = 0
leftDoorSprite.y = 14
rightDoorSprite.x = 70
rightDoorSprite.y = 14



def draw_doors(n):
    sprites = [topDoorSprite, bottDoorSprite, leftDoorSprite, rightDoorSprite]
    for i in range(len(n)):
        if n[i] > 0:
            thumby.display.drawSprite(sprites[i])



class player():
    def __init__(self):
        self.moveNum = 0.15
        self.room = [0,0]
        self.room_neighbors = [0,0,0,0]
        self.height = 9
        self.width = 6
        self.facing = 2 #up/down/left/right
        self.attacking = 0
        self.maxlife = 10
        self.life = 10
        self.attack = 5
        self.gold = 100
        self.is_hit = 0
        # BITMAP: width: 10, height: 9
        charRBMAP = bytearray([62,227,43,35,233,62,
                    0,0,1,1,0,0])
        charLBMAP = bytearray([62,233,35,43,227,62,
                    0,0,1,1,0,0])
        charUBMAP = bytearray([62,239,47,47,239,62,
                    0,0,1,1,0,0])
        charDBMAP = bytearray([62,235,35,35,235,62,
                    0,0,1,1,0,0])
        self.charSprite = thumby.Sprite(6,9,charRBMAP+charLBMAP+
                                        charUBMAP+charDBMAP,
                                        key=0)
        self.hitbox = [[0,0],[5,8]]

    def blank_wait(self):
        t0 = time.ticks_ms()   # Get time (ms)
        thumby.display.fill(0) # Fill canvas to black
        thumby.display.update()
        time.sleep(0.25)
        
    def user_move(self):
        if thumby.buttonL.pressed():
            if self.charSprite.x == 0 and \
                    self.charSprite.y > 13 and \
                    self.charSprite.y < 19 and \
                    self.room_neighbors[2] > 0:
                self.room[1] -= 1
                self.room_neighbors = d.room_neighbors(p1.room[1], p1.room[0])
                self.charSprite.x += 61
                self.blank_wait()
            else:
                self.charSprite.x -= self.moveNum
                self.charSprite.setFrame(1)
                self.facing = 2
        if thumby.buttonR.pressed():
            if self.charSprite.x == 66 and \
                    self.charSprite.y > 13 and \
                    self.charSprite.y < 19 and \
                    self.room_neighbors[3] > 0:
                self.room[1] += 1
                self.room_neighbors = d.room_neighbors(p1.room[1], p1.room[0])
                self.charSprite.x -= 61
                self.blank_wait()
            else:
                self.charSprite.x += self.moveNum
                self.charSprite.setFrame(0)
                self.facing = 3
        if thumby.buttonU.pressed():
            if self.charSprite.x > 29 and \
                    self.charSprite.x < 38 and \
                    self.charSprite.y == 0 and \
                    self.room_neighbors[0] > 0:
                self.room[0] -= 1
                self.room_neighbors = d.room_neighbors(p1.room[1], p1.room[0])
                self.charSprite.y += 30
                self.blank_wait()
            else:
                self.charSprite.y -= self.moveNum
                self.charSprite.setFrame(2)
                self.facing = 0
        if thumby.buttonD.pressed():
            if self.charSprite.x > 29 and \
                    self.charSprite.x < 38 and \
                    self.charSprite.y == 31 and \
                    self.room_neighbors[1] > 0:
                self.room[0] += 1
                self.room_neighbors = d.room_neighbors(p1.room[1], p1.room[0])
                self.charSprite.y -= 30
                self.blank_wait()
            else:
                self.charSprite.y += self.moveNum
                self.charSprite.setFrame(3)
                self.facing = 1
        self.hitbox = [[self.charSprite.x, self.charSprite.y],[self.charSprite.x+5, self.charSprite.y+8]]
  
                
    def user_attack(self):
        if thumby.buttonA.pressed() and self.attacking == 0:
            self.attacking = 30
            x = self.charSprite.x
            y = self.charSprite.y
            if self.facing == 0:
                y -= 6
            elif self.facing == 1:
                y += 9
            elif self.facing == 2:
                x -= 6
            elif self.facing == 3:
                x += 6
            fireball = attacker(x, y, self.facing, s=2, l=40)
            return 1, fireball

        elif self.attacking > 0 and not thumby.buttonA.pressed():
            self.attacking -= 1
            return 0,0
        else: return 0,0


class attacker():
    def __init__(self,x,y,d,s,l):
        self.d = d #direc
        self.s = s #speed
        self.l = l #life
        self.attackSprite = thumby.Sprite(6,6,fire1+fire2+fire3+fire4, key=0)
        self.attackSprite.x = x
        self.attackSprite.y = y
        self.hitbox = [[x,y],[ x+5,y+5]]
    
    def update(self):
        if self.l % 4 == 0:
            if self.d == 0:
                self.attackSprite.y -= self.s
            elif self.d == 1:
                self.attackSprite.y += self.s
            elif self.d == 2:
                self.attackSprite.x -= self.s
            else: 
                self.attackSprite.x += self.s
            x = int(int(self.l/4) % 4)
            self.hitbox = [[self.attackSprite.x,self.attackSprite.y],\
                            [self.attackSprite.x+5,self.attackSprite.y+5]]
            self.attackSprite.setFrame(x)
        self.l -= 1
        


class dungeon():
    def __init__(self):
        self.w = 9
        self.h = 9
        self.random_floor()

    def random_sample(self, array, n):
        sample = []
        while len(sample) < n:
            x = random.choice(array)
            if x not in sample:
                sample.append(x)
        return sample

    def random_floor(self):
        size = random.randint(10,30)
        print('room count',size)
        rooms = [[random.randint(0,self.w-1),random.randint(0,self.h-1)]]
        while len(rooms) < size:
            i_room = random.choice(rooms)
            xy = random.randint(0,1)
            inc_dec = random.choice([-1,1])
            j_room = [i_room[0], i_room[1]]
            j_room[xy] += inc_dec
            if j_room not in rooms \
                    and j_room[0] >= 0 \
                    and j_room[0] < self.h \
                    and j_room[1] >= 0 \
                    and j_room[1] < self.w:
                rooms.append(j_room)
        self.map = [[0 for i in range(self.w)] for i in range(self.h)]
        for i in rooms:
            self.map[i[0]][i[1]] = 1
        key_rooms = self.random_sample(range(0,len(rooms)), 3)
        for i in range(len(key_rooms)):
            self.map[rooms[key_rooms[i]][0]][rooms[key_rooms[i]][1]] += i+1

    def room_finder(self, room):
        # Room types: 2=start, 3=stairs, 4=store
        for i in range(len(self.map)):
            if room in self.map[i]:
                return [i, self.map[i].index(room)]
    
    def room_neighbors(self, x, y):
        neighbors = [0,0,0,0] #up/down/left/right
        if y > 0:
            if self.map[y-1][x] > 0:
                neighbors[0] = 1
        if y < 8:
            if self.map[y+1][x] > 0:
                neighbors[1] = 1
        if x > 0:
            if self.map[y][x-1] > 0:
                neighbors[2] = 1
        if x < 8:
            if self.map[y][x+1] > 0:
                neighbors[3] = 1
        self.neighbors = neighbors
        return neighbors


class shop():
    def __init__(self):

            # BITMAP: width: 8, height: 6  
        shopIndicator = bytearray([63,33,33,33,18,18,12,4])
        self.shopIndicatorSprite = thumby.Sprite(7,6,shopIndicator)
        self.shopIndicatorSprite.x = 14
        self.shopIndicatorSprite.y = 3
        self.position = 0

    def shopping_loop(self, gold,lifeHave,atkHave):
        pos = 0
        # BITMAP: width: 3, height: 3
        bitmap3 = bytearray([5,5,2])
        selector = thumby.Sprite(3,3,bitmap3)
        selector.x = 1
        selector.y = 16
        shopping = True
        while shopping:
            lifePrice = int(lifeHave*math.log(lifeHave, 10)*4)
            atkPrice = int(2*atkHave*math.log(2*atkHave, 10)*4)
            t0 = time.ticks_ms()   # Get time (ms)
            thumby.display.fill(0) # Fill canvas to black
            thumby.display.setFont("/lib/font5x7.bin", 5, 7, 1)
            thumby.display.drawText('Atk:'+str(atkPrice), 5, 15, 1)
            thumby.display.drawText('Lif:'+str(lifePrice), 5, 27, 1)
            thumby.display.drawText(str(atkHave), 51, 15, 1)
            thumby.display.drawText(str(lifeHave), 51, 27, 1)
            thumby.display.drawText('P:'+str(gold), 5, 1, 1)
            thumby.display.drawLine(7, 1, 7, 7, 1)
            thumby.display.drawText('Lvl', 51, 1, 1)
            thumby.display.drawLine(0, 9, 72, 9, 1)
            thumby.display.drawLine(48, 0, 48, 40, 1)

            if thumby.buttonU.pressed():
                selector.y = 17
                pos = 0
            elif thumby.buttonD.pressed():
                selector.y = 29
                pos = 1
            elif thumby.buttonA.pressed():
                price = atkPrice if pos == 0 else lifePrice
                if gold >= price:
                    gold -= price
                    if pos == 0:
                        atkHave += 1
                    if pos ==1: 
                        lifeHave += 1
                time.sleep(.2)
            elif thumby.buttonB.pressed():
                shopping = False
            thumby.display.drawSprite(selector)
            thumby.display.update()

        return gold,lifeHave,atkHave


class enemy():
    def __init__(self):
        self.direction = random.randint(1,4)

    def move(self):
        r = random.randint(1,4)
        if self.direction == 1:
            if self.sprite.y > 0:
                self.sprite.y = self.sprite.y-1  
                self.hitbox[0][1] = self.hitbox[0][1]-1
                self.hitbox[1][1] = self.hitbox[1][1]-1
            else: self.direction = r
        elif self.direction == 2:
            if self.sprite.y < 32:
                self.sprite.y = self.sprite.y+1  
                self.hitbox[0][1] = self.hitbox[0][1]+1
                self.hitbox[1][1] = self.hitbox[1][1]+1
            else: self.direction = r
        elif self.direction == 3:
            if self.sprite.x > 0:
                self.sprite.x = self.sprite.x-1  
                self.hitbox[0][0] = self.hitbox[0][0]-1
                self.hitbox[1][0] = self.hitbox[1][0]-1
            else: self.direction = r
        elif self.direction == 4:
            if self.sprite.x < 64:
                self.sprite.x = self.sprite.x+1  
                self.hitbox[0][0] = self.hitbox[0][0]+1
                self.hitbox[1][0] = self.hitbox[1][0]+1
            else: self.direction = r
        if random.random() < 0.05:
            self.direction = random.randint(1,4)


class goblin(enemy):
    def __init__(self,xy):
        #self.direction = random.randint(1,4)
        super(goblin, self).__init__()
        # BITMAP: width: 7, height: 8
        goblinBitmap = bytearray([57,142,251,63,251,142,57])
        self.sprite = thumby.Sprite(7,8,goblinBitmap)
        self.sprite.x = xy[0]
        self.sprite.y = xy[1]
        self.hitbox = [[xy[0], xy[1]], [xy[0]+6, xy[1]+7]]
        self.life = 4 + (2*floor)
        self.attack = 1 *floor
        self.type = 0


class minotaur(enemy):
    def __init__(self,xy):
        super(goblin, self).__init__()
        #self.direction = random.randint(1,4)
        # BITMAP: width: 8, height: 8
        minotaurBitmap =  bytearray([58,143,218,126,126,218,143,58])
        self.sprite = thumby.Sprite(8,8,minotaurBitmap)
        self.sprite.x = xy[0]
        self.sprite.y = xy[1]
        self.hitbox = [[xy[0], xy[1]], [xy[0]+7, xy[1]+7]]
        self.life = 9 + (2*floor)
        self.attack = 1 + (2*floor)
        self.type = 1


class explosion():
    def __init__(self,x,y):
        # BITMAP: width: 8, height: 8
        e1 = bytearray([0,0,0,24,24,0,0,0])
        e2 = bytearray([0,24,36,90,90,36,24,0])
        e3 = bytearray([36,90,165,90,90,165,90,36])
        e4 = bytearray([36,90,165,66,66,165,90,36])
        e5 = bytearray([36,66,129,0,0,129,66,36])
        self.life = 60
        self.sprite = thumby.Sprite(8,8,e1+e2+e3+e4+e5,key=0)
        self.sprite.x = x
        self.sprite.y = y

    def update(self):
        self.life = self.life - 1
        self.sprite.setFrame(5-(self.life+12)//12)


def boundary_enforcer(x_size, y_size, obj):
    if obj.x > 72-x_size:
        obj.x = 72-x_size
    if obj.x < 0:
        obj.x = 0
    if obj.y > 40-y_size:
        obj.y = 40-y_size
    if obj.y < 0:
        obj.y = 0

def clean_array(array):
    to_del = []
    for i in range(len(array)):
        if array[i].l == 0:
            to_del.append(i)
    array = [array[i] for i in range(len(array)) if i not in to_del]
    return array

def update_player_dungeon(p1,d):
    for i in d.map:
        print(i)
    if p1.room == [0,0]:
        start_room = d.room_finder(2)
        p1.room = start_room
    if p1.room_neighbors == [0,0,0,0]:
        p1.room_neighbors = d.room_neighbors(p1.room[1], p1.room[0])

def spawn_positions(p1x,p1y,n):
    positions = []
    positions_selected = []
    x = [i*9+1 for i in range(8)]
    y = [i*9+1 for i in range(4)]
    y = [i if i<15 else i+3 for i in y]
    if p1x > 60:
        x = [i for i in x if i < 36]
    elif p1x < 10:
        x = [i for i in x if i > 36]
    if p1y > 28:
        y = [i for i in y if i < 20]
    elif p1y < 4:
        y = [i for i in y if i > 20]
    for i in x:
        for j in y:
            positions.append([i,j])
    for i in range(n):
        x = 16 - 1 - n
        idx = random.randint(0,x)
        positions_selected.append(positions.pop(idx))
    return positions_selected


def overlap_box(a,b):
    if a[0][0] > b[1][0] or a[1][0] < b[0][0] or a[0][1] > b[1][1] or a[1][1] < b[0][1]:
        return False
    else: return True
    

def loading_splash():
    t0 = time.ticks_ms()   # Get time (ms)
    thumby.display.fill(0) # Fill canvas to black
    thumby.display.setFont("/lib/font5x7.bin", 5, 7, 1)
    thumby.display.drawText("8-bitty", 5, 3, 1)
    thumby.display.drawText("Dungeon", 5, 11, 1)
    thumby.display.drawText("8bdungeon.", 8, 22, 1)
    thumby.display.drawText("github.io", 8, 29, 1)
    thumby.display.update()
    time.sleep(2)

floor = 1
d = dungeon()  
p1 = player()
stairs_loc = d.room_finder(3)
store_loc = d.room_finder(4)
update_player_dungeon(p1,d)
attacks = []
enemies = []
explosions = []
print('stairs', d.room_finder(3))
print('store', d.room_finder(4))
shopCooldown = 0
room_last_spawned = [p1.room[0],p1.room[1]]
tock = 0

status = 0 #0=first load, 1=active_gameplay, 2=gameover

while True:
    if status == 0: 
        loading_splash()
        status = 1
        
    elif p1.life < 1:
        time.sleep(1)
        while p1.life < 1:
            t0 = time.ticks_ms()   # Get time (ms)
            thumby.display.fill(0) # Fill canvas to black
            thumby.display.setFont("/lib/font5x7.bin", 5, 7, 1)
            thumby.display.drawText("Game Over", 8, 4, 1)
            thumby.display.drawText("A: restart", 5, 22, 1)
            thumby.display.update()
            if thumby.buttonA.pressed():
                floor = 1
                d = dungeon()  
                p1 = player()
                stairs_loc = d.room_finder(3)
                store_loc = d.room_finder(4)
                update_player_dungeon(p1,d)
                attacks = []
                enemies = []
                explosions = []
                shopCooldown = 0
                room_last_spawned = [p1.room[0],p1.room[1]]
                tock = 0
    
    elif status == 1:
        t0 = time.ticks_ms()   # Get time (ms)
        thumby.display.fill(0) # Fill canvas to black
        
        if tock == 12:
            for enemy in enemies:
                enemy.move()
            tock = 0
        else:
            tock += 1
            
        hit = []
        for a in range(len(attacks)):
            for e in range(len(enemies)):
                if overlap_box(attacks[a].hitbox,enemies[e].hitbox):
                    hit.append(e)
                    
        if len(hit) > 0: attacks = []
        
        to_del = []
        for e in hit:
            enemies[e].life = enemies[e].life - p1.attack
            if enemies[e].life < 1:
                etype = enemies[e].type
                p1.gold += (floor + 1) * max(etype*5, 1)
                to_del.append(e)
    
        if len(to_del) > 0: 
            x,y = enemies[to_del[0]].sprite.x, enemies[to_del[0]].sprite.y
            explosions.append(explosion(x,y))
            del enemies[to_del[0]]
        
        for e in explosions:
            e.update()
            thumby.display.drawSprite(e.sprite)
            if e.life == 0:
                explosions = []
            
        if p1.is_hit == 0:
            for e in enemies:
                if overlap_box(e.hitbox, p1.hitbox):
                    p1.life -= e.attack
                    p1.is_hit = 120

        if p1.room == stairs_loc:
            thumby.display.drawSprite(stairsSprite)
            px = p1.charSprite.x
            py = p1.charSprite.y
            if px < 41 and px > 26 and py < 26 and py > 7:
                p1.room = [0,0]
                d = dungeon()  
                p1.life = p1.maxlife
                floor += 1
                stairs_loc = d.room_finder(3)
                store_loc = d.room_finder(4)
                update_player_dungeon(p1,d)
                attacks = []
                
        elif p1.room == store_loc:
            thumby.display.drawSprite(storeSprite)
            px = p1.charSprite.x
            py = p1.charSprite.y
            if px < 42 and px > 25 and py < 27 and py > 8 and shopCooldown == 0:
                gold = p1.gold
                life = p1.maxlife
                atk = p1.attack
                s = shop()
                gold,life,atk = s.shopping_loop(gold,life,atk)
                p1.gold = gold
                p1.maxlife = life
                p1.attack = atk
                p1.life = p1.maxlife
                shopCooldown = 300
                
        elif p1.room != d.room_finder(2) and p1.room != stairs_loc \
                and p1.room != store_loc and p1.room != room_last_spawned:
            print(p1.room, d.room_finder(2), d.room_finder(3), d.room_finder(4))
            enemies = []
            room_last_spawned = [p1.room[0],p1.room[1]]
            n = random.randint(1,3)
            positions = spawn_positions(p1.charSprite.x,p1.charSprite.y,n)
            for i in range(n):
                p = random.random()
                if p > 0.1:
                    enemies.append(goblin(positions[i]))
                else:
                    enemies.append(minotaur(positions[i]))
        
        
        if p1.room != room_last_spawned:
            enemies = []
            
        room_last_spawned = [p1.room[0],p1.room[1]]
        for i in enemies:
            thumby.display.drawSprite(i.sprite)
            
        if shopCooldown > 0:
            shopCooldown -= 1
            
        p1.user_move()
        attack_status, attack = p1.user_attack()
        if attack_status:
            attacks.append(attack)
            
        boundary_enforcer(p1.width,p1.height, p1.charSprite)
        if p1.is_hit == 0:
            thumby.display.drawSprite(p1.charSprite)
            
        else:
            if p1.is_hit%2:
                thumby.display.drawSprite(p1.charSprite)
            p1.is_hit -= 1
            
        attacks = clean_array(attacks)
        for i in range(len(attacks)):
            attacks[i].update()
            thumby.display.drawSprite(attacks[i].attackSprite)
        
        l = int(10*(p1.life/p1.maxlife))
        if l > 0:
            thumby.display.drawLine(61, 2, 60+l, 2, 1)
        
        draw_doors(p1.room_neighbors)
        thumby.display.update()
        
        
        
        
        
        