#### !!!! BLOCKLY EXPORT !!!! ####
from thumbyGraphics import display
from thumbySprite import Sprite
import thumbyButton as buttons
import random
Number = int
from thumbyAudio import audio
from thumbySaves import saveData

car_1_x = None
car_1_y = None
car_2_x = None
car_2_y = None
player_car = None
Main_menu = None
truck_x = None
score = None
road_lines_y = None
car_1 = None
car_2 = None
odd_or_even = None
truck_y = None
player_car_x = None
truck = None

Main_menu = Sprite(1,1,bytearray([1]))

car_2 = Sprite(1,1,bytearray([1]))

car_1 = Sprite(1,1,bytearray([1]))

truck = Sprite(1,1,bytearray([1]))

player_car = Sprite(1,1,bytearray([1]))

# Describe this function...
def Game():
  global car_1_x, car_1_y, car_2_x, car_2_y, player_car, Main_menu, truck_x, score, road_lines_y, car_1, car_2, odd_or_even, truck_y, player_car_x, truck
  player_car.setFrame(0)
  odd_or_even = 0
  score = 0
  player_car_x = 28
  road_lines_y = -8
  car_1_x = 12
  car_2_x = 12
  truck_x = 28
  truck_y = -64
  player_car.x = player_car_x
  player_car.y = 22
  spawn_car_1()
  spawn_car_2()
  spawn_truck()
  while not buttons.buttonA.justPressed():
    display.setFont("/lib/font3x5.bin", 3, 5, display.textSpaceWidth)
    display.drawSprite(Main_menu)
    display.drawText(str('Press - A'), 20, 30, 1)
    display.update()
    display.fill(0)
  while True:
    main_game_loop()

# Describe this function...
def spawn_car_1():
  global car_1_x, car_1_y, car_2_x, car_2_y, player_car, Main_menu, truck_x, score, road_lines_y, car_1, car_2, odd_or_even, truck_y, player_car_x, truck
  car_1_x = random.choice([28, 44, 12])
  car_1_y = -48
  car_1.x = car_1_x
  car_1.y = car_1_y

# Describe this function...
def main_game_loop():
  global car_1_x, car_1_y, car_2_x, car_2_y, player_car, Main_menu, truck_x, score, road_lines_y, car_1, car_2, odd_or_even, truck_y, player_car_x, truck
  if car_1_y > 112:
    score = (score if isinstance(score, Number) else 0) + 1
    respawn_car_1()
  if car_2_y > 80:
    score = (score if isinstance(score, Number) else 0) + 1
    respawn_car_2()
  if truck_x == 28:
    respawn_truck()
  if truck_y > 48:
    respawn_truck()
    score = (score if isinstance(score, Number) else 0) + 1
  if buttons.buttonL.justPressed() and player_car_x > 12:
    audio.play(1000, 50)
    for count in range(16):
      score2()
      roads()
      draw_car_1()
      draw_car_2()
      draw_truck()
      player_car.setFrame(2)
      display.drawSprite(player_car)
      display.update()
      if car_1_y > 8:
        car_1_collision_check()
      if car_2_y > 8:
        car_2_collision_check()
      if truck_y > -20:
        truck_collision_check()
      display.fill(0)
      player_car_x = (player_car_x if isinstance(player_car_x, Number) else 0) + -1
      player_car.x = player_car_x
    player_car.setFrame(0)
  if buttons.buttonR.justPressed() and player_car_x < 44:
    audio.play(1000, 50)
    for count2 in range(16):
      score2()
      roads()
      draw_car_1()
      draw_car_2()
      draw_truck()
      player_car.setFrame(1)
      display.drawSprite(player_car)
      display.update()
      if car_1_y > 8:
        car_1_collision_check()
      if car_2_y > 8:
        car_2_collision_check()
      if truck_y > -20:
        truck_collision_check()
      display.fill(0)
      player_car_x = (player_car_x if isinstance(player_car_x, Number) else 0) + 1
      player_car.x = player_car_x
    player_car.setFrame(0)
  roads()
  draw_car_1()
  draw_car_2()
  draw_truck()
  display.drawSprite(player_car)
  score2()
  display.update()
  if car_1_y > 8:
    car_1_collision_check()
  if car_2_y > 8:
    car_2_collision_check()
  if truck_y > -20:
    truck_collision_check()
  display.fill(0)

# Describe this function...
def spawn_car_2():
  global car_1_x, car_1_y, car_2_x, car_2_y, player_car, Main_menu, truck_x, score, road_lines_y, car_1, car_2, odd_or_even, truck_y, player_car_x, truck
  car_2_x = random.choice([28, 44, 12])
  car_2_y = -80
  car_2.x = car_2_x
  car_2.y = car_2_y

