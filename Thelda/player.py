from random import randrange
from time import sleep
from sys import path
path.append("/Games/Thelda")


class Sword:
    def __init__(self, direction, x, y, enemy_controller, thumby):
        self.sword = True
        self.x = x
        self.y = y
        self.direction = direction
        self.speed = 3
        self.timer = 0
        self.lifespan = 30
        self.interval = 12
        self.dying = False
        self.animation_counter = 0
        self.has_hit = False
        # BITMAP: width: 5, height: 5
        self.item = bytearray([31,23,0,23,31])
        self.sword_right = bytearray([27,17,27,27,27])
        self.sword_up = bytearray([31,23,0,23,31])
        self.sword_flash = bytearray([31,31,31,31,31])
        
        self.death_map_1 = bytearray([255,255,255,255,255,159,223,255,223,159,255,255,255,255,255,
           127,127,127,127,127,124,125,127,125,124,127,127,127,127,127])
           # BITMAP: width: 15, height: 15
        self.death_map_2 = bytearray([255,255,243,251,255,255,255,255,255,255,255,251,243,255,255,
           127,127,103,111,127,127,127,127,127,127,127,111,103,127,127])
          # BITMAP: width: 15, height: 15
        self.death_map_3 = bytearray([252,254,255,255,255,255,255,255,255,255,255,255,255,254,252,
           31,63,127,127,127,127,127,127,127,127,127,127,127,63,31])
           
        self.death_sprite = thumby.Sprite(15, 15, self.death_map_1+self.death_map_2+self.death_map_3, self.x - 5, self.y - 5, key=1)
        self.sprite = thumby.Sprite(5, 5, self.sword_up, self.x, self.y, key=1)
        self.sword_sprite = thumby.Sprite(5, 5, self.sword_up, self.x, self.y, key=1)
        
    def process_hit(self, enemy, thumby):
        thumby.audio.playBlocking(392, 50)
        thumby.audio.play(523, 150)
        enemy.health -= 1
        self.has_hit = True
        self.timer = self.lifespan
        
    def move(self, enemy_controller, thumby):
        if self.direction == "up":
            self.sword_sprite = thumby.Sprite(5, 5, self.sword_up+self.sword_flash, self.x, self.y - 4, key=1)
            self.sword_sprite.setFrame(self.timer)
            thumby.display.drawSprite(self.sword_sprite)
            self.y -= self.speed
        elif self.direction == "down":
            self.sword_sprite = thumby.Sprite(5, 5, self.sword_up+self.sword_flash, self.x, self.y + 4, key=1, mirrorX=0, mirrorY=1)
            self.sword_sprite.setFrame(self.timer)
            thumby.display.drawSprite(self.sword_sprite)
            self.y += self.speed
        elif self.direction == "right":
            self.sword_sprite = thumby.Sprite(5, 5, self.sword_right+self.sword_flash, self.x + 4, self.y, key=1)
            self.sword_sprite.setFrame(self.timer)
            thumby.display.drawSprite(self.sword_sprite)
            self.x += self.speed
        elif self.direction == "left":
            self.sword_sprite = thumby.Sprite(5, 5, self.sword_right+self.sword_flash, self.x - 4, self.y, key=1, mirrorX=1, mirrorY=0)
            self.sword_sprite.setFrame(self.timer)
            thumby.display.drawSprite(self.sword_sprite)
            self.x -= self.speed
        self.timer += 1
            
        for enemy in enemy_controller.enemies:
            if not self.has_hit:
                if (((self.x < enemy.x + 5) and (self.x + 5 > enemy.x)) and 
                ((enemy.y < self.y + 5) and (enemy.y + 5 > self.y))):
                    if enemy.enemy_type == "leever":
                        if not enemy.is_buried:
                            self.process_hit(enemy, thumby)
                    else:
                        if not enemy.enemy_type == "blade:":
                            self.process_hit(enemy, thumby)

    
    def display_death_sprite(self, thumby):
        self.death_sprite = thumby.Sprite(15, 15, self.death_map_1+self.death_map_1+self.death_map_2+self.death_map_2+self.death_map_3+self.death_map_3, self.x -5, self.y - 5, key=1)
        self.death_sprite.setFrame(self.animation_counter)
        thumby.display.drawSprite(self.death_sprite)
        self.animation_counter += 1
        

