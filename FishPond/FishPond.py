#### !!!! BLOCKLY EXPORT !!!! ####
import time
from thumbySprite import Sprite
from thumbyGraphics import display
import thumbyButton as buttons
from thumbySaves import saveData
Number = int
import random
from thumbyAudio import audio

counter = None
river_birds = None
bobber_idle = None
title = None
rand_seed = None
can_catch = None
bobber_nibble = None
bobber_bite = None
fish1 = None
river_bg = None
cast_pwr = None
rand_wait = None
rand_nibbles = None
cast_anim = None
cast_anim_fin = None
exclm_point = None
caught_fish_size = None
cast_direction = None
display_qty = None
draw_fishingline_x = None
draw_fishingline_y = None

# Set random seed based on ms
def setup_rand():
  global counter, river_birds, bobber_idle, title, rand_seed, can_catch, bobber_nibble, bobber_bite, fish1, river_bg, cast_pwr, rand_wait, rand_nibbles, cast_anim, cast_anim_fin, exclm_point, caught_fish_size, cast_direction, display_qty, draw_fishingline_x, draw_fishingline_y
  rand_seed = int(time.ticks_ms())
  exec('random.seed(rand_seed)')

title = Sprite(1,1,bytearray([1]))

river_bg = Sprite(1,1,bytearray([1]))

river_birds = Sprite(1,1,bytearray([1]))

bobber_idle = Sprite(1,1,bytearray([1]))

cast_anim = Sprite(1,1,bytearray([1]))

cast_anim_fin = Sprite(1,1,bytearray([1]))

bobber_nibble = Sprite(1,1,bytearray([1]))

bobber_bite = Sprite(1,1,bytearray([1]))

fish1 = Sprite(1,1,bytearray([1]))

exclm_point = Sprite(1,1,bytearray([1]))

