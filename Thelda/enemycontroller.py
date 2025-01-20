from thumby import Sprite, display
import gc
from sys import path
path.append("/Games/Thelda")
from random import choice, randrange, randint

class Octorok:
    def __init__(self, x, y, facingDirection, walk_distance, rocks, identity):
        self.identity = identity
        self.enemy_type = "octorok"
        self.x = x
        self.y = y
        self.damage = 1
        self.starting_health = 1
        self.health = 1
        self.frozen = False
        self.freeze_counter = 0
        self.is_dead = False
        self.attack_speed = 199
        self.prespawn = True

        self.blank_map = bytearray([31, 31, 31, 31, 31])
        self.prespawn_map = bytearray([25, 5, 14, 20, 19])
        self.enemy_up_map = bytearray([7, 10, 0, 10, 7])
        self.enemy_up_map_2 = bytearray([19, 9, 1, 9, 19])
        self.enemy_right_map = bytearray([0, 10, 17, 27, 17])
        self.enemy_right_map_2 = bytearray([17, 10, 0, 17, 31])

        self.directions = ["up", "down", "left", "right"]
        self.facingDirection = facingDirection
        self.colliding_wall = None
        self.move_speed = 1
        self.move_buffer = 0
        self.walk_distance = walk_distance
        self.distance_count = 0
        self.attack_counter = 0
        self.rocks = rocks


class Tektite:
    def __init__(self, x, y, identity):
        self.identity = identity
        self.enemy_type = "tektite"
        self.x = x
        self.y = y
        self.damage = 1
        self.starting_health = 1
        self.health = 1
        self.frozen = False
        self.freeze_counter = 0
        self.is_dead = False
        self.attack_speed = 199
        self.prespawn = True
        self.move_speed = 1
        self.animation_counter = 0
        self.is_jumping = False
        self.apex_reached = False
        self.jump_counter = 0
        self.jump_direction = ""
        self.jump_x = int
        self.jump_y = int
        self.prejump_x = int
        self.prejump_y = int
        self.blank_map = bytearray([31, 31, 31, 31, 31])
        self.prespawn_map = bytearray([25, 5, 14, 20, 19])
        self.extended_map = bytearray([5, 26, 24, 26, 5])
        self.crouched_map = bytearray([3, 21, 17, 21, 3])


class Zora:
    def __init__(self, x, y, identity):
        self.identity = identity
        self.enemy_type = "zora"
        self.x = x
        self.y = y
        self.damage = 1
        self.starting_health = 3
        self.health = 3
        self.frozen = False
        self.freeze_counter = 0
        self.is_dead = False
        self.attack_speed = 199
        self.magic = []
        self.prespawn = True
        self.spawn_animation_counter = 0
        self.blank_map = bytearray([31, 31, 31, 31, 31])
        self.prespawn_map = bytearray([25, 5, 14, 20, 19])
        self.surface_map_1 = bytearray([15, 15, 23, 23, 23])
        self.surface_map_2 = bytearray([23, 23, 15, 15, 15])
        self.surface_map_3 = bytearray([23, 15, 15, 23, 23])
        self.attack_map = bytearray([1, 10, 8, 10, 1])
        self.has_fired = False


class Leever:
    def __init__(self, x, y, identity):
        self.identity = identity
        self.enemy_type = "leever"
        self.x = x
        self.y = y
        self.damage = 1
        self.starting_health = 3
        self.health = 3
        self.frozen = False
        self.freeze_counter = 0
        self.is_dead = False
        self.prespawn = True
        self.spawn_animation_counter = 0
        self.is_buried = True

        self.directions = ["up", "down", "left", "right"]
        self.facingDirection = ""
        self.colliding_wall = None
        self.move_speed = 1
        self.move_buffer = 0
        self.walk_distance = 5
        self.distance_count = 0
        self.blank_map = bytearray([31, 31, 31, 31, 31])
        self.prespawn_map = bytearray([31, 31, 31, 31, 31])
        self.surface_map_1 = bytearray([15, 31, 15, 31, 15])
        self.surface_map_2 = bytearray([15, 23, 15, 23, 15])
        self.surface_map_3 = bytearray([15, 19, 3, 19, 15])
        self.attacking_map_1 = bytearray([15, 4, 1, 4, 15])
        self.attacking_map_2 = bytearray([14, 5, 0, 5, 14])


class Stalfos:
    def __init__(self, x, y, facingDirection, walk_distance, identity):
        self.identity = identity
        self.enemy_type = "stalfos"
        self.x = x
        self.y = y
        self.damage = 1
        self.health = 2
        self.frozen = False
        self.freeze_counter = 0
        self.starting_health = 2
        self.animation_counter = 0
        # BITMAP: width: 7, height: 6
        self.map = bytearray([27,21,16,5,28])
        self.directions = ["up", "down", "left", "right"]
        self.prespawn = True
        self.prespawn_map = bytearray([25, 5, 14, 20, 19])
        self.facingDirection = facingDirection
        self.walk_distance = walk_distance
        self.distance_count = 0
        self.move_buffer = 0
        self.is_dead = False
        self.move_speed = 1
        self.has_key = False
        self.blank_map = bytearray([31, 31, 31, 31, 31])
        

class Keese:
    def __init__(self, x, y, identity):
        self.identity = identity
        self.enemy_type = "keese"
        self.x = x
        self.y = y
        self.damage = 1
        self.starting_health = 1
        self.health = 1
        self.frozen = False
        self.freeze_counter = 0
        self.is_dead = False
        self.attack_speed = randrange(20, 60)
        self.prespawn = True
        self.animation_counter = 0
        self.is_flying = False
        self.fly_counter = 0
        self.flight_time = 120
        self.blank_map = bytearray([31, 31, 31, 31, 31])
        self.prespawn_map = bytearray([31,19,25,19,31])
        self.flap1_map = bytearray([25,29,27,29,25])
        self.flap2_map = bytearray([23,19,27,19,23])
        
        