# Describe this function...
def respawn_car_1():
  global car_1_x, car_1_y, car_2_x, car_2_y, player_car, Main_menu, truck_x, score, road_lines_y, car_1, car_2, odd_or_even, truck_y, player_car_x, truck
  car_1_x = random.choice([44, 28, 12])
  car_1_y = -48
  car_1.x = car_1_x
  car_1.y = car_1_y

# Describe this function...
def respawn_car_2():
  global car_1_x, car_1_y, car_2_x, car_2_y, player_car, Main_menu, truck_x, score, road_lines_y, car_1, car_2, odd_or_even, truck_y, player_car_x, truck
  car_2_x = random.choice([44, 28, 12])
  car_2_y = -80
  car_2.x = car_2_x
  car_2.y = car_2_y

# Describe this function...
def spawn_truck():
  global car_1_x, car_1_y, car_2_x, car_2_y, player_car, Main_menu, truck_x, score, road_lines_y, car_1, car_2, odd_or_even, truck_y, player_car_x, truck
  if car_1_x != 12 and car_2_x != 12:
    truck_x = 12
    truck_y = -32
    truck.x = truck_x
    truck.y = truck_y
  if car_1_x != 44 and car_2_x != 44:
    truck_x = 44
    truck_y = -32
    truck.x = truck_x
    truck.y = truck_y
  if car_1_x != 12 and car_2_x != 12 and car_1_x != 44 and car_2_x != 44:
    truck_x = random.choice([44, 12])
    truck_y = -32
    truck.x = truck_x
    truck.y = truck_y

# Describe this function...
def respawn_truck():
  global car_1_x, car_1_y, car_2_x, car_2_y, player_car, Main_menu, truck_x, score, road_lines_y, car_1, car_2, odd_or_even, truck_y, player_car_x, truck
  truck_x = 28
  truck_y = -32
  if car_1_x != 12 and car_2_x != 12:
    truck_x = 12
    truck_y = -32
    truck.x = truck_x
    truck.y = truck_y
  if car_1_x != 44 and car_2_x != 44:
    truck_x = 44
    truck_y = -32
    truck.x = truck_x
    truck.y = truck_y
  if car_1_x != 12 and car_2_x != 12 and car_1_x != 44 and car_2_x != 44:
    truck_x = random.choice([44, 12])
    truck_y = -32
    truck.x = truck_x
    truck.y = truck_y

# Describe this function...
def roads():
  global car_1_x, car_1_y, car_2_x, car_2_y, player_car, Main_menu, truck_x, score, road_lines_y, car_1, car_2, odd_or_even, truck_y, player_car_x, truck
  if road_lines_y > 40:
    road_lines_y = -40
  road_lines_y = (road_lines_y if isinstance(road_lines_y, Number) else 0) + 4
  left_road_lines()
  right_road_lines()
  display.drawLine(12, 0, 12, 40, 1)
  display.drawLine(60, 0, 60, 40, 1)

# Describe this function...
def left_road_lines():
  global car_1_x, car_1_y, car_2_x, car_2_y, player_car, Main_menu, truck_x, score, road_lines_y, car_1, car_2, odd_or_even, truck_y, player_car_x, truck
  display.drawRectangle(28, road_lines_y + -40, 1, 5, 1)
  display.drawRectangle(28, road_lines_y + -20, 1, 5, 1)
  display.drawRectangle(28, road_lines_y + 0, 1, 5, 1)
  display.drawRectangle(28, road_lines_y + 20, 1, 5, 1)
  display.drawRectangle(28, road_lines_y + 40, 1, 5, 1)
  display.drawRectangle(28, road_lines_y + 60, 1, 5, 1)
  display.drawRectangle(28, road_lines_y + 80, 1, 5, 1)

# Describe this function...
def right_road_lines():
  global car_1_x, car_1_y, car_2_x, car_2_y, player_car, Main_menu, truck_x, score, road_lines_y, car_1, car_2, odd_or_even, truck_y, player_car_x, truck
  display.drawRectangle(44, road_lines_y + -40, 1, 5, 1)
  display.drawRectangle(44, road_lines_y + -20, 1, 5, 1)
  display.drawRectangle(44, road_lines_y + 0, 1, 5, 1)
  display.drawRectangle(44, road_lines_y + 20, 1, 5, 1)
  display.drawRectangle(44, road_lines_y + 40, 1, 5, 1)
  display.drawRectangle(44, road_lines_y + 60, 1, 5, 1)
  display.drawRectangle(44, road_lines_y + 80, 1, 5, 1)

# Describe this function...
def draw_car_2():
  global car_1_x, car_1_y, car_2_x, car_2_y, player_car, Main_menu, truck_x, score, road_lines_y, car_1, car_2, odd_or_even, truck_y, player_car_x, truck
  car_2_y = (car_2_y if isinstance(car_2_y, Number) else 0) + 1
  car_2.y = car_2_y
  display.drawSprite(car_2)