class Boomerang:
    def __init__(self, playerSprite, direction, display):
        self.x = playerSprite.x + 4
        self.y = playerSprite.y + 4
        self.item_type = "boomerang"
        self.direction = direction
        self.animation_counter = 0
        self.lifespan = 10
        self.lifecounter = 0
        self.playerx = playerSprite.x + 4
        self.playery = playerSprite.y + 4
        self.speed = 2
        
        
        
    def move(self, display, playerSprite, items):
        mx = int
        my = int
        if not self.lifecounter > self.lifespan:
            if self.x >= 0 and self.x < 71 and self.y >= 5 and self.y < 40:
                # if self.direction == "up" and thumby.buttonR.pressed():
                #     self.direction = "NE"
                # if self.direction == "up" and thumby.buttonL.pressed():
                #     self.direction = "NW"
                # if self.direction == "down" and thumby.buttonR.pressed():
                #     self.direction = "SE"
                # if self.direction == "down" and thumby.buttonR.pressed():
                #     self.direction = "SW"
                    
                if self.direction == "up":
                    mx = 0
                    my = -2
                elif self.direction == "down":
                    mx = 0
                    my = 2
                elif self.direction == "right":
                    mx = 2
                    my = 0
                elif self.direction == "left":
                    mx = -2
                    my = 0
                elif self.direction == "NW":
                    mx = -2
                    my = -2
                elif self.direction == "SW":
                    mx = -2
                    my = 2
                elif self.direction == "NE":
                    mx = 2
                    my = -2
                elif self.direction == "SE":
                    mx = 2
                    my = 2
                else:
                    mx = 0
                    my = 0
                self.x += mx
                self.y += my
                
            # else:
            #     thumby.audio.play(4186, 50)
        else:
            self.playerx = playerSprite.x + 4
            self.playery = playerSprite.y + 4
            self.dir = (self.playerx - self.x, self.playery - self.y)
            self.length = (abs(self.dir[0]) + abs(self.dir[1]))
            self.dir = (self.dir[0] / self.length, self.dir[1] / self.length)
            self.x = round(self.x + self.dir[0] * self.speed)
            self.y = round(self.y + self.dir[1] * self.speed)
            
            
        if self.animation_counter == 0:
            display.blit(bytearray([31,17,29,29,31]), self.x, self.y, 5, 5, 1, 0, 0)
            self.animation_counter += 1
        elif self.animation_counter == 1:
            display.blit(bytearray([31,17,29,29,31]), self.x, self.y, 5, 5, 1, 0, 1)
            self.animation_counter += 1
        elif self.animation_counter == 2:
            display.blit(bytearray([31,17,29,29,31]), self.x, self.y, 5, 5, 1, 1, 1)
            self.animation_counter += 1
        elif self.animation_counter >=3:
            display.blit(bytearray([31,17,29,29,31]), self.x, self.y, 5, 5, 1, 1, 0)
            self.animation_counter = 0
        

class Bomb:
    def __init__(self, x, y):
        self.item_type = "bomb"
        self.x = x
        self.y = y
        self.timer = 0
        self.exploding = False
        
    def explode(self, display):
        self.exploding = True
        if self.timer == 40:
            display.blit(bytearray([255,255,255,255,143,239,47,191,47,239,143,255,255,255,255,
            127,127,127,127,120,123,122,126,122,123,120,127,127,127,127]), self.x - 5, self.y - 5, 15, 15, 1, 0, 0)
            self.timer += 1
        elif self.timer == 41:
            display.blit(bytearray([255,225,125,101,245,223,191,231,191,223,245,101,125,225,255,
            127,67,95,83,87,125,126,115,126,125,87,83,95,67,127]), self.x - 5, self.y - 5, 15, 15, 1, 0, 0)
            self.timer += 1
        elif self.timer == 42:
            display.blit(bytearray([224,126,114,250,238,223,255,249,255,223,238,250,114,126,224,
            3,63,39,47,59,125,127,79,127,125,59,47,39,63,3]), self.x - 5, self.y - 5, 15, 15, 1, 0, 0)
            self.timer += 1
            self.exploding = False
        
        
class Loot:
    def __init__(self, x, y, type_of_loot, thumby):
        self.x = x
        self.y = y
        self.loot_type = type_of_loot
        self.heart_drop_map = bytearray([31,25,19,25,31])
        self.rupee_drop_map = bytearray([31,17,14,17,31])
        self.bigrupee_drop_map = bytearray([31,17,0,17,31])
        self.bomb_drop_map = bytearray([31,3,1,2,30])
        self.loot_flash = bytearray([31,31,31,31,31])
        self.timer = 0
        self.lifespan = 100
        self.destroyed = False
        self.sprite = thumby.Sprite(5, 5, self.heart_drop_map, self.x, self.y, key=1)
        
        
        if self.loot_type == "none":
            self.sprite = thumby.Sprite(5, 5, self.loot_flash, self.x, self.y, key=1)
            self.destroyed = True
        if self.loot_type == "heart":
            self.sprite = thumby.Sprite(5, 5, self.heart_drop_map, self.x, self.y, key=1)
        if self.loot_type == "rupee":
            self.sprite = thumby.Sprite(5, 5, self.rupee_drop_map, self.x, self.y, key=1)
        if self.loot_type == "bigrupee":
            self.sprite = thumby.Sprite(5, 5, self.bigrupee_drop_map, self.x, self.y, key=1)
        if self.loot_type == "bomb":
            self.sprite = thumby.Sprite(5, 5, self.bomb_drop_map, self.x, self.y, key=1)
    
    def display_loot(self, display):
        if self.timer < self.lifespan:
            display.drawSprite(self.sprite)
            self.timer += 1
        else:
            self.loot_type = "none"
            self.destroyed = True