# Load all the sprites...
def setup_sprites():
  global counter, river_birds, bobber_idle, title, rand_seed, can_catch, bobber_nibble, bobber_bite, fish1, river_bg, cast_pwr, rand_wait, rand_nibbles, cast_anim, cast_anim_fin, exclm_point, caught_fish_size, cast_direction, display_qty, draw_fishingline_x, draw_fishingline_y
  title = Sprite(72,40,bytearray([0,0,64,64,64,160,32,32,16,16,8,8,4,4,130,0,0,0,0,0,0,0,0,136,120,0,0,0,0,0,0,0,8,8,8,8,232,200,16,16,16,16,16,16,16,96,128,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,64,192,0,0,0,
             0,0,0,0,255,255,16,16,8,8,0,0,200,56,0,0,24,20,36,196,0,0,192,63,8,4,4,248,0,0,0,0,0,0,0,252,255,3,8,8,8,16,16,16,8,132,67,64,64,128,0,0,32,224,64,32,32,32,192,0,128,64,32,32,32,64,224,30,1,0,0,0,
             0,0,8,8,11,11,8,8,8,8,8,8,9,9,8,4,5,5,5,4,4,5,5,4,4,4,5,5,4,0,0,0,0,0,47,47,32,32,32,32,32,32,32,32,35,36,40,40,40,164,35,64,78,73,64,64,64,78,73,64,67,68,72,72,72,92,83,64,64,0,0,0,
             0,0,0,120,20,120,0,0,40,0,0,0,0,0,0,72,84,36,0,4,124,4,0,120,20,120,0,124,20,104,0,4,124,4,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,2,1,0,32,82,37,2,240,8,8,40,12,10,10,18,110,192,0,128,128,64,192,0,
             0,0,0,31,21,26,0,0,10,0,0,0,0,0,0,18,21,9,0,31,21,17,0,1,31,1,0,1,31,1,0,0,31,0,0,31,14,31,0,14,17,29,0,18,21,9,0,0,0,0,0,0,0,0,0,0,1,2,12,20,28,20,4,4,4,3,7,24,96,60,3,0]), title.x,title.y,title.key,title.mirrorX,title.mirrorY)
  river_bg = Sprite(72,40,bytearray([255,255,255,255,255,254,252,252,56,112,96,232,212,170,85,170,87,172,216,112,80,96,64,0,4,136,72,80,32,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,128,128,128,128,64,64,64,32,32,32,32,32,16,16,16,24,136,136,72,64,255,255,255,255,255,254,253,253,248,242,229,202,213,170,85,170,85,170,117,235,86,108,88,40,48,1,1,130,196,40,48,32,0,0,0,0,0,0,0,0,0,192,32,16,72,132,196,98,34,17,9,9,8,8,136,132,132,4,2,2,2,2,1,129,65,33,1,1,128,64,32,16,255,255,255,255,255,251,243,231,207,207,159,43,87,47,79,172,73,170,85,170,85,186,110,172,68,196,128,128,8,11,4,132,128,128,64,64,32,96,144,144,16,59,36,200,80,80,49,18,12,0,0,0,32,25,0,0,192,48,0,0,1,129,65,32,16,8,4,3,0,0,0,0,255,255,255,223,191,31,63,31,63,191,127,63,127,127,254,124,249,242,69,27,31,10,14,5,5,5,154,226,66,33,49,17,17,10,12,12,4,4,2,2,3,1,1,32,32,16,16,16,136,4,0,0,64,64,56,6,1,0,128,112,15,0,56,68,196,68,56,128,128,64,64,32,255,255,255,127,127,127,255,255,255,255,62,126,126,252,252,56,56,120,112,98,98,2,2,2,1,1,0,128,64,0,0,0,16,8,4,2,2,0,16,8,4,4,4,130,130,65,65,33,32,16,8,0,0,224,24,4,2,1,0,0,8,4,4,202,63,201,11,12,0,0,0,0,255,255,255,255,255,254,252,252,56,112,96,232,212,170,85,170,87,172,216,112,80,96,64,0,4,136,72,80,32,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,128,128,128,128,64,64,64,32,32,32,32,32,16,16,16,24,136,136,72,64,255,255,255,255,255,254,253,253,248,242,229,202,213,170,85,170,85,170,117,235,86,108,88,40,48,1,1,130,196,40,48,32,0,0,0,0,0,0,0,0,0,192,32,16,72,132,196,98,34,17,9,9,8,8,8,4,132,4,2,2,2,130,65,33,33,33,1,1,128,64,32,16,255,255,255,255,255,251,243,231,207,207,159,43,87,47,79,172,73,170,85,170,85,186,110,172,68,196,128,128,8,11,4,132,128,128,64,64,32,96,144,144,16,59,36,200,80,80,49,18,12,0,0,0,48,9,1,225,16,16,0,0,1,128,64,32,16,8,4,3,0,0,0,0,255,255,255,223,191,31,63,31,63,191,127,63,127,127,254,124,249,242,69,27,31,10,14,5,5,5,154,226,66,33,49,17,17,10,12,12,4,4,2,2,3,1,1,32,16,8,8,8,4,132,0,0,96,28,3,0,0,0,128,112,15,0,56,68,196,68,56,128,128,64,64,32,255,255,255,127,127,127,255,255,255,255,62,126,126,252,252,56,56,120,112,98,98,2,2,2,1,1,128,64,0,0,0,16,16,8,4,2,0,0,0,16,8,8,8,132,68,34,34,18,17,8,8,0,0,224,24,4,2,1,0,0,8,4,4,202,63,201,11,12,0,0,0,0]),river_bg.x,river_bg.y,river_bg.key,river_bg.mirrorX,river_bg.mirrorY)
  river_birds = Sprite(12,6,bytearray([8,16,32,16,8,0,0,4,2,4,2,4,32,16,32,16,32,0,0,1,2,4,2,1]),river_birds.x,river_birds.y,river_birds.key,river_birds.mirrorX,river_birds.mirrorY)
  bobber_idle = Sprite(72,40,bytearray([0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,128,128,64,64,64,64,32,32,32,16,16,16,8,8,4,4,4,2,2,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,2,0,2,2,1,1,2,6,4,4,0,0,0,0,0,0,0,0,0,0,128,224,240,240,248,248,252,252,253,252,252,248,248,240,240,224,128,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,16,16,16,16,32,32,32,16,16,16,32,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,128,190,207,143,143,31,31,31,63,63,63,63,63,63,31,159,143,143,207,190,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,1,1,0,0,0,1,1,2,2,2,3,1,1,1,1,1,1,0,0,0,1,1,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,2,2,1,1,1,1,2,2,2,2,0,2,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,128,128,128,128,64,64,64,32,32,32,16,16,8,8,8,4,4,2,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,2,0,2,2,4,4,2,2,1,1,0,0,0,0,0,0,0,0,0,0,0,0,192,224,224,240,240,248,248,250,249,249,240,240,224,224,192,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,32,0,32,32,32,16,16,16,32,32,32,16,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,128,252,159,159,31,63,63,63,127,127,127,127,127,127,63,63,159,159,159,252,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,0,0,0,0,1,1,1,1,1,1,2,2,2,2,2,1,0,0,0,1,1,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,2,2,4,4,4,4,2,2,2,2,0,2,0,0,0,0,0,0,0,0,0,0,0,0]),bobber_idle.x,bobber_idle.y,bobber_idle.key,bobber_idle.mirrorX,bobber_idle.mirrorY)
  cast_anim = Sprite(32,37,bytearray([0,0,128,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,2,7,2,1,6,8,16,96,128,0,0,0,0,48,72,132,132,132,72,48,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,6,8,24,104,172,66,255,66,124,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,253,3,28,224,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,16,31,0,0,17,30,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,8,28,8,0,248,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,63,192,48,72,132,132,132,72,48,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,15,248,108,70,255,50,12,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,252,3,28,224,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,16,31,0,0,17,30,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,2,199,50,12,2,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,192,240,76,135,132,132,72,48,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,12,3,0,1,14,18,255,10,4,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,252,3,28,224,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,16,31,0,0,17,30,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,128,128,64,64,32,32,144,208,128,0,0,0,0,0,0,0,0,0,64,64,32,224,240,72,132,132,132,76,50,2,1,1,0,0,0,0,0,0,0,1,0,0,0,0,0,0,0,0,0,0,0,0,7,5,31,20,10,255,6,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,252,3,28,224,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,16,31,0,0,17,30,0,0,0,0,0,0,0,0,0,0,0,0]),cast_anim.x,cast_anim.y,cast_anim.key,cast_anim.mirrorX,cast_anim.mirrorY)
  cast_anim_fin = Sprite(32,37,bytearray([64,128,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,
             0,0,3,4,8,48,64,128,0,0,0,0,0,48,72,132,132,132,72,48,0,0,0,0,0,0,0,0,0,0,0,0,
             0,0,0,0,0,0,0,0,3,4,8,48,120,168,36,34,255,34,60,0,0,0,0,0,0,0,0,0,0,0,0,0,
             0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,252,3,28,224,0,0,0,0,0,0,0,0,0,0,0,0,0,
             0,0,0,0,0,0,0,0,0,0,0,0,0,0,16,31,0,0,17,30,0,0,0,0,0,0,0,0,0,0,0,0]), cast_anim_fin.x,cast_anim_fin.y,cast_anim_fin.key,cast_anim_fin.mirrorX,cast_anim_fin.mirrorY)
  bobber_nibble = Sprite(72,40,bytearray([0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,128,128,64,64,32,32,16,16,8,8,4,4,2,2,1,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,2,0,2,2,1,1,2,6,4,4,0,0,0,0,0,0,0,0,0,0,0,128,192,192,224,224,240,240,244,244,242,226,225,193,192,128,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,16,16,16,16,32,32,32,16,16,16,32,0,0,0,0,0,0,0,0,0,0,32,32,16,16,16,8,8,0,0,0,72,16,128,252,190,191,191,255,255,255,255,255,255,255,255,255,255,255,191,191,190,248,0,64,32,0,8,8,8,16,16,0,0,0,0,64,128,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,16,16,16,17,17,33,32,32,32,32,32,0,1,1,1,33,33,33,33,33,33,32,32,32,33,17,17,17,16,16,16,16,8,8,8,4,4,4,2,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,2,2,1,1,1,1,2,2,2,2,0,2,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,128,128,64,64,32,32,16,8,8,4,4,2,2,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,2,0,2,2,4,4,2,2,1,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,128,128,192,192,208,200,200,132,132,2,2,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,32,0,32,32,32,16,16,16,32,32,32,16,0,0,0,0,0,0,0,0,0,32,16,16,8,8,8,4,4,0,0,32,36,12,128,224,248,254,255,255,255,255,255,255,255,255,255,255,255,255,255,254,248,224,0,0,32,48,16,0,0,0,0,0,0,0,0,0,64,128,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,32,32,33,33,33,32,64,64,64,65,65,1,1,1,1,67,67,67,67,67,65,65,65,65,33,35,34,34,32,32,32,32,16,16,16,8,8,8,4,2,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,2,2,4,4,4,4,2,2,2,2,0,2,0,0,0,0,0,0,0,0,0,0,0,0]),bobber_nibble.x,bobber_nibble.y,bobber_nibble.key,bobber_nibble.mirrorX,bobber_nibble.mirrorY)
  bobber_bite = Sprite(72,40,bytearray([0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,128,64,32,16,8,4,2,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,2,0,2,2,1,1,2,6,4,4,0,0,0,0,0,0,0,0,128,128,128,128,128,128,128,128,128,128,128,128,128,128,0,0,0,0,128,64,32,16,8,4,2,1,0,0,0,0,0,0,0,0,0,0,0,0,0,16,16,16,16,32,32,32,16,16,16,32,0,0,128,192,192,192,192,192,192,192,192,192,192,192,192,128,16,17,17,1,1,1,0,0,0,12,28,28,60,120,224,12,156,64,32,144,200,100,50,49,56,24,0,0,16,17,17,17,18,34,34,2,2,4,4,132,8,8,16,16,32,32,64,0,0,0,0,0,0,0,0,0,0,0,255,255,192,192,255,255,192,192,255,255,192,192,255,255,0,0,32,32,32,32,64,64,64,64,64,64,0,2,3,3,67,66,66,64,64,66,66,70,68,64,32,32,32,32,32,32,32,16,16,16,8,8,8,4,3,0,0,0,0,128,64,48,8,0,0,0,0,0,0,0,0,0,7,15,12,12,15,15,12,12,15,15,12,12,15,7,16,16,16,16,16,16,32,32,32,32,32,32,32,32,32,32,32,32,32,32,32,32,32,32,32,32,0,16,16,16,16,16,0,0,8,8,8,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,128,96,16,8,4,2,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,2,0,2,2,4,4,2,2,1,1,0,0,0,0,128,128,128,128,128,128,128,128,128,128,64,64,64,64,64,64,64,64,64,0,0,0,128,64,32,16,8,4,130,129,128,0,0,0,0,0,0,0,0,0,0,0,0,32,0,32,32,32,16,16,16,32,32,32,16,0,0,128,192,192,192,192,192,192,192,192,192,208,208,208,136,8,8,0,0,0,0,0,8,28,28,28,24,56,48,1,7,142,64,32,16,8,6,49,24,28,14,14,4,0,8,8,16,17,17,17,1,1,2,2,2,132,4,8,8,16,16,32,64,0,0,0,0,0,0,0,0,0,0,255,255,192,192,255,255,192,192,255,255,192,192,255,255,0,0,64,64,64,64,64,128,128,128,128,128,0,1,1,1,130,130,130,130,128,128,132,156,152,64,64,64,64,64,64,64,64,32,32,32,16,16,16,8,4,3,0,0,0,0,128,64,48,8,0,0,0,0,0,0,0,0,7,15,12,12,15,15,12,12,15,15,12,12,15,7,32,32,32,32,32,32,64,64,64,64,64,64,64,64,64,64,64,64,64,64,64,64,64,64,64,64,0,32,32,32,32,32,0,0,32,32,32,32,16,16,0,0,0,0,0,1,0,0,0,0,0,0,0,0,0,0]),bobber_bite.x,bobber_bite.y,bobber_bite.key,bobber_bite.mirrorX,bobber_bite.mirrorY)
  fish1 = Sprite(36,40,bytearray([0,0,0,0,16,40,72,136,8,8,8,4,4,4,196,36,36,196,4,8,8,144,16,32,64,128,0,0,0,0,0,0,0,0,0,0,
             0,0,0,8,24,40,72,72,137,138,132,0,0,0,0,129,129,128,64,68,34,33,16,24,36,194,1,2,4,12,20,100,136,8,176,192,
             0,0,0,0,0,0,0,0,0,0,0,1,1,97,147,10,4,2,0,128,112,0,0,0,0,128,127,0,0,0,0,128,127,3,0,0,
             0,0,0,0,0,0,0,0,0,0,0,224,16,32,32,161,33,33,127,128,160,144,136,132,67,64,32,48,40,40,20,15,0,0,0,0,
             0,0,0,0,0,0,0,0,0,0,0,3,4,10,17,32,48,40,70,64,79,80,32,0,0,0,0,0,0,0,0,0,0,0,0,0]), fish1.x,fish1.y,fish1.key,fish1.mirrorX,fish1.mirrorY)
  exclm_point = Sprite(2,8,bytearray([223,223]), exclm_point.x,exclm_point.y,exclm_point.key,exclm_point.mirrorX,exclm_point.mirrorY)

