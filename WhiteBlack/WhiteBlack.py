# main.py  -- lightweight launcher / menu
import thumby
import gc
import time
import sys

CURRENT_FOLDER = '/Games/WhiteBlack'
sys.path.insert(1, CURRENT_FOLDER)

# small shared constants
SCREEN_W = 72
SCREEN_H = 40
CHAR_W = 6
CHAR_H = 8

LEFT_WORD_1 = "White"
LEFT_WORD_2 = "Black"

def draw_vertical_word(word, x, invert=False):
    total_h = len(word) * CHAR_H
    y0 = (SCREEN_H - total_h) // 2
    if invert:
        thumby.display.drawFilledRectangle(x, y0, CHAR_W, total_h, 1)
        color = 0
    else:
        color = 1
    for i, c in enumerate(word):
        thumby.display.drawText(c, x, y0 + i * CHAR_H, color)

def run_menu():
    selected = 0
    while True:

        thumby.display.fill(0)
        draw_vertical_word(LEFT_WORD_1, 0, invert=True)
        draw_vertical_word(LEFT_WORD_2, SCREEN_W - CHAR_W)

        # menu text
        options = ["Start", "Quit"]
        total_menu_h = (len(options) * CHAR_H) + (len(options) - 1) * 6
        menu_y0 = (SCREEN_H - total_menu_h) // 2
        for i, text in enumerate(options):
            text_x = (SCREEN_W - len(text) * CHAR_W) // 2
            text_y = menu_y0 + i * (CHAR_H + 6)
            thumby.display.drawText(text, text_x, text_y, 1)
            if i == selected:
                thumby.display.drawText(">", text_x - 8, text_y, 1)
        thumby.display.update()

        # Use Up / Down instead of B
        if thumby.buttonU.justPressed():
            selected = (selected - 1) % len(options)
            time.sleep(0.12)
        if thumby.buttonD.justPressed():
            selected = (selected + 1) % len(options)
            time.sleep(0.12)

        # Select with A
        if thumby.buttonA.justPressed():
            if selected == 0:
                return "start"
            else:
                # show credits
                thumby.display.fill(0)
                
                text1 = "github.com"
                text2 = "/b-mf-a"
                
                # calculate total block height (two lines + small spacing)
                spacing = 2
                total_h = (CHAR_H * 2) + spacing
                
                # starting y so text block is vertically centered
                start_y = (SCREEN_H - total_h) // 2
                
                # centered x positions
                x1 = (SCREEN_W - len(text1) * CHAR_W) // 2
                x2 = (SCREEN_W - len(text2) * CHAR_W) // 2
                
                # draw centered text
                thumby.display.drawText(text1, x1, start_y, 1)
                thumby.display.drawText(text2, x2, start_y + CHAR_H + spacing, 1)

                thumby.display.update()

                time.sleep(5)
                
                # return to the Thumby menu
                thumby.reset()
                
                #return "credits"

        time.sleep(0.01)


# main loop
import opening      # lazy-loaded module; small import
import game
import closing
gc.collect()
#try:
while True:
    choice = run_menu()
    gc.collect()
    if choice == "start":
        # run opening animations
        try:
            opening.run_opening()
        except Exception:
            # if anything fails, continue to game
            pass
        gc.collect()
        # run game
        try:
            res = game.run_game()
        except Exception as e:
            # show small error and stop
            thumby.display.fill(0)
            thumby.display.drawText("ERR", 1, 1, 1)
            thumby.display.update()
            time.sleep(1.0)
            break
        gc.collect()
        if res == "quit":
            try:
                closing.run_closing()
            except Exception:
                pass
        gc.collect()
        
    else:
        # credits chosen already shown in run_menu
        pass
'''
except Exception:
    # fatal fallback
    thumby.display.fill(0)
    thumby.display.drawText("BOOTERR", 1, 1, 1)
    thumby.display.update()
    while True:
        time.sleep(0.2)
    '''