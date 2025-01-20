import time
from thumbySaves import saveData
import gc
from thumbySprite import Sprite
from thumbyGraphics import display
Number = int
import thumbyButton as buttons
import io
import random
from thumbyAudio import audio

counter = None
rand_seed = None
fish_qty_rec_var = None
rec_counter = None
list_all_fish = None
font5x6_sprite = None
dwn_arrw = None
bob_idle_spr = None
cast_anim = None
cght_13 = None
fish_list_counter = None
catch_msg = None
fish_spr_1 = None
fish_spr_2 = None
fish_spr_3 = None
fish_spr_4 = None
nav_sprite = None
bob_nibbl_spr = None
cast_anim_fin = None
bob_bite_spr = None
qty = None
narr_fish = None
fish_size_rec_var = None
exclm_point = None
can_catch = None
narr_weights = None
title_bg = None
quest_mark = None
fish_ID = None
exit_nav = None
rand_msg = None
cast_pwr = None
cght_fish_size = None
possible_fish = None
rand_wait = None
rand_nibbles = None
bob_A_hit = None
biome_select = None
cght_fish_dtls = None
weighted_list = None
weighted_fish = None
compltn_countr = None
cast_dir = None
draw_castx = None
display_qty = None
draw_casty = None

def setup_all_fish():
  global list_all_fish
  list_all_fish = [['001', 'river', 'Trout', '30', '70', '5', '20', '60'], ['002', 'river', 'Bass', '20', '80', '4', '40', '90'], ['003', 'river', 'Salmon', '25', '150', '3', '75', '100'], ['004', 'lake', 'Minnow', '5', '20', '5', '10', '55'], ['005', 'lake', 'Carp', '25', '125', '3', '30', '75'], ['006', 'lake', 'Sturgeon', '35', '350', '2', '70', '100'], ['007', 'ocean', 'Flounder', '22', '95', '4', '15', '50'], ['008', 'ocean', 'Tuna', '75', '475', '2', '40', '90'], ['009', 'ocean', 'Shark', '100', '630', '1', '80', '100'], ['010', 'pond', 'Snail', '5', '15', '5', '10', '60'], ['011', 'pond', 'Eel', '20', '85', '5', '30', '98'], ['012', 'pond', 'Goldfish', '5', '25', '1', '75', '100'], ['013', 'all', 'Stick', '15', '60', '3', '0', '35'], ['014', 'secret', 'Bass', '116', '118', '1', '0', '99'], ['015', 'secret', 'Demo Fish', '10', '100', '1', '0', '99'], ['016', 'secret', 'BIG GOLD', '10', '999999', '1', '100', '100']]

def setup_rand():
  global rand_seed
  rand_seed = int(time.ticks_ms())
  random.seed(rand_seed)

saveData.setName(globals().get('__file__', 'FAST_EXECUTE').replace('/Games/','').strip('/').split('/')[0].split('.')[0])

title_bg = Sprite(1,1,bytearray([1]))

def title_screen():
  global counter, title_bg, exit_nav
  if saveData.hasItem('sound_setting') == False:
    saveData.setItem('sound_setting', 1)
    saveData.save()
  gc.collect()
  while True:
    title_bg = Sprite(72,40,bytearray([0,64,160,160,32,160,208,16,16,8,8,4,4,2,2,64,0,0,0,0,0,0,0,4,196,60,0,0,0,0,0,0,8,20,20,4,4,244,228,8,8,8,8,8,8,8,48,192,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,32,32,224,0,0,0,0,0,0,0,255,255,8,8,4,4,0,0,228,156,0,0,140,138,146,98,0,128,224,31,4,2,130,252,0,0,0,0,0,0,128,254,127,1,4,4,4,8,8,8,196,34,17,16,16,32,192,16,16,240,32,16,16,16,224,0,192,32,16,16,16,32,240,15,0,0,0,0,0,0,4,4,5,5,4,4,4,4,4,4,4,4,4,2,2,2,2,2,2,2,2,2,2,2,2,2,2,0,0,0,0,0,23,23,16,16,16,16,16,16,16,16,17,18,20,20,20,18,17,32,39,36,160,32,32,39,36,32,33,34,36,36,36,46,41,32,32,0,0,64,32,48,42,126,0,36,0,0,0,68,74,74,82,38,0,4,66,126,2,2,64,32,48,42,126,0,2,122,18,50,76,0,4,66,126,2,2,0,0,0,0,0,0,0,0,0,0,0,4,10,4,0,16,41,18,1,240,8,40,12,10,10,18,46,194,130,128,64,64,192,64,66,126,74,74,52,0,36,0,0,0,68,74,74,82,38,0,2,126,74,74,98,0,4,66,126,2,2,0,4,66,126,2,2,0,66,126,66,0,2,126,8,50,126,0,60,66,66,86,48,0,68,74,74,82,38,0,0,1,14,20,28,20,4,12,10,1,6,8,16,63,0,0,0,64,160,160,32,160,208,16,16,8,8,4,4,2,2,64,0,0,0,0,0,0,0,4,196,60,0,0,0,0,0,0,8,20,20,4,4,244,228,8,8,8,8,8,8,8,48,192,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,32,32,224,0,0,0,0,0,0,0,255,255,8,8,4,4,0,0,228,156,0,0,140,138,146,98,0,128,224,31,4,2,130,252,0,0,0,0,0,0,128,254,127,1,4,4,4,8,8,8,196,34,17,16,16,32,192,16,16,240,32,16,16,16,224,0,192,32,16,16,16,32,240,15,0,0,0,0,0,0,4,4,5,5,4,4,4,4,4,4,4,4,4,2,2,2,2,2,2,2,2,2,2,2,2,2,2,0,0,0,0,0,23,23,16,16,16,16,16,16,16,16,17,18,20,20,20,18,17,32,39,36,32,160,32,39,36,32,33,34,36,36,36,46,41,32,32,0,0,64,32,48,42,126,0,36,0,0,0,68,74,74,82,38,0,4,66,126,2,2,64,32,48,42,126,0,2,122,18,50,76,0,4,66,126,2,2,0,0,0,0,0,0,0,0,0,0,2,5,2,0,0,8,20,9,2,241,8,40,12,10,10,18,46,194,130,128,64,64,192,64,66,126,74,74,52,0,36,0,0,0,68,74,74,82,38,0,2,126,74,74,98,0,4,66,126,2,2,0,4,66,126,2,2,0,66,126,66,0,2,126,8,50,126,0,60,66,66,86,48,0,68,74,74,82,38,0,0,1,14,20,28,20,4,12,10,1,6,8,16,63,0,0]),title_bg.x,title_bg.y,title_bg.key,title_bg.mirrorX,title_bg.mirrorY)
    while True:
      if exit_nav == 0:
        display.fill(0)
        display.update()
        exit_nav = 1
        biome_select_screen()
      else:
        counter = (counter if isinstance(counter, Number) else 0) + 1
        display.drawSprite(title_bg)
        if counter % 25 == 0:
          title_bg.setFrame(title_bg.getFrame() + 1)
        display.update()
        display.fill(0)
        if buttons.buttonA.justPressed():
          biome_select_screen()
        elif buttons.buttonB.justPressed():
          settings_screen()

dwn_arrw = Sprite(1,1,bytearray([1]))

nav_sprite = Sprite(1,1,bytearray([1]))

