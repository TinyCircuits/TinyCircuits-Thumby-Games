import thumby
import gc
import json
from sys import path
path.append("/Games/Thelda")
# import thumbyHardware
import fonthandler
from player import Player
gc.collect()
from enemycontroller import EnemyController
gc.collect()
from scenecontroller import SceneController
gc.collect()
from hudcontroller import HudController
gc.collect()


# Set framerate
thumby.display.setFPS(20) # set frame rate

# # Set tiny, almost unreadable font
font_handler = fonthandler.FontHandler()
gc.collect()

# Create Scene Controller
scene_controller = SceneController()
gc.collect()

#Create enemy controller
enemy_controller = EnemyController()
gc.collect
# from musicplayer import MusicPlayer

def loadgame():
    with open("/Games/Thelda/save.json", 'r') as savefile:
        thisdata = json.load(savefile)
        return thisdata

title_screen = bytearray([0,252,14,246,26,234,234,234,106,106,106,234,106,234,106,234,106,234,234,234,234,106,234,234,234,106,234,234,234,106,106,234,234,106,234,234,234,106,106,234,234,106,106,234,234,234,106,106,106,234,106,106,106,234,234,234,234,234,234,234,234,234,234,234,234,234,234,26,22,14,252,0,
           0,255,0,255,0,255,255,255,159,164,183,55,244,246,52,55,52,4,5,207,247,52,5,197,63,196,244,53,7,196,13,244,247,20,20,21,7,204,7,244,7,12,253,254,7,247,244,53,52,103,204,30,63,255,7,247,23,23,55,199,15,63,255,255,255,255,255,0,0,0,255,0,
           0,255,0,255,0,255,255,255,207,147,156,159,135,224,248,199,153,158,159,135,227,243,194,146,158,143,129,224,198,152,159,159,145,145,145,128,230,192,158,159,152,152,155,155,131,128,199,158,152,153,152,159,192,224,192,159,156,132,229,228,223,152,128,135,255,255,255,0,0,0,255,0,
           0,255,254,253,251,250,120,184,216,184,120,248,248,248,248,248,248,248,248,248,248,56,184,56,248,56,184,120,248,56,184,184,248,56,184,184,248,56,184,184,248,248,248,248,248,56,248,120,184,120,248,56,248,248,248,248,248,248,248,248,248,120,184,216,184,120,248,248,252,254,255,0,
           0,63,127,119,115,116,118,116,114,116,118,116,115,119,127,127,127,127,127,127,127,120,126,126,127,120,126,121,127,120,122,123,127,122,122,120,127,122,122,120,127,127,127,127,127,127,127,120,126,120,127,127,127,127,127,127,127,127,119,115,116,118,116,114,116,118,116,115,119,127,63,0])

gc.collect()

menu = True
menu2 = False
while menu:
    thumby.display.fill(0)
    thumby.display.blit(title_screen, 0, 0, 72, 40, -1, 0, 0)
    playing = False
    start_button_pressed = thumby.buttonA.justPressed()
    if start_button_pressed:
        # playing = True
        menu2 = True
        menu = False
        arrow_position_y = 19
        gc.collect()
    else: menu = True
    
    thumby.display.update()
    
while menu2:
    thumby.display.fill(1)
    thumby.display.drawText("New Game", 10, 17, 0)
    thumby.display.drawText("Load Game", 10, 25, 0)
    arrow = bytearray([0,0,5])
    thumby.display.blit(arrow, 6, arrow_position_y, 3, 3, -1, 0, 0)
    if arrow_position_y == 19:
        if thumby.dpadJustPressed():
            arrow_position_y = 27
            thumby.display.blit(arrow, 6, arrow_position_y, 3, 3, -1, 0, 0)
    else:
        if arrow_position_y == 27:
            if thumby.dpadJustPressed():
                arrow_position_y = 19
                thumby.display.blit(arrow, 6, arrow_position_y, 3, 3, -1, 0, 0)
    if thumby.buttonA.justPressed():
        if arrow_position_y == 19:
            savedata = [6, 6, 0, 0, 0, True, [], []]
            menu2 = False
            playing = True
        else:
            try:
                savedata = loadgame()
            except:
                savedata = [6, 6, 0, 0, 0, True, [], []]
            else:
                scene_controller.isDangerous = savedata[5]
                scene_controller.doors_unlocked = savedata[6]
                scene_controller.keys_used = savedata[7]
                gc.collect()
            menu2 = False
            playing = True
        print(savedata)
    thumby.display.update()
                

my_player = Player(enemy_controller, scene_controller, thumby, savedata)
gc.collect()

#Create HudController
hud_controller = HudController(my_player)

gc.collect()

# music_player = MusicPlayer()
# Begin main game loop that runs for the course of the game
while playing:
    # allocmem = gc.mem_alloc()
    # freemem = gc.mem_free()
    
    # music_player.play_song()
    thumby.display.fill(1) # Fill canvas to white
    scene_controller.build_scene(scene_controller.scene_x, scene_controller.scene_y, font_handler, thumby.display, enemy_controller)
    enemy_controller.populate_enemies(scene_controller)
    enemy_controller.move_enemies(scene_controller)
    enemy_controller.attack(my_player)
    enemy_controller.display_loot(my_player, enemy_controller, thumby.display)
    if not my_player.swinging:
        my_player.move_player(scene_controller, enemy_controller, thumby, json)
        my_player.use_item(enemy_controller, thumby)
    if not scene_controller.isDangerous:
        my_player.swing_sword(enemy_controller, thumby)
    hud_controller.display_hearts(my_player)
    hud_controller.display_rupees(font_handler, my_player)
    hud_controller.display_keys(font_handler, my_player)
    hud_controller.display_bombs(font_handler, my_player)
    hud_controller.pause_game(font_handler, my_player)
    my_player.hit_detection(enemy_controller, thumby)
    my_player.death(thumby.display)
    # print(f"Memory Allocated: {allocmem}")
    # print(f"Memory Free: {freemem}")
    # print(f"Keys used: {scene_controller.keys_used}")
    thumby.display.update()
    