# Describe this function...
def draw_truck():
  global car_1_x, car_1_y, car_2_x, car_2_y, player_car, Main_menu, truck_x, score, road_lines_y, car_1, car_2, odd_or_even, truck_y, player_car_x, truck
  if truck_x == 12:
    if odd_or_even % 2 == 0:
      truck_y = (truck_y if isinstance(truck_y, Number) else 0) + 1
      truck.y = truck_y
      display.drawSprite(truck)
    if odd_or_even % 2 == 1:
      truck.y = truck_y
      display.drawSprite(truck)
    odd_or_even = (odd_or_even if isinstance(odd_or_even, Number) else 0) + 1
  if truck_x == 44:
    if odd_or_even % 2 == 0:
      truck_y = (truck_y if isinstance(truck_y, Number) else 0) + 1
      truck.y = truck_y
      display.drawSprite(truck)
    if odd_or_even % 2 == 1:
      truck.y = truck_y
      display.drawSprite(truck)
    odd_or_even = (odd_or_even if isinstance(odd_or_even, Number) else 0) + 1

# Describe this function...
def draw_car_1():
  global car_1_x, car_1_y, car_2_x, car_2_y, player_car, Main_menu, truck_x, score, road_lines_y, car_1, car_2, odd_or_even, truck_y, player_car_x, truck
  car_1_y = (car_1_y if isinstance(car_1_y, Number) else 0) + 1
  car_1.y = car_1_y
  display.drawSprite(car_1)

# Describe this function...
def score2():
  global car_1_x, car_1_y, car_2_x, car_2_y, player_car, Main_menu, truck_x, score, road_lines_y, car_1, car_2, odd_or_even, truck_y, player_car_x, truck
  display.drawText(str(score), 0, 0, 1)

# Describe this function...
def car_1_collision_check():
  global car_1_x, car_1_y, car_2_x, car_2_y, player_car, Main_menu, truck_x, score, road_lines_y, car_1, car_2, odd_or_even, truck_y, player_car_x, truck
  if bool(display.getPixel(car_1_x + 4, car_1_y + 5)) == True or bool(display.getPixel(car_1_x + 12, car_1_y + 5)) == True:
    Game_over()
  if bool(display.getPixel(car_1_x + 4, car_1_y + 15)) == True or bool(display.getPixel(car_1_x + 12, car_1_y + 15)) == True:
    Game_over()

# Describe this function...
def car_2_collision_check():
  global car_1_x, car_1_y, car_2_x, car_2_y, player_car, Main_menu, truck_x, score, road_lines_y, car_1, car_2, odd_or_even, truck_y, player_car_x, truck
  if bool(display.getPixel(car_2_x + 4, car_2_y + 15)) == True or bool(display.getPixel(car_2_x + 12, car_2_y + 15)) == True:
    Game_over()
  if bool(display.getPixel(car_2_x + 4, car_2_y + 5)) == True or bool(display.getPixel(car_2_x + 12, car_2_y + 5)) == True:
    Game_over()

# Describe this function...
def truck_collision_check():
  global car_1_x, car_1_y, car_2_x, car_2_y, player_car, Main_menu, truck_x, score, road_lines_y, car_1, car_2, odd_or_even, truck_y, player_car_x, truck
  if bool(display.getPixel(truck_x + 4, truck_y + 32)) == True or bool(display.getPixel(truck_x + 12, truck_y + 32)) == True:
    Game_over()
  truck_side_collision_check()

# Describe this function...
def truck_side_collision_check():
  global car_1_x, car_1_y, car_2_x, car_2_y, player_car, Main_menu, truck_x, score, road_lines_y, car_1, car_2, odd_or_even, truck_y, player_car_x, truck
  if bool(display.getPixel(truck_x + 4, truck_y + 8)) == True or bool(display.getPixel(truck_x + 12, truck_y + 8)) == True:
    Game_over()
  if bool(display.getPixel(truck_x + 3, truck_y + 16)) == True or bool(display.getPixel(truck_x + 13, truck_y + 16)) == True:
    Game_over()
  if bool(display.getPixel(truck_x + 3, truck_y + 24)) == True or bool(display.getPixel(truck_x + 13, truck_y + 24)) == True:
    Game_over()

saveData.setName(globals().get('__file__', 'FAST_EXECUTE').replace('/Games/','').strip('/').split('/')[0].split('.')[0])