def settings_screen():
  global dwn_arrw, nav_sprite
  if buttons.inputJustPressed():
    pass
  dwn_arrw = Sprite(5,4,bytearray([1,7,15,7,1]), dwn_arrw.x,dwn_arrw.y,dwn_arrw.key,dwn_arrw.mirrorX,dwn_arrw.mirrorY)
  nav_sprite = Sprite(8,37,bytearray([0,0,30,5,30,0,0,10,
             0,4,14,14,31,0,0,10,
             8,14,15,14,8,0,0,10,
             0,31,14,14,4,0,0,10,
             0,0,31,21,26,0,0,10]), nav_sprite.x,nav_sprite.y,nav_sprite.key,nav_sprite.mirrorX,nav_sprite.mirrorY)
  dwn_arrw.x = 45
  dwn_arrw.y = 9
  nav_sprite.y = 1
  nav_sprite.x = 8
  while True:
    display.drawSprite(nav_sprite)
    display.setFont("/lib/font3x5.bin", 3, 5, display.textSpaceWidth)
    display.drawText(str('RECORDS'), 20, 1, 1)
    display.drawText(str('SOUND'), 20, 9, 1)
    if int(saveData.getItem('completion_record')) == 1:
      display.drawText(str('SOUND   :CRED'), 20, 9, 1)
      display.drawSprite(dwn_arrw)
    else:
      display.drawText(str('SOUND'), 20, 9, 1)
    display.drawText(str('HOW TO PLAY'), 20, 17, 1)
    display.drawText(str('CLEAR DATA'), 20, 25, 1)
    display.drawText(str('RETURN'), 20, 33, 1)
    display.setFont("/lib/font5x7.bin", 5, 7, display.textSpaceWidth)
    display.update()
    display.fill(0)
    if buttons.buttonA.justPressed():
      records_screen()
    elif buttons.buttonB.justPressed():
      break
    elif buttons.buttonR.justPressed():
      clear_data_screen()
    elif buttons.buttonU.justPressed():
      tutorial_screen()
    elif buttons.buttonL.justPressed():
      sound_screen()
    elif buttons.buttonD.justPressed():
      if int(saveData.getItem('completion_record')) == 1:
        completion_screen()
      else:
        pass
  gc.collect()

quest_mark = Sprite(1,1,bytearray([1]))

def records_screen():
  global rec_counter, fish_qty_rec_var, fish_size_rec_var, quest_mark, fish_ID
  rec_counter = 1
  fish_qty_rec_var = saveData.getItem('fish_qty_record')
  fish_size_rec_var = saveData.getItem('fish_size_record')
  quest_mark = Sprite(36,40,bytearray([0,0,0,0,0,0,0,0,0,0,0,128,128,192,192,192,192,192,192,192,192,192,192,128,128,0,0,0,0,0,0,0,0,0,0,0,
             0,0,0,0,0,0,0,0,0,14,15,7,1,0,0,0,0,0,0,0,0,0,1,1,7,255,252,0,0,0,0,0,0,0,0,0,
             0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,192,224,112,56,28,14,7,3,1,0,0,0,0,0,0,0,0,0,
             0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,63,63,3,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,
             0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,6,15,15,6,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]), quest_mark.x,quest_mark.y,quest_mark.key,quest_mark.mirrorX,quest_mark.mirrorY)
  while True:
    fish_ID = rec_counter
    if len(list_all_fish[int(rec_counter - 1)][2]) >= 7:
      display.setFont("/lib/font3x5.bin", 3, 5, display.textSpaceWidth)
      display.textSpaceWidth = 1
    elif len(list_all_fish[int(rec_counter - 1)][2]) >= 6:
      display.setFont("/lib/font5x7.bin", 5, 7, display.textSpaceWidth)
      display.textSpaceWidth = 0
    else:
      display.setFont("/lib/font5x7.bin", 5, 7, display.textSpaceWidth)
      display.textSpaceWidth = 1
    if fish_qty_rec_var[int(rec_counter - 1)] == 0:
      display.setFont("/lib/font5x7.bin", 5, 7, display.textSpaceWidth)
      display.textSpaceWidth = 1
      quest_mark.x = 36
      display.drawSprite(quest_mark)
      display.drawText(str('???'), 0, 0, 1)
    else:
      fish_sprite_by_id()
      display.drawText(str(list_all_fish[int(rec_counter - 1)][2]), 0, 0, 1)
    display.setFont("/lib/font5x7.bin", 5, 7, display.textSpaceWidth)
    display.textSpaceWidth = 1
    display.drawText(str(str(list_all_fish[int(rec_counter - 1)][1])), 0, 8, 1)
    display.drawText(str(str(fish_qty_rec_var[int(rec_counter - 1)]) + ' qty'), 0, 17, 1)
    if fish_size_rec_var[int(rec_counter - 1)] > 99999:
      display.drawText(str(str(int(fish_size_rec_var[int(rec_counter - 1)] / 10000) / 10) + 'km'), 0, 25, 1)
    elif fish_size_rec_var[int(rec_counter - 1)] > 99:
      display.drawText(str(str(int(fish_size_rec_var[int(rec_counter - 1)] / 10) / 10) + 'm'), 0, 25, 1)
    else:
      display.drawText(str(str(fish_size_rec_var[int(rec_counter - 1)]) + 'cm'), 0, 25, 1)
    display.setFont("/lib/font3x5.bin", 3, 5, display.textSpaceWidth)
    display.drawText(str(''.join([str(x) for x in ['< ', rec_counter, '/', len(list_all_fish), ' >']])), 0, 35, 1)
    display.update()
    display.fill(0)
    if buttons.buttonL.justPressed():
      rec_counter = (rec_counter if isinstance(rec_counter, Number) else 0) + -1
      if rec_counter < 1:
        rec_counter = len(list_all_fish)
    elif buttons.buttonR.justPressed():
      rec_counter = (rec_counter if isinstance(rec_counter, Number) else 0) + 1
      if rec_counter > len(list_all_fish):
        rec_counter = 1
    elif buttons.actionJustPressed():
      break
  if buttons.inputJustPressed():
    pass
  gc.collect()

def sound_screen():
  while True:
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
    if buttons.buttonA.justPressed():
      if int(saveData.getItem('sound_setting')) == 1:
        saveData.setItem('sound_setting', int(0))
        saveData.save()
        display.drawText(str('SOUND OFF'), 5, 10, 1)
        display.drawText(str('SAVED'), 5, 20, 1)
        display.update()
        display.fill(0)
        time.sleep(1)
        break
      elif int(saveData.getItem('sound_setting')) == 0:
        saveData.setItem('sound_setting', int(1))
        saveData.save()
        display.drawText(str('SOUND ON'), 5, 10, 1)
        display.drawText(str('SAVED'), 5, 20, 1)
        display.update()
        display.fill(0)
        time.sleep(1)
        break
    elif buttons.buttonB.justPressed():
      break

def clear_data_screen():
  global list_all_fish
  gc.collect()
  display.setFont("/lib/font8x8.bin", 8, 8, display.textSpaceWidth)
  display.drawText(str('REALLY'), 9, 0, 1)
  display.setFont("/lib/font5x7.bin", 5, 7, display.textSpaceWidth)
  display.drawText(str('DELETE'), 16, 10, 1)
  display.drawText(str('SAVE DATA?'), 8, 19, 1)
  display.drawText(str('A:yes B:no'), 6, 31, 1)
  display.update()
  display.fill(0)
  while True:
    if buttons.buttonB.justPressed():
      break
    elif buttons.buttonA.justPressed():
      saveData.delItem('fish_qty_record')
      saveData.delItem('fish_size_record')
      saveData.delItem('existing_game')
      saveData.setItem('completion_record', 0)
      saveData.save()
      saveData.setItem('fish_size_record', [0] * len(list_all_fish))
      saveData.save()
      saveData.setItem('fish_qty_record', [0] * len(list_all_fish))
      saveData.save()
      display.setFont("/lib/font5x7.bin", 5, 7, display.textSpaceWidth)
      display.drawText(str('DATA'), 5, 10, 1)
      display.drawText(str('CLEARED'), 5, 20, 1)
      display.update()
      display.fill(0)
      time.sleep(2)
      break
  gc.collect()

def tutorial_screen():
  gc.collect()
  environments.tutorial_screen()
  gc.collect()

font5x6_sprite = Sprite(1,1,bytearray([1]))

def __setFontFromBytes__(width, height, data):
    if width > len(data) or height > 8:
        return
    display.textBitmapFile = io.BytesIO(data)
    display.textWidth = width
    display.textHeight = height
    display.textBitmap = bytearray(width)
    display.textCharCount = len(data) // width