class Gel:
    def __init__(self, x, y, facingDirection, walk_distance, identity):
        self.identity = identity
        self.enemy_type = "gel"
        self.x = x
        self.y = y
        self.damage = 1
        self.health = 1
        self.frozen = False
        self.freeze_counter = 0
        self.starting_health = 1
        self.animation_counter = 0
        # BITMAP: width: 7, height: 6
        self.map = bytearray([31,19,21,19,31])
        self.move_map = bytearray([31,23,19,23,31])
        self.directions = ["up", "down", "left", "right"]
        self.prespawn = True
        self.prespawn_map = bytearray([25, 5, 14, 20, 19])
        self.facingDirection = facingDirection
        self.walk_distance = walk_distance
        self.distance_count = 0
        self.move_buffer = 0
        self.is_dead = False
        self.move_speed = 5
        self.has_key = False
        self.blank_map = bytearray([31, 31, 31, 31, 31])
        

class Blade:
    def __init__(self, x, y, h_move_distance, v_move_distance, identity):
        self.identity = identity
        self.enemy_type = "blade"
        self.x = x
        self.y = y
        self.starting_x = x
        self.starting_y = y
        self.damage = 1
        # BITMAP: width: 7, height: 6
        self.map = bytearray([21,0,17,0,21])
        self.directions = ["up", "down", "left", "right"]
        self.horizontal_move_distance = h_move_distance
        self.vertical_move_distance = v_move_distance
        self.distance_count = 0
        self.move_buffer = 0
        self.move_speed = 1
        self.prespawn = False
        self.frozen = False
        self.attacking = False
        self.attacking_direction = "Null"


class Rock:
    def __init__(self, enemy):
        self.parent_enemy = enemy
        self.x = enemy.x + 1
        self.y = enemy.y + 1
        self.rock = bytearray([0,2,0])
        self.direction = enemy.facingDirection
        self.speed = 2
        self.timer = 0
        self.lifespan = 10
        self.reflected = False


    def move(self):
        if self.direction == "up":
            self.y -= self.speed
            if self.reflected:
                self.x -= self.speed
        elif self.direction == "down":
            self.y += self.speed
            if self.reflected:
                self.x += self.speed
        elif self.direction == "right":
            self.x += self.speed
            if self.reflected:
                self.y += self.speed
        elif self.direction == "left":
            self.x -= self.speed
            if self.reflected:
                self.y -= self.speed
        self.timer += 1
        self.rock_sprite = Sprite(3, 3, self.rock, self.x, self.y, key=-1)

        
class Magic:
    def __init__(self, enemy, player_x, player_y):
        self.enemy = enemy
        # self.target_x = player.playerSprite.x + 6
        # self.target_y = player.playerSprite.y + 6
        self.target_x = player_x + 6
        self.target_y = player_y + 6
        self.x = enemy.x + 1
        self.y = enemy.y + 1
        self.dir = (self.target_x - self.x, self.target_y - self.y)
        self.length = (abs(self.dir[0]) + abs(self.dir[1]))
        self.magic_map = bytearray([0,2,0])
        self.magic_map_flash = bytearray([0,0,0])
        self.animation_counter = 0
        self.speed = 2
        self.reflected = False
        self.dir = (self.dir[0] / self.length, self.dir[1] / self.length)

    def move(self):
        self.x = self.x + self.dir[0] * self.speed
        self.y = self.y + self.dir[1] * self.speed
        
        if self.animation_counter == 0:
            self.magic_sprite = Sprite(3, 3, self.magic_map, self.x, self.y, key=1)
            self.animation_counter += 1
        elif self.animation_counter == 1:
            self.magic_sprite = Sprite(3, 3, self.magic_map_flash, self.x, self.y, key=1)
            self.animation_counter -= 1
        
        
