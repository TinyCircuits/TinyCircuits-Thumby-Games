#### !!!! BLOCKLY EXPORT !!!! ####
from thumbySprite import Sprite
Number = int
import random
from thumbyGraphics import display
from thumbyAudio import audio
import time
import thumbyButton as buttons
import machine

orb_y = None
enemy_sprite = None
player_x = None
orb_sprite = None
enemy_x_value = None
player_y = None
player_sprite = None
orb_x = None
orb_collected_value = None
orb_spawn_side_value = None
enemy_y_value = None
lives_value = None
OBJ1_anim_value = None
ded_sprite = None
title_sprite = None

orb_sprite = Sprite(1,1,bytearray([1]))

enemy_sprite = Sprite(1,1,bytearray([1]))

player_sprite = Sprite(1,1,bytearray([1]))

# spawn sprites
def setup_sprites():
  global orb_y, enemy_sprite, player_x, orb_sprite, enemy_x_value, player_y, player_sprite, orb_x, orb_collected_value, orb_spawn_side_value, enemy_y_value, lives_value, OBJ1_anim_value, ded_sprite, title_sprite
  orb_sprite = Sprite(8,8,bytearray([0,0,24,36,36,24,0,0]), orb_sprite.x,orb_sprite.y,orb_sprite.key,orb_sprite.mirrorX,orb_sprite.mirrorY)
  orb_sprite.key = 0
  orb_sprite.x = 56
  orb_sprite.y = 30
  orb_collected_value = 0
  orb_spawn_side_value = 0
  enemy_sprite = Sprite(8,8,bytearray([2,56,37,84,89,98,28,0,0,56,38,90,82,76,33,20,0,56,70,154,42,164,28,64,40,132,50,74,90,100,28,0]),enemy_sprite.x,enemy_sprite.y,enemy_sprite.key,enemy_sprite.mirrorX,enemy_sprite.mirrorY)
  enemy_sprite.key = 0
  enemy_sprite.x = 0
  enemy_sprite.y = 16
  player_sprite = Sprite(8,8,bytearray([0,24,124,58,58,126,0,0]), player_sprite.x,player_sprite.y,player_sprite.key,player_sprite.mirrorX,player_sprite.mirrorY)
  player_sprite.x = 32
  lives_value = 3

# set values to sprite positions
def log_items_pos():
  global orb_y, enemy_sprite, player_x, orb_sprite, enemy_x_value, player_y, player_sprite, orb_x, orb_collected_value, orb_spawn_side_value, enemy_y_value, lives_value, OBJ1_anim_value, ded_sprite, title_sprite
  player_x = int(player_sprite.x)
  player_y = int(player_sprite.y)
  orb_x = int(orb_sprite.x)
  orb_y = int(orb_sprite.y)
  orb_x = (orb_x if isinstance(orb_x, Number) else 0) + 4
  orb_y = (orb_y if isinstance(orb_y, Number) else 0) + 4

# move the orb once collected
def orb_placement_checker():
  global orb_y, enemy_sprite, player_x, orb_sprite, enemy_x_value, player_y, player_sprite, orb_x, orb_collected_value, orb_spawn_side_value, enemy_y_value, lives_value, OBJ1_anim_value, ded_sprite, title_sprite
  if orb_spawn_side_value == 0:
    orb_sprite.x = random.randint(0, 64)
    orb_sprite.y = 30
  if orb_spawn_side_value == 1:
    orb_sprite.x = random.randint(0, 64)
    orb_sprite.y = 0

# orb is touched and collected
def collect_orb_draw_checker():
  global orb_y, enemy_sprite, player_x, orb_sprite, enemy_x_value, player_y, player_sprite, orb_x, orb_collected_value, orb_spawn_side_value, enemy_y_value, lives_value, OBJ1_anim_value, ded_sprite, title_sprite
  if bool(display.getPixel(int(orb_x), int(orb_y))):
    audio.play(5000, 75)
    orb_collected_value = (orb_collected_value if isinstance(orb_collected_value, Number) else 0) + 1
    print(orb_collected_value)
    orb_spawn_side_value = (orb_spawn_side_value if isinstance(orb_spawn_side_value, Number) else 0) + 1
    if orb_spawn_side_value > 1:
      orb_spawn_side_value = 0
    orb_placement_checker()