def completion_screen():
  global font5x6_sprite
  __setFontFromBytes__(5, 6, font5x6_sprite.bitmap)
  display.drawText(str('CONGRATS!'), 2, 1, 1)
  display.drawText(str('You caught'), 2, 13, 1)
  display.drawText(str('every fish'), 2, 22, 1)
  display.drawText(str('in the game!'), 2, 31, 1)
  display.update()
  display.fill(0)
  while True:
    if buttons.inputJustPressed():
      break
  display.drawText(str('WAY TO GO!'), 2, 1, 1)
  display.drawText(str('You are a'), 2, 13, 1)
  display.drawText(str('fin-tastic'), 2, 22, 1)
  display.drawText(str('fisher!'), 2, 31, 1)
  display.update()
  display.fill(0)
  while True:
    if buttons.inputJustPressed():
      break
  display.drawText(str('CREDITS'), 2, 1, 1)
  display.drawLine(0, 9, 72, 9, 1)
  display.setFont("/lib/font3x5.bin", 3, 5, display.textSpaceWidth)
  display.drawText(str('GAME BY:'), 2, 12, 1)
  display.drawText(str('marigoldfish'), 2, 18, 1)
  display.drawText(str('5KM GOLDFISH:'), 2, 27, 1)
  display.drawText(str('UnRedKnown (idea)'), 2, 34, 1)
  display.update()
  display.fill(0)
  while True:
    if buttons.inputJustPressed():
      break

def biome_select_screen():
  global fish_qty_rec_var, cght_13, qty, dwn_arrw, nav_sprite, biome_select
  fish_qty_rec_var = saveData.getItem('fish_qty_record')
  cght_13 = True
  # Check if fish 1-13 have been caught, to unlock secret pond
  for qty in fish_qty_rec_var[ : 13]:
    if qty < 1:
      cght_13 = False
      break
    else:
      continue
  dwn_arrw = Sprite(5,4,bytearray([1,7,15,7,1]), dwn_arrw.x,dwn_arrw.y,dwn_arrw.key,dwn_arrw.mirrorX,dwn_arrw.mirrorY)
  nav_sprite = Sprite(8,37,bytearray([0,0,30,5,30,0,0,10,
             0,4,14,14,31,0,0,10,
             8,14,15,14,8,0,0,10,
             0,31,14,14,4,0,0,10,
             0,0,31,21,26,0,0,10]), nav_sprite.x,nav_sprite.y,nav_sprite.key,nav_sprite.mirrorX,nav_sprite.mirrorY)
  dwn_arrw.x = 45
  dwn_arrw.y = 9
  nav_sprite.x = 8
  nav_sprite.y = 1
  display.drawSprite(nav_sprite)
  display.setFont("/lib/font3x5.bin", 3, 5, display.textSpaceWidth)
  display.drawText(str('RIVER'), 20, 1, 1)
  if cght_13 == True:
    display.drawText(str('LAKE    :???'), 20, 9, 1)
    display.drawSprite(dwn_arrw)
  else:
    display.drawText(str('LAKE'), 20, 9, 1)
  display.drawText(str('OCEAN'), 20, 17, 1)
  display.drawText(str('POND'), 20, 25, 1)
  display.drawText(str('RETURN'), 20, 33, 1)
  display.setFont("/lib/font5x7.bin", 5, 7, display.textSpaceWidth)
  display.update()
  display.fill(0)
  while True:
    if buttons.buttonA.justPressed():
      biome_select = 'river'
      break
    elif buttons.buttonB.justPressed():
      biome_select = 'menu'
      break
    elif buttons.buttonL.justPressed():
      biome_select = 'lake'
      break
    elif buttons.buttonU.justPressed():
      biome_select = 'ocean'
      break
    elif buttons.buttonR.justPressed():
      biome_select = 'pond'
      break
    elif buttons.buttonD.justPressed():
      if cght_13 == True:
        biome_select = 'secret'
        break
      else:
        pass
  if biome_select == 'river':
    river_screen()
  elif biome_select == 'lake':
    lake_screen()
  elif biome_select == 'ocean':
    ocean_screen()
  elif biome_select == 'pond':
    pond_screen()
  elif biome_select == 'secret':
    secret_screen()
  else:
    pass
  gc.collect()

def river_screen():
  gc.collect()
  environments.river_screen()
  gc.collect()
  cast_screen()

def lake_screen():
  gc.collect()
  environments.lake_screen()
  gc.collect()
  cast_screen()

def ocean_screen():
  gc.collect()
  environments.ocean_screen()
  gc.collect()
  cast_screen()

def pond_screen():
  gc.collect()
  environments.pond_screen()
  gc.collect()
  cast_screen()

def secret_screen():
  gc.collect()
  environments.secret_screen()
  gc.collect()
  cast_screen()

cast_anim = Sprite(1,1,bytearray([1]))

cast_anim_fin = Sprite(1,1,bytearray([1]))

exclm_point = Sprite(1,1,bytearray([1]))

def cast_screen():
  global cast_anim, cast_anim_fin, exclm_point, cast_dir, draw_castx, draw_casty, cast_pwr
  gc.collect()
  cast_anim = Sprite(32,37,bytearray([0,0,128,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,2,7,2,1,6,8,48,64,128,0,0,0,0,48,72,132,132,132,72,48,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,2,4,24,40,232,44,66,255,66,124,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,252,3,28,224,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,16,31,0,0,17,30,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,8,28,8,0,248,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,63,192,48,72,132,132,132,72,48,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,15,248,108,70,255,50,12,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,252,3,28,224,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,16,31,0,0,17,30,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,2,199,50,12,2,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,192,240,76,135,132,132,72,48,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,12,3,0,1,14,18,255,10,4,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,252,3,28,224,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,16,31,0,0,17,30,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,128,128,64,64,32,32,144,208,128,0,0,0,0,0,0,0,0,0,64,64,32,224,240,72,132,132,132,76,50,2,1,1,0,0,0,0,0,0,0,1,0,0,0,0,0,0,0,0,0,0,0,0,7,5,31,20,10,255,6,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,252,3,28,224,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,16,31,0,0,17,30,0,0,0,0,0,0,0,0,0,0,0,0]),cast_anim.x,cast_anim.y,cast_anim.key,cast_anim.mirrorX,cast_anim.mirrorY)
  cast_anim_fin = Sprite(32,37,bytearray([64,128,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,
             0,0,3,4,8,48,64,128,0,0,0,0,0,48,72,132,132,132,72,48,0,0,0,0,0,0,0,0,0,0,0,0,
             0,0,0,0,0,0,0,0,3,4,8,48,120,168,36,34,255,34,60,0,0,0,0,0,0,0,0,0,0,0,0,0,
             0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,252,3,28,224,0,0,0,0,0,0,0,0,0,0,0,0,0,
             0,0,0,0,0,0,0,0,0,0,0,0,0,0,16,31,0,0,17,30,0,0,0,0,0,0,0,0,0,0,0,0]), cast_anim_fin.x,cast_anim_fin.y,cast_anim_fin.key,cast_anim_fin.mirrorX,cast_anim_fin.mirrorY)
  exclm_point = Sprite(2,8,bytearray([223,223]), exclm_point.x,exclm_point.y,exclm_point.key,exclm_point.mirrorX,exclm_point.mirrorY)
  if saveData.hasItem('existing_game') == False:
    tutorial_screen()
    saveData.setItem('existing_game', True)
    saveData.save()
  setup_rand()
  display.fill(0)
  display.update()
  time.sleep(0.1)
  cast_anim.key = 0
  cast_anim_fin.key = 0
  cast_anim.x = 40
  cast_anim.y = 3
  cast_anim_fin.x = 40
  cast_anim_fin.y = 3
  exclm_point.x = 65
  exclm_point.y = 20
  cast_anim.setFrame(0)
  cast_dir = 1
  cast_pwr = -1
  # Adjust the speed of the casting bar (default 35)
  display.setFPS(35)
  if buttons.inputJustPressed():
    pass
  while True:
    display.drawRectangle(3, 28, 46, 11, 1)
    display.setFont("/lib/font5x7.bin", 5, 7, display.textSpaceWidth)
    display.drawText(str('HOLD A'), 8, 30, 1)
    if buttons.buttonA.pressed():
      display.drawFilledRectangle(5, 29, 43, 9, 0)
    display.drawFilledRectangle(4, 28, min(max(int((cast_pwr / 100) * 44), 0), 44), 11, 1)
    display.drawSprite(cast_anim)
    if buttons.buttonA.justPressed():
      pass
    if buttons.buttonA.pressed():
      cast_pwr = (cast_pwr if isinstance(cast_pwr, Number) else 0) + cast_dir * 2
      display.drawLine(18, 30, 18, 36, 0)
      display.drawLine(33, 30, 33, 36, 0)
    # Max cast power is >100, to allow a "perfect cast" window without being frame-perfect.
    if cast_pwr <= 0:
      cast_pwr = 0
      cast_dir = 1
    elif cast_pwr >= 106:
      cast_dir = -1
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
    if not buttons.buttonA.justPressed() and not buttons.buttonA.pressed() and cast_pwr > 0:
      break
    display.update()
    display.fill(0)
  display.fill(0)
  draw_castx = 39
  draw_casty = 2
  if cast_pwr > 100:
    cast_pwr = 100
  display.setFPS(25 + int(cast_pwr / 5))
  while not draw_castx == 0:
    display.drawSprite(cast_anim_fin)
    display.drawLine(39, 8, draw_castx, 2, 1)
    draw_castx = (draw_castx if isinstance(draw_castx, Number) else 0) + -1
    display.update()
    display.fill(0)
  display.setFPS(display.frameRate - int(display.frameRate * 0.1))
  while not draw_casty == 14:
    display.drawSprite(cast_anim_fin)
    display.drawLine(39, 8, draw_castx, draw_casty, 1)
    draw_casty = (draw_casty if isinstance(draw_casty, Number) else 0) + 1
    display.update()
    display.fill(0)
  display.setFPS(30)
  draw_casty = (draw_casty if isinstance(draw_casty, Number) else 0) + 1
  time.sleep(0.5)
  display.drawSprite(cast_anim_fin)
  display.drawLine(39, 8, draw_castx, draw_casty, 1)
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
  if buttons.inputJustPressed():
    pass
  gc.collect()
  fishing_screen()