saveData.setName(globals().get('__file__', 'FAST_EXECUTE').replace('/Games/','').strip('/').split('/')[0].split('.')[0])

# Title Screen
def title_screen():
  global counter, river_birds, bobber_idle, title, rand_seed, can_catch, bobber_nibble, bobber_bite, fish1, river_bg, cast_pwr, rand_wait, rand_nibbles, cast_anim, cast_anim_fin, exclm_point, caught_fish_size, cast_direction, display_qty, draw_fishingline_x, draw_fishingline_y
  display.fill(0)
  display.drawSprite(title)
  display.update()
  display.fill(0)
  while True:
    if buttons.buttonA.justPressed():
      if saveData.hasItem('existing_game') == False:
        tutorial_screen()
        saveData.setItem('existing_game', True)
        saveData.save()
      river_screen()
    elif buttons.buttonB.justPressed():
      settings_screen()

# Settings Screen
def settings_screen():
  global counter, river_birds, bobber_idle, title, rand_seed, can_catch, bobber_nibble, bobber_bite, fish1, river_bg, cast_pwr, rand_wait, rand_nibbles, cast_anim, cast_anim_fin, exclm_point, caught_fish_size, cast_direction, display_qty, draw_fishingline_x, draw_fishingline_y
  while True:
    display.setFont("/lib/font3x5.bin", 3, 5, display.textSpaceWidth)
    display.drawText(str('A: RECORDS'), 0, 0, 1)
    display.drawText(str('<: SOUNDS'), 0, 8, 1)
    display.drawText(str('^: HOW TO PLAY'), 0, 16, 1)
    display.drawText(str('>: CLEAR DATA'), 0, 24, 1)
    display.drawText(str('B: RETURN'), 0, 33, 1)
    display.update()
    display.fill(0)
    if buttons.buttonA.justPressed():
      records_screen()
    elif buttons.buttonB.justPressed():
      title_screen()
    elif buttons.buttonR.justPressed():
      clear_data_screen()
    elif buttons.buttonU.justPressed():
      tutorial_screen()
    elif buttons.buttonL.justPressed():
      sound_settings()

