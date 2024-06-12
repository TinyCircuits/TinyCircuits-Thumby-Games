import gc
from sys import path
path.append("/Games/Thelda")


class T:
    __slots__ = ("x", "y")
    def __init__(self, x, y):
        self.x = x
        self.y = y
        
class Door:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.cave_door = bytearray([0, 0, 0, 0, 0])
        
class Block:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        
class Key:
    def __init__(self, x, y, is_solo, identity, scenestring, conditional):
        self.key = bytearray([31,13,2,29,31])
        self.identity = identity
        self.x = x
        self.y = y
        self.solo = is_solo
        self.carried = False
        self.home_scene = scenestring
        self.conditional = conditional
        

class SceneController:
    def __init__(self):
        
        self.scene_x = 8
        self.scene_y = 0
        self.wall = bytearray([8,22,5,26,4])
        self.water_tile = bytearray([7,26,31,11,28])
        self.bush = bytearray([17,14,14,4,1])
        self.bridge_tile = bytearray([65,93,65,93,65])
        self.tree_tile = bytearray([30,29,0,0,23])
        self.sand_tile = bytearray([0])
        self.walls = []
        self.water = []
        self.bushes = []
        self.doors = []
        self.sprites = []
        self.items = []
        self.slopes = []
        self.bridges = []
        self.sand = []
        self.trees = []
        self.barriers = []
        self.doorways = []
        self.stairs = []
        self.locks = []
        self.keys = []
        self.blocks = []
        self.frame_timer = 0
        self.frame_delay = 0
        self.is_still_here = False
        self.is_dungeon = False
        self.in_dungeon = False
        self.built = False
        self.isDangerous = True
        self.doors_unlocked = []
        self.keys_used = []
        self.key_assigned = False
        print(f"Items:{len(self.items)}")

    
    def build_scene(self, x, y, font_handler, display, enemy_controller):
        # BITMAP: width: 35, height: 18
        # BITMAP: width: 35, height: 18
        # self.dungeon_wall = bytearray([0,252,250,246,14,238,238,236,226,238,238,238,238,236,226,238,238,238,238,236,226,238,238,238,238,236,226,238,238,238,236,224,238,238,238,
        #     0,158,189,189,0,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,
        #     0,3,3,3,0,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3])
        self.dungeon_wall = bytearray([0,252,250,246,14,238,238,236,226,238,238,238,238,236,226,238,238,238,238,236,226,238,238,238,238,236,226,238,238,238,236,226,238,238,238,
          0,222,189,189,0,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,
          0,3,3,3,0,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3])
            
        if not self.built:
            self.scene_string = f"scene {x},{y}"
            scene_modules = {
                1: 'scenes1',
                2: 'scenes2',
                3: 'scenes3',
                4: 'scenes4',
                5: 'scenes5',
                6: 'scenes6',
                7: 'scenes7',
                8: 'scenes8',
                9: 'scenes9',
                10: 'scenes10',
                11: 'scenes11',
                12: 'scenes12',
                13: 'scenes13',
            }
            
            abs_x = abs(x)
            if abs_x in scene_modules:
                module_name = scene_modules[abs_x]
                module = __import__(module_name)
                scenes_class = getattr(module, f"Scenes{abs_x}")
                self.this_scene = scenes_class().scenes[self.scene_string]
            elif x < -20:
                from dungeons1 import Scenes80
                self.this_scene = Scenes80().scenes[self.scene_string]


            if "dungeon" in self.this_scene:
                self.is_dungeon = True
            if self.walls == []:
                if "walls" in self.this_scene:
                    for wall in self.this_scene["walls"]:
                        self.walls.append(T(wall[0], wall[1]))
                    if len(self.walls) > 0:
                        print(f"Walls:{len(self.walls)}")
            if self.barriers == []:
                if "barriers" in self.this_scene:
                    for barrier in self.this_scene["barriers"]:
                        self.barriers.append(T(barrier[0], barrier[1]))
                    if len(self.barriers) > 0:
                        print(f"Barriers:{len(self.barriers)}")
            if self.water == []:
                if "water" in self.this_scene:
                    for water in self.this_scene["water"]:
                        self.water.append(T(water[0], water[1]))
                    if len(self.water) > 0:
                        print(f"Water:{len(self.water)}")
            if self.bridges == []:
                if "bridges" in self.this_scene:
                    for bridge in self.this_scene["bridges"]:
                        self.bridges.append(T(bridge[0], bridge[1]))
                    if len(self.bridges) > 0:
                        print(f"Bridges:{len(self.bridges)}")
            if self.sand == []:
                if "sand" in self.this_scene:
                    for sand in self.this_scene["sand"]:
                        self.sand.append(T(sand[0], sand[1]))
                    if len(self.sand) > 0:
                        print(f"Sand:{len(self.sand)}")
            if self.doors == []:
                if "doors" in self.this_scene:
                    for door in self.this_scene["doors"]:
                        self.doors.append(Door(door[0], door[1]))
                    if len(self.doors) > 0:
                        print(f"Doors:{len(self.doors)}")
            if self.stairs == []:
                if "stairs" in self.this_scene:
                    for stairs in self.this_scene["stairs"]:
                        self.stairs.append(T(stairs[0], stairs[1]))
                    if len(self.doors) > 0:
                        print(f"Doors:{len(self.doors)}")
            if self.bushes == []:
                if "bushes" in self.this_scene:
                    for bush in self.this_scene["bushes"]:
                        self.bushes.append(T(bush[0], bush[1]))
                    if len(self.bushes) > 0:
                        print(f"Bushes:{len(self.bushes)}")
            if self.sprites == []:
                if "sprites" in self.this_scene:
                    for sprite in self.this_scene["sprites"]:
                        self.sprites.append(sprite)
                    if len(self.sprites) > 0:
                        print(f"Sprites:{len(self.sprites)}")
            if self.items == []:
                if "items" in self.this_scene:
                    for item in self.this_scene["items"]:
                        if not item.item_type == "sword":
                            self.items.append(item)
                        else:
                            if self.isDangerous:
                                self.items.append(item)
                    if len(self.items) > 0:
                        print(f"Items:{len(self.items)}")
            if self.trees == []:
                if "trees" in self.this_scene:
                    for tree in self.this_scene["trees"]:
                        self.trees.append(T(tree[0], tree[1]))
                    if len(self.trees) > 0:
                        print(f"Trees:{len(self.trees)}")
            if self.doorways == []:
                if "doorways" in self.this_scene:
                    for doorway in self.this_scene["doorways"]:
                        self.doorways.append(doorway)
            if self.locks == []:
                if "locks" in self.this_scene:
                    for lock in self.this_scene["locks"]:
                        if not lock.identity in self.doors_unlocked:
                            self.locks.append(lock)
            # if self.keys == []:
            if "keys" in self.this_scene:
                for key in self.this_scene["keys"]:
                    if not key[3] in self.keys_used:
                        self.keys.append(Key(key[0], key[1], key[2], key[3], self.scene_string, key[4]))
            if self.blocks == []:
                if "blocks" in self.this_scene:
                    for block in self.this_scene["blocks"]:
                        self.blocks.append(Block(block[0], block[1]))
                        
            gc.collect()
                        
            self.built = True
        if "null" in self.this_scene:
            font_handler.write("under", 26, 17)
            font_handler.write("construction", 11, 22)
                
        # Top and side black bars.  Yes... side. 70px works better than 72 for my 5x5 tiles
        display.drawLine(0, 0, 0, 39, 0)
        display.drawLine(71, 0, 71, 39, 0)
        for wall in self.walls:
            display.blit(self.wall, wall.x, wall.y, 5, 5, -1, 0, 0)
        for water in self.water:
            display.blit(self.water_tile, water.x, water.y, 5, 5, -1, 0, 0)
        for bridge in self.bridges:
            display.blit(self.bridge_tile, bridge.x, bridge.y - 1, 5, 7, -1, 0, 0)
        for sand in self.sand:
            display.blit(self.sand_tile, sand.x, sand.y, 1, 1, -1, 0, 0)
        for slope in self.slopes:
            display.blit(slope.slope, slope.x, slope.y, 5, 5, -1, 0, 0)
        for door in self.doors:
            display.blit(door.cave_door, door.x, door.y, 5, 5, -1, 0, 0)
        for stairs in self.stairs:
            display.blit(bytearray([15,0,14,0,12]), stairs.x, stairs.y, 5, 5, -1, 0, 0)
        for bush in self.bushes:
            if not self.in_dungeon:
                display.blit(self.bush, bush.x, bush.y, 5, 5, -1, 0, 0)
            else:
                display.blit(bytearray([10,21,10,21,10]), bush.x, bush.y, 5, 5, -1, 0, 0)
        for item in self.items:
            display.blit(item.item, item.x, item.y, 5, 5, -1, 0, 0)
        for tree in self.trees:
            display.blit(self.tree_tile, tree.x, tree.y, 5, 5, -1, 0, 0)
        for key in self.keys:
            if key.home_scene == self.scene_string:
                if key.solo:
                    if not key.conditional:
                        display.blit(key.key, key.x, key.y, 5, 5, -1, 0, 0)
                    else:
                        if enemy_controller.enemies == [] and not key.identity in self.keys_used:
                            display.blit(key.key, key.x, key.y, 5, 5, -1, 0, 0)
                else:
                    if not self.key_assigned:
                        if not len(enemy_controller.enemies) == 0:
                            self.keyholder = enemy_controller.enemies[0]
                            self.key_assigned = True
                            key.carried = True
                        else:
                            key.carried = False
                            display.blit(key.key, key.x, key.y, 5, 5, -1, 0, 0)
                    else:    
                        if self.keyholder in enemy_controller.enemies:
                            key.x = self.keyholder.x
                            key.y = self.keyholder.y
                            display.blit(key.key, self.keyholder.x, self.keyholder.y, 5, 5, -1, 0, 0)
                        else:
                            key.carried = False
                            display.blit(key.key, key.x, key.y, 5, 5, -1, 0, 0)
                        
        if self.in_dungeon:
            display.blit(self.dungeon_wall, 1, 5, 35, 18, 1, 0, 0)
            display.blit(self.dungeon_wall, 36, 5, 35, 18, 1, 1, 0)
            display.blit(self.dungeon_wall, 1, 22, 35, 18, 1, 0, 1)
            display.blit(self.dungeon_wall, 36, 22, 35, 18, 1, 1, 1)
            
            for doorway in self.doorways:
                display.blit(doorway.doorway, doorway.x, doorway.y, doorway.size_x, 5, 0, 0, 0)
                
            for lock in self.locks:
                display.blit(lock.lock, lock.x, lock.y, lock.size_x, 5, 1, 0, 0)
                
            for block in self.blocks:
                display.blit(bytearray([0,14,6,2,0]), block.x, block.y, 5, 5, 1, 0, 0)
            
        
        for sprite in self.sprites:
            if self.scene_x == -7 and self.scene_y == 1 and is_dangerous:
                self.is_still_here = True
            elif self.scene_x == -7 and self.scene_y == 1 and not is_dangerous:  # and not self.is_still_here:  # Makes Old Man and text not disappear when sword is taken.  Unsure if I like it.
                self.this_scene["sprites"][0].y -= 40
                self.this_scene["sprites"][1].y -= 40
                        
            if self.frame_delay > 10:
                sprite.setFrame(self.frame_timer)
                display.drawSprite(sprite)
                self.frame_timer += 1
                self.frame_delay = 0
            else:
                self.frame_delay += 1
                display.drawSprite(sprite)
                
    def clear_scene(self, enemy_controller):
        self.walls = []
        self.water = []
        self.bridges = []
        self.sand = []
        self.bushes = []
        self.doors = []
        self.stairs = []
        self.sprites = []
        self.items = []
        self.slopes = []
        self.barriers = []
        self.trees = []
        self.doorways = []
        self.locks = []
        self.blocks = []
        self.key_assigned = False
        for enemy in enemy_controller.enemies:
            if enemy.enemy_type == "zora":
                for magic in enemy.magic:
                    enemy.magic.remove(magic)
        enemy_controller.enemies = []
        enemy_controller.loot = []
        enemy_controller.spawn_counter = 0
        # if not self.in_dungeon:
        enemy_controller.enemies_killed = False
        self.this_scene = None
        gc.collect()
        self.built = False
    
        