bob_idle_spr = Sprite(1,1,bytearray([1]))

def bobber_idle_screen():
  global counter, bob_idle_spr
  display.fill(0)
  display.drawSprite(bob_idle_spr)
  counter = (counter if isinstance(counter, Number) else 0) + 1
  if counter % 22 == 0:
    bob_idle_spr.setFrame(bob_idle_spr.getFrame() + 1)
  display.update()
  display.fill(0)

bob_bite_spr = Sprite(1,1,bytearray([1]))

def bobber_bite_screen():
  global counter, bob_bite_spr
  counter = (counter if isinstance(counter, Number) else 0) + 1
  display.fill(0)
  display.drawSprite(bob_bite_spr)
  if counter % 10 == 0:
    bob_bite_spr.setFrame(bob_bite_spr.getFrame() + 1)
  display.update()
  display.fill(0)

bob_nibbl_spr = Sprite(1,1,bytearray([1]))

def bobber_nibble_screen():
  global counter, rand_seed, bob_nibbl_spr
  display.fill(0)
  counter = (counter if isinstance(counter, Number) else 0) + 1
  display.drawSprite(bob_nibbl_spr)
  if counter % 15 == 0:
    bob_nibbl_spr.setFrame(bob_nibbl_spr.getFrame() + 1)
  display.update()
  display.fill(0)