class Player:

    def __init__(self, enemy_controller, scene_controller, thumby, savedata):
        self.hearts = savedata[0]
        self.rupees = savedata[2]
        self.keys = savedata[3]
        self.bombs = savedata[4]
        self.max_hearts = savedata[1]
        self.rupees_text = str(self.rupees)
        self.keys_text = str(self.keys)
        self.bombs_text = str(self.bombs)
        self.loot_types = ["heart", "rupee", "bigrupee", "bomb", "none"]
        self.loot_randomizer = int
        self.type_of_loot = int
        self.facingDirection = ""
        self.isColliding = False
        self.colliding_wall = None
        self.inCave = False
        self.entranceCoords = [0, 0]
        self.isTransitioning = False
        self.enemyCollision = False
        self.enemyCollisionBuffer = 20
        self.swinging = False
        self.swing_counter = 0
        self.sword_projectile = []
        self.sword_projectile_timer = 12
        self.sword_projectile_delay = 12
        self.entrance_scene = (0, 0)
        self.in_dungeon = False
        self.exit_scene = tuple
        self.active_item = ""
        self.items = []
        
        
        # Player Sprites width: 13, height: 13
        self.playerFront = bytearray([255,255,255,255,63,15,47,15,191,255,255,255,255,
           31,31,31,31,31,30,31,30,31,31,31,31,31])
        self.playerLeft = bytearray([255,255,255,255,63,15,47,15,255,255,255,255,255,
           31,31,31,31,31,30,31,30,31,31,31,31,31])
        self.playerRight = bytearray([255,255,255,255,255,15,47,15,63,255,255,255,255,
           31,31,31,31,31,30,31,30,31,31,31,31,31])

        self.playerBack = bytearray([255,255,255,255,191,15,15,15,63,255,255,255,255,
           31,31,31,31,31,30,31,30,31,31,31,31,31])
        self.playerLeftWalk = bytearray([255,255,255,255,63,15,47,15,255,255,255,255,255,
           31,31,31,31,30,31,31,31,30,31,31,31,31])
        self.playerRightWalk = bytearray([255,255,255,255,255,15,47,15,63,255,255,255,255,
           31,31,31,31,30,31,31,31,30,31,31,31,31])
        # BITMAP: width: 13, height: 13
        self.playerFrontWalk1 = bytearray([255,255,255,255,63,15,47,15,191,255,255,255,255,
           31,31,31,31,31,31,31,30,31,31,31,31,31])
        # BITMAP: width: 13, height: 13
        self.playerFrontWalk2 = bytearray([255,255,255,255,63,15,47,15,191,255,255,255,255,
           31,31,31,31,31,30,31,31,31,31,31,31,31])
        self.playerBackWalk1 = bytearray([255,255,255,255,191,15,15,15,63,255,255,255,255,
           31,31,31,31,31,31,31,30,31,31,31,31,31])
        # BITMAP: width: 13, height: 13
        self.playerBackWalk2 = bytearray([255,255,255,255,191,15,15,15,63,255,255,255,255,
           31,31,31,31,31,30,31,31,31,31,31,31,31])
        self.playerLift = bytearray([255,255,255,255,207,15,47,15,207,255,255,255,255,
            31,31,31,31,31,30,31,30,31,31,31,31,31])

        self.swordRight1 = bytearray([255,255,255,255,191,15,47,15,191,255,255,255,255,
            31,31,31,31,30,31,31,30,31,31,31,31,31])
        self.swordRight2 = bytearray([255,255,255,255,191,15,47,15,191,31,255,255,255,
            31,31,31,31,30,31,31,30,31,31,31,31,31])
        self.swordRight3 = bytearray([255,255,255,255,191,15,47,15,191,31,191,191,255,
            31,31,31,31,30,31,31,30,31,31,31,31,31])
        self.swordRight4 = bytearray([255,255,255,255,191,15,47,15,191,31,191,191,191,
            31,31,31,31,30,31,31,30,31,31,31,31,31])
            
        self.swordFront1 = bytearray([255,255,255,255,191,15,47,15,255,255,255,255,255,
            31,31,31,31,31,31,30,30,31,31,31,31,31])
        self.swordFront2 = bytearray([255,255,255,255,191,15,47,15,255,255,255,255,255,
            31,31,31,31,31,29,28,28,31,31,31,31,31])
        self.swordFront3 = bytearray([255,255,255,255,191,15,47,15,255,255,255,255,255,
            31,31,31,31,31,29,16,28,31,31,31,31,31])
        self.swordFront4 = bytearray([255,255,255,255,191,15,47,15,255,255,255,255,255,
            31,31,31,31,31,29,0,28,31,31,31,31,31])
            
        self.swordBack1 = bytearray([255,255,255,255,255,15,15,15,191,255,255,255,255,
            31,31,31,31,31,31,31,30,31,31,31,31,31])
        self.swordBack2 = bytearray([255,255,255,255,255,15,7,15,191,255,255,255,255,
            31,31,31,31,31,31,31,30,31,31,31,31,31])
        self.swordBack3 = bytearray([255,255,255,255,255,15,1,15,191,255,255,255,255,
            31,31,31,31,31,31,31,30,31,31,31,31,31])
        self.swordBack4 = bytearray([255,255,255,255,255,7,0,7,191,255,255,255,255,
            31,31,31,31,31,31,31,30,31,31,31,31,31])


        self.playerSprite = thumby.Sprite(13, 13, self.playerFront + self.playerBack + self.playerLeft + self.playerRight, self.playerLeft, key=1)
        self.playerSprite.x = 29  # Initial placement - middle of screen
        self.playerSprite.y = 13
        
        self.up_walking_sprite = thumby.Sprite(13, 13, self.playerBack + self.playerBackWalk1 + self.playerBack + self.playerBackWalk2, key=1)
        self.down_walking_sprite = thumby.Sprite(13, 13, self.playerFront + self.playerFrontWalk1 + self.playerFront + self.playerFrontWalk2, key=1)
        self.left_walking_sprite = thumby.Sprite(13, 13, self.playerLeft + self.playerLeft + self.playerLeftWalk + self.playerLeftWalk, key=1)
        self.right_walking_sprite = thumby.Sprite(13, 13, self.playerRight + self.playerRight + self.playerRightWalk + self.playerRightWalk, key=1)
        
        self.lifting_sprite = thumby.Sprite(13, 13, self.playerLift, key=1)
        
        # Player movement distance per frame
        self.moveNum = 1
        
        # Sprite animation counters
        self.walkCounter = 0
        self.swordCounter = 0
        
        # Bool to determine when using sword
        self.swinging = False

        
    def death(self, display):
        if self.hearts < 1:
            display.fill(0)
            display.drawText("GAME OVER", 10, 17, 1)
            display.update()
            sleep(2)
            thumby.thumbyHardware.reset() 
            
            
    def get_collision(self, collider, mod1, mod2, mod3, mod4, mod5, mod6):
        if (((self.playerSprite.x + mod1 < collider.x + mod2) and (self.playerSprite.x + mod3 > collider.x)) and 
            ((collider.y < self.playerSprite.y + mod4) and (collider.y + mod5 > self.playerSprite.y + mod6))):
                self.isColliding = True
                self.colliding_wall = collider
                
                
    def process_hit(self, direction, enemy, thumby):
        if enemy.enemy_type == "leever":
            if not enemy.is_buried:
                thumby.audio.playBlocking(392, 50)
                thumby.audio.play(523, 150)
                enemy.health -= 1
                if enemy.facingDirection == "up":
                    if direction == "down":
                        enemy.y += 4
                elif enemy.facingDirection == "down":
                    if direction == "up":
                        enemy.y -= 4
                elif enemy.facingDirection == "left":
                    if direction == "right":
                        enemy.x += 4
                elif enemy.facingDirection == "right":
                    if direction == "left":
                        enemy.x -= 4
        if enemy.enemy_type == "stalfos":
            thumby.audio.playBlocking(392, 50)
            thumby.audio.play(523, 150)
            enemy.health -= 1
            if enemy.facingDirection == "up":
                if direction == "down":
                    enemy.y += 4
            elif enemy.facingDirection == "down":
                if direction == "up":
                    enemy.y -= 4
            elif enemy.facingDirection == "left":
                if direction == "right":
                    enemy.x += 4
            elif enemy.facingDirection == "right":
                if direction == "left":
                    enemy.x -= 4
        else:
            if not enemy.enemy_type == "blade":
                thumby.audio.playBlocking(392, 50)
                thumby.audio.play(523, 150)
                enemy.health -= 1
                
    
    def hit_detection(self, enemy_controller, thumby):
        for enemy in enemy_controller.enemies:
            if self.facingDirection == "up":
                if (((self.playerSprite.x + 6 <= enemy.x + 5) and (self.playerSprite.x + 7 >= enemy.x)) and 
            ((enemy.y < self.playerSprite.y + 4) and (enemy.y + 5 > self.playerSprite.y))):
                    if self.swinging:
                        self.process_hit(self.facingDirection, enemy, thumby)
            elif self.facingDirection == "down":
                if (((self.playerSprite.x + 6 <= enemy.x + 5) and (self.playerSprite.x + 7 >= enemy.x)) and 
            ((enemy.y < self.playerSprite.y + 13) and (enemy.y + 5 > self.playerSprite.y + 9))):
                    if self.swinging:
                        self.process_hit(self.facingDirection, enemy, thumby)
            elif self.facingDirection == "right":
                if (((self.playerSprite.x + 6 < enemy.x + 5) and (self.playerSprite.x + 13 > enemy.x)) and 
            ((enemy.y <= self.playerSprite.y + 7) and (enemy.y + 5 >= self.playerSprite.y + 6))):
                    if self.swinging:
                        self.process_hit(self.facingDirection, enemy, thumby)
            elif self.facingDirection == "left":
                if (((self.playerSprite.x < enemy.x + 5) and (self.playerSprite.x + 4 > enemy.x)) and 
            ((enemy.y <= self.playerSprite.y + 7) and (enemy.y + 5 >= self.playerSprite.y + 6))):
                    if self.swinging:
                        self.process_hit(self.facingDirection, enemy, thumby)