# Records screen - show scores
def records_screen():
  global counter, river_birds, bobber_idle, title, rand_seed, can_catch, bobber_nibble, bobber_bite, fish1, river_bg, cast_pwr, rand_wait, rand_nibbles, cast_anim, cast_anim_fin, exclm_point, caught_fish_size, cast_direction, display_qty, draw_fishingline_x, draw_fishingline_y
  while True:
    display.setFont("/lib/font5x7.bin", 5, 7, display.textSpaceWidth)
    display.drawText(str('Fish Caught:'), 2, 0, 1)
    if saveData.hasItem('fish_qty_record') == False:
      display.drawText(str('NONE :('), 2, 9, 1)
    else:
      display.drawText(str(saveData.getItem('fish_qty_record')), 2, 9, 1)
    display.drawText(str('Largest:'), 2, 20, 1)
    if saveData.hasItem('fish_size_record') == False:
      display.drawText(str('N/A'), 2, 29, 1)
    else:
      display.drawText(str(str(saveData.getItem('fish_size_record')) + ' cm'), 2, 29, 1)
    display.update()
    display.fill(0)
    if buttons.inputJustPressed():
      settings_screen()

# Tutorial/How to Play
def tutorial_screen():
  global counter, river_birds, bobber_idle, title, rand_seed, can_catch, bobber_nibble, bobber_bite, fish1, river_bg, cast_pwr, rand_wait, rand_nibbles, cast_anim, cast_anim_fin, exclm_point, caught_fish_size, cast_direction, display_qty, draw_fishingline_x, draw_fishingline_y
  # Show tutorial
  while True:
    display.setFont("/lib/font5x7.bin", 5, 7, display.textSpaceWidth)
    display.drawText(str('How to Play'), 4, 1, 1)
    display.drawLine(0, 10, 72, 10, 1)
    display.drawText(str('Hold A &'), 4, 13, 1)
    display.drawText(str('release to'), 4, 22, 1)
    display.drawText(str('cast!'), 4, 31, 1)
    display.update()
    display.fill(0)
    if buttons.inputJustPressed():
      while True:
        display.drawText(str('Catch Fish'), 4, 1, 1)
        display.drawLine(0, 10, 72, 10, 1)
        display.drawText(str('Press A'), 4, 13, 1)
        display.drawText(str('when !!!'), 4, 22, 1)
        display.drawText(str('appears'), 4, 31, 1)
        display.update()
        display.fill(0)
        if buttons.inputJustPressed():
          break
      break