def fishing_screen():
  global counter, bob_idle_spr, bob_nibbl_spr, bob_bite_spr, can_catch, rand_wait, rand_nibbles, bob_A_hit
  gc.collect()
  bob_idle_spr = Sprite(72,40,bytearray([0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,128,128,64,64,64,64,32,32,32,16,16,16,8,8,4,4,4,2,2,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,2,0,2,2,1,1,2,4,4,4,0,0,0,0,0,0,0,0,0,0,128,224,240,240,248,248,252,252,253,252,252,248,248,240,240,224,128,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,16,16,16,16,32,32,32,16,16,16,32,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,126,143,15,15,31,31,31,63,63,63,63,63,63,31,31,15,15,15,254,128,128,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,2,0,1,1,1,1,1,2,2,2,1,1,1,1,1,1,2,2,2,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,2,2,1,1,1,1,2,2,2,2,0,2,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,128,128,128,128,64,64,64,32,32,32,16,16,8,8,8,4,4,2,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,2,0,2,2,4,4,2,2,1,1,0,0,0,0,0,0,0,0,0,0,0,0,192,224,224,240,240,248,248,250,249,249,240,240,224,224,192,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,32,0,32,32,32,16,16,16,32,32,32,16,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,128,252,159,159,31,63,63,63,127,127,127,127,127,127,63,63,159,159,159,252,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,0,0,0,0,1,1,1,1,1,1,2,2,2,2,2,1,0,0,0,0,1,1,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,2,2,4,4,4,4,2,2,2,2,0,2,0,0,0,0,0,0,0,0,0,0,0,0]),bob_idle_spr.x,bob_idle_spr.y,bob_idle_spr.key,bob_idle_spr.mirrorX,bob_idle_spr.mirrorY)
  bob_nibbl_spr = Sprite(72,40,bytearray([0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,128,128,64,64,32,32,16,16,8,8,4,4,2,2,1,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,2,0,2,2,1,1,2,4,4,4,0,0,0,0,0,0,0,0,0,0,0,128,192,192,224,224,240,240,244,244,242,226,225,193,192,128,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,16,16,16,16,32,32,32,16,16,16,32,0,0,0,0,0,0,0,0,0,0,32,32,16,16,16,8,8,0,0,0,72,16,128,252,190,191,191,255,255,255,255,255,255,255,255,255,255,255,191,191,190,248,0,64,32,0,8,8,8,16,16,0,0,0,0,64,128,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,16,16,16,17,17,33,32,32,32,32,32,0,1,1,1,33,33,33,33,33,33,32,32,32,33,17,17,17,16,16,16,16,8,8,8,4,4,4,2,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,2,2,1,1,1,1,2,2,2,2,0,2,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,128,128,64,64,32,32,16,8,8,4,4,2,2,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,2,0,2,2,4,4,2,2,1,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,128,128,192,192,208,200,200,132,132,2,2,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,32,0,32,32,32,16,16,16,32,32,32,16,0,0,0,0,0,0,0,0,0,32,16,16,8,8,8,4,4,0,0,32,36,12,128,224,248,254,255,255,255,255,255,255,255,255,255,255,255,255,255,254,248,224,0,0,32,48,16,0,0,0,0,0,0,0,0,0,64,128,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,32,32,33,33,33,32,64,64,64,65,65,1,1,1,1,67,67,67,67,67,65,65,65,65,33,35,34,34,32,32,32,32,16,16,16,8,8,8,4,2,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,2,2,4,4,4,4,2,2,2,2,0,2,0,0,0,0,0,0,0,0,0,0,0,0]),bob_nibbl_spr.x,bob_nibbl_spr.y,bob_nibbl_spr.key,bob_nibbl_spr.mirrorX,bob_nibbl_spr.mirrorY)
  bob_bite_spr = Sprite(72,40,bytearray([0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,128,64,32,16,8,4,2,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,2,0,2,2,1,1,2,4,4,4,0,0,0,0,0,0,0,0,128,128,128,128,128,128,128,128,128,128,128,128,128,128,0,0,0,0,128,64,32,16,8,4,2,1,0,0,0,0,0,0,0,0,0,0,0,0,0,16,16,16,16,32,32,32,16,16,16,32,0,0,128,192,192,192,192,192,192,192,192,192,192,192,192,128,16,17,17,1,1,1,0,0,0,12,28,28,60,120,224,12,156,64,32,144,200,100,50,49,56,24,0,0,16,17,17,17,18,34,34,2,2,4,4,132,8,8,16,16,32,32,64,0,0,0,0,0,0,0,0,0,0,0,255,255,192,192,255,255,192,192,255,255,192,192,255,255,0,0,32,32,32,32,64,64,64,64,64,64,0,2,3,3,67,66,66,64,64,66,66,70,68,64,32,32,32,32,32,32,32,16,16,16,8,8,8,4,3,0,0,0,0,128,64,48,8,0,0,0,0,0,0,0,0,0,7,15,12,12,15,15,12,12,15,15,12,12,15,7,16,16,16,16,16,16,32,32,32,32,32,32,32,32,32,32,32,32,32,32,32,32,32,32,32,32,0,16,16,16,16,16,0,0,8,8,8,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,128,96,16,8,4,2,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,2,0,2,2,4,4,2,2,1,1,0,0,0,0,128,128,128,128,128,128,128,128,128,128,64,64,64,64,64,64,64,64,64,0,0,0,128,64,32,16,8,4,130,129,128,0,0,0,0,0,0,0,0,0,0,0,0,32,0,32,32,32,16,16,16,32,32,32,16,0,0,128,192,192,192,192,192,192,192,192,192,208,208,208,136,8,8,0,0,0,0,0,8,28,28,28,24,56,48,1,7,142,64,32,16,8,6,49,24,28,14,14,4,0,8,8,16,17,17,17,1,1,2,2,2,132,4,8,8,16,16,32,64,0,0,0,0,0,0,0,0,0,0,255,255,192,192,255,255,192,192,255,255,192,192,255,255,0,0,64,64,64,64,64,128,128,128,128,128,0,1,1,1,130,130,130,130,128,128,132,156,152,64,64,64,64,64,64,64,64,32,32,32,16,16,16,8,4,3,0,0,0,0,128,64,48,8,0,0,0,0,0,0,0,0,7,15,12,12,15,15,12,12,15,15,12,12,15,7,32,32,32,32,32,32,64,64,64,64,64,64,64,64,64,64,64,64,64,64,64,64,64,64,64,64,0,32,32,32,32,32,0,0,32,32,32,32,16,16,0,0,0,0,0,1,0,0,0,0,0,0,0,0,0,0]),bob_bite_spr.x,bob_bite_spr.y,bob_bite_spr.key,bob_bite_spr.mirrorX,bob_bite_spr.mirrorY)
  counter = 0
  display.setFPS(30)
  can_catch = 0
  rand_wait = random.randint(3, 10)
  rand_nibbles = random.randint(1, 4)
  bob_A_hit = False
  display.setFont("/lib/font5x7.bin", 5, 7, display.textSpaceWidth)
  for count11 in range(1):
    for count in range(int(rand_wait * 30)):
      bobber_idle_screen()
      if buttons.buttonA.justPressed():
        bob_A_hit = True
        break
    display.fill(0)
    if bob_A_hit == True:
      eval_screen()
      break
    # 0 = no bite
    # 1 = too early
    # 2 = successful catch
    # 3 = too late
    can_catch = 1
    for count4 in range(int(rand_nibbles)):
      for count2 in range(30):
        bobber_nibble_screen()
        if buttons.buttonA.justPressed():
          bob_A_hit = True
          break
      display.fill(0)
      if bob_A_hit == True:
        break
      for count3 in range(int(30 * random.randint(1, 3))):
        bobber_idle_screen()
        if buttons.buttonA.justPressed():
          bob_A_hit = True
          break
      display.fill(0)
      if bob_A_hit == True:
        break
    if bob_A_hit == True:
      eval_screen()
      break
    for count5 in range(10):
      display.drawSprite(bob_nibbl_spr)
      display.update()
      display.fill(0)
      if buttons.buttonA.justPressed():
        bob_A_hit = True
        break
    if bob_A_hit == True:
      eval_screen()
      break
    bob_nibbl_spr.setFrame(1)
    for count6 in range(10):
      display.drawSprite(bob_nibbl_spr)
      display.update()
      display.fill(0)
      if buttons.buttonA.justPressed():
        bob_A_hit = True
        break
    if bob_A_hit == True:
      eval_screen()
      break
    # !!! The magic is about to happen! You can catch this fish!
    can_catch = 2
    if int(saveData.getItem('sound_setting')) == 1:
      audio.play(800, 150)
    for count7 in range(30):
      bobber_bite_screen()
      if buttons.buttonA.justPressed():
        bob_A_hit = True
        break
    if bob_A_hit == True:
      eval_screen()
      break
    for count8 in range(10):
      display.drawSprite(bob_nibbl_spr)
      display.update()
      display.fill(0)
      if buttons.buttonA.justPressed():
        bob_A_hit = True
        break
    if bob_A_hit == True:
      eval_screen()
      break
    bob_nibbl_spr.setFrame(0)
    can_catch = 3
    for count9 in range(10):
      display.drawSprite(bob_nibbl_spr)
      display.update()
      display.fill(0)
      if buttons.buttonA.justPressed():
        bob_A_hit = True
        break
    if bob_A_hit == True:
      eval_screen()
      break
    for count10 in range(int(display.frameRate * 5)):
      bobber_idle_screen()
      if buttons.buttonA.justPressed():
        bob_A_hit = True
        break
    eval_screen()
    break

def pick_fish():
  global fish_list_counter, narr_fish, narr_weights, fish_size_rec_var, fish_qty_rec_var, possible_fish, list_all_fish, biome_select, weighted_list, weighted_fish, fish_ID, cght_fish_dtls, cght_fish_size, cast_pwr
  gc.collect()
  fish_list_counter = 1
  narr_fish = ''
  narr_weights = ''
  fish_size_rec_var = saveData.getItem('fish_size_record')
  fish_qty_rec_var = saveData.getItem('fish_qty_record')
  for possible_fish in list_all_fish:
    if possible_fish[1] == biome_select or possible_fish[1] == 'all':
      if cast_pwr >= int(possible_fish[6]) and cast_pwr <= int(possible_fish[7]):
        narr_fish = str(narr_fish) + str(possible_fish[0])
        narr_fish = str(narr_fish) + ';'
        narr_weights = str(narr_weights) + str(possible_fish[5])
        narr_weights = str(narr_weights) + ';'
  narr_fish = narr_fish[:-1]
  narr_weights = narr_weights[:-1]
  narr_fish = narr_fish.split(';')
  narr_weights = narr_weights.split(';')
  weighted_list = ''
  for weighted_fish in narr_fish:
    for count12 in range(int(narr_weights[int(fish_list_counter - 1)])):
      weighted_list = str(weighted_list) + str(narr_fish[int(fish_list_counter - 1)])
      weighted_list = str(weighted_list) + ';'
    fish_list_counter = (fish_list_counter if isinstance(fish_list_counter, Number) else 0) + 1
  weighted_list = weighted_list[:-1]
  weighted_list = weighted_list.split(';')
  fish_ID = random.choice(weighted_list)
  cght_fish_dtls = list_all_fish[int(int(fish_ID) - 1)]
  cght_fish_size = random.randint(int(cght_fish_dtls[3]), int(cght_fish_dtls[4]))
  if fish_size_rec_var[int(int(fish_ID) - 1)] < cght_fish_size:
    fish_size_rec_var[int(int(fish_ID) - 1)] = cght_fish_size
  fish_qty_rec_var[int(int(fish_ID) - 1)] = fish_qty_rec_var[int(int(fish_ID) - 1)] + 1
  saveData.setItem('fish_size_record', fish_size_rec_var)
  saveData.save()
  saveData.setItem('fish_qty_record', fish_qty_rec_var)
  saveData.save()
  fish_size_rec_var = saveData.getItem('fish_size_record')
  fish_qty_rec_var = saveData.getItem('fish_qty_record')
  gc.collect()

