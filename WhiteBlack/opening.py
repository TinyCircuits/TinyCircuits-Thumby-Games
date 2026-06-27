# opening.py  -- opening animations (fast, buffer-based)
import thumby
import time

# constants replicated (small)
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

def animate_words_slide_back(start_left_x, start_right_x):
    white_x = start_left_x
    black_x = start_right_x
    target_white_x = 0
    target_black_x = SCREEN_W - CHAR_W
    total_steps = abs(start_left_x - target_white_x)
    buf = thumby.display.display.buffer

    for _ in range(total_steps):
        thumby.display.fill(0)
        restore_end = white_x + CHAR_W
        if restore_end > 0:
            for row in range(0, SCREEN_H, 8):
                row_base = (row // 8) * SCREEN_W
                for xx in range(min(restore_end, SCREEN_W)):
                    buf[row_base + xx] = 0xFF
        draw_vertical_word(LEFT_WORD_1, white_x, invert=True)
        draw_vertical_word(LEFT_WORD_2, black_x)
        thumby.display.update()
        white_x -= 1
        black_x += 1
        time.sleep(0.005)

    # final static
    thumby.display.fill(0)
    for row in range(0, SCREEN_H, 8):
        row_base = (row // 8) * SCREEN_W
        for xx in range(CHAR_W):
            buf[row_base + xx] = 0xFF
    draw_vertical_word(LEFT_WORD_1, 0, invert=True)
    draw_vertical_word(LEFT_WORD_2, target_black_x)
    thumby.display.update()

def animate_words_meet_adjacent():
    white_x = 0
    black_x = SCREEN_W - CHAR_W
    target_white_x = (SCREEN_W - (2 * CHAR_W)) // 2
    target_black_x = target_white_x + CHAR_W
    steps = abs(target_white_x - white_x)
    buf = thumby.display.display.buffer

    for _ in range(steps):
        thumby.display.fill(0)
        white_fill_end = white_x + CHAR_W
        if white_fill_end > 0:
            left = 0
            right = min(SCREEN_W, white_fill_end)
            for row in range(0, SCREEN_H, 8):
                row_base = (row // 8) * SCREEN_W
                for xx in range(left, right):
                    buf[row_base + xx] = 0xFF
        draw_vertical_word(LEFT_WORD_1, white_x, invert=True)
        draw_vertical_word(LEFT_WORD_2, black_x)
        thumby.display.update()
        white_x += 1
        black_x -= 1
        time.sleep(0.005)

    thumby.display.fill(0)
    white_fill_end = target_white_x + CHAR_W
    if white_fill_end > 0:
        left = 0
        right = min(SCREEN_W, white_fill_end)
        for row in range(0, SCREEN_H, 8):
            row_base = (row // 8) * SCREEN_W
            for xx in range(left, right):
                buf[row_base + xx] = 0xFF
    draw_vertical_word(LEFT_WORD_1, target_white_x, invert=True)
    draw_vertical_word(LEFT_WORD_2, target_black_x)
    thumby.display.update()

    animate_words_slide_back(target_white_x, target_black_x)

def run_opening():
    # small entry point which defines nothing new at import-time
    animate_words_meet_adjacent()
    
    # reveal lines
    line1 = "buyme"
    line2 = "acoffee"
    line3 = "/gea3w6orn"
    base_x = CHAR_W + 4
    y1 = 5
    y2 = y1 + CHAR_H + 2
    y3 = y2 + CHAR_H + 2
    line3_x = max(CHAR_W, base_x - 4)
    thumby.display.drawText(line1, base_x, y1, 1)
    thumby.display.update()
    time.sleep(0.50)
    thumby.display.drawText(line2, base_x, y2, 1)
    thumby.display.update()
    time.sleep(0.50)
    thumby.display.drawText(line3, line3_x, y3, 1)
    thumby.display.update()
    time.sleep(0.50)
    
    while not thumby.buttonA.justPressed():
        time.sleep(0.01)
    
    animate_words_meet_adjacent()
    # animate_second_cycle (fast) mirrors what you had originally
    # but calling animate_words_slide_back inside animate_words_meet_adjacent