# Sound Settings
# 0: Sound off
# 1: Sound on
def sound_settings():
  global counter, river_birds, bobber_idle, title, rand_seed, can_catch, bobber_nibble, bobber_bite, fish1, river_bg, cast_pwr, rand_wait, rand_nibbles, cast_anim, cast_anim_fin, exclm_point, caught_fish_size, cast_direction, display_qty, draw_fishingline_x, draw_fishingline_y
  display.setFont("/lib/font5x7.bin", 5, 7, display.textSpaceWidth)
  display.drawText(str('Sound is'), 2, 0, 1)
  if int(saveData.getItem('sound_setting')) == 1:
    display.drawText(str('ON'), 2, 9, 1)
    display.drawText(str('A: TURN OFF'), 2, 21, 1)
  elif int(saveData.getItem('sound_setting')) == 0:
    display.drawText(str('OFF'), 2, 9, 1)
    display.drawText(str('A: TURN ON'), 2, 21, 1)
  display.drawText(str('B: CANCEL'), 2, 31, 1)
  display.update()
  display.fill(0)
  while True:
    if buttons.buttonA.justPressed():
      if int(saveData.getItem('sound_setting')) == 1:
        saveData.setItem('sound_setting', int(0))
        saveData.save()
        display.drawText(str('SOUND OFF'), 5, 10, 1)
        display.drawText(str('SAVED'), 5, 20, 1)
        display.update()
        display.fill(0)
        time.sleep(1)
        settings_screen()
      elif int(saveData.getItem('sound_setting')) == 0:
        saveData.setItem('sound_setting', int(1))
        saveData.save()
        display.drawText(str('SOUND ON'), 5, 10, 1)
        display.drawText(str('SAVED'), 5, 20, 1)
        display.update()
        display.fill(0)
        time.sleep(1)
        settings_screen()
    elif buttons.buttonB.justPressed():
      settings_screen()

# Clear Data Screen
def clear_data_screen():
  global counter, river_birds, bobber_idle, title, rand_seed, can_catch, bobber_nibble, bobber_bite, fish1, river_bg, cast_pwr, rand_wait, rand_nibbles, cast_anim, cast_anim_fin, exclm_point, caught_fish_size, cast_direction, display_qty, draw_fishingline_x, draw_fishingline_y
  display.setFont("/lib/font8x8.bin", 8, 8, display.textSpaceWidth)
  display.drawText(str('REALLY'), 9, 0, 1)
  display.setFont("/lib/font5x7.bin", 5, 7, display.textSpaceWidth)
  display.drawText(str('DELETE'), 16, 10, 1)
  display.drawText(str('SAVE DATA?'), 8, 19, 1)
  display.drawText(str('B:YES A:NO'), 6, 31, 1)
  display.update()
  display.fill(0)
  # Delete save data
  while True:
    if buttons.buttonA.justPressed():
      break
    elif buttons.buttonB.justPressed():
      saveData.delItem('fish_qty_record')
      saveData.delItem('fish_size_record')
      saveData.delItem('existing_game')
      display.setFont("/lib/font5x7.bin", 5, 7, display.textSpaceWidth)
      display.drawText(str('DATA'), 0, 10, 1)
      display.drawText(str('CLEARED'), 0, 20, 1)
      display.update()
      display.fill(0)
      time.sleep(2)
      break

# Show the river animation
def river_screen():
  global counter, river_birds, bobber_idle, title, rand_seed, can_catch, bobber_nibble, bobber_bite, fish1, river_bg, cast_pwr, rand_wait, rand_nibbles, cast_anim, cast_anim_fin, exclm_point, caught_fish_size, cast_direction, display_qty, draw_fishingline_x, draw_fishingline_y
  river_birds.x = 36
  river_birds.y = 3
  river_birds.key = 0
  for count in range(int(30 * 4)):
    counter = (counter if isinstance(counter, Number) else 0) + 1
    display.drawSprite(river_bg)
    display.drawSprite(river_birds)
    if counter % 10 == 0:
      river_bg.setFrame(river_bg.getFrame() + 1)
    if counter % 20 == 0:
      river_birds.x += -1
      river_birds.setFrame(river_birds.getFrame() + 1)
    display.update()
    display.fill(0)
    if buttons.inputJustPressed():
      display.update()
      display.fill(0)
      break
  time.sleep(0.2)
  cast_screen()