def display_caught_fish():
  global catch_msg, font5x6_sprite, cght_fish_size, rand_msg, cght_fish_dtls,compltn_countr, fish_qty_rec_var, list_all_fish, fish_ID, fish_size_rec_var,display_qty, qty
  gc.collect()
  catch_msg = [['Good', 'catch!'], ['Wow!', "It's a"], ['Catch!', "It's a"], ['You', 'got a'], ['Cool', 'catch!'], ["That's", 'sure a'], ['Seems', 'fishy!']]
  __setFontFromBytes__(5, 6, font5x6_sprite.bitmap)
  if cght_fish_size == 69:
    display.drawText(str('NICE'), 1, 1, 1)
    display.drawText(str(';)'), 1, 10, 1)
  else:
    rand_msg = random.randint(1, len(catch_msg))
    display.drawText(str(catch_msg[int(rand_msg - 1)][0]), 1, 1, 1)
    display.drawText(str(catch_msg[int(rand_msg - 1)][1]), 1, 9, 1)
  display.setFont("/lib/font5x7.bin", 5, 7, display.textSpaceWidth)
  if cght_fish_size > 99999:
    display.drawText(str(str(int(cght_fish_size / 10000) / 10) + 'km'), 1, 22, 1)
  elif cght_fish_size > 99:
    display.drawText(str(str(int(cght_fish_size / 10) / 10) + 'm'), 1, 22, 1)
  else:
    display.drawText(str(str(cght_fish_size) + 'cm'), 1, 22, 1)
  if len(cght_fish_dtls[2]) >= 7:
    display.setFont("/lib/font3x5.bin", 3, 5, display.textSpaceWidth)
    display.textSpaceWidth = 1
  elif len(cght_fish_dtls[2]) >= 6:
    __setFontFromBytes__(5, 6, font5x6_sprite.bitmap)
    display.textSpaceWidth = 0
  else:
    __setFontFromBytes__(5, 6, font5x6_sprite.bitmap)
    display.textSpaceWidth = 1
  display.drawText(str(str(cght_fish_dtls[2]) + '!'), 1, 32, 1)
  fish_sprite_by_id()
  display.update()
  display.fill(0)
  gc.collect()
  if int(saveData.getItem('sound_setting')) == 1:
    time.sleep(0.1)
    audio.playBlocking(1046, 190)
    audio.playBlocking(988, 180)
    audio.playBlocking(1046, 200)
    time.sleep(0.1)
    audio.play(2093, 250)
  while True:
    if buttons.inputJustPressed():
      break
  if int(saveData.getItem('completion_record')) == 0:
    compltn_countr = 0
    fish_qty_rec_var = saveData.getItem('fish_qty_record')
    for qty in fish_qty_rec_var:
      if qty > 0:
        compltn_countr = (compltn_countr if isinstance(compltn_countr, Number) else 0) + 1
  if compltn_countr == len(list_all_fish):
    completion_screen()
    saveData.setItem('completion_record', 1)
    saveData.save()
  __setFontFromBytes__(5, 6, font5x6_sprite.bitmap)
  display.textSpaceWidth = 1
  display.drawText(str(str(cght_fish_dtls[2])), 2, 0, 1)
  display.setFont("/lib/font5x7.bin", 5, 7, display.textSpaceWidth)
  display.drawLine(0, 8, 72, 8, 1)
  if cght_fish_size > 99999:
    display.drawText(str(''.join([str(x2) for x2 in ['Size: ', int(cght_fish_size / 10000) / 10, 'km']])), 2, 10, 1)
  elif cght_fish_size > 99:
    display.drawText(str(''.join([str(x3) for x3 in ['Size: ', int(cght_fish_size / 10) / 10, 'm']])), 2, 10, 1)
  else:
    display.drawText(str(''.join([str(x4) for x4 in ['Size: ', cght_fish_size, 'cm']])), 2, 10, 1)
  if cght_fish_size == int(list_all_fish[int(int(fish_ID) - 1)][4]):
    display.setFont("/lib/font3x5.bin", 3, 5, display.textSpaceWidth)
    display.drawText(str('MAX SIZE!!'), 15, 18, 1)
    display.setFont("/lib/font5x7.bin", 5, 7, display.textSpaceWidth)
  elif saveData.hasItem('fish_size_record') == False or cght_fish_size > int(fish_size_rec_var[int(int(fish_ID) - 1)]) - 1:
    display.setFont("/lib/font3x5.bin", 3, 5, display.textSpaceWidth)
    display.drawText(str('NEW RECORD!'), 15, 18, 1)
    display.setFont("/lib/font5x7.bin", 5, 7, display.textSpaceWidth)
  if fish_qty_rec_var[int(int(fish_ID) - 1)] == 1:
    display.drawText(str('First Catch!'), 2, 25, 1)
  else:
    display_qty = fish_qty_rec_var[int(int(fish_ID) - 1)]
    display.drawText(str(str(display_qty) + ' caught'), 2, 25, 1)
  display.setFont("/lib/font3x5.bin", 3, 5, display.textSpaceWidth)
  display.drawText(str('A: AGAIN  B: MENU'), 2, 35, 1)
  display.update()
  display.fill(0)

fish_spr_1 = Sprite(1,1,bytearray([1]))

fish_spr_2 = Sprite(1,1,bytearray([1]))

fish_spr_3 = Sprite(1,1,bytearray([1]))

fish_spr_4 = Sprite(1,1,bytearray([1]))