class EnemyController: 
    def __init__(self):
        self.enemies = []
        self.loot = []
        self.spawn_counter = 0
        self.spawn_time = 30
        self.enemies_killed = False
        self.animation_counter = 0
        self.animation_length = 8
        self.map_to_display = ()
        self.enemies_used = ()
        
           
    def display_death_sprite(self, enemy):
        
        death_map_1 = bytearray([255,255,255,239,215,239,255,255,255,
            1,1,1,1,1,1,1,1,1])
        death_map_2 = bytearray([255,255,239,215,187,215,239,255,255,
            1,1,1,1,1,1,1,1,1])
          # BITMAP: width: 15, height: 15
        death_map_3 = bytearray([255,239,187,255,125,255,187,239,255,
            1,1,1,1,1,1,1,1,1])
        death_map_4 = bytearray([238,125,255,255,254,255,255,125,238,
            0,1,1,1,0,1,1,1,0])
        
        death_sprite = Sprite(9, 9, death_map_1+death_map_1+death_map_2+death_map_2+death_map_3+death_map_3+death_map_4+death_map_4, enemy.x - 2, enemy.y - 2, key=1)
        death_sprite.setFrame(self.animation_counter)
        display.drawSprite(death_sprite)
        self.animation_counter += 1
    
    
    def check_for_overlap(self, scene_controller, enemy):
        elements = scene_controller.walls + scene_controller.bushes + scene_controller.water + scene_controller.trees + scene_controller.barriers + scene_controller.blocks + scene_controller.locks + scene_controller.pushable_blocks + scene_controller.block_locks
    
        while any(enemy.x < element.x + 5 and enemy.x + 5 > element.x and element.y < enemy.y + 5 and element.y + 5 > enemy.y for element in elements):
            enemy.x = randrange(11, 56, 5)
            enemy.y = randrange(10, 25, 5)
    
        gc.collect()
        
    
    def populate_enemies(self, scene_controller):
        if not self.enemies_killed:
            if self.enemies == []:
                if "enemies" in scene_controller.this_scene:
                    for enemy in scene_controller.this_scene["enemies"]:
                                    
                        if enemy == "octorok":
                            for octorok in scene_controller.this_scene["enemies"][enemy]:
                                enemyx = randrange(11, 56, 5)
                                enemyy = randrange(10, 25, 5)
                                enemy_facingDirection = choice(["up", "down", "left", "right"])
                                enemy_walkDistance = randrange(10, 30)
                                enemy_rocks = []
                                if not octorok in self.enemies_used:
                                    self.enemies.append(Octorok(enemyx, enemyy, enemy_facingDirection, enemy_walkDistance, enemy_rocks, octorok))
                                    gc.collect()
                                    
                        if enemy == "tektite":
                            for tektite in scene_controller.this_scene["enemies"][enemy]:
                                enemyx = randrange(11, 56, 5)
                                enemyy = randrange(10, 25, 5)
                                if not tektite in self.enemies_used:
                                    self.enemies.append(Tektite(enemyx, enemyy, tektite))
                                    gc.collect()
                                    
                        if enemy == "leever":
                            for leever in scene_controller.this_scene["enemies"][enemy]:
                                enemyx = randrange(11, 56, 5)
                                enemyy = randrange(10, 25, 5)
                                if not leever in self.enemies_used:
                                    self.enemies.append(Leever(enemyx, enemyy, leever))
                                    gc.collect()
                                    
                        if enemy == "zora":
                            for zora in scene_controller.this_scene["enemies"][enemy]:
                                spawn_tile = choice(scene_controller.water)
                                x = spawn_tile.x
                                y = spawn_tile.y
                                if not zora in self.enemies_used:
                                    self.enemies.append(Zora(x, y, zora))
                                    gc.collect()
                            
                        if enemy == "stalfos":
                            for stalfos in scene_controller.this_scene["enemies"][enemy]:
                                enemyx = randrange(11, 56, 5)
                                enemyy = randrange(10, 25, 5)
                                enemy_facingDirection = choice(["up", "down", "left", "right"])
                                enemy_walkDistance = randrange(10, 30)
                                if not stalfos in self.enemies_used:
                                    self.enemies.append(Stalfos(enemyx, enemyy, enemy_facingDirection, enemy_walkDistance, stalfos))
                                    gc.collect()
                                    
                        if enemy == "gel":
                            for gel in scene_controller.this_scene["enemies"][enemy]:
                                enemyx = randrange(11, 56, 5)
                                enemyy = randrange(10, 25, 5)
                                enemy_facingDirection = choice(["up", "down", "left", "right"])
                                enemy_walkDistance = 5
                                if not gel in self.enemies_used:
                                    self.enemies.append(Gel(enemyx, enemyy, enemy_facingDirection, enemy_walkDistance, gel))
                                    gc.collect()
                        
                        if enemy == "blade":
                            for blade in scene_controller.this_scene["enemies"][enemy]:
                                if not blade in self.enemies_used:
                                    self.enemies.append(Blade(blade[0], blade[1], blade[2], blade[3], blade[4]))
                                    gc.collect()
                            
                        if enemy == "keese":
                            for keese in scene_controller.this_scene["enemies"][enemy]:
                                if not keese[2] in self.enemies_used:
                                    self.enemies.append(Keese(keese[0], keese[1], keese[2]))
                                    gc.collect()
                                    
                        if enemy == "aquamentus":
                            for boss in scene_controller.this_scene["enemies"][enemy]:
                                if not boss[2] in self.enemies_used:
                                    from bosses import Aquamentus
                                    self.enemies.append(Aquamentus(boss[0], boss[1], boss[2]))
                                    gc.collect()
                            
                        
                    if len(self.enemies) > 0:
                        print(f"Enemies: {len(self.enemies)}")
                        for enemy in self.enemies:
                            if not enemy.enemy_type == "zora" and not enemy.enemy_type == "tektite" and not enemy.enemy_type == "keese" and not enemy.enemy_type == "aquamentus":
                                self.check_for_overlap(scene_controller, enemy)
                            print(enemy.enemy_type)
                    # gc.collect()

    
    def move_enemies(self, scene_controller, player): 
        desired_movement_buffer = 1
        self.map_to_display = ()
        for enemy in self.enemies:
            if enemy.enemy_type == "blade":
                if enemy.x == enemy.starting_x and enemy.y == enemy.starting_y and not enemy.attacking:
                    enemy.distance_count = 0
                if not enemy.attacking:
                    if enemy.x > enemy.starting_x:
                        enemy.x -= 1
                    if enemy.x < enemy.starting_x:
                        enemy.x += 1
                    if enemy.y > enemy.starting_y:
                        enemy.y -= 1
                    if enemy.y < enemy.starting_y:
                        enemy.y += 1
                if not enemy.attacking and enemy.distance_count == 0:
                    if player.playerSprite.x + 4 == enemy.x:
                        enemy.attacking = True
                        if player.playerSprite.y > enemy.y:
                            enemy.attacking_direction = "down"
                        elif player.playerSprite.y < enemy.y:
                            enemy.attacking_direction = "up"
                    elif player.playerSprite.y + 4 == enemy.y:
                        enemy.attacking = True
                        if player.playerSprite.x > enemy.x:
                            enemy.attacking_direction = "right"
                        elif player.playerSprite.x < enemy.x:
                            enemy.attacking_direction = "left"
                        
                    
                if enemy.attacking:
                    if enemy.attacking_direction == "down":
                        if enemy.distance_count < enemy.vertical_move_distance:
                            enemy.y += enemy.move_speed
                            enemy.distance_count += enemy.move_speed
                        elif enemy.distance_count >= enemy.vertical_move_distance:
                            enemy.attacking = False
                            
                    elif enemy.attacking_direction == "up":
                        if enemy.distance_count < enemy.vertical_move_distance:
                            enemy.y -= enemy.move_speed
                            enemy.distance_count += enemy.move_speed
                        elif enemy.distance_count >= enemy.vertical_move_distance:
                            enemy.attacking = False

                    elif enemy.attacking_direction == "right":
                        if enemy.distance_count < enemy.horizontal_move_distance:
                            enemy.x += enemy.move_speed
                            enemy.distance_count += enemy.move_speed
                        elif enemy.distance_count >= enemy.horizontal_move_distance:
                            enemy.attacking = False
                                
                    elif enemy.attacking_direction == "left":
                        if enemy.distance_count < enemy.horizontal_move_distance:
                            enemy.x -= enemy.move_speed
                            enemy.distance_count += enemy.move_speed
                        elif enemy.distance_count >= enemy.horizontal_move_distance:
                            enemy.attacking = False
                self.map_to_display = (enemy.map, 0, 0)
                
            if enemy.enemy_type == "aquamentus":
                enemy.move()
                enemy.spawn_animation_counter += 1
                self.map_to_display = (enemy.prespawn_map, enemy.x, enemy.y)
                
            if enemy.frozen:
                if enemy.freeze_counter < 40:
                    enemy.frozen = True
                    enemy.freeze_counter += 1
                else:
                    enemy.freeze_counter = 0
                    enemy.frozen = False
            if self.spawn_counter < self.spawn_time:
                if not enemy.enemy_type == "blade" and not enemy.enemy_type == "aquamentus":
                    enemy.prespawn = True
                
                if enemy.enemy_type == "zora":
                    if enemy.spawn_animation_counter < 10:
                        self.map_to_display = (enemy.surface_map_1, 0, 0)
                        enemy.spawn_animation_counter += 1
                        self.spawn_counter += 1
                    elif enemy.spawn_animation_counter < 20:
                        self.map_to_display = (enemy.surface_map_2, 0, 0)
                        enemy.spawn_animation_counter += 1
                        self.spawn_counter += 1
                    elif enemy.spawn_animation_counter < 30:
                        self.map_to_display = (enemy.surface_map_3, 0, 0)
                        enemy.spawn_animation_counter += 1
                        self.spawn_counter += 1
                    else:
                        self.map_to_display = (enemy.attack_map, 0, 0)
                        enemy.spawn_animation_counter = 0
                        self.spawn_counter += 1
                else:
                    if not enemy.enemy_type == "blade" and not enemy.enemy_type == "aquamentus":
                        self.map_to_display = (enemy.prespawn_map, 0, 0)
                        self.spawn_counter += 1
                
                if enemy.enemy_type == "leever":
                    if enemy.spawn_animation_counter < 10:
                        self.map_to_display = (enemy.surface_map_1, 0, 0)
                        enemy.spawn_animation_counter += 1
                        self.spawn_counter += 1
                    elif enemy.spawn_animation_counter < 20:
                        self.map_to_display = (enemy.surface_map_2, 0, 0)
                        enemy.spawn_animation_counter += 1
                        self.spawn_counter += 1
                    elif enemy.spawn_animation_counter < 30:
                        self.map_to_display = (enemy.surface_map_3, 0, 0)
                        enemy.spawn_animation_counter += 1
                        self.spawn_counter += 1
                    else:
                        self.map_to_display = (enemy.attacking_map_1, 0, 0)
                        enemy.spawn_animation_counter = 0
                        self.spawn_counter += 1
                else:
                    if not enemy.enemy_type == "zora" and not enemy.enemy_type == "blade" and not enemy.enemy_type == "aquamentus":
                        self.map_to_display = (enemy.prespawn_map, 0, 0)
                        self.spawn_counter += 1
            else:
                enemy.prespawn = False
                
                
                if enemy.enemy_type == "octorok" or enemy.enemy_type == "stalfos" or enemy.enemy_type == "gel":
                    if not enemy.frozen:
                        # if enemy.enemy_type == "gel":
                        #     enemy.walk_distance = 5
                        # else:
                        enemy.walk_distance = randint(15, 25)
                        if enemy.y % 5 == 0 or enemy.x % 5 == 0:
                            if enemy.distance_count >= enemy.walk_distance:
                                enemy.facingDirection = choice(enemy.directions)
                                enemy.distance_count = 0
                            else:
                                if enemy.enemy_type == "gel":
                                    enemy.distance_count += 5
                                else:
                                    enemy.distance_count += 1
                    
                        def check_for_collisions(scene_controller, mod1, mod2, mod3, mod4):
                            enemy.isColliding = False
                            collidables = (scene_controller.walls + scene_controller.bushes +
                                           scene_controller.water + scene_controller.barriers +
                                           scene_controller.blocks + scene_controller.pushable_blocks + scene_controller.block_locks)
                            
                            for obj in collidables:
                                if (((enemy.x < obj.x + mod1) and (enemy.x + mod2 > obj.x)) and
                                    ((obj.y < enemy.y + mod3) and (obj.y + mod4 > enemy.y))):
                                    enemy.isColliding = True
                                    enemy.colliding_wall = obj
                                    break  # Stop checking further if a collision is found

                                
                        if enemy.facingDirection == "up":
                            check_for_collisions(scene_controller, 5, 5, 5, 6)
                            if enemy.isColliding:
                                enemy.y = enemy.colliding_wall.y + 5
                                while enemy.facingDirection == "up":
                                    enemy.facingDirection = choice(enemy.directions)
                                    enemy.isColliding = False
                            elif enemy.y > 5:
                                if enemy.enemy_type == "gel":
                                    if enemy.move_buffer > desired_movement_buffer + randint(10, 30):
                                        if not enemy.isColliding:
                                            enemy.y -= enemy.move_speed
                                            enemy.move_buffer = 0
                                    else:
                                        enemy.move_buffer += 1
                                else:    
                                    if enemy.move_buffer < desired_movement_buffer:
                                        if not enemy.isColliding:
                                            enemy.y -= enemy.move_speed
                                            enemy.move_buffer += 1
                                    else:
                                        enemy.move_buffer = 0
                            else:
                                enemy.facingDirection = choice(enemy.directions)
            
                                
                        elif enemy.facingDirection == "down":
                            check_for_collisions(scene_controller, 5, 5, 6, 5)
                            if enemy.isColliding:
                                enemy.y = enemy.colliding_wall.y - 5
                                while enemy.facingDirection == "down":
                                    enemy.facingDirection = choice(enemy.directions)
                                    enemy.isColliding = False
                            elif enemy.y < 30:
                                if enemy.enemy_type == "gel":
                                    if enemy.move_buffer > desired_movement_buffer + randint(10, 30):
                                        if not enemy.isColliding:
                                            enemy.y += enemy.move_speed
                                            enemy.move_buffer = 0
                                    else:
                                        enemy.move_buffer += 1
                                else:
                                    if enemy.move_buffer < desired_movement_buffer:
                                        if not enemy.isColliding:
                                            enemy.y += enemy.move_speed
                                            enemy.move_buffer += 1
                                    else:
                                        enemy.move_buffer = 0
                            else:
                                enemy.facingDirection = choice(enemy.directions)
            
            
                        elif enemy.facingDirection == "right":
                            check_for_collisions(scene_controller, 5, 6, 5, 5)
                            if enemy.isColliding:
                                enemy.x = enemy.colliding_wall.x - 5
                                while enemy.facingDirection == "right":
                                    enemy.facingDirection = choice(enemy.directions)
                                    enemy.isColliding = False
                            elif enemy.x < 61:
                                if enemy.enemy_type == "gel":
                                    if enemy.move_buffer > desired_movement_buffer + randint(10, 30):
                                        if not enemy.isColliding:
                                            enemy.x += enemy.move_speed
                                            enemy.move_buffer = 0
                                    else:
                                        enemy.move_buffer += 1
                                else:
                                    if enemy.move_buffer < desired_movement_buffer:
                                        if not enemy.isColliding:
                                            enemy.x += enemy.move_speed
                                            enemy.move_buffer += 1
                                    else:
                                        enemy.move_buffer = 0
                            else:
                                enemy.facingDirection = choice(enemy.directions)
            
            
                        elif enemy.facingDirection == "left":
                            check_for_collisions(scene_controller, 6, 5, 5, 5)
                            if enemy.isColliding:
                                enemy.x = enemy.colliding_wall.x  + 5
                                while enemy.facingDirection == "left":
                                    enemy.facingDirection = choice(enemy.directions)
                                    enemy.isColliding = False
                            elif enemy.x > 6:
                                if enemy.enemy_type == "gel":
                                    if enemy.move_buffer > desired_movement_buffer + randint(10, 30):
                                        if not enemy.isColliding:
                                            enemy.x -= enemy.move_speed
                                            enemy.move_buffer = 0
                                    else:
                                        enemy.move_buffer += 1
                                else:
                                    if enemy.move_buffer < desired_movement_buffer:
                                        if not enemy.isColliding:
                                            enemy.x -= enemy.move_speed
                                            enemy.move_buffer += 1
                                    else:
                                        enemy.move_buffer = 0
                            else:
                                enemy.facingDirection = choice(enemy.directions)
        
                    if not enemy.is_dead:
                        if enemy.enemy_type == "stalfos" or enemy.enemy_type == "gel":
                            if enemy.enemy_type == "gel":
                                if enemy.animation_counter >= 6:
                                    self.map_to_display = (enemy.move_map, 0, 0)
                                    enemy.animation_counter = 0
                                else:
                                    self.map_to_display = (enemy.map, 1, 0)
                                    enemy.animation_counter += 1
                            else:
                                if enemy.animation_counter >= 2:
                                    self.map_to_display = (enemy.map, 0, 0)
                                    enemy.animation_counter = 0
                                else:
                                    self.map_to_display = (enemy.map, 1, 0)
                                    enemy.animation_counter += 1
                        else:
                            if enemy.facingDirection == "up" and enemy.move_buffer < 1:
                                self.map_to_display = (enemy.enemy_up_map, 0, 0)
                            elif enemy.facingDirection == "up" and enemy.move_buffer >= 1:
                                self.map_to_display = (enemy.enemy_up_map_2, 0, 0)
                            elif enemy.facingDirection == "right" and enemy.move_buffer < 1:
                                self.map_to_display = (enemy.enemy_right_map, 0, 0)
                            elif enemy.facingDirection == "right" and enemy.move_buffer >= 1:
                                self.map_to_display = (enemy.enemy_right_map_2, 0, 0)
                            elif enemy.facingDirection == "down" and enemy.move_buffer < 1:
                                self.map_to_display = (enemy.enemy_up_map, 0, 1)
                            elif enemy.facingDirection == "down" and enemy.move_buffer >= 1:
                                self.map_to_display = (enemy.enemy_up_map_2, 0, 1)
                            elif enemy.facingDirection == "left" and enemy.move_buffer < 1:
                                self.map_to_display = (enemy.enemy_right_map, 1, 0)
                            elif enemy.facingDirection == "left" and enemy.move_buffer >= 1:
                                self.map_to_display = (enemy.enemy_right_map_2, 1, 0)
                            
                    display.blit(self.map_to_display[0], enemy.x, enemy.y, 5, 5, 1, self.map_to_display[1], self.map_to_display[2])
                    
                if enemy.enemy_type == "tektite":
                    jump_directions = ("left", "right")
                    if enemy.animation_counter >= 10:
                        self.map_to_display = (enemy.extended_map, 0, 0)
                        enemy.animation_counter = 0
                    elif enemy.animation_counter <= 5:
                        self.map_to_display = (enemy.extended_map, 0, 0)
                        enemy.animation_counter += 1
                    else:
                        self.map_to_display = (enemy.crouched_map, 0, 0)
                        enemy.animation_counter += 1
                    if enemy.is_jumping == False:
                        enemy.jump_counter = randint(0, 20)
                        enemy.jump_direction = choice(jump_directions)
                    
                    if self.map_to_display == (enemy.extended_map, 0, 0):
                        if not enemy.frozen:
                            if enemy.jump_counter == 1 and enemy.is_jumping == False:
                                # print(f"is jumping {enemy.jump_direction}")
                                enemy.is_jumping = True
                                enemy.prejump_x = enemy.x
                                enemy.prejump_y = enemy.y
                                enemy.jump_x = randint(7, 14)
                                enemy.jump_y = randint(0, 7)
    
                            if enemy.is_jumping:
                                if enemy.jump_direction == "right" and enemy.x >= enemy.prejump_x + enemy.jump_x:
                                    enemy.is_jumping = False
                                    enemy.apex_reached = False
                                if enemy.jump_direction == "right" and enemy.x < enemy.prejump_x + enemy.jump_x and enemy.x < 66:
                                    enemy.x += 1
                                    if enemy.x >= 66:
                                        enemy.is_jumping = False
                                        enemy.x -= 1
                                if enemy.jump_direction == "left" and enemy.x <= enemy.prejump_x - enemy.jump_x:
                                    enemy.is_jumping = False
                                    enemy.apex_reached = False
                                if enemy.jump_direction == "left" and enemy.x > enemy.prejump_x - enemy.jump_x and enemy.x > 0:
                                    enemy.x -= 1 
                                    if enemy.x <= 0:
                                        enemy.is_jumping = False
                                        enemy.x += 1
                                if enemy.y < enemy.prejump_y - enemy.jump_y or enemy.y <= 5:
                                    enemy.apex_reached = True
                                if enemy.apex_reached == False:
                                    if enemy.y > 5:
                                        enemy.y -= 1
                                elif enemy.apex_reached:
                                    if enemy.y < 35:
                                        enemy.y += 1
                
                if enemy.enemy_type == "zora":
                    if enemy.spawn_animation_counter < 10:
                        self.map_to_display = (enemy.surface_map_1, 0, 0)
                        enemy.spawn_animation_counter += 1
                    elif enemy.spawn_animation_counter < 20:
                        self.map_to_display = (enemy.surface_map_2, 0, 0)
                        enemy.spawn_animation_counter += 1
                    elif enemy.spawn_animation_counter < 30:
                        self.map_to_display = (enemy.surface_map_3, 0, 0)
                        enemy.spawn_animation_counter += 1
                    elif enemy.spawn_animation_counter < 70:
                        self.map_to_display = (enemy.attack_map, 0, 0)
                        enemy.spawn_animation_counter += 1
                    elif enemy.spawn_animation_counter < 80:
                        self.map_to_display = (enemy.surface_map_3, 0, 0)
                        enemy.spawn_animation_counter += 1
                    elif enemy.spawn_animation_counter < 90:
                        self.map_to_display = (enemy.surface_map_2, 0, 0)
                        enemy.spawn_animation_counter += 1
                    elif enemy.spawn_animation_counter < 100:
                        self.map_to_display = (enemy.surface_map_1, 0, 0)
                        enemy.spawn_animation_counter += 1
                        
                # Helper function to check collisions for each direction
                def check_collision(enemy, scene_controller, direction):
                    enemy.isColliding = False
                    collidables = scene_controller.walls + scene_controller.bushes + scene_controller.water
                    
                    for obj in collidables:
                        if direction == "up":
                            if (((enemy.x < obj.x + 5) and (enemy.x + 5 > obj.x)) and 
                                ((obj.y < enemy.y + 5) and (obj.y + 6 > enemy.y))):
                                enemy.isColliding = True
                                enemy.colliding_wall = obj
                                break
                        elif direction == "down":
                            if (((enemy.x < obj.x + 5) and (enemy.x + 5 > obj.x)) and 
                                ((obj.y - 1 < enemy.y + 5) and (obj.y + 5 > enemy.y))):
                                enemy.isColliding = True
                                enemy.colliding_wall = obj
                                break
                        elif direction == "right":
                            if (((enemy.x < obj.x + 5) and (enemy.x + 5 > obj.x - 1)) and 
                                ((obj.y < enemy.y + 5) and (obj.y + 5 > enemy.y))):
                                enemy.isColliding = True
                                enemy.colliding_wall = obj
                                break
                        elif direction == "left":
                            if (((enemy.x < obj.x + 6) and (enemy.x + 5 > obj.x)) and 
                                ((obj.y < enemy.y + 5) and (obj.y + 5 > enemy.y))):
                                enemy.isColliding = True
                                enemy.colliding_wall = obj
                                break
                
                # Main enemy logic
                if enemy.enemy_type == "leever":
                    if enemy.is_buried:
                        if enemy.distance_count >= enemy.walk_distance:
                            enemy.facingDirection = choice(enemy.directions)
                            enemy.distance_count = 0
                        else:
                            enemy.distance_count += 1
                    else:
                        if not enemy.frozen:
                            direction = enemy.facingDirection
                            check_collision(enemy, scene_controller, direction)
                            
                            if direction == "up":
                                if enemy.isColliding:
                                    enemy.y = enemy.colliding_wall.y + 5
                                    enemy.facingDirection = "down"
                                    enemy.isColliding = False
                                elif enemy.y > 5:
                                    if enemy.move_buffer < desired_movement_buffer:
                                        if not enemy.isColliding:
                                            enemy.y -= enemy.move_speed
                                            enemy.move_buffer += 1
                                    else:
                                        enemy.move_buffer = 0
                                else:
                                    enemy.facingDirection = "down"
                            elif direction == "down":
                                if enemy.isColliding:
                                    enemy.y = enemy.colliding_wall.y - 5
                                    enemy.facingDirection = "up"
                                    enemy.isColliding = False
                                elif enemy.y < 30:
                                    if enemy.move_buffer < desired_movement_buffer:
                                        if not enemy.isColliding:
                                            enemy.y += enemy.move_speed
                                            enemy.move_buffer += 1
                                    else:
                                        enemy.move_buffer = 0
                                else:
                                    enemy.facingDirection = "up"
                            elif direction == "right":
                                if enemy.isColliding:
                                    enemy.x = enemy.colliding_wall.x - 5
                                    enemy.facingDirection = "left"
                                    enemy.isColliding = False
                                elif enemy.x < 61:
                                    if enemy.move_buffer < desired_movement_buffer:
                                        if not enemy.isColliding:
                                            enemy.x += enemy.move_speed
                                            enemy.move_buffer += 1
                                    else:
                                        enemy.move_buffer = 0
                                else:
                                    enemy.facingDirection = "left"
                            elif direction == "left":
                                if enemy.isColliding:
                                    enemy.x = enemy.colliding_wall.x + 5
                                    enemy.facingDirection = "right"
                                    enemy.isColliding = False
                                elif enemy.x > 6:
                                    if enemy.move_buffer < desired_movement_buffer:
                                        if not enemy.isColliding:
                                            enemy.x -= enemy.move_speed
                                            enemy.move_buffer += 1
                                    else:
                                        enemy.move_buffer = 0
                                else:
                                    enemy.facingDirection = "right"

                    
                    
                    if enemy.spawn_animation_counter < 10:
                        self.map_to_display = (enemy.surface_map_1, 0, 0)
                        enemy.spawn_animation_counter += 1
                    elif enemy.spawn_animation_counter < 20:
                        self.map_to_display = (enemy.surface_map_2, 0, 0)
                        enemy.spawn_animation_counter += 1
                    elif enemy.spawn_animation_counter < 30:
                        self.map_to_display = (enemy.surface_map_3, 0, 0)
                        enemy.spawn_animation_counter += 1
                    elif enemy.spawn_animation_counter < 40:
                        enemy.is_buried = False
                        self.map_to_display = (enemy.attacking_map_1, 0, 0)
                        enemy.spawn_animation_counter += 1
                    elif enemy.spawn_animation_counter < 45:
                        self.map_to_display = (enemy.attacking_map_2, 0, 0)
                        enemy.spawn_animation_counter += 1
                    elif enemy.spawn_animation_counter < 50:
                        self.map_to_display = (enemy.attacking_map_1, 0, 0)
                        enemy.spawn_animation_counter += 1
                    elif enemy.spawn_animation_counter < 55:
                        self.map_to_display = (enemy.attacking_map_2, 0, 0)
                        enemy.spawn_animation_counter += 1
                    elif enemy.spawn_animation_counter < 60:
                        self.map_to_display = (enemy.attacking_map_1, 0, 0)
                        enemy.spawn_animation_counter += 1
                    elif enemy.spawn_animation_counter < 65:
                        self.map_to_display = (enemy.attacking_map_2, 0, 0)
                        enemy.spawn_animation_counter += 1
                    elif enemy.spawn_animation_counter < 70:
                        enemy.is_buried = True
                        self.map_to_display = (enemy.surface_map_3, 0, 0)
                        enemy.spawn_animation_counter += 1
                    elif enemy.spawn_animation_counter < 80:
                        self.map_to_display = (enemy.surface_map_2, 0, 0)
                        enemy.spawn_animation_counter += 1
                    elif enemy.spawn_animation_counter < 90:
                        self.map_to_display = (enemy.surface_map_1, 0, 0)
                        enemy.spawn_animation_counter += 1
                    elif enemy.spawn_animation_counter < 100:
                        self.map_to_display = (enemy.prespawn_map, 0, 0)
                        enemy.spawn_animation_counter += 1
                        