# TO DO:  Put this in the enemy_controller object
            if not enemy.enemy_type == "blade":
                if enemy.health < 1:
                    enemy.is_dead = True
                    enemy_controller.enemies_used = enemy_controller.enemies_used + (enemy.identity, )
                    self.loot_randomizer = randrange(0, 5)
                    
                    if self.loot_randomizer == 1:
                        self.type_of_loot = self.loot_types[0]
                    elif self.loot_randomizer == 2:
                        self.type_of_loot = self.loot_types[1]
                    elif self.loot_randomizer == 3:
                        self.type_of_loot = self.loot_types[2]
                    elif self.loot_randomizer == 4:
                        self.type_of_loot = self.loot_types[3]
                    else:
                        self.type_of_loot = self.loot_types[4]
                    enemy_controller.loot.append(Loot(enemy.x, enemy.y, self.type_of_loot, thumby))
                    
                    while enemy_controller.animation_counter < enemy_controller.animation_length:
                        enemy.map_to_display = [enemy.blank_map, 0, 0]
                        enemy_controller.display_death_sprite(enemy)
                        
                    else:
                        enemy.health = enemy.starting_health
                        enemy.is_dead = False
                        enemy_index = enemy_controller.enemies.index(enemy)
                        # print(enemy_index)
                        del enemy_controller.enemies[enemy_index]
                        enemy_controller.animation_counter = 0
                if len(enemy_controller.enemies) == 0:
                    enemy_controller.enemies_killed = True
    
    def save_game(self, scene_controller, json):
        save_list = [6, self.max_hearts, self.rupees, self.keys, self.bombs, scene_controller.isDangerous, scene_controller.doors_unlocked, scene_controller.keys_used]
        with open("/Games/Thelda/save.json", 'w') as savefile: 
            json.dump(save_list, savefile)
            
    def remove_block_lock(self, scene_controller):
        if "blocklocks" in scene_controller.this_scene:
            for blocklock in scene_controller.block_locks:
                if blocklock.id == self.colliding_wall.id:
                    scene_controller.doors_unlocked.append(blocklock.id)
                    scene_controller.block_locks.remove(blocklock)
    

    # Dpad movement.  TO DO:  Refactor this monstrosity
    def move_player(self, scene_controller, enemy_controller, thumby, json):

        for item in scene_controller.items:
            if (((self.playerSprite.x + 4 < item.x + 5) and (self.playerSprite.x + 9 > item.x)) and 
            ((item.y < self.playerSprite.y + 9) and (item.y + 5 > self.playerSprite.y + 4))):
                if scene_controller.isDangerous:
                    if item.sword:
                        scene_controller.isDangerous = False
                        scene_controller.this_scene["items"][0].y -= 40
                else:
                    if item.item_type == "heartcontainer":
                        self.max_hearts += 2
                        self.hearts = self.max_hearts
                        scene_controller.heart_containers_used.append(item.identity)
                        scene_controller.items.remove(item)
                        
        for lock in scene_controller.locks:
            if (((self.playerSprite.x + 4 < lock.x + 6) and (self.playerSprite.x + 9 > lock.x - 1)) and 
            ((lock.y - 1 < self.playerSprite.y + 9) and (lock.y + 6 > self.playerSprite.y + 4))):
                if self.keys > 0:
                    scene_controller.doors_unlocked.append(lock.identity)
                    scene_controller.locks.remove(lock)
                    print(scene_controller.doors_unlocked)
                    self.keys -= 1
                    self.keys_text = str(self.keys)
        for key in scene_controller.keys:
            if not key.carried and key.home_scene == scene_controller.scene_string:
                if (((self.playerSprite.x + 4 < key.x + 3) and (self.playerSprite.x + 9 > key.x)) and 
                ((key.y < self.playerSprite.y + 9) and (key.y + 3 > self.playerSprite.y + 4))):
                    if not key.conditional:
                        print(f"keys used: {scene_controller.keys_used}")
                        print(f"key id: {key.identity}")
                        if not key.identity in scene_controller.keys_used:
                            scene_controller.keys_used.append(key.identity)
                            scene_controller.keys.remove(key)
                            scene_controller.key_assigned = False
                            print(scene_controller.keys_used)
                            self.keys += 1
                            self.keys_text = str(self.keys)
                    else:
                        if enemy_controller.enemies == []:
                            print(f"keys used: {scene_controller.keys_used}")
                            print(f"key id: {key.identity}")
                            if not key.identity in scene_controller.keys_used:
                                scene_controller.keys_used.append(key.identity)
                                scene_controller.keys.remove(key)
                                scene_controller.key_assigned = False
                                print(scene_controller.keys_used)
                                self.keys += 1
                                self.keys_text = str(self.keys)

                
        for door in scene_controller.doors:
            if self.playerSprite.x == door.x - 4 and self.playerSprite.y == door.y - 4:
                self.save_game(scene_controller, json)
                scene_controller.clear_scene(enemy_controller)
                self.entranceCoords = [self.playerSprite.x, self.playerSprite.y + 5]
                if scene_controller.is_dungeon:
                    self.entrance_scene = (scene_controller.scene_x, scene_controller.scene_y)
                    print(f"Entrance Scene: {self.entrance_scene}")
                    scene_controller.scene_x *= -100
                    scene_controller.scene_y *= 100
                    self.exit_scene = (scene_controller.scene_x, scene_controller.scene_y)
                    print(f"Exit Scene: {self.exit_scene}")
                    self.in_dungeon = True
                    scene_controller.in_dungeon = True
                    self.playerSprite.x = 29
                    self.playerSprite.y = 31
                    scene_controller.is_dungeon = False
                    
                else:
                    scene_controller.scene_x *= -1
                    scene_controller.scene_y += 1
                    print(f"Scene:{scene_controller.scene_x}, {scene_controller.scene_y}")
                    self.playerSprite.x = 29
                    self.playerSprite.y = 31
                    self.inCave = True
                return
            
        for enemy in enemy_controller.enemies:
            if not enemy.prespawn:
                if (((self.playerSprite.x + 4 < enemy.x + 5) and (self.playerSprite.x + 9 > enemy.x)) and 
                ((enemy.y < self.playerSprite.y + 9) and (enemy.y + 5 > self.playerSprite.y + 4))):
                    if not self.enemyCollision:
                        if self.enemyCollisionBuffer >= 20:
                            # thumby.audio.play(523, 300)
                            if enemy.enemy_type == "leever":
                                if not enemy.is_buried:
                                    thumby.audio.playBlocking(523, 50)
                                    thumby.audio.play(392, 200)
                                    self.hearts -= enemy.damage
                                    thumby.display.fill(1)
                                    if enemy.facingDirection == "up":
                                        enemy.facingDirection = "down"
                                    elif enemy.facingDirection == "down":
                                        enemy.facingDirection = "up"
                                    elif enemy.facingDirection == "left":
                                        enemy.facingDirection = "right"
                                    elif enemy.facingDirection == "right":
                                        enemy.facingDirection = "left"
                            else:
                                thumby.audio.playBlocking(523, 50)
                                thumby.audio.play(392, 200)
                                self.hearts -= enemy.damage
                                thumby.display.fill(1)
                            self.enemyCollisionBuffer = 0
            if enemy.enemy_type == "octorok":            
                for rock in enemy.rocks:
                    if (((self.playerSprite.x + 4 < rock.x + 3) and (self.playerSprite.x + 9 > rock.x)) and 
                    ((rock.y < self.playerSprite.y + 9) and (rock.y + 3 > self.playerSprite.y + 4))):
                        # print("hit by rock")
                        
                        if self.facingDirection == "up" and rock.direction == "down":
                            rock.direction = "up"
                            rock.reflected = True
                            thumby.audio.play(4186, 50)
                        elif self.facingDirection == "down" and rock.direction == "up":
                            rock.direction = "down"
                            rock.reflected = True
                            thumby.audio.play(4186, 50)
                        elif self.facingDirection == "right" and rock.direction == "left":
                            rock.direction = "right"
                            rock.reflected = True
                            thumby.audio.play(4186, 50)
                        elif self.facingDirection == "left" and rock.direction == "right":
                            rock.direction = "left"
                            rock.reflected = True
                            thumby.audio.play(4186, 50)
                        else:
                            thumby.audio.playBlocking(523, 50)
                            thumby.audio.play(392, 200)
                            self.hearts -= 1
                            thumby.display.fill(1)
                            rock_index = enemy.rocks.index(rock)
                            del enemy.rocks[rock_index]
            if enemy.enemy_type == "zora" or enemy.enemy_type == "aquamentus":            
                for magic in enemy.magic:
                    if (((self.playerSprite.x + 4 < magic.x + 3) and (self.playerSprite.x + 9 > magic.x)) and 
                    ((magic.y < self.playerSprite.y + 9) and (magic.y + 3 > self.playerSprite.y + 4))):
                        print("hit by magic")
                        thumby.audio.playBlocking(523, 50)
                        thumby.audio.play(392, 200)
                        self.hearts -= 1
                        thumby.display.fill(1)
                        magic_index = enemy.magic.index(magic)
                        del enemy.magic[magic_index]
                        enemy.has_fired = True
        

        self.enemyCollisionBuffer += 1
        if self.enemyCollisionBuffer > 20:
            self.enemyCollision = False
    
        collidables = (scene_controller.walls + scene_controller.bushes + 
                   scene_controller.water + scene_controller.barriers + 
                   scene_controller.locks + scene_controller.blocks + scene_controller.pushable_blocks + scene_controller.block_locks)
        if thumby.buttonU.pressed():
            if not self.isTransitioning:
                self.isColliding = False
                self.facingDirection = "up"
                for collidable in collidables:
                    self.get_collision(collidable, 4, 5, 9, 9, 5, 3)
                if self.isColliding:
                    if self.colliding_wall in scene_controller.pushable_blocks:
                        if self.colliding_wall.pushable == self.facingDirection:
                            self.colliding_wall.y -= 5
                            self.colliding_wall.pushable = "Null"
                            self.remove_block_lock(scene_controller)
                    self.playerSprite.y = self.colliding_wall.y + 2
                    self.isColliding = False
                player_sprite_x = self.playerSprite.x
                player_sprite_y = self.playerSprite.y
                self.playerSprite = self.up_walking_sprite
                self.playerSprite.x = player_sprite_x
                self.playerSprite.y = player_sprite_y
                self.playerSprite.setFrame(self.walkCounter)
                if self.playerSprite.y > 1:
                    if not self.isColliding:
                        self.playerSprite.y -= self.moveNum
                else:
                    scene_controller.is_dungeon = False
                    self.save_game(scene_controller, json)
                    self.items = []
                    scene_controller.clear_scene(enemy_controller)
                    scene_controller.scene_y += 1
                    print(f"Scene:{scene_controller.scene_x}, {scene_controller.scene_y}")
                    self.playerSprite.y += 30
                    self.isTransitioning = True

        

         
        if thumby.buttonD.pressed():
            if not self.isTransitioning:
                self.isColliding = False
                self.facingDirection = "down"
                for collidable in collidables:    
                    self.get_collision(collidable, 4, 5, 9, 10, 5, 4)
                if self.isColliding:
                    if self.colliding_wall in scene_controller.pushable_blocks:
                        if self.colliding_wall.pushable == self.facingDirection:
                            self.colliding_wall.y += 5
                            self.colliding_wall.pushable = "Null"
                            self.remove_block_lock(scene_controller)
                    self.playerSprite.y = self.colliding_wall.y - 10
                    self.isColliding = False
                player_sprite_x = self.playerSprite.x
                player_sprite_y = self.playerSprite.y
                self.playerSprite = self.down_walking_sprite
                self.playerSprite.x = player_sprite_x
                self.playerSprite.y = player_sprite_y
                self.playerSprite.setFrame(self.walkCounter)
                if self.playerSprite.y < 31:
                    if not self.isColliding:
                        self.playerSprite.y += self.moveNum
                else:
                    if self.inCave:
                        self.save_game(scene_controller, json)
                        self.items = []
                        scene_controller.clear_scene(enemy_controller)
                        scene_controller.scene_x *= -1
                        scene_controller.scene_y -= 1
                        print(f"Scene:{scene_controller.scene_x}, {scene_controller.scene_y}")
                        self.playerSprite.x = self.entranceCoords[0]
                        self.playerSprite.y = self.entranceCoords[1]
                        self.inCave = False
                        scene_controller.is_still_here = False
                    elif self.in_dungeon:
                        self.save_game(scene_controller, json)
                        self.items = []
                        scene_controller.clear_scene(enemy_controller)
                        if scene_controller.scene_x == self.exit_scene[0] and scene_controller.scene_y == self.exit_scene[1]:
                            scene_controller.scene_x = self.entrance_scene[0]
                            scene_controller.scene_y = self.entrance_scene[1]
                            self.playerSprite.x = self.entranceCoords[0]
                            self.playerSprite.y = self.entranceCoords[1]
                            print(f"Scene:{scene_controller.scene_x}, {scene_controller.scene_y}")
                            self.in_dungeon = False
                            scene_controller.in_dungeon = False
                            enemy_controller.enemies_used = ()
                        else:
                            self.save_game(scene_controller, json)
                            self.items = []
                            scene_controller.clear_scene(enemy_controller)
                            scene_controller.scene_y -= 1
                            print(f"Scene:{scene_controller.scene_x}, {scene_controller.scene_y}")
                            self.playerSprite.y -= 30
                            self.isTransitioning = True
                            
                        
                    else:
                        scene_controller.is_dungeon = False
                        self.save_game(scene_controller, json)
                        self.items = []
                        scene_controller.clear_scene(enemy_controller)
                        scene_controller.scene_y -= 1
                        print(f"Scene:{scene_controller.scene_x}, {scene_controller.scene_y}")
                        self.playerSprite.y -= 30
                        self.isTransitioning = True


        if thumby.buttonL.pressed():
            if not self.isTransitioning:
                self.isColliding = False
                self.facingDirection = "left"
                for collidable in collidables:    
                    self.get_collision(collidable, 3, 5, 9, 9, 5, 4)
                if self.isColliding:
                    if self.colliding_wall in scene_controller.pushable_blocks:
                        if self.colliding_wall.pushable == self.facingDirection:
                            self.colliding_wall.x -= 5
                            self.colliding_wall.pushable = "Null"
                            self.remove_block_lock(scene_controller)
                    self.playerSprite.x = self.colliding_wall.x + 2
                    self.isColliding = False
                player_sprite_x = self.playerSprite.x
                player_sprite_y = self.playerSprite.y
                self.playerSprite = self.left_walking_sprite
                self.playerSprite.x = player_sprite_x
                self.playerSprite.y = player_sprite_y
                self.playerSprite.setFrame(self.walkCounter)
                if self.playerSprite.x > -4:
                    if not self.isColliding:
                        self.playerSprite.x -= self.moveNum
                else:
                    scene_controller.is_dungeon = False
                    self.save_game(scene_controller, json)
                    self.items = []
                    scene_controller.clear_scene(enemy_controller)
                    scene_controller.scene_x -= 1
                    print(f"Scene:{scene_controller.scene_x}, {scene_controller.scene_y}")
                    self.playerSprite.x += 67
                    self.isTransitioning = True

        if thumby.buttonR.pressed():
            if not self.isTransitioning:
                self.isColliding = False
                self.facingDirection = "right"
                for collidable in collidables:    
                    self.get_collision(collidable, 4, 5, 10, 9, 5, 4)
                if self.isColliding:
                    if self.colliding_wall in scene_controller.pushable_blocks:
                        if self.colliding_wall.pushable == self.facingDirection:
                            self.colliding_wall.x += 5
                            self.colliding_wall.pushable = "Null"
                            self.remove_block_lock(scene_controller)
                    self.playerSprite.x = self.colliding_wall.x - 10
                    self.isColliding = False
                player_sprite_x = self.playerSprite.x
                player_sprite_y = self.playerSprite.y
                self.playerSprite = self.right_walking_sprite
                self.playerSprite.x = player_sprite_x
                self.playerSprite.y = player_sprite_y
                self.playerSprite.setFrame(self.walkCounter)
                if self.playerSprite.x < 63:
                    if not self.isColliding:
                        self.playerSprite.x += self.moveNum
                else:
                    scene_controller.is_dungeon = False
                    self.save_game(scene_controller, json)
                    self.items = []
                    scene_controller.clear_scene(enemy_controller)
                    scene_controller.scene_x += 1
                    print(f"Scene:{scene_controller.scene_x}, {scene_controller.scene_y}")
                    self.playerSprite.x -= 67
                    self.isTransitioning = True

        if not thumby.dpadPressed():
            self.walkCounter = 0
            self.playerSprite.setFrame(self.walkCounter)

        # Display Sprite
        self.walkCounter += 1
        thumby.display.drawSprite(self.playerSprite)
        self.isTransitioning = False
        
        # print(f"{self.isColliding}")
            
            
    def swing_sword(self, enemy_controller, thumby):
        if len(self.sword_projectile) >= 1:
            for projectile in self.sword_projectile:
                if projectile.timer > projectile.lifespan:
                    projectile.dying = True
                if projectile.x < 0 or projectile.x + 2 >= 71 or projectile.y <= 4 or projectile.y + 2 >= 39:  # Detects screen edges for sword projectile
                    projectile.dying = True
                if projectile.dying == True:
                    projectile.display_death_sprite(thumby)
                    if projectile.animation_counter > 3:
                        self.sword_projectile = []
                else:
                    projectile.move(enemy_controller, thumby)

        else:
            self.sword_projectile_timer += 1
        
        if self.facingDirection == "up" and not thumby.actionPressed():
            self.playerSprite = self.up_walking_sprite
            self.swing_counter = 0
        elif self.facingDirection == "down" and not thumby.actionPressed():
            self.playerSprite = self.down_walking_sprite
            self.swing_counter = 0
        elif self.facingDirection == "right" and not thumby.actionPressed():
            self.playerSprite = self.right_walking_sprite
            self.swing_counter = 0
        elif self.facingDirection == "left" and not thumby.actionPressed():
            self.playerSprite = self.left_walking_sprite
            self.swing_counter = 0
        thumby.display.drawSprite(self.playerSprite)

    
        if thumby.buttonA.pressed() and self.swing_counter < 5:
            if self.hearts == self.max_hearts and self.sword_projectile == []:
                if self.sword_projectile_timer > self.sword_projectile_delay:
                    self.sword_projectile.append(Sword(self.facingDirection, self.playerSprite.x + 4, self.playerSprite.y + 4, enemy_controller, thumby))
                    # print(self.sword_projectile)
                    self.sword_projectile_timer = 0
            self.swinging = True
            self.swordCounter = 0
            while self.facingDirection == "right" and self.swordCounter <= 4:
                player_sprite_x = self.playerSprite.x
                player_sprite_y = self.playerSprite.y
                self.playerSprite = thumby.Sprite(13, 13, self.swordRight1+self.swordRight2+self.swordRight3+self.swordRight4, player_sprite_x, player_sprite_y, key=1)
                self.playerSprite.setFrame(self.swordCounter)
                thumby.display.drawSprite(self.playerSprite)
                self.swordCounter += 1
            
            while self.facingDirection == "left" and self.swordCounter <= 4:
                player_sprite_x = self.playerSprite.x
                player_sprite_y = self.playerSprite.y
                self.playerSprite = thumby.Sprite(13, 13, self.swordRight1+self.swordRight2+self.swordRight3+self.swordRight4, player_sprite_x, player_sprite_y, key=1, mirrorX=1)
                self.playerSprite.setFrame(self.swordCounter)
                thumby.display.drawSprite(self.playerSprite)
                self.swordCounter += 1
                
            while self.facingDirection == "up" and self.swordCounter <= 4:
                player_sprite_x = self.playerSprite.x
                player_sprite_y = self.playerSprite.y
                self.playerSprite = thumby.Sprite(13, 13, self.swordBack1+self.swordBack2+self.swordBack3+self.swordBack4, player_sprite_x, player_sprite_y, key=1)
                self.playerSprite.setFrame(self.swordCounter)
                thumby.display.drawSprite(self.playerSprite)
                self.swordCounter += 1
                
            while self.facingDirection == "down" and self.swordCounter <= 4:
                player_sprite_x = self.playerSprite.x
                player_sprite_y = self.playerSprite.y
                self.playerSprite = thumby.Sprite(13, 13, self.swordFront1+self.swordFront2+self.swordFront3+self.swordFront4, player_sprite_x, player_sprite_y, key=1)
                self.playerSprite.setFrame(self.swordCounter)
                thumby.display.drawSprite(self.playerSprite)
                self.swordCounter += 1
            self.swing_counter += 1

                
        else:
            self.swinging = False
        thumby.display.drawSprite(self.playerSprite)
        
        
    def use_item(self, enemy_controller, thumby):
        if thumby.buttonB.pressed():
            if self.active_item == "boomerang":
                if self.items == []:
                    self.items.append(Boomerang(self.playerSprite, self.facingDirection, thumby.display))
            elif self.active_item == "bombs" and self.bombs >= 1:
                if self.items == []:
                    if self.facingDirection == "up":
                        bomb_x = self.playerSprite.x + 4
                        bomb_y = self.playerSprite.y - 1
                    elif self.facingDirection == "down":
                        bomb_x = self.playerSprite.x + 4
                        bomb_y = self.playerSprite.y + 9
                    elif self.facingDirection == "right":
                        bomb_x = self.playerSprite.x + 9
                        bomb_y = self.playerSprite.y + 4
                    elif self.facingDirection == "left":
                        bomb_x = self.playerSprite.x
                        bomb_y = self.playerSprite.y + 4
                    else:
                        bomb_x = playerSprite.x
                        bomb_y = playerSprite.y
                    self.items.append(Bomb(bomb_x, bomb_y))
                    if self.bombs > 0:
                        self.bombs -= 1
        if not self.items == []:
            for item in self.items:
                if item.item_type == "boomerang":
                    item.move(thumby.display, self.playerSprite, self.items)
                    for enemy in enemy_controller.enemies:
                        if enemy.x < item.x + 5 and enemy.x + 5 > item.x and item.y < enemy.y + 5 and item.y + 5 > enemy.y:
                            thumby.audio.play(4186, 50)
                            item.lifecounter = item.lifespan
                            if not enemy.frozen:
                                if not enemy.enemy_type == "blade" and not enemy.enemy_type == "aquamentus":
                                    enemy.frozen = True
                                
                    if (((self.playerSprite.x + 4 < item.x + 5) and (self.playerSprite.x + 9 > item.x)) and 
                    ((item.y < self.playerSprite.y + 9) and (item.y + 5 > self.playerSprite.y + 4))) and item.lifecounter >= item.lifespan:
                        self.items.remove(item)
                    else:
                        item.lifecounter += 1
            
                elif item.item_type == "bomb":
                    if item.timer >= 40:
                        item.explode(thumby.display)
                        thumby.audio.play(523, 150)
                        for enemy in enemy_controller.enemies:
                            if ((enemy.x < item.x + 10) and (enemy.x + 5 > item.x - 5) and 
                            (enemy.y < item.y + 10) and (enemy.y + 5 > item.y - 5)):
                                enemy.health -= 3
                        if item.timer == 42:
                            if ((self.playerSprite.x - 4 < item.x + 10) and (self.playerSprite.x + 9 > item.x - 5) and 
                                (self.playerSprite.y - 4 < item.y + 10) and (self.playerSprite.y + 9 > item.y - 5)):
                                    thumby.audio.playBlocking(523, 50)
                                    thumby.audio.play(392, 200)
                                    self.hearts -= 2
                                    thumby.display.fill(1)
                            
                        if item.timer >= 43:
                            self.items.remove(item)
                    else:
                        thumby.display.blit(bytearray([31,3,9,2,31]), item.x, item.y, 5, 5, 1, 0, 0)
                        item.timer += 1
        
    