def fish_sprite_by_id():
  global fish_spr_1, fish_spr_2, fish_spr_3, fish_spr_4, fish_ID
  if int(fish_ID) <= 4:
    fish_spr_1 = Sprite(36,40,bytearray([0,200,84,84,162,162,66,82,170,18,194,66,66,34,36,252,8,136,16,16,16,32,32,64,128,0,0,0,0,0,0,0,0,0,0,0,0,0,1,2,4,4,9,17,50,43,68,132,228,4,10,141,14,31,31,62,124,248,240,224,192,129,2,12,52,200,8,16,16,32,32,192,0,0,0,0,0,0,0,0,0,0,0,0,15,16,16,8,7,8,16,32,64,224,1,3,7,15,31,62,248,240,15,240,16,14,1,0,0,0,0,0,0,0,0,0,0,0,224,48,204,16,32,64,128,0,0,0,0,3,4,132,131,252,64,32,144,79,35,144,127,0,0,0,0,0,0,0,2,6,10,18,33,35,36,68,72,73,66,64,60,75,73,73,73,37,37,36,36,18,17,9,4,2,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,128,128,64,32,32,16,16,8,0,28,34,42,34,28,196,52,12,4,194,242,250,122,36,24,0,0,240,8,8,136,104,24,136,68,66,81,88,68,64,68,73,74,146,36,36,36,40,72,64,66,1,8,36,35,19,147,147,74,42,42,26,12,1,6,24,255,0,0,251,244,4,8,8,136,200,224,240,248,249,252,252,126,62,30,12,52,68,134,218,33,1,0,0,0,0,0,0,0,0,0,0,0,15,16,33,71,152,0,0,31,127,255,255,255,255,1,152,228,130,26,6,98,28,200,48,16,208,48,16,104,24,136,80,32,0,0,0,0,0,0,0,0,0,1,2,2,4,4,9,11,31,31,28,16,16,17,17,51,42,46,68,92,100,2,2,1,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,128,64,32,160,144,8,4,250,198,50,248,0,0,0,0,0,0,0,0,0,0,128,128,128,192,32,16,16,8,4,4,2,130,66,34,15,16,96,140,17,17,16,192,33,24,6,1,0,0,0,0,0,0,0,0,0,135,104,16,15,128,64,32,16,8,4,130,193,224,240,254,113,49,25,29,15,3,1,0,0,0,0,0,64,160,96,32,160,118,137,21,50,201,68,226,97,112,176,120,28,30,35,65,33,31,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,1,6,25,100,81,63,0,0,0,1,1,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,28,226,2,34,82,36,136,80,224,64,128,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,3,28,52,202,9,12,2,5,24,96,129,2,4,8,112,160,32,64,128,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,62,68,40,16,32,193,134,24,32,192,7,56,224,25,6,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,15,17,18,12,8,17,102,152,161,70,216,96,64,128,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,15,50,77,82,61,10,12,9,6,0]),fish_spr_1.x,fish_spr_1.y,fish_spr_1.key,fish_spr_1.mirrorX,fish_spr_1.mirrorY)
    fish_spr_1.key = 0
    fish_spr_1.x = 36
    fish_spr_1.setFrame(int(fish_ID) - 1)
    display.drawSprite(fish_spr_1)
  elif int(fish_ID) > 4 and int(fish_ID) <= 8:
    fish_spr_2 = Sprite(36,40,bytearray([0,0,0,224,24,36,148,148,20,100,8,244,4,100,244,148,104,8,240,176,96,192,128,0,128,128,0,0,0,0,0,0,0,0,0,0,8,144,80,78,33,161,166,24,241,1,15,16,32,18,130,130,66,193,112,175,85,170,85,255,132,128,121,7,0,0,0,0,0,0,0,0,0,3,14,9,25,20,20,18,16,15,24,97,129,5,24,96,130,3,6,140,121,2,85,170,255,3,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,62,33,17,14,8,124,65,33,25,32,67,93,170,181,110,24,16,72,132,132,148,100,20,12,4,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,31,96,20,8,4,3,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,3,3,5,5,137,138,82,34,4,200,48,32,48,72,80,160,32,32,32,192,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,2,3,2,2,2,1,1,9,21,19,18,10,4,8,49,194,7,248,192,128,128,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,192,192,64,112,48,48,16,24,24,8,136,8,198,131,193,96,31,8,8,7,0,0,0,0,0,0,192,32,144,144,8,12,20,23,35,193,1,24,184,240,140,216,230,108,99,118,49,27,12,6,1,0,0,0,0,0,32,48,40,36,38,83,80,144,177,40,72,68,138,138,4,5,6,4,4,8,16,16,16,17,18,18,20,24,0,0,0,0,0,0,0,0,0,128,64,192,64,224,32,48,200,72,48,64,64,32,32,96,96,160,160,160,160,96,32,160,96,64,192,64,64,128,0,0,0,0,0,0,0,7,24,227,68,128,1,1,0,0,0,0,128,64,160,30,32,72,128,0,32,113,33,2,6,9,52,82,201,47,240,0,0,0,0,0,24,38,33,17,10,204,57,193,1,33,1,15,16,72,232,71,0,0,15,48,64,130,0,16,56,16,128,0,192,63,0,0,0,0,0,0,0,0,0,0,0,7,58,73,165,146,204,164,152,208,176,144,208,176,82,80,112,80,33,33,34,194,68,192,35,90,150,20,20,132,104,16,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,3,28,17,18,8,4,4,2,1,0,0,0,0,0,0,0,0,0,0,0,0,0,193,191,129,66,36,40,48,32,32,32,32,32,32,32,32,32,64,64,64,128,128,0,0,0,0,0,0,0,0,0,128,128,224,144,140,66,65,64,64,64,64,32,32,32,112,176,176,240,30,241,208,208,208,236,210,210,172,145,10,10,4,4,6,230,85,77,36,36,252,228,252,248,248,248,248,248,248,248,120,120,124,63,63,63,127,92,139,31,47,207,7,7,3,3,1,1,0,0,0,0,0,0,0,0,0,7,239,31,63,255,227,205,148,184,96,16,8,8,196,52,12,4,0,1,2,4,9,30,48,0,0,0,0,0,0,0,0,0,0,0,128,126,49,12,3,0,3,4,3,3,4,24,32,65,126,128,0,0,0,0,0,0,0,0,0,0,0,0,0]),fish_spr_2.x,fish_spr_2.y,fish_spr_2.key,fish_spr_2.mirrorX,fish_spr_2.mirrorY)
    fish_spr_2.key = 0
    fish_spr_2.x = 36
    fish_spr_2.setFrame(int(fish_ID) - 1)
    display.drawSprite(fish_spr_2)
  elif int(fish_ID) > 8 and int(fish_ID) <= 12:
    fish_spr_3 = Sprite(36,40,bytearray([0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,128,64,32,16,16,8,4,252,4,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,128,64,32,16,8,8,4,4,2,142,1,128,0,64,128,0,0,0,1,2,2,4,4,8,8,16,16,32,32,64,128,0,0,60,98,97,96,232,104,224,96,224,98,23,39,16,224,192,193,206,192,231,0,0,0,0,0,0,28,32,64,192,128,128,128,0,0,255,0,0,0,0,0,0,0,0,0,0,7,8,12,6,3,3,17,16,40,40,41,73,73,74,18,148,24,40,208,144,97,35,39,44,50,33,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,128,192,188,67,32,16,15,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,128,224,80,168,88,168,88,168,88,168,80,176,96,192,128,0,0,24,52,60,88,160,64,128,128,128,64,160,80,44,30,26,12,0,0,254,85,186,71,145,173,137,117,169,83,134,61,234,85,170,85,175,214,107,62,4,3,0,49,192,0,224,17,22,40,80,96,0,0,0,32,48,43,38,77,90,117,106,117,106,85,90,76,75,141,134,131,129,128,128,64,64,32,32,31,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,192,224,204,50,242,250,121,61,61,253,253,253,189,61,57,57,58,122,114,242,244,244,228,228,200,200,144,16,32,192,0,0,0,0,0,31,127,255,255,62,89,243,224,0,0,0,1,3,3,2,0,0,0,0,0,0,0,1,131,255,255,255,127,0,128,127,0,0,0,0,0,0,0,0,1,3,0,0,1,128,192,192,224,224,240,240,240,248,120,120,124,60,62,159,143,71,35,17,8,6,1,0,0,0,0,0,0,0,0,0,0,0,240,254,255,63,15,199,35,19,9,9,4,132,66,66,33,17,137,196,226,242,242,242,242,226,132,24,32,192,0,0,0,0,0,0,0,0,7,15,31,62,124,120,113,114,114,113,121,60,60,62,31,31,15,7,7,1,0,0,1,3,7,4,8,7,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,192,32,144,140,228,136,136,208,144,224,128,192,160,160,144,80,80,72,72,40,40,136,104,16,0,0,0,0,0,0,128,96,16,136,4,30,55,107,213,170,85,170,85,170,85,170,245,63,232,82,82,162,164,36,68,64,6,153,112,0,0,0,0,0,0,3,4,8,9,18,17,32,32,32,255,10,197,10,77,154,109,30,39,74,138,145,16,16,224,1,1,2,2,7,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,3,2,1,1,0,0,0,0,0,0,0,1,2,1,0,0,0,0,0,0,0,0,0,0]),fish_spr_3.x,fish_spr_3.y,fish_spr_3.key,fish_spr_3.mirrorX,fish_spr_3.mirrorY)
    fish_spr_3.key = 0
    fish_spr_3.x = 36
    fish_spr_3.setFrame(int(fish_ID) - 1)
    display.drawSprite(fish_spr_3)
  elif int(fish_ID) > 12 and int(fish_ID) <= 16:
    fish_spr_4 = Sprite(36,40,bytearray([0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,16,32,64,128,192,240,56,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,56,70,132,72,48,0,0,0,0,0,224,252,63,23,16,8,8,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,2,2,3,6,12,24,112,224,248,127,15,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,192,240,254,159,67,64,32,32,48,40,4,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,128,224,248,60,15,7,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,128,192,96,240,208,240,160,192,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,128,64,160,80,168,87,45,31,27,15,6,3,1,0,0,0,0,0,0,0,0,0,128,96,16,136,196,116,204,64,160,80,168,84,42,21,10,5,2,1,0,0,0,0,0,0,0,0,0,0,224,24,8,4,4,4,226,177,120,92,238,247,251,116,180,79,74,41,24,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,3,12,16,32,32,64,192,163,191,95,95,35,29,2,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,16,40,72,136,8,8,8,4,4,4,196,36,36,196,4,8,8,144,16,32,64,128,0,0,0,0,0,0,0,0,0,0,0,0,0,8,24,40,72,72,137,138,132,0,0,0,0,129,129,128,64,68,34,33,16,24,36,194,1,2,4,12,20,100,136,8,176,192,0,0,0,0,0,0,0,0,0,0,0,1,1,97,147,10,4,2,0,128,112,0,0,0,0,128,127,0,0,0,0,128,127,3,0,0,0,0,0,0,0,0,0,0,0,0,0,224,16,32,32,161,33,33,127,128,160,144,136,132,67,64,32,48,40,40,20,15,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,3,4,10,17,32,48,40,70,64,79,80,32,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,4,26,98,138,10,18,18,20,148,164,168,40,240,96,184,100,180,98,162,121,163,100,200,240,128,0,0,0,0,0,0,0,0,0,0,0,0,28,230,129,144,81,73,41,40,20,84,186,143,253,170,85,170,85,170,85,170,245,26,13,119,137,6,53,37,137,118,0,0,0,0,0,0,0,1,0,0,0,0,120,132,68,36,34,18,9,7,27,38,83,66,177,194,63,8,8,8,4,5,3,1,128,0,0,0,0,176,240,176,240,0,128,128,128,0,0,0,0,0,128,192,192,128,0,240,80,112,208,112,80,240,0,0,248,168,168,248,175,168,248,0,0,170,255,170,255,0,255,204,255,0,0,0,254,235,251,43,251,235,251,254,1,255,221,247,213,255,0,254,246,214,222,254,0,255,255,0,0]),fish_spr_4.x,fish_spr_4.y,fish_spr_4.key,fish_spr_4.mirrorX,fish_spr_4.mirrorY)
    fish_spr_4.key = 0
    fish_spr_4.x = 36
    fish_spr_4.setFrame(int(fish_ID) - 1)
    display.drawSprite(fish_spr_4)