#############################################################################TEST##############################################################################                

                
                
                if enemy.enemy_type == "keese":
                    if enemy.prespawn:
                        enemy.flight_time = randrange(60, 120)
                        self.map_to_display = (enemy.prespawn_map, enemy.x, enemy.y)
                        
                    if enemy.animation_counter >= enemy.attack_speed:
                        if not enemy.frozen:
                            enemy.is_flying = True
                            enemy.flight_time = randrange(60, 120)
                            xmod = choice([-1, 0, 1])
                            ymod = choice([-1, 0, 1])
                            if xmod > 0 and enemy.x < 66:
                                enemy.x += xmod
                            elif xmod < 0 and enemy.x > 1:
                                enemy.x += xmod
                            if ymod > 0 and enemy.y < 35:
                                enemy.y += ymod
                            elif ymod < 0 and enemy.y > 5:
                                enemy.y += ymod
                            enemy.animation_counter += 1
                            flight_duration = enemy.attack_speed + enemy.flight_time
                            if enemy.animation_counter >= flight_duration:
                                enemy.is_flying = False
                                enemy.animation_counter = 0
                                enemy.flight_time = randrange(60, 120)
                                enemy.attack_speed = randrange(20, 40)
                        if enemy.fly_counter == 0:
                            self.map_to_display = (enemy.flap1_map, enemy.x, enemy.y)
                            enemy.fly_counter = 1
                        else:
                            self.map_to_display = (enemy.flap2_map, enemy.x, enemy.y)
                            enemy.fly_counter = 0
                            
                                
                    else:
                        enemy.animation_counter += 1
                        self.map_to_display = (enemy.prespawn_map, enemy.x, enemy.y)
                        
              
