from thumby import Sprite, display
import gc
from sys import path
path.append("/Games/Thelda")
from random import choice, randrange, randint


class Aquamentus:
    def __init__(self, x, y, identity):
        self.identity = identity
        self.enemy_type = "aquamentus"
        self.x = x
        self.y = y
        self.damage = 1
        self.starting_health = 6
        self.health = 6
        self.frozen = False
        self.is_dead = False
        self.attack_speed = 199
        self.magic = []
        self.prespawn = False
        self.walk_distance = 0
        self.direction = -1
        self.blank_map = bytearray([255,255,255,255,255,255,255,255,255,255,
           3,3,3,3,3,3,3,3,3,3])
        self.prespawn_map = bytearray([25,233,242,252,224,222,95,219,231,15,
           3,0,1,2,2,2,2,0,1,2])
        self.prespawn_mask = bytearray([230,246,255,255,255,225,224,228,248,240,
           0,1,3,1,1,1,1,3,3,1])
        self.has_fired = False
        self.pick_new_direction_and_distance()
        self.move_tick = 0
        self.spawn_animation_counter = 0

    def pick_new_direction_and_distance(self):
        self.direction = choice([-1, 1])
        self.walk_distance = randint(1, 6)
        self.target_x = self.x + self.direction * self.walk_distance
        if self.direction == -1:
            self.target_x = max(35, self.target_x)
        else:
            self.target_x = min(55, self.target_x)

    def move(self):
        # Move every 4 ticks
        if self.move_tick == 0:
            if self.direction == -1:
                self.x = max(35, self.x - 1)
            else:
                self.x = min(55, self.x + 1)
            
            if self.x == self.target_x or (self.direction == -1 and self.x == 35) or (self.direction == 1 and self.x == 55):
                self.pick_new_direction_and_distance()

        self.move_tick = (self.move_tick + 1) % 4
            
    