# Full Room Template
# "walls": [(1, 5), (6, 5), (11, 5), (16, 5), (21, 5), (26, 5), (31, 5), (36, 5), (41, 5), (46, 5), (51, 5), (56, 5), (61, 5), (66, 5), 
# (1, 35), (6, 35), (11, 35), (16, 35), (21, 35), (26, 35), (31, 35), (36, 35), (41, 35), (46, 35), (51, 35), (56, 35), (61, 35), (66, 35), 
# (1, 10), (6, 10), (11, 10), (16, 10), (21, 10), (26, 10), (31, 10), (36, 10), (41, 10), (46, 10), (51, 10), (56, 10), (61, 10), (66, 10),
# (1, 15), (6, 15), (11, 15), (16, 15), (21, 15), (26, 15), (31, 15), (36, 15), (41, 15), (46, 15), (51, 15), (56, 15), (61, 15), (66, 15),
# (1, 20), (6, 20), (11, 20), (16, 20), (21, 20), (26, 20), (31, 20), (36, 20), (41, 20), (46, 20), (51, 20), (56, 20), (61, 20), (66, 20),
# (1, 25), (6, 25), (11, 25), (16, 25), (21, 25), (26, 25), (31, 25), (36, 25), (41, 25), (46, 25), (51, 25), (56, 25), (61, 25), (66, 25),
# (1, 30), (6, 30), (11, 30), (16, 30), (21, 30), (26, 30), (31, 30), (36, 30), (41, 30), (46, 30), (51, 30), (56, 30), (61, 30), (66, 30)],
                