# Cycle bobber_idle animation
def bobber_idle2():
  global counter, river_birds, bobber_idle, title, rand_seed, can_catch, bobber_nibble, bobber_bite, fish1, river_bg, cast_pwr, rand_wait, rand_nibbles, cast_anim, cast_anim_fin, exclm_point, caught_fish_size, cast_direction, display_qty, draw_fishingline_x, draw_fishingline_y
  display.drawSprite(bobber_idle)
  counter = (counter if isinstance(counter, Number) else 0) + 1
  if counter % 22 == 0:
    bobber_idle.setFrame(bobber_idle.getFrame() + 1)
  display.update()
  display.fill(0)

# Cycle bobber_nibble animation
def bobber_nibble2():
  global counter, river_birds, bobber_idle, title, rand_seed, can_catch, bobber_nibble, bobber_bite, fish1, river_bg, cast_pwr, rand_wait, rand_nibbles, cast_anim, cast_anim_fin, exclm_point, caught_fish_size, cast_direction, display_qty, draw_fishingline_x, draw_fishingline_y
  counter = (counter if isinstance(counter, Number) else 0) + 1
  display.drawSprite(bobber_nibble)
  if counter % 15 == 0:
    bobber_nibble.setFrame(bobber_nibble.getFrame() + 1)
  display.update()
  display.fill(0)

# Cycle bobber_bite animation
def bobber_bite2():
  global counter, river_birds, bobber_idle, title, rand_seed, can_catch, bobber_nibble, bobber_bite, fish1, river_bg, cast_pwr, rand_wait, rand_nibbles, cast_anim, cast_anim_fin, exclm_point, caught_fish_size, cast_direction, display_qty, draw_fishingline_x, draw_fishingline_y
  counter = (counter if isinstance(counter, Number) else 0) + 1
  display.drawSprite(bobber_bite)
  if counter % 10 == 0:
    bobber_bite.setFrame(bobber_bite.getFrame() + 1)
  display.update()
  display.fill(0)

# Display the "Too early, try again" screen
def early_screen():
  global counter, river_birds, bobber_idle, title, rand_seed, can_catch, bobber_nibble, bobber_bite, fish1, river_bg, cast_pwr, rand_wait, rand_nibbles, cast_anim, cast_anim_fin, exclm_point, caught_fish_size, cast_direction, display_qty, draw_fishingline_x, draw_fishingline_y
  display.setFont("/lib/font5x7.bin", 5, 7, display.textSpaceWidth)
  display.drawText(str('Too early!'), 5, 2, 1)
  display.drawText(str('It got'), 5, 14, 1)
  display.drawText(str('away... :('), 5, 24, 1)
  display.setFont("/lib/font3x5.bin", 3, 5, display.textSpaceWidth)
  display.drawText(str('A: AGAIN  B: MENU'), 2, 35, 1)
  display.update()
  display.fill(0)
  display.setFont("/lib/font5x7.bin", 5, 7, display.textSpaceWidth)
  while True:
    if buttons.buttonA.justPressed():
      river_screen()
    elif buttons.buttonB.justPressed():
      title_screen()