###############################################################################TEST#######################################################################
                
                        
            if enemy.enemy_type == "zora" or enemy.enemy_type == "aquamentus":
                if enemy.spawn_animation_counter >= 100:
                    if not enemy.frozen:
                        enemy.magic = []
                        if enemy.enemy_type == "zora":
                            spawn_tile = choice(scene_controller.water)
                            enemy.x = spawn_tile.x
                            enemy.y = spawn_tile.y
                        enemy.spawn_animation_counter = 0
                        enemy.has_fired = False
                else:
                    display.blit(self.map_to_display[0], enemy.x, enemy.y, 5, 5, -1, self.map_to_display[1], self.map_to_display[2])
            if enemy.enemy_type == "leever":
                if enemy.spawn_animation_counter >= 100:
                    if not enemy.frozen:
                        enemy.x = randrange(11, 56, 5)
                        enemy.y = randrange(10, 25, 5)
                        self.check_for_overlap(scene_controller, enemy)
                        enemy.spawn_animation_counter = 0
                else:
                    display.blit(self.map_to_display[0], enemy.x, enemy.y, 5, 5, 1, self.map_to_display[1], self.map_to_display[2])
            if enemy.enemy_type == "aquamentus":
                display.blitWithMask(self.map_to_display[0], enemy.x, enemy.y, 10, 10, 1, self.map_to_display[1], self.map_to_display[2], enemy.prespawn_mask)
            else:
                display.blit(self.map_to_display[0], enemy.x, enemy.y, 5, 5, 1, self.map_to_display[1], self.map_to_display[2])

            
    def attack(self, player):
        for enemy in self.enemies:
            if enemy.prespawn == False:
                if not enemy.frozen:
                    if enemy.enemy_type == "octorok":
                        enemy.attack_counter = randint(0, 200)
                        if enemy.attack_counter >= enemy.attack_speed:
                            enemy.move_speed = 0
                            if enemy.rocks == []:
                                enemy.rocks.append(Rock(enemy))
                                
                        for rock in enemy.rocks:
                            rock.move()
                            display.drawSprite(rock.rock_sprite)
                            if rock.timer > rock.lifespan:
                                rock.parent_enemy.move_speed = 1
                                rock_index = enemy.rocks.index(rock)
                                del enemy.rocks[rock_index]
                                rock.timer = 0
                                
                    if enemy.enemy_type == "zora" or enemy.enemy_type == "aquamentus":
                        if not enemy.has_fired:
                            if enemy.spawn_animation_counter >= 40:
                                if enemy.magic == []:
                                    if enemy.enemy_type == "aquamentus":
                                        enemy.magic.append(Magic(enemy, player.playerSprite.x - 5, player.playerSprite.y))
                                        enemy.magic.append(Magic(enemy, player.playerSprite.x - 5, player.playerSprite.y + 15))
                                        enemy.magic.append(Magic(enemy, player.playerSprite.x - 5, player.playerSprite.y - 15))
                                    else:
                                        enemy.magic.append(Magic(enemy, player.playerSprite.x, player.playerSprite.y))
                            for magic in enemy.magic:
                                magic.move()
                                display.drawSprite(magic.magic_sprite)
                                
                    
       
                    
    def display_loot(self, my_player, enemy_controller, display):
        for loot in self.loot:
            this_loot_index = self.loot.index(loot)
            if not loot.destroyed:
                loot.display_loot(display)
            elif loot.destroyed:
                loot.destroyed = False
                loot_index = self.loot.index(loot)
                del self.loot[loot_index]
        if len(self.loot) == 0:
            self.loot = []
            
        for loot in self.loot:
            if (((my_player.playerSprite.x + 4 < loot.x + 5) and (my_player.playerSprite.x + 9 > loot.x)) and ((loot.y < my_player.playerSprite.y + 9) and (loot.y + 5 > my_player.playerSprite.y + 4))):
                loot_index = enemy_controller.loot.index(loot)
                if loot.loot_type == "heart" and my_player.hearts >= my_player.max_hearts:
                    del self.loot[loot_index]
                if loot.loot_type == "heart" and my_player.hearts == my_player.max_hearts - 1:
                    del self.loot[loot_index]
                    my_player.hearts += 1
                if loot.loot_type == "heart" and my_player.hearts <= my_player.max_hearts - 2:
                    del self.loot[loot_index]
                    my_player.hearts += 2
                if loot.loot_type == "rupee" and my_player.rupees < 999:
                    del self.loot[loot_index]
                    my_player.rupees += 1
                    my_player.rupees_text = str(my_player.rupees)
                if loot.loot_type == "bigrupee" and my_player.rupees < 994:
                    del self.loot[loot_index]
                    my_player.rupees += 5
                    my_player.rupees_text = str(my_player.rupees)
                if loot.loot_type == "bomb" and my_player.bombs < 9:
                    del self.loot[loot_index]
                    my_player.bombs += 1
                    my_player.bombs_text = str(my_player.bombs)
                else:
                    loot.destroyed = True