# Enemy movement left to right
def enemy_movement_update():
  global orb_y, enemy_sprite, player_x, orb_sprite, enemy_x_value, player_y, player_sprite, orb_x, orb_collected_value, orb_spawn_side_value, enemy_y_value, lives_value, OBJ1_anim_value, ded_sprite, title_sprite
  enemy_sprite.x += 2
  if orb_collected_value > 20:
    enemy_sprite.y += random.randint(-1, 1)
  if orb_collected_value > 35:
    enemy_sprite.x += random.randint(0, 1)
  enemy_x_value = int(enemy_sprite.x)
  enemy_y_value = int(enemy_sprite.y)
  enemy_x_value = (enemy_x_value if isinstance(enemy_x_value, Number) else 0) + 8
  enemy_y_value = (enemy_y_value if isinstance(enemy_y_value, Number) else 0) + 3
  enemy_touch_draw_checker()
  if enemy_sprite.x > 72:
    enemy_sprite.x += -80
    enemy_sprite.y = random.randint(12, 20)
  OBJ1_anim_value = (OBJ1_anim_value if isinstance(OBJ1_anim_value, Number) else 0) + 1
  enemy_sprite.setFrame(OBJ1_anim_value)

# enemy is touched
def enemy_touch_draw_checker():
  global orb_y, enemy_sprite, player_x, orb_sprite, enemy_x_value, player_y, player_sprite, orb_x, orb_collected_value, orb_spawn_side_value, enemy_y_value, lives_value, OBJ1_anim_value, ded_sprite, title_sprite
  if player_y > enemy_y_value - 9:
    if player_y < enemy_y_value + 3:
      if player_x > enemy_x_value - 12:
        if player_x < enemy_x_value - 6:
          print(enemy_x_value)
          enemy_sprite.x = -48 - random.randint(0, 32)
          player_sprite.x = 32
          player_sprite.y = 0
          orb_spawn_side_value = (orb_spawn_side_value if isinstance(orb_spawn_side_value, Number) else 0) + 0
          lives_value = (lives_value if isinstance(lives_value, Number) else 0) + -1
          Lives_left()
          orb_placement_checker()

# show lives left
def Lives_left():
  global orb_y, enemy_sprite, player_x, orb_sprite, enemy_x_value, player_y, player_sprite, orb_x, orb_collected_value, orb_spawn_side_value, enemy_y_value, lives_value, OBJ1_anim_value, ded_sprite, title_sprite
  enemy_x_value = 0
  display.fill(0)
  display.update()
  audio.play(1000, 150)
  display.setFont("/lib/font5x7.bin", 5, 7, display.textSpaceWidth)
  display.drawText(str(str(lives_value) + ' lives left'), 1, 16, 1)
  display.display.show()
  time.sleep(1.5)
  audio.play(3000, 25)

title_sprite = Sprite(1,1,bytearray([1]))

ded_sprite = Sprite(1,1,bytearray([1]))