# Casting Screen
def cast_screen():
  global counter, river_birds, bobber_idle, title, rand_seed, can_catch, bobber_nibble, bobber_bite, fish1, river_bg, cast_pwr, rand_wait, rand_nibbles, cast_anim, cast_anim_fin, exclm_point, caught_fish_size, cast_direction, display_qty, draw_fishingline_x, draw_fishingline_y
  setup_rand()
  display.fill(0)
  display.update()
  # Set sprite positions and initial variables
  cast_anim.key = 0
  cast_anim_fin.key = 0
  cast_anim.x = 40
  cast_anim.y = 3
  cast_anim_fin.x = 40
  cast_anim_fin.y = 3
  exclm_point.x = 65
  exclm_point.y = 20
  cast_direction = 1
  cast_pwr = 0
  # Player holds A to charge cast
  while True:
    display.drawRectangle(2, 28, 47, 11, 1)
    display.setFont("/lib/font5x7.bin", 5, 7, display.textSpaceWidth)
    display.drawText(str('HOLD A'), 8, 30, 1)
    # Constrains rectangle width to 100% even though
    # cast power can go >100. Rectangle is 45px wide.
    display.drawFilledRectangle(3, 28, min(max(int((cast_pwr / 100) * 45), 0), 45), 11, 1)
    display.drawSprite(cast_anim)
    if buttons.buttonA.pressed():
      cast_pwr = (cast_pwr if isinstance(cast_pwr, Number) else 0) + cast_direction * 2
    # Makes the cast bar "bounce."
    #
    # Max cast power = 106, to allow a 12-frame "perfect cast" window without being
    # frame-perfect. 
    if cast_pwr <= 0:
      cast_pwr = 0
      cast_direction = 1
    elif cast_pwr >= 106:
      cast_direction = -1
    # Switch cast_anim frame depending on cast power.
    if cast_pwr >= 0 and cast_pwr < 25:
      cast_anim.setFrame(0)
    elif cast_pwr >= 25 and cast_pwr < 50:
      cast_anim.setFrame(1)
    elif cast_pwr >= 50 and cast_pwr < 75:
      cast_anim.setFrame(2)
    elif cast_pwr >= 75:
      cast_anim.setFrame(3)
    if cast_pwr >= 100:
      display.drawSprite(exclm_point)
    # When A is released, break out of the loop
    if not buttons.buttonA.justPressed() and not buttons.buttonA.pressed() and cast_pwr > 0:
      break
    print(cast_pwr)
    display.update()
    display.fill(0)
  display.fill(0)
  # Initial fishing line position
  draw_fishingline_x = 39
  draw_fishingline_y = 2
  # Files off the "perfect cast" window so % multiplier does not exceed 100
  if cast_pwr > 100:
    cast_pwr = 100
  # Uses cast power as a speed multiplier on the FPS
  # to adjust the speed of the fishing line animation
  display.setFPS(25 + int(cast_pwr / 5))
  # Draws the fishing line animation.
  while not draw_fishingline_x == 0:
    display.drawSprite(cast_anim_fin)
    display.drawLine(39, 8, draw_fishingline_x, 2, 1)
    draw_fishingline_x = (draw_fishingline_x if isinstance(draw_fishingline_x, Number) else 0) + -1
    display.update()
    display.fill(0)
  # Reduce line speed by 10%
  display.setFPS(display.frameRate - int(display.frameRate * 0.1))
  while not draw_fishingline_y == 14:
    display.drawSprite(cast_anim_fin)
    display.drawLine(39, 8, draw_fishingline_x, draw_fishingline_y, 1)
    draw_fishingline_y = (draw_fishingline_y if isinstance(draw_fishingline_y, Number) else 0) + 1
    display.update()
    display.fill(0)
  # Return FPS to normal
  display.setFPS(30)
  draw_fishingline_y = (draw_fishingline_y if isinstance(draw_fishingline_y, Number) else 0) + 1
  time.sleep(0.5)
  display.drawSprite(cast_anim_fin)
  display.drawLine(39, 8, draw_fishingline_x, draw_fishingline_y, 1)
  time.sleep(0.1)
  display.setFont("/lib/font3x5.bin", 3, 5, display.textSpaceWidth)
  display.drawText(str('* SPLASH *'), 2, 25, 1)
  display.update()
  time.sleep(0.75)
  display.setFont("/lib/font5x7.bin", 5, 7, display.textSpaceWidth)
  display.drawFilledRectangle(2, 25, 40, 5, 0)
  display.update()
  display.fill(0)
  time.sleep(0.5)
  # Nullifies any button inputs made during the cast animation
  if buttons.inputJustPressed():
    exec('pass')
  fishing_screen()

# Fishing Screen - the main event!
def fishing_screen():
  global counter, river_birds, bobber_idle, title, rand_seed, can_catch, bobber_nibble, bobber_bite, fish1, river_bg, cast_pwr, rand_wait, rand_nibbles, cast_anim, cast_anim_fin, exclm_point, caught_fish_size, cast_direction, display_qty, draw_fishingline_x, draw_fishingline_y
  counter = 0
  # 0 = can't catch
  # 1 = can catch
  # 2 = missed catch
  can_catch = 0
  # Set random bobber idle time
  rand_wait = random.randint(3, 10)
  # Set random number of nibbles before bite
  rand_nibbles = random.randint(1, 5)
  # Used to debug issues with the randomizer
  print(counter)
  print(rand_wait)
  print(rand_nibbles)
  display.setFont("/lib/font5x7.bin", 5, 7, display.textSpaceWidth)
  # Wait a random number of seconds, or print message if A hit
  for count2 in range(int(rand_wait * 30)):
    bobber_idle2()
    if can_catch == 0 and buttons.buttonA.justPressed():
      if int(saveData.getItem('sound_setting')) == 1:
        audio.playBlocking(400, 100)
      display.drawText(str('Wait for'), 5, 5, 1)
      display.drawText(str('a bite'), 5, 15, 1)
      display.drawText(str('first!'), 5, 25, 1)
      display.update()
      display.fill(0)
      time.sleep(1.5)
      fishing_screen()
  # Nibble a random number of times, with a 1-3 second wait between nibbles.
  # Print message and return to cast screen if A hit.
  for count5 in range(int(rand_nibbles)):
    for count3 in range(30):
      bobber_nibble2()
      if can_catch == 0 and buttons.buttonA.justPressed():
        if int(saveData.getItem('sound_setting')) == 1:
          audio.playBlocking(400, 150)
          audio.playBlocking(300, 100)
          early_screen()
    for count4 in range(int(30 * random.randint(1, 3))):
      bobber_idle2()
      if can_catch == 0 and buttons.buttonA.justPressed():
        if int(saveData.getItem('sound_setting')) == 1:
          audio.playBlocking(400, 150)
          audio.playBlocking(300, 100)
          early_screen()
  # Display some manually timed nibble frames before
  # the bite, and display early message if A hit.
  display.drawSprite(bobber_nibble)
  display.update()
  display.fill(0)
  time.sleep(0.3)
  bobber_nibble.setFrame(1)
  display.drawSprite(bobber_nibble)
  display.update()
  display.fill(0)
  time.sleep(0.3)
  if can_catch == 0 and buttons.buttonA.justPressed():
    if int(saveData.getItem('sound_setting')) == 1:
      audio.playBlocking(400, 150)
      audio.playBlocking(300, 100)
    early_screen()
  # !!! The magic is about to happen! You can catch this fish!
  can_catch = 1
  # It's a bite!
  for count6 in range(30):
    bobber_bite2()
    if can_catch == 1 and buttons.buttonA.justPressed():
      if int(saveData.getItem('sound_setting')) == 1:
        audio.playBlocking(1500, 100)
        audio.playBlocking(3000, 100)
      catch_screen()
  # Manually timed nibble frames to ease out of the bite animation
  display.drawSprite(bobber_nibble)
  display.update()
  display.fill(0)
  bobber_nibble.setFrame(0)
  time.sleep(0.3)
  display.drawSprite(bobber_nibble)
  display.update()
  display.fill(0)
  # Catch! That! Fish!
  if can_catch == 1 and buttons.buttonA.justPressed():
    if int(saveData.getItem('sound_setting')) == 1:
      audio.playBlocking(1500, 100)
      audio.playBlocking(3000, 100)
    catch_screen()
  # If A was not pressed while the bite sprite
  # is displayed, set can_catch to 2 (missed).
  can_catch = 2
  # Trying to catch a missed fish will just reset to the cast screen.
  while True:
    bobber_idle2()
    if can_catch == 2 and buttons.buttonA.justPressed():
      if int(saveData.getItem('sound_setting')) == 1:
        audio.playBlocking(400, 150)
        audio.playBlocking(300, 100)
      display.setFont("/lib/font5x7.bin", 5, 7, display.textSpaceWidth)
      display.drawText(str('Too late!'), 5, 2, 1)
      display.drawText(str('Better luck'), 5, 14, 1)
      display.drawText(str('next time!'), 5, 24, 1)
      display.setFont("/lib/font3x5.bin", 3, 5, display.textSpaceWidth)
      display.drawText(str('A: AGAIN  B: MENU'), 2, 35, 1)
      display.update()
      display.fill(0)
      display.setFont("/lib/font5x7.bin", 5, 7, display.textSpaceWidth)
      while True:
        if buttons.buttonA.justPressed():
          river_screen()
        elif buttons.buttonB.justPressed():
          title_screen()