# Describe this function...
def Game_over():
  global car_1_x, car_1_y, car_2_x, car_2_y, player_car, Main_menu, truck_x, score, road_lines_y, car_1, car_2, odd_or_even, truck_y, player_car_x, truck
  audio.play(800, 1000)
  if saveData.getItem('high score') == None:
    saveData.setItem('high score', 0)
    saveData.save()
  if saveData.getItem('high score') < score:
    saveData.setItem('high score', score)
    saveData.save()
  while not buttons.buttonA.justPressed():
    display.setFont("/lib/font8x8.bin", 8, 8, display.textSpaceWidth)
    display.fill(0)
    display.drawText(str(score), 32, 10, 1)
    display.drawText(str(saveData.getItem('high score')), 32, 30, 1)
    display.setFont("/lib/font5x7.bin", 5, 7, display.textSpaceWidth)
    display.drawText(str('score'), 20, 0, 1)
    display.drawText(str('high score'), 5, 20, 1)
    display.update()
    display.fill(0)
  Game()


display.setFPS(30)
Main_menu = Sprite(72,40,bytearray([0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,128,128,128,64,64,64,64,64,64,64,64,64,64,64,64,64,64,64,64,128,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,
            0,0,0,0,0,0,0,0,0,0,0,0,0,0,128,128,128,128,128,96,16,8,4,2,1,1,129,192,160,144,136,132,130,130,130,130,130,130,130,130,130,132,136,144,162,197,137,18,36,72,144,160,192,128,128,128,128,128,128,128,128,0,0,0,0,0,0,0,0,0,0,0,
            0,0,0,0,0,0,192,48,72,76,52,2,129,65,160,80,48,48,48,80,160,64,128,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,128,64,160,80,48,48,48,80,160,64,128,1,1,31,34,34,36,248,0,0,0,0,0,
            0,0,0,0,0,0,0,3,4,4,4,4,3,0,3,4,8,8,8,4,3,0,7,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,3,0,3,4,8,8,8,4,3,0,3,4,4,4,4,4,4,3,0,0,0,0,0,
            0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]), Main_menu.x,Main_menu.y,Main_menu.key,Main_menu.mirrorX,Main_menu.mirrorY)
car_2 = Sprite(16,16,bytearray([0,0,0,48,252,222,206,206,206,206,222,252,48,0,0,0,
           0,0,0,24,63,59,51,51,51,51,59,63,24,0,0,0]), car_2.x,car_2.y,car_2.key,car_2.mirrorX,car_2.mirrorY)
car_1 = Sprite(16,16,bytearray([0,0,48,204,2,33,49,49,49,49,33,2,204,48,0,0,
           0,0,24,39,64,68,76,76,76,76,68,64,39,24,0,0]), car_1.x,car_1.y,car_1.key,car_1.mirrorX,car_1.mirrorY)
car_2 = Sprite(16,16,bytearray([0,0,48,204,2,33,49,49,49,49,33,2,204,48,0,0,
           0,0,24,39,64,68,76,76,76,76,68,64,39,24,0,0]), car_2.x,car_2.y,car_2.key,car_2.mirrorX,car_2.mirrorY)
truck = Sprite(16,32,bytearray([0,24,230,1,17,25,25,25,25,25,25,17,1,230,24,0,
            0,248,15,12,12,12,12,12,12,12,12,12,12,15,248,0,
            0,255,0,0,0,0,0,0,0,0,0,0,0,0,255,0,
            0,127,64,64,64,64,64,64,64,64,64,64,64,64,127,0]), truck.x,truck.y,truck.key,truck.mirrorX,truck.mirrorY)
player_car = Sprite(48,16,bytearray([0,0,0,48,252,222,206,206,206,206,222,252,48,0,0,0,0,0,0,192,192,224,240,252,236,206,158,62,252,248,112,0,0,112,248,252,62,158,206,236,252,240,224,192,192,0,0,0,
            0,0,0,24,63,59,51,51,51,51,59,63,24,0,0,0,0,0,7,15,30,60,57,51,31,31,7,3,1,1,0,0,0,0,1,1,3,7,31,31,51,57,60,30,15,7,0,0]), player_car.x,player_car.y,player_car.key,player_car.mirrorX,player_car.mirrorY)
player_car = Sprite(16,16,bytearray([0,0,0,48,252,222,206,206,206,206,222,252,48,0,0,0,0,0,0,24,63,59,51,51,51,51,59,63,24,0,0,0,0,0,0,192,192,224,240,252,236,206,158,62,252,248,112,0,0,0,7,15,30,60,57,51,31,31,7,3,1,1,0,0,0,112,248,252,62,158,206,236,252,240,224,192,192,0,0,0,0,0,1,1,3,7,31,31,51,57,60,30,15,7,0,0]),player_car.x,player_car.y,player_car.key,player_car.mirrorX,player_car.mirrorY)
player_car.key = 0
car_1.key = 0
car_2.key = 0
truck.key = 0
Game()

#### !!!! BLOCKLY EXPORT !!!! ####