def eval_screen():
  global can_catch, rand_wait, exit_nav, fish_size_rec_var, fish_qty_rec_var
  gc.collect()
  if can_catch == 0:
    if int(saveData.getItem('sound_setting')) == 1:
      audio.play(587, 250)
    display.drawText(str('Wait for'), 5, 5, 1)
    display.drawText(str('a bite'), 5, 15, 1)
    display.drawText(str('first!'), 5, 25, 1)
    display.update()
    display.fill(0)
    rand_wait = (rand_wait if isinstance(rand_wait, Number) else 0) + 1
    time.sleep(1.5)
    fishing_screen()
  elif can_catch == 1:
    display.setFont("/lib/font5x7.bin", 5, 7, display.textSpaceWidth)
    display.drawText(str('Too early!'), 5, 2, 1)
    display.drawText(str('It got'), 5, 14, 1)
    display.drawText(str('away... :('), 5, 24, 1)
    display.setFont("/lib/font3x5.bin", 3, 5, display.textSpaceWidth)
    display.drawText(str('A: AGAIN  B: MENU'), 2, 35, 1)
    display.update()
    display.fill(0)
    display.setFont("/lib/font5x7.bin", 5, 7, display.textSpaceWidth)
    if int(saveData.getItem('sound_setting')) == 1:
      audio.playBlocking(587, 200)
      audio.play(554, 150)
  elif can_catch == 2:
    pick_fish()
    display_caught_fish()
  elif can_catch == 3:
    display.setFont("/lib/font5x7.bin", 5, 7, display.textSpaceWidth)
    display.drawText(str('Too late!'), 5, 2, 1)
    display.drawText(str('Better luck'), 5, 14, 1)
    display.drawText(str('next time...'), 5, 24, 1)
    display.setFont("/lib/font3x5.bin", 3, 5, display.textSpaceWidth)
    display.drawText(str('A: AGAIN  B: MENU'), 2, 35, 1)
    display.update()
    display.fill(0)
    display.setFont("/lib/font5x7.bin", 5, 7, display.textSpaceWidth)
    if int(saveData.getItem('sound_setting')) == 1:
      audio.playBlocking(587, 200)
      audio.playBlocking(554, 200)
      audio.play(523, 275)
  while True:
    if buttons.buttonA.justPressed():
      # 0: go directly to biome select
      # 1: go back to main menu
      exit_nav = 0
      break
    elif buttons.buttonB.justPressed():
      exit_nav = 1
      break
  fish_qty_rec_var = 0
  fish_size_rec_var = 0

setup_all_fish()
font5x6_sprite = Sprite(95,40,bytearray([0,0,0,0,0,0,0,47,0,0,0,3,0,3,0,10,31,10,31,10,36,42,63,42,18,33,16,12,2,33,22,41,45,18,40,0,0,3,0,0,0,0,30,33,0,0,0,33,30,0,0,10,4,10,0,8,8,62,8,8,0,32,16,0,0,0,4,4,4,0,0,0,32,0,0,32,16,12,2,1,28,50,41,37,30,0,34,33,63,32,36,50,41,41,38,
           18,33,37,37,26,8,12,10,63,8,23,37,37,37,25,30,41,37,37,24,3,41,25,13,10,22,41,37,38,24,4,42,41,41,30,0,0,18,0,0,0,32,18,0,0,0,8,20,34,0,0,20,20,20,0,0,34,20,8,0,2,1,41,5,2,30,41,21,29,22,32,16,24,21,63,33,63,37,37,26,28,34,33,37,34,33,61,33,33,30,1,63,37,37,49,
           1,63,9,9,3,30,33,33,43,24,33,63,4,37,63,0,33,63,33,0,16,35,33,31,1,33,63,12,18,33,1,63,32,32,48,63,4,24,5,63,1,63,4,25,63,30,33,33,33,30,1,61,9,9,6,30,33,41,17,46,1,61,9,25,38,34,37,37,41,19,2,33,63,1,1,1,31,32,33,31,1,31,32,25,7,31,32,28,33,31,33,51,12,45,51,
           1,3,36,61,3,35,49,41,37,51,0,0,63,33,0,1,2,12,16,32,0,0,33,63,0,4,2,1,2,4,32,32,32,32,32,0,0,1,2,0,24,36,34,62,34,33,63,36,36,24,24,36,34,34,36,24,36,36,63,33,28,50,42,36,16,40,62,9,1,2,4,42,42,30,2,33,63,4,34,60,0,4,61,32,0,0,16,32,36,29,0,33,63,8,54,
           0,1,63,32,0,62,2,28,2,60,2,62,4,2,60,24,36,34,34,28,0,62,20,18,14,0,8,20,18,46,4,56,4,2,4,0,36,42,42,18,0,5,63,36,0,2,30,32,32,30,2,14,48,16,14,30,32,28,32,30,34,54,8,54,34,2,6,40,42,30,0,50,42,42,38,0,26,37,0,0,0,0,63,0,0,0,0,37,26,0,24,4,8,16,12]), font5x6_sprite.x,font5x6_sprite.y,font5x6_sprite.key,font5x6_sprite.mirrorX,font5x6_sprite.mirrorY)
from sys import path
if not '/Games/FishPond' in path:
  path.append( '/Games/FishPond' )
import environments
display.setFPS(30)
cast_pwr = 0
counter = 0
if saveData.hasItem('fish_size_record') == False:
  saveData.setItem('fish_size_record', [0] * len(list_all_fish))
  saveData.save()
if saveData.hasItem('fish_qty_record') == False:
  saveData.setItem('fish_qty_record', [0] * len(list_all_fish))
  saveData.save()
if saveData.hasItem('completion_record') == False:
  saveData.setItem('completion_record', 0)
  saveData.save()
while True:
  title_screen()