# Shows details of caught fish
def catch_screen():
  global counter, river_birds, bobber_idle, title, rand_seed, can_catch, bobber_nibble, bobber_bite, fish1, river_bg, cast_pwr, rand_wait, rand_nibbles, cast_anim, cast_anim_fin, exclm_point, caught_fish_size, cast_direction, display_qty, draw_fishingline_x, draw_fishingline_y
  # Catch splash screen
  display.setFont("/lib/font8x8.bin", 8, 8, display.textSpaceWidth)
  fish1.x = 36
  display.drawSprite(fish1)
  display.drawText(str('GOOD'), 2, 9, 1)
  display.drawText(str('CATCH'), 2, 19, 1)
  display.update()
  display.fill(0)
  time.sleep(2)
  display.setFont("/lib/font5x7.bin", 5, 7, display.textSpaceWidth)
  # Set random fish size, and add a bonus of 20% of cast power
  caught_fish_size = int(random.randint(10, 150) + cast_pwr / 5)
  # Display fish stats
  display.drawText(str(''.join([str(x) for x in ['Size: ', int(caught_fish_size), 'cm']])), 2, 0, 1)
  if saveData.hasItem('fish_size_record') == False or caught_fish_size > int(saveData.getItem('fish_size_record')):
    saveData.setItem('fish_size_record', caught_fish_size)
    saveData.save()
    display.setFont("/lib/font3x5.bin", 3, 5, display.textSpaceWidth)
    display.drawText(str('NEW RECORD!'), 15, 11, 1)
    display.setFont("/lib/font5x7.bin", 5, 7, display.textSpaceWidth)
  if saveData.hasItem('fish_qty_record') == False:
    saveData.setItem('fish_qty_record', 1)
    saveData.save()
    display.drawText(str('First Catch!'), 2, 25, 1)
  else:
    display_qty = saveData.getItem('fish_qty_record')
    saveData.setItem('fish_qty_record', display_qty + 1)
    saveData.save()
    display_qty = saveData.getItem('fish_qty_record')
    if display_qty == 69:
      display.drawText(str(str(display_qty) + ' caught ;)'), 2, 23, 1)
    else:
      display.drawText(str(str(display_qty) + ' caught'), 2, 23, 1)
  display.setFont("/lib/font3x5.bin", 3, 5, display.textSpaceWidth)
  display.drawText(str('A: AGAIN  B: MENU'), 2, 35, 1)
  display.update()
  display.fill(0)
  time.sleep(1)
  while True:
    if buttons.buttonA.justPressed():
      river_screen()
    elif buttons.buttonB.justPressed():
      title_screen()


# The actual game execution starts here.
if saveData.hasItem('sound_setting') == False:
  # Prevent null value in sound setting - defaults to sound on
  saveData.setItem('sound_setting', 1)
  saveData.save()
display.setFPS(30)
cast_pwr = 0
setup_sprites()
title_screen()

#### !!!! BLOCKLY EXPORT !!!! ####