# The main game block
def main_game_clump():
  global orb_y, enemy_sprite, player_x, orb_sprite, enemy_x_value, player_y, player_sprite, orb_x, orb_collected_value, orb_spawn_side_value, enemy_y_value, lives_value, OBJ1_anim_value, ded_sprite, title_sprite
  while True:
    display.setFPS(30 + orb_collected_value)
    if player_x < orb_x - 4:
      player_sprite = Sprite(8,8,bytearray([0,24,124,58,58,126,0,0]), player_sprite.x,player_sprite.y,player_sprite.key,player_sprite.mirrorX,player_sprite.mirrorY)
      player_sprite.x += 1
    if player_x > orb_x - 4:
      player_sprite = Sprite(8,8,bytearray([0,0,126,58,58,124,24,0]), player_sprite.x,player_sprite.y,player_sprite.key,player_sprite.mirrorX,player_sprite.mirrorY)
      player_sprite.x += -1
    if buttons.buttonU.pressed() and player_sprite.y > 0:
      player_sprite.y += -1
    if buttons.buttonD.pressed() and player_sprite.y < 32:
      player_sprite.y += 1
    enemy_movement_update()
    log_items_pos()
    collect_orb_draw_checker()
    enemy_touch_draw_checker()
    if lives_value <= 0:
      break
    display.fill(0)
    display.drawSprite(player_sprite)
    display.drawSprite(enemy_sprite)
    display.drawSprite(orb_sprite)
    display.update()
  display.fill(0)
  display.update()
  display.setFont("/lib/font5x7.bin", 5, 7, display.textSpaceWidth)
  display.drawText(str('GAME OVER'), 10, 4, 1)
  display.setFont("/lib/font3x5.bin", 3, 5, display.textSpaceWidth)
  display.drawText(str(str(orb_collected_value) + ' EGGS!'), 23, 14, 1)
  display.display.show()
  display.drawText(str('A/restart B/exit'), 4, 33, 1)
  ded_sprite = Sprite(16,8,bytearray([14,59,31,59,14,0,0,0,224,144,248,248,248,240,144,0]), ded_sprite.x,ded_sprite.y,ded_sprite.key,ded_sprite.mirrorX,ded_sprite.mirrorY)
  ded_sprite.x = 28
  ded_sprite.y = 22
  display.drawSprite(ded_sprite)
  display.update()
  time.sleep(1)
  while True:
    if buttons.buttonA.justPressed():
      machine.reset()
    if buttons.buttonB.justPressed():
      break
  setup_sprites()
  Lives_left()
  log_items_pos()
  main_game_clump()


orb_y

print('loaded.')
display.setFont("/lib/font5x7.bin", 5, 7, display.textSpaceWidth)
display.drawText(str('DIABLOHEAD'), 6, 16, 1)
display.setFont("/lib/font3x5.bin", 3, 5, display.textSpaceWidth)
display.drawText(str('GAMES'), 27, 24, 1)
display.display.show()
time.sleep(1.5)
display.fill(0)
display.update()
time.sleep(0.5)
while True:
  title_sprite = Sprite(72,40,bytearray([0,0,56,240,240,96,96,192,128,128,240,254,28,120,224,128,0,0,0,0,192,224,112,112,48,112,112,224,0,0,240,248,60,28,56,112,192,128,0,0,252,254,14,6,102,102,224,96,64,0,240,248,0,0,0,0,224,240,48,0,224,240,176,48,48,48,0,0,0,0,0,0,
             0,48,0,3,63,127,224,0,1,1,3,3,0,0,1,7,63,60,0,0,7,15,24,16,16,16,24,15,0,0,15,31,0,0,0,0,3,15,0,0,3,7,7,6,4,6,3,0,0,0,3,7,12,12,12,6,3,0,60,124,112,97,33,49,63,30,0,0,48,0,0,0,
             0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,252,252,204,206,198,198,198,70,0,0,0,252,254,3,3,3,195,198,192,0,254,255,3,3,1,195,194,192,0,0,14,31,57,113,227,3,2,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,
             0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,7,15,12,12,12,12,12,12,8,0,0,3,7,12,12,14,7,0,0,0,1,7,6,14,15,15,0,0,0,7,6,6,6,6,3,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,
             0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]), title_sprite.x,title_sprite.y,title_sprite.key,title_sprite.mirrorX,title_sprite.mirrorY)
  display.drawSprite(title_sprite)
  display.setFont("/lib/font3x5.bin", 3, 5, display.textSpaceWidth)
  display.drawText(str('A or B to start'), 6, 33, 1)
  display.update()
  if buttons.actionJustPressed():
    break
setup_sprites()
Lives_left()
log_items_pos()
main_game_clump()

#### !!!! BLOCKLY EXPORT !